# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
import csv
import io
import base64
import pytz


class BalanceAmountsWizard(models.TransientModel):
    _name = 'balance.amounts.wizard'
    _description = 'Balance Amounts Wizard'

    balance_attachment = fields.Binary(string='Balance attachment')

    @staticmethod
    def format_number(number):
        try:
            result = float(number.replace('$', '').replace('.', '').replace(',,', '.'))
            return result
        except Exception as e:
            return 0

    def balance_amounts(self):
        string_io = io.StringIO(base64.b64decode(self.balance_attachment).decode('utf-8'))
        csv_reader = csv.reader(string_io, delimiter=' ')
        orders = self.env['pos.order'].browse(self._context.get('active_ids'))
        pricelist = self.env['product.pricelist'].search([('currency_id.name', '=', 'MXR')])
        product = self.env.ref('pos_diff_balance.product_product_system_difference')
        seller = self.env.ref('pos_diff_balance.res_partner_system_difference')
        for row in csv_reader:
            try:
                date = datetime.strptime(row[0].replace(',,', '').replace(',', ''), '%d/%m/%Y')
                day_orders = orders.filtered(lambda order: order.date_order.astimezone(
                    pytz.timezone(self.env.user.tz or 'UTC')).date() == date.date())
                if day_orders and not day_orders.filtered(lambda order: order.is_system_diff):
                    orders_total = sum(day_orders.mapped('amount_currency'))
                    cell_total = self.format_number(row[1])
                    diff = (orders_total - cell_total) * -1
                    lines_diff = diff + (orders_total - sum(day_orders.mapped('lines.amount_currency')))
                    if diff or lines_diff:
                        self.env['pos.order'].create({
                            'pricelist_id': pricelist.id,
                            'session_id': day_orders[0].session_id.id,
                            'seller_id': seller.id,
                            'name': "%s/System difference/%s" % (self.env.company.name, date.date()),
                            'lines': [(0, 0, {
                                'name': product.name,
                                'product_id': product.id,
                                'price_subtotal': lines_diff,
                                'price_subtotal_incl': lines_diff,
                                'amount_currency': lines_diff,
                            })],
                            'amount_currency': diff,
                            'amount_total': diff,
                            'amount_paid': diff,
                            'amount_return': 0,
                            'state': 'done',
                            'is_system_diff': True,
                            'amount_tax': 0,
                            'date_order': day_orders[0].date_order})
            except Exception as e:
                continue
