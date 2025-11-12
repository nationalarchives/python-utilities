# Strings

## `slugify()`

Convert a string to a URL-friendly slug.

### Arguments

| Argument        | Description                         | Default |
| --------------- | ----------------------------------- | ------- |
| `value`         | The string to slugify               | [none]  |
| `allow_unicode` | If `True`, allow unicode characters | `False` |

### Example

```py
from tna_utils.strings import slugify

print(slugify("TNA Python Utilities Docs"))
# tna-python-utilities-docs
```

## `unslugify()`

Convert a slug back to a human-readable string.

### Arguments

| Argument           | Description                                | Default |
| ------------------ | ------------------------------------------ | ------- |
| `slug`             | The slug to unslugify                      | [none]  |
| `capitalize_first` | If `True`, capitalise the first characters | `True`  |

### Example

```py
from tna_utils.strings import unslugify

print(unslugify("tna-python-utilities-docs"))
# Tna python utilities docs
```
