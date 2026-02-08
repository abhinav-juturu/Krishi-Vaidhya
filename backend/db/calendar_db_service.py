# kvb/db/calendar_db_service.py
"""
Firestore operations for calendar management.
"""

from firebase_admin import firestore
from .firebase_init import db
from datetime import datetime


def save_calendar(calendar: dict) -> str:
    """
    Save a calendar to Firestore.
    
    Args:
        calendar: Calendar dict
    
    Returns:
        Calendar ID
    """
    if db is None:
        print("Database not available. Returning mock ID.")
        return "mock_calendar_id_123"

    # Add timestamps
    calendar["createdAt"] = firestore.SERVER_TIMESTAMP
    calendar["updatedAt"] = firestore.SERVER_TIMESTAMP
    
    # Save to Firestore
    ref = db.collection("calendars").document()
    ref.set(calendar)
    
    return ref.id


def get_calendar(calendar_id: str) -> dict:
    """
    Retrieve a calendar from Firestore.
    
    Args:
        calendar_id: Calendar document ID
    
    Returns:
        Calendar dict or None if not found
    """
    if db is None:
        print("Database not available. Returning mock calendar.")
        # Return a mock calendar for testing if needed, or None
        return {
            "calendarId": calendar_id,
            "crop": "Tomato",
            "lifecycle": [],
            "status": "active",
            "userId": "mock_user",
            "sowingDate": "2023-01-01",
            "durationDays": 100,
            "location": {"lat": 0, "lng": 0},
            "optimalConditions": {},
            "reschedulingHistory": []
        }

    if db is None:
        print("Database not available. Returning mock calendar.")
        return {
            "calendarId": calendar_id,
            "crop": "Tomato",
            "lifecycle": [],
            "status": "active",
            "userId": "mock_user",
            "sowingDate": "2023-01-01",
            "durationDays": 100,
            "location": {"lat": 0, "lng": 0},
            "optimalConditions": {},
            "reschedulingHistory": []
        }

    doc = db.collection("calendars").document(calendar_id).get()
    
    if doc.exists:
        calendar = doc.to_dict()
        calendar["calendarId"] = doc.id
        return calendar
    else:
        return None


def update_calendar(calendar_id: str, calendar: dict) -> bool:
    """
    Update an existing calendar.
    
    Args:
        calendar_id: Calendar document ID
        calendar: Updated calendar dict
    
    Returns:
        True if successful
    """
    if db is None:
        return True

    calendar["updatedAt"] = firestore.SERVER_TIMESTAMP
    
    db.collection("calendars").document(calendar_id).set(calendar, merge=True)
    
    return True


def delete_calendar(calendar_id: str) -> bool:
    """
    Delete a calendar.
    
    Args:
        calendar_id: Calendar document ID
    
    Returns:
        True if successful
    """
    if db is None:
        return True
    db.collection("calendars").document(calendar_id).delete()
    return True


def get_user_calendars(user_id: str, status: str = None) -> list:
    """
    Get all calendars for a user.
    
    Args:
        user_id: User ID
        status: Optional status filter ("active", "completed", "archived")
    
    Returns:
        List of calendars
    """
    if db is None:
        return []

    query = db.collection("calendars").where(filter=firestore.FieldFilter("userId", "==", user_id))
    
    if status:
        query = query.where(filter=firestore.FieldFilter("status", "==", status))
    
    # Note: Ordering requires a composite index in Firestore
    # Commented out until index is created
    # query = query.order_by("createdAt", direction=firestore.Query.DESCENDING)
    
    calendars = []
    for doc in query.stream():
        calendar = doc.to_dict()
        calendar["calendarId"] = doc.id
        calendars.append(calendar)
    
    # Sort in Python instead (temporary workaround)
    calendars.sort(key=lambda x: x.get("createdAt", datetime.min), reverse=True)
    
    return calendars


def get_active_calendars() -> list:
    """
    Get all active calendars (for background processing).
    
    Returns:
        List of active calendars
    """
    if db is None:
        return []

    query = db.collection("calendars").where(filter=firestore.FieldFilter("status", "==", "active"))
    
    calendars = []
    for doc in query.stream():
        calendar = doc.to_dict()
        calendar["calendarId"] = doc.id
        calendars.append(calendar)
    
    return calendars