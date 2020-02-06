# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api , _ 

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	def _get_category_id(self):
		res = self.env["uom.uom"].search([],limit=1,order='id')
		return res.category_id

	@api.depends('category_id')
	def _get_multi_uom_product(self):
		res = self.env["uom.uom"].search([('category_id','=',self.category_id.id)])
		return res

	category_id = fields.Many2one('uom.category','Category',default=_get_category_id)
	multi_uom_product = fields.Many2many("uom.uom",string=" Related Units of Measure",default=_get_multi_uom_product)
	for_domain = fields.Many2many("uom.uom",'for_domain_rel',string="For domain",copy=False)

	@api.onchange('uom_id')
	def _onchange_uom_id(self):		
		self.category_id = self.uom_id.category_id
		res = self.env["uom.uom"].search([('category_id','=',self.category_id.id)])
		self.multi_uom_product = self.uom_id
		self.for_domain = res

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	multi_uom_product = fields.Many2many("uom.uom",string="Units of Measure",store=True)
	product_uom = fields.Many2one('uom.uom',string='Unit of Measure')

	@api.onchange('product_id')
	def product_id_change(self):
		
		self.multi_uom_product = self.product_id.multi_uom_product

		if not self.product_id:
			return
		valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids

		for pacv in self.product_custom_attribute_value_ids:
			if pacv.custom_product_template_attribute_value_id_id not in valid_values:
				self.product_custom_attribute_value_ids -= pacv

		for ptav in self.product_no_variant_attribute_value_ids:
			if ptav._origin not in valid_values:
				self.product_no_variant_attribute_value_ids -= ptav

		vals = {}
		if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
			if len(self.product_id.multi_uom_product) > 0 :
				vals['product_uom'] = self.product_id.multi_uom_product[0]
				vals['multi_uom_product'] = self.product_id.multi_uom_product
			else :
				vals['product_uom'] = self.product_id.uom_id
				vals['multi_uom_product'] = self.product_id.uom_id
			vals['product_uom_qty'] = self.product_uom_qty or 1.0

		product = self.product_id.with_context(
			lang = self.order_id.partner_id.lang,
			partner = self.order_id.partner_id,
			quantity = vals.get('product_uom_qty') or self.product_uom_qty,
			date = self.order_id.date_order,
			pricelist = self.order_id.pricelist_id.id,
			uom=self.product_uom.id
		)

		vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

		self._compute_tax_id()

		if self.order_id.pricelist_id and self.order_id.partner_id :
			vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
		self.update(vals)
		