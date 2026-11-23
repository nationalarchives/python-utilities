from collections.abc import Mapping
from copy import deepcopy

from django.utils.csp import CSP

from ..security import GOOGLE_CSP_DIRECTIVES, TYPEKIT_CSP_DIRECTIVES, CspGenerator


def csp_settings(
    content_security_policy: Mapping[str, object] | None = None,
    *,
    allow_google_content_security_policy: bool = False,
    allow_typekit_content_security_policy: bool = False,
) -> dict[str, object]:
    """Return a CSP mapping for Django 6's native CSP middleware."""
    csp: dict[str, object] = {
        directive: sources for directive, sources in CspGenerator().to_dict().items()
    }
    if content_security_policy is not None:
        csp.update(deepcopy(dict(content_security_policy)))

    providers = []
    if allow_google_content_security_policy:
        providers.append(GOOGLE_CSP_DIRECTIVES)
    if allow_typekit_content_security_policy:
        providers.append(TYPEKIT_CSP_DIRECTIVES)
    for provider in providers:
        for directive, additions in provider.items():
            if directive not in csp:
                sources = [CSP.SELF]
            else:
                value = csp[directive]
                if value is None or value is False:
                    continue
                if isinstance(value, str):
                    sources = [value]
                elif isinstance(value, (list, tuple, set)) and all(
                    isinstance(source, str) for source in value
                ):
                    sources = sorted(value) if isinstance(value, set) else list(value)
                else:
                    raise ValueError(f"{directive} must contain CSP source strings")
                if sources == [CSP.NONE]:
                    sources = [CSP.SELF]
                elif CSP.SELF not in sources and CSP.NONE not in sources:
                    sources.insert(0, CSP.SELF)
            for source in additions:
                if source not in sources:
                    sources.append(source)
            csp[directive] = sources
    return csp


def security_settings(
    *,
    debug: bool = False,
    content_security_policy: Mapping[str, object] | None = None,
    allow_google_content_security_policy: bool = False,
    allow_typekit_content_security_policy: bool = False,
    referrer_policy: str = "strict-origin-when-cross-origin",
    force_https: bool = True,
    session_cookie_secure: bool = False,
) -> dict[str, object]:
    """Return native Django settings for CSP, HTTPS, headers and cookies."""
    return {
        "SECURE_CSP": csp_settings(
            content_security_policy,
            allow_google_content_security_policy=allow_google_content_security_policy,
            allow_typekit_content_security_policy=allow_typekit_content_security_policy,
        ),
        "SECURE_SSL_REDIRECT": force_https and not debug,
        "SECURE_REFERRER_POLICY": referrer_policy,
        "SECURE_CONTENT_TYPE_NOSNIFF": True,
        "SECURE_CROSS_ORIGIN_OPENER_POLICY": "same-origin",
        "SESSION_COOKIE_SECURE": session_cookie_secure or (force_https and not debug),
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_AGE": 60 * 60 * 24,
    }
