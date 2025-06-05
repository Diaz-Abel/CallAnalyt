from typing import Dict, Any, List
import re
import unicodedata

class ProtocolAnalyzer:
    def __init__(self, tokens: List[Dict[str, Any]], utterances: List[Dict[str, Any]]):
        """
        Inicializa el analizador de protocolo.
        
        Args:
            tokens: Lista de tokens del texto.
            utterances: Lista de utterances con información de hablantes.
        """
        self.tokens = tokens
        self.utterances = utterances
        
        # Frases/patrones clave para cada fase
        self.saludo_frases = [
            r"buen[oa]s? (d[ií]as|tardes|noches)",
            r"hola",
            r"bienvenido[ae]?"
        ]
        self.identificacion_frases = [
            r"con qui[eé]n tengo el gusto",
            r"me puede indicar su nombre",
            r"podr[ií]a confirmarme su n[uú]mero de documento",
            r"me indica su n[uú]mero de cliente",
            r"para verificar sus datos",
            r"me podr[ií]a facilitar su identificaci[oó]n",
            r"me podr[ií]a decir su nombre"
        ]
        self.despedida_frases = [
            r"gracias por comunicarse",
            r"gracias por contactarnos",
            r"gracias por su preferencia",
            r"que tenga (un|una)? (buen[oa]?|excelente|gran) (d[ií]a|tarde|noche)",
            r"algo m[aá]s en lo que le pueda (ayudar|asistir)",
            r"fue un placer atenderle",
            r"le deseo (un|una)? (excelente|buen[oa]?|gran) (d[ií]a|tarde|noche)",
            r"hasta luego"
        ]

    def _normalizar(self, texto):
        # Quitar tildes y pasar a minúsculas
        texto = texto.lower()
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto

    def _buscar_frases(self, frases, texto):
        texto_norm = self._normalizar(texto)
        for patron in frases:
            if re.search(patron, texto_norm):
                return True
        return False

    def analyze(self) -> Dict[str, Any]:
        """
        Analiza el cumplimiento del protocolo de atención.
        
        Returns:
            Diccionario con el análisis del protocolo.
        """
        # Obtener utterances del agente
        agent_utterances = [u for u in self.utterances if u.get("speaker") == "A"]
        saludo = any(self._buscar_frases(self.saludo_frases, u["text"]) for u in agent_utterances)
        identificacion = any(self._buscar_frases(self.identificacion_frases, u["text"]) for u in agent_utterances)
        # Despedida amable: solo en los últimos 2 utterances del agente
        despedida = any(self._buscar_frases(self.despedida_frases, u["text"]) for u in agent_utterances[-2:])
        # Palabras prohibidas: sigue usando tokens
        palabras_prohibidas = [t["lexema"] for t in self.tokens if t.get("token") == "PALABRA_PROHIBIDA"]
        return {
            "saludo": {
                "status": "OK" if saludo else "Faltante",
                "found": saludo
            },
            "identificacion": {
                "status": "OK" if identificacion else "Faltante",
                "found": identificacion
            },
            "palabras_prohibidas": {
                "status": "OK" if not palabras_prohibidas else "Detectadas",
                "found": palabras_prohibidas if palabras_prohibidas else ["Ninguna detectada"]
            },
            "despedida": {
                "status": "OK" if despedida else "Faltante",
                "found": despedida
            }
        }
        
    def _check_greeting(self, tokens: List[Dict[str, Any]]) -> bool:
        """Verifica si hay un saludo en los primeros tokens."""
        if not tokens:
            return False
            
        # Buscar en los primeros 5 tokens
        for token in tokens[:5]:
            if token.get("token") == "SALUDO":
                return True
        return False
        
    def _check_identification(self, tokens: List[Dict[str, Any]]) -> bool:
        """Verifica si se pidió identificación al cliente."""
        # Buscar en los primeros 10 tokens
        for token in tokens[:10]:
            if token.get("token") == "IDENTIFICACION":
                return True
        return False
        
    def _check_prohibited_words(self, tokens: List[Dict[str, Any]]) -> List[str]:
        """Verifica si se usaron palabras prohibidas."""
        found_words = []
        for token in tokens:
            if token.get("token") == "PALABRA_PROHIBIDA":
                found_words.append(token["lexema"])
        return found_words
        
    def _check_farewell(self, tokens: List[Dict[str, Any]]) -> bool:
        """Verifica si hay una despedida amable."""
        if not tokens:
            return False
            
        # Buscar en los últimos 5 tokens
        for token in tokens[-5:]:
            if token.get("token") == "DESPEDIDA":
                return True
        return False 