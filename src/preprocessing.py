"""
Data Preprocessing Module for Multilingual Fake News Detection System

This module contains all text preprocessing functions including:
- Text lowercasing
- Punctuation removal
- Stopword removal
- Lemmatization
- Clean text normalization
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, SnowballStemmer

FALLBACK_ENGLISH_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'were', 'will', 'with', 'this', 'these', 'those'
}

# Initialize lemmatizer and stemmer
lemmatizer = WordNetLemmatizer()
english_stemmer = SnowballStemmer('english')


def _load_stopwords(language):
    """Load NLTK stopwords if available without downloading during import."""
    try:
        return set(stopwords.words(language))
    except LookupError:
        if language == 'english':
            return FALLBACK_ENGLISH_STOPWORDS
        return set()
    except OSError:
        if language == 'english':
            return FALLBACK_ENGLISH_STOPWORDS
        return set()


def _safe_lemmatize(word):
    """Lemmatize when WordNet data exists; otherwise keep the token unchanged."""
    try:
        return lemmatizer.lemmatize(word)
    except LookupError:
        return word


# Get stopwords for both languages without network calls at import time.
english_stopwords = _load_stopwords('english')
hindi_stopwords = _load_stopwords('hindi')


def clean_text_english(text):
    """
    Clean English text by removing URLs, HTML tags, and special characters.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_text_hindi(text):
    """
    Clean Hindi text by removing URLs and special characters.
    
    Args:
        text (str): Raw Hindi text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    # Keep Hindi characters and remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def preprocess_text_english(text):
    """
    Comprehensive preprocessing for English text.
    Steps: Clean → Lowercase → Remove punctuation → Tokenize → Remove stopwords → Lemmatize
    
    Args:
        text (str): Raw text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    # Clean text
    text = clean_text_english(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize without requiring NLTK punkt data at runtime.
    tokens = re.findall(r'\b[a-zA-Z]+\b', text)

    # Remove stopwords and lemmatize
    tokens = [_safe_lemmatize(word) for word in tokens
              if word not in english_stopwords and len(word) > 2]
    
    # Join back to string
    return ' '.join(tokens)


def preprocess_text_hindi(text):
    """
    Comprehensive preprocessing for Hindi text.
    Steps: Clean → Remove punctuation → Normalize → Remove stopwords
    
    Args:
        text (str): Raw Hindi text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    # Clean text
    text = clean_text_hindi(text)
    
    # Remove English punctuation and normalize
    text = re.sub(r'[!@#$%^&*()_+=\[\]{};:\'",.<>?/\\|-]', '', text)
    
    # Tokenize (for Hindi, we do basic space-based tokenization)
    tokens = text.split()
    
    # Remove stopwords and short tokens
    tokens = [word for word in tokens 
              if word not in hindi_stopwords and len(word) > 2]
    
    return ' '.join(tokens)


def preprocess_text(text, language='english'):
    """
    Main preprocessing function that routes to appropriate language handler.
    
    Args:
        text (str): Text to preprocess
        language (str): Language code - 'english' or 'hindi'
        
    Returns:
        str: Preprocessed text
    """
    if language.lower() == 'hindi':
        return preprocess_text_hindi(text)
    else:
        return preprocess_text_english(text)


def batch_preprocess(texts, language='english'):
    """
    Preprocess a batch of texts.
    
    Args:
        texts (list): List of texts to preprocess
        language (str): Language code
        
    Returns:
        list: List of preprocessed texts
    """
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
    """
    Identify suspicious keywords that might indicate fake news.
    
    Args:
        text (str): Preprocessed or raw text to analyze
        language (str): Language code
        
    Returns:
        list: List of suspicious words found
    """
    text_lower = text.lower()
    
    if language.lower() == 'hindi':
        keywords = SUSPICIOUS_KEYWORDS_HINDI
    else:
        keywords = SUSPICIOUS_KEYWORDS_ENGLISH
    
    found_keywords = [word for word in keywords if word in text_lower]
    return found_keywords


if __name__ == "__main__":
    # Test the preprocessing functions
    sample_english = "This is FAKE NEWS!!! Check this out: http://example.com. Contact: test@example.com"
    sample_hindi = "यह झूठी खबर है। http://example.com देखें।"
    
    print("English Preprocessing:")
    print(f"Original: {sample_english}")
    print(f"Processed: {preprocess_text_english(sample_english)}\n")
    
    print("Hindi Preprocessing:")
    print(f"Original: {sample_hindi}")
    print(f"Processed: {preprocess_text_hindi(sample_hindi)}\n")
    
    print("Suspicious Words (English):")
    print(highlight_suspicious_words(sample_english, 'english'))
    
    print("\nSuspicious Words (Hindi):")
    print(highlight_suspicious_words(sample_hindi, 'hindi'))
