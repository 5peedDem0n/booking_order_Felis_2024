from odoo import models, fields, api

class ServiceTeam(models.Model):
    _name = 'booking_order.service_team'

    name = fields.Char(string='Team Name', required=True)
    team_leader_id = fields.Many2one('res.users',
        string='Team Leader',
        required=True
    )
    team_member_ids = fields.Many2many(
        'res.users',
        string='Team Members',
    )
    