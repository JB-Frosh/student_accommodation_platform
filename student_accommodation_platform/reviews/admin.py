from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "listing", "reviewer_name", "user", "rating", "created_at"]
    list_filter = ["rating"]
    search_fields = ["reviewer_name", "comment", "listing__title"]