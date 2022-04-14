from django.urls import path
from .views import SearchCreateView, SearchDeleteView, SearchUpdateView, SearchListView, SearchResultsView, SearchDetailView

app_name = "search"
urlpatterns = [
    path("", SearchCreateView.as_view(), name="search-create"),
    path("search_list/", SearchListView.as_view(), name="search-list"),
    path("search_list/", SearchUpdateView.as_view(), name="search-update"),
    path("search_list/", SearchDeleteView.as_view(), name="search-delete"),
    path("search_results", SearchResultsView.as_view(), name="search-resutls")
]
