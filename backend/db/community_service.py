# kvb/db/community_service.py
from .firebase_init import db
from firebase_admin import firestore
from datetime import datetime
from google.cloud.firestore import Increment, ArrayUnion


# ---------------- CREATE POST ----------------
def create_post(user_id: str, content: str, lat: float, lng: float) -> str:
    """
    Create a community post with normalized location.
    
    Args:
        user_id: User ID (phone number)
        content: Post content
        lat: Latitude
        lng: Longitude
    
    Returns:
        Post document ID
    """
    # Import here to avoid circular dependency
    from ..location.location_service import normalize_location
    
    # Normalize location
    location = normalize_location(lat, lng)
    
    doc_ref = db.collection("community").document()
    doc_ref.set({
        "userId": user_id,
        "content": content,
        "location": location,
        "likes": 0,
        "commentsCount": 0,
        "createdAt": datetime.utcnow()
    })
    
    return doc_ref.id


# ---------------- GET FEED ----------------
def get_posts(limit: int = 20):
    """Get recent community posts."""
    posts = (
        db.collection("community")
        .order_by("createdAt", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )
    return [{"id": doc.id, **doc.to_dict()} for doc in posts]


# ---------------- ADD COMMENT ----------------
def add_comment(post_id: str, user_id: str, content: str):
    """Add a comment to a post."""
    post_ref = db.collection("community").document(post_id)
    
    # Add comment as subcollection
    post_ref.collection("comments").add({
        "userId": user_id,
        "content": content,
        "createdAt": datetime.utcnow()
    })
    
    # Increment comment count
    post_ref.update({
        "commentsCount": Increment(1)
    })


# ---------------- LIKE POST ----------------
def like_post(post_id: str, user_id: str):
    """Like a post (increment count and track user)."""
    post_ref = db.collection("community").document(post_id)
    
    post_ref.update({
        "likes": Increment(1),
        "likedBy": ArrayUnion([user_id])
    })