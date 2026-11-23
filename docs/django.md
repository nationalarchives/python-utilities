# Django

The Django utilities require Django 6 or later and Python 3.12 or later.

Install with `pip install 'tna-utilities[django]'`.

## Cache control

These decorators match the Flask cache-control API and wrap synchronous Django views returning response objects:

```python
from django.http import HttpResponse
from tna_utilities.django import (
    cacheable_duration,
    cacheable_duration_cloudfront,
    do_not_cache,
    set_cache_control,
)


@cacheable_duration(3600)
def page(request):
    return HttpResponse("Cache for one hour")


@cacheable_duration_cloudfront(60, 3600)
def cloudfront_page(request):
    return HttpResponse("Cache for longer in CloudFront")


@do_not_cache()
def private_page(request):
    return HttpResponse("Do not cache")


@set_cache_control("private, max-age=120")
def custom_page(request):
    return HttpResponse("Custom cache policy")
```

`cacheable_duration()` defaults to 3600 seconds. CloudFront durations default to 3600 seconds; `s-maxage` is included only when the CloudFront duration is positive and differs from the client duration. The optional stale directives are included only when positive.

Like the Flask decorators, these **replace**, rather than merge, the `Cache-Control` header. When combining decorators that set it, the outermost one wins.

## Content negotiation

`get_requested_accept(options)` selects an offered media type from `Accept` and passes it to the view as `preferred_content_type`:

```python
from django.http import HttpResponse
from tna_utilities.django import get_requested_accept


@get_requested_accept(["text/html", "text/markdown"])
def page(request, preferred_content_type):
    if preferred_content_type == "text/markdown":
        return HttpResponse("# Example", content_type="text/markdown")
    return HttpResponse("<h1>Example</h1>", content_type="text/html")
```

The view must produce the chosen representation. If `Accept` is absent or empty, the argument is `None`, so the view should choose a default.

A nonempty header with no acceptable option returns an empty 406 without calling the view. An empty options list rejects every nonempty header.

Quality values, wildcards, and `q=0` exclusions are considered; ties use the order of `options`. Matching uses Django's media type parsing, so malformed headers and parameters may be interpreted differently from Flask's Werkzeug parser.

The decorator adds `Accept` to `Vary`, preserving existing values, and sets `Cache-Control: no-store` on 406 responses. Other decorators or middleware must not overwrite those headers with conflicting cache policies.

The decorator wraps synchronous views returning Django response objects.

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

By default, `default-src`, `base-uri`, `form-action` and `frame-ancestors` are `'none'`. Form submissions are blocked unless `form-action` is configured.

The mapping accepts Django's native directive values and overrides those defaults; use `None` or `False` to omit a directive.

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

Django's native CSP middleware handles report-only policies, per-view CSP decorators and nonces. To use nonces in templates, configure `django.template.context_processors.csp`; avoid caching responses containing a nonce.

See the [Django CSP documentation](https://docs.djangoproject.com/en/6.0/howto/csp/).
