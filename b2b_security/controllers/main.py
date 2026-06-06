import time
from odoo import http, fields
from odoo.http import request
from odoo.addons.web.controllers.session import Session

def _parse_user_agent(ua_string):
    if not ua_string:
        return "Desconocido"
    ua_lower = ua_string.lower()
    
    # Detectar SO
    os = "Desconocido"
    if "windows" in ua_lower: os = "Windows"
    elif "mac os" in ua_lower or "macintosh" in ua_lower: os = "macOS"
    elif "android" in ua_lower: os = "Android"
    elif "iphone" in ua_lower or "ipad" in ua_lower: os = "iOS"
    elif "linux" in ua_lower: os = "Linux"
    
    # Detectar Navegador
    browser = "Navegador"
    if "edg" in ua_lower: browser = "Edge"
    elif "opr" in ua_lower or "opera" in ua_lower: browser = "Opera"
    elif "chrome" in ua_lower: browser = "Chrome"
    elif "firefox" in ua_lower: browser = "Firefox"
    elif "safari" in ua_lower and "chrome" not in ua_lower: browser = "Safari"
    
    return f"{browser} en {os}"

class B2BSessionController(Session):
    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        # Interceptar el cierre de sesión para revocar instantáneamente el registro
        session_sid = request.session.sid
        if session_sid:
            try:
                activity_env = request.env['b2b.session.activity'].sudo()
                activity = activity_env.search([('session_sid', '=', session_sid), ('is_revoked', '=', False)], limit=1)
                if activity:
                    activity.write({'is_revoked': True})
            except Exception:
                pass
        return super(B2BSessionController, self).logout(redirect=redirect)

class B2BSecurityController(http.Controller):
    
    @http.route('/b2b_security/ping', type='json', auth='user')
    def security_ping(self, **kwargs):
        user = request.env.user
        session_sid = request.session.sid
        param_obj = request.env['ir.config_parameter'].sudo()
        activity_env = request.env['b2b.session.activity'].sudo()
        
        # Obtener configuraciones del sistema (respetando si el usuario tiene bypass de reglas automáticas)
        if user.bypass_b2b_security:
            prevent_logins = False
            timeout_minutes = 0
            absolute_timeout_minutes = 0
        else:
            prevent_logins = param_obj.get_param('b2b_security.prevent_simultaneous_logins') == 'True'
            
            session_timeout = param_obj.get_param('b2b_security.b2b_session_timeout', default='0')
            timeout_minutes = int(session_timeout) if session_timeout else 0
            
            force_absolute = param_obj.get_param('b2b_security.force_absolute_timeout') == 'True'
            absolute_timeout_minutes = int(param_obj.get_param('b2b_security.absolute_timeout_minutes', default='60')) if force_absolute else 0

        msg_kicked_other_device = param_obj.get_param('b2b_security.msg_kicked_other_device', default='Su sesión ha sido cerrada desde otro dispositivo o por el administrador.')
        msg_timeout_inactivity = param_obj.get_param('b2b_security.msg_timeout_inactivity', default='Su sesión ha expirado por inactividad.')
        msg_timeout_absolute = param_obj.get_param('b2b_security.msg_timeout_absolute', default='Su sesión ha alcanzado el límite máximo de tiempo permitido.')

        # Buscar si ya existe registro de esta sesión en la base de datos
        activity = activity_env.search([
            ('session_sid', '=', session_sid),
            ('user_id', '=', user.id)
        ], limit=1)

        now_dt = fields.Datetime.now()

        # Obtener IP real detrás de Proxy (si aplica)
        ip_addr = request.httprequest.headers.get('X-Forwarded-For', request.httprequest.remote_addr)
        if ip_addr and ',' in ip_addr:
            ip_addr = ip_addr.split(',')[0].strip()

        raw_ua = request.httprequest.user_agent.string if request.httprequest.user_agent else ''
        user_agent = _parse_user_agent(raw_ua)

        if not activity:
            # 1. Crear nuevo registro para esta sesión activa (Primera vez)
            activity = activity_env.create({
                'user_id': user.id,
                'session_sid': session_sid,
                'ip_address': ip_addr,
                'user_agent': user_agent,
                'login_time': now_dt,
                'last_activity': now_dt
            })

            # Si está activa la prevención de logins simultáneos, revocar las OTRAS sesiones activas
            if prevent_logins:
                other_sessions = activity_env.search([
                    ('user_id', '=', user.id),
                    ('session_sid', '!=', session_sid),
                    ('is_revoked', '=', False)
                ])
                other_sessions.write({'is_revoked': True})
        else:
            # 2. Si ya existe, verificar si ha sido revocada por el administrador o por otra sesión
            if activity.is_revoked:
                request.session.logout(keep_db=True)
                return {'status': 'kicked', 'message': msg_kicked_other_device}

            # 3. Validar Expiraciones en el Servidor (por ejemplo, si el usuario regresa tras cerrar la laptop)
            # Validar Idle (Inactividad)
            if timeout_minutes > 0:
                elapsed_idle = (now_dt - activity.last_activity).total_seconds()
                if elapsed_idle > (timeout_minutes * 60):
                    activity.write({'is_revoked': True})
                    request.session.logout(keep_db=True)
                    return {'status': 'kicked', 'message': msg_timeout_inactivity}

            # Validar Límite Absoluto
            if absolute_timeout_minutes > 0:
                elapsed_absolute = (now_dt - activity.login_time).total_seconds()
                if elapsed_absolute > (absolute_timeout_minutes * 60):
                    activity.write({'is_revoked': True})
                    request.session.logout(keep_db=True)
                    return {'status': 'kicked', 'message': msg_timeout_absolute}

            # Si pasa las validaciones, actualizar la última actividad en base de datos
            activity.write({
                'last_activity': now_dt,
                'ip_address': ip_addr,
                'user_agent': user_agent
            })

        # Calcular segundos transcurridos desde el inicio de la sesión
        elapsed_seconds = (now_dt - activity.login_time).total_seconds()

        return {
            'status': 'ok',
            'timeout_minutes': timeout_minutes,
            'absolute_timeout_minutes': absolute_timeout_minutes,
            'elapsed_seconds': elapsed_seconds,
            'msg_timeout_inactivity': msg_timeout_inactivity,
            'msg_timeout_absolute': msg_timeout_absolute
        }
