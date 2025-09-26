# -*- coding: utf-8 -*-
from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_send_bill_to_contact(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Bill to Contact',
            'res_model': 'send.vendor.bill.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_bill_id': self.id,
                'default_partner_id': self.partner_id.id,
            }
        }