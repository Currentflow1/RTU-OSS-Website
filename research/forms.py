from django import forms

from .models import ResearchField, ResearchTitle


class ResearchSubmissionForm(forms.ModelForm):
    abstract = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": "Enter the research abstract...",
                "class": (
                    "w-full rounded-lg border border-[#d8c3a8] "
                    "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                    "placeholder-[#9a806b] outline-none transition "
                    "focus:border-[#8a5a36] focus:ring-2 "
                    "focus:ring-[#8a5a36]/20"
                ),
            }
        )
    )

    submitter_email = forms.EmailField(
        required=False,
        label="Email Address",
        help_text="Optional. We may use this to contact you about your submission.",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email address (optional)",
                "class": (
                    "w-full rounded-lg border border-[#d8c3a8] "
                    "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                    "placeholder-[#9a806b] outline-none transition "
                    "focus:border-[#8a5a36] focus:ring-2 "
                    "focus:ring-[#8a5a36]/20"
                ),
            }
        ),
    )

    document = forms.FileField(
        label="Research Document",
        help_text="Upload the final research document as a PDF.",
        widget=forms.ClearableFileInput(
            attrs={
                "class": (
                    "block w-full rounded-lg border border-[#d8c3a8] "
                    "bg-white text-sm text-[#4a2d1c] "
                    "file:mr-4 file:rounded-md file:border-0 "
                    "file:bg-[#f3eadc] file:px-4 file:py-2 "
                    "file:text-sm file:font-semibold "
                    "file:text-[#6f4328] "
                    "hover:file:bg-[#eadcc9] "
                    "focus:outline-none"
                ),
            }
        ),
    )

    class Meta:
        model = ResearchTitle
        fields = [
            "research_field",
            "title",
            "description",
            "authors",
            "keywords",
            "department",
            "program",
            "adviser",
            "school_year",
            "submitter_email",
        ]
        widgets = {
            "research_field": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Research title",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Brief description of the research...",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "authors": forms.TextInput(
                attrs={
                    "placeholder": "Author names",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "keywords": forms.TextInput(
                attrs={
                    "placeholder": "Example: regression, probability, statistics",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "department": forms.TextInput(
                attrs={
                    "placeholder": "Department",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "program": forms.TextInput(
                attrs={
                    "placeholder": "Degree or academic program",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "adviser": forms.TextInput(
                attrs={
                    "placeholder": "Research adviser",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "school_year": forms.TextInput(
                attrs={
                    "placeholder": "Example: 2025-2026",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["research_field"].queryset = (
            ResearchField.objects.order_by("name")
        )

    def clean_document(self):
        document = self.cleaned_data["document"]

        if not document.name.lower().endswith(".pdf"):
            raise forms.ValidationError(
                "Only PDF documents are accepted."
            )

        return document