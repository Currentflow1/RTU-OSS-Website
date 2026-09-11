from django.db.models import Q
from .models import ResearchTitle


def search_research(query="", field=None):
    queryset = (
        ResearchTitle.objects
        .filter(is_published=True)
        .select_related("research_field")
    )

    query = query.strip()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(authors__icontains=query)
            | Q(research_field__name__icontains=query)
            | Q(papers__abstract__icontains=query)
        ).distinct()

    if field:
        queryset = queryset.filter(research_field__slug=field)

    return queryset.order_by("-created_at")
