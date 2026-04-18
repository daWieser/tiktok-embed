from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountAssetProfile(models.Model):
    _inherit = "account.asset.profile"

    at_half_year_depreciation = fields.Boolean(
        string="Austrian Half-Year Depreciation",
        help=(
            "If enabled, assets that start in the second half of the fiscal "
            "year use Austrian half-year depreciation. The current "
            "implementation supports yearly linear depreciation only."
        ),
    )

    @api.constrains(
        "at_half_year_depreciation", "method", "method_time", "method_period"
    )
    def _check_at_half_year_depreciation(self):
        for profile in self.filtered("at_half_year_depreciation"):
            if profile.method not in ("linear", "linear-limit"):
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation only supports "
                        "linear depreciation methods."
                    )
                )
            if profile.method_time != "year":
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation requires "
                        "Time Method = Number of Years or end date."
                    )
                )
            if profile.method_period != "year":
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation currently requires "
                        "Period Length = Year."
                    )
                )
