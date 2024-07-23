from odoo import models, fields, api

class SuccessPopup(models.TransientModel):
    _name = 'booking_order.success_popup'

    message = fields.Text(string='Message', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(SuccessPopup, self).default_get(fields)
        res['message'] = self.env.context.get('message', '')
        return res
