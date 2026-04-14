# API

## `SimpleJsonApiClient`

### Simple example

```python
from tna_utilities.flask.api import SimpleJsonApiClient

# Create an API client with a base URL
client = SimpleJsonApiClient("https://wagtail.nationalarchives.gov.uk/api/v2")

# Get the data from the /pages/ endpoint
pages = client.get("pages")

# Get the data from the /global-notifications/ endpoint
global_notifications = client.get("global-notifications")
```

### Handling errors

```python
from tna_utilities.flask.api import SimpleJsonApiClient

client = SimpleJsonApiClient("https://wagtail.nationalarchives.gov.uk/api/v2")

try:
    pages = client.get("pages")
except Exception as error:
    print(f"An error occured with the API: {error}")
    pages = []
```

You can catch and handle some of the more common exceptions:

- `tna_utilities.flask.api.ResourceForbidden`
- `tna_utilities.flask.api.ResourceNotFound`
- `tna_utilities.flask.api.ResourceUnauthorized`

You can also catch [expections raised by `requests`](https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/).

```python
from requests import Timeout
from tna_utilities.flask.api import SimpleJsonApiClient

client = SimpleJsonApiClient("https://wagtail.nationalarchives.gov.uk/api/v2")

try:
    pages = client.get("pages")
except Timeout:
    print("The request timed out")
    pages = []
```

### Headers

```python
from tna_utilities.flask.api import SimpleJsonApiClient

# Set a default header for any request from the client
client = SimpleJsonApiClient(
    "https://wagtail.nationalarchives.gov.uk/api/v2",
    default_headers={
        "Host": "my.test.client.com"
    }
)

# Append a default header to all requests
client.add_header("Authorization", "Token abc123")

# Add a specific header to the GET request
#   Host: my.test.client.com
#   Authorization: Token abc123
#   Pragma: no-cache
pages = client.get(
    "pages",
    headers={
        "Pragma": "no-cache"
    }
)

#   Host: my.test.client.com
#   Authorization: Token abc123
global_notifications = client.get("global-notifications")
```

### Query parameters

```python
from tna_utilities.flask.api import SimpleJsonApiClient

# Append a default query parameter to all requests
client = SimpleJsonApiClient(
    "https://wagtail.nationalarchives.gov.uk/api/v2",
    default_params={
        "format": "json"
    }
)

# Append a default query parameter to all requests
client.add_parameter("limit", "100")

# https://wagtail.nationalarchives.gov.uk/api/v2/pages/?format=json&limit=100&offset=400
pages = client.get(
    "pages",
    params={
        "offset": "400"
    }
)
```
