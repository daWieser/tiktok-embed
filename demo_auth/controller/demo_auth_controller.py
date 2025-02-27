from odoo import http
from odoo.http import request


class DemoAuthController(http.Controller):

    @http.route('/web/demo_login', type='http', auth='public', website=True)
    def demo_login(self, redirect='/web'):
        credential = {'login': "demo", 'password': "demo", 'type': 'password'}
        request.session.authenticate(request.db, credential)
        return request.redirect(redirect)
