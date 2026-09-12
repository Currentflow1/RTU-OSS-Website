from django.contrib import admin

from .models import ResearchField, ResearchPaper, ResearchTitle


@admin.register(ResearchField)
class ResearchFieldAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "description",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(ResearchTitle)
class ResearchTitleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "research_field",
        "publication_status",
        "school_year",
        "created_at",
    )
    list_filter = (
        "publication_status",
        "research_field",
        "school_year",
    )
    search_fields = (
        "title",
        "authors",
        "keywords",
        "department",
        "program",
        "adviser",
    )
    list_select_related = (
        "research_field",
        "submitted_by",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = (
        "research_title",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "research_title__title",
        "abstract",
    )
    list_select_related = (
        "research_title",
    )