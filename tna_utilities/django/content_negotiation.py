import math
from functools import wraps

from django.http import HttpResponse
from django.http.request import MediaType
from django.utils.cache import patch_vary_headers


def _preferred_type(request, options):
    accepted = []
    for token in request.headers.get("Accept", "").split(","):
        if not token.strip():
            continue
        media_type = MediaType(token.lower())
        if not media_type.main_type or not media_type.sub_type:
            continue
        if media_type.main_type == "*" and media_type.sub_type != "*":
            continue
        try:
            quality = float(media_type.params.get("q", 1))
        except ValueError:
            continue
        if not math.isfinite(quality) or not 0 <= quality <= 1:
            continue
        accepted.append((media_type, quality))

    accepted.sort(key=lambda item: (item[0].specificity, item[1]), reverse=True)
    preferred = None
    best_rank = (0, -1)
    for option in options:
        media_type = MediaType(option.lower())
        for accepted_type, quality in accepted:
            wildcard = (
                accepted_type.main_type == "*"
                or media_type.main_type == "*"
                or (
                    media_type.main_type == accepted_type.main_type
                    and (accepted_type.sub_type == "*" or media_type.sub_type == "*")
                )
            )
            if wildcard or (
                media_type.match(accepted_type)
                and media_type.range_params == accepted_type.range_params
            ):
                rank = (quality, accepted_type.specificity)
                if quality > 0 and rank > best_rank:
                    preferred, best_rank = option, rank
                break
    return preferred


def get_requested_accept(options):
    """Pass the negotiated type as preferred_content_type and vary by Accept."""

    def decorator(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            requested_accept = request.headers.get("Accept")
            preferred_content_type = _preferred_type(request, options)
            if requested_accept and preferred_content_type is None:
                response = HttpResponse(status=406)
            else:
                kwargs["preferred_content_type"] = preferred_content_type
                response = view(request, *args, **kwargs)
            if response.status_code == 406:
                response.headers["Cache-Control"] = "no-store"
            patch_vary_headers(response, ("Accept",))
            return response

        return wrapped

    return decorator
