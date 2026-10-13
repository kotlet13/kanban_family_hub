<?php
// Documentation example only: add desired settings to Kanboard's protected config.
// No database credentials, SMTP passwords, encryption keys or service accounts here.
define('FAMILYHUB_ENABLE_NATIVE_API', true);
define('FAMILYHUB_ACCOUNT_MODE', 'self_hosted');
// Legacy project invitations are separate from Native sharing and stay disabled.
define('FAMILYHUB_ENABLE_PROJECT_INVITATIONS', false);
// Empty by default: configure exact trusted proxy IPs/browser origins if needed.
define('FAMILYHUB_TRUSTED_PROXY_IPS', []);
define('FAMILYHUB_CORS_ORIGINS', []);
// Optional email/push settings are documented in README; keep secrets private.
define('FAMILYHUB_ENABLE_FCM', false);
