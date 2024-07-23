from odoo import models, fields, api

class WorkOrderCancel(models.TransientModel):
    _name = 'booking_order.work_order_cancel'
    
    note = fields.Text(string='Cancellation Note')

    @api.multi
    def confirm_cancel(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', [])
        work_orders = self.env['booking_order.work_order'].browse(active_ids)
        for work_order in work_orders:
            work_order.write({
                'state': 'cancel',
                'note': self.note,
            })
