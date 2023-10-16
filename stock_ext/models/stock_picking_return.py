# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockReturnPickingLine(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    product_barcode = fields.Char(related='product_id.barcode')
