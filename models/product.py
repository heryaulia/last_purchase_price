# Import necessary models
from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Define computed fields to get the last purchase price and currency
    last_purchase = fields.Char('Last Purchase', compute='_compute_last_purchase')

    @api.depends('stock_move_ids')
    def _compute_last_purchase(self):
        for variant in self:
            # Get all purchase stock moves for the variant
            purchase_moves = variant.stock_move_ids.filtered(lambda m: m.picking_type_id.code == 'incoming')

            # If there are no purchase moves, set the last purchase to 'No purchase history'
            if not purchase_moves:
                variant.last_purchase = 'No purchase history'
                continue

            # Sort the purchase moves by date in descending order
            sorted_moves = purchase_moves.sorted(key=lambda m: m.date, reverse=True)

            # Set the last purchase to the currency and price of the most recent purchase move
            currency = sorted_moves[0].currency_id.name
            price = sorted_moves[0].price_unit
            variant.last_purchase = f"{currency} {price}"
