import os
from gtts import gTTS
import tempfile
from pydub import AudioSegment

def crear_audio_tts(archivo_dialogo: str, archivo_salida: str):
    """
    Genera un archivo de audio a partir de un diálogo usando gTTS.
    Usa voz masculina para el agente y femenina para el cliente.
    
    Args:
        archivo_dialogo: Ruta al archivo de diálogo.
        archivo_salida: Ruta donde guardar el archivo de audio.
    """
    # Leer el archivo de diálogo
    with open(archivo_dialogo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # Lista para almacenar los fragmentos de audio
    fragmentos_audio = []

    # Procesar cada línea
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        # Detectar si es agente o cliente
        if linea.startswith('Agente:'):
            texto = linea[7:].strip()  # Quitar "Agente: "
            tld = 'es'  # Voz masculina
        elif linea.startswith('Cliente:'):
            texto = linea[8:].strip()  # Quitar "Cliente: "
            tld = 'com.mx'  # Voz femenina
        else:
            continue

        print(f"Generando audio para: {texto[:30]}...")

        # Crear síntesis de voz
        tts = gTTS(text=texto, lang='es', tld=tld)
        
        # Guardar temporalmente el fragmento
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            tts.save(temp_file.name)
            
            # Cargar el fragmento con pydub
            fragmento = AudioSegment.from_mp3(temp_file.name)
            fragmentos_audio.append(fragmento)
            
            # Agregar una pequeña pausa entre fragmentos
            fragmentos_audio.append(AudioSegment.silent(duration=500))  # 500ms de silencio

        # Limpiar archivo temporal
        os.unlink(temp_file.name)

    # Unir todos los fragmentos
    audio_final = sum(fragmentos_audio)

    # Asegurar que el directorio de salida existe
    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)

    # Guardar el audio final
    audio_final.export(archivo_salida, format="mp3")
    print(f"Audio generado exitosamente en: {archivo_salida}")

if __name__ == "__main__":
    # Obtener el directorio base del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Generar audio para diálogo negativo
    archivo_dialogo = os.path.join(base_dir, "data", "dialogos", "dialogo_negativo.txt")
    archivo_salida = os.path.join(base_dir, "audio", "audio_negativo.mp3")
    crear_audio_tts(archivo_dialogo, archivo_salida)
    
    # Generar audio para diálogo positivo
    archivo_dialogo = os.path.join(base_dir, "data", "dialogos", "dialogo_positivo.txt")
    archivo_salida = os.path.join(base_dir, "audio", "audio_positivo.mp3")
    crear_audio_tts(archivo_dialogo, archivo_salida)
    
    # Generar audio para diálogo neutro
    archivo_dialogo = os.path.join(base_dir, "data", "dialogos", "dialogo_neutro.txt")
    archivo_salida = os.path.join(base_dir, "audio", "audio_neutro.mp3")
    crear_audio_tts(archivo_dialogo, archivo_salida) 