import assemblyai as aai
import json
import os
import sys
from typing import Dict, Any

# Agregar la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from credentials.config import ASSEMBLY_API_KEY

class SpeechToText:
    def __init__(self, api_key: str = None):
        """
        Inicializa el convertidor de voz a texto usando AssemblyAI.
        
        Args:
            api_key: Clave API de AssemblyAI. Si es None, usa la clave por defecto.
        """
        self.api_key = api_key or ASSEMBLY_API_KEY
        aai.settings.api_key = self.api_key
        
    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe y diariza un archivo de audio.
        
        Args:
            audio_path: Ruta al archivo de audio.
            
        Returns:
            Diccionario con la transcripción y diarización.
        """
        # Configurar directorio de salida
        outdir = os.path.join("outputs", os.path.splitext(os.path.basename(audio_path))[0])
        os.makedirs(outdir, exist_ok=True)
        outpath = os.path.join(outdir, "transcripcion_assembly.json")
        
        # Verificar si ya existe la transcripción
        if os.path.exists(outpath):
            print(f"Usando transcripción existente de: {outpath}")
            with open(outpath, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # Configurar transcripción en español con diarización
        config = aai.TranscriptionConfig(
            speaker_labels=True,
            language_code="es"
        )
        
        # Transcribir
        print(f"Iniciando transcripción de: {audio_path}")
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_path)
        
        # Extraer solo la información necesaria
        json_data = transcript.json_response
        resultado = {
            "text": json_data.get("text"),
            "utterances": json_data.get("utterances")
        }
        
        # Guardar resultado
        print(f"Guardando transcripción en: {outpath}")
        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        
        return resultado 