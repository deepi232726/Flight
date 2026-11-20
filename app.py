# ==========================================================
# FLIGHTMATE - SMART AIRPORT RIDE SHARING
# FINAL APP.PY - PART 1
# ==========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    jsonify
)

from datetime import datetime
import math


# ==========================================================
# EXISTING FLIGHTMATE MODULES
# ==========================================================

from safety_engine import (
    calculate_trust_score,
    calculate_risk_score,
    is_safe_rider,
    generate_ride_otp as safety_generate_ride_otp,
    send_sos,
    live_tracking,
    verify_driver,
    account_status,
    emergency_contacts
)

from verification import (
    verify_aadhaar,
    verify_phone,
    verify_flight,
    verify_ticket
)

from otp_service import (
    generate_login_otp,
    generate_ride_otp,
    generate_registration_otp,
    generate_emergency_otp,
    verify_otp,
    send_otp,
    resend_otp
)

from gps_tracker import (
    get_live_location,
    driver_location,
    calculate_distance,
    route_deviation,
    detect_fake_gps,
    tracking_status,
    emergency_location,
    simulate_driver
)

from ai_engine import (
    trust_score,
    risk_score,
    is_safe_user,
    match_score,
    suspicious_account,
    recommend_rider,
    ai_decision,
    safety_report
)


# ==========================================================
# FLASK APPLICATION
# ==========================================================

app = Flask(__name__)

app.secret_key = "flightmate_pro_2026"


# ==========================================================
# DEMO USERS
# ==========================================================

users = {

    "deepika@gmail.com": {

        "password": "123456",

        "name": "Deepika",

        "phone": "9876543210",

        "rides": 10,

        "saved": 3600,

        "rating": 4.9,

        "verified": True,

        "phone_verified": True,

        "reports": 0,

        "failed_login": 0,

        "gender": "Female"

    }

}


# ==========================================================
# DEMO CO-RIDERS
# ==========================================================

all_riders = [

    {
        "name": "Revathi",

        "gender": "Female",

        "pickup": "Gandhipuram",

        "distance": 6,

        "verified": True,

        "phone_verified": True,

        "rating": 4.9,

        "rides": 32,

        "reports": 0,

        "failed_login": 0,

        "aadhaar_verified": True,

        "phone_identity_verified": True,

        "flight_verified": True,

        "ticket_verified": True

    },

    {
        "name": "Prabhu",

        "gender": "Male",

        "pickup": "Singanallur",

        "distance": 8,

        "verified": True,

        "phone_verified": True,

        "rating": 4.7,

        "rides": 25,

        "reports": 0,

        "failed_login": 0,

        "aadhaar_verified": True,

        "phone_identity_verified": True,

        "flight_verified": True,

        "ticket_verified": True

    },

    {
        "name": "Madhanika",

        "gender": "Female",

        "pickup": "Peelamedu",

        "distance": 5,

        "verified": True,

        "phone_verified": True,

        "rating": 4.8,

        "rides": 18,

        "reports": 0,

        "failed_login": 0,

        "aadhaar_verified": True,

        "phone_identity_verified": True,

        "flight_verified": True,

        "ticket_verified": True

    }

]


# ==========================================================
# VERIFIED DRIVER DATABASE
# ==========================================================

drivers = [

    {
        "name": "Suresh Kumar",

        "vehicle": "Toyota Innova",

        "number": "TN37 AB 2025",

        "phone": "9876543212",

        "verified": True,

        "phone_verified": True,

        "license_verified": True,

        "vehicle_verified": True,

        "rating": 4.9,

        "rides": 148,

        "reports": 0,

        "failed_login": 0

    }

]


# ==========================================================
# TRUSTED CONTACTS
# ==========================================================

