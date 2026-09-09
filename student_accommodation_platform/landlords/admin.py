from django.contrib import admin

from .models import Landlord


@admin.register(Landlord)
class LandlordAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "phone", "verified", "date_joined"]
    list_filter = ["verified"]
    search_fields = ["name", "phone"]