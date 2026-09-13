from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ElectricityAvailability(models.TextChoices):
    HOURS_24 = "24hr", "24 hours"
    RATIONED = "rationed", "Rationed"
    NONE = "none", "None"


class WaterAvailability(models.TextChoices):
    PIPE_BORNE = "pipe_borne", "Pipe-borne"
    BOREHOLE = "borehole", "Borehole"
    WELL = "well", "Well"
    NONE = "none", "None"


class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    landlord = models.ForeignKey(
        "landlords.Landlord",
        on_delete=models.CASCADE,
        related_name="listings",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Monthly rent in Nigerian Naira (NGN).",
    )
    rooms = models.PositiveIntegerField(default=1)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    address_text = models.CharField(max_length=300)
    electricity_availability = models.CharField(
        max_length=10,
        choices=ElectricityAvailability.choices,
    )
    water_availability = models.CharField(
        max_length=12,
        choices=WaterAvailability.choices,
    )
    internet_availability = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"]


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="listing-images/%Y/%m/")
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Image for {self.listing_id}"


class SecurityRating(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="security_ratings",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Security rating from 1 (poor) to 5 (excellent).",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.listing_id} - {self.rating}/5"