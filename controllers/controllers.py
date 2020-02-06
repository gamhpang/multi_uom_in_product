# -*- coding: utf-8 -*-
# from odoo import http


# class MultiUomInProduct(http.Controller):
#     @http.route('/multi_uom_in_product/multi_uom_in_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/multi_uom_in_product/multi_uom_in_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('multi_uom_in_product.listing', {
#             'root': '/multi_uom_in_product/multi_uom_in_product',
#             'objects': http.request.env['multi_uom_in_product.multi_uom_in_product'].search([]),
#         })

#     @http.route('/multi_uom_in_product/multi_uom_in_product/objects/<model("multi_uom_in_product.multi_uom_in_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('multi_uom_in_product.object', {
#             'object': obj
#         })
