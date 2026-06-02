from odoo import models, fields, api

class B2BSessionActivity(models.Model):
    _name = 'b2b.session.activity'
    _description = 'Actividad de Sesiones B2B'
    _order = 'last_activity desc'

    user_id = fields.Many2one('res.users', string="Usuario", required=True, ondelete='cascade')
    session_sid = fields.Char(string="ID de Sesión", required=True, index=True)
    ip_address = fields.Char(string="Dirección IP")
    user_agent = fields.Char(string="Agente de Usuario / Navegador")
    login_time = fields.Datetime(string="Fecha de Inicio", default=fields.Datetime.now)
    last_activity = fields.Datetime(string="Última Actividad", default=fields.Datetime.now)
    is_revoked = fields.Boolean(string="Revocada", default=False)

    def action_revoke(self):
        self.write({'is_revoked': True})

    @api.model
    @api.autovacuum
    def _gc_session_activity(self):
        """
        Limpiar sesiones automáticamente:
        Elimina sesiones que tengan más de 7 días de antigüedad para evitar
        que la base de datos crezca indefinidamente.
        """
        expiration_date = fields.Datetime.subtract(fields.Datetime.now(), days=7)
        expired_sessions = self.search([('last_activity', '<', expiration_date)])
        if expired_sessions:
            expired_sessions.unlink()

    @api.model
    def _sweep_ghost_sessions(self):
        """
        Marcador de sesiones abandonadas (Cron Job):
        Busca sesiones activas cuya última actividad rebase el tiempo de expiración
        (o 2 horas por defecto si no hay límite configurado) y las revoca.
        """
        param_obj = self.env['ir.config_parameter'].sudo()
        session_timeout_str = param_obj.get_param('b2b_security.b2b_session_timeout', default='0')
        timeout_minutes = int(session_timeout_str) if session_timeout_str else 0
        
        # Si no hay límite estricto, revocamos por defecto después de 120 minutos sin pings
        minutes_to_check = timeout_minutes if timeout_minutes > 0 else 120
        # Damos un margen de gracia de 5 minutos por posibles retrasos de red
        minutes_to_check += 5
        
        threshold_date = fields.Datetime.subtract(fields.Datetime.now(), minutes=minutes_to_check)
        
        ghost_sessions = self.search([
            ('is_revoked', '=', False),
            ('last_activity', '<', threshold_date)
        ])
        
        if ghost_sessions:
            ghost_sessions.write({'is_revoked': True})
