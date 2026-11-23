# Currency

All three functions accept `decimals` before `simplify`. If you previously
passed `simplify` or `currency_symbol` positionally, use keyword arguments or
include `decimals` in the new position.

## `currency()`

Formats a number as a currency without the currency symbol.

### Arguments

| Argument   | Description                                                | Default |
| ---------- | ---------------------------------------------------------- | ------- |
| `value`    | The value to format                                        | [none]  |
| `decimals` | Number of decimal places to show for non-simplified values | `2`     |
| `simplify` | If `True`, remove the decimal places for whole numbers     | `True`  |

For a numeric zero, `currency()` returns `"0"` when simplified and `"0.00"`
otherwise, regardless of `decimals`.

### Example

```python
from tna_utilities.currency import currency

print(currency(5))
# 5

print(currency(5, simplify=False))
# 5.00

print(currency(5.2))
# 5.20

print(currency(5.125, decimals=3))
# 5.125
```

## `pretty_price()`

Formats a number as a price.

### Arguments

| Argument          | Description                                                | Default |
| ----------------- | ---------------------------------------------------------- | ------- |
| `value`           | The value to format                                        | [none]  |
| `decimals`        | Number of decimal places to show for non-simplified values | `2`     |
| `simplify`        | If `True`, remove the decimal places for whole numbers     | `True`  |
| `currency_symbol` | The currency symbol to use                                 | `£`     |

Values that round to zero at two decimal places are displayed as `"Free"`,
regardless of `decimals`.

### Example

```python
from tna_utilities.currency import pretty_price

print(pretty_price(5))
# £5

print(pretty_price(5, simplify=False))
# £5.00

print(pretty_price(5, currency_symbol="€"))
# €5

print(pretty_price(5, decimals=3, simplify=False))
# £5.000
```

## `pretty_price_range()`

Formats a price range.

### Arguments

| Argument          | Description                                                | Default |
| ----------------- | ---------------------------------------------------------- | ------- |
| `value_from`      | The starting value                                         | `None`  |
| `value_to`        | The ending value                                           | `None`  |
| `decimals`        | Number of decimal places to show for non-simplified values | `2`     |
| `simplify`        | If `True`, remove the decimal places for whole numbers     | `True`  |
| `currency_symbol` | The currency symbol to use                                 | `£`     |

When both values are nonzero, they are displayed in ascending order. Price
formatting, including the `"Free"` rule above, applies to each endpoint.

### Example

```python
from tna_utilities.currency import pretty_price_range

print(pretty_price_range(5, 10))
# £5 to £10

print(pretty_price_range(0, 15))
# Free to £15

print(pretty_price_range(10, 0))
# From £10

print(pretty_price_range(5.125, 10.125, decimals=3))
# £5.125 to £10.125
```
