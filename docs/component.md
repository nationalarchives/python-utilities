# Component

> Added in `v1.5.0`.

## `paginate()`

Creates a pagination object in accordance with the [pages to show in a pagination component](https://design-system.nationalarchives.gov.uk/components/pagination/#number-of-page-links) in the National Archives Design System.

### Arguments

| Argument       | Description                                                | Default |
| -------------- | ---------------------------------------------------------- | ------- |
| `pages`        | The total number of pages to paginate                      | [none]  |
| `current_page` | The number of the current page                             | [none]  |
| `around`       | The number of items to always show around the current page | `1`     |

### Example

```python
from tna_utilities.component import paginate

print(paginate(42, 7))
# [1, "...", 6, 7, 8, "...", 42]

print(paginate(42, 7, around=2))
# [1, "...", 5, 6, 7, 8, 9, "...", 42]
```

## `tna_frontend_pagination()`

> Added in `v1.8.0`.

Creates an object that be used directly in a [National Archives pagination component](https://design-system.nationalarchives.gov.uk/components/pagination/) using [`tna_frontend_pagination_items()`](#tna_frontend_pagination_items).

### Arguments

| Argument                   | Description                                                                     | Default                                                            |
| -------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `pages`                    | The total number of pages to paginate                                           | [none]                                                             |
| `current_page`             | The number of the current page                                                  | [none]                                                             |
| `base_url`                 | The base URL including the blank query string for the page                      | [none]                                                             |
| `custom_properties`        | A dictionary of custom properties for the pagination component                  | [none]                                                             |
| `around`                   | The number of items to always show around the current page                      | `1`                                                                |
| `transformer`              | A function to create the item given a number and whether it is the current page | `tna_utilities.component.tna_frontend_pagination_item_transformer` |
| `ellipsis`                 | A dictionary to use in place of an ellipsis                                     | `{"ellipsis": True}`                                               |
| `previous_page_properties` | Properties to use for the previous page button                                  | [none]                                                             |
| `next_page_properties`     | Properties to use for the next page button                                      | [none]                                                             |

### Example

```python
from tna_utilities.component import tna_frontend_pagination

print(tna_frontend_pagination(42, 7, "?page=", {"landmarkLabel": "Pages of results"}, next_page_properties={"text": "Go on..."}))
# {
#     "landmarkLabel": "Pages of results",
#     "items": [
#         {"number": 1, "current": False, "href": "?page=1"},
#         {"ellipsis": True},
#         {"number": 6, "current": False, "href": "?page=6"},
#         {"number": 7, "current": True, "href": "?page=7"},
#         {"number": 8, "current": False, "href": "?page=8"},
#         {"ellipsis": True},
#         {"number": 42, "current": False, "href": "?page=42"},
#     ],
#     "previous": {
#         "href": "?page=6",
#     },
#     "next": {
#         "text": "Go on...",
#         "href": "?page=8",
#     },
# }
```

## `tna_frontend_pagination_items()`

Creates a list of items that be used directly in a [National Archives pagination component](https://design-system.nationalarchives.gov.uk/components/pagination/).

### Arguments

| Argument       | Description                                                                     | Default                                                            |
| -------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `pages`        | The total number of pages to paginate                                           | [none]                                                             |
| `current_page` | The number of the current page                                                  | [none]                                                             |
| `base_url`     | The base URL including the blank query string for the page                      | [none]                                                             |
| `around`       | The number of items to always show around the current page                      | `1`                                                                |
| `transformer`  | A function to create the item given a number and whether it is the current page | `tna_utilities.component.tna_frontend_pagination_item_transformer` |
| `ellipsis`     | A dictionary to use in place of an ellipsis                                     | `{"ellipsis": True}`                                               |

### Example

```python
from tna_utilities.component import tna_frontend_pagination_items

print(tna_frontend_pagination_items(42, 7, "?page="))
# [
#     {"number": 1, "current": False, "href": "?page=1"},
#     {"ellipsis": True},
#     {"number": 6, "current": False, "href": "?page=6"},
#     {"number": 7, "current": True, "href": "?page=7"},
#     {"number": 8, "current": False, "href": "?page=8"},
#     {"ellipsis": True},
#     {"number": 42, "current": False, "href": "?page=42"},
# ]
```
