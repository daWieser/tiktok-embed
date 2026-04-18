# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAustrianHalfYearDepreciation(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.asset_model = cls.env["account.asset"]
        cls.asset_profile_model = cls.env["account.asset.profile"]
        cls.profile = cls.asset_profile_model.create(
            {
                "account_expense_depreciation_id": cls.company_data[
                    "default_account_expense"
                ].id,
                "account_asset_id": cls.company_data["default_account_assets"].id,
                "account_depreciation_id": cls.company_data[
                    "default_account_assets"
                ].id,
                "journal_id": cls.company_data["default_journal_purchase"].id,
                "name": "AT Half-Year Linear 5Y",
                "method": "linear",
                "method_time": "year",
                "method_number": 5,
                "method_period": "year",
                "prorata": False,
                "at_half_year_depreciation": True,
            }
        )

    def test_half_year_schedule_for_second_half_start(self):
        asset = self.asset_model.create(
            {
                "name": "Half-Year Machine",
                "profile_id": self.profile.id,
                "purchase_value": 4000.0,
                "date_start": "2026-09-15",
            }
        )

        asset.compute_depreciation_board()
        asset.invalidate_recordset()
        depreciation_lines = asset.depreciation_line_ids.filtered(
            lambda line: line.type == "depreciate"
        ).sorted(key=lambda line: line.line_date)

        self.assertEqual(len(depreciation_lines), 6)
        self.assertEqual(
            [line.amount for line in depreciation_lines],
            [400.0, 800.0, 800.0, 800.0, 800.0, 400.0],
        )
        self.assertEqual(
            [str(line.line_date) for line in depreciation_lines],
            [
                "2026-12-31",
                "2027-12-31",
                "2028-12-31",
                "2029-12-31",
                "2030-12-31",
                "2031-12-31",
            ],
        )

    def test_regular_schedule_for_first_half_start(self):
        asset = self.asset_model.create(
            {
                "name": "Regular Machine",
                "profile_id": self.profile.id,
                "purchase_value": 4000.0,
                "date_start": "2026-03-15",
            }
        )

        asset.compute_depreciation_board()
        asset.invalidate_recordset()
        depreciation_lines = asset.depreciation_line_ids.filtered(
            lambda line: line.type == "depreciate"
        ).sorted(key=lambda line: line.line_date)

        self.assertEqual(len(depreciation_lines), 5)
        self.assertEqual(
            [line.amount for line in depreciation_lines],
            [800.0, 800.0, 800.0, 800.0, 800.0],
        )

    def test_asset_can_override_profile_flag(self):
        asset = self.asset_model.create(
            {
                "name": "Override Machine",
                "profile_id": self.profile.id,
                "purchase_value": 4000.0,
                "date_start": "2026-09-15",
                "at_half_year_depreciation": False,
            }
        )

        asset.compute_depreciation_board()
        asset.invalidate_recordset()
        depreciation_lines = asset.depreciation_line_ids.filtered(
            lambda line: line.type == "depreciate"
        ).sorted(key=lambda line: line.line_date)

        self.assertFalse(asset.at_half_year_depreciation)
        self.assertEqual(len(depreciation_lines), 5)
        self.assertEqual(
            [line.amount for line in depreciation_lines],
            [800.0, 800.0, 800.0, 800.0, 800.0],
        )
