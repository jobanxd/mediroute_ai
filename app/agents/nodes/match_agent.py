"""Match agent node — filters and ranks hospitals by insurance, capability, and distance."""
import logging
import json
from math import radians, sin, cos, sqrt, atan2

from langchain_core.messages import AIMessage

from app.agents.state import AgentState
from app.data.hospitals import HOSPITALS, EMERGENCY_CAPABILITY_MAP

logger = logging.getLogger(__name__)


# ── Haversine Distance ────────────────────────────────────────────────────────

def _haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance in km between two coordinates."""
    r = 6371  # Earth radius in km
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    return r * 2 * atan2(sqrt(a), sqrt(1 - a))


# ── Geocoding (mock) ──────────────────────────────────────────────────────────

def _get_patient_coordinates(location: str) -> tuple:
    """
    Mock geocoding — maps known PH locations to lat/lng.
    In production replace with Nominatim or Google Maps API.
    """
    location_lower = location.lower()

    location_map = {
        "bgc": (14.5494, 121.0509),
        "bonifacio global city": (14.5494, 121.0509),
        "taguig": (14.5243, 121.0792),
        "makati": (14.5547, 121.0244),
        "ortigas": (14.5872, 121.0674),
        "pasig": (14.5764, 121.0851),
        "quezon city": (14.6760, 121.0437),
        "qc": (14.6760, 121.0437),
        "manila": (14.5995, 120.9842),
        "malate": (14.5649, 120.9904),
        "ermita": (14.5831, 120.9794),
        "alabang": (14.4195, 121.0347),
        "muntinlupa": (14.4081, 121.0415),
        "san juan": (14.5997, 121.0382),
        "greenhills": (14.5997, 121.0382),
        "mandaluyong": (14.5794, 121.0359),
    }

    for key, coords in location_map.items():
        if key in location_lower:
            return coords

    # Default to Metro Manila center if location not recognized
    logger.warning("Location not recognized: %s - defaulting to Metro Manila center", location)
    return (14.5995, 120.9842)


# ── Capability Scoring ────────────────────────────────────────────────────────

def _score_hospital(hospital: dict, emergency_type: str) -> tuple:
    """
    Returns (required_met: bool, score: int).
    Score is based on how many preferred capabilities are available.
    """
    caps = EMERGENCY_CAPABILITY_MAP.get(emergency_type, EMERGENCY_CAPABILITY_MAP["GENERAL"])
    hospital_caps = hospital["capabilities"]

    # Check required capabilities
    required_met = all(hospital_caps.get(cap, False) for cap in caps["required"])

    # Score preferred capabilities
    preferred_score = sum(1 for cap in caps["preferred"] if hospital_caps.get(cap, False))

    return required_met, preferred_score


# ── Match Agent Node ──────────────────────────────────────────────────────────

async def match_agent_node(state: AgentState) -> AgentState:
    """
    Match agent node — pure logic, no LLM call.
    Filters hospitals by insurance and capability, ranks by distance and score.
    """
    logger.info("="*30)
    logger.info("Match Agent Node")
    logger.info("="*30)

    # Parse intake output from last message
    last_message = state["messages"][-1]
    try:
        intake_data = json.loads(last_message.content)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse intake data: %s", e)
        return {
            "messages": [
                AIMessage(
                    content=json.dumps({"error": "Failed to parse intake data"}),
                    name="match_agent"
                )
            ],
            "next_agent": "response_agent"
        }

    emergency_type = intake_data.get("emergency_type", "GENERAL")
    location = intake_data.get("location", "unknown")
    insurance_provider = intake_data.get("insurance_provider", "unknown")

    logger.info("Matching for — Emergency: %s | Location: %s | Insurance: %s",
                emergency_type, location, insurance_provider)

    # Get patient coordinates
    patient_lat, patient_lng = _get_patient_coordinates(location)
    logger.info("Patient coordinates: %s, %s", patient_lat, patient_lng)

    # ── Step 1: Filter by insurance ───────────────────────────────────────────
    insurance_filtered = [
        h for h in HOSPITALS
        if insurance_provider in h["insurance_accepted"]
    ]
    logger.info("Hospitals after insurance filter: %s", len(insurance_filtered))

    # ── Step 2: Filter by emergency type support + required capabilities ──────
    capable_hospitals = []
    for hospital in insurance_filtered:
        if emergency_type in hospital["emergency_types_supported"]:
            required_met, preferred_score = _score_hospital(hospital, emergency_type)
            if required_met:
                capable_hospitals.append((hospital, preferred_score))
    logger.info("Hospitals after capability filter: %s", len(capable_hospitals))

    # ── Step 3: Calculate distance and rank ───────────────────────────────────
    ranked = []
    for hospital, preferred_score in capable_hospitals:
        distance_km = _haversine_distance(
            patient_lat, patient_lng,
            hospital["lat"], hospital["lng"]
        )
        ranked.append({
            "hospital": hospital,
            "distance_km": round(distance_km, 2),
            "preferred_score": preferred_score
        })

    # Sort: primary by distance, secondary by preferred score (desc)
    ranked.sort(key=lambda x: (x["distance_km"], -x["preferred_score"]))

    # ── Top 3 results ─────────────────────────────────────────────────────────
    top_matches = ranked[:3]

    if not top_matches:
        logger.warning("No matching hospitals found.")
        match_result = {
            "intake_data": intake_data,
            "matches": [],
            "no_match_reason": (f"No hospitals found accepting {insurance_provider}"
                                f"with {emergency_type} capabilities. ")
        }
    else:
        match_result = {
            "intake_data": intake_data,
            "matches": [
                {
                    "rank": idx + 1,
                    "id": m["hospital"]["id"],
                    "name": m["hospital"]["name"],
                    "address": m["hospital"]["address"],
                    "distance_km": m["distance_km"],
                    "contact": m["hospital"]["contact"],
                    "emergency_contact": m["hospital"]["emergency_contact"],
                    "capabilities": m["hospital"]["capabilities"],
                    "preferred_score": m["preferred_score"]
                }
                for idx, m in enumerate(top_matches)
            ]
        }

    logger.info("Match result: %s", json.dumps(match_result, indent=2))

    return {
        "messages": [AIMessage(content=json.dumps(match_result), name="match_agent")],
        "next_agent": "response_agent"
    }
