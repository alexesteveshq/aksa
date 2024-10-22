# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockProductCategory(models.Model):
    _name = 'stock.product.category'
    _description = 'Product Category'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')

    @api.model_create_multi
    def create(self, vals_list):
        result = super(StockProductCategory, self).create(vals_list)
        for categ in result:
            if categ.name:
                categ.code = categ.name.lower().replace(" ", "_")
        return result
