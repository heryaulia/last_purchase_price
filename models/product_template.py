from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_purchase_line_ids = fields.One2many(
        comodel_name="purchase.order.line",
        related="product_variant_ids.last_purchase_line_ids",
        string="Last Purchase Order Lines",
    )
    last_purchase_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        compute="_compute_last_purchase_line_id",
        string="Last Purchase Line",
    )
    last_purchase_price = fields.Char(
        compute="_compute_last_purchase_line_id_info", string="Last Purchase Price"
    )

    @api.depends("last_purchase_line_ids")
    def _compute_last_purchase_line_id(self):
        for item in self:
            item.last_purchase_line_id = fields.first(item.last_purchase_line_ids)

    @api.depends("last_purchase_line_id")
    def _compute_last_purchase_line_id_info(self):
        for item in self:
            if item.last_purchase_line_id and item.last_purchase_line_id.currency_id:
                currency = item.last_purchase_line_id.currency_id.name
                price = item.last_purchase_line_id.price_unit
                item.last_purchase_price = f"{currency} {price:.2f}"
            else:
                item.last_purchase_price = "0.00"

