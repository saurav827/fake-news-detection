"""
Model Utility Functions for Fake News Detection System

This module provides utility functions for loading, saving, and managing models.
"""

import os
import joblib
from pathlib import Path


def get_models_directory():
    """
    Get the models directory path.
    
    Returns:
        str: Path to models directory
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'models')


def get_data_directory():
    """
    Get the data directory path.
    
    Returns:
        str: Path to data directory
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'data')


def check_model_exists(language='english'):
    """
    Check if trained model exists for a language.
    
    Args:
        language (str): 'english' or 'hindi'
        
    Returns:
        bool: True if model exists, False otherwise
    """
    models_dir = get_models_directory()
    model_path = os.path.join(models_dir, f'{language}_model.pkl')
    vectorizer_path = os.path.join(models_dir, f'{language}_vectorizer.pkl')
    
    return os.path.exists(model_path) and os.path.exists(vectorizer_path)


def get_available_models():
    """
    Get list of available trained models.
    
    Returns:
        list: List of language codes for available models
    """
    available = []
    for language in ['english', 'hindi']:
        if check_model_exists(language):
            available.append(language)
    return available


def load_model(language='english'):
    """
    Load pre-trained model and vectorizer for a language.
    
    Args:
        language (str): 'english' or 'hindi'
        
    Returns:
        tuple: (model, vectorizer) or (None, None) if not found
    
    Type:
        Tuple[Any | None, Any | None]
    """
    models_dir = get_models_directory()
    model_path = os.path.join(models_dir, f'{language}_model.pkl')
    vectorizer_path = os.path.join(models_dir, f'{language}_vectorizer.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return None, None
    
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        return model, vectorizer
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None


def load_stats(language='english'):
    """
    Load training statistics for a model.
    
    Args:
        language (str): 'english' or 'hindi'
        
    Returns:
        dict: Training statistics or empty dict if not found
    """
    models_dir = get_models_directory()
    stats_path = os.path.join(models_dir, f'{language}_stats.pkl')
    
    if not os.path.exists(stats_path):
        return {}
    
    try:
        stats = joblib.load(stats_path)
        return stats
    except Exception as e:
        print(f"Error loading stats: {e}")
        return {}


def print_model_info():
    """
    Print information about available models.
    """
    print("\nAvailable Models:")
    print("-" * 40)
    
    available = get_available_models()
    
    if not available:
        print("No models found. Run 'python src/train.py' to train models.")
        return
    
    for language in available:
        stats = load_stats(language)
        print(f"\n{language.upper()}:")
        
        if stats:
            print(f"  Accuracy:  {stats.get('test_accuracy', 'N/A'):.4f}")
            print(f"  Precision: {stats.get('precision', 'N/A'):.4f}")
            print(f"  Recall:    {stats.get('recall', 'N/A'):.4f}")
            print(f"  F1-Score:  {stats.get('f1_score', 'N/A'):.4f}")
            print(f"  Samples:   {stats.get('train_samples', 'N/A')} training")
            print(f"  Features:  {stats.get('total_features', 'N/A')} TF-IDF")
        else:
            print("  Stats not found")


if __name__ == "__main__":
    print_model_info()
