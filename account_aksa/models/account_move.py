# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _stock_account_prepare_anglo_saxon_out_lines_vals(self):
        res = super(AccountMove, self)._stock_account_prepare_anglo_saxon_out_lines_vals()
        for line in res:
            if 'analytic_distribution' in line:
                product = self.env['product.product'].browse(line['product_id'])
                total_tax = (line['amount_currency'] * product.taxes_id.amount) / 100
                untaxed_amount = line['amount_currency'] - total_tax
                res.append({
                    'name': product.taxes_id.name,
                    'move_id': line['move_id'],
                    'partner_id': line['partner_id'],
                    'product_id': line['product_id'],
                    'quantity': 1,
                    'amount_currency': total_tax,
                    'tax_ids': [],
                    'display_type': 'cogs',
                    'account_id': product.categ_id.property_account_tax_categ_id.id,
                })
                line.update({'amount_currency': untaxed_amount})
        return res
