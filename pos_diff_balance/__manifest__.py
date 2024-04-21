# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'POS Diff Balance',
    'summary': 'POS Diff Balance',
    'description': 'POS Diff Balance',
    'category': 'Point of Sale',
    'author': 'Alex Esteves',
    'depends': [
        'point_of_sale',
        'pos_ext',
        'pos_sellers',
    ],
    'data': [
        'data/ir_actions.xml',
        'data/pos_diff_balance_data.xml',
        'wizard/balance_amounts_wizard_views.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
