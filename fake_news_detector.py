import pickle
import os
import re
from pathlib import Path

class FakeNewsDetector:
    """Detects fake news using pre-trained ML model"""
    
    def __init__(self):
        # Get the directory where this file is located
        current_dir = Path(__file__).parent
        model_dir = current_dir / "fake news"
        
        # Load the model and vectorizer
        model_path = model_dir / "model.pkl"
        vector_path = model_dir / "vector.pkl"
        
        if not model_path.exists() or not vector_path.exists():
            raise FileNotFoundError(f"Model files not found in {model_dir}")
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(vector_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
    
    def preprocess_text(self, text):
        """Preprocess text for prediction"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def is_fake(self, text):
        """
        Predict if the news text is fake or real
        
        Args:
            text (str): News article text (title + description)
            
        Returns:
            bool: True if fake, False if real
        """
        if not text:
            return False
        
        # Preprocess the text
        processed_text = self.preprocess_text(text)
        
        if not processed_text:
            return False
        
        try:
            # Vectorize the text
            text_vector = self.vectorizer.transform([processed_text])
            
            # Predict
            prediction = self.model.predict(text_vector)[0]
            
            # Model trained with: 0 = Real, 1 = Fake
            # Return True if fake (prediction == 1)
            return prediction == 1
            
        except Exception as e:
            print(f"Error in fake news detection: {e}")
            # In case of error, assume it's real to avoid false positives
            return False
    
    def get_confidence(self, text):
        """
        Get prediction confidence/probability
        
        Args:
            text (str): News article text
            
        Returns:
            float: Confidence score (0-1)
        """
        if not text:
            return 0.0
        
        processed_text = self.preprocess_text(text)
        
        if not processed_text:
            return 0.0
        
        try:
            text_vector = self.vectorizer.transform([processed_text])
            
            # Get probability if model supports it
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(text_vector)[0]
                # Return probability of being fake
                return probabilities[1] if len(probabilities) > 1 else probabilities[0]
            else:
                # If no probability, return binary prediction
                prediction = self.model.predict(text_vector)[0]
                return float(prediction)
                
        except Exception as e:
            print(f"Error getting confidence: {e}")
            return 0.0
    
    def filter_fake_articles(self, articles, threshold=0.7, max_filter_percentage=50):
        """
        Filter out fake news articles from a list
        
        Args:
            articles (list): List of article dictionaries
            threshold (float): Confidence threshold (0-1) - higher is stricter
            max_filter_percentage (int): Maximum percentage of articles to filter (safety)
            
        Returns:
            tuple: (real_articles, fake_count, filtered_articles)
        """
        if not articles:
            return [], 0, []
        
        real_articles = []
        filtered_articles = []
        fake_count = 0
        
        for article in articles:
            # Combine title and description for analysis
            text = f"{article.get('title', '')} {article.get('description', '')}"
            
            # Check if fake with confidence
            try:
                confidence = self.get_confidence(text)
                is_fake_prediction = self.is_fake(text)
                
                # Only filter if we're confident it's fake
                if is_fake_prediction and confidence >= threshold:
                    fake_count += 1
                    filtered_articles.append(article)
                    print(f"🚫 Filtered fake news (confidence: {confidence:.2f}): {article.get('title', 'Unknown')[:50]}...")
                else:
                    real_articles.append(article)
            except Exception as e:
                # If error, keep the article (benefit of doubt)
                real_articles.append(article)
        
        # Safety check: if we filtered too many, something might be wrong
        total = len(articles)
        filter_rate = (fake_count / total * 100) if total > 0 else 0
        
        if filter_rate > max_filter_percentage:
            print(f"⚠️ Warning: Filtered {filter_rate:.1f}% of articles. Keeping all to avoid over-filtering.")
            return articles, 0, []
        
        return real_articles, fake_count, filtered_articles
