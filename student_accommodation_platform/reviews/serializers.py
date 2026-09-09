from rest_framework import serializers

from accommodations.models import Listing

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    listing_id = serializers.PrimaryKeyRelatedField(
        source="listing", queryset=Listing.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "listing_id", "user", "reviewer_name", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def validate(self, attrs):
        user = getattr(self.context.get("request"), "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            if not attrs.get("reviewer_name"):
                attrs["reviewer_name"] = user.get_full_name() or user.username
        elif not attrs.get("reviewer_name"):
            raise serializers.ValidationError(
                {"reviewer_name": "Reviewer name is required for anonymous reviewers."}
            )
        return attrs