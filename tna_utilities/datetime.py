import datetime
import math
from typing import Optional


def get_date_from_string(date_string: str) -> datetime.datetime:  # noqa: C901
    if not date_string:
        raise ValueError("Empty string cannot be parsed as date")
    s = date_string.replace("Z", "+00:00")
    try:
        return datetime.datetime.fromisoformat(s)
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(s, "%Y-%m")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(s, "%Y")
    except ValueError:
        pass
    raise ValueError(f"Unable to parse date from string: {date_string}")


def pretty_date(s: str, show_day: bool = False, show_time: bool = False) -> str:
    if not s:
        return s
    try:
        date = datetime.datetime.strptime(s, "%Y-%m-%d")
        return date.strftime("%A %-d %B %Y") if show_day else date.strftime("%-d %B %Y")
    except ValueError:
        pass
    try:
        date = datetime.datetime.strptime(s, "%Y-%m")
        return date.strftime("%B %Y")
    except ValueError:
        pass
    try:
        date = datetime.datetime.strptime(s, "%Y")
        return date.strftime("%Y")
    except ValueError:
        pass
    try:
        date = get_date_from_string(s)
    except ValueError:
        return s
    if date:
        if show_time:
            return (
                date.strftime("%A %-d %B %Y, %H:%M")
                if show_day
                else date.strftime("%-d %B %Y, %H:%M")
            )
        return date.strftime("%A %-d %B %Y") if show_day else date.strftime("%-d %B %Y")
    return s


def pretty_datetime_range(
    s_from: Optional[str],
    s_to: Optional[str],
    lowercase_first: bool = False,
    hide_date_if_single_day: bool = False,
) -> str:
    try:
        date_from = get_date_from_string(s_from)
    except ValueError:
        date_from = None
    try:
        date_to = get_date_from_string(s_to)
    except ValueError:
        date_to = None
    if date_from and date_to:
        if (
            date_from.year == date_to.year
            and date_from.month == date_to.month
            and date_from.day == date_to.day
        ):
            if date_from.hour != date_to.hour or date_from.minute != date_to.minute:
                if hide_date_if_single_day:
                    return (
                        f"{date_from.strftime('%H:%M')} to {date_to.strftime('%H:%M')}"
                    )
                return f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%H:%M')}"
            if hide_date_if_single_day:
                return f"{date_from.strftime('%H:%M')}"
            return f"{date_from.strftime('%-d %B %Y, %H:%M')}"
        return f"{date_from.strftime('%-d %B %Y, %H:%M')} to {date_to.strftime('%-d %B %Y, %H:%M')}"
    if date_from:
        start = "from" if lowercase_first else "From"
        return f"{start} {date_from.strftime('%-d %B %Y, %H:%M')}"
    if date_to:
        start = "now to" if lowercase_first else "Now to"
        return f"{start} {date_to.strftime('%-d %B %Y, %H:%M')}"
    return f"{s_from} to {s_to}"


def pretty_date_range(  # noqa: C901
    s_from: Optional[str],
    s_to: Optional[str],
    omit_days: bool = False,
    lowercase_first: bool = False,
) -> str:
    try:
        date_from = get_date_from_string(s_from)
    except ValueError:
        date_from = None
    try:
        date_to = get_date_from_string(s_to)
    except ValueError:
        date_to = None
    if date_from and date_to:
        date_to_string = date_to.strftime("%B %Y" if omit_days else ("%-d %B %Y"))
        if (
            date_from.day == 1
            and date_from.month == 1
            and date_to.day == 31
            and date_to.month == 12
        ):
            if date_from.year == date_to.year:
                return str(date_from.year)
            return f"{date_from.year} to {date_to.year}"
        if date_from.year == date_to.year:
            if date_from.month == date_to.month:
                if date_from.day == date_to.day:
                    return date_from.strftime("%B %Y" if omit_days else "%-d %B %Y")
                if omit_days:
                    return date_to_string
                return f"{date_from.strftime('%-d')} to {date_to_string}"
            return f"{date_from.strftime('%B' if omit_days else '%-d %B')} to {date_to_string}"
        return f"{date_from.strftime('%B %Y' if omit_days else '%-d %B %Y')} to {date_to_string}"
    if date_from:
        start = "from" if lowercase_first else "From"
        return f"{start} {date_from.strftime('%B %Y' if omit_days else '%-d %B %Y')}"
    if date_to:
        start = "now to" if lowercase_first else "Now to"
        return f"{start} {date_to.strftime('%B %Y' if omit_days else '%-d %B %Y')}"
    return f"{s_from} to {s_to}"


def is_today_or_future(s: str) -> bool:
    date = get_date_from_string(s)
    today = datetime.datetime.now().date()
    return today <= date.date()


def is_today_in_date_range(s_from: str, date_to: str) -> bool:
    date_from = get_date_from_string(s_from).date()
    date_to = get_date_from_string(date_to).date()
    today = datetime.datetime.now().date()
    return date_from <= today <= date_to


def group_items_by_year_and_month(
    items: list[dict], date_key: str
) -> dict:  # noqa: C901
    grouped = []
    for item in items.get("items", []):
        if request_date := item.get(date_key):
            try:
                request_datetime = get_date_from_string(request_date)
            except ValueError:
                continue
            if request_datetime:
                month = request_datetime.strftime("%B")
                year = request_datetime.strftime("%Y")
                year_index = next(
                    (i for i, d in enumerate(grouped) if d["heading"] == year), None
                )
                if year_index is None:
                    grouped.append(
                        {
                            "heading": year,
                            "items": [{"heading": month, "items": [item]}],
                        }
                    )
                else:
                    month_index = next(
                        (
                            i
                            for i, m in enumerate(grouped[year_index]["items"])
                            if m["heading"] == month
                        ),
                        None,
                    )
                    if month_index is None:
                        grouped[year_index]["items"].append(
                            {"heading": month, "items": [item]}
                        )
                    else:
                        grouped[year_index]["items"][month_index]["items"].append(item)
    return grouped


def seconds_to_iso_8601_duration(total_seconds: int) -> str:
    if not total_seconds:
        return "PT0S"
    hours = math.floor(total_seconds / 3600)
    minutes = math.floor((total_seconds - (hours * 3600)) / 60)
    seconds = total_seconds - (hours * 3600) - (minutes * 60)
    if hours:
        return f"PT{hours}H{minutes}M{seconds}S"
    if minutes:
        return f"PT{minutes}M{seconds}S"
    return f"PT{seconds}S"


def seconds_to_duration(total_seconds: int) -> str:
    if not total_seconds:
        return "00h 00m 00s"
    hours = math.floor(total_seconds / 3600)
    minutes = math.floor((total_seconds - (hours * 3600)) / 60)
    seconds = total_seconds - (hours * 3600) - (minutes * 60)
    return f"{str(hours).rjust(2, '0')}h {str(minutes).rjust(2, '0')}m {str(seconds).rjust(2, '0')}s"


def rfc_822_date_format(s: str) -> str:
    if not s:
        return s
    try:
        date = get_date_from_string(s)
        return date.strftime("%a, %-d %b %Y %H:%M:%S GMT")
    except ValueError:
        pass
    return s
