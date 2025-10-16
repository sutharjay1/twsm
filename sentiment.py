from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
from typing import Dict, List, Tuple
import re


class SentimentAnalyzer:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.labels = ['Negative', 'Neutral', 'Positive']
        self._load_model()

    def _load_model(self):
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def preprocess_text(self, text: str) -> str:
        words = []
        for word in text.split(' '):
            if word.startswith('@') and len(word) > 1:
                word = '@user'
            elif word.startswith('http'):
                word = "http"
            words.append(word)
        return " ".join(words)

    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        if not text.strip():
            return {
                "text": text,
                "sentiment": "Neutral",
                "confidence": 0.0,
                "scores": {"Negative": 0.33, "Neutral": 0.34, "Positive": 0.33}
            }

        processed_text = self.preprocess_text(text)
        
        try:
            encoded_text = self.tokenizer(processed_text, return_tensors='pt', truncation=True, max_length=512)
            
            with torch.no_grad():
                output = self.model(**encoded_text)
            
            scores = output.logits[0].detach().numpy()
            scores = softmax(scores)
            
            max_score_index = scores.argmax()
            sentiment_label = self.labels[max_score_index]
            confidence = float(scores[max_score_index])
            
            score_dict = {label: float(score) for label, score in zip(self.labels, scores)}
            
            return {
                "text": text,
                "sentiment": sentiment_label,
                "confidence": confidence,
                "scores": score_dict
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                "text": text,
                "sentiment": "Error",
                "confidence": 0.0,
                "scores": {"Negative": 0.0, "Neutral": 0.0, "Positive": 0.0}
            }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        results = []
        for text in texts:
            result = self.analyze_sentiment(text)
            results.append(result)
        return results

    def get_sentiment_summary(self, texts: List[str]) -> Dict[str, any]:
        results = self.analyze_batch(texts)
        
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        total_confidence = 0
        
        for result in results:
            sentiment = result["sentiment"]
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
            total_confidence += result["confidence"]
        
        total_texts = len(results)
        avg_confidence = total_confidence / total_texts if total_texts > 0 else 0
        
        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        
        return {
            "total_analyzed": total_texts,
            "sentiment_distribution": sentiment_counts,
            "dominant_sentiment": dominant_sentiment,
            "average_confidence": avg_confidence,
            "detailed_results": results
        }
