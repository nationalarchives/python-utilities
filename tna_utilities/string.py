import re


def slugify(string: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    """

    if not string:
        return string

    slug = string.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    slug = re.sub(r"^-+|-+$", "", slug)
    return slug


def unslugify(slug: str, capitalize_first: bool = True) -> str:
    """
    Convert a slug back to a human-readable string.
    """

    if not slug:
        return slug

    string = slug.split("-")
    if capitalize_first:
        string[0] = string[0].capitalize()
    return " ".join(string)
