from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountAsset(models.Model):
    _inherit = "account.asset"

    at_half_year_depreciation = fields.Boolean(
        string="Austrian Half-Year Depreciation",
        compute="_compute_at_half_year_depreciation",
        readonly=False,
        store=True,
        help=(
            "Technical flag derived from the asset profile. If enabled and the "
            "asset starts in the second half of the fiscal year, the first "
            "and last depreciation years are halved."
        ),
    )

    @api.depends("profile_id")
    def _compute_at_half_year_depreciation(self):
        for asset in self:
            asset.at_half_year_depreciation = bool(
                asset.profile_id.at_half_year_depreciation
            )

    @api.constrains(
        "at_half_year_depreciation", "method", "method_time", "method_period", "prorata"
    )
    def _check_at_half_year_depreciation(self):
        for asset in self.filtered("at_half_year_depreciation"):
            if asset.method not in ("linear", "linear-limit"):
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation only supports "
                        "linear depreciation methods."
                    )
                )
            if asset.method_time != "year":
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation requires "
                        "Time Method = Number of Years or end date."
                    )
                )
            if asset.method_period != "year":
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation currently requires "
                        "Period Length = Year."
                    )
                )
            if asset.prorata:
                raise ValidationError(
                    self.env._(
                        "Austrian half-year depreciation cannot be combined "
                        "with Prorata Temporis."
                    )
                )

    def _use_at_half_year_depreciation(self):
        self.ensure_one()
        return (
            self.at_half_year_depreciation
            and self.method in ("linear", "linear-limit")
            and self.method_time == "year"
            and self.method_period == "year"
            and not self.prorata
            and not self.method_end
            and bool(self.method_number)
        )

    def _is_second_half_of_fiscal_year(self):
        self.ensure_one()
        fy = self._get_fy_info(self.date_start)["record"]
        second_half_start = fy.date_from + relativedelta(months=6)
        return fields.Date.to_date(self.date_start) >= second_half_start

    def _is_half_year_first_entry(self, entry):
        self.ensure_one()
        return (
            entry["date_start"]
            <= fields.Date.to_date(self.date_start)
            <= entry["date_stop"]
        )

    def _is_half_year_last_entry(self, entry, depreciation_stop_date):
        self.ensure_one()
        return entry["date_stop"] >= depreciation_stop_date

    def _get_depreciation_stop_date(self, depreciation_start_date):
        depreciation_stop_date = super()._get_depreciation_stop_date(
            depreciation_start_date
        )
        if (
            self._use_at_half_year_depreciation()
            and self._is_second_half_of_fiscal_year()
        ):
            depreciation_stop_date += relativedelta(years=1)
        return depreciation_stop_date

    def _compute_year_amount(
        self, residual_amount, depreciation_start_date, depreciation_stop_date, entry
    ):
        amount = super()._compute_year_amount(
            residual_amount, depreciation_start_date, depreciation_stop_date, entry
        )
        if not (
            self._use_at_half_year_depreciation()
            and self._is_second_half_of_fiscal_year()
        ):
            return amount
        if self._is_half_year_first_entry(entry) or self._is_half_year_last_entry(
            entry, depreciation_stop_date
        ):
            return amount / 2
        return amount
