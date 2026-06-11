"""
Data Preprocessing Module for Multilingual Fake News Detection System

This module contains optimized text preprocessing functions including:
- Text lowercasing
- Punctuation removal
- Stopword removal
- Stemming (using SnowballStemmer)
- URL, email, and HTML tag removal
- Emoji and repeated whitespace cleaning
"""

import re
import string
import nltk

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('stopwords', quiet=True)
    except Exception:
        pass

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer


FALLBACK_ENGLISH_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'were', 'will', 'with', 'this', 'these', 'those'
}

# Initialize Snowball Stemmer
english_stemmer = SnowballStemmer('english')


def _load_stopwords(language):
    """Load NLTK stopwords with local fallbacks if not found."""
    try:
        return set(stopwords.words(language))
    except Exception:
        if language == 'english':
            return FALLBACK_ENGLISH_STOPWORDS
        return set()


# Get stopwords for both languages.
english_stopwords = _load_stopwords('english')
hindi_stopwords = _load_stopwords('hindi')


def clean_text_english(text):
    """
    Clean English text by removing URLs, HTML tags, emojis, emails, and repeated spaces.
    """
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove emojis (supplementary plane characters)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_text_hindi(text):
    """
    Clean Hindi text by removing URLs, HTML tags, emojis, emails, and repeated spaces.
    """
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove emojis
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def preprocess_text_english(text):
    """
    Comprehensive preprocessing for English text.
    Steps: Clean → Lowercase → Remove punctuation → Tokenize → Remove stopwords → Stem
    """
    text = clean_text_english(text)
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize words (letters only)
    tokens = re.findall(r'\b[a-zA-Z]+\b', text)

    # Filter stopwords and apply stemming
    processed_tokens = []
    for word in tokens:
        if word not in english_stopwords and len(word) > 2:
            try:
                stemmed = english_stemmer.stem(word)
                processed_tokens.append(stemmed)
            except Exception:
                processed_tokens.append(word)
                
    return ' '.join(processed_tokens)


def preprocess_text_hindi(text):
    """
    Comprehensive preprocessing for Hindi text.
    Steps: Clean → Remove punctuation → Tokenize → Remove stopwords
    """
    text = clean_text_hindi(text)
    
    # Remove English/common punctuation and brackets
    text = re.sub(r'[!@#$%^&*()_+=\[\]{};:\'",.<>?/\\|`~-]', '', text)
    
    # Split by spaces
    tokens = text.split()
    
    # Remove Hindi stopwords and short tokens
    processed_tokens = [word for word in tokens 
                        if word not in hindi_stopwords and len(word) > 1]
    
    return ' '.join(processed_tokens)


def preprocess_text(text, language='english'):
    """
    Main preprocessing function that routes to the appropriate language handler.
    """
    if str(language).lower() == 'hindi':
        return preprocess_text_hindi(text)
    else:
        return preprocess_text_english(text)


def batch_preprocess(texts, language='english'):
    """Preprocess a list of texts."""
    return [preprocess_text(text, language) for text in texts]


# Suspicious keywords that often indicate fake news
SUSPICIOUS_KEYWORDS_ENGLISH = {
    'fake', 'fraud', 'conspiracy', 'hoax', 'unreliable', 'misleading',
    'sensational', 'exaggerated', 'biased', 'propaganda', 'scam', 'viral',
    'shocking', 'unbelievable', 'click bait', 'anonymous source', 'rumor'
}

SUSPICIOUS_KEYWORDS_HINDI = {
    'झूठ', 'धोखा', 'षड्यंत्र', 'असत्य', 'गलत', 'भ्रामक',
    'अतिशंक', 'पूर्वाग्रह', 'प्रचार', 'स्कैम', 'वायरल'
}


def highlight_suspicious_words(text, language='english'):
    """Identify suspicious keywords that might indicate fake news."""
    text_lower = str(text).lower()
    keywords = SUSPICIOUS_KEYWORDS_HINDI if str(language).lower() == 'hindi' else SUSPICIOUS_KEYWORDS_ENGLISH
    return [word for word in keywords if word in text_lower]


if __name__ == "__main__":
    sample_english = "This is FAKE NEWS!!! Check this out: http://example.com. Contact: test@example.com 😊"
    sample_hindi = "यह झूठी खबर है। http://example.com देखें। 😊"
    
    print("English Preprocessed:", preprocess_text_english(sample_english))
    print("Hindi Preprocessed:", preprocess_text_hindi(sample_hindi))
    print(highlight_suspicious_words(sample_english, 'english'))
    
    print("\nSuspicious Words (Hindi):")
    print(highlight_suspicious_words(sample_hindi, 'hindi'))
