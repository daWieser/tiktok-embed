{
    'name': "TikTok embed",
    'version': '1.0',
    'depends': ['website', 'html_editor'],
    'author': "Vorstieg Software FlexCo",
    'website': "https://www.vorstieg.eu",
    'category': 'Website/Website',
    'description': """
    This extention allowes easy embedding of TikTok videos
    """,
    # data files always loaded at installation
    'data': [
        'views/s_tiktok_embed.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_tiktok_embed/static/src/snippets/s_tiktok_embed/000.js',
            'website_tiktok_embed/static/src/snippets/s_tiktok_embed/000.scss'],

    },
    'license': 'GPL-3',
    'images': ['images/thumbnail.png']
}
