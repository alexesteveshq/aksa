# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    additional_cost = fields.Float(string='Additional Cost')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    additional_cost = fields.Float(related='order_id.additional_cost', store=True)
