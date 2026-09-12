from django.db.models import Q
from django.utils.text import slugify

from .models import ResearchTitle


def search_research(query="", field=None):
  queryset = (
    ResearchTitle.objects
    .filter(
      publication_status=ResearchTitle.PublicationStatus.PUBLISHED
    )
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
    queryset = queryset.filter(
      research_field__slug=field
    )

  return queryset.order_by("-created_at")


def generate_unique_research_slug(title):
  base_slug = slugify(title)
  slug = base_slug
  counter = 2

  while ResearchTitle.objects.filter(slug=slug).exists():
    slug = f"{base_slug}-{counter}"
    counter += 1

  return slug