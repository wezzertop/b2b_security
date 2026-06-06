# B2B Security: Restrict Logins & Session Timeout

This module provides advanced control over user sessions for B2B portals in Odoo. It is designed to improve security and control customer access to the portal.

## Main Features

1. **Restrict Simultaneous Accesses**: Prevents the same account from logging in from different devices or browsers at the same time.
2. **Inactivity Logout**: Sets a maximum inactivity time (in minutes). If the user does not interact with the platform in that time, their session will expire.
3. **Absolute Expiration (Optional)**: Forces logout after a certain time, regardless of user activity.
4. **Professional & Customizable Notifications**: Provides complete control over the messages shown to users when they are logged out. You can define specific, professional alerts for when a session expires due to inactivity, maximum time reached, or when a login occurs from another device.

## Installation

1. Download and extract the `b2b_security` folder in your Odoo `addons` directory.
2. Update the apps list (Activate Developer Mode -> Apps -> Update Apps List).
3. Search for `B2B Security` in the apps list.
4. Click **Install**.

## Configuration and Usage

All configuration is done from the Odoo settings menu:

1. Go to **Settings** > **General Settings**.
2. Scroll down until you find the **B2B Security** section.
3. **Prevent Simultaneous Logins**: Check this box to prevent the same account from being used in multiple places at the same time.
4. **Inactivity Timeout (minutes)**: Enter the time in minutes after which an inactive session will automatically close (e.g. 30 minutes).
5. **Absolute forced logout**: Check this box if you want to set a maximum time limit for a session (e.g. 480 minutes), after which it will close even if the user is active.
6. **Logout Messages (Mensajes de Cierre de Sesión)**: Fill in your custom texts to communicate professionally with your users in each logout scenario.

## Support

If you have any problems, questions, or need custom development, do not hesitate to contact the author.

**Author**: JDDM
