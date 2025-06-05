from typing import Dict, Any
import json
import os

class ReportGenerator:
    def __init__(self, sentiment_analysis: Dict[str, Any], protocol_analysis: Dict[str, Any]):
        """
        Inicializa el generador de reportes.
        
        Args:
            sentiment_analysis: Resultado del análisis de sentimiento.
            protocol_analysis: Resultado del análisis de protocolo.
        """
        self.sentiment_analysis = sentiment_analysis
        self.protocol_analysis = protocol_analysis
        
    def generate_report(self, output_path: str = None) -> Dict[str, Any]:
        """
        Genera un reporte completo del análisis.
        
        Args:
            output_path: Ruta donde guardar el reporte. Si es None, no se guarda.
            
        Returns:
            Diccionario con el reporte completo.
        """
        report = {
            "sentiment_analysis": {
                "sentiment": self.sentiment_analysis["sentiment"],
                "score": self.sentiment_analysis["score"],
                "positive_words_count": self.sentiment_analysis["positive_words_count"],
                "negative_words_count": self.sentiment_analysis["negative_words_count"],
                "most_positive": self.sentiment_analysis["most_positive"],
                "most_negative": self.sentiment_analysis["most_negative"]
            },
            "protocol_analysis": {
                "greeting": self.protocol_analysis["saludo"],
                "identification": self.protocol_analysis["identificacion"],
                "prohibited_words": self.protocol_analysis["palabras_prohibidas"],
                "farewell": self.protocol_analysis["despedida"]
            }
        }
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
                
        return report
        
    def print_report(self):
        """Imprime el reporte en formato legible."""
        print("\n=== ANÁLISIS DE SENTIMIENTO ===")
        print(f"Sentimiento general: {self.sentiment_analysis['sentiment']} ({self.sentiment_analysis['score']})")
        print(f"Palabras positivas: {self.sentiment_analysis['positive_words_count']}")
        print(f"Palabras negativas: {self.sentiment_analysis['negative_words_count']}")
        
        if self.sentiment_analysis['most_positive']:
            print(f"Palabra más positiva: {self.sentiment_analysis['most_positive']} ({self.sentiment_analysis['positive_score']})")
        if self.sentiment_analysis['most_negative']:
            print(f"Palabra más negativa: {self.sentiment_analysis['most_negative']} ({self.sentiment_analysis['negative_score']})")
            
        print("\n=== ANÁLISIS DE PROTOCOLO ===")
        print(f"Fase de saludo: {self.protocol_analysis['saludo']['status']}")
        print(f"Identificación del cliente: {self.protocol_analysis['identificacion']['status']}")
        print(f"Uso de palabras prohibidas: {self.protocol_analysis['palabras_prohibidas']['status']}")
        if self.protocol_analysis['palabras_prohibidas']['found']:
            print(f"Palabras prohibidas encontradas: {', '.join(self.protocol_analysis['palabras_prohibidas']['found'])}")
        print(f"Despedida amable: {self.protocol_analysis['despedida']['status']}") 