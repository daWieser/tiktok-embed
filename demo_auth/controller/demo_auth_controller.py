from odoo import http
from odoo.http import request


class DemoAuthController(http.Controller):

    @http.route('/web/demo_login', type='http', auth='public', website=True)
    def demo_login(self, redirect='/web'):
        # In Odoo 19.0: authenticate(env, credential)
        # credential must be a dict with 'type', 'login', and 'password' keys
        credential = {'type': 'password', 'login': "demo", 'password': "demo"}
        request.session.authenticate(request.env, credential)
        return request.redirect(redirect)
