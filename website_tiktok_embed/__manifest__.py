{
    'name': "TikTok embed",
    'version': '1.0',
    'depends': ['website', 'web_editor'],
    'author': "Benjamin Wieser",
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
        'website.assets_wysiwyg': [
            'website_tiktok_embed/static/src/snippets/s_tiktok_embed/options.js', ],
    },
    'license': 'OPL-1',
    'price': 10,
    'images': ['images/thumbnail.png'],
    'website': 'https://www.wieser-engineering.xyz/'
}
