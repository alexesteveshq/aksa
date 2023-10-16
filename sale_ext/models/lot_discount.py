# -*- coding: utf-8 -*-

from odoo import fields, models


class LotDiscount(models.Model):
    _name = 'lot.discount'
    _description = 'Lot Discount'

    order_id = fields.Many2one('sale.order', string='Order')
    lot_id = fields.Many2one('stock.lot', string='Lot')
    value = fields.Float(string='Value')
