from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Prefetch, Q
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from org.models import Announcement

from .forms import ResearchSubmissionForm
from .models import ResearchField, ResearchPaper, ResearchTitle
from .services import (
    generate_unique_research_slug,
    search_research,
)

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

    results = (
        search_research(
            query=query,
            field=field,
        )
        .select_related("research_field")
        .prefetch_related(
            Prefetch(
                "papers",
                queryset=ResearchPaper.objects.only(
                    "id",
                    "research_title_id",
                    "abstract",
                ),
            )
        )
    )

    paginator = Paginator(results, 8)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    fields = (
        ResearchField.objects
        .only("id", "name", "slug")
        .order_by("name")
    )

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
    field = get_object_or_404(
        ResearchField.objects.annotate(
            research_count=Count(
                "research_titles",
                filter=Q(
                    research_titles__publication_status=(
                        ResearchTitle.PublicationStatus.PUBLISHED
                    )
                ),
                distinct=True,
            ),
            paper_count=Count(
                "research_titles__papers",
                filter=Q(
                    research_titles__publication_status=(
                        ResearchTitle.PublicationStatus.PUBLISHED
                    )
                ),
                distinct=True,
            ),
        ),
        slug=slug,
    )

    research_titles = (
        ResearchTitle.objects
        .filter(
            research_field=field,
            publication_status=ResearchTitle.PublicationStatus.PUBLISHED,
        )
        .select_related("research_field")
        .order_by("-created_at")[:8]
    )

    return render(request, "research/field_detail.html", {
        "field": field,
        "research_titles": research_titles,
        "research_count": field.research_count,
        "paper_count": field.paper_count,
    })


def research_detail(request, slug):
    research = get_object_or_404(
        ResearchTitle.objects.select_related("research_field"),
        slug=slug,
        publication_status=(
            ResearchTitle.PublicationStatus.PUBLISHED
        ),
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


def paper_file(request, pk):
    paper = get_object_or_404(
        ResearchPaper.objects.select_related("research_title"),
        pk=pk,
        research_title__publication_status=(
            ResearchTitle.PublicationStatus.PUBLISHED
        ),
    )

    response = FileResponse(
        paper.document.open("rb"),
        content_type="application/pdf",
    )

    response["Content-Disposition"] = "inline"

    return response


def research_submit(request):
    if request.method == "POST":
        form = ResearchSubmissionForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            with transaction.atomic():
                research = form.save(commit=False)

                research.slug = generate_unique_research_slug(
                    research.title
                )

                if request.user.is_authenticated:
                    research.submitted_by = request.user

                research.publication_status = (
                    ResearchTitle.PublicationStatus.PENDING
                )

                research.save()

                ResearchPaper.objects.create(
                    research_title=research,
                    abstract=form.cleaned_data["abstract"],
                    document=form.cleaned_data["document"],
                )

            return redirect("research:submission_success")
    else:
        form = ResearchSubmissionForm()

    return render(request, "research/research_submit.html", {
        "form": form,
    })


def submission_success(request):
    return render(request, "research/submission_success.html")


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def admin_submission_list(request):
    if not is_admin(request.user):
        return redirect("research:home")

    submissions = (
        ResearchTitle.objects
        .filter(
            publication_status=(
                ResearchTitle.PublicationStatus.PENDING
            )
        )
        .select_related(
            "research_field",
            "submitted_by",
        )
        .order_by("-created_at")
    )

    return render(request, "research/admin_submission_list.html", {
        "submissions": submissions,
    })


@login_required
def admin_submission_detail(request, pk):
    if not is_admin(request.user):
        return redirect("research:home")

    submission = get_object_or_404(
        ResearchTitle.objects.select_related(
            "research_field",
            "submitted_by",
        ),
        pk=pk,
    )

    paper = submission.papers.first()

    return render(request, "research/admin_submission_detail.html", {
        "submission": submission,
        "paper": paper,
    })


@login_required
@require_POST
def admin_submission_approve(request, pk):
    if not is_admin(request.user):
        return redirect("research:home")

    submission = get_object_or_404(
        ResearchTitle,
        pk=pk,
        publication_status=(
            ResearchTitle.PublicationStatus.PENDING
        ),
    )

    submission.publication_status = (
        ResearchTitle.PublicationStatus.PUBLISHED
    )
    submission.publication_date = timezone.now().date()

    submission.save(
        update_fields=[
            "publication_status",
            "publication_date",
            "updated_at",
        ]
    )

    return redirect("research:admin_submission_list")


@login_required
@require_POST
def admin_submission_reject(request, pk):
    if not is_admin(request.user):
        return redirect("research:home")

    submission = get_object_or_404(
        ResearchTitle,
        pk=pk,
        publication_status=(
            ResearchTitle.PublicationStatus.PENDING
        ),
    )

    submission.publication_status = (
        ResearchTitle.PublicationStatus.REJECTED
    )

    submission.save(
        update_fields=[
            "publication_status",
            "updated_at",
        ]
    )

    return redirect("research:admin_submission_list")


@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect("research:home")

    counts = ResearchTitle.objects.aggregate(
        total=Count("id"),
        pending=Count(
            "id",
            filter=Q(
                publication_status=(
                    ResearchTitle.PublicationStatus.PENDING
                )
            ),
        ),
        published=Count(
            "id",
            filter=Q(
                publication_status=(
                    ResearchTitle.PublicationStatus.PUBLISHED
                )
            ),
        ),
        rejected=Count(
            "id",
            filter=Q(
                publication_status=(
                    ResearchTitle.PublicationStatus.REJECTED
                )
            ),
        ),
    )

    recent_pending = (
        ResearchTitle.objects
        .filter(
            publication_status=(
                ResearchTitle.PublicationStatus.PENDING
            )
        )
        .select_related("research_field")
        .order_by("-created_at")[:5]
    )

    recent_published = (
        ResearchTitle.objects
        .filter(
            publication_status=(
                ResearchTitle.PublicationStatus.PUBLISHED
            )
        )
        .select_related("research_field")
        .order_by(
            "-publication_date",
            "-created_at",
        )[:5]
    )

    recent_announcements = (
        Announcement.objects
        .order_by(
            "-published_at",
            "-created_at",
        )[:5]
    )

    return render(request, "research/admin_dashboard.html", {
        "counts": counts,
        "recent_pending": recent_pending,
        "recent_published": recent_published,
        "recent_announcements": recent_announcements,
    })