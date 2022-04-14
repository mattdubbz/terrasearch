from django import forms

from .models import Search


class SearchScrapeForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ["city", "state", "bed_diff", "bath_diff", "year_built_diff"]
