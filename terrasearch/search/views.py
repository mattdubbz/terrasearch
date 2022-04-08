from django.views import generic

from .models import Search


class SearchListView(generic.ListView):
    model = Search
    template_name = "search_list.html"
    queryset = Search.objects.all()
    context_object_name = "searches"
