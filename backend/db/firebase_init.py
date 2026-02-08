import os

# Try to import firebase_admin, handle failure gracefully
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError as e:
    print(f"Firebase Admin SDK not available or missing dependencies: {e}")
    FIREBASE_AVAILABLE = False
    firebase_admin = None
    firestore = None
    credentials = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "firebase-key.json")

# Prevent double initialization
if FIREBASE_AVAILABLE and not firebase_admin._apps:
    if os.path.exists(KEY_PATH):
        try:
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
    else:
        print(f"Firebase key not found at {KEY_PATH}. Database operations will fail.")
        # OPTIONAL: Initialize with no query (for testing without DB) or Mock?
        # For now, we leave it uninitialized or let client() fail later.

try:
    if FIREBASE_AVAILABLE and firebase_admin._apps:
        db = firestore.client()
    else:
        print("Firebase not initialized. Using Mock/None for db.")
        db = None
except Exception as e:
    print(f"Error creating Firestore client: {e}")
    db = None

