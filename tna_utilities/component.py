from collections.abc import Callable

PAGINATION_GAP = "..."


def paginate(pages: int, current_page: int, around: int = 1) -> list[int | str]:
    """
    Paginate a list of items, highlighting the current page and adding gaps where appropriate.

    Args:
        pages (int): The total number of pages to paginate.
        current_page (int): The current page number.
        around (int, optional): The number of pages to show around the current page. Defaults to 1.
    Returns:
        list: A list of dictionaries representing the paginated items, with "current" indicating the current page.
    """

    assert isinstance(pages, int), "pages must be an integer"
    assert pages >= 1, "pages must be at least 1"
    assert isinstance(current_page, int), "current_page must be an integer"
    assert current_page >= 1, "current_page must be at least 1"
    assert (
        current_page <= pages
    ), "current_page cannot be greater than the number of pages"
    assert around >= 0, "around must be non-negative"

    items = [item + 1 for item in range(pages)]
    total = len(items)

    pagination = set()
    pagination.add(1)
    pagination.add(total)

    for i in range(
        max(current_page - around, 1), min(current_page + around, total) + 1
    ):
        pagination.add(i)

    sorted_pages = sorted(pagination)

    if around >= 1:
        for i in range(len(sorted_pages) - 1):
            if sorted_pages[i + 1] - sorted_pages[i] == 2:
                pagination.add(sorted_pages[i] + 1)

        sorted_pages = sorted(pagination)

    result = []
    for i, page in enumerate(sorted_pages):
        if i > 0 and page - sorted_pages[i - 1] > 1:
            result.append(PAGINATION_GAP)
        item = items[page - 1]
        result.append(item)

    return result


def tna_frontend_pagination_items(
    pages: int,
    current_page: int,
    base_url: str,
    around: int = 1,
    transformer: Callable[
        [int, int, str], dict
    ] = lambda item, current_page, base_url: {
        "number": item,
        "current": item == current_page,
        "href": f"{base_url}{item}",
    },
    ellipsis: dict | None = None,
) -> list[dict]:
    """
    Convert paginated items to a format suitable for the TNA frontend.

    Args:
        pages (int): The total number of pages to paginate.
        current_page (int): The current page number.
        base_url (str): The base URL to use for pagination links.
        around (int, optional): The number of pages to show around the current page. Defaults to 1.
        transformer (callable, optional): A function to transform each page item.
        ellipsis (dict, optional): A dictionary representing the ellipsis item. Defaults to {"ellipsis": True}.
    Returns:
        list: A list of dictionaries representing the paginated items for the TNA frontend, with "number" for page numbers, "current" for the current page, and "href" for pagination links. Gaps are represented with "ellipsis": True.
    """

    paginated_items = paginate(pages, current_page, around)
    if ellipsis is None:
        ellipsis = {"ellipsis": True}
    return [
        (transformer(item, current_page, base_url) if type(item) is int else ellipsis)
        for item in paginated_items
    ]
