from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
from typing import Dict, List, Tuple, Optional
import re
import numpy as np


class EnhancedSentimentAnalyzer:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.labels = ['Negative', 'Neutral', 'Positive']
        self.financial_keywords = self._load_financial_keywords()
        self._load_model()

    def _load_model(self):
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def _load_financial_keywords(self) -> Dict[str, List[str]]:
        return {
            "positive": [
                "surge", "rally", "gains", "bullish", "upward", "growth", "profit", "earnings",
                "outperform", "beat", "strong", "robust", "recovery", "boom", "soar", "climb",
                "rise", "increase", "advance", "momentum", "optimistic", "confident", "upgrade"
            ],
            "negative": [
                "plunge", "crash", "decline", "bearish", "downward", "loss", "deficit", "miss",
                "underperform", "weak", "fragile", "recession", "slump", "fall", "drop",
                "decrease", "retreat", "pessimistic", "concern", "worry", "downgrade", "risk"
            ],
            "neutral": [
                "stable", "steady", "maintain", "hold", "unchanged", "flat", "sideways",
                "consolidate", "range", "mixed", "moderate", "cautious", "watch", "monitor"
            ]
        }

    def preprocess_text(self, text: str, source: str = None) -> str:
        text = text.strip()
        
        words = []
        for word in text.split(' '):
            if word.startswith('@') and len(word) > 1:
                word = '@user'
            elif word.startswith('http'):
                word = "http"
            words.append(word)
        
        processed_text = " ".join(words)
        
        processed_text = re.sub(r'\s+', ' ', processed_text)
        processed_text = re.sub(r'[^\w\s@#$%.,!?-]', '', processed_text)
        
        return processed_text

    def calculate_financial_bias(self, text: str) -> Dict[str, float]:
        text_lower = text.lower()
        bias_scores = {"positive": 0, "negative": 0, "neutral": 0}
        
        for sentiment, keywords in self.financial_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    bias_scores[sentiment] += 1
        
        total_keywords = sum(bias_scores.values())
        if total_keywords > 0:
            for sentiment in bias_scores:
                bias_scores[sentiment] = bias_scores[sentiment] / total_keywords
        else:
            bias_scores = {"positive": 0.33, "negative": 0.33, "neutral": 0.34}
        
        return bias_scores

    def analyze_sentiment(self, text: str, source: str = None) -> Dict[str, any]:
        if not text.strip():
            return {
                "text": text,
                "sentiment": "Neutral",
                "confidence": 0.0,
                "scores": {"Negative": 0.33, "Neutral": 0.34, "Positive": 0.33},
                "financial_bias": {"positive": 0.33, "negative": 0.33, "neutral": 0.34},
                "source": source
            }

        processed_text = self.preprocess_text(text, source)
        financial_bias = self.calculate_financial_bias(text)
        
        try:
            encoded_text = self.tokenizer(processed_text, return_tensors='pt', truncation=True, max_length=512)
            
            with torch.no_grad():
                output = self.model(**encoded_text)
            
            scores = output.logits[0].detach().numpy()
            scores = softmax(scores)
            
            financial_weight = 0.3
            adjusted_scores = np.array([
                scores[0] * (1 - financial_weight) + financial_bias["negative"] * financial_weight,
                scores[1] * (1 - financial_weight) + financial_bias["neutral"] * financial_weight,
                scores[2] * (1 - financial_weight) + financial_bias["positive"] * financial_weight
            ])
            
            max_score_index = adjusted_scores.argmax()
            sentiment_label = self.labels[max_score_index]
            confidence = float(adjusted_scores[max_score_index])
            
            score_dict = {label: float(score) for label, score in zip(self.labels, adjusted_scores)}
            
            return {
                "text": text,
                "sentiment": sentiment_label,
                "confidence": confidence,
                "scores": score_dict,
                "financial_bias": financial_bias,
                "source": source,
                "raw_scores": {label: float(score) for label, score in zip(self.labels, scores)}
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {
                "text": text,
                "sentiment": "Error",
                "confidence": 0.0,
                "scores": {"Negative": 0.0, "Neutral": 0.0, "Positive": 0.0},
                "financial_bias": financial_bias,
                "source": source
            }

    def analyze_batch(self, texts: List[str], sources: List[str] = None) -> List[Dict[str, any]]:
        if sources is None:
            sources = [None] * len(texts)
        
        results = []
        for text, source in zip(texts, sources):
            result = self.analyze_sentiment(text, source)
            results.append(result)
        return results

    def get_sentiment_summary(self, texts: List[str], sources: List[str] = None) -> Dict[str, any]:
        results = self.analyze_batch(texts, sources)
        
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        source_sentiment = {}
        total_confidence = 0
        financial_bias_totals = {"positive": 0, "negative": 0, "neutral": 0}
        
        for result in results:
            sentiment = result["sentiment"]
            source = result.get("source", "unknown")
            
            if sentiment in sentiment_counts:
                sentiment_counts[sentiment] += 1
            
            if source not in source_sentiment:
                source_sentiment[source] = {"Positive": 0, "Neutral": 0, "Negative": 0, "total": 0}
            
            if sentiment in source_sentiment[source]:
                source_sentiment[source][sentiment] += 1
            source_sentiment[source]["total"] += 1
            
            total_confidence += result["confidence"]
            
            if "financial_bias" in result:
                for bias_type, value in result["financial_bias"].items():
                    financial_bias_totals[bias_type] += value
        
        total_texts = len(results)
        avg_confidence = total_confidence / total_texts if total_texts > 0 else 0
        
        for bias_type in financial_bias_totals:
            financial_bias_totals[bias_type] /= total_texts if total_texts > 0 else 1
        
        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        
        market_outlook = self._determine_market_outlook(sentiment_counts, financial_bias_totals)
        
        return {
            "total_analyzed": total_texts,
            "sentiment_distribution": sentiment_counts,
            "source_breakdown": source_sentiment,
            "dominant_sentiment": dominant_sentiment,
            "average_confidence": avg_confidence,
            "financial_bias_summary": financial_bias_totals,
            "market_outlook": market_outlook,
            "detailed_results": results
        }

    def _determine_market_outlook(self, sentiment_counts: Dict, financial_bias: Dict) -> Dict[str, str]:
        total = sum(sentiment_counts.values())
        if total == 0:
            return {"outlook": "Unknown", "confidence": "Low", "description": "No data available"}
        
        positive_ratio = sentiment_counts["Positive"] / total
        negative_ratio = sentiment_counts["Negative"] / total
        
        financial_positive = financial_bias.get("positive", 0)
        financial_negative = financial_bias.get("negative", 0)
        
        combined_positive = (positive_ratio + financial_positive) / 2
        combined_negative = (negative_ratio + financial_negative) / 2
        
        if combined_positive > 0.6:
            outlook = "Strongly Bullish"
            confidence = "High"
            description = "Strong positive sentiment across sources"
        elif combined_positive > 0.4:
            outlook = "Bullish"
            confidence = "Medium"
            description = "Generally positive market sentiment"
        elif combined_negative > 0.6:
            outlook = "Strongly Bearish"
            confidence = "High"
            description = "Strong negative sentiment across sources"
        elif combined_negative > 0.4:
            outlook = "Bearish"
            confidence = "Medium"
            description = "Generally negative market sentiment"
        else:
            outlook = "Mixed/Neutral"
            confidence = "Medium"
            description = "Balanced sentiment with no clear direction"
        
        return {
            "outlook": outlook,
            "confidence": confidence,
            "description": description,
            "positive_ratio": combined_positive,
            "negative_ratio": combined_negative
        }

    def get_source_comparison(self, multi_source_data: Dict) -> Dict[str, any]:
        source_analyses = {}
        
        for source, data in multi_source_data.items():
            if "data" in data and isinstance(data["data"], dict):
                headlines = data["data"].get("headlines", [])
                stock_news = data["data"].get("stock_news", [])
                all_texts = headlines + stock_news
                
                if all_texts:
                    source_summary = self.get_sentiment_summary(all_texts, [source] * len(all_texts))
                    source_analyses[source] = {
                        "sentiment_summary": source_summary,
                        "article_count": len(all_texts),
                        "dominant_sentiment": source_summary["dominant_sentiment"],
                        "confidence": source_summary["average_confidence"],
                        "market_outlook": source_summary["market_outlook"]
                    }
        
        return {
            "source_analyses": source_analyses,
            "comparison_summary": self._create_source_comparison_summary(source_analyses)
        }

    def _create_source_comparison_summary(self, source_analyses: Dict) -> Dict:
        if not source_analyses:
            return {"message": "No source data available for comparison"}
        
        most_bullish = max(source_analyses.items(), 
                          key=lambda x: x[1]["sentiment_summary"]["sentiment_distribution"]["Positive"])
        most_bearish = max(source_analyses.items(), 
                          key=lambda x: x[1]["sentiment_summary"]["sentiment_distribution"]["Negative"])
        highest_confidence = max(source_analyses.items(), 
                               key=lambda x: x[1]["confidence"])
        
        return {
            "most_bullish_source": {
                "source": most_bullish[0],
                "positive_count": most_bullish[1]["sentiment_summary"]["sentiment_distribution"]["Positive"],
                "outlook": most_bullish[1]["market_outlook"]["outlook"]
            },
            "most_bearish_source": {
                "source": most_bearish[0],
                "negative_count": most_bearish[1]["sentiment_summary"]["sentiment_distribution"]["Negative"],
                "outlook": most_bearish[1]["market_outlook"]["outlook"]
            },
            "highest_confidence_source": {
                "source": highest_confidence[0],
                "confidence": highest_confidence[1]["confidence"],
                "article_count": highest_confidence[1]["article_count"]
            },
            "total_sources": len(source_analyses)
        }
