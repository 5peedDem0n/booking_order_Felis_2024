# -*- coding: utf-8 -*-
{
    'name': "booking_order_FELIS_2024",

    'summary': """
        Booking Order System""",

    'description': """
        Odoo technical test from KNITTO
    """,

    'sequence': 0,
    'author': "Felis Tigris Hafizhulloh",
    'website': "https://knitto.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/service_team.xml',
        'views/sale_order.xml',
        'views/work_order.xml',
        'data/sequence_data.xml',
        'report/work_order_report.xml',
        'report/work_order_report_template.xml',
        'wizard/cancel_popup.xml',
        'wizard/succeed_popup.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}