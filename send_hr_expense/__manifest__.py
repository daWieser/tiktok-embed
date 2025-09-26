{
    'name': ' Send HR Expense to Contact',
    'version': '0.1',
    'summary': 'Adds a button to send an approved expense report to a contact via mail',
    'author': 'Vorstieg Software FlexCo',
    'website': 'https://www.vorstieg.eu',
    'category': 'Human Resources',
    'depends': ['hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/send_to_contact_wizard_views.xml',
        'views/hr_expense_views.xml',
        'data/mail_template.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
    'images': ['images/thumbnail.png']
}
