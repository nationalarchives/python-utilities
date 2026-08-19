from urllib.parse import urlencode


class BaseQueryString:
    """
    A utility class to query URL query strings.

    Args:
        args: An object representing the query parameters, typically an
              ImmutableMultiDict (Django) or QueryDict (Flask) which can be
              accessed with request.GET (Django) or request.args (Flask).
        tolerant: If True, the transformer will not raise exceptions when
                  keys don't exist.
    """

    def __init__(self, args=None, tolerant=False) -> None:
        if isinstance(args, list):
            self.args = args
        elif args is not None:
            try:
                args_lists = args.lists()
            except AttributeError as e:
                raise AttributeError(
                    "args must be an ImmutableMultiDict (Django), a QueryDict (Flask) object or an iterable of (key, [values]) tuples"
                ) from e
            self.args = list(args_lists)
        else:
            self.args = []
        self.tolerant = tolerant

    def parameter_exists(self, parameter) -> bool:
        """
        Check if a parameter exists in the query parameters.
        """

        return any(key == parameter for key, _ in self.args)

    def parameter_values(self, parameter: str) -> list:
        """
        Get the values associated with a parameter in the query parameters.
        Raises a KeyError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                return values
        if self.tolerant:
            return []
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def is_value_in_parameter(self, parameter: str, value: str | int) -> bool:
        """
        Check if a specific value exists within a parameter's values.
        Raises a KeyError if the parameter does not exist and tolerant mode is not enabled.
        """

        for key, values in self.args:
            if key == parameter:
                return str(value) in values
        if self.tolerant:
            return False
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def get_query_string(self) -> str:
        """
        Get the full query string.
        Returns an empty string if there are no query parameters.
        """

        query = urlencode(self.args, doseq=True)
        if not query:
            return ""
        return f"?{query}"


class QueryStringModifier(BaseQueryString):
    """
    A utility class to manipulate URL query strings.
    """

    def add_parameter(
        self, parameter: str, values: str | int | list | None = None
    ) -> "QueryStringModifier":
        """
        Add a new parameter to the query parameters.
        Raises a ValueError if the parameter already exists and tolerant mode is not enabled.
        """

        parameter_exists = self.parameter_exists(parameter)
        if parameter_exists and not self.tolerant:
            raise ValueError(f"Parameter '{parameter}' already exists")
        if not isinstance(values, list):
            values = [str(values)] if values is not None else []
        else:
            values = [str(v) for v in values]
        if parameter_exists:
            self.update_parameter(parameter, values)
        else:
            self.args.append((parameter, values))
        return self

    def update_parameter(
        self, parameter: str, values: str | int | list | None = None
    ) -> "QueryStringModifier":
        """
        Update an existing parameter in the query parameters.
        If the parameter does not exist, it will be added.
        """

        if self.parameter_exists(parameter):
            self.remove_parameter(parameter)
        self.add_parameter(parameter, values)
        return self

    def remove_parameter(self, parameter: str) -> "QueryStringModifier":
        """
        Remove a parameter from the query parameters.
        Raises a KeyError if the parameter does not exist and tolerant mode is not enabled.
        """

        for index, (key, _vals) in enumerate(self.args):
            if key == parameter:
                del self.args[index]
                return self
        if self.tolerant:
            return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def add_parameter_value(
        self, parameter: str, value: str | int
    ) -> "QueryStringModifier":
        """
        Add a specific value to a parameter's values.
        Raises a KeyError if the parameter does not exist and tolerant mode is not enabled.
        """

        for key, values in self.args:
            if key == parameter:
                if str(value) not in values:
                    values.append(str(value))
                return self
        if self.tolerant:
            self.args.append((parameter, [str(value)]))
            return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def toggle_parameter_value(
        self, parameter: str, value: str | int
    ) -> "QueryStringModifier":
        """
        Toggle a value within a parameter's values.
        If the value exists, it will be removed; if it does not exist, it will be added.
        Raises a KeyError if the parameter does not exist and tolerant mode is not enabled.
        """

        for key, values in self.args:
            if key == parameter:
                str_value = str(value)
                if str_value in values:
                    values.remove(str_value)
                elif str_value not in values:
                    values.append(str_value)
                return self
        if self.tolerant:
            self.args.append((parameter, [str(value)]))
            return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def remove_parameter_value(
        self, parameter: str, value: str | int
    ) -> "QueryStringModifier":
        """
        Remove a specific value from a parameter's values.
        Raises a KeyError if the parameter does not exist or if the value is not present and tolerant mode is not enabled.
        """

        for key, values in self.args:
            if key == parameter:
                if str(value) in values:
                    values.remove(str(value))
                    return self
                raise KeyError(
                    f"Value '{value}' does not exist for parameter '{parameter}'"
                )
        if self.tolerant:
            return self
        raise KeyError(f"Parameter '{parameter}' does not exist")


class QueryStringTransformer(BaseQueryString):
    """
    A utility class that extends QueryStringModifier to manipulate query strings while keeping a copy of the initial query string intact for querying later.

    Args:
        args: An object representing the query parameters, typically an
              ImmutableMultiDict (Django) or QueryDict (Flask) which can be
              accessed with request.GET (Django) or request.args (Flask).
        tolerant: If True, the transformer will not raise exceptions when
                  keys don't exist.
    """

    def __init__(self, args=None, tolerant=False) -> None:
        super().__init__(args, tolerant)
        self.initial_args = self.args

    def new(self) -> "QueryStringModifier":
        """
        Create a new instance of QueryStringModifier with the same initial query string.
        """

        return QueryStringModifier(self.initial_args.copy(), self.tolerant)
