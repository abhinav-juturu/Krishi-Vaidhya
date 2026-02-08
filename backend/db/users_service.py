# users_service.py
from . import firebase_init
from firebase_admin import firestore
from .firebase_init import db

def upsert_user(phone: str, name: str, language: str, crops: list):
    if db is None:
        print("Database not available. Returning mock success.")
        return {
            "userId": phone,
            "status": "mock_success_no_db"
        }

    user_ref = db.collection("users").document(phone)

    user_ref.set({
        "name": name,
        "phone": phone,
        "language": language,
        "crops": crops,
        "lastActive": firestore.SERVER_TIMESTAMP,
        "createdAt": firestore.SERVER_TIMESTAMP
    }, merge=True)

    return {
        "userId": phone,
        "status": "user_saved"
    }
