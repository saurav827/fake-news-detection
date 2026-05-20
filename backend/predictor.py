import numpy as np
import sys
import os

# Ensure src can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.preprocessing import preprocess_text, highlight_suspicious_words

def predict_fake_news(text, language, models):
    """
    Predict whether news is fake or real.
    
    Args:
        text (str): Input news text
        language (str): 'english' or 'hindi'
        models (dict): Dictionary containing loaded models
        
    Returns:
        dict: Prediction results including label, confidence, and probabilities
    """
    # Get appropriate model and vectorizer
    model_key = f'{language}_model'
    vectorizer_key = f'{language}_vectorizer'
    
    if model_key not in models or vectorizer_key not in models:
        return None
    
    model = models[model_key]
    vectorizer = models[vectorizer_key]
    
    # Preprocess text
    processed_text = preprocess_text(text, language)
    
    # Vectorize
    text_tfidf = vectorizer.transform([processed_text])
    
    # Predict
    prediction = model.predict(text_tfidf)[0]
    
    # Predict probabilities - SVM with linear kernel may not have predict_proba unless initialized with probability=True
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(text_tfidf)[0]
    else:
        # Fallback if probability=True was not used
        decision = model.decision_function(text_tfidf)[0]
        # Sigmoid approximation
        prob = 1 / (1 + np.exp(-decision))
        probabilities = np.array([1 - prob, prob])
    
    # Get suspicious keywords
    suspicious_words = highlight_suspicious_words(text, language)
    
    # Prepare results
    result = {
        'prediction': 'REAL NEWS ✓' if prediction == 1 else 'FAKE NEWS ✗',
        'is_real': prediction == 1,
        'confidence': max(probabilities) * 100,
        'fake_probability': probabilities[0] * 100,
        'real_probability': probabilities[1] * 100,
        'suspicious_words': suspicious_words,
        'processed_text': processed_text
    }
    
    return result
