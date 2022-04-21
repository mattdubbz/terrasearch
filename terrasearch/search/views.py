from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import SearchScrapeForm
from .models import LeadProperty, Search
from .tasks import scrape_async


class SearchListView(LoginRequiredMixin, generic.ListView):
    template_name = "search/search_list.html"
    model = Search
    context_object_name = "searches"
    login_url = "account_login"

    def get_queryset(self):
        return Search.objects.filter(user=self.request.user)


class SearchDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "search/search_detail.html"
    model = Search
    context_object_name = "search"
    login_url = "account_login"


class SearchUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "search/search_update.html"
    model = Search
    context_object_name = "search"
    form_class = SearchScrapeForm
    login_url = "account_login"

    def get_success_url(self):
        return reverse_lazy("search:search-detail", kwargs={"pk": self.kwargs["pk"]})


class SearchDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "search/search_delete.html"
    model = Search
    success_url = reverse_lazy("search:search-list")
    login_url = "account_login"


class SearchCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "search/search_create.html"
    model = Search
    form_class = SearchScrapeForm
    login_url = "account_login"

    def form_valid(self, form):
        scrape_async.delay()
        form.save(self.request.user)
        return super(SearchCreateView, self).form_valid(form)


class LeadsListView(LoginRequiredMixin, generic.ListView):
    template_name = "search/lead_list.html"
    context_object_name = "leads"
    login_url = "account_login"

    def get_queryset(self):
        search_pk = self.kwargs["pk"]
        search = get_object_or_404(Search, pk=search_pk)
        leads = search.leads.all()

        # LeadProperty.objects.filter(search=search_pk)
        # # OR
        # LeadProperty.objects.filter(search=search)
        # search = get_object_or_404(Search, pk=search.pk)
        # LeadProperty.objects.filter(search=search)

        return leads

    def get_context_data(self, **kwargs):
        context = super(LeadsListView, self).get_context_data(**kwargs)
        search_pk = self.kwargs["pk"]
        search = get_object_or_404(Search, pk=search_pk)
        count = LeadProperty.objects.filter(search=search).count()
        context["total_count"] = count
        return context
