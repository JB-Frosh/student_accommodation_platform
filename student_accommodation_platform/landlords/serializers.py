from rest_framework import serializers

from .models import Landlord


class LandlordSerializer(serializers.ModelSerializer):
    listing_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Landlord
        fields = ["id", "name", "phone", "verified", "date_joined", "listing_count"]
        read_only_fields = ["id", "date_joined", "listing_count"]