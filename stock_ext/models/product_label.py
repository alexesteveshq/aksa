# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockProductLabel(models.Model):
    _name = 'stock.product.label'
    _description = 'Product Label'

    name = fields.Char(string='Name')
