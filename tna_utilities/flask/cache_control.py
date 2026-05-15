from functools import wraps

from flask import make_response


def do_not_cache():
    """
    Decorator to set Cache-Control headers to prevent caching of the response.
    """

    return set_cache_control("no-store")


def cacheable_duration(seconds: int = 3600):
    """
    Decorator to set Cache-Control headers to allow caching of the response for a specified duration.
    """

    return set_cache_control(f"public, max-age={seconds}")


def set_cache_control(instructions: str):
    """
    Decorator to set Cache-Control headers with custom instructions provided as a string.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            headers = response.headers
            headers["Cache-Control"] = instructions
            return response

        return decorated_function

    return decorator


def vary_by_cookies():
    """
    Decorator to set Vary headers to indicate that the response varies based on cookies.
    """

    return vary_by_headers("Cookie")


def vary_by_headers(headers: str):
    """
    Decorator to set Vary headers to indicate that the response varies based on specified headers.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.headers["Vary"] = headers
            return response

        return decorated_function

    return decorator
