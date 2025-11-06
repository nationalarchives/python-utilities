import re
import unicodedata


def slugify(value: str, allow_unicode=False) -> str:
    """
    Convert a string to a URL-friendly slug.

    Derived from Django
    https://github.com/django/django/blob/stable/6.0.x/django/utils/text.py#L469-L486
    """

    if not isinstance(value, str):
        raise TypeError("value must be a string")

    if not value:
        return value

    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def unslugify(slug: str, capitalize_first: bool = True) -> str:
    """
    Convert a slug back to a human-readable string.
    """

    if not isinstance(slug, str):
        raise TypeError("slug must be a string")

    if not slug:
        return slug

    string = slug.split("-")
    if capitalize_first:
        string[0] = string[0].capitalize()
    return " ".join(string)
