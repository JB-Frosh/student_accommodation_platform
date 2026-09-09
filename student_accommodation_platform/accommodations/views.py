from django.db.models import Avg, Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Listing
from .serializers import ListingSerializer, ScoredListingSerializer
from .services import compute_scam_flags, distance_from_campus, parse_preferences, rank_listings


def _parse_bool(value):
    return str(value).lower() in ("true", "1", "yes")


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    search_fields = ["title", "description", "address_text"]
    ordering_fields = ["price", "created_at", "rooms"]

    def get_queryset(self):
        return (
            Listing.objects.select_related("landlord")
            .annotate(
                avg_rating=Avg("reviews__rating"),
                review_count=Count("reviews", distinct=True),
            )
            .order_by("-created_at")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not hasattr(self, "_scam_flags"):
            self._scam_flags = compute_scam_flags()
        context["scam_flags"] = self._scam_flags
        return context

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params

        price_min = params.get("price_min")
        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        price_max = params.get("price_max")
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)

        electricity = params.get("electricity")
        if electricity:
            queryset = queryset.filter(electricity_availability=electricity)
        water = params.get("water")
        if water:
            queryset = queryset.filter(water_availability=water)
        internet = params.get("internet")
        if internet is not None:
            queryset = queryset.filter(internet_availability=_parse_bool(internet))

        min_rating = params.get("min_rating")
        if min_rating is not None:
            queryset = queryset.filter(avg_rating__gte=float(min_rating))

        queryset = self._filter_by_distance(queryset)
        return queryset

    def _filter_by_distance(self, queryset):
        params = self.request.query_params
        distance_min = params.get("distance_min")
        distance_max = params.get("distance_max")
        if distance_min is None and distance_max is None:
            return queryset

        listings = list(queryset)

        filtered = []
        for listing in listings:
            distance = distance_from_campus(listing)
            if distance_min is not None and distance < float(distance_min):
                continue
            if distance_max is not None and distance > float(distance_max):
                continue
            filtered.append(listing)
        return filtered

    @action(detail=False, methods=["get"], url_path="rank")
    def rank(self, request):
        budget = request.query_params.get("budget")
        max_distance = request.query_params.get("max_distance")
        if budget is None or max_distance is None:
            return Response(
                {"error": "The 'budget' and 'max_distance' query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset()
        min_rating = request.query_params.get("min_rating")
        if min_rating is not None:
            queryset = queryset.filter(avg_rating__gte=float(min_rating))

        preferences = parse_preferences(request.query_params)
        ranked = rank_listings(
            queryset,
            budget=float(budget),
            max_distance=float(max_distance),
            preferences=preferences,
        )
        return Response(
            ScoredListingSerializer(ranked, many=True, context=self.get_serializer_context()).data
        )

    @action(detail=False, methods=["get"], url_path="scam-flags")
    def scam_flags(self, request):
        flags = compute_scam_flags()
        flagged_ids = [listing_id for listing_id, info in flags.items() if info["flagged"]]
        listings = self.get_queryset().filter(id__in=flagged_ids)
        data = []
        for listing in listings:
            payload = ListingSerializer(listing, context=self.get_serializer_context()).data
            payload["scam_info"] = flags[listing.id]
            data.append(payload)
        return Response(data)