# ==========================================================
# FlightMate AI Risk & Safety Engine
# ==========================================================

from datetime import datetime


# ==========================================================
# TRUST SCORE
# ==========================================================

def trust_score(user):

    score = 0

    # Identity verification
    if user.get("verified", False):
        score += 25

    # Phone verification
    if user.get("phone_verified", False):
        score += 15

    # Good rating
    rating = float(user.get("rating", 0))

    if rating >= 4.8:
        score += 25
    elif rating >= 4.5:
        score += 20
    elif rating >= 4.0:
        score += 10

    # Ride history
    rides = int(user.get("rides", 0))

    if rides >= 50:
        score += 25
    elif rides >= 20:
        score += 20
    elif rides >= 10:
        score += 10
    elif rides > 0:
        score += 5

    # Driver verification
    if user.get("driver_verified", False):
        score += 10

    return min(score, 100)


# ==========================================================
# RISK SCORE
# ==========================================================

def risk_score(user):

    risk = 0

    # Identity not verified
    if not user.get("verified", False):
        risk += 25

    # Phone not verified
    if not user.get("phone_verified", False):
        risk += 15

    # Low rating
    rating = float(user.get("rating", 5))

    if rating < 3:
        risk += 30
    elif rating < 4:
        risk += 15

    # Complaints / reports
    reports = int(user.get("reports", 0))

    if reports >= 5:
        risk += 35
    elif reports >= 3:
        risk += 25
    elif reports >= 1:
        risk += 10

    # Suspicious login activity
    failed_login = int(user.get("failed_login", 0))

    if failed_login >= 10:
        risk += 30
    elif failed_login >= 5:
        risk += 20

    # Driver verification
    if user.get("is_driver", False):

        if not user.get("driver_verified", False):
            risk += 25

    # Previous safety flag
    if user.get("safety_flag", False):
        risk += 30

    return min(risk, 100)


# ==========================================================
# RISK LEVEL
# ==========================================================

def risk_level(user):

    risk = risk_score(user)

    if risk >= 70:
        return "HIGH"

    elif risk >= 40:
        return "MEDIUM"

    return "LOW"


# ==========================================================
# SAFE USER CHECK
# ==========================================================

def is_safe_user(user):

    trust = trust_score(user)
    risk = risk_score(user)

    return trust >= 60 and risk < 40


# ==========================================================
# ACCOUNT STATUS
# ==========================================================

def account_status(user):

    risk = risk_score(user)

    if risk >= 70:
        return "Blocked / Safety Review"

    elif risk >= 40:
        return "Additional Verification Required"

    elif trust_score(user) >= 60:
        return "Verified"

    return "Needs Verification"


# ==========================================================
# AI DECISION
# ==========================================================

def ai_decision(user):

    trust = trust_score(user)
    risk = risk_score(user)

    if risk >= 70:
        return "Ride Blocked"

    elif risk >= 40:
        return "Additional Verification Required"

    elif trust >= 75 and risk < 30:
        return "Ride Approved"

    elif trust >= 60:
        return "Ride Approved with Monitoring"

    return "Verification Required"


# ==========================================================
# MATCH SCORE
# ==========================================================

def match_score(user, rider):

    score = 0

    # Pickup similarity
    if user.get("pickup") == rider.get("pickup"):
        score += 25

    # Gender preference
    preference = user.get("gender", "Any")

    if preference == "Any":
        score += 20

    elif preference == rider.get("gender"):
        score += 20

    # Distance similarity
    user_distance = float(user.get("distance", 0))
    rider_distance = float(rider.get("distance", 0))

    if abs(user_distance - rider_distance) <= 2:
        score += 25

    elif abs(user_distance - rider_distance) <= 5:
        score += 15

    # Rating
    rating = float(rider.get("rating", 0))

    if rating >= 4.8:
        score += 20

    elif rating >= 4.5:
        score += 15

    elif rating >= 4:
        score += 10

    # Safety
    if is_safe_user(rider):
        score += 10

    return min(score, 100)


# ==========================================================
# RIDER RECOMMENDATION
# ==========================================================

def recommend_rider(user, riders):

    safe_riders = []

    for rider in riders:

        if is_safe_user(rider):

            rider_copy = rider.copy()

            rider_copy["match_score"] = match_score(
                user,
                rider_copy
            )

            rider_copy["trust_score"] = trust_score(
                rider_copy
            )

            rider_copy["risk_score"] = risk_score(
                rider_copy
            )

            rider_copy["risk_level"] = risk_level(
                rider_copy
            )

            rider_copy["account_status"] = account_status(
                rider_copy
            )

            safe_riders.append(rider_copy)

    safe_riders.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return safe_riders


# ==========================================================
# SAFETY REPORT
# ==========================================================

def safety_report(user):

    trust = trust_score(user)
    risk = risk_score(user)

    return {

        "trust_score": trust,

        "risk_score": risk,

        "risk_level": risk_level(user),

        "status": account_status(user),

        "decision": ai_decision(user),

        "generated_at":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

    }
# ==========================================================
# COMPATIBILITY FUNCTIONS
# ==========================================================

def TrustScore(user):
    return trust_score(user)


def RiskScore(user):
    return risk_score(user)


def MatchScore(user, rider):
    return match_score(user, rider)
# ==========================================================
# COMPATIBILITY FUNCTION
# ==========================================================

def suspicious_account(user):

    return risk_score(user) >= 60