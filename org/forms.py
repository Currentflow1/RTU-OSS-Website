from django import forms
from django.utils import timezone

from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
                "class": (
                    "w-full rounded-lg border border-[#d8c3a8] "
                    "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                    "outline-none transition "
                    "focus:border-[#8a5a36] focus:ring-2 "
                    "focus:ring-[#8a5a36]/20"
                ),
            },
        ),
    )

    class Meta:
        model = Announcement
        fields = [
            "title",
            "summary",
            "content",
            "published_at",
            "is_published",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Announcement title",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "summary": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Short summary of the announcement...",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "Write the full announcement...",
                    "class": (
                        "w-full rounded-lg border border-[#d8c3a8] "
                        "bg-white px-4 py-3 text-sm text-[#4a2d1c] "
                        "placeholder-[#9a806b] outline-none transition "
                        "focus:border-[#8a5a36] focus:ring-2 "
                        "focus:ring-[#8a5a36]/20"
                    ),
                }
            ),
            "is_published": forms.CheckboxInput(
                attrs={
                    "class": (
                        "h-4 w-4 rounded border-[#d8c3a8] "
                        "text-[#6f4328] focus:ring-[#8a5a36]"
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.published_at:
            self.initial["published_at"] = timezone.localtime(
                self.instance.published_at
            ).strftime("%Y-%m-%dT%H:%M")
        elif not self.initial.get("published_at"):
            self.initial["published_at"] = timezone.localtime().strftime(
                "%Y-%m-%dT%H:%M"
            )