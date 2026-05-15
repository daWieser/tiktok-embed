{
    "name": "Austria - MIS Financial Reports",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/Reporting",
    "summary": "Austrian MIS Profit and Loss template based on l10n_at report tags",
    "description": """
Austria - MIS Financial Reports
===============================

This module provides an Austrian Profit and Loss MIS template based on the
same `l10n_at` account tags used by the enterprise `l10n_at_reports` module.

The template reproduces the GuV structure of § 231 UGB (Gesamtkostenverfahren)
inside MIS Builder so it can be exported to Excel or PDF.
""",
    "author": "Vorstieg Software FlexCo",
    "website": "https://www.vorstieg.eu",
    "license": "LGPL-3",
    "depends": [
        "l10n_at",
        "mis_builder",
        "mis_template_financial_report",
    ],
    "data": [
        "data/mis_report.xml",
        "data/mis_report_balance.xml",
        "data/mis_report_guv.xml",
    ],
    "installable": True,
    "auto_install": False,
}
