{
    'name': 'B2B Security: Restrict Logins & Session Timeout',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Prevents simultaneous logins, adds inactivity session timeouts, and customizable logout messages for portal users.',
    'description': """
B2B Security & Session Control
==============================
This module helps protect B2B portal environments by implementing key security features with a professional user experience:
1. Prevents multiple users from logging into the same account simultaneously from different devices/browsers.
2. Automatically logs users out after a configurable period of inactivity to protect sensitive data.
3. Fully Customizable Logout Messages: Configure professional, branded messages to explain exactly why a session was closed (e.g. login from another device, inactivity, or maximum time reached).
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
    'price': 10.00,
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
