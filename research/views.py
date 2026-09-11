from django.shortcuts import render, get_object_or_404

from .models import ResearchField, ResearchTitle, ResearchPaper


def home(request):
    fields = (
        ResearchField.objects
        .prefetch_related("research_titles")
        .all()
    )

    recent_research = (
        ResearchTitle.objects
        .filter(is_published=True)
        .select_related("research_field")
        .order_by("-created_at")[:6]
    )

    return render(request, "research/home.html", {
        "fields": fields,
        "recent_research": recent_research,
    })


def field_list(request):
    fields = ResearchField.objects.all()

    return render(request, "research/field_list.html", {
        "fields": fields,
    })


def field_detail(request, slug):
    field = get_object_or_404(
        ResearchField,
        slug=slug,
    )

    research_titles = (
        ResearchTitle.objects
        .filter(
            research_field=field,
            is_published=True,
        )
        .order_by("-created_at")
    )

    return render(request, "research/field_detail.html", {
        "field": field,
        "research_titles": research_titles,
    })


def research_detail(request, slug):
    research = get_object_or_404(
        ResearchTitle.objects.select_related("research_field"),
        slug=slug,
        is_published=True,
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
        research_title__is_published=True,
    )

    return render(request, "research/paper_detail.html", {
        "paper": paper,
    })