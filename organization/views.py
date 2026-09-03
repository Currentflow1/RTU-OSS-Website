from django.shortcuts import get_object_or_404, render

from .models import Announcement

def announcement_list(request):
  announcements = Announcement.objects.filter(
    is_published=True,
  )
  featured = announcements.filter(
    is_featured=True,
  ).first()

  regular_announcements = announcements.exclude(
    pk=featured.pk if featured else None,
  )

  return render(request, "announcements/list.html", {
    'featured': featured,
    'announcements': regular_announcements,
  })


def announcement_detail(request, pk):
  announcement = get_object_or_404(Announcement, pk=pk, is_published=True)

  return render(request, "announcements/detail.html", {
    "announcement": announcement
  })