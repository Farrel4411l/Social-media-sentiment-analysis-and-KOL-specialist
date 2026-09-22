# Author: Muhammad Farrel Haidar
# Project: AI PR & KOL Specialist DSS
# Date: 2026-09-22

from textblob import TextBlob
from typing import Dict, Any

class NLPSentimentEngine:
    """
    Mesin NLP untuk mengekstrak opini publik dan mengklasifikasikan sentimen
    dari input raw text. Digunakan di awal pipeline sebelum RAG.
    """
    def __init__(self):
        pass

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Melakukan analisis sentimen menggunakan TextBlob sebagai baseline.
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        # Ekstraksi Pain Points secara sederhana menggunakan Noun Phrases
        # Di environment nyata, bisa diganti dengan Named Entity Recognition (NER) atau Zero-Shot Classification
        pain_points = ", ".join(blob.noun_phrases) if blob.noun_phrases else text
            
        return {
            "original_text": text,
            "sentiment": sentiment,
            "polarity_score": round(polarity, 2),
            "pain_points": pain_points
        }
