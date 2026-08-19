# URLs

## `QueryStringTransformer`

A utility class to manipulate query strings.

Use this to take a query string like `?q=pizza&page=3&category=social` and manipulate only what you need, for example changing the `page` parameter to `4`, or switching out the category from `social` to `work`, while keeping the rest of the query string intact.

This can be useful when generating things like links in filters, avoiding the need to `POST` a form and have a stateful page that can't be shared or refreshed.

### Instantiation

#### Flask

```python
from tna_utilities.url import QueryStringTransformer

# ?a=1&b=2&b=3
print(request.args)
# ImmutableMultiDict([('a', '1'), ('b', '2'), ('b', '3')])

normalised_args = list(request.args.lists())
print(normalised_args)
# [('a', ['1']), ('b', ['2', '3'])]

qs = QueryStringTransformer(normalised_args)
```

#### Django

```python
from tna_utilities.url import QueryStringTransformer

# ?a=1&b=2&b=3
print(request.GET)
# <QueryDict: {'a': ['1'], 'b': ['2', '3']}>

normalised_args = list(request.GET.lists())
print(normalised_args)
# [('a', ['1']), ('b', ['2', '3'])]

qs = QueryStringTransformer(normalised_args)
```

#### Bespoke

```python
from tna_utilities.url import QueryStringTransformer

qs = QueryStringTransformer([("a", ["1"]), ("b", ["2", "3"])])
```

### Check and get values

```python
from tna_utilities.url import QueryStringTransformer

# ?a=1&b=2&b=3
qs = QueryStringTransformer([("a", ["1"]), ("b", ["2", "3"])])

qs.parameter_exists("a")
# True
qs.parameter_exists("c")
# False

qs.parameter_values("a")
# ["1"]
qs.parameter_values("b")
# ["2", "3"]
qs.parameter_values("c")
# Raises AttributeError

qs.is_value_in_parameter("b", "2")
# True
qs.is_value_in_parameter("b", "4")
# False
```

### Add, update and remove parameters

Here, we are creating a new query string using `.new()` which creates a modifyable object which allows us to add, update and remove parameters and their values.

```python
from tna_utilities.url import QueryStringTransformer

# ?a=1&b=2&b=3
qs = QueryStringTransformer([("a", ["1"]), ("b", ["2", "3"])])

new_qs = qs.new()

new_qs.add_parameter("c", "4")
new_qs.update_parameter("b", ["5", "6"])
new_qs.add_parameter_value("b", "7")
new_qs.toggle_parameter_value("b", "1")
new_qs.remove_parameter_value("b", "5")
new_qs.remove_parameter("a")
print(new_qs.get_query_string())
# ?b=1&b=6&b=7&c=4

# Chainable (as of v1.1.0)
print(new_qs.add_parameter(
    "c", "4"
).update_parameter(
    "b", ["5", "6"]
).add_parameter_value(
    "b", "7"
).toggle_parameter_value(
    "b", "1"
).remove_parameter_value(
    "b", "5"
).remove_parameter(
    "a"
).get_query_string())
```

### Tolerant mode

> Added in `v1.7.0`.

```python
from tna_utilities.url import QueryStringTransformer

# ?a=1
qs = QueryStringTransformer([("a", ["1"])])
new_qs = qs.new()
new_qs.remove_parameter_value("b", "2")  # Raises KeyError: Parameter 'b' does not exist
print(new_qs.is_value_in_parameter("c", "3"))  # Raises KeyError: Parameter 'c' does not exist

# ?a=1
tolerant_qs = QueryStringTransformer([("a", ["1"])], tolerant=True)
new_tolerant_qs = tolerant_qs.new()
new_tolerant_qs.remove_parameter_value("b", "2")  # No exception raised
print(new_tolerant_qs.is_value_in_parameter("c", "3"))
# False
```
