# URLs

## `QueryStringTransformer`

A utility class to manipulate query strings.

### Instantiation

#### Flask

```python
from tna_utils.urls import QueryStringTransformer

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
from tna_utils.urls import QueryStringTransformer

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
from tna_utils.urls import QueryStringTransformer

# Create an iterable list that will allow
# us to use the lists() method to get the
# values and replicate the structure that
# Flask and Django provide
args = iter([("a", ["1"]), ("b", ["2", "3"])])

qs = QueryStringTransformer(args)
```

### Check and get values

```python
from tna_utils.urls import QueryStringTransformer

# ?a=1&b=2&b=3
qs = QueryStringTransformer(iter([("a", ["1"]), ("b", ["2", "3"])]))

qs.parameter_exists("a")
# True
qs.parameter_exists("c")
# False

qs.parameter_values("a")
# ["1"]
qs.parameter_values("b")
# ["2", "3"]
qs.parameter_values("c")
# AttributeError

qs.is_value_in_parameter("b", "2")
# True
qs.is_value_in_parameter("b", "4")
# False
```

### Add and remove parameters

```python
from tna_utils.urls import QueryStringTransformer

# ?a=1&b=2&b=3
qs = QueryStringTransformer(iter([("a", ["1"]), ("b", ["2", "3"])]))

qs.add_parameter("c", "4")
qs.update_parameter("b", ["5", "6"])
qs.remove_parameter("a")

print(qs.get_query_string())
# ?b=5&b=6&c=4
```

### Update parameter values

```python
from tna_utils.urls import QueryStringTransformer

# ?a=1&b=2&b=3
qs = QueryStringTransformer(iter([("a", ["1"]), ("b", ["2", "3"])]))

qs.add_parameter_value("a", "4")
qs.toggle_parameter_value("b", "3")
qs.remove_parameter_value("a", "1")

print(qs.get_query_string())
# ?a=4&b=2
```
