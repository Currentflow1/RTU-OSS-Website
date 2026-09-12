from django.db import models

# Create your models here.
class ResearchField(models.Model):
  name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  description = models.TextField(blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['name']

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
    publication_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    related_name='papers'
  )

  abstract = models.TextField()
  document = models.FileField(upload_to='research/papers/')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.research_title.title





