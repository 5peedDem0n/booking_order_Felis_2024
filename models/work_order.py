from odoo import models, fields, api
from datetime import datetime

class WorkOrder(models.Model):
    _name = 'booking_order.work_order'

    name = fields.Char(string='WO Number', readonly=True, copy=False, index=True, default=lambda self: ('New'))
    sale_order_id = fields.Many2one(
        string='Booking Order Reference',
        comodel_name='booking_order.sale_order',
        readonly=True
    )
    team_id = fields.Many2one(
        'booking_order.service_team',
        string='Team',
        required=True
    )
    team_leader_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        required=True,
        compute='get_team_leader'
    )
    team_member_ids = fields.Many2many(
        'res.users',
        string='Team Members',
        compute='get_team_members'
    )
    start_plan = fields.Datetime(string='Planned Start', required=True)
    end_plan = fields.Datetime(string='Planned End', required=True)
    start_date = fields.Datetime(string='Date Start', readonly=True)
    end_date = fields.Datetime(string='Date End', readonly=True)
    state = fields.Selection(
        string='State',
        selection=[('pending', 'Pending'), ('progress', 'In Progress'), ('done', 'Done'), ('cancel', 'Cancelled')]
    )
    note = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', ('New')) == ('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('booking_order.work_order') or ('New')
        return super(WorkOrder, self).create(vals)
    
    @api.depends('team_id')
    def get_team_leader(self):
        for record in self:
            if record.team_id:
                record.team_leader_id = record.team_id.team_leader_id

    @api.depends('team_id')
    def get_team_members(self):
        for record in self:
            if record.team_id:
                record.team_member_ids = record.team_id.team_member_ids
                    
                # _logger.info(record.team_id.team_member_ids)

    def generate_start_work(self):
        for record in self:
            record.start_date = datetime.now()
            record.state = 'progress'

    def generate_end_work(self):
        for record in self:
            record.end_date = datetime.now()
            record.state = 'done'

    def generate_reset_work(self):
        for record in self:
            record.start_date = None
            record.state = 'pending'

    def generate_cancel_work(self):
        return {
            'name': 'Cancel Work Order',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'booking_order.work_order_cancel',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('booking_order.work_order_cancel_form').id,
            'target': 'new',
        }

    @api.multi
    def print_report(self):
        return self.env['report'].get_action(self, 'booking_order.report_work_order')
    
    
    

    
    