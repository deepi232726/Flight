# ==========================================================
# FlightMate GPS Tracker
# File : gps_tracker.py
# ==========================================================

import random
import math
from datetime import datetime


# ==========================================================
# LIVE LOCATION
# ==========================================================

def get_live_location():

    return {

        "latitude": 11.0168,

        "longitude": 76.9558,

        "city": "Coimbatore",

        "status": "Tracking Enabled"

    }


# ==========================================================
# DRIVER LOCATION
# ==========================================================

def driver_location():

    return {

        "driver": "Suresh Kumar",

        "latitude": 11.0250,

        "longitude": 76.9600,

        "distance": "2.5 km",

        "eta": "8 Minutes"

    }


# ==========================================================
# DISTANCE CALCULATION
# ==========================================================

def calculate_distance(lat1, lon1, lat2, lon2):

    R = 6371

    dlat = math.radians(lat2 - lat1)

    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


# ==========================================================
# ROUTE DEVIATION
# ==========================================================

def route_deviation(expected_km, actual_km):

    deviation = actual_km - expected_km

    if deviation > 5:

        return {

            "safe": False,

            "message": "Route Deviation Detected"

        }

    return {

        "safe": True,

        "message": "Route Safe"

    }


# ==========================================================
# FAKE GPS DETECTION
# ==========================================================

def detect_fake_gps(speed):

    if speed > 250:

        return {

            "safe": False,

            "message": "Fake GPS Suspected"

        }

    return {

        "safe": True,

        "message": "GPS Verified"

    }


# ==========================================================
# LIVE TRACK STATUS
# ==========================================================

def tracking_status():

    return {

        "tracking": True,

        "last_updated": datetime.now().strftime("%H:%M:%S"),

        "status": "Live"

    }


# ==========================================================
# SOS LOCATION
# ==========================================================

def emergency_location():

    location = get_live_location()

    return {

        "status": "Emergency",

        "latitude": location["latitude"],

        "longitude": location["longitude"],

        "shared": True

    }


# ==========================================================
# RANDOM DRIVER MOVEMENT (Demo)
# ==========================================================

def simulate_driver():

    distance = random.randint(1, 10)

    eta = random.randint(2, 15)

    return {

        "distance": str(distance) + " km",

        "eta": str(eta) + " Minutes"

    }


# ==========================================================
# COMPLETE GPS DASHBOARD
# ==========================================================

def gps_dashboard():

    return {

        "user": get_live_location(),

        "driver": driver_location(),

        "tracking": tracking_status(),

        "emergency": emergency_location()

    }