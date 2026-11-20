# matcher.py

from datetime import datetime
import math

# ---------------- DEMO RIDERS DATABASE ----------------

RIDERS = [

    {
        "name": "Revathi",
        "gender": "Female",
        "pickup": "Gandhipuram",
        "distance": 6,
        "rating": 4.9,
        "verified": True,
        "phone_verified": True
    },

    {
        "name": "Prabhu",
        "gender": "Male",
        "pickup": "Singanallur",
        "distance": 8,
        "rating": 4.7,
        "verified": True,
        "phone_verified": True
    },

    {
        "name": "Madhanika",
        "gender": "Female",
        "pickup": "Peelamedu",
        "distance": 5,
        "rating": 4.8,
        "verified": True,
        "phone_verified": True
    },

    {
        "name": "Keerthana",
        "gender": "Female",
        "pickup": "Saravanampatti",
        "distance": 9,
        "rating": 4.6,
        "verified": True,
        "phone_verified": True
    },

    {
        "name": "Arun",
        "gender": "Male",
        "pickup": "Ukkadam",
        "distance": 7,
        "rating": 4.5,
        "verified": True,
        "phone_verified": True
    }

]


# ---------------- TIME CONVERSION ----------------

def parse_time(t):

    try:
        return datetime.strptime(t, "%H:%M")

    except:

        return datetime.strptime("10:00", "%H:%M")


# ---------------- FIND MATCHES ----------------

def find_matches(user):

    matches = []

    user_time = parse_time(user["time"])

    for rider in RIDERS:

        # -------- GENDER FILTER --------

        if user["gender"] == "Female Only":

            if rider["gender"] != "Female":
                continue

        elif user["gender"] == "Male Only":

            if rider["gender"] != "Male":
                continue

        # -------- PRIVATE RIDE --------

        if user["preference"] == "Private Ride":

            continue

        # -------- TIME MATCH --------

        other_time = parse_time(user["time"])

        diff = abs(
            (user_time - other_time).total_seconds()
            / 60
        )

        if diff <= 30:

            rider["match_score"] = calculate_match_score(
                rider["distance"]
            )

            rider["share"] = 0

            matches.append(rider)

    return matches


# ---------------- MATCH SCORE ----------------

def calculate_match_score(distance):

    if distance <= 3:

        return 98

    elif distance <= 5:

        return 94

    elif distance <= 8:

        return 90

    elif distance <= 12:

        return 85

    return 75


# ---------------- COST ----------------

def calculate_cost(distance):

    base_charge = 150

    per_km_charge = 12

    total = base_charge + (distance * per_km_charge)

    return round(total)


# ---------------- SPLIT COST ----------------

def split_cost(total_cost, passengers):

    if passengers <= 1:

        return total_cost

    return math.ceil(total_cost / passengers)


# ---------------- ESTIMATED SAVINGS ----------------

def estimated_savings(total_cost, share):

    return total_cost - share


# ---------------- ECO IMPACT ----------------

def eco_saved(passengers):

    if passengers <= 1:

        return {

            "co2": 0,

            "trees": 0,

            "fuel": 0

        }

    co2_saved = round((passengers - 1) * 1.2, 2)

    trees_equivalent = round(co2_saved * 7, 2)

    fuel_saved = round(co2_saved * 4, 2)

    return {

        "co2": co2_saved,

        "trees": trees_equivalent,

        "fuel": fuel_saved

    }


# ---------------- DRIVER DETAILS ----------------

def driver_details():

    return {

        "name": "Suresh Kumar",

        "vehicle": "Toyota Innova",

        "vehicle_no": "TN37 AB 2025",

        "eta": "8 Minutes",

        "status": "Driver Arriving"

    }


# ---------------- TRUSTED CONTACTS ----------------

def trusted_contacts():

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


# ---------------- SOS ----------------

def send_sos():

    contacts = trusted_contacts()

    message = {

        "status": "Emergency Alert Sent",

        "message": "Location shared successfully",

        "contacts": contacts

    }

    return message


# ---------------- LIVE LOCATION ----------------

def live_location():

    return {

        "latitude": 11.0168,

        "longitude": 76.9558,

        "status": "Live Tracking Enabled"

    }


# ---------------- AUDIO RECORDING ----------------

def audio_recording():

    return {

        "status": "Recording Active",

        "file": "ride_audio_001.mp3"

    }


# ---------------- VERIFICATION ----------------

def verification():

    return {

        "aadhaar_verified": True,

        "phone_verified": True,

        "ride_safe": True

    }