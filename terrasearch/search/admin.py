from django.contrib import admin

from .models import Comparable, LeadProperty, Search


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ["city", "state", "user"]
    search_fields = ["city", "state", "user"]


admin.site.register(LeadProperty)
admin.site.register(Comparable)
