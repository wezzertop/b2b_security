/** @odoo-module **/

import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

export const sessionSecurityService = {
    dependencies: [],
    start(env) {
        let lastActivity = Date.now();
        let timeoutMinutes = 0;
        let pingInterval = null;

        const resetActivity = () => {
            lastActivity = Date.now();
        };

        window.addEventListener("mousemove", resetActivity);
        window.addEventListener("keydown", resetActivity);
        window.addEventListener("click", resetActivity);
        window.addEventListener("scroll", resetActivity);

        const checkSecurity = async () => {
            try {
                const response = await fetch("/b2b_security/ping", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        jsonrpc: "2.0",
                        method: "call",
                        params: {},
                        id: Math.floor(Math.random() * 1000000000)
                    })
                });
                
                const json = await response.json();
                if (json.error) {
                    return; // Ignorar errores de red o autenticación
                }
                
                const result = json.result;
                
                if (result && result.status === "kicked") {
                    window.alert(result.message || "Su sesión ha sido cerrada desde otro dispositivo o por el administrador.");
                    browser.location.href = "/web/session/logout?redirect=/web/login";
                    return;
                }
                
                if (result && result.timeout_minutes !== undefined) {
                    timeoutMinutes = result.timeout_minutes;
                }
                
                if (timeoutMinutes > 0) {
                    const elapsedMs = Date.now() - lastActivity;
                    const timeoutMs = timeoutMinutes * 60 * 1000;
                    
                    if (elapsedMs > timeoutMs) {
                        window.alert(result.msg_timeout_inactivity || "Su sesión ha expirado por inactividad.");
                        browser.location.href = "/web/session/logout?redirect=/web/login";
                        return;
                    }
                }

                if (result && result.absolute_timeout_minutes > 0) {
                    const elapsedSeconds = result.elapsed_seconds;
                    const timeoutSeconds = result.absolute_timeout_minutes * 60;
                    
                    if (elapsedSeconds > timeoutSeconds) {
                        window.alert(result.msg_timeout_absolute || "Su sesión ha alcanzado el límite máximo de tiempo permitido.");
                        browser.location.href = "/web/session/logout?redirect=/web/login";
                        return;
                    }
                }
            } catch (error) {
                console.warn("[b2b_security] Ping falló (posible desconexión).");
            }
        };

        // Enviar ping cada 30 segundos
        pingInterval = browser.setInterval(checkSecurity, 30000);
        
        // Retrasamos el primer ping unos segundos para no bloquear la carga inicial
        browser.setTimeout(checkSecurity, 5000);
    }
};

registry.category("services").add("b2b_session_security", sessionSecurityService);
