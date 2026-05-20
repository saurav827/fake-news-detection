"""
Configuration file for Fake News Detection System
"""

# Model Configuration
MODEL_CONFIG = {
    'max_features': 5000,
    'min_df': 2,
    'max_df': 0.8,
    'ngram_range': (1, 2),
    'test_size': 0.2,
    'random_state': 42,
}

# Language Configuration
LANGUAGES = ['english', 'hindi']

# Language-specific settings
LANGUAGE_CONFIG = {
    'english': {
        'stopwords': 'english',
        'stemmer': 'english'
    },
    'hindi': {
        'stopwords': 'hindi',
        'stemmer': 'hindi'
    }
}

# UI Configuration
UI_CONFIG = {
    'page_title': 'Fake News Detector',
    'page_icon': ':newspaper:',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

DEMO_WARNING = (
    "Demo-level educational fake news detector: this project uses a small sample "
    "dataset, so predictions and confidence scores should not be treated as fact. "
    "Always verify important news with trusted sources."
)

# Thresholds
THRESHOLDS = {
    'confidence_min': 50,  # Minimum confidence percentage
    'confidence_default': 70,
    'confidence_max': 100
}

# File Paths (relative to project root)
FILE_PATHS = {
    'data_dir': 'data',
    'models_dir': 'models',
    'src_dir': 'src',
    'english_data': 'data/english_news.csv',
    'hindi_data': 'data/hindi_news.csv',
}

# Suspicious Keywords
SUSPICIOUS_KEYWORDS = {
    'english': {
        'fake', 'fraud', 'conspiracy', 'hoax', 'unreliable',
        'misleading', 'sensational', 'exaggerated', 'biased',
        'propaganda', 'scam', 'viral', 'shocking', 'unbelievable',
        'click bait', 'anonymous', 'rumor'
    },
    'hindi': {
        'झूठ', 'धोखा', 'षड्यंत्र', 'असत्य', 'गलत',
        'भ्रामक', 'अतिशंक', 'पूर्वाग्रह', 'प्रचार',
        'स्कैम', 'वायरल'
    }
}

# Performance Optimization
OPTIMIZATION = {
    'cache_models': True,
    'use_gpu': False,  # Set True if GPU available
    'batch_size': 32,
    'n_jobs': -1  # Use all processors
}

# Logging Configuration
LOGGING = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'logs/app.log'
}

if __name__ == "__main__":
    import json
    print("Configuration:")
    print(json.dumps({k: v for k, v in globals().items() if k.isupper()}, indent=2, default=str))
