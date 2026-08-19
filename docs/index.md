# TNA Python Utilities

This is a library of common Python functions, some specific to The National Archives to help speed up some aspects of Python application development.

- [API](./api.md)
- [Components](./component.md)
- [Currency](./currency.md)
- [Dates and times](./dates-and-times.md)
- [Numbers](./number.md)
- [Security](./security.md)
- [Strings](./string.md)
- [URLs](./url.md)

## Optional modules

- [Flask](./flask.md)

[Read the changelog](https://github.com/nationalarchives/python-utilities/blob/main/CHANGELOG.md).

## Root-level functions

### `strtobool()`

Converts a string to boolean based on a number of predefined truthy and falsy values.

#### Arguments

| Argument | Description          | Default |
| -------- | -------------------- | ------- |
| `value`  | The value to convert | [none]  |

#### Example

```python
from tna_utilities import strtobool

print(strtobool("yes"))
# True

print(strtobool("0"))
# False

print(strtobool("maybe"))  # Raises ValueError: Invalid truth value

print(strtobool(True))  # Raises TypeError: Invalid truth value
```
