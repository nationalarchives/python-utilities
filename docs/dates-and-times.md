# Dates and times

## get_date_from_string()

Parses a date string into a datetime object.

### Arguments

| Argument      | Description        | Default |
| ------------- | ------------------ | ------- |
| `date_string` | The value to parse | [none]  |

### Example

```python
from tna_utilities.datetime import get_date_from_string

print(get_date_from_string("2006-05-04T01:02:03"))
# datetime.datetime(2006, 5, 4, 1, 2, 3)

print(get_date_from_string("2006-05-04T01:02:03+01:00"))
# datetime.datetime(2006, 5, 4, 1, 2, 3, tzinfo=datetime.timezone(datetime.timedelta(hours=1)))
```

## pretty_date()

Formats a date into the format used by The National Archives.

### Arguments

| Argument   | Description                                                                                | Default |
| ---------- | ------------------------------------------------------------------------------------------ | ------- |
| `date`     | A date or datetime object or the date string in either YYYY-MM-DD, YYYY-MM, or YYYY format | [none]  |
| `show_day` | If `True`, show the day (Monday-Sunday)                                                    | `False` |

### Example

```python
from tna_utilities.datetime import pretty_date

print(pretty_date("2000-01-01T12:00:00Z"))
# 1 January 2000

print(pretty_date(datetime.date(2000, 12, 31), show_day=True))
# Sunday 31 December 2000
```

## pretty_datetime()

Formats a date and time into the format used by The National Archives.

### Arguments

| Argument       | Description                                     | Default |
| -------------- | ----------------------------------------------- | ------- |
| `date`         | The date to format                              | [none]  |
| `show_day`     | If `True`, show the day (Monday-Sunday)         | `False` |
| `show_seconds` | If `True`, show the seconds (added in `v1.4.0`) | `False` |

### Example

```python
from tna_utilities.datetime import pretty_datetime

print(pretty_datetime("2000-01-01T12:00:00Z"))
# 1 January 2000, 12:00

print(pretty_datetime(datetime.datetime(2000, 12, 31, 12, 30, 0), show_day=True))
# Sunday 31 December 2000, 12:30
```

## pretty_date_range()

Formats a date range into the format used by The National Archives.

### Arguments

| Argument          | Description                                                                                 | Default |
| ----------------- | ------------------------------------------------------------------------------------------- | ------- |
| `date_from`       | The start date                                                                              | [none]  |
| `date_to`         | The end date                                                                                | [none]  |
| `omit_days`       | If `True`, don't output the day of month, only the month and year range                     | `False` |
| `lowercase_first` | If `True`, use `from` and `now to` for ranges that normally start `From...` and `Now to...` | `False` |
| `show_seconds`    | If `True`, show the seconds (added in `v1.4.0`)                                             | `False` |

### Example

```python
from tna_utilities.datetime import pretty_date_range

print(pretty_date_range(datetime.date(2000, 1, 1), "2000-01-02"))
# 1 to 2 January 2000

print(pretty_date_range(datetime.date(2000, 1, 1), datetime.date(2000, 2, 1)))
# 1 January to 1 February 2000

print(pretty_date_range(datetime.date(2000, 1, 1), datetime.date(2000, 12, 31)))
# 2000

print(pretty_date_range(datetime.date(2000, 1, 1), None))
# From 1 January 2000
```

## pretty_datetime_range()

Formats a date/time range into the format used by The National Archives.

### Arguments

| Argument                  | Description                                                                                 | Default |
| ------------------------- | ------------------------------------------------------------------------------------------- | ------- |
| `date_from`               | The start datetime                                                                          | [none]  |
| `date_to`                 | The end datetime                                                                            | [none]  |
| `lowercase_first`         | If `True`, use `from` and `now to` for ranges that normally start `From...` and `Now to...` | `False` |
| `hide_date_if_single_day` | If `True`, only show a time range if the start and end date are the same                    | `False` |

### Example

```python
from tna_utilities.datetime import pretty_datetime_range

print(pretty_datetime_range(datetime.datetime(2000, 1, 1, 12, 30, 0), "2000-01-01T12:45:00Z"))
# 1 January 2000, 12:30 to 12:45

print(pretty_datetime_range(datetime.datetime(2000, 1, 1, 12, 30, 0), datetime.datetime(2001, 2, 2, 14, 45, 0)))
# 1 January 2000, 12:30 to 2 February 2001, 14:45

print(pretty_datetime_range(datetime.datetime(2000, 1, 1, 12, 30, 0), datetime.datetime(2000, 1, 1, 12, 45, 0), hide_date_if_single_day=True))
# 12:30 to 12:45

print(pretty_datetime_range(datetime.datetime(2000, 1, 1, 12, 30, 0), None))
# From 1 January 2000, 12:30
```

## pretty_age()

Formats a datetime into a human-readable delta.

> Added in `v1.2.0`.

### Arguments

