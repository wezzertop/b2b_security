{
    'name': 'B2B Security: Restrict Logins & Session Timeout',
    'version': '19.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Prevents simultaneous logins and adds inactivity session timeouts for portal users.',
    'description': """
B2B Security & Session Control
==============================
This module helps protect B2B portal environments by implementing two key security features:
1. Prevents multiple users from logging into the same account simultaneously from different devices/browsers.
2. Automatically logs users out after a configurable period of inactivity to protect sensitive data.
Administrators can configure these settings from General Settings and can bypass restrictions for specific users.
    """,
    'author': 'JDDM',
    'depends': ['base', 'base_setup', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml',
        'views/session_activity_views.xml',
        'views/res_users_views.xml',
    ],
    'images': ['static/description/banner.gif', 'static/description/icon.png'],
    'price': 120.00,
    'currency': 'USD',
    'installable': True,
    'application': True,
    'license': 'OPL-1',
    'assets': {
        'web.assets_backend': [
            'b2b_security/static/src/js/session_security.js',
        ],
        'web.assets_frontend': [
            'b2b_security/static/src/js/session_security.js',
        ],
    }
}