TRUSTED_CONTACTS = [

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
# POLICE / EMERGENCY AUTHORITY
# ==========================================================

EMERGENCY_AUTHORITY = {

    "name": "Emergency Response",

    "number": "112",

    "status": "Ready"

}


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    ride_booked = session.get(
        "ride_booked",
        False
    )

    flight_data = {

        "name": session.get(
            "name",
            "Deepika"
        ),

        "flight": session.get(
            "flight"
        ),

        "airport": session.get(
            "airport"
        ),

        "pickup": session.get(
            "pickup"
        ),

        "time": session.get(
            "time"
        ),

        "duration": session.get(
            "duration"
        ),

        "gender": session.get(
            "gender"
        ),

        "status": "On Time"

    }

    return render_template(

        "home.html",

        flight=flight_data,

        ride_booked=ride_booked

    )


# ==========================================================
# LOGIN
# ==========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if (

            email in users

            and

            users[email]["password"] == password

        ):

            user = users[email]

            session["email"] = email

            session["name"] = user["name"]

            session["gender"] = user.get(
                "gender",
                "Any"
            )

            session["logged_in"] = True

            session["failed_login"] = 0

            return redirect("/")

        if email in users:

            users[email]["failed_login"] = (
                users[email].get(
                    "failed_login",
                    0
                ) + 1
            )

        return render_template(

            "login.html",

            error="Invalid Credentials"

        )

    return render_template(
        "login.html"
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ==========================================================
# BOOK RIDE
# ==========================================================

@app.route(
    "/book",
    methods=["GET", "POST"]
)
def book():

    if request.method == "POST":

        session["name"] = request.form.get(
            "name",
            session.get(
                "name",
                "Deepika"
            )
        )

        session["flight"] = request.form.get(
            "flight",
            ""
        )

        session["airport"] = request.form.get(
            "airport",
            ""
        )

        session["pickup"] = request.form.get(
            "pickup",
            ""
        )

        session["time"] = request.form.get(
            "time",
            ""
        )

        session["duration"] = request.form.get(
            "duration",
            ""
        )

        session["gender"] = request.form.get(
            "gender",
            "Any"
        )

        session["preference"] = request.form.get(
            "preference",
            "Shared Ride"
        )

        session["gender_preference"] = request.form.get(
            "gender_preference",
            "Any"
        )

        session["women_safe"] = (

            request.form.get(
                "women_safe",
                "off"
            )

            in

            ["on", "true", "yes", "1"]

        )

        session["eco"] = request.form.get(
            "eco",
            "No"
        )

        # --------------------------------------------------
        # WOMEN SAFE MODE
        # --------------------------------------------------

        if (

            session["gender"] == "Female"

            and

            session["women_safe"]

        ):

            session["gender_preference"] = (
                "Female Only"
            )

        return redirect("/matches")

    return render_template(
        "book.html"
    )


# ==========================================================
# MATCHES
# ==========================================================

@app.route("/matches")
def matches():

    preference = session.get(
        "preference",
        "Shared Ride"
    )

    gender_preference = session.get(
        "gender_preference",
        "Any"
    )

    user_gender = session.get(
        "gender",
        "Any"
    )

    women_safe = session.get(
        "women_safe",
        False
    )

    # ------------------------------------------------------
    # CURRENT USER PROFILE FOR AI
    # ------------------------------------------------------

    current_user = {

        "name": session.get(
            "name",
            "Deepika"
        ),

        "gender": user_gender,

        "pickup": session.get(
            "pickup",
            ""
        ),

        "distance": 5,

        "verified": True,

        "phone_verified": True,

        "rating": 4.9,

        "rides": 10,

        "reports": 0,

        "failed_login": 0

    }

    # ------------------------------------------------------
    # PRIVATE RIDE
    # ------------------------------------------------------

    if preference == "Private Ride":

        riders = []

        return render_template(

            "matches.html",

            riders=riders,

            private=True,

            women_safe=women_safe

        )

    riders = []

    # ======================================================
    # FILTER + AI MATCHING
    # ======================================================

    for original_rider in all_riders:

        # Create copy so original demo data is not modified
        rider = dict(original_rider)

        # --------------------------------------------------
        # GENDER FILTER
        # --------------------------------------------------

        if gender_preference == "Female Only":

            if rider["gender"] != "Female":

                continue

        elif gender_preference == "Male Only":

            if rider["gender"] != "Male":

                continue

        # --------------------------------------------------
        # WOMEN SAFE MODE
        # --------------------------------------------------

        if women_safe:

            if rider["gender"] != "Female":

                continue

        # --------------------------------------------------
        # AI SAFETY CHECK
        # --------------------------------------------------

        if not is_safe_user(rider):

            continue

        # --------------------------------------------------
        # TRUST SCORE
        # --------------------------------------------------

        rider["trust_score"] = trust_score(
            rider
        )

        # --------------------------------------------------
        # RISK SCORE
        # --------------------------------------------------

        rider["risk_score"] = risk_score(
            rider
        )

        # --------------------------------------------------
        # ACCOUNT STATUS
        # --------------------------------------------------

        rider["status"] = account_status(
            rider
        )

        # --------------------------------------------------
        # AI MATCH SCORE
        # --------------------------------------------------

        rider["match_score"] = match_score(

            current_user,

            rider

        )

        # --------------------------------------------------
        # SAFETY STATUS
        # --------------------------------------------------

        if rider["risk_score"] < 30:

            rider["safety_status"] = "Low Risk"

        elif rider["risk_score"] < 60:

            rider["safety_status"] = "Medium Risk"

        else:

            rider["safety_status"] = "High Risk"

        # --------------------------------------------------
        # COST SHARE
        # --------------------------------------------------

        rider["share"] = 200

        riders.append(rider)

    # ------------------------------------------------------
    # SORT BY AI MATCH SCORE
    # ------------------------------------------------------

    riders.sort(

        key=lambda x: x.get(
            "match_score",
            0
        ),

        reverse=True

    )

    return render_template(

        "matches.html",

        riders=riders,

        private=False,

        women_safe=women_safe

    )


# ==========================================================
# CONFIRM RIDE
# ==========================================================

@app.route("/confirm")
def confirm():

    selected = request.args.getlist(
        "rider"
    )

    selected_riders = []

    for rider in all_riders:

        if rider["name"] in selected:

            selected_riders.append(
                dict(rider)
            )

    passengers = (
        len(selected_riders) + 1
    )

    total_cost = 600

    your_share = math.ceil(
        total_cost / passengers
    )

    savings = (
        total_cost - your_share
    )

    # ------------------------------------------------------
    # VERIFIED DRIVER
    # ------------------------------------------------------

    driver = drivers[0]

    driver["trust_score"] = trust_score(
        driver
    )

    driver["risk_score"] = risk_score(
        driver
    )

    driver["verification_status"] = (

        "Verified Driver"

        if verify_driver(driver)

        else

        "Verification Required"

    )

    # ------------------------------------------------------
    # RIDE OTP
    # ------------------------------------------------------

    ride_otp_data = generate_ride_otp()

    session["ride_otp"] = str(
        ride_otp_data["otp"]
    )

    session["ride_otp_expiry"] = (
        ride_otp_data["expires"]
    )

    session["ride_verified"] = False

    session["ride_booked"] = True

    session["passengers"] = passengers

    session["selected_riders"] = [
        r["name"]
        for r in selected_riders
    ]

    return render_template(

        "confirm.html",

        selected_riders=selected_riders,

        total_cost=total_cost,

        your_share=your_share,

        savings=savings,

        driver=driver,

        ride_otp=ride_otp_data

    )


# ==========================================================
# RIDE OTP VERIFICATION
# ==========================================================

@app.route(
    "/verify-ride-otp",
    methods=["POST"]
)
def verify_ride_otp():

    user_otp = request.form.get(
        "otp",
        ""
    )

    actual_otp = session.get(
        "ride_otp",
        ""
    )

    result = verify_otp(
        user_otp,
        actual_otp
    )

    if result["verified"]:

        session["ride_verified"] = True

        return jsonify({

            "success": True,

            "message":
            "Ride OTP Verified Successfully"

        })

    return jsonify({

        "success": False,

        "message":
        "Incorrect Ride OTP"

    })


# ==========================================================
# SUCCESS
# ==========================================================

@app.route("/success")
def success():

    return render_template(
        "success.html"
    )
# ==========================================================
# FLIGHTMATE - FINAL APP.PY
# PART 2
# ==========================================================


# ==========================================================
# ECO / CARBON SAVING DASHBOARD
# ==========================================================

@app.route("/eco")
def eco():

    passengers = session.get(
        "passengers",
        1
    )

    # Number of passengers sharing the ride
    shared_passengers = max(
        passengers - 1,
        0
    )

    # Demo environmental calculation
    co2_saved = round(
        shared_passengers * 1.2,
        2
    )

    fuel_saved = round(
        shared_passengers * 0.5,
        2
    )

    trees_equivalent = round(
        co2_saved * 7,
        2
    )

    eco_data = {

        "co2": str(
            co2_saved
        ) + " kg",

        "trees": trees_equivalent,

        "fuel": str(
            fuel_saved
        ) + " L",

        "emission":
        str(passengers) + "x",

        "passengers":
        passengers,

        "message":
        "Shared rides help reduce fuel usage and carbon emissions."

    }

    return render_template(

        "eco.html",

        eco=eco_data

    )


# ==========================================================
# LIVE GPS TRACKER
# ==========================================================

@app.route("/tracker")
def tracker():

    user_location = get_live_location()

    driver = driver_location()

    tracking = tracking_status()

    ride = {

        "driver":
        driver.get(
            "driver",
            "Suresh Kumar"
        ),

        "vehicle":
        "Toyota Innova",

        "vehicle_no":
        "TN37 AB 2025",

        "eta":
        driver.get(
            "eta",
            "8 Minutes"
        ),

        "status":
        "Driver Arriving",

        "location":
        driver.get(
            "distance",
            "2.5 km"
        ),

        "latitude":
        user_location.get(
            "latitude"
        ),

        "longitude":
        user_location.get(
            "longitude"
        ),

        "tracking":
        tracking.get(
            "tracking",
            True
        ),

        "last_updated":
        tracking.get(
            "last_updated"
        )

    }

    return render_template(

        "tracker.html",

        ride=ride

    )


# ==========================================================
# GPS API
# ==========================================================

@app.route("/api/location")
def api_location():

    location = get_live_location()

    return jsonify({

        "success": True,

        "latitude":
        location["latitude"],

        "longitude":
        location["longitude"],

        "city":
        location.get(
            "city",
            "Coimbatore"
        ),

        "status":
        "Live Tracking Enabled",

        "updated":
        datetime.now().strftime(
            "%H:%M:%S"
        )

    })


# ==========================================================
# DRIVER LIVE LOCATION API
# ==========================================================

@app.route("/api/driver-location")
def api_driver_location():

    location = driver_location()

    return jsonify({

        "success": True,

        "driver":
        location.get(
            "driver",
            "Suresh Kumar"
        ),

        "latitude":
        location.get(
            "latitude"
        ),

        "longitude":
        location.get(
            "longitude"
        ),

        "distance":
        location.get(
            "distance",
            "2.5 km"
        ),

        "eta":
        location.get(
            "eta",
            "8 Minutes"
        ),

        "status":
        "Driver Arriving"

    })


# ==========================================================
# SAFETY DASHBOARD
# ==========================================================

@app.route("/safety")
def safety():

    email = session.get(
        "email",
        "deepika@gmail.com"
    )

    user = users.get(
        email,
        users["deepika@gmail.com"]
    )

    report = safety_report(
        user
    )

    # ------------------------------------------------------
    # ADD EXTRA SECURITY INFORMATION
    # ------------------------------------------------------

    report["phone_verified"] = user.get(
        "phone_verified",
        False
    )

    report["identity_verified"] = user.get(
        "verified",
        False
    )

    report["failed_logins"] = user.get(
        "failed_login",
        0
    )

    report["reports"] = user.get(
        "reports",
        0
    )

    report["safety_level"] = (

        "HIGH"

        if report["trust_score"] >= 80
        and report["risk_score"] < 30

        else

        "MEDIUM"

        if report["trust_score"] >= 60
        and report["risk_score"] < 60

        else

        "LOW"

    )

    return render_template(

        "safety.html",

        trusted=TRUSTED_CONTACTS,

        report=report

    )


# ==========================================================
# SOS PAGE + SOS ACTIVATION
# ==========================================================

@app.route(
    "/sos",
    methods=["GET", "POST"]
)
def sos():

    user_name = session.get(
        "name",
        "Deepika"
    )

    # ------------------------------------------------------
    # GET CURRENT LOCATION
    # ------------------------------------------------------

    location = get_live_location()

    # ------------------------------------------------------
    # POST = ACTIVATE SOS
    # ------------------------------------------------------

    if request.method == "POST":

        # Browser GPS values
        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )

        # If browser did not send GPS,
        # use demo location
        if not latitude:

            latitude = location.get(
                "latitude"
            )

        if not longitude:

            longitude = location.get(
                "longitude"
            )

        emergency_location_data = {

            "latitude":
            latitude,

            "longitude":
            longitude,

            "city":
            "Coimbatore",

            "status":
            "Emergency Location Captured"

        }

        # --------------------------------------------------
        # SAVE SOS STATE
        # --------------------------------------------------

        session["sos_active"] = True

        session["sos_time"] = (
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        )

        session["sos_location"] = (
            emergency_location_data
        )

        # --------------------------------------------------
        # SOS SERVICE
        # --------------------------------------------------

        sos_result = send_sos(

            user_name,

            emergency_location_data

        )

        # --------------------------------------------------
        # POLICE / EMERGENCY AUTHORITY
        # --------------------------------------------------

        police_notification = {

            "authority":
            EMERGENCY_AUTHORITY["name"],

            "number":
            EMERGENCY_AUTHORITY["number"],

            "status":
            "Emergency Alert Prepared",

            "location_shared":
            True,

            "time":
            session["sos_time"]

        }

        # --------------------------------------------------
        # TRUSTED CONTACT NOTIFICATION
        # --------------------------------------------------

        contact_notifications = []

        for contact in TRUSTED_CONTACTS:

            contact_notifications.append({

                "name":
                contact["name"],

                "phone":
                contact["phone"],

                "status":
                "Emergency Message Prepared",

                "location_shared":
                True

            })

        # --------------------------------------------------
        # EMERGENCY OTP
        # --------------------------------------------------

        emergency_otp = (
            generate_emergency_otp()
        )

        session["emergency_otp"] = str(
            emergency_otp["otp"]
        )

        return jsonify({

            "success": True,

            "message":
            "SOS Activated Successfully",

            "user":
            user_name,

            "location":
            emergency_location_data,

            "police":
            police_notification,

            "trusted_contacts":
            contact_notifications,

            "otp":
            emergency_otp["otp"],

            "sos":
            sos_result,

            "time":
            session["sos_time"]

        })

    # ------------------------------------------------------
    # NORMAL SOS PAGE
    # ------------------------------------------------------

    return render_template(

        "sos.html",

        user_name=user_name,

        location=location,

        trusted_contacts=TRUSTED_CONTACTS,

        police_station=EMERGENCY_AUTHORITY

    )


