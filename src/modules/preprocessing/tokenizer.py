import os
import re
import json
from typing import List, Dict, Any
from ...utils.distance_metrics import distance, hamming_distance_with_padding
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QHeaderView, QDialog
import phunspell
from PyQt6.QtGui import QIcon


dic_es = phunspell.Phunspell('es_PY')


class Tokenizer:
    def __init__(self, dictionary_path: str = None):
        """
        Inicializa el tokenizador.
        
        Args:
            dictionary_path: Ruta al archivo de diccionario. Si es None, usa el diccionario por defecto.
        """
        self.dictionary_path = dictionary_path or "diccionario/tabla_simbolos.json"
        self.dictionary = self._load_dictionary(self.dictionary_path)
        
    def _load_dictionary(self, dictionary_path: str) -> Dict[str, int]:
        """
        Carga el diccionario de palabras válidas.
        
        Args:
            dictionary_path: Ruta al archivo de diccionario.
            
        Returns:
            Diccionario con palabras y sus puntajes de sentimiento.
        """
        if not os.path.exists(dictionary_path):
            os.makedirs(os.path.dirname(dictionary_path), exist_ok=True)
            with open(dictionary_path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            print(f"Diccionario creado automáticamente en {dictionary_path}")
        try:
            with open(dictionary_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar el diccionario: {e}")
            return {}
            
    def tokenize(self, text: str, parent_widget=None) -> List[Dict[str, Any]]:
        """
        Tokeniza el texto y valida las palabras contra el diccionario.
        Args:
            text: Texto a tokenizar.
            parent_widget: (ya no se usa, solo para compatibilidad)
        Returns:
            Lista de tokens con información de validez y sentimiento.
        """
        # Convertir a minúsculas y tokenizar
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        # Validar palabras y generar tokens
        tokens = []
        for word in words:
            entry = self.dictionary.get(word)
            if entry:
                tokens.append({
                    "lexema": word,
                    "valido": True,
                    "sentiment": entry["puntaje"] if isinstance(entry, dict) and "puntaje" in entry else 0,
                    "token": entry["token"] if isinstance(entry, dict) and "token" in entry else "OTRO",
                    "sugerencias": []
                })
            elif dic_es.lookup(word):
                tokens.append({
                    "lexema": word,
                    "valido": False,
                    "sentiment": 0,
                    "token": "OTRO",
                    "sugerencias": []
                })
            else:
                sugerencias = self._find_suggestions(word)
                tokens.append({
                    "lexema": word,
                    "valido": False,
                    "sentiment": 0,
                    "token": "OTRO",
                    "sugerencias": sugerencias
                })
        return tokens
        
    def _find_suggestions(self, word: str, max_distance: int = 2) -> List[str]:
        """
        Encuentra sugerencias para una palabra basadas en las distancias de Levenshtein y Hamming.
        Primero obtiene sugerencias de phunspell y luego filtra por distancia.
        
        Args:
            word: Palabra para la que buscar sugerencias.
            max_distance: Distancia máxima permitida.
            
        Returns:
            Lista de sugerencias ordenadas por distancia (máximo 3).
        """
        # Obtener sugerencias base de phunspell
        base_suggestions = list(dic_es.suggest(word))
        suggestions = []
        
        # Filtrar usando ambas distancias (Levenshtein y Hamming)
        for dict_word in base_suggestions:
            # Calcular distancia de Levenshtein
            lev_dist = distance(word, dict_word)
            
            # Calcular distancia de Hamming con padding para palabras de diferente longitud
            hamming_dist = hamming_distance_with_padding(word, dict_word)
            
            # Usar la menor de las dos distancias
            min_dist = min(lev_dist, hamming_dist)
            
            if min_dist <= max_distance:
                suggestions.append((dict_word, min_dist, lev_dist, hamming_dist))
        
        # Ordenar por distancia mínima y devolver solo las palabras (máximo 3)
        return [word for word, _, _, _ in sorted(suggestions, key=lambda x: x[1])][:3] 