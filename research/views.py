from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Prefetch
from django.db.models import Count, Q

from .models import ResearchField, ResearchTitle, ResearchPaper
from .services import search_research


def home(request):
    fields = (
        ResearchField.objects
        .annotate(
            research_count=Count(
                "research_titles",
                filter=Q(
                    research_titles__publication_status=(
                        ResearchTitle.PublicationStatus.PUBLISHED
                    )
                ),
            )
        )
        .order_by("name")[:6]
    )

    recent_research = (
        ResearchTitle.objects
        .filter(
            publication_status=ResearchTitle.PublicationStatus.PUBLISHED
        )
        .select_related("research_field")
        .order_by("-created_at")[:6]
    )

    return render(request, "research/home.html", {
        "fields": fields,
        "recent_research": recent_research,
    })


def search(request):
    query = request.GET.get("q", "").strip()
    field = request.GET.get("field", "").strip()

    results = search_research(
        query=query,
        field=field,
    ).prefetch_related(
        Prefetch(
            "papers",
            queryset=ResearchPaper.objects.only(
                "id",
                "research_title_id",
                "abstract",
            ),
        )
    )

    paginator = Paginator(results, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    fields = ResearchField.objects.all()

    return render(request, "research/search.html", {
        "query": query,
        "field": field,
        "page_obj": page_obj,
        "fields": fields,
    })


def field_list(request):
    fields = (
        ResearchField.objects
        .annotate(
            research_count=Count(
                "research_titles",
                filter=Q(
                    research_titles__publication_status=(
                        ResearchTitle.PublicationStatus.PUBLISHED
                    )
                ),
            )
        )
        .order_by("name")
    )

    return render(request, "research/field_list.html", {
        "fields": fields,
    })


def field_detail(request, slug):
    field = get_object_or_404(ResearchField, slug=slug)

    research_queryset = (
        ResearchTitle.objects
        .filter(
            research_field=field,
            publication_status=ResearchTitle.PublicationStatus.PUBLISHED,
        )
    )

    research_count = research_queryset.count()

    paper_count = ResearchPaper.objects.filter(
        research_title__in=research_queryset
    ).count()

    research_titles = (
        research_queryset
        .order_by("-created_at")[:8]
    )

    return render(request, "research/field_detail.html", {
        "field": field,
        "research_titles": research_titles,
        "research_count": research_count,
        "paper_count": paper_count,
    })


def research_detail(request, slug):
    research = get_object_or_404(
        ResearchTitle.objects.select_related("research_field"),
        slug=slug,
        publication_status=ResearchTitle.PublicationStatus.PUBLISHED,
    )

    papers = research.papers.all()

    return render(request, "research/research_detail.html", {
        "research": research,
        "papers": papers,
    })


def paper_detail(request, pk):
    paper = get_object_or_404(
        ResearchPaper.objects.select_related(
            "research_title",
            "research_title__research_field",
        ),
        pk=pk,
        research_title__publication_status=(
            ResearchTitle.PublicationStatus.PUBLISHED
        ),
    )

    return render(request, "research/paper_detail.html", {
        "paper": paper,
    })