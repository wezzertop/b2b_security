{
    'name': 'B2B Security: Restrict Logins & Session Timeout',
    'version': '19.0.1.0.0',
    'category': 'Website/Security',
    'summary': 'Controla inicios de sesión simultáneos y fuerza la expiración de sesión por inactividad en el portal.',
    'description': """
B2B Security: Restrict Logins & Session Timeout
===============================================
Este módulo proporciona control avanzado sobre las sesiones de usuario para portales B2B en Odoo.
Permite restringir los inicios de sesión simultáneos (evitando que varias personas usen la misma cuenta),
estableciendo límites de inactividad y forzando cierres de sesión absolutos para mayor seguridad.
Ideal para controlar el acceso de clientes a tu portal.
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
    'price': 25.00,
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