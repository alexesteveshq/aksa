# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def print_sticker(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                move.product_id.print_sticker()
