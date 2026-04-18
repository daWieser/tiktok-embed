{
    "name": "Austrian Asset Half-Year Depreciation",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Adds Austrian half-year depreciation to account_asset_management",
    "description": """
Austrian Asset Half-Year Depreciation
=====================================

This module adds Austrian half-year depreciation support on top of
`account_asset_management`.

When enabled on an asset profile and the asset starts in the second half of the
fiscal year, the first and last depreciation years are halved.

The first implementation is intentionally limited to yearly linear
depreciation, which matches the Austrian half-year tax rule cleanly.
""",
    "author": "Vorstieg Software FlexCo",
    "website": "https://www.vorstieg.eu",
    "license": "LGPL-3",
    "depends": [
        "account_asset_management",
    ],
    "data": [
        "views/account_asset_profile_views.xml",
        "views/account_asset_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
