from django.contrib import admin

from .models import ResearchField, ResearchTitle, ResearchPaper


admin.site.register(ResearchField)
admin.site.register(ResearchTitle)
admin.site.register(ResearchPaper)