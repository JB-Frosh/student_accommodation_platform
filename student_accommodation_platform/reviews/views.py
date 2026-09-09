from rest_framework import viewsets

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    search_fields = ["reviewer_name", "comment"]
    ordering_fields = ["created_at", "rating"]

    def get_queryset(self):
        return Review.objects.select_related("listing", "user").order_by("-created_at")

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params

        listing_id = params.get("listing")
        if listing_id:
            queryset = queryset.filter(listing_id=listing_id)

        rating_min = params.get("rating_min")
        if rating_min is not None:
            queryset = queryset.filter(rating__gte=rating_min)
        rating_max = params.get("rating_max")
        if rating_max is not None:
            queryset = queryset.filter(rating__lte=rating_max)

        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()