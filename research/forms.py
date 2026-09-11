from django import forms

from .models import ResearchField, ResearchTitle, ResearchPaper


class ResearchFieldForm(forms.ModelForm):
    class Meta:
        model = ResearchField
        fields = [
            "name",
            "slug",
            "description",
        ]


class ResearchTitleForm(forms.ModelForm):
    class Meta:
        model = ResearchTitle
        fields = [
            "research_field",
            "title",
            "slug",
            "description",
            "authors",
            "publication_date",
            "is_published",
        ]


class ResearchPaperForm(forms.ModelForm):
    class Meta:
        model = ResearchPaper
        fields = [
            "research_title",
            "abstract",
            "document",
        ]