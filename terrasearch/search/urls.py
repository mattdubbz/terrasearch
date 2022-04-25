from django.urls import path

from .views import (
    LeadsListView,
    SearchCreateView,
    SearchDeleteView,
    SearchDetailView,
    SearchListView,
    SearchUpdateView,
)

app_name = "search"
urlpatterns = [
    path("", SearchCreateView.as_view(), name="search-create"),
    path("search_list/", SearchListView.as_view(), name="search-list"),
    path("search_detail/<int:pk>/", SearchDetailView.as_view(), name="search-detail"),
    path("search_update/<int:pk>/", SearchUpdateView.as_view(), name="search-update"),
    path("search_delete/<int:pk>/", SearchDeleteView.as_view(), name="search-delete"),
    path(
        "lead_list/<int:pk>", LeadsListView.as_view(), name="leads-list"
    ),  # int is pk of the Search object
]
