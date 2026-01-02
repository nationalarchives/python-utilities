from urllib.parse import urlencode


class QueryStringTransformer:
    """
    A utility class to manipulate query strings.

    Args:
        args: An object representing the query parameters, typically an
              ImmutableMultiDict (Django) or QueryDict (Flask) which can be
              accessed with request.GET (Django) or request.args (Flask).
    """

    def __init__(self, args=None) -> None:
        if isinstance(args, list):
            self.args = args
        elif args is not None:
            try:
                args_lists = args.lists()
            except AttributeError:
                raise AttributeError(
                    "args must be an ImmutableMultiDict (Django), a QueryDict (Flask) object or an iterable of (key, [values]) tuples"
                )
            self.args = list(args_lists)
        else:
            self.args = []

    def parameter_exists(self, parameter) -> bool:
        """
        Check if a parameter exists in the query parameters.
        """

        for key, _ in self.args:
            if key == parameter:
                return True
        return False

    def parameter_values(self, parameter: str) -> list:
        """
        Get the values associated with a parameter in the query parameters.
        Raises a KeyError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                return values
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def add_parameter(
        self, parameter: str, values: str | int | list | None = None
    ) -> "QueryStringTransformer":
        """
        Add a new parameter to the query parameters.
        Raises a ValueError if the parameter already exists.
        """

        for key, vals in self.args:
            if key == parameter:
                raise ValueError(f"Parameter '{parameter}' already exists")
        if not isinstance(values, list):
            values = [str(values)] if values is not None else []
        else:
            values = [str(v) for v in values]
        self.args.append((parameter, values))
        return self

    def update_parameter(
        self, parameter: str, values: str | int | list | None = None
    ) -> "QueryStringTransformer":
        """
        Update an existing parameter in the query parameters.
        If the parameter does not exist, it will be added.
        """

        if self.parameter_exists(parameter):
            self.remove_parameter(parameter)
        self.add_parameter(parameter, values)
        return self

    def remove_parameter(self, parameter: str) -> "QueryStringTransformer":
        """
        Remove a parameter from the query parameters.
        Raises a KeyError if the parameter does not exist.
        """

        for key, vals in self.args:
            if key == parameter:
                self.args.remove((key, vals))
                return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def is_value_in_parameter(self, parameter: str, value: str | int) -> bool:
        """
        Check if a specific value exists within a parameter's values.
        Raises a KeyError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                return str(value) in values
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def add_parameter_value(
        self, parameter: str, value: str | int
    ) -> "QueryStringTransformer":
        """
        Add a specific value to a parameter's values.
        Raises a KeyError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                if str(value) not in values:
                    values.append(str(value))
                return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def toggle_parameter_value(
        self, parameter: str, value: str | int
    ) -> "QueryStringTransformer":
        """
        Toggle a value within a parameter's values.
        If the value exists, it will be removed; if it does not exist, it will be added.
        Raises a KeyError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                if str(value) in values:
                    self.remove_parameter_value(parameter, value)
                else:
                    self.add_parameter_value(parameter, value)
                return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def remove_parameter_value(
        self, parameter: str, value: str | int
    ) -> "QueryStringTransformer":
        """
        Remove a specific value from a parameter's values.
        Raises a KeyError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                if str(value) in values:
                    values.remove(str(value))
                return self
        raise KeyError(f"Parameter '{parameter}' does not exist")

    def get_query_string(self) -> str:
        """
        Get the full query string.
        """

        return f"?{urlencode(self.args, doseq=True)}"
