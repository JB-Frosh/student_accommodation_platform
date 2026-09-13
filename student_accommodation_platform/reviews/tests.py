from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accommodations.models import Listing
from landlords.models import Landlord

from .models import Review


class ReviewApiTests(APITestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="reviewer",
			password="test-password",
		)
		landlord = Landlord.objects.create(name="Ada Landlord", phone="08012345678")
		self.listing = Listing.objects.create(
			title="Epe Student Room",
			landlord=landlord,
			price="250000.00",
			latitude=6.59,
			longitude=3.996,
			address_text="Epe, Lagos",
			electricity_availability="24hr",
			water_availability="borehole",
		)

	def test_anonymous_user_cannot_create_review(self):
		response = self.client.post(
			"/api/reviews/",
			{"listing_id": self.listing.id, "rating": 5, "comment": "Excellent."},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_authenticated_review_is_attributed_to_user(self):
		self.client.force_authenticate(user=self.user)

		response = self.client.post(
			"/api/reviews/",
			{"listing_id": self.listing.id, "rating": 5, "comment": "Excellent."},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Review.objects.get().user, self.user)
		self.assertEqual(response.data["reviewer_name"], "reviewer")
