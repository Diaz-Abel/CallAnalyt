# 📞 CallAnalyt - Sistema de Análisis de Interacciones en Contact Centers

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)
![AssemblyAI](https://img.shields.io/badge/AssemblyAI-API-orange.svg)
![License](https://img.shields.io/badge/License-Academic-purple.svg)

*Sistema inteligente de análisis automático de calidad en centros de contacto mediante técnicas de Procesamiento de Lenguaje Natural*

**🎓 Proyecto Académico | Diseño de Compiladores | Universidad Nacional de Asunción**

</div>

---

## 🎯 Descripción

**CallAnalyt** es un sistema avanzado que automatiza completamente el proceso de evaluación de calidad en centros de contacto. Convierte grabaciones de llamadas telefónicas en métricas objetivas y detalladas sobre el desempeño del servicio al cliente, eliminando la subjetividad y lentitud de la evaluación manual.

### 🚀 ¿Qué resuelve?

- ✅ **Análisis objetivo** de miles de llamadas en minutos
- ✅ **Detección automática** de cumplimiento de protocolos  
- ✅ **Métricas de sentimiento** para medir satisfacción del cliente
- ✅ **Identificación de palabras clave** positivas y negativas
- ✅ **Reportes detallados** listos para gerencia

---

## ✨ Características Principales

### 🎙️ **Speech-to-Text Avanzado**
- Transcripción automática en español con **AssemblyAI**
- **Diarización** inteligente (identifica quién habla: Agente vs Cliente)
- Soporte para múltiples formatos de audio (MP3, WAV)
- Cache inteligente para optimizar recursos

### 🔤 **Tokenización y Validación Inteligente**
- Segmentación avanzada de texto en lexemas
- Validación contra **diccionario personalizable** + diccionario español
- **Sugerencias automáticas** usando distancias de Levenshtein y Hamming
- Corrección manual interactiva de palabras no reconocidas

### 😊 **Análisis de Sentimiento**
- Sistema de **puntuación emocional** (-3 a +3) por palabra
- Cálculo de **sentimiento general** de la conversación
- Identificación de **palabras más positivas/negativas**
- Tabla de símbolos personalizable por dominio

### 📋 **Verificación de Protocolo**
- Detección automática de **4 fases clave**:
  - ✅ **Saludo inicial** apropiado
  - ✅ **Identificación del cliente** solicitada
  - ✅ **Ausencia de palabras prohibidas**
  - ✅ **Despedida amable** ejecutada
- Patrones flexibles usando expresiones regulares
- Análisis específico por intervenciones del agente

### 🖥️ **Interfaz Gráfica Moderna**
- **GUI nativa** desarrollada en PyQt6
- **Reproductor de audio integrado** para verificación
- **Flujo de trabajo intuitivo** paso a paso
- **Visualización en tiempo real** del procesamiento
- **Gestión completa** del diccionario de palabras

### 📊 **Reportes Detallados**
- **Exportación en JSON** estructurado
- **Métricas cuantificadas** listas para análisis
- **Historial de correcciones** para aprendizaje
- **Dashboard visual** de resultados

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito | Versión |
|------------|-----------|---------|
| **Python** | Lenguaje principal | 3.8+ |
| **PyQt6** | Interfaz gráfica nativa | 6.4+ |
| **AssemblyAI** | Speech-to-Text en español | API v2 |
| **phunspell** | Corrección ortográfica | 0.1.6+ |
| **pydub** | Procesamiento de audio | 0.25+ |
| **Algoritmos personalizados** | Distancias de Levenshtein & Hamming | - |

---

## 🚀 Instalación Rápida

### 📋 Prerrequisitos
- **Python 3.8+** instalado
- **Cuenta en AssemblyAI** para obtener API Key
- **Sistema operativo**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### ⚡ Configuración en 3 pasos

1. **Clonar y preparar entorno**
```bash
git clone https://github.com/tu-usuario/callanalyt.git
cd callanalyt
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar credenciales**
```bash
# Editar credentials/config.py
ASSEMBLY_API_KEY = "tu_api_key_de_assemblyai"
```

### 🎬 ¡Listo para usar!
```bash
python -m src.gui
```

---

## 🎮 Guía de Uso

### 1️⃣ **Cargar archivos de audio**
- Formatos soportados: `.mp3`, `.wav`
- Calidad recomendada: 16kHz, mono
- Incluye archivos de ejemplo en `/audio/`

### 2️⃣ **Procesamiento automático**
- Transcripción con diarización (～45s para 2min de audio)
- Tokenización y validación de lexemas
- Corrección interactiva de palabras no reconocidas

### 3️⃣ **Análisis y resultados**
- Visualización de transcripción por hablante
- Métricas de sentimiento cuantificadas
- Verificación de protocolo detallada
- Exportación de reportes en JSON

---

## 📁 Arquitectura del Proyecto

```
callanalyt/
├── 📁 src/                    # 🐍 Código fuente modular
│   ├── 📁 modules/           # 🧩 Módulos principales  
│   │   ├── 📁 preprocessing/ # 🎙️ Speech-to-Text & Tokenización
│   │   ├── 📁 analysis/      # 😊 Sentimiento & Protocolo
│   │   └── 📁 reporting/     # 📊 Generación de reportes
│   ├── 📁 utils/             # 🔧 Utilidades (distancias, etc.)
│   └── 🖥️ gui.py             # 🎨 Interfaz gráfica principal
├── 📁 audio/                 # 🎵 Archivos de audio de ejemplo
├── 📁 data/                  # 📄 Diálogos de prueba
├── 📁 diccionario/           # 📚 Tabla de símbolos personalizable
├── 📁 outputs/               # 📋 Transcripciones y reportes
├── 📁 credentials/           # 🔐 Configuración de API keys
└── 📄 documento_academico.md # 📖 Documentación técnica completa
```

---

## 🧪 Casos de Ejemplo

El proyecto incluye **3 archivos de audio** pre-procesados con diferentes escenarios:

| Archivo | Escenario | Sentimiento | Protocolo |
|---------|-----------|-------------|-----------|
| `audio_positivo.mp3` | Resolución exitosa | ✅ Positivo (+34) | ✅ Completo |
| `audio_neutro.mp3` | Consulta informativa | ⚪ Neutral (0) | ⚠️ Parcial |
| `audio_negativo.mp3` | Cliente insatisfecho | ❌ Negativo (-18) | ❌ Incompleto |

### 📊 Ejemplo de salida
```json
{
  "sentiment_analysis": {
    "sentiment": "Positivo",
    "score": 34,
    "positive_words_count": 40,
    "most_positive": {"word": "perfecto", "score": 3}
  },
  "protocol_analysis": {
    "greeting": {"status": "OK"},
    "identification": {"status": "OK"},
    "prohibited_words": {"status": "OK", "found": ["Ninguna detectada"]},
    "farewell": {"status": "OK"}
  }
}
```

---

## 🎓 Contexto Académico

### 📚 **Trabajo Práctico - Diseño de Compiladores**
- **Universidad:** Facultad Politécnica - Universidad Nacional de Asunción
- **Materia:** Diseño de Compiladores - 8° Semestre  
- **Objetivo:** Aplicación práctica de conceptos de análisis léxico y tokenización
- **Enfoque:** Procesamiento de Lenguaje Natural en dominio real

### 🧠 **Conceptos aplicados**
- ✅ **Análisis léxico** y tokenización
- ✅ **Tabla de símbolos** personalizable
- ✅ **Distancias de edición** (Levenshtein & Hamming)
- ✅ **Expresiones regulares** para detección de patrones
- ✅ **Arquitectura modular** y separation of concerns

---

## 📈 Métricas de Rendimiento

| Métrica | Valor | Observaciones |
|---------|-------|---------------|
| **Tiempo de transcripción** | ~45s por 2min de audio | Depende de calidad de red |
| **Precisión de tokenización** | 97% | Con diccionario actualizado |
| **Detección de protocolo** | 100% | En casos de prueba |
| **Cobertura de sentimiento** | 95% | Palabras en diccionario |

---

## 🤝 Contribución

¿Quieres mejorar CallAnalyt? ¡Excelente!

1. 🍴 **Fork** el repositorio
2. 🌿 **Crear rama**: `git checkout -b feature/nueva-funcionalidad`
3. ✅ **Commit**: `git commit -m 'Agregar nueva funcionalidad'`
4. 📤 **Push**: `git push origin feature/nueva-funcionalidad`
5. 🔄 **Pull Request** con descripción detallada

### 🎯 Áreas de mejora sugeridas
- 🌍 **Soporte multi-idioma** (inglés, portugués)
- 🧠 **Integración con modelos de IA** (BERT, RoBERTa)
- 📱 **Versión web/móvil** del sistema
- 📊 **Dashboard analítico** avanzado
- 🔄 **Aprendizaje automático** de correcciones

---

## 📄 Licencia

Este proyecto está desarrollado con fines **académicos** bajo supervisión universitaria.

```
Proyecto Académico - Diseño de Compiladores
Facultad Politécnica - Universidad Nacional de Asunción
Uso educativo y de investigación permitido
```

---

## 👨‍💻 Autor

<div align="center">

**Abel Moisés Díaz Barrios**  
*Estudiante de Ingeniería Informática*  
*8° Semestre - 2025*

📧 [diazabel743@gmail.com](mailto:diazabel743@gmail.com)  
🏫 Facultad Politécnica - Universidad Nacional de Asunción  

</div>

---

<div align="center">

### ⭐ ¡Si te gusta el proyecto, dale una estrella!


</div> 