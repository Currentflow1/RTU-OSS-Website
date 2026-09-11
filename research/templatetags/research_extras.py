import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


def _highlight_text(value, query):
    """
    Highlight the searched query inside already escaped text.
    """
    if not value or not query:
        return conditional_escape(value or "")

    value = conditional_escape(value)
    query = conditional_escape(query)

    pattern = re.compile(
        re.escape(query),
        re.IGNORECASE,
    )

    return pattern.sub(
        lambda match: (
            '<mark class="rounded bg-[#ead6a8] px-0.5 font-medium text-[#3f2618]">'
            + match.group(0)
            + "</mark>"
        ),
        value,
    )


@register.filter
def contains_query(value, query):
    """
    Return True when query exists inside value, case-insensitively.
    """
    if not value or not query:
        return False

    return query.strip().lower() in str(value).lower()


@register.filter
def highlight(value, query):
    """
    Highlight every occurrence of query inside value.
    """
    if not value:
        return ""

    if not query:
        return conditional_escape(value)

    return mark_safe(_highlight_text(value, query))


@register.filter
def search_context(value, query, radius=180):
    """
    Return a short excerpt surrounding the first occurrence
    of the searched query.

    The matching query is highlighted.
    """
    if not value or not query:
        return ""

    text = str(value).strip()
    query = str(query).strip()

    if not text or not query:
        return ""

    match = re.search(
        re.escape(query),
        text,
        re.IGNORECASE,
    )

    if not match:
        return ""

    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)

    excerpt = text[start:end].strip()

    # Avoid cutting words at the beginning.
    if start > 0:
        first_space = excerpt.find(" ")

        if first_space != -1:
            excerpt = excerpt[first_space + 1:].strip()

    # Avoid cutting words at the end.
    if end < len(text):
        last_space = excerpt.rfind(" ")

        if last_space != -1:
            excerpt = excerpt[:last_space].strip()

    if start > 0:
        excerpt = "… " + excerpt

    if end < len(text):
        excerpt = excerpt + " …"

    return mark_safe(
        _highlight_text(excerpt, query)
    )
