# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _prepare_tax_totals(self, base_lines, currency, tax_lines=None):
        result = super(AccountTax, self)._prepare_tax_totals(base_lines, currency, tax_lines)
        result['weight'] = round(sum([line['weight'] for line in base_lines]), 2)
        return result
