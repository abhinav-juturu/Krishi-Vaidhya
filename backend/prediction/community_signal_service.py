# kvb/prediction/community_signal_service.py
"""
Community Signal Service
Analyzes nearby disease outbreaks from community posts.
This is PREPARATION ONLY - no ML prediction logic yet.
"""

import math
from datetime import datetime, timedelta
from ..db.firebase_init import db


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate distance between two points in km (Haversine formula)."""
    R = 6371
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lng / 2) ** 2)
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def get_nearby_outbreaks(
    crop: str,
    location: dict,
    radius_km: int = 20,
    days: int = 14
) -> dict:
    """
    Analyze nearby disease outbreaks from community posts.
    
    Args:
        crop: Crop name (e.g., "Apple")
        location: Normalized location dict
        radius_km: Search radius in km
        days: Look back period in days
    
    Returns:
        {
            "total_cases": int,
            "diseases": list[str],
            "risk_score": float (0-1)
        }
    """
    lat = location["lat"]
    lng = location["lng"]
    geohash = location["geohash"]
    
    # Calculate time threshold
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    # Query community posts
    # Note: Firestore doesn't support geospatial queries directly
    # We use geohash prefix matching + client-side distance filtering
    
    geohash_prefix = geohash[:3]  # Broader area for initial query
    
    posts_ref = db.collection("community")
    query = posts_ref.where("createdAt", ">=", cutoff_date)
    
    matching_posts = []
    diseases = []
    
    try:
        for doc in query.stream():
            post = doc.to_dict()
            post_location = post.get("location", {})
            
            # Skip if no location
            if not post_location or "lat" not in post_location:
                continue
            
            # Check geohash prefix match (fast filter)
            post_geohash = post_location.get("geohash", "")
            if not post_geohash.startswith(geohash_prefix):
                continue
            
            # Calculate exact distance
            post_lat = post_location["lat"]
            post_lng = post_location["lng"]
            distance = calculate_distance(lat, lng, post_lat, post_lng)
            
            if distance <= radius_km:
                content = post.get("content", "").lower()
                
                # Simple disease keyword matching
                # In production, use NLP or link to diagnosis records
                disease_keywords = [
                    "black rot", "scab", "rust", "blight",
                    "leaf spot", "powdery mildew", "wilt"
                ]
                
                for disease in disease_keywords:
                    if disease in content and crop.lower() in content:
                        matching_posts.append(post)
                        diseases.append(disease.title())
                        break
        
        # Calculate risk score (simple heuristic)
        total_cases = len(matching_posts)
        
        if total_cases == 0:
            risk_score = 0.0
        elif total_cases <= 2:
            risk_score = 0.3
        elif total_cases <= 5:
            risk_score = 0.6
        else:
            risk_score = 0.9
        
        return {
            "total_cases": total_cases,
            "diseases": list(set(diseases)),  # Unique diseases
            "risk_score": round(risk_score, 2)
        }
    
    except Exception as e:
        print(f"⚠️ Failed to fetch community signals: {e}")
        return {
            "total_cases": 0,
            "diseases": [],
            "risk_score": 0.0
        }