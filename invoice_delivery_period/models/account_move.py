# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_period_start_date = fields.Date(string='Delivery Period Start')
    delivery_period_end_date = fields.Date(string='Delivery Period End')
