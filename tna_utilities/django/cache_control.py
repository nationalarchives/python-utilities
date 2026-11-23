from functools import wraps


def do_not_cache():
    """Set Cache-Control to prevent caching."""
    return set_cache_control("no-store")


def cacheable_duration(seconds: int = 3600):
    """Allow public caching for the specified duration in seconds."""
    return set_cache_control(f"public, max-age={seconds}")


def cacheable_duration_cloudfront(
    client_seconds: int = 3600,
    cloudfront_seconds: int = 3600,
    stale_while_revalidate_seconds: int = 0,
    stale_if_error_seconds: int = 0,
):
    """Set client and CloudFront cache durations and optional stale directives."""
    instructions = f"public, max-age={client_seconds}"
    if cloudfront_seconds > 0 and cloudfront_seconds != client_seconds:
        instructions += f", s-maxage={cloudfront_seconds}"
    if stale_while_revalidate_seconds > 0:
        instructions += f", stale-while-revalidate={stale_while_revalidate_seconds}"
    if stale_if_error_seconds > 0:
        instructions += f", stale-if-error={stale_if_error_seconds}"
    return set_cache_control(instructions)


def set_cache_control(instructions: str):
    """Replace the Cache-Control header with the given instructions."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            response = view(*args, **kwargs)
            response.headers["Cache-Control"] = instructions
            return response

        return wrapped

    return decorator
