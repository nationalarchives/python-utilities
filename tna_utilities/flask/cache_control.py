from functools import wraps

from flask import make_response


def do_not_cache():
    """
    Decorator to set Cache-Control headers to prevent caching of the response.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            headers = response.headers
            headers["Cache-Control"] = "no-store"
            return response

        return decorated_function

    return decorator


def cacheable_duration(seconds: int = 3600):
    """
    Decorator to set Cache-Control headers to allow caching of the response for a specified duration.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            headers = response.headers
            headers["Cache-Control"] = f"public, max-age={seconds}"
            return response

        return decorated_function

    return decorator


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
