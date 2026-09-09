from django.db.models import Count
from rest_framework import viewsets

from .models import Landlord
from .serializers import LandlordSerializer


class LandlordViewSet(viewsets.ModelViewSet):
    serializer_class = LandlordSerializer
    search_fields = ["name", "phone"]
    ordering_fields = ["date_joined", "name"]

    def get_queryset(self):
        queryset = Landlord.objects.annotate(listing_count=Count("listings"))
        return queryset.order_by("-date_joined")

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        verified = self.request.query_params.get("verified")
        if verified is not None:
            queryset = queryset.filter(verified=verified.lower() in ("true", "1", "yes"))
        return queryset