from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from landlords.models import Landlord

from .models import Listing


class ListingApiTests(APITestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="student",
			password="test-password",
		)
		self.landlord = Landlord.objects.create(
			name="Ada Landlord",
			phone="08012345678",
		)
		self.listing_data = {
			"title": "Epe Student Room",
			"description": "A clean room near campus.",
			"landlord_id": self.landlord.id,
			"price": "250000.00",
			"rooms": 1,
			"latitude": 6.59,
			"longitude": 3.996,
			"address_text": "Epe, Lagos",
			"electricity_availability": "24hr",
			"water_availability": "borehole",
			"internet_availability": True,
		}

	def test_listing_can_be_read_anonymously(self):
		Listing.objects.create(**self.listing_data)

		response = self.client.get("/api/listings/")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["count"], 1)

	def test_anonymous_user_cannot_create_listing(self):
		response = self.client.post("/api/listings/", self.listing_data, format="json")

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_user_can_create_listing(self):
		self.client.force_authenticate(user=self.user)

		response = self.client.post("/api/listings/", self.listing_data, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["title"], self.listing_data["title"])
