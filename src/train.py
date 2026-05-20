"""
Training Script for Multilingual Fake News Detection System

This script:
1. Loads English and Hindi news datasets
2. Preprocesses text data
3. Converts text to TF-IDF vectors
4. Trains multiple ML models (Logistic Regression, Naive Bayes, Random Forest, SVM)
5. Evaluates and compares all models
6. Selects the best model based on accuracy
7. Saves the best trained models and vectorizers

Requirements: pandas, scikit-learn, nltk
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import warnings

warnings.filterwarnings('ignore')

# Import preprocessing module
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing import preprocess_text

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Create models directory if it doesn't exist
os.makedirs(MODELS_DIR, exist_ok=True)


class FakeNewsDetectionModel:
    """
    Class to handle training, comparison, and saving of fake news detection models.
    """
    
    def __init__(self, language='english', max_features=5000):
        self.language = language
        self.max_features = max_features
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2),
            stop_words='english' if language == 'english' else None
        )
        
        # Define all the models we want to train and compare
        self.models = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
            'Naive Bayes': MultinomialNB(),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'SVM': SVC(probability=True, kernel='linear', random_state=42)
        }
        
        self.best_model_name = None
        self.best_model = None
        self.training_stats = {}
        self.all_results = {}
    
    def load_data(self, csv_file):
        print(f"\nLoading {self.language} dataset from {csv_file}...")
        df = pd.read_csv(csv_file)
        
        # Combine title and text if title exists
        if 'title' in df.columns:
            df['full_text'] = df['title'].fillna('') + ' ' + df['text'].fillna('')
        else:
            df['full_text'] = df['text'].fillna('')
            
        texts = df['full_text'].values
        labels = np.asarray(df['label'].values, dtype=np.int64)
        
        print(f"Loaded {len(texts)} samples")
        return texts, labels
    
    def preprocess_data(self, texts):
        print(f"Preprocessing {len(texts)} texts for {self.language}...")
        preprocessed_texts = []
        
        for i, text in enumerate(texts):
            if pd.isna(text) or text.strip() == '':
                preprocessed_texts.append('')
            else:
                processed = preprocess_text(str(text), self.language)
                preprocessed_texts.append(processed)
        
        print(f"Preprocessing complete!")
        return preprocessed_texts
    
    def train_and_compare(self, texts, labels, test_size=0.2):
        print(f"\n{'='*60}")
        print(f"TRAINING & COMPARING MODELS FOR {self.language.upper()}")
        print(f"{'='*60}\n")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=test_size, random_state=42, stratify=labels
        )
        
        # Vectorization
        print("Converting texts to TF-IDF vectors...")
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        print(f"TF-IDF matrix shape: {X_train_tfidf.shape}\n")
        
        best_accuracy = 0
        
        # Train and evaluate each model
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train_tfidf, y_train)
            
            # Predict
            y_pred = model.predict(X_test_tfidf)
            
            # Calculate metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            self.all_results[name] = {
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1_score': f1
            }
            
            # Check if this is the best model so far
            if acc > best_accuracy:
                best_accuracy = acc
                self.best_model_name = name
                self.best_model = model
                
                # Store stats for the best model
                self.training_stats = {
                    'language': self.language,
                    'best_model': name,
                    'test_accuracy': acc,
                    'precision': prec,
                    'recall': rec,
                    'f1_score': f1,
                    'train_samples': len(X_train),
                    'test_samples': len(X_test),
                    'total_features': len(self.vectorizer.get_feature_names_out())
                }
                
        # Print comparison table
        print("\nModel Comparison Table:")
        print("-" * 50)
        print(f"{'Model Name':<20} | {'Accuracy':<10} | {'F1-Score':<10}")
        print("-" * 50)
        for name, metrics in self.all_results.items():
            print(f"{name:<20} | {metrics['accuracy']:.4f}     | {metrics['f1_score']:.4f}")
        print("-" * 50)
        
        print(f"\n=> Best Model Selected: {self.best_model_name} with Accuracy: {best_accuracy:.4f}\n")
        
        return self.training_stats
    
    def save_best_model(self, model_dir=None):
        if model_dir is None:
            model_dir = MODELS_DIR
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save best model
        model_path = os.path.join(model_dir, f'{self.language}_model.pkl')
        joblib.dump(self.best_model, model_path)
        print(f"Best Model ({self.best_model_name}) saved: {model_path}")
        
        # Save vectorizer
        vectorizer_path = os.path.join(model_dir, f'{self.language}_vectorizer.pkl')
        joblib.dump(self.vectorizer, vectorizer_path)
        print(f"Vectorizer saved: {vectorizer_path}")
        
        # Save training stats
        stats_path = os.path.join(model_dir, f'{self.language}_stats.pkl')
        joblib.dump(self.training_stats, stats_path)
        print(f"Stats saved: {stats_path}\n")


def main():
    print("\n" + "="*60)
    print("MULTILINGUAL FAKE NEWS DETECTION SYSTEM")
    print("Training Script - Model Comparison & Selection")
    print("="*60 + "\n")
    
    # Train English Models
    english_csv = os.path.join(DATA_DIR, 'english_news.csv')
    if os.path.exists(english_csv):
        print("STEP 1: Training English Models")
        en_model = FakeNewsDetectionModel(language='english')
        en_texts, en_labels = en_model.load_data(english_csv)
        en_texts_processed = en_model.preprocess_data(en_texts)
        en_model.train_and_compare(en_texts_processed, en_labels)
        en_model.save_best_model()
    else:
        print(f"Error: {english_csv} not found! Skipping English training.")
    
    # Train Hindi Models
    hindi_csv = os.path.join(DATA_DIR, 'hindi_news.csv')
    if os.path.exists(hindi_csv):
        print("\nSTEP 2: Training Hindi Models")
        hi_model = FakeNewsDetectionModel(language='hindi')
        hi_texts, hi_labels = hi_model.load_data(hindi_csv)
        hi_texts_processed = hi_model.preprocess_data(hi_texts)
        hi_model.train_and_compare(hi_texts_processed, hi_labels)
        hi_model.save_best_model()
    else:
        print(f"Error: {hindi_csv} not found! Skipping Hindi training.")
    
    print("\n✓ Training and comparison complete! Best models saved for deployment.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
