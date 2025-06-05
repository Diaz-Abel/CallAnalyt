from typing import Dict, Any, List
from collections import Counter

class SentimentAnalyzer:
    def __init__(self, tokens: List[Dict[str, Any]]):
        """
        Inicializa el analizador de sentimiento.
        
        Args:
            tokens: Lista de tokens con información de sentimiento.
        """
        self.tokens = tokens
        
    def analyze(self) -> Dict[str, Any]:
        """
        Analiza el sentimiento general del texto.
        
        Returns:
            Diccionario con el análisis de sentimiento.
        """
        # Contar palabras positivas y negativas
        positive_words = [t for t in self.tokens if t["sentiment"] > 0]
        negative_words = [t for t in self.tokens if t["sentiment"] < 0]
        
        # Calcular puntuación total
        total_score = sum(t["sentiment"] for t in self.tokens)
        
        # Encontrar palabras más positivas y negativas
        most_positive = max(positive_words, key=lambda x: x["sentiment"]) if positive_words else None
        most_negative = min(negative_words, key=lambda x: x["sentiment"]) if negative_words else None
        
        # Formato seguro para most_positive y most_negative
        most_positive_dict = {"word": most_positive["lexema"], "score": most_positive["sentiment"]} if most_positive else {"word": "", "score": 0}
        most_negative_dict = {"word": most_negative["lexema"], "score": most_negative["sentiment"]} if most_negative else {"word": "", "score": 0}
        
        # Determinar sentimiento general
        if total_score > 0:
            sentiment = "Positivo"
        elif total_score < 0:
            sentiment = "Negativo"
        else:
            sentiment = "Neutral"
            
        return {
            "sentiment": sentiment,
            "score": total_score,
            "positive_words_count": len(positive_words),
            "negative_words_count": len(negative_words),
            "most_positive": most_positive_dict,
            "most_negative": most_negative_dict
        } 