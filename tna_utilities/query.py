from urllib.parse import urlencode


class QueryStringManipulator:
    """
    A utility class to manipulate query strings from web requests.

    Args:
        args: An object representing the query parameters, typically an
              ImmutableMultiDict (Django) or QueryDict (Flask) which can be
              accessed with request.GET (Django) or request.args (Flask).
    """

    def __init__(self, args):
        try:
            args_lists = args.lists()
        except AttributeError:
            raise TypeError(
                "args must be a ImmutableMultiDict (Django) or QueryDict (Flask) object"
            )
        self.args = list(args_lists)

    def filter_exists(self, filter):
        """
        Check if a filter exists in the query parameters.
        """

        for key, _ in self.args:
            if key == filter:
                return True
        return False

    def filter_values(self, filter):
        """
        Get the values associated with a filter in the query parameters.
        Raises an AttributeError if the filter does not exist.
        """

        for key, values in self.args:
            if key == filter:
                return values
        raise AttributeError(f"Filter '{filter}' does not exist")

    def add_filter(self, filter, values=None):
        """
        Add a new filter to the query parameters.
        Raises a ValueError if the filter already exists.
        """

        for key, vals in self.args:
            if key == filter:
                raise ValueError(f"Filter '{filter}' already exists")
        if type(values) is not list:
            values = [str(values)] if values is not None else []
        else:
            values = [str(v) for v in values]
        self.args.append((filter, values))

    def update_filter(self, filter, values=None):
        """
        Update an existing filter in the query parameters.
        If the filter does not exist, it will be added.
        """

        try:
            self.remove_filter(filter)
        except AttributeError:
            pass
        self.add_filter(filter, values)

    def remove_filter(self, filter):
        """
        Remove a filter from the query parameters.
        Raises an AttributeError if the filter does not exist.
        """

        for key, vals in self.args:
            if key == filter:
                self.args.remove((key, vals))
                return
        raise AttributeError(f"Filter '{filter}' does not exist")

    def is_value_in_filter(self, filter, value):
        """
        Check if a specific value exists within a filter's values.
        Raises an AttributeError if the filter does not exist.
        """

        for key, values in self.args:
            if key == filter:
                return value in values
        raise AttributeError(f"Filter '{filter}' does not exist")

    def toggle_filter_value(self, filter, value):
        """
        Toggle a value within a filter's values.
        If the value exists, it will be removed; if it does not exist, it will be added.
        Raises an AttributeError if the filter does not exist.
        """

        for key, values in self.args:
            if key == filter:
                if value in values:
                    self.remove_filter_value(filter, value)
                else:
                    self.add_filter_value(filter, value)
                return
        raise AttributeError(f"Filter '{filter}' does not exist")

    def remove_filter_value(self, filter, value):
        """
        Remove a specific value from a filter's values.
        Raises an AttributeError if the filter does not exist.
        """

        for key, values in self.args:
            if key == filter:
                if value in values:
                    values.remove(value)
                return
        raise AttributeError(f"Filter '{filter}' does not exist")

    def add_filter_value(self, filter, value):
        """
        Add a specific value to a filter's values.
        Raises an AttributeError if the filter does not exist.
        """

        for key, values in self.args:
            if key == filter:
                if value not in values:
                    values.append(value)
                return
        raise AttributeError(f"Filter '{filter}' does not exist")

    def get_query_string(self):
        """
        Get the full query string.
        """

        return f"?{urlencode(self.args, doseq=True)}"
