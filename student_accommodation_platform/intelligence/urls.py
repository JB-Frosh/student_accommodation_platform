from django.urls import path

from .views import (
    AssistantView,
    NLPView,
    PredictionView,
    RecommendationView,
    ScamAnalysisView,
    VisionView,
)

urlpatterns = [
    path("recommendations/", RecommendationView.as_view(), name="intelligence-recommendations"),
    path("scam-analysis/", ScamAnalysisView.as_view(), name="intelligence-scam-analysis"),
    path("prediction/", PredictionView.as_view(), name="intelligence-prediction"),
    path("nlp/", NLPView.as_view(), name="intelligence-nlp"),
    path("vision/", VisionView.as_view(), name="intelligence-vision"),
    path("assistant/", AssistantView.as_view(), name="intelligence-assistant"),
]
