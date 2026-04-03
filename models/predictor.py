import pickle
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_PATH, VECTORIZER_PATH

def load_models():
    model = None
    vectorizer = None
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, "rb") as f:
            vectorizer = pickle.load(f)
    return model, vectorizer

def predict_job_role(text):
    model, vectorizer = load_models()
    if not model or not vectorizer:
        return "Model not trained", 0.0
    
    vec_text = vectorizer.transform([text])
    prediction = model.predict(vec_text)[0]
    
    # For confidence score, we can use predict_proba max probability
    proba = model.predict_proba(vec_text)[0]
    confidence = max(proba)
    return prediction, confidence
