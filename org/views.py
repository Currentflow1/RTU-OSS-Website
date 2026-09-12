from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .forms import AnnouncementForm
from .models import Announcement

def home(request):
  announcements = Announcement.objects.filter(
    is_published=True
  )

  return render(request, "org/home.html", {
    "announcements": announcements,
  })


def announcement_detail(request, slug):
  announcement = get_object_or_404(
    Announcement,
    slug=slug,
    is_published=True,
  )

  return render(request, "org/announcement_detail.html", {
    "announcement": announcement,
  })

def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
def admin_announcement_create(request):
    if not is_admin(request.user):
        return redirect("org:home")

    if request.method == "POST":
        form = AnnouncementForm(request.POST)

        if form.is_valid():
            announcement = form.save(commit=False)

            base_slug = slugify(announcement.title)
            slug = base_slug
            counter = 2

            while Announcement.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            announcement.slug = slug
            announcement.save()

            return redirect("research:admin_announcement_list")
    else:
        form = AnnouncementForm()

    return render(
        request,
        "org/admin_announcement_form.html",
        {
            "form": form,
            "page_title": "Create Announcement",
        },
    )


@login_required
def admin_announcement_list(request):
    if not is_admin(request.user):
        return redirect("org:home")

    announcements = Announcement.objects.order_by(
        "-published_at",
        "-created_at",
    )

    return render(
        request,
        "org/admin_announcement_list.html",
        {
            "announcements": announcements,
        },
    )


@login_required
def admin_announcement_edit(request, pk):
    if not is_admin(request.user):
        return redirect("org:home")

    announcement = get_object_or_404(
        Announcement,
        pk=pk,
    )

    if request.method == "POST":
        form = AnnouncementForm(
            request.POST,
            instance=announcement,
        )

        if form.is_valid():
            announcement = form.save(commit=False)

            base_slug = slugify(announcement.title)
            slug = base_slug
            counter = 2

            while Announcement.objects.filter(
                slug=slug
            ).exclude(pk=announcement.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            announcement.slug = slug
            announcement.save()

            return redirect("research:admin_announcement_list")
    else:
        form = AnnouncementForm(
            instance=announcement,
        )

    return render(
        request,
        "org/admin_announcement_form.html",
        {
            "form": form,
            "page_title": "Edit Announcement",
            "announcement": announcement,
        },
    )


@login_required
@require_POST
def admin_announcement_delete(request, pk):
    if not is_admin(request.user):
        return redirect("org:home")

    announcement = get_object_or_404(
        Announcement,
        pk=pk,
    )

    announcement.delete()

    return redirect("research:admin_announcement_list")