import firebase_init
from diagnosis_service import save_diagnosis

cnn_output = {
    "crop": "Apple",
    "predicted_disease": "Apple___Black_rot",
    "confidence": 0.9984,
    "explainability": {
        "method": "Grad-CAM",
        "summary": "Focused on leaf lesions and dark spots"
    }
}

llm_output = {
    "disease_overview": "Apple Black rot is a fungal disease...",
    "why_this_prediction": "The model focused on lesion regions...",
    "chemical_treatments": ["Captan", "Ziram"],
    "organic_treatments": ["Copper spray"],
    "prevention_tips": "Remove infected debris"
}

result = save_diagnosis(
    user_id="9999999999",
    cnn_output=cnn_output,
    llm_output=llm_output
)

print(result)
