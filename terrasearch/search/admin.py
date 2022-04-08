from django.contrib import admin

from .models import Comparable, LeadProperty, Search


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ["address", "zip", "user"]
    search_fields = ["address", "zip", "user"]


admin.site.register(LeadProperty)
admin.site.register(Comparable)
