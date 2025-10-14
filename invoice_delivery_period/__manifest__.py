{
    'name': 'Invoice Delivery Period',
    'version': '1.0',
    'summary': 'Adds an optional delivery period to an invoice wich replaces the delivery date.',
    'summary_de': 'Fügt einen optionale Lieferzeitraum zu Rechnungen hinzu welche das Lieferdatum ersetzt.',
    'author': 'Vorstieg Software FlexCo',
    'website': 'https://www.vorstieg.eu',
    'category': 'Accounting',
    'depends': ['account', 'l10n_din5008'],
    'data': [
        'views/account_move_views.xml',
        'reports/invoice_report.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
    'images': ['images/thumbnail.png'],
    'i18n': {
        'de': 'i18n/de.po',
    },
}