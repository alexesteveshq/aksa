# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_id = fields.Many2one(ondelete='cascade')
    barcode = fields.Char(related='product_id.barcode', store=True)
