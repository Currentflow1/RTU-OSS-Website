from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "is_published",
        "is_featured",
        "published_at",
    )

    list_filter = (
        "is_published",
        "is_featured",
        "published_at",
    )

    search_fields = (
        "title",
        "summary",
        "content",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Announcement",
            {
                "fields": (
                    "title",
                    "summary",
                    "content",
                    "image",
                )
            },
        ),
        (
            "Publishing",
            {
                "fields": (
                    "author",
                    "is_published",
                    "is_featured",
                    "published_at",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )