from typing import Optional, Union


def currency(value: Union[float, str, int], simplify_output: bool = True) -> str:
    """
    Formats a number as a currency without the currency symbol.

    If simplify_output is True, removes unnecessary decimal places for whole numbers.
    """
    if not value:
        return "0" if simplify_output else "0.00"

    float_number = float(value)
    int_number = int(float_number)

    if simplify_output and int_number == float_number:
        return str("{:,}".format(int_number))

    return str("{:,.2f}".format(float_number))


def pretty_price(
    value: Union[float, str, int],
    simplify_output: bool = True,
    currency_symbol: str = "£",
) -> str:
    """
    Formats a number as a price.

    If the value is 0, returns "Free".
    Otherwise, returns the currency symbol followed by the formatted currency.
    """
    if value == 0 or value == "0" or round(float(value) * 100) == 0:
        return "Free"

    return f"{currency_symbol}{currency(value, simplify_output)}"


def pretty_price_range(
    from_in: Optional[Union[float, str, int]] = 0,
    to_in: Optional[Union[float, str, int]] = 0,
) -> str:
    """
    Formats a price range.

    If both from_in and to_in are 0 or None, returns "Free".
    If from_in equals to_in, returns the pretty price of that value.
    If from_in is 0 or None, returns "Free to {to_in}".
    If to_in is 0 or None, returns "From {from_in}".
    Otherwise, returns "{min_price} to {max_price}".
    """
    from_float = float(from_in) if from_in else 0
    to_float = float(to_in) if to_in else 0

    if from_float == 0 and to_float == 0:
        return "Free"

    if from_float == to_float:
        return pretty_price(from_float)

    if from_float == 0:
        return f"Free to {pretty_price(to_float)}"

    if to_float == 0:
        return f"From {pretty_price(from_float)}"

    min_price = min(float(from_float), float(to_float))
    max_price = max(float(from_float), float(to_float))
    return f"{pretty_price(min_price)} to {pretty_price(max_price)}"
