from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    last_sid = fields.Char(string="Último ID de Sesión", copy=False)
    last_activity = fields.Float(string="Última Actividad (Timestamp)", copy=False)
    bypass_b2b_security = fields.Boolean(
        string="Bypasar Seguridad de Sesión",
        default=False,
        help="Si se activa, este usuario no se verá afectado por cierres por inactividad o límites de logins simultáneos."
    )
    b2b_session_count = fields.Integer(
        string="Sesiones Activas",
        compute="_compute_b2b_session_count",
        help="Número de sesiones activas actualmente para este usuario."
    )

    def _compute_b2b_session_count(self):
        # Evitar consultas SQL crudas; usamos el ORM directamente
        try:
            if 'b2b.session.activity' in self.env:
                activity_env = self.env['b2b.session.activity']
                for user in self:
                    user.b2b_session_count = activity_env.search_count([
                        ('user_id', '=', user.id),
                        ('is_revoked', '=', False)
                    ])
            else:
                for user in self:
                    user.b2b_session_count = 0
        except Exception:
            for user in self:
                user.b2b_session_count = 0