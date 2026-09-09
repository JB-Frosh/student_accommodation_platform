from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    listing = models.ForeignKey(
        "accommodations.Listing",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    reviewer_name = models.CharField(max_length=150, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="review_rating_range",
            ),
        ]

    def __str__(self):
        author = self.user.get_username() if self.user else self.reviewer_name
        return f"{self.listing_id} - {author}: {self.rating}/5"