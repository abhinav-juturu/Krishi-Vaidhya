# pipeline.py
"""
Full AI pipeline:
CNN → Grad-CAM → LLM → Firestore
"""

import os
import tensorflow as tf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from .infer import run_inference
from .gradcam import run_gradcam
from .llm import get_llm_explanation
from ..db.diagnosis_service import create_diagnosis
from ..location.location_service import normalize_location

MODEL_PATH = os.path.join(BASE_DIR, "model", "plant_disease_model.h5")

# Load once
model = tf.keras.models.load_model(MODEL_PATH)


def run_pipeline(image_path: str, user_id: str, lat: float, lng: float) -> dict:
    """
    Run full AI pipeline with location integration.
    
    Args:
        image_path: Path to plant image
        user_id: User ID
        lat: Latitude
        lng: Longitude
    
    Returns:
        Complete diagnosis with location and nearby agri stores
    """
    # Step 1: CNN Inference
    cnn_output = run_inference(image_path)
    cnn_output["userId"] = user_id
    
    # Step 2: Grad-CAM Explainability
    cnn_output = run_gradcam(image_path, cnn_output, model)
    
    # Step 3: LLM Explanation
    llm_output = get_llm_explanation(cnn_output)
    
    # Step 4: Normalize Location
    location = normalize_location(lat, lng)
    
    # Step 5: Save to Firestore
    diagnosis_id = create_diagnosis(
        user_id=cnn_output["userId"],
        crop=cnn_output["crop"],
        disease=cnn_output["predicted_disease"],
        confidence=cnn_output["confidence"],
        explainability=cnn_output["explainability"],
        location=location,
        llm=llm_output
    )
    
    # Step 6: Get Nearby Agri Stores
    from .agri_store_service import get_nearby_agri_stores
    agri_stores = get_nearby_agri_stores(location, radius_km=10)
    
    # Final output
    final_output = {
        **cnn_output,
        "llm": llm_output,
        "location": location,
        "diagnosisId": diagnosis_id,
        "nearbyAgriStores": agri_stores
    }
    
    return final_output


if __name__ == "__main__":
    result = run_pipeline(
        image_path=os.path.join(BASE_DIR, "test_image.JPG"),
        user_id="9999999999",
        lat=12.9716,
        lng=77.5946
    )
    
    print("\n✅ PIPELINE RESULT\n")
    print(result)