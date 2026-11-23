# Flask

## Cache control

> Added in `v1.5.0`.

A set of decorators to manage the `Cache-Control` response header of a route.

### Examples

```python
from flask import Flask
from tna_utilities.flask import (
    cacheable_duration,
    do_not_cache,
    set_cache_control,
    cacheable_duration_cloudfront,
)

app = Flask(__name__)


@app.route("/default/")
def default():
    return "No cache instructions given"


@app.route("/cacheable/")
@cacheable_duration(3600)
def cachable_for_up_to_1h():
    return "You can cache me for up to an hour"


@app.route("/not-cacheable/")
@do_not_cache()
def not_cachable():
    return "Don't cache me!"


@app.route("/custom-cache/")
@set_cache_control("private, max-age=120")
def custom_cache():
    return "Cache me in private caches for up to 2 minutes"


@app.route("/cloudfront-cache/")
@cacheable_duration_cloudfront(3600, 86400)
def cloudfront_cache():
    return (
        "Cache me in client caches for up to an hour and in Cloudfront for up to a day"
    )
```

## Content negotiation

`get_requested_accept(options)` selects an offered media type from the request's `Accept` header and passes it to the view as `preferred_content_type`. The view is responsible for producing the corresponding representation and content type:

```python
from flask import Flask, Response
from tna_utilities.flask import get_requested_accept

app = Flask(__name__)


@app.get("/page/")
@get_requested_accept(["text/html", "text/markdown"])
def page(preferred_content_type):
    if preferred_content_type == "text/markdown":
        return Response("# Example", content_type="text/markdown")
    return Response("<h1>Example</h1>", content_type="text/html")
```

Quality values, wildcards, and exclusions (`q=0`) are handled by Flask's Werkzeug negotiation. Ties use the order of `options`.

If the header is absent or empty, `preferred_content_type` is `None`; choose a default in the view. If a nonempty header matches no option, the view is not called and an empty 406 response is returned. An empty options list therefore rejects every nonempty `Accept` header.

The decorator adds `Accept` to `Vary`, preserving existing values, and sets `Cache-Control: no-store` on 406 responses. Other decorators or middleware must not overwrite those headers with conflicting cache policies.

## `Talisman`

> Added in `v1.4.0`.

A stripped-down and opinionated reproduction of [wntrblm/flask-talisman](https://github.com/wntrblm/flask-talisman) which is a fork of [GoogleCloudPlatform/flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman).

Talisman preserves `SESSION_COOKIE_SECURE=True` when configured before initialisation, including in debug mode or when `force_https=False`. Otherwise, it enables secure session cookies when `force_https=True` and debug mode is off.

By default, the CSP sets `default-src`, `base-uri`, `form-action` and `frame-ancestors` to `'none'`. In particular, form submissions are blocked unless `form-action` is configured in `content_security_policy`.

### Examples

```python
from flask import Flask
from tna_utilities.flask import Talisman

app = Flask(__name__)
Talisman(
    app,
    content_security_policy={
        "form-action": ["'self'"],
        "img-src": ["img.example.com"],
        "sandbox": [
            "allow-scripts",
            "allow-downloads",
            "allow-forms",
            "allow-same-origin",
            "allow-popups",
        ],
    },
    allow_google_content_security_policy=True,
)
```
