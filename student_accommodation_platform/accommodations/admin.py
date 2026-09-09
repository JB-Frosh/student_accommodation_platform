from django.contrib import admin

from .models import Listing, SecurityRating


class SecurityRatingInline(admin.TabularInline):
    model = SecurityRating
    extra = 0


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "landlord",
        "price",
        "rooms",
        "electricity_availability",
        "water_availability",
        "internet_availability",
        "created_at",
    ]
    list_filter = [
        "electricity_availability",
        "water_availability",
        "internet_availability",
        "landlord__verified",
    ]
    search_fields = ["title", "description", "address_text"]
    inlines = [SecurityRatingInline]


@admin.register(SecurityRating)
class SecurityRatingAdmin(admin.ModelAdmin):
    list_display = ["id", "listing", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["listing__title"]