| Argument           | Description                                                                                  | Default |
| ------------------ | -------------------------------------------------------------------------------------------- | ------- |
| `date`             | The datetime to show the delta from                                                          | [none]  |
| `just_now_seconds` | The maximum number of seconds in the past to use `Just now` instead of `x seconds ago`       | `5`     |
| `lowercase_first`  | If `True`, use `just now` and `in...` for outputs that normally start `Just now` and `In...` | `False` |

### Example

```python
from tna_utilities.datetime import pretty_age

print(pretty_age(datetime.datetime.now() - datetime.timedelta(seconds=1337)))
# 22 minutes ago

print(pretty_age(datetime.datetime.now() + datetime.timedelta(days=1)))
# In 1 day

print(pretty_age(datetime.datetime.now() - datetime.timedelta(seconds=29), just_now_seconds=60))
# Just now
```

## is_today_or_future()

Determines if the given date string represents today or a future date.

### Arguments

| Argument | Description      | Default |
| -------- | ---------------- | ------- |
| `date`   | The date to test | [none]  |

### Example

```python
from tna_utilities.datetime import is_today_or_future

print(is_today_or_future(datetime.date(2999, 1, 1)))
# True

print(is_today_or_future(datetime.date(2000, 1, 1)))
# False
```

## is_today_in_date_range()

Determines if today's date falls within the given date range.

### Arguments

| Argument    | Description                          | Default |
| ----------- | ------------------------------------ | ------- |
| `date_from` | The start of the date range to check | [none]  |
| `date_to`   | The end of the date range to check   | [none]  |

### Example

```python
from tna_utilities.datetime import is_today_in_date_range

print(is_today_in_date_range(datetime.date(2000, 1, 1), datetime.date(2001, 1, 1)))
# False

print(is_today_in_date_range(datetime.date(2000, 1, 1), datetime.date(2999, 1, 1)))
# True
```

## group_by_year_and_month()

Groups a list of items by year and month based on a date key in each item.

### Arguments

| Argument   | Description                                                  | Default |
| ---------- | ------------------------------------------------------------ | ------- |
| `items`    | A list of items to group                                     | [none]  |
| `date_key` | The key of the date to sort by                               | [none]  |
| `reverse`  | If `True`, show the most recent items at the top of the list | `False` |

### Example

```python
from tna_utilities.datetime import group_by_year_and_month

items = [
    {"id": 1, "date": datetime.date(2022, 5, 15)},
    {"id": 2, "date": datetime.date(2022, 5, 20)},
    {"id": 3, "date": datetime.date(2022, 6, 10)},
    {"id": 4, "date": datetime.date(2021, 12, 25)},
]
print(group_by_year_and_month(items, date_key="date"))
# [
#     {
#         "heading": "2021",
#         "index": 2021,
#         "items": [
#             {
#                 "heading": "December",
#                 "index": 12,
#                 "items": [
#                     {"id": 4, "date": datetime.date(2021, 12, 25)}
#                 ],
#             },
#         ],
#     },
#     {
#         "heading": "2022",
#         "index": 2022,
#         "items": [
#             {
#                 "heading": "May",
#                 "index": 5,
#                 "items": [
#                     {"id": 1, "date": datetime.date(2022, 5, 15)},
#                     {"id": 2, "date": datetime.date(2022, 5, 20)},
#                 ],
#             },
#             {
#                 "heading": "June",
#                 "index": 6,
#                 "items": [
#                     {"id": 3, "date": datetime.date(2022, 6, 10)},
#                 ],
#             },
#         ],
#     },
# ]
```

## seconds_to_iso_8601_duration()

Converts a total number of seconds into an ISO 8601 duration string.

### Arguments

| Argument        | Description                     | Default |
| --------------- | ------------------------------- | ------- |
| `total_seconds` | The number of seconds to format | [none]  |

### Example

```python
from tna_utilities.datetime import seconds_to_iso_8601_duration

print(seconds_to_iso_8601_duration(1337))
# PT22M17S
```

## seconds_to_duration()

Converts a total number of seconds into a human-readable duration string.

### Arguments

| Argument        | Description                                         | Default |
| --------------- | --------------------------------------------------- | ------- |
| `total_seconds` | The number of seconds to format                     | [none]  |
| `simplify`      | If `True`, omit leading zero-valued time components | `False` |

### Example

```python
from tna_utilities.datetime import seconds_to_duration

print(seconds_to_duration(1337))
# 00h 22m 17s

print(seconds_to_duration(1337, simplify=True))
# 22m 17s
```

## rfc_822_date_format()

Formats a date into RFC 822 format.

### Arguments

| Argument | Description        | Default |
| -------- | ------------------ | ------- |
| `date`   | The date to format | [none]  |

### Example

```python
from tna_utilities.datetime import rfc_822_date_format

print(rfc_822_date_format(datetime.datetime(2000, 1, 1, 12, 30, 45)))
# Sat, 1 Jan 2000 12:30:45 GMT
```
