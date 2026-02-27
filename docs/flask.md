# Flask

> Added in `v1.4.0`.

## `Talisman`

A stripped-down and opinionated reproduction of [wntrblm/flask-talisman](https://github.com/wntrblm/flask-talisman) which is a fork of [GoogleCloudPlatform/flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman).

### Examples

```python
from flask import Flask
from tna_utilities.flask.talisman import Talisman

app = Flask(__name__)
Talisman(app)
```