# ==========================================================
# SOS STATUS
# ==========================================================

@app.route("/sos/status")
def sos_status():

    return jsonify({

        "active":
        session.get(
            "sos_active",
            False
        ),

        "location":
        session.get(
            "sos_location",
            None
        ),

        "time":
        session.get(
            "sos_time",
            None
        ),

        "audio_recording":
        session.get(
            "audio_recording",
            False
        )

    })


# ==========================================================
# EMERGENCY AUDIO START
# ==========================================================

@app.route(
    "/sos/audio/start",
    methods=["POST"]
)
def sos_audio_start():

    session["audio_recording"] = True

    return jsonify({

        "success": True,

        "recording": True,

        "message":
        "Emergency audio recording started"

    })


# ==========================================================
# EMERGENCY AUDIO STOP
# ==========================================================

@app.route(
    "/sos/audio/stop",
    methods=["POST"]
)
def sos_audio_stop():

    session["audio_recording"] = False

    return jsonify({

        "success": True,

        "recording": False,

        "message":
        "Emergency audio recording stopped"

    })


# ==========================================================
# EMERGENCY OTP
# ==========================================================

@app.route(
    "/sos/verify-otp",
    methods=["POST"]
)
def verify_emergency_otp():

    user_otp = request.form.get(
        "otp",
        ""
    )

    actual_otp = session.get(
        "emergency_otp",
        ""
    )

    result = verify_otp(

        user_otp,

        actual_otp

    )

    return jsonify(result)


