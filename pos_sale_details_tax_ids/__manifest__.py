{
    'name': "POS Sales Report with tax position on every line",
    'version': '19.0.1.0',
    'depends': ['point_of_sale'],
    'author': "Vorstieg Software FlexCo",
    'website': "https://www.vorstieg.eu",
    'category': 'Point of Sale',
    'summary': 'Shows applied taxes on each line of the POS sales details report.',
    'description': """
        Extends the POS sales details report to display the tax names
        applied on each product line (after fiscal position).
    """,
    'license': 'GPL-3',
    'images': ['images/thumbnail.png'],
    'data': [
        'views/pos_session_sales_details.xml',
    ],
    'installable': True,
    'application': False,
}
