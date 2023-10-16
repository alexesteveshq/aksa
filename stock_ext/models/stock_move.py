# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_id = fields.Many2one(ondelete='cascade')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_barcode = fields.Char(related='product_id.barcode')

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super(StockMoveLine, self)._get_aggregated_product_quantities(**kwargs)
        for key in result.keys():
            result[key]['barcode'] = result[key]['product'].barcode
        return result

    def print_sticker_retail(self):
        prod_model = self.env['product.product']
        for move in self:
            piece = prod_model.sudo().search([('barcode', '=', move.product_id.barcode)])
            piece.sudo().print_sticker(retail=True)
