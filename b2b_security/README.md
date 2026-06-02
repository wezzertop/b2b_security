# B2B Security: Restrict Logins & Session Timeout

Este módulo proporciona control avanzado sobre las sesiones de usuario para portales B2B en Odoo. Está diseñado para mejorar la seguridad y controlar el acceso de los clientes al portal.

## Características Principales

1. **Restricción de Accesos Simultáneos**: Evita que una misma cuenta inicie sesión desde diferentes dispositivos o navegadores al mismo tiempo.
2. **Cierre de Sesión por Inactividad**: Establece un tiempo máximo de inactividad (en minutos). Si el usuario no interactúa con la plataforma en ese tiempo, su sesión expirará.
3. **Expiración Absoluta (Opcional)**: Fuerza el cierre de sesión tras un tiempo determinado, independientemente de la actividad del usuario.

## Instalación

1. Descarga y extrae la carpeta `b2b_security` en el directorio de `addons` de tu instancia de Odoo 18.0.
2. Actualiza la lista de aplicaciones (Activa el Modo Desarrollador -> Aplicaciones -> Actualizar Lista de Aplicaciones).
3. Busca `B2B Security` en la lista de aplicaciones.
4. Haz clic en **Instalar**.

## Configuración y Uso

Toda la configuración se realiza desde el menú de ajustes de Odoo:

1. Ve a **Ajustes** > **Ajustes Generales**.
2. Desplázate hacia abajo hasta encontrar la sección **Seguridad B2B**.
3. **Evitar Inicios de Sesión Simultáneos**: Marca esta casilla para evitar que la misma cuenta se use en múltiples lugares al mismo tiempo.
4. **Tiempo de Inactividad (minutos)**: Introduce el tiempo en minutos tras el cual una sesión inactiva se cerrará automáticamente (ej. 30 minutos).
5. **Cierre de sesión forzado absoluto**: Marca esta casilla si deseas establecer un límite máximo de tiempo para una sesión (ej. 480 minutos), tras el cual se cerrará incluso si el usuario está activo.

## Soporte

Si tienes algún problema, duda o necesitas desarrollo a medida, no dudes en contactar al autor.

**Autor**: JDDM
