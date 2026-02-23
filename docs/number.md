# Number

Added in `v1.2.0`.

## `numberish()`

Formats a number as an approximate, human-readable value.

### Arguments

| Argument       | Description                       | Default  |
| -------------- | --------------------------------- | -------- |
| `value`        | The value to format               | [none]   |
| `simple_units` | If `True`, use simple units       | `False`  |
| `prefix_text`  | Custom prefix for rounded numbers | `About ` |

`prefix_text` can be a string or a tuple of two strings where the values are used when the value was rounded up or down.

### Example

```python
from tna_utilities.number import numberish

print(numberish(67))
# 67

print(numberish(123456789))
# About 120 million

print(numberish(1337, simple_units=True, prefix_text="~"))
# ~1.3k
```

## `pretty_file_size()`

Added in `v1.3.0`.

Formats file size to a human-readable string.

### Arguments

| Argument   | Description                                                | Default |
| ---------- | ---------------------------------------------------------- | ------- |
| `bytes`    | The number of bytes                                        | [none]  |
| `simplify` | If `True`, simplify the string and remove fractional sizes | `True`  |

### Example

```python
from tna_utilities.number import pretty_file_size

print(pretty_file_size(1337))
# 1kB

print(pretty_file_size(1337, simplify=False))
# 1.337kB
```
