from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger("*___INI LAGI TESTING___*")

class SaleOrder(models.Model):
    _name = 'booking_order.sale_order'
    _rec_name = "id"
    # _inherit = ['mail.thread']

    is_booking_order = fields.Boolean(string='Is Booking Order')
    team_id = fields.Many2one(
        'booking_order.service_team',
        string='Team',
        required=True
    )
    team_leader_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        compute='get_team_leader'
    )
    team_member_ids = fields.Many2many(
        'res.users',
        string='Team Members',
        compute="get_team_members"
    )
    start_book = fields.Datetime(string='Booking Start', required=True)
    end_book = fields.Datetime(string='Booking End', required=True)
    work_order_count = fields.Integer(string='Work Order', compute='get_work_order_count')

    @api.model
    def create(self, vals):
        vals['is_booking_order'] = True
        return super(SaleOrder, self).create(vals)

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

    def check_work_order(self):
        isAvailable = True
        message = ""
        work_order = self.env['booking_order.work_order'].sudo().search([
            '|',
            ('team_id', '=', self.team_id.id),
            ('team_leader_id', '=', self.team_leader_id.id),
            ('state', '!=', 'cancel')
        ])

         
        for record in work_order:
            notAvailable = (self.start_book >= record.start_plan and self.start_book <= record.end_plan) or (self.end_book >= record.start_plan and self.end_book <= record.end_plan)
            if notAvailable:
                isAvailable = False
                message = 'Team already has work order during that period on {}.'.format(record.name)
        
        if isAvailable == False:
            raise ValidationError(_(message))
        else:
            _logger.info('Team is available for booking')
            return {
                'name': (''),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'booking_order.success_popup',
                'type': 'ir.actions.act_window',
                'view_id': self.env.ref('booking_order.success_popup_form').id,
                'target': 'new',
                'context': {
                    'message': 'Team is available for booking.'
                }
            }

    def create_work_order(self):
        isAvailable = True
        message = ""
        work_order = self.env['booking_order.work_order'].sudo().search([
            '|',
            ('team_id', '=', self.team_id.id),
            ('team_leader_id', '=', self.team_leader_id.id),
            ('state', '!=', 'cancel')
        ])

         
        for record in work_order:
            notAvailable = (self.start_book >= record.start_plan and self.start_book <= record.end_plan) or (self.end_book >= record.start_plan and self.end_book <= record.end_plan)
            if notAvailable:
                isAvailable = False
                message = 'Team is not available during this period, already booked on {}. Please book on another date.'.format(record.name)

        vals = {
            'sale_order_id': self.id,
            'team_id': self.team_id.id,
            'start_plan': self.start_book,
            'end_plan': self.end_book,
            'state': 'pending'
        }

        if isAvailable == False:
            raise ValidationError(_(message))
        else:
            self.env['booking_order.work_order'].create(vals)

    def get_work_order_count(self):
        count = self.env['booking_order.work_order'].search_count([('sale_order_id', '=', self.id)])
        self.work_order_count = count

    @api.multi
    def open_work_order(self):
        self.ensure_one()
        action = self.env.ref('booking_order.action_work_order').read()[0]

        action['domain'] = [('sale_order_id', '=', self.id)]
        return action
