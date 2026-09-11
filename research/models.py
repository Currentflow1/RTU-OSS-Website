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
  research_field = models.ForeignKey(
    ResearchField,
    on_delete=models.PROTECT,
    related_name='research_titles'
  )
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=300, unique=True)

  description = models.TextField()
  authors = models.CharField(max_length=200, blank=True)
  publication_date = models.DateField(null=True, blank=True)

  is_published = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']

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





