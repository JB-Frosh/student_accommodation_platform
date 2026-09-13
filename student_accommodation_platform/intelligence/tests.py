from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accommodations.models import Listing
from landlords.models import Landlord


class IntelligenceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        landlord = Landlord.objects.create(name="LASU Homes", phone="08012345678")
        self.listing = Listing.objects.create(
            title="Epe Campus Room",
            landlord=landlord,
            price="250000.00",
            rooms=1,
            latitude=6.5905,
            longitude=3.9965,
            address_text="Near LASU Epe campus",
            electricity_availability="24hr",
            water_availability="borehole",
            internet_availability=True,
        )

    def test_stage_one_recommendations_return_explanation(self):
        response = self.client.get(
            "/api/intelligence/recommendations/",
            {"budget": "300000", "max_distance": "2", "internet": "true"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stage"], 1)
        result = response.data["results"][0]
        self.assertEqual(result["listing"]["id"], self.listing.id)
        self.assertIn("budget", result["components"])
        self.assertIn("weights", result)

    def test_recommendations_reject_invalid_numbers(self):
        response = self.client.get(
            "/api/intelligence/recommendations/",
            {"budget": "not-a-number"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_scam_analysis_returns_distance_band_result(self):
        response = self.client.get("/api/intelligence/scam-analysis/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.listing.id, response.data["results"])
        self.assertIn("distance_band_km", response.data["results"][self.listing.id])

    def test_later_stages_are_explicitly_planned(self):
        for stage in ("prediction", "nlp", "vision", "assistant"):
            response = self.client.get(f"/api/intelligence/{stage}/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["status"], "planned")
