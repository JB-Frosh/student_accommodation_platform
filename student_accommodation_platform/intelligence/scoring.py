"""Stage 1 rule-based intelligence for the LASU Epe case study.

This module deliberately has no ML dependency. It provides deterministic,
explainable scores while the platform collects enough data for later stages.
"""

from collections import defaultdict

from accommodations.services import distance_from_campus

DEFAULT_WEIGHTS = {
    "budget": 0.35,
    "distance": 0.25,
    "facilities": 0.30,
    "rating": 0.10,
}
DISTANCE_BAND_KM = 1.0
DEFAULT_LOW_PRICE_RATIO = 0.60
MIN_BAND_SIZE = 3


def _bounded(value):
    return round(max(0.0, min(1.0, value)), 4)


def _budget_fit(price, budget):
    if budget <= 0:
        return 1.0
    return _bounded(1 - max(0.0, float(price) - budget) / budget)


def _distance_fit(distance, max_distance):
    if max_distance <= 0:
        return 1.0
    return _bounded(1 - max(0.0, distance - max_distance) / max_distance)


def _facilities_match(listing, preferences):
    checks = []
    if preferences.get("electricity"):
        checks.append(listing.electricity_availability == preferences["electricity"])
    if preferences.get("water"):
        checks.append(listing.water_availability == preferences["water"])
    if "internet" in preferences:
        checks.append(listing.internet_availability == preferences["internet"])
    return sum(checks) / len(checks) if checks else 1.0


def normalise_weights(weights=None):
    values = {**DEFAULT_WEIGHTS, **(weights or {})}
    values = {key: max(0.0, float(value)) for key, value in values.items()}
    total = sum(values.values()) or 1.0
    return {key: value / total for key, value in values.items()}


def score_listing(listing, *, budget, max_distance, preferences=None, weights=None):
    """Return an explainable 0-1 suitability score for one listing."""
    preferences = preferences or {}
    distance = distance_from_campus(listing)
    components = {
        "budget": _budget_fit(listing.price, budget),
        "distance": _distance_fit(distance, max_distance),
        "facilities": _facilities_match(listing, preferences),
        "rating": _bounded(float(getattr(listing, "avg_rating", None) or 0) / 5),
    }
    applied_weights = normalise_weights(weights)
    score = sum(components[key] * applied_weights[key] for key in components)
    return {
        "score": round(score, 4),
        "distance_km": round(distance, 2),
        "components": components,
        "weights": {key: round(value, 4) for key, value in applied_weights.items()},
    }


def rank_listings(listings, *, budget, max_distance, preferences=None, weights=None):
    ranked = []
    for listing in listings:
        result = score_listing(
            listing,
            budget=budget,
            max_distance=max_distance,
            preferences=preferences,
            weights=weights,
        )
        ranked.append({"listing": listing, **result})
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


def scam_flags(listings, *, low_price_ratio=DEFAULT_LOW_PRICE_RATIO, band_width=DISTANCE_BAND_KM):
    """Flag prices below a configurable ratio of their distance-band average."""
    bands = defaultdict(list)
    for listing in listings:
        distance = distance_from_campus(listing)
        bands[int(distance // band_width)].append(listing)

    flags = {}
    for band, members in bands.items():
        average = sum(float(item.price) for item in members) / len(members)
        for listing in members:
            ratio = float(listing.price) / average if average else 1.0
            flags[listing.id] = {
                "flagged": len(members) >= MIN_BAND_SIZE and ratio < low_price_ratio,
                "distance_band_km": [round(band * band_width, 2), round((band + 1) * band_width, 2)],
                "band_average_price": round(average, 2),
                "band_size": len(members),
                "price_ratio": round(ratio, 4),
            }
    return flags
