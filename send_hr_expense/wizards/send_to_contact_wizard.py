# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SendToContactWizard(models.TransientModel):
    _name = 'send.to.contact.wizard'
    _description = 'Send to Contact Wizard'

    expense_id = fields.Many2one('hr.expense', string='Expense', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True)

    def action_send_email(self):
        self.ensure_one()
        if self.expense_id and self.partner_id:
            template = self.env.ref('send_hr_expense.email_template_expense_report')
            attachment = self.env['ir.attachment'].search([
                ('res_model', '=', 'hr.expense'),
                ('res_id', '=', self.expense_id.id)
            ], limit=1)

            if template and attachment:
                template.attachment_ids = [(6, 0, [attachment.id])]
                template.send_mail(self.expense_id.id, force_send=True, email_values={'email_to': self.partner_id.email})
        return {'type': 'ir.actions.act_window_close'}
