# -*- coding: utf-8 -*-

from odoo import fields, models, api
from ..LabelManager import LabelManager


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection(default='product')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _default_piece_barcode(self):
        return self.env['ir.sequence'].next_by_code('stock_ext.stock_piece')

    weight = fields.Float(tracking=True)
    list_price = fields.Float(string='List price', compute='_compute_price', store=True, readonly=False,
                              tracking=True)
    lot_id = fields.Many2one('stock.lot', string='Lot', tracking=True)
    barcode = fields.Char(default=_default_piece_barcode, tracking=True)
    raw_data = fields.Char(string='Raw data')
    product_label_id = fields.Many2one('stock.product.label', string='Product label')
    category_id = fields.Many2one(related='product_label_id.category_id', store=True)
    standard_price = fields.Float(compute='_compute_standard_price', store=True, readonly=False,
                                  tracking=True, company_dependent=True,)
    total_cost = fields.Float(string='Total Cost', compute='_compute_standard_price', store=True)
    cost_usd = fields.Float(string='Cost USD')
    price_usd = fields.Float(string='Price USD', compute='_compute_price', store=True, readonly=False,
                             tracking=True)
    price_mxn = fields.Float(string='Price MXN', compute='_compute_price', store=True, readonly=False,
                             tracking=True)
    print_enabled = fields.Boolean(string='Print enabled')
    print_queue = fields.Integer(string='Print queue')
    scale_created = fields.Boolean(string='Scale created')
    quant_create = fields.Boolean(string='Quant create')
    cost_retail_calculation = fields.Boolean(string='Cost retail calculation')

    @api.onchange('category_id')
    def onchange_category_id(self):
        if self.category_id:
            self.product_label_id.category_id = self.category_id

    @api.onchange('product_label_id')
    def onchange_product_label_id(self):
        self.name = self.product_label_id.name

    @api.onchange('cost_usd')
    def _onchange_cost_usd(self):
        if self.cost_usd:
            currency_mxn = self.env['res.currency'].browse(self.env.ref('base.USD').id)
            self.standard_price = self.cost_usd * currency_mxn.inverse_rate

    @api.model_create_multi
    def create(self, vals_list):
        result = super(ProductProduct, self).create(vals_list)
        for piece in result:
            if piece.quant_create:
                self.env['stock.quant'].create({
                    'product_id': piece.id,
                    'quantity': 1,
                    'location_id': self.env.ref('stock.stock_location_stock').id})
            if piece.scale_created:
                piece.name = piece.barcode
                piece.categ_id = self.env.ref('stock_ext.product_category_piece')
        return result

    @api.depends('lot_id', 'lot_id.cost_2', 'lot_id.additional_usd', 'weight')
    def _compute_standard_price(self):
        currency_mxn = self.env['res.currency'].browse(self.env.ref('base.USD').id)
        for piece in self:
            piece.standard_price = ((piece.lot_id.cost_2 + piece.lot_id.additional_usd) *
                                    piece.weight * currency_mxn.inverse_rate)
            piece.cost_usd = (piece.lot_id.cost_2 + piece.lot_id.additional_usd) * piece.weight
            piece.total_cost = piece.lot_id.cost_2 * piece.weight

    @api.depends('lot_id', 'cost_usd', 'lot_id.tax_id', 'lot_id.variant')
    def _compute_price(self):
        currency_model = self.env['res.currency']
        for piece in self:
            price_untaxed = (piece.cost_usd * (piece.lot_id.variant or 1))
            price = price_untaxed + (price_untaxed * piece.lot_id.tax_id.amount / 100)
            currency_mxn = currency_model.browse(self.env.ref('base.USD').id)
            price_mxn = price * currency_mxn.inverse_rate
            piece.price_usd = piece.lot_id.purchase_cost if not price else price
            piece.price_mxn = piece.lot_id.purchase_cost if not price else price_mxn
            piece.list_price = piece.cost_usd * (piece.lot_id.variant or 1) * currency_mxn.inverse_rate

    def print_sticker(self, print_enabled=True):
        if not self.raw_data:
            manager = LabelManager()
            data = {'code': self.barcode or "",
                    'product': self.name,
                    'weight': self.weight,
                    'price_usd': str(round(self.price_usd)),
                    'price_mxn': str(round(self.price_mxn))}
            label = manager.generate_label_data(data)
            self.write({'raw_data': label.dumpZPL()})
        self.write({'print_enabled': print_enabled,
                    'print_queue': int(self.qty_available)})

    def print_sticker_wholesale(self):
        for piece in self:
            piece.print_sticker()

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        name = name.upper()
        return super(ProductProduct, self)._name_search(
            name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
