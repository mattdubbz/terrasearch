from django import forms
from django import forms
from .models import Search


class SearchScrapeForm(forms.ModelForm):
    class Meta:
        model = Search
        exclude = ['user']
