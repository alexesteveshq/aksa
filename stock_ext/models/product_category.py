# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockProductCategory(models.Model):
    _name = 'stock.product.category'
    _description = 'Product Category'

    name = fields.Char(string='Name')
