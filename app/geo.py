"""
Lightweight geolocation utilities.
Uses a bundled zip code dataset for coordinate lookup and Haversine for distance.
"""

import csv
import math
import os

_ZIP_DATA = {}


def _load_zip_data():
    """Load zip code coordinates from bundled CSV."""
    global _ZIP_DATA
    if _ZIP_DATA:
        return

    csv_path = os.path.join(os.path.dirname(__file__), "data", "zipcodes.csv")
    if not os.path.exists(csv_path):
        return

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                _ZIP_DATA[row["zip"]] = (float(row["lat"]), float(row["lng"]))
            except (ValueError, KeyError):
                continue


def get_coordinates(zip_code):
    """Return (latitude, longitude) for a US zip code, or None."""
    _load_zip_data()
    return _ZIP_DATA.get(zip_code.strip())


def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculate distance in miles between two lat/lon points."""
    R = 3958.8  # Earth radius in miles

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def find_colleges_nearby(colleges, zip_code, radius_miles=50):
    """Filter and sort colleges by distance from a zip code.

    Args:
        colleges: list of CollegeProfile objects
        zip_code: patient's zip code
        radius_miles: max distance

    Returns:
        list of (college, distance_miles) tuples, sorted by distance
    """
    origin = get_coordinates(zip_code)
    if not origin:
        # If we can't geocode, return all colleges with unknown distance
        return [(c, None) for c in colleges]

    results = []
    for college in colleges:
        if college.latitude and college.longitude:
            dist = haversine_miles(origin[0], origin[1], college.latitude, college.longitude)
            if dist <= radius_miles:
                results.append((college, round(dist, 1)))
        else:
            # College without coordinates — try to geocode from their zip
            coords = get_coordinates(college.zip_code)
            if coords:
                dist = haversine_miles(origin[0], origin[1], coords[0], coords[1])
                if dist <= radius_miles:
                    results.append((college, round(dist, 1)))

    results.sort(key=lambda x: x[1] if x[1] is not None else 9999)
    return results
