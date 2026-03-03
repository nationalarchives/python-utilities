import math
import re
from typing import Union


def round_to_significant_figures(value: float, sig_figs: int = 1) -> float:
    """
    Round a positive float to the given number of significant figures.

    This computes the appropriate number of decimal places for ``round`` based
    on the order of magnitude of ``value``. For example, with ``sig_figs=1``,
    values are rounded to one significant figure (e.g. 1234 -> 1000, 0.0123 -> 0.01).
    """
    if value == 0:
        return 0.0
    # Determine how many decimal places are needed so that ``round`` keeps
    # ``sig_figs`` significant digits.
    decimal_places = -int(math.floor(math.log10(abs(value)))) + (sig_figs - 1)
    return round(value, decimal_places)


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
            # Round to one significant figure to produce a human-friendly value,
            # e.g. 1234 -> 1000, 1.23 -> 1, 0.0123 -> 0.01.
            base_value_rounded = round_to_significant_figures(base_value, 1)
            if base_value_rounded == base_value:
                prefix_text = ""
            elif isinstance(prefix_text, tuple):
                if len(prefix_text) != 2:
                    raise ValueError("prefix_text tuple must have exactly two elements")
                if not all(isinstance(pt, str) for pt in prefix_text):
                    raise ValueError(
                        "Both elements of the prefix_text tuple must be strings"
                    )
                approximation_is_over = base_value_rounded * threshold - value >= 0
                prefix_text = (
                    prefix_text[0] if approximation_is_over else prefix_text[1]
                )
            return f"{prefix_text}{base_value_rounded:g}{unit}"
    return str(int(value))


def pretty_file_size(bytes, simplify=True):
    if not isinstance(bytes, int):
        raise ValueError("file_size must be an integer")
    byte_unit = 1000
    suffixes = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = 0
    prettified_file_size = bytes
    while prettified_file_size >= byte_unit and i < len(suffixes) - 1:
        prettified_file_size /= byte_unit
        i += 1
    if prettified_file_size == 0:
        return "0B"
    if simplify:
        prettified_file_size = f"{prettified_file_size:.{max(i - 1, 0)}f}"
    else:
        prettified_file_size = round(prettified_file_size, 3)
    prettified_file_size = re.sub(r"(\.0*)$", "", str(prettified_file_size))
    return f"{prettified_file_size}{suffixes[i]}"
