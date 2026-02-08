# test_user.py
import firebase_init
from users_service import upsert_user

result = upsert_user(
    phone="9999999999",
    name="Test Farmer",
    language="en",
    crops=["Tomato", "Apple"]
)

print(result)
