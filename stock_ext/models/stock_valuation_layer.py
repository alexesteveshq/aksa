# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    product_id = fields.Many2one(ondelete='cascade')
