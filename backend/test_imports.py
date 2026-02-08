
import sys

with open("import_test_result.txt", "w") as f:
    f.write("Testing imports...\n")
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        f.write("Firebase Admin imported successfully\n")
    except ImportError as e:
        f.write(f"Firebase Admin import failed: {e}\n")
    except Exception as e:
        f.write(f"Firebase Admin error: {e}\n")

    try:
        import google.auth.transport.requests
        f.write("google.auth.transport.requests imported successfully\n")
    except Exception as e:
        f.write(f"google.auth.transport.requests failed: {e}\n")

    try:
        import requests
        f.write(f"requests version: {requests.__version__}\n")
    except Exception as e:
        f.write(f"requests failed: {e}\n")
