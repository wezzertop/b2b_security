from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    prevent_simultaneous_logins = fields.Boolean(
        string="Restringir Logins Simultáneos",
        config_parameter="b2b_security.prevent_simultaneous_logins",
        help="Si está activo, iniciar sesión en un dispositivo cerrará las sesiones anteriores del mismo usuario."
    )

    b2b_session_timeout = fields.Integer(
        string="Tiempo de Expiración de Sesión (Minutos)",
        config_parameter="b2b_security.b2b_session_timeout",
        default=30,
        help="Minutos de inactividad antes de forzar el cierre de sesión de forma automática."
    )

    force_absolute_timeout = fields.Boolean(
        string="Forzar Cierre de Sesión Absoluto",
        config_parameter="b2b_security.force_absolute_timeout",
        help="Cerrar la sesión sin importar si el usuario sigue dando clics o usando el sistema."
    )

    absolute_timeout_minutes = fields.Integer(
        string="Minutos Máximos Absolutos",
        config_parameter="b2b_security.absolute_timeout_minutes",
        default=60,
        help="Minutos totales que puede durar la sesión antes de cerrarse obligatoriamente."
    )