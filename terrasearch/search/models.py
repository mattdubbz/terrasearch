from django.db import models
from django.urls import reverse


# Base abstract model for all properties and Search model to inherit from
class Property(models.Model):
    address = models.CharField(max_length=100)
    zip = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    year_built = models.IntegerField()
    sqft = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.address


# ------------------------------------------------------------------------------
# A LeadProperty is one that meets all search criteria and is returned by the search.
# A LeadProperty has not been sold but is up for sale
# A Lead in the sense that it is a lead for the investor to look at and can be flipped.
class LeadProperty(Property):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="leads"
    )
    list_price = models.IntegerField()
    list_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "LeadProperty"
        verbose_name_plural = "LeadProperties"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("LeadProperty_detail", kwargs={"pk": self.pk})


# ------------------------------------------------------------------------------
# Comparble is a property that has already sold that is similar to the search criteria.
# Its presence indicates that a LeadProperty may exists if it is similar and nearby the Comparable.
class Comparable(Property):
    date_sold = models.DateField(blank=True, null=True)
    sold_price = models.IntegerField()
    distance = models.DecimalField(
        blank=True, null=True, max_digits=3, decimal_places=2
    )

    class Meta:
        verbose_name = "Comparable"
        verbose_name_plural = "Comparables"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("Comparable_detail", kwargs={"pk": self.pk})


# ------------------------------------------------------------------------------
# The Search model represents the search criteria used to locate a LeadProperty based on the existance
# of Comparables.  A user can have many searches and searches can be re-used.
class Search(Property):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="searches"
    )
    address = models.CharField(max_length=100, blank=True, null=True)
    comp_count = models.IntegerField(default=1)
    bed_diff = models.IntegerField(default=1)
    bath_diff = models.IntegerField(default=1)
    year_built_diff = models.IntegerField(default=10)
    distance_diff = models.DecimalField(
        max_digits=3, decimal_places=2, default=0, blank=True, null=True
    )
    sqft_diff = models.IntegerField(default=150)

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("Search_detail", kwargs={"pk": self.pk})
