# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError
import base64
import io
import logging
from PIL import Image

_logger = logging.getLogger(__name__)


class SendToContactWizard(models.TransientModel):
    _name = 'send.to.contact.wizard'
    _description = 'Send to Contact Wizard'

    expense_id = fields.Many2one('hr.expense', string='Expense', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Contact', required=True)
    convert_to_pdf = fields.Boolean(string='Convert attachment to PDF', default=True,
                                    help="If the attachment is an image, it will be converted to a PDF before sending.")

    def action_send_email(self):
        self.ensure_one()
        if not self.expense_id or not self.partner_id:
            return {'type': 'ir.actions.act_window_close'}

        if not self.partner_id.email:
            raise UserError(_('The selected contact has no email address.'))

        template = self.env.ref('send_hr_expense.email_template_expense_report')
        attachment = self.env['ir.attachment'].search([
            ('res_model', '=', 'hr.expense'),
            ('res_id', '=', self.expense_id.id)
        ], limit=1)

        attachment_to_send = attachment
        temp_attachment = self.env['ir.attachment']

        if self.convert_to_pdf and attachment and attachment.mimetype and attachment.mimetype.startswith('image'):
            try:
                image_data = base64.b64decode(attachment.datas)
                image = Image.open(io.BytesIO(image_data))

                if image.mode == 'RGBA':
                    image = image.convert('RGB')

                pdf_buffer = io.BytesIO()
                image.save(pdf_buffer, format='PDF', resolution=100.0)
                pdf_data = base64.b64encode(pdf_buffer.getvalue())

                pdf_attachment_name = attachment.name.rsplit('.', 1)[0] + '.pdf'

                temp_attachment = self.env['ir.attachment'].create({
                    'name': pdf_attachment_name,
                    'type': 'binary',
                    'datas': pdf_data,
                    'mimetype': 'application/pdf',
                    'res_model': self._name,  # Attach to the wizard to avoid cluttering the expense
                    'res_id': self.id,
                })
                attachment_to_send = temp_attachment
            except Exception as e:
                _logger.warning(f"Could not convert image to PDF for expense {self.expense_id.name}: {e}")
                # Fallback to original attachment

        if template and attachment_to_send:
            email_values = {
                'email_to': self.partner_id.email,
                'attachment_ids': [(6, 0, [attachment_to_send.id])]
            }
            template.send_mail(self.expense_id.id, force_send=True, email_values=email_values)

        if temp_attachment:
            temp_attachment.unlink()

        return {'type': 'ir.actions.act_window_close'}
