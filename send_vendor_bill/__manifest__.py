{
    'name': 'Send Vendor Bill to Contact',
    'version': '1.0',
    'summary': 'Adds a button to send a posted vendor bill to a contact via mail.',
    'author': 'Vorstieg Software FlexCo',
    'website': 'https://www.vorstieg.eu',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/send_vendor_bill_wizard_views.xml',
        'views/account_move_views.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}