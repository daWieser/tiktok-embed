{
    'name': "Demo Auth",
    'version': '19.0.1.0',
    'depends': ['base', 'website'],
    'author': "Vorstieg Software FlexCo",
    'website': "https://www.vorstieg.eu",
    'category': 'Tools',
    'description': """
    This module allows users to log in with a demo user without a username or password
    """,
    'license': 'GPL-3',
    'post_init_hook': 'post_init_hook',
    'images': ['images/thumbnail.png'],
    'installable': True,
    'application': False,
}
