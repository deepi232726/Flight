# ==========================================================
# FlightMate OTP Service
# File : otp_service.py
# ==========================================================

import random
from datetime import datetime, timedelta


# ==========================================================
# LOGIN OTP
# ==========================================================

def generate_login_otp():

    otp = random.randint(100000, 999999)

    expiry = datetime.now() + timedelta(minutes=5)

    return {

        "otp": otp,

        "expires": expiry.strftime("%H:%M:%S"),

        "purpose": "Login"

    }


# ==========================================================
# RIDE OTP
# ==========================================================

def generate_ride_otp():

    otp = random.randint(1000, 9999)

    expiry = datetime.now() + timedelta(minutes=30)

    return {

        "otp": otp,

        "expires": expiry.strftime("%H:%M:%S"),

        "purpose": "Ride Start"

    }


# ==========================================================
# REGISTRATION OTP
# ==========================================================

def generate_registration_otp():

    otp = random.randint(100000, 999999)

    expiry = datetime.now() + timedelta(minutes=10)

    return {

        "otp": otp,

        "expires": expiry.strftime("%H:%M:%S"),

        "purpose": "Registration"

    }


# ==========================================================
# EMERGENCY OTP
# ==========================================================

def generate_emergency_otp():

    otp = random.randint(100000, 999999)

    expiry = datetime.now() + timedelta(minutes=2)

    return {

        "otp": otp,

        "expires": expiry.strftime("%H:%M:%S"),

        "purpose": "Emergency"

    }


# ==========================================================
# VERIFY OTP
# ==========================================================

def verify_otp(user_otp, actual_otp):

    if str(user_otp) == str(actual_otp):

        return {

            "verified": True,

            "message": "OTP Verified Successfully"

        }

    return {

        "verified": False,

        "message": "Incorrect OTP"

    }


# ==========================================================
# SEND OTP (DEMO)
# ==========================================================

def send_otp(phone, otp):

    return {

        "status": "Success",

        "phone": phone,

        "otp": otp,

        "message": "OTP Sent Successfully"

    }


# ==========================================================
# RESEND OTP
# ==========================================================

def resend_otp(phone):

    new_otp = generate_login_otp()

    return {

        "status": "Resent",

        "phone": phone,

        "otp": new_otp["otp"],

        "expires": new_otp["expires"]

    }


# ==========================================================
# OTP STATUS
# ==========================================================

def otp_status():

    return {

        "status": "Active",

        "validity": "5 Minutes"

    }