# ==========================================================
# STOP SOS
# ==========================================================

@app.route(
    "/sos/stop",
    methods=["POST"]
)
def stop_sos():

    session["sos_active"] = False

    session["audio_recording"] = False

    return jsonify({

        "success": True,

        "message":
        "Emergency mode closed"

    })


# ==========================================================
# DRIVER VERIFICATION PAGE / API
# ==========================================================

@app.route("/driver-verification")
def driver_verification():

    driver = dict(
        drivers[0]
    )

    driver["trust_score"] = trust_score(
        driver
    )

    driver["risk_score"] = risk_score(
        driver
    )

    driver["verified_driver"] = (
        verify_driver(driver)
    )

    return jsonify({

        "driver":
        driver,

        "verification": {

            "identity":
            True,

            "phone":
            driver["phone_verified"],

            "license":
            driver["license_verified"],

            "vehicle":
            driver["vehicle_verified"]

        }

    })


# ==========================================================
# USER VERIFICATION
# ==========================================================

@app.route(
    "/verify-user",
    methods=["GET", "POST"]
)
def verify_user():

    if request.method == "POST":

        aadhaar = request.form.get(
            "aadhaar",
            ""
        )

        phone = request.form.get(
            "phone",
            ""
        )

        flight = request.form.get(
            "flight",
            ""
        )

        ticket = request.form.get(
            "ticket",
            ""
        )

        aadhaar_result = verify_aadhaar(
            aadhaar
        )

        phone_result = verify_phone(
            phone
        )

        flight_result = verify_flight(
            flight
        )

        ticket_result = verify_ticket(
            ticket
        )

        overall = all([

            aadhaar_result["verified"],

            phone_result["verified"],

            flight_result["verified"],

            ticket_result["verified"]

        ])

        return jsonify({

            "verified":
            overall,

            "aadhaar":
            aadhaar_result,

            "phone":
            phone_result,

            "flight":
            flight_result,

            "ticket":
            ticket_result

        })

    return jsonify({

        "message":
        "User Verification API Ready",

        "methods": [

            "Aadhaar Validation",

            "Phone Verification",

            "Flight Verification",

            "Ticket Verification"

        ]

    })


