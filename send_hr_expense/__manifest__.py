{
    'name': 'Send HR Expense to Contact',
    'version': '19.0.1.0',
    'summary': 'Adds a button to send an approved expense report to a contact via mail, with an option to convert image attachments to PDF.',
    'author': 'Vorstieg Software FlexCo',
    'website': 'https://www.vorstieg.eu',
    'category': 'Human Resources',
    'depends': ['hr_expense', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/send_to_contact_wizard_views.xml',
        'views/hr_expense_views.xml',
        'data/mail_template.xml',
    ],
    'external_dependencies': {
        'python': ['Pillow'],
    },
    'installable': True,
    'license': 'LGPL-3',
    'images': ['images/thumbnail.png'],
}
