from django import forms

from .models import Search


class SearchScrapeForm(forms.ModelForm):
    class Meta:
        model = Search
        exclude = ["user"]

    def save(self, user=None):
        search = super(SearchScrapeForm, self).save(commit=False)
        if user:
            search.user = user
        search.save()
        return search
