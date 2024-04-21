# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import pytz


class PosOrder(models.Model):
    _inherit = 'pos.order'

    is_system_diff = fields.Boolean(string='System difference')

    def _export_for_ui(self, order):
        if order.is_system_diff:
            timezone = pytz.timezone(self._context.get('tz') or self.env.user.tz or 'UTC')
            return {
                'lines': [[0, 0, line] for line in order.lines.export_for_ui()],
                'statement_ids': [[0, 0, payment] for payment in order.payment_ids.export_for_ui()],
                'name': order.pos_reference,
                'uid': order.pos_reference,
                'amount_paid': order.amount_paid,
                'amount_total': order.amount_total,
                'amount_tax': order.amount_tax,
                'amount_return': order.amount_return,
                'pos_session_id': order.session_id.id,
                'pricelist_id': order.pricelist_id.id,
                'partner_id': order.partner_id.id,
                'user_id': order.user_id.id,
                'sequence_number': order.sequence_number,
                'creation_date': str(order.date_order.astimezone(timezone)),
                'fiscal_position_id': order.fiscal_position_id.id,
                'to_invoice': order.to_invoice,
                'to_ship': order.to_ship,
                'state': order.state,
                'account_move': order.account_move.id,
                'id': order.id,
                'is_tipped': order.is_tipped,
                'tip_amount': order.tip_amount,
                'access_token': order.access_token,
            }
        return super(PosOrder, self)._export_for_ui(order)

    def action_balance_amounts(self):
        return {
            'name': _('Balance amounts'),
            'type': 'ir.actions.act_window',
            'res_model': 'balance.amounts.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
