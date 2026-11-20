
# ==========================================================
# FlightMate Safety Engine
# ==========================================================

import random
from datetime import datetime


# ==========================================================
# TRUST SCORE
# ==========================================================

def calculate_trust_score(rider):

    score = 0

    # ID Verification
    if rider.get("verified", False):
        score += 30

    # Phone Verification
    if rider.get("phone_verified", False):
        score += 20

    # Rating
    rating = rider.get("rating", 0)

    if rating >= 4.8:
        score += 25

    elif rating >= 4.5:
        score += 20

    elif rating >= 4:
        score += 10

    # Previous Rides
    rides = rider.get("rides", 0)

    if rides >= 50:
        score += 25

    elif rides >= 20:
        score += 20

    elif rides >= 10:
        score += 10

    return min(score, 100)


# ==========================================================
# RISK SCORE
# ==========================================================

def calculate_risk_score(rider):

    risk = 0

    if not rider.get("verified", False):
        risk += 40

    if not rider.get("phone_verified", False):
        risk += 20

    if rider.get("rating", 5) < 4:
        risk += 20

    if rider.get("reports", 0) >= 3:
        risk += 40

    if rider.get("failed_login", 0) >= 5:
        risk += 20

    return min(risk, 100)


# ==========================================================
# SAFE RIDER CHECK
# ==========================================================

def is_safe_rider(rider):

    trust = calculate_trust_score(rider)

    risk = calculate_risk_score(rider)

    return trust >= 70 and risk < 50


# ==========================================================
# RIDE OTP
# ==========================================================

def generate_ride_otp():

    return random.randint(1000, 9999)


# ==========================================================
# LOGIN OTP
# ==========================================================

def generate_login_otp():

    return random.randint(100000, 999999)


# ==========================================================
# ROUTE DEVIATION
# ==========================================================

def detect_route_deviation(expected_km, actual_km):

    difference = actual_km - expected_km

    return difference > 5


# ==========================================================
# FAKE GPS DETECTION
# ==========================================================

def detect_fake_gps(speed):

    return speed > 250


# ==========================================================
# SOS
# ==========================================================

def send_sos(user_name, location):

    return {

        "status": "Emergency",

        "user": user_name,

        "location": location,

        "message": "SOS Sent Successfully"

    }


# ==========================================================
# LIVE TRACKING
# ==========================================================

def live_tracking():

    return {

        "latitude": 11.0168,

        "longitude": 76.9558,

        "status": "Tracking Enabled"

    }


# ==========================================================
# DRIVER VERIFICATION
# ==========================================================

def verify_driver(driver):

    return driver.get(
        "verified",
        False
    )


# ==========================================================
# ACCOUNT STATUS
# ==========================================================

def account_status(rider):

    risk = calculate_risk_score(rider)

    if risk >= 70:

        return "Blocked"

    elif risk >= 40:

        return "Manual Verification"

    return "Verified"


# ==========================================================
# REPORT USER
# ==========================================================

def report_user(rider):

    rider["reports"] = rider.get(
        "reports",
        0
    ) + 1

    return rider["reports"]


# ==========================================================
# EMERGENCY CONTACTS
# ==========================================================

def emergency_contacts():

    return [

        {
            "name": "Mother",
            "phone": "+91 9876543210"
        },

        {
            "name": "Father",
            "phone": "+91 9876543211"
        }

    ]


# ==========================================================
# SAFETY DASHBOARD
# ==========================================================

def safety_dashboard(rider):

    return {

        "trust_score":
            calculate_trust_score(rider),

        "risk_score":
            calculate_risk_score(rider),

        "status":
            account_status(rider),

        "ride_otp":
            generate_ride_otp(),

        "tracking":
            live_tracking(),

        "contacts":
            emergency_contacts(),

        "time":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

    }