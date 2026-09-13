from django.db.models import Avg, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accommodations.serializers import ListingSerializer
from accommodations.models import Listing

from .scoring import rank_listings, scam_flags


def _number(params, key, default=None):
    value = params.get(key, default)
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        raise ValueError(f"'{key}' must be a number.")


def _preferences(params):
    preferences = {}
    if params.get("electricity"):
        preferences["electricity"] = params["electricity"]
    if params.get("water"):
        preferences["water"] = params["water"]
    if params.get("internet") is not None:
        preferences["internet"] = params["internet"].lower() in ("true", "1", "yes", "on")
    return preferences


class RecommendationView(APIView):
    """Stage 1: explainable ranking for a student's LASU Epe preferences."""

    def get(self, request):
        try:
            budget = _number(request.query_params, "budget", 0)
            max_distance = _number(request.query_params, "max_distance", 0)
            weights = {
                key: _number(request.query_params, f"w_{key}", None)
                for key in ("budget", "distance", "facilities", "rating")
            }
            weights = {key: value for key, value in weights.items() if value is not None}
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Listing.objects.select_related("landlord").annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews", distinct=True),
        )
        ranked = rank_listings(
            queryset,
            budget=budget,
            max_distance=max_distance,
            preferences=_preferences(request.query_params),
            weights=weights,
        )
        data = []
        for item in ranked:
            data.append(
                {
                    "listing": ListingSerializer(item["listing"], context={"request": request}).data,
                    "score": item["score"],
                    "distance_km": item["distance_km"],
                    "components": item["components"],
                    "weights": item["weights"],
                }
            )
        return Response({"stage": 1, "method": "rule_based", "results": data})


class ScamAnalysisView(APIView):
    """Stage 1: distance-band price anomaly flags."""

    def get(self, request):
        listings = list(Listing.objects.all())
        try:
            ratio = _number(request.query_params, "low_price_ratio", 0.60)
            band_width = _number(request.query_params, "band_width_km", 1.0)
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        flags = scam_flags(listings, low_price_ratio=ratio, band_width=band_width)
        return Response({"stage": 1, "method": "distance_band_price_threshold", "results": flags})


class IntelligenceStubView(APIView):
    """Document a future intelligence stage without pretending it is active."""

    stage = None
    name = ""
    description = ""
    requirements = []

    def get(self, request):
        return Response(
            {
                "stage": self.stage,
                "status": "planned",
                "name": self.name,
                "description": self.description,
                "requirements": self.requirements,
            }
        )


class PredictionView(IntelligenceStubView):
    stage = 2
    name = "statistical ML"
    description = "Train rent regression, learned feedback ranking, and isolation-forest anomaly detection after at least 100 listings."
    requirements = ["scikit-learn", "at least 100 quality listings", "save/click feedback"]


class NLPView(IntelligenceStubView):
    stage = 3
    name = "review NLP"
    description = "Generate review sentiment, trust scores, and structured issue flags once real review text exists."
    requirements = ["real review text", "transformers or a lexicon model"]


class VisionView(IntelligenceStubView):
    stage = 4
    name = "photo intelligence"
    description = "Detect reused listing photos with perceptual hashes and optionally estimate room condition later."
    requirements = ["imagehash", "Pillow", "listing images"]


class AssistantView(IntelligenceStubView):
    stage = 5
    name = "conversational personalization"
    description = "Parse natural-language searches into filters and send predictive alerts for matching listings."
    requirements = ["saved searches", "notification channel", "language parser"]
