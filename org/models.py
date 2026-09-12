from django.db import models

# Create your models here.
class Announcement(models.Model):
  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=300, unique=True)

  summary = models.TextField(
    help_text='Short summary shown on the announcement page.'
  )

  content = models.TextField()
  published_at = models.DateTimeField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  is_published = models.BooleanField(default=False)

  class Meta: 
    ordering = ['-published_at']

  def __str__(self):
    return self.title
