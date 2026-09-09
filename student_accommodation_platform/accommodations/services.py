from django.conf import settings

from .geo import haversine_distance_km
from .models import Listing

SCORING_WEIGHTS = {
    "price": 0.35,
    "distance": 0.25,
    "facility": 0.30,
    "rating": 0.10,
}

DISTANCE_BAND_KM = 1.0
LOW_PRICE_RATIO = 0.6
MIN_BAND_SIZE = 3


def campus_coordinates():
    return (
        settings.LASU_EPE_CAMPUS["lat"],
        settings.LASU_EPE_CAMPUS["lng"],
    )


def parse_preferences(params):
    preferences = {}
    for key in ("electricity", "water"):
        value = params.get(key)
        if value:
            preferences[key] = value
    internet = params.get("internet")
    if internet is not None:
        if str(internet).lower() in ("true", "1", "yes", "on"):
            preferences["internet"] = True
        elif str(internet).lower() in ("false", "0", "no", "off"):
            preferences["internet"] = False
    return preferences


def distance_from_campus(listing):
    lat, lng = campus_coordinates()
    return haversine_distance_km(listing.latitude, listing.longitude, lat, lng)


def _price_score(price, budget):
    price = float(price)
    if budget <= 0:
        return 1.0
    if price <= budget:
        return 1.0
    return max(0.0, 1.0 - (price - budget) / budget)


def _distance_score(distance, max_distance):
    if max_distance <= 0:
        return 1.0
    if distance <= max_distance:
        return 1.0
    return max(0.0, 1.0 - (distance - max_distance) / max_distance)


def facility_match_score(listing, preferences):
    requested = 0
    matched = 0

    electricity = preferences.get("electricity")
    if electricity:
        requested += 1
        matched += int(listing.electricity_availability == electricity)

    water = preferences.get("water")
    if water:
        requested += 1
        matched += int(listing.water_availability == water)

    internet = preferences.get("internet")
    if internet is not None:
        requested += 1
        matched += int(listing.internet_availability == internet)

    if requested == 0:
        return 1.0
    return matched / requested


def rank_listings(queryset, *, budget, max_distance, preferences=None):
    preferences = preferences or {}
    weighted = []

    for listing in queryset:
        distance = distance_from_campus(listing)
        components = {
            "price": _price_score(listing.price, budget),
            "distance": _distance_score(distance, max_distance),
            "facility": facility_match_score(listing, preferences),
            "rating": float(getattr(listing, "avg_rating", None) or 0) / 5.0,
        }
        score = sum(SCORING_WEIGHTS[k] * v for k, v in components.items())
        weighted.append(
            {
                "listing": listing,
                "score": round(score, 4),
                "distance_km": round(distance, 2),
                "components": {k: round(v, 4) for k, v in components.items()},
            }
        )

    weighted.sort(key=lambda item: item["score"], reverse=True)
    return weighted


def _distance_band(distance_km, band_width=DISTANCE_BAND_KM):
    return int(distance_km // band_width)


def compute_scam_flags(queryset=None, low_price_ratio=LOW_PRICE_RATIO, band_width=DISTANCE_BAND_KM):
    """Flag listings priced below `low_price_ratio` x the average price of
    comparable listings in the same distance band from campus."""
    listings = list(queryset) if queryset is not None else list(Listing.objects.all())

    bands = {}
    for listing in listings:
        band = _distance_band(distance_from_campus(listing), band_width)
        bands.setdefault(band, []).append(listing)

    flags = {}
    for band, band_listings in bands.items():
        if len(band_listings) < MIN_BAND_SIZE:
            continue
        band_average = sum(float(l.price) for l in band_listings) / len(band_listings)
        for listing in band_listings:
            price_ratio = float(listing.price) / band_average if band_average else 1.0
            flags[listing.id] = {
                "flagged": price_ratio < low_price_ratio,
                "band": band,
                "band_average": round(band_average, 2),
                "band_size": len(band_listings),
                "price_ratio": round(price_ratio, 4),
            }
    return flags


def flag_scam_flag(listing):
    return bool(compute_scam_flags().get(listing.id, {}).get("flagged", False))