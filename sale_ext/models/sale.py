# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode=''):
        piece = self.env['product.product'].search([('barcode', '=', barcode.upper())], limit=1)
        if piece.qty_available == 0:
            raise UserError(_('Scanned piece with barcode %s is not available.') % barcode)
        if piece:
            self.order_line = [(0, 0, {'product_id': piece.id,
                                       'product_uom_qty': 1})]
        else:
            raise UserError(_('Scanned piece with barcode %s does not exist.') % barcode)

    lot_discount_ids = fields.One2many('lot.discount', 'order_id', string='Lot discount')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    piece_lot_it = fields.Many2one(related='product_id.lot_id')
    barcode = fields.Char(related='product_id.barcode')
    weight = fields.Float(related='product_id.weight')
    average_price_gram = fields.Float(string='Avg. Price per gram', compute='_compute_average_price_gram', store=True)
    avg_price_calc = fields.Float(string='Avg. Price calc')
    discount = fields.Float()

    def _convert_to_tax_base_line_dict(self):
        result = super(SaleOrderLine, self)._convert_to_tax_base_line_dict()
        result['weight'] = self.weight
        return result

    @api.onchange('avg_price_calc')
    def onchange_avg_price_calc(self):
        for line in self:
            line.price_unit = line.avg_price_calc * line.weight

    @api.depends('product_id', 'product_id.weight')
    def _compute_average_price_gram(self):
        for line in self:
            if line.product_id and not line.average_price_gram:
                line.average_price_gram = round(line.price_subtotal / (line.product_id.weight or 1), 2)
            else:
                line.average_price_gram = 0

    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.lot_discount_ids',
                 'order_id.lot_discount_ids.lot_id', 'order_id.lot_discount_ids.value')
    def _compute_discount(self):
        super(SaleOrderLine, self)._compute_discount()
        for line in self:
            disc_line = line.order_id.lot_discount_ids.filtered(lambda disc: disc.lot_id == line.product_id.lot_id)
            if disc_line:
                line.discount = disc_line[0].value
