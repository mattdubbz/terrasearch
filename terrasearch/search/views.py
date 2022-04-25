from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import SearchScrapeForm
from .models import ForSaleProperty, LeadProperty, Search, SoldProperty
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
        form.save(self.request.user)
        return super(SearchCreateView, self).form_valid(form)


class LeadsListView(LoginRequiredMixin, generic.ListView):
    template_name = "search/leads_list.html"
    context_object_name = "leads"
    login_url = "account_login"

    def setup(self, request, *args, **kwargs):
        super(LeadsListView, self).setup(request, *args, **kwargs)
        search_pk = self.kwargs["pk"]
        scrape_async.delay(search_pk)
        self.kwargs["pk"] = search_pk
        return

    def get_queryset(self):
        search_pk = self.kwargs["pk"]
        search = get_object_or_404(Search, pk=search_pk)
        for_sale_props = ForSaleProperty.objects.filter(search=search_pk)
        sold_props = SoldProperty.objects.filter(search=search_pk)
        # get average sale price:
        avg_sold_price = 0
        count = 1
        sum = 0
        for sold in sold_props:
            sum += sold.sold_price
            count += 1
        avg_sold_price = sum / count
        # loop through all for-sale and sold-props to compare them
        for sale in for_sale_props:
            for sold in sold_props:
                if sale.list_price <= (avg_sold_price * 0.70):
                    if (sale.beds >= sold.beds - search.bed_diff) and (
                        sale.beds <= sold.beds + search.bed_diff
                    ):
                        if (sale.baths >= sold.baths - search.bath_diff) and (
                            sale.baths <= sold.baths + search.bath_diff
                        ):
                            if (sale.sqft >= sold.sqft - search.sqft_diff) and (
                                sale.sqft <= sold.sqft + search.sqft_diff
                            ):
                                LeadProperty.objects.create(
                                    search=search,
                                    list_price=sale.list_price,
                                    image=sale.image,
                                    link=sale.link,
                                    address=sale.address,
                                    city=sale.city,
                                    state=sale.state,
                                    zip=sale.zip,
                                    beds=sale.beds,
                                    baths=sale.baths,
                                    sqft=sale.sqft,
                                )
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
