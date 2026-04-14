from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    l10n_at_wareneingangsbuch_include = fields.Boolean(
        string="Include in Wareneingangsbuch",
        help=(
            "Enable this category for the Austrian Wareneingangsbuch report. "
            "Use it only for goods that should be tracked in the register."
        ),
    )
    l10n_at_wareneingangsbuch_label = fields.Char(
        string="Wareneingangsbuch Label",
        help=(
            "Optional generic goods description for this category, for example "
            "'KFZ-Ersatzteile'."
        ),
    )
