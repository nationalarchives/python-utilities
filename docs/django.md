# Django

The Django utilities require Django 6 or later and Python 3.12 or later.

Install with `pip install 'tna-utilities[django]'`.

## CSP settings

Use `csp_settings()` to build a policy for Django's native CSP middleware:

```python
from django.utils.csp import CSP
from tna_utilities.django import csp_settings

SECURE_CSP = csp_settings(
    {
        "form-action": [CSP.SELF],
        "script-src": [CSP.SELF, CSP.NONCE],
    },
    allow_google_content_security_policy=True,
)

# Add this to your existing MIDDLEWARE setting.
MIDDLEWARE += ["django.middleware.csp.ContentSecurityPolicyMiddleware"]
```

By default, `default-src`, `base-uri`, `form-action` and `frame-ancestors` are `'none'`. Form submissions are blocked unless `form-action` is configured. The mapping accepts Django's native directive values and overrides those defaults; use `None` or `False` to omit a directive.

The optional `allow_google_content_security_policy` and `allow_typekit_content_security_policy` arguments add the same allowlists as the Flask utility. They add `'self'` to the affected directives unless the existing sources contain `'none'`; a sole `'none'` is replaced by `'self'` and the provider sources.

## Security settings

`security_settings()` returns a dictionary of native Django settings, including `SECURE_CSP`. It accepts the same CSP arguments as `csp_settings()` via `content_security_policy` and the provider options:

```python
from django.utils.csp import CSP
from tna_utilities.django import security_settings

security = security_settings(
    debug=DEBUG,
    content_security_policy={"form-action": [CSP.SELF]},
)
SECURE_CSP = security["SECURE_CSP"]
SECURE_SSL_REDIRECT = security["SECURE_SSL_REDIRECT"]
# Apply other returned settings explicitly if desired.
```

The helper does not change settings or middleware itself. Its other returned keys are:

- `SECURE_REFERRER_POLICY`
- `SECURE_CONTENT_TYPE_NOSNIFF`
- `SECURE_CROSS_ORIGIN_OPENER_POLICY`
- `SESSION_COOKIE_SECURE`
- `SESSION_COOKIE_HTTPONLY`
- `SESSION_COOKIE_SAMESITE`
- `SESSION_COOKIE_AGE` (one day)

Pass `session_cookie_secure=True` to retain secure cookies when HTTPS redirects are disabled.

`force_https=False` disables redirects; `debug=True` disables them for development.

Use Django's `django.middleware.security.SecurityMiddleware` for security headers and HTTPS redirects, and keep `django.contrib.sessions.middleware.SessionMiddleware` for sessions. Django's HTTPS redirects are permanent (301).

Configure Django's `SECURE_SSL_HOST`, `SECURE_REDIRECT_EXEMPT` and `SECURE_PROXY_SSL_HEADER` settings as appropriate for your deployment. Do not trust forwarded headers from arbitrary clients.

Django's native CSP middleware handles report-only policies, per-view CSP decorators and nonces. To use nonces in templates, configure `django.template.context_processors.csp`; avoid caching responses containing a nonce. See the [Django CSP documentation](https://docs.djangoproject.com/en/6.0/howto/csp/).
