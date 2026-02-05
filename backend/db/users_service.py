# users_service.py
import firebase_init  # <-- THIS LINE is mandatory
from firebase_admin import firestore

db = firestore.client()

def upsert_user(phone: str, name: str, language: str, crops: list):
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
