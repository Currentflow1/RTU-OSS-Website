from django.conf import settings
from django.db import models


class ResearchField(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ResearchTitle(models.Model):

    class PublicationStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending Review"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"

    research_field = models.ForeignKey(
        ResearchField,
        on_delete=models.PROTECT,
        related_name="research_titles",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField()
    authors = models.CharField(max_length=200, blank=True)
    keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="Separate keywords with commas.",
    )
    department = models.CharField(max_length=200, blank=True)
    program = models.CharField(max_length=200, blank=True)
    adviser = models.CharField(max_length=200, blank=True)
    school_year = models.CharField(
        max_length=20,
        blank=True,
        help_text="Example: 2025-2026",
    )
    publication_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="research_submissions",
        null=True,
        blank=True,
    )
    submitter_email = models.EmailField(
        blank=True,
        help_text="Optional email address for contacting the submitter.",
    )
    publication_status = models.CharField(
        max_length=20,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
    )

    def __str__(self):
        return self.title



class ResearchPaper(models.Model):
    research_title = models.ForeignKey(
        ResearchTitle,
        on_delete=models.CASCADE,
        related_name="papers",
    )
    abstract = models.TextField()
    document = models.FileField(
        upload_to="research/papers/",
        max_length=500,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.research_title.title