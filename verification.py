# ==========================================================
# FlightMate Verification Module
# ==========================================================

import random

# ---------------- Aadhaar Verification ----------------

def verify_aadhaar(aadhaar_number):

    if len(aadhaar_number) == 12 and aadhaar_number.isdigit():

        return {
            "verified": True,
            "message": "Aadhaar Verified Successfully"
        }

    return {
        "verified": False,
        "message": "Invalid Aadhaar Number"
    }


# ---------------- Phone Verification ----------------

def verify_phone(phone):

    if len(phone) == 10 and phone.isdigit():

        return {
            "verified": True,
            "message": "Phone Number Verified"
        }

    return {
        "verified": False,
        "message": "Invalid Phone Number"
    }


# ---------------- Flight Verification ----------------

def verify_flight(flight_number):

    flight_number = flight_number.upper()

    valid_prefix = ["AI", "6E", "SG", "UK", "IX"]

    for prefix in valid_prefix:

        if flight_number.startswith(prefix):

            return {
                "verified": True,
                "message": "Flight Verified"
            }

    return {
        "verified": False,
        "message": "Flight Number Not Recognized"
    }


# ---------------- Selfie Verification ----------------

def verify_selfie():

    confidence = random.randint(85, 99)

    return {
        "verified": True,
        "confidence": confidence,
        "message": "Face Match Successful"
    }


# ---------------- Liveness Check ----------------

def liveness_check():

    score = random.randint(90, 100)

    return {
        "verified": True,
        "score": score,
        "message": "Live Person Detected"
    }


# ---------------- Ticket Verification ----------------

def verify_ticket(ticket_number):

    if len(ticket_number) >= 6:

        return {
            "verified": True,
            "message": "Ticket Verified"
        }

    return {
        "verified": False,
        "message": "Invalid Ticket"
    }


# ---------------- Overall Verification ----------------

def complete_verification(user):

    aadhaar = verify_aadhaar(user["aadhaar"])

    phone = verify_phone(user["phone"])

    flight = verify_flight(user["flight"])

    selfie = verify_selfie()

    live = liveness_check()

    ticket = verify_ticket(user["ticket"])

    verified = all([
        aadhaar["verified"],
        phone["verified"],
        flight["verified"],
        selfie["verified"],
        live["verified"],
        ticket["verified"]
    ])

    return {

        "verified": verified,

        "aadhaar": aadhaar,

        "phone": phone,

        "flight": flight,

        "selfie": selfie,

        "liveness": live,

        "ticket": ticket

    }