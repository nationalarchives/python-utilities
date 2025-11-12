# Currency

## `currency()`

Formats a number as a currency without the currency symbol.

### Arguments

| Argument   | Description                                                     | Default |
| ---------- | --------------------------------------------------------------- | ------- |
| `value`    | The value to format                                             | [none]  |
| `simplify` | If `True`, remove the decimal values for whole number of pounds | `True`  |

### Example

```py
from tna_utils.currency import currency

print(currency(5))
# 5.00

print(currency(5, simplify=True))
# 5

print(currency(5.2))
# 5.20
```

## `pretty_price()`

Formats a number as a price.

### Arguments

| Argument          | Description                                                     | Default |
| ----------------- | --------------------------------------------------------------- | ------- |
| `value`           | The value to format                                             | [none]  |
| `simplify`        | If `True`, remove the decimal values for whole number of pounds | `True`  |
| `currency_symbol` | The currency sybmol to use                                      | `£`     |

### Example

```py
from tna_utils.currency import pretty_price

print(pretty_price(5))
# £5.00

print(pretty_price(5, simplify=True))
# £5

print(pretty_price(5, currency_symbol="€"))
# €5.00
```

## `pretty_price_range()`

Formats a price range.

### Arguments

| Argument          | Description                                                     | Default |
| ----------------- | --------------------------------------------------------------- | ------- |
| `value_from`      | The lower value                                                 | `None`  |
| `value_to`        | The higher value                                                | `None`  |
| `simplify`        | If `True`, remove the decimal values for whole number of pounds | `True`  |
| `currency_symbol` | The currency sybmol to use                                      | `£`     |

### Example

```py
from tna_utils.currency import pretty_price_range

print(pretty_price_range(5, 10))
# £5.00 to £10

print(pretty_price_range(0, 15))
# Free to £15.00

print(pretty_price_range(10, 0))
# From £10.00
```
