# Security

> Added in `v1.3.0`.

## `CspGenerator`

A utility class to generate a CSP.

### Examples

```python
from tna_utilities.security import CspGenerator

generator = CspGenerator()

# Add a single directive source (plus 'self')
generator.script_src("example.com")

# Add multiple sources for a directive (plus 'self')
generator.style_src("example.com", "another.net")

# Add a directive source without allowing 'self'
generator.object_src("example.com", omit_self=True)

# Disallow a directive
generator.disallow("worker-src")

generator.to_string()
# default-src 'self'; script-src 'self' example.com; style-src 'self' example.com another.net; object-src example.com; worker-src 'none';
```

## `common_security_headers`

> Renamed from `security_headers` in `v1.4.0`.

Get a dictionary of common security headers.

### Arguments

| Argument                            | Description                                                   | Default       |
| ----------------------------------- | ------------------------------------------------------------- | ------------- |
| `cross_origin_embedder_policy`      | The option for the `Cross-Origin-Embedder-Policy` header      | `unsafe-none` |
| `cross_origin_opener_policy`        | The option for the `Cross-Origin-Opener-Policy` header        | `same-origin` |
| `cross_origin_resource_policy`      | The option for the `Cross-Origin-Resource-Policy` header      | `same-origin` |
| `x_content_type_options`            | The option for the `X-Content-Type-Options` header            | `no-sniff`    |
| `x_permitted_cross_domain_policies` | The option for the `X-Permitted-Cross-Domain-Policies` header | `none`        |

### Example

```python
from tna_utilities.security import security_headers

print(security_headers())
# {
#   "Cross-Origin-Embedder-Policy": "unsafe-none",
#   "Cross-Origin-Opener-Policy": "same-origin",
#   "Cross-Origin-Resource-Policy": "same-origin",
#   "X-Permitted-Cross-Domain-Policies": "none",
#   "X-Content-Type-Options": "no-sniff",
# }
```
