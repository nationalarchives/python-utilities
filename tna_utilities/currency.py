def currency(s: float | str | int) -> str:
    if not s:
        return "0"
    float_number = float(s)
    int_number = int(float_number)
    if int_number == float_number:
        return str("{:,}".format(int_number))
    return str("{:,.2f}".format(float_number))


def pretty_price(s: float | str | int) -> str:
    price = s if s else 0
    if price == 0 or price == "0":
        return "Free"
    return f"£{currency(price)}"


def pretty_price_range(
    from_in: float | str | int = 0, to_in: float | str | int = 0
) -> str:
    from_float = float(from_in) or 0
    to_float = float(to_in) or 0
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
