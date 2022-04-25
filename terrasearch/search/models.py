from django.db import models
from django.urls import reverse

"""Base abstract model for all properties and Search model to inherit from"""


class Property(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    year_built = models.IntegerField(blank=True, null=True)
    sqft = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.address


# ------------------------------------------------------------------------------
"""Comparable is a property that has already sold that is similar to the search criteria.
Its presence indicates that a LeadProperty may exists if it is similar and nearby the Comparable."""


class Comparable(Property):
    search = models.ForeignKey(
        "search.Search", on_delete=models.CASCADE, related_name="comps"
    )
    date_sold = models.DateField(blank=True, null=True)
    sold_price = models.IntegerField()
    distance = models.DecimalField(
        blank=True, null=True, max_digits=3, decimal_places=2
    )
    image = models.ImageField(
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
        blank=True,
        null=True,
    )
    link = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Comparable"
        verbose_name_plural = "Comparables"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("search:comparable-detail", kwargs={"pk": self.pk})


# ------------------------------------------------------------------------------
"""A SoldProperty is a property in the sold search results used for comparison with
ForSale properties using the search criteria to determine if a LeadProperty is present
or if a Comparable is present.  It is conceptually different than a Comparable and used
for comaprison purposes only."""


class SoldProperty(Property):
    search = models.ForeignKey(
        "search.Search", on_delete=models.CASCADE, related_name="sold_props"
    )
    date_sold = models.DateField(blank=True, null=True)
    sold_price = models.IntegerField()
    distance = models.DecimalField(
        blank=True, null=True, max_digits=3, decimal_places=2
    )
    image = models.ImageField(
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
        blank=True,
        null=True,
    )
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Sold Property"
        verbose_name_plural = "Sold Properties"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("search:sold-property-detail", kwargs={"pk": self.pk})


# ------------------------------------------------------------------------------
"""A ForSaleProperty is a property in the for-sale search results used for comparison
with SoldProperties using the search criteria to determine is a LeadProperty or
Comparable is present.  It is conceptually different than a LeadProperty and
used for comparison purposes only."""


class ForSaleProperty(Property):
    search = models.ForeignKey(
        "search.Search", on_delete=models.CASCADE, related_name="for_sale_props"
    )
    list_price = models.IntegerField(blank=True, null=True)
    list_date = models.DateField(blank=True, null=True)
    image = models.ImageField(
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
        blank=True,
        null=True,
    )
    link = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("search:for-sale-property-detail", kwargs={"pk": self.pk})


# ------------------------------------------------------------------------------
"""A LeadProperty is one that meets all search criteria and is returned by the
search. A LeadProperty has not been sold but is up for sale, A Lead in the
sense that it is a lead for the investor to look at and can be flipped."""


class LeadProperty(Property):
    search = models.ForeignKey(
        "search.Search", on_delete=models.CASCADE, related_name="leads"
    )
    list_price = models.IntegerField(blank=True, null=True)
    list_date = models.DateField(blank=True, null=True)
    image = models.ImageField(
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=100,
        blank=True,
        null=True,
    )
    link = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("search:lead-detail", kwargs={"pk": self.pk})


# ------------------------------------------------------------------------------
"""The Search model represents the search criteria used to locate a LeadProperty
based on the existance of Comparables.  A user can have many searches and
searches can be re-used."""


class Search(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="searches"
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    bed_diff = models.IntegerField(default=1)
    bath_diff = models.DecimalField(max_digits=3, decimal_places=1, default=0.5)
    year_built_diff = models.IntegerField(blank=True, null=True)
    sqft_diff = models.IntegerField(default=150)

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    def __str__(self):
        return self.city + ", " + self.state

    def get_absolute_url(self):
        return reverse("search:search-detail", kwargs={"pk": self.pk})
