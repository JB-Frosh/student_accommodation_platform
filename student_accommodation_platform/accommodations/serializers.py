from rest_framework import serializers

from landlords.models import Landlord
from landlords.serializers import LandlordSerializer

from .models import Listing, SecurityRating
from .services import distance_from_campus, flag_scam_flag


class SecurityRatingSerializer(serializers.ModelSerializer):
    listing_id = serializers.PrimaryKeyRelatedField(
        source="listing", queryset=Listing.objects.all()
    )

    class Meta:
        model = SecurityRating
        fields = ["id", "listing_id", "rating", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]


class ListingSerializer(serializers.ModelSerializer):
    landlord = LandlordSerializer(read_only=True)
    landlord_id = serializers.PrimaryKeyRelatedField(
        source="landlord",
        queryset=Landlord.objects.all(),
        write_only=True,
    )
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    distance_from_campus = serializers.SerializerMethodField()
    scam_flag = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "landlord",
            "landlord_id",
            "price",
            "rooms",
            "latitude",
            "longitude",
            "address_text",
            "electricity_availability",
            "water_availability",
            "internet_availability",
            "created_at",
            "avg_rating",
            "review_count",
            "distance_from_campus",
            "scam_flag",
        ]
        read_only_fields = ["id", "created_at", "avg_rating", "review_count"]

    def get_distance_from_campus(self, obj):
        return distance_from_campus(obj)

    def get_scam_flag(self, obj):
        flags = self.context.get("scam_flags")
        if flags is not None:
            info = flags.get(obj.id)
            return bool(info and info.get("flagged", False))
        return flag_scam_flag(obj)


class ScoredListingSerializer(serializers.Serializer):
    listing = ListingSerializer(read_only=True)
    score = serializers.FloatField()
    distance_km = serializers.FloatField()
    components = serializers.DictField(child=serializers.FloatField())