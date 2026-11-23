from functools import wraps

from flask import make_response, request


def get_requested_accept(options):
    """
    Pass the negotiated type as preferred_content_type and vary by Accept.
    """

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            requested_accept = request.headers.get("Accept")
            preferred_content_type = request.accept_mimetypes.best_match(options)
            if requested_accept and preferred_content_type is None:
                response = make_response("", 406)
            else:
                kwargs["preferred_content_type"] = preferred_content_type
                response = make_response(f(*args, **kwargs))
            if response.status_code == 406:
                response.cache_control.clear()
                response.cache_control.no_store = True
            if "*" not in response.vary:
                response.vary.add("Accept")
            return response

        return wrapped

    return decorator