# ==========================================================
# PROFILE
# ==========================================================

@app.route("/profile")
def profile():

    email = session.get(
        "email",
        "deepika@gmail.com"
    )

    user = users.get(
        email,
        users["deepika@gmail.com"]
    )

    return render_template(

        "profile.html",

        user={

            "name":
            user["name"],

            "email":
            email,

            "rides":
            user["rides"],

            "saved":
            "₹" + str(
                user["saved"]
            ),

            "rating":
            user["rating"],

            "trust_score":
            trust_score(user),

            "risk_score":
            risk_score(user),

            "verified":
            user["verified"],

            "phone_verified":
            user["phone_verified"]

        }

    )


# ==========================================================
# AI MATCH API
# ==========================================================

@app.route("/api/match-score")
def api_match_score():

    rider_name = request.args.get(
        "rider",
        ""
    )

    current_user = {

        "gender":
        session.get(
            "gender",
            "Female"
        ),

        "pickup":
        session.get(
            "pickup",
            ""
        ),

        "distance":
        5,

        "verified":
        True,

        "phone_verified":
        True,

        "rating":
        4.9,

        "rides":
        10,

        "reports":
        0,

        "failed_login":
        0

    }

    for rider in all_riders:

        if rider["name"] == rider_name:

            return jsonify({

                "rider":
                rider["name"],

                "match_score":
                match_score(
                    current_user,
                    rider
                ),

                "trust_score":
                trust_score(rider),

                "risk_score":
                risk_score(rider),

                "status":
                account_status(rider)

            })

    return jsonify({

        "error":
        "Rider not found"

    }), 404


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return jsonify({

        "application":
        "FlightMate",

        "status":
        "Running",

        "version":
        "Final Safety Edition",

        "features": [

            "AI Match Score",

            "Trust Score",

            "Risk Score",

            "Women Safe Mode",

            "Driver Verification",

            "Ride OTP",

            "Live GPS Tracking",

            "Carbon Saving Dashboard",

            "Emergency SOS",

            "Safety Dashboard"

        ]

    })


# ==========================================================
# ERROR HANDLER
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "error":
        "Page Not Found",

        "message":
        "FlightMate route does not exist"

    }), 404


# ==========================================================
# MAIN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )