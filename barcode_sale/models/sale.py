# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import _, models, fields
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
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
