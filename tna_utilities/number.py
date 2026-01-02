from typing import Union


def numberish(
    value: Union[float, int],
    simple_units: bool = False,
    prefix_text: Union[str, tuple[str, str]] = "About ",
) -> str:
    """
    Convert a number into a human-readable string with appropriate units.
    """

    if not isinstance(value, (int, float)):
        raise ValueError("Value must be an integer or float")
    if value == 0:
        return "None"
    if value < 1000:
        return str(int(value))
    units = [
        ("billion", "b", 1_000_000_000),
        ("million", "m", 1_000_000),
        ("thousand", "k", 1_000),
    ]
    for unit_full, unit_simple, threshold in units:
        if value >= threshold:
            unit = unit_simple if simple_units else " " + unit_full
            base_value = value / threshold
            if base_value.is_integer():
                return f"{int(base_value)}{unit}"
            base_value_rounded = float(f"{base_value:.2g}")
            if base_value_rounded == base_value:
                prefix_text = ""
            elif isinstance(prefix_text, tuple):
                if len(prefix_text) != 2:
                    raise ValueError("prefix_text tuple must have exactly two elements")
                if not all(isinstance(pt, str) for pt in prefix_text):
                    raise ValueError(
                        "Both elements of the prefix_text tuple must be strings"
                    )
                is_approximation_high = base_value_rounded * threshold - value >= 0
                prefix_text = (
                    prefix_text[0] if is_approximation_high else prefix_text[1]
                )
            return f"{prefix_text}{base_value_rounded:g}{unit}"
