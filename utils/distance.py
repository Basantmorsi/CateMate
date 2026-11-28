from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371


def distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> int:
    """Great-circle distance in whole kilometres (haversine).

    Owner coordinates are already rounded to about 1 km, so a whole number is
    all the precision there is.
    """
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return round(2 * EARTH_RADIUS_KM * asin(sqrt(a)))
