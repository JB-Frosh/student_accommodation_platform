import math

EARTH_RADIUS_KM = 6371.0088


def haversine_distance_km(lat1, lng1, lat2, lng2):
    """Straight-line great-circle distance in km between two lat/lng points."""
    lat1, lng1, lat2, lng2 = map(math.radians, (lat1, lng1, lat2, lng2))
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))