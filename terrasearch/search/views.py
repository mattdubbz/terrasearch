from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from .forms import SearchScrapeForm
from .models import LeadProperty, Search
from .tasks import scrape_async


class SearchListView(LoginRequiredMixin, generic.ListView):
    model = Search
    template_name = "search/search_list.html"
    queryset = Search.objects.all()
    context_object_name = "searches"


class SearchDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "search/search_detail.html"
    model = Search
    context_object_name = "search"


class SearchCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "search/search_create.html"
    form_class = SearchScrapeForm

    def get_success_url(self):
        return reverse("search:search-results", kwargs={"pk": self.search.pk})

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.reuqest.user
        instance.save()
        self.search = instance
        return super(SearchCreateView, self).form_valid(form)


class SearchUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "search/search_update.html"
    form_class = SearchScrapeForm

    def get_queryset(self):
        return Search.objects.filter(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("search:search-detail", kwargs={"pk": self.get_object().pk})


class SearchDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "search/search_delete.html"

    def get_queryset(self):
        return Search.objects.filter(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("search:search-list")


class SearchResultsView(LoginRequiredMixin, generic.ListView):
    template_name = "search/search_results.html"
    model = LeadProperty
    context_object_name = "results"

    def get_queryset(self):
        qs = LeadProperty.objects.all()
        list_price = self.request.GET.get("list_price", None)
        if list_price:
            qs = qs.filter(list_price__icontains=list_price)
        return qs.order_by("-list_price")

    def form_valid(self, form):
        scrape_async.delay()
        return super(SearchResultsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        count = LeadProperty.objects.all().count()
        context.update({"total_count": count})
        return context
