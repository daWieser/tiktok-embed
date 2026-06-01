{
    'name': "Lottie Animation Embed",
    'summary': "Easy Lottie Animation Embedding for your Odoo Website",
    'version': '19.0.1.0',
    'depends': ['website', 'html_editor', 'html_builder'],
    'author': "Vorstieg Software FlexCo",
    'website': "https://www.vorstieg.eu",
    'category': 'Website/Website',
    'description': "This extention allowes easy embedding of Lottie Animation",
    'data': [
        'views/s_lottie_embed.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_lottie_embed/static/lib/lottie-player/lottie-player.js',
            'website_lottie_embed/static/src/snippets/s_lottie_embed/lottie_utils.js',
            'website_lottie_embed/static/src/snippets/s_lottie_embed/000.js',
            'website_lottie_embed/static/src/snippets/s_lottie_embed/000.scss',
        ],
        'website.website_builder_assets': [
            'website_lottie_embed/static/lib/lottie-player/lottie-player.js',
            'website_lottie_embed/static/src/snippets/s_lottie_embed/lottie_utils.js',
            'website_lottie_embed/static/src/snippets/s_lottie_embed/options.js',
            'website_lottie_embed/static/src/snippets/s_lottie_embed/options.xml',
        ],
    },
    'license': 'LGPL-3',
    'images': ['images/thumbnail.png'],
    'installable': True,
    'application': False
}