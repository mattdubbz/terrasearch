from django.urls import path

from .views import (
    SearchCreateView,
    SearchDeleteView,
    SearchDetailView,
    SearchListView,
    SearchResultsView,
    SearchUpdateView,
)

app_name = "search"
urlpatterns = [
    path("", SearchCreateView.as_view(), name="search-create"),
    path("search_list/", SearchListView.as_view(), name="search-list"),
    path("search_detail/", SearchDetailView.as_view(), name="search-detail"),
    path("search_update/", SearchUpdateView.as_view(), name="search-update"),
    path("search_delete/", SearchDeleteView.as_view(), name="search-delete"),
    path("search_results", SearchResultsView.as_view(), name="search-resutls"),
]
