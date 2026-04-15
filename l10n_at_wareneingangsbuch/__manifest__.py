{
    "name": "Austrian Wareneingangsbuch",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Wareneingangsbuch report for Austrian accounting and tax compliance",
    "description": """
Austrian Wareneingangsbuch
==========================

This module adds a dedicated Wareneingangsbuch report for Austrian businesses
that need to document qualifying goods purchases in chronological order.

The report excludes services and is intended for Austrian accounting use cases
where a Wareneingangsbuch must be maintained.
""",
    "author": "Vorstieg Software FlexCo",
    "website": "https://www.vorstieg.eu",
    "license": "LGPL-3",
    "depends": [
        "account",
        "product",
        "purchase_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_category_views.xml",
        "views/product_template_views.xml",
        "views/wareneingangsbuch_report_views.xml",
    ],
    "images": [
        "static/description/icon.png",
    ],
    "installable": True,
    "auto_install": False,
}
