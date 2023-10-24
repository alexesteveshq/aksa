# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_account_tax_categ_id = fields.Many2one('account.account', string='Tax Account')
