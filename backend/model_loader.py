import os
import joblib
try:
    import streamlit as st
except ImportError:
    st = None


def _cache_resource(func):
    if st is not None and _is_streamlit_runtime():
        return st.cache_resource(func)
    return func


def _is_streamlit_runtime():
    try:
        from streamlit.runtime import exists
        return exists()
    except Exception:
        return False


def _show_error(message):
    if st is not None and _is_streamlit_runtime():
        st.error(message)
    else:
        print(message)


@_cache_resource
def load_models():
    """
    Load pre-trained models and vectorizers for both languages.
    Uses Streamlit's caching to load models only once.
    """
    models = {}
    
    # Get the project root directory (parent of backend folder)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(base_dir, 'models')
    
    try:
        # Load English models and stats
        en_model_path = os.path.join(models_dir, 'english_model.pkl')
        en_vectorizer_path = os.path.join(models_dir, 'english_vectorizer.pkl')
        en_stats_path = os.path.join(models_dir, 'english_stats.pkl')
        
        if os.path.exists(en_model_path) and os.path.exists(en_vectorizer_path):
            models['english_model'] = joblib.load(en_model_path)
            models['english_vectorizer'] = joblib.load(en_vectorizer_path)
            if os.path.exists(en_stats_path):
                models['english_stats'] = joblib.load(en_stats_path)
        
        # Load Hindi models and stats
        hi_model_path = os.path.join(models_dir, 'hindi_model.pkl')
        hi_vectorizer_path = os.path.join(models_dir, 'hindi_vectorizer.pkl')
        hi_stats_path = os.path.join(models_dir, 'hindi_stats.pkl')
        
        if os.path.exists(hi_model_path) and os.path.exists(hi_vectorizer_path):
            models['hindi_model'] = joblib.load(hi_model_path)
            models['hindi_vectorizer'] = joblib.load(hi_vectorizer_path)
            if os.path.exists(hi_stats_path):
                models['hindi_stats'] = joblib.load(hi_stats_path)
        
        return models
    
    except Exception as e:
        _show_error(f"Error loading models: {e}")
        return None
