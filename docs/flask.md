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
    cacheable_duration_cloudfront
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
    return "Cache me in client caches for up to an hour and in Cloudfront for up to a day"
```

### Vary

> Added in `v1.6.0`.

Decorators to help set the `Vary` response header of a route.

### Examples

```python
from flask import Flask
from tna_utilities.flask import vary_by_cookies, vary_by_headers

app = Flask(__name__)

@app.route("/vary-cookies/")
@vary_by_cookies()
def response_varies_based_on_cookies():
    return "Send different cookies to get a different response"

@app.route("/vary-accept/")
@vary_by_headers("Accept")
def response_varies_based_on_accept_header():
    return "Send a request with a different Accept header to get a different response"
```

## `Talisman`

> Added in `v1.4.0`.

A stripped-down and opinionated reproduction of [wntrblm/flask-talisman](https://github.com/wntrblm/flask-talisman) which is a fork of [GoogleCloudPlatform/flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman).

### Examples

```python
from flask import Flask
from tna_utilities.flask import Talisman

app = Flask(__name__)
Talisman(app)
```
