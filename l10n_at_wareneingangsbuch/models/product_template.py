from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    l10n_at_wareneingangsbuch_label = fields.Char(
        string="Wareneingangsbuch Label",
        help=(
            "Optional product-specific generic goods description. If empty, the "
            "category label is used."
        ),
    )
