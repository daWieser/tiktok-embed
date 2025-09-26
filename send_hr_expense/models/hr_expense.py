# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    def action_send_to_contact(self):
        _logger.info("action_send_to_contact called")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send to Contact',
            'res_model': 'send.to.contact.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_expense_id': self.id,
            }
        }
