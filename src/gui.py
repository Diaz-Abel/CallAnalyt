import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QFileDialog, QTextEdit, QStackedWidget, QListWidgetItem, QMessageBox, QProgressBar, QDialog, QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QLineEdit, QHeaderView, QSizePolicy, QStyle, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QMovie
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from pydub import AudioSegment
from typing import Dict, Any, List
from datetime import datetime

# Importar los nuevos módulos
from .modules.preprocessing.speech_to_text import SpeechToText
from .modules.preprocessing.tokenizer import Tokenizer as TokenizerBase
from .modules.analysis.sentiment_analyzer import SentimentAnalyzer
from .modules.analysis.protocol_analyzer import ProtocolAnalyzer
from .modules.reporting.report_generator import ReportGenerator

AUDIO_EXTS = [".mp3", ".wav"]
AUDIO_DIR = "../audio/"
OUTPUT_DIR = "../outputs/"

class ProcesamientoThread(QThread):
    progreso = pyqtSignal(int)
    terminado = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, audio_path, parent=None):
        super().__init__()
        self.audio_path = audio_path
        self.parent = parent

    def run(self):
        try:
            # 1. Transcripción y diarización
            self.progreso.emit(10)
            stt = SpeechToText()
            transcripcion = stt.transcribe(self.audio_path)
            self.progreso.emit(40)
            
            # 2. Tokenización
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(transcripcion["text"], self.parent)
            self.progreso.emit(60)
            
            # 3. Análisis de sentimiento
            sentiment_analyzer = SentimentAnalyzer(tokens)
            sentiment_result = sentiment_analyzer.analyze()
            self.progreso.emit(80)
            
            # 4. Análisis de protocolo
            protocol_analyzer = ProtocolAnalyzer(tokens, transcripcion["utterances"])
            protocol_result = protocol_analyzer.analyze()
            
            # 5. Generación de reporte
            report_generator = ReportGenerator(sentiment_result, protocol_result)
            output_dir = os.path.join("outputs", os.path.splitext(os.path.basename(self.audio_path))[0])
            os.makedirs(output_dir, exist_ok=True)
            report_path = os.path.join(output_dir, "reporte.json")
            report_generator.generate_report(report_path)
            
            self.progreso.emit(100)
            self.terminado.emit(self.audio_path)
        except Exception as e:
            self.error.emit(str(e))

class PantallaBienvenida(QWidget):
    archivos_seleccionados = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("")
        self.label = QLabel("CallAnalyt")
        self.label.setObjectName("tituloApp")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icono = QLabel()
        self.icono.setText("📞")
        self.icono.setStyleSheet("font-size: 60px;")
        self.icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitulo = QLabel("Análisis inteligente de llamadas")
        self.subtitulo.setObjectName("subtituloApp")
        self.subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.boton = QPushButton("Seleccionar archivos de audio")
        self.boton.clicked.connect(self.seleccionar_archivos)
        layout.addStretch()
        layout.addWidget(self.icono)
        layout.addWidget(self.label)
        layout.addWidget(self.subtitulo)
        layout.addWidget(self.boton)
        layout.addStretch()
        self.setLayout(layout)

    def seleccionar_archivos(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar audios", AUDIO_DIR, "Archivos de audio (*.mp3 *.wav)")
        if files:
            self.archivos_seleccionados.emit(files)

class PantallaLista(QWidget):
    audio_seleccionado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setStyleSheet("")
        self.btn_volver = QPushButton()
        self.btn_volver.setText("←")
        self.btn_volver.setObjectName("btnVolver")
        self.btn_volver.setIcon(QIcon())
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.clicked.connect(self.volver_bienvenida)
        topbar = QHBoxLayout()
        topbar.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        topbar.addStretch()
        layout.addLayout(topbar)
        self.label = QLabel("Lista de audios")
        self.label.setObjectName("tituloAnalisis")
        self.card = QWidget()
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0,0,0,0)
        self.card.setLayout(card_layout)
        self.card.setStyleSheet("")
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Nombre", "Tipo", "Duración", "Reproducir"])
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabla.cellDoubleClicked.connect(self.abrir_audio)
        self.tabla.cellClicked.connect(self.marcar_audio)
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 120)  # Columna de reproducir más angosta
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setCornerButtonEnabled(False)
        card_layout.addWidget(self.tabla)
        layout.addWidget(self.label)
        layout.addWidget(self.card, stretch=1)
        self.setLayout(layout)
        self.reproductores = {}

    def set_audios(self, audios):
        from os.path import basename, splitext
        self.audios = audios  # Guardar la lista de rutas completas
        self.tabla.setRowCount(len(audios))
        for i, audio in enumerate(audios):
            nombre = basename(audio)
            tipo = splitext(audio)[1][1:].upper()
            try:
                duracion = AudioSegment.from_file(audio).duration_seconds
                minutos = int(duracion // 60)
                segundos = int(duracion % 60)
                duracion_str = f"{minutos}:{segundos:02d} min"
            except Exception:
                duracion_str = "-"
            self.tabla.setItem(i, 0, QTableWidgetItem(nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(tipo))
            self.tabla.setItem(i, 2, QTableWidgetItem(duracion_str))
            reproductor = ReproductorAudio()
            reproductor.set_audio(audio)
            # Centrar el reproductor en la celda
            cell_widget = QWidget()
            cell_layout = QHBoxLayout()
            cell_layout.setContentsMargins(0,0,0,0)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell_layout.addWidget(reproductor)
            cell_widget.setLayout(cell_layout)
            self.tabla.setCellWidget(i, 3, cell_widget)
            self.reproductores[audio] = reproductor
            self.tabla.setRowHeight(i, 44)
        self.tabla.resizeColumnsToContents()

    def cleanup(self):
        for reproductor in self.reproductores.values():
            reproductor.cleanup()
        self.reproductores.clear()

    def abrir_audio(self, row, col):
        if col == 3:
            return
        # Usar la ruta completa guardada en self.audios
        audio_path = self.audios[row]
        self.audio_seleccionado.emit(audio_path)

    def marcar_audio(self, row, col):
        if col == 3:
            return
        self.tabla.selectRow(row)
        self.tabla.setFocus()

    def volver_bienvenida(self):
        self.cleanup()
        if hasattr(self, 'ventana_principal') and self.ventana_principal:
            self.ventana_principal.stacked.setCurrentWidget(self.ventana_principal.pantalla_bienvenida)

class DialogoAsignarPuntaje(QDialog):
    def __init__(self, palabras, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Asignar puntaje a palabras desconocidas")
        self.setMinimumWidth(400)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Asigna un puntaje de -3 a 3 a cada palabra (0 = neutral):"))
        self.tabla = QTableWidget(len(palabras), 2)
        self.tabla.setHorizontalHeaderLabels(["Lexema", "Ponderación"])
        for i, palabra in enumerate(palabras):
            item = QTableWidgetItem(palabra)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tabla.setItem(i, 0, item)
            spin = QSpinBox()
            spin.setRange(-3, 3)
            spin.setValue(0)
            self.tabla.setCellWidget(i, 1, spin)
        layout.addWidget(self.tabla)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar y continuar")
        self.btn_ok.clicked.connect(self.accept)
        btns.addWidget(self.btn_ok)
        layout.addLayout(btns)
        self.setLayout(layout)

    def obtener_puntajes(self):
        resultado = {}
        for i in range(self.tabla.rowCount()):
            palabra = self.tabla.item(i, 0).text()
            puntaje = self.tabla.cellWidget(i, 1).value()
            resultado[palabra] = puntaje
        return resultado

class PantallaResumen(QWidget):
    def __init__(self, resumen, protocolo, on_close, parent=None):
        super().__init__(parent)
        self.on_close = on_close
        layout = QVBoxLayout()
        label_resumen = QLabel()
        label_resumen.setObjectName("resumenDialogo")
        label_resumen.setText(resumen)
        label_resumen.setWordWrap(True)
        label_protocolo = QLabel()
        label_protocolo.setObjectName("protocoloDialogo")
        label_protocolo.setText(protocolo)
        label_protocolo.setWordWrap(True)
        layout.addWidget(QLabel("<b>Sentimiento y palabras clave</b>"))
        layout.addWidget(label_resumen)
        layout.addSpacing(10)
        layout.addWidget(QLabel("<b>Verificación de protocolo</b>"))
        layout.addWidget(label_protocolo)
        btns = QHBoxLayout()
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.cerrar)
        btns.addStretch()
        btns.addWidget(btn_cerrar)
        layout.addLayout(btns)
        self.setLayout(layout)
    def cerrar(self):
        self.on_close()

class PantallaCorreccionLexemas(QWidget):
    def __init__(self, palabras_no_validas, on_finish, ventana_principal, parent=None):
        super().__init__(parent)
        self.on_finish = on_finish
        self.ventana_principal = ventana_principal
        self.palabras_no_validas = palabras_no_validas
        layout = QVBoxLayout()
        # Botón de retroceder
        self.btn_volver = QPushButton()
        self.btn_volver.setText("←")
        self.btn_volver.setObjectName("btnVolver")
        self.btn_volver.setIcon(QIcon())
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.clicked.connect(self.volver_analisis)
        topbar = QHBoxLayout()
        topbar.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        topbar.addStretch()
        layout.addLayout(topbar)
        label = QLabel(
            "Corrige o confirma cada palabra no válida.\n"
            "Puedes elegir una sugerencia o escribir el lexema correcto.\n"
            "También asigna su puntaje (-3 a 3) y su categoría/token:"
        )
        layout.addWidget(label)
        self.tabla = QTableWidget(len(palabras_no_validas), 5)
        self.tabla.setHorizontalHeaderLabels(["¿Válido?", "Lexema", "Sugerencia", "Puntaje", "Token"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        import phunspell
        dic_es = phunspell.Phunspell('es_PY')
        # Opciones de token/categoría
        opciones_token = [
            "SALUDO",
            "IDENTIFICACION",
            "DESPEDIDA",
            "PALABRA_PROHIBIDA",
            "CONSULTA",
            "OTRO"
        ]
        for i, v in enumerate(palabras_no_validas):
            # Columna ¿Válido? (Hunspell)
            valido = dic_es.lookup(v["lexema"])
            valido_item = QTableWidgetItem("Sí" if valido else "No")
            valido_item.setFlags(valido_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tabla.setItem(i, 0, valido_item)
            # Lexema (palabra original)
            item = QTableWidgetItem(v["lexema"])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tabla.setItem(i, 1, item)
            # Sugerencia: QLineEdit solo lectura si es válido, QComboBox editable si no
            if valido:
                from PyQt6.QtWidgets import QLineEdit
                line = QLineEdit(v["lexema"])
                line.setReadOnly(True)
                self.tabla.setCellWidget(i, 2, line)
            else:
                combo = QComboBox()
                combo.setEditable(True)
                combo.addItem(v["lexema"])
                for s in v.get("sugerencias", []):
                    if s != v["lexema"]:
                        combo.addItem(s)
                def wheelEventIgnoreCombo(event, combo=combo):
                    event.ignore()
                combo.wheelEvent = wheelEventIgnoreCombo
                self.tabla.setCellWidget(i, 2, combo)
            spin = QSpinBox()
            spin.setRange(-3, 3)
            spin.setValue(0)
            # Deshabilitar la rueda del ratón en el QSpinBox
            spin.wheelEvent = lambda event: None
            self.tabla.setCellWidget(i, 3, spin)
            # Token/categoría
            combo_token = QComboBox()
            combo_token.addItems(opciones_token)
            # Por defecto seleccionar 'OTRO'
            combo_token.setCurrentText("OTRO")
            # Deshabilitar la rueda del ratón en el QComboBox de token
            def wheelEventIgnoreToken(event, combo=combo_token):
                event.ignore()
            combo_token.wheelEvent = wheelEventIgnoreToken
            self.tabla.setCellWidget(i, 4, combo_token)
        layout.addWidget(self.tabla)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Guardar y continuar")
        self.btn_ok.clicked.connect(self.guardar_y_continuar)
        btns.addWidget(self.btn_ok)
        layout.addLayout(btns)
        self.setLayout(layout)

    def guardar_y_continuar(self):
        resultado = []
        for i in range(self.tabla.rowCount()):
            original = self.tabla.item(i, 1).text()
            # Si es válido, la sugerencia es un QLineEdit, si no, es un QComboBox
            widget = self.tabla.cellWidget(i, 2)
            if hasattr(widget, 'currentText'):
                lexema = widget.currentText().strip()
            else:
                lexema = widget.text().strip()
            puntaje = self.tabla.cellWidget(i, 3).value()
            token = self.tabla.cellWidget(i, 4).currentText().strip()
            resultado.append({"original": original, "lexema": lexema, "puntaje": puntaje, "token": token})
        self.on_finish(resultado)

    def volver_analisis(self):
        self.ventana_principal.stacked.setCurrentWidget(self.ventana_principal.pantalla_analisis)

class PantallaAnalisis(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Barra superior con botón volver
        self.btn_volver = QPushButton()
        self.btn_volver.setText("←")
        self.btn_volver.setObjectName("btnVolver")
        self.btn_volver.setIcon(QIcon())
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.clicked.connect(self.volver_lista)
        topbar = QHBoxLayout()
        topbar.addWidget(self.btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        topbar.addStretch()
        layout.addLayout(topbar)
        
        # Título y reproductor
        self.titulo = QLabel("Análisis de llamada")
        self.titulo.setObjectName("audioNombre")
        
        audio_header = QHBoxLayout()
        self.audio_label = QLabel("")
        self.audio_label.setObjectName("tituloAnalisis")
        self.reproductor = ReproductorAudio()
        audio_header.addWidget(self.audio_label)
        audio_header.addWidget(self.reproductor)
        audio_header.addStretch()
        
        # Etiqueta de procesamiento
        self.processing_label = QLabel("")
        self.processing_label.setStyleSheet("color: #666;")
        
        # Área de texto para la transcripción
        self.text_chat = QTextEdit()
        self.text_chat.setReadOnly(True)
        self.text_chat.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.text_chat.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Botón para ver resumen
        self.btn_ver_resumen = QPushButton("Ver resumen de análisis")
        self.btn_ver_resumen.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.btn_ver_resumen.clicked.connect(self.mostrar_resumen)
        
        # Agregar widgets al layout
        layout.addWidget(self.titulo)
        layout.addLayout(audio_header)
        layout.addWidget(self.processing_label)
        layout.addWidget(self.text_chat, stretch=2)
        
        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(self.btn_ver_resumen)
        layout.addLayout(btns)
        
        self.setLayout(layout)
        self.audio_path = None
        self.ventana_principal = None
        self._resumen = ""
        self._protocolo = ""
        self.processing_thread = None

    def mostrar_analisis(self, audio_path=None, data=None):
        if audio_path:
            self.audio_path = audio_path
            self.audio_label.setText(f"Audio: {os.path.basename(audio_path)}")
            self.reproductor.set_audio(os.path.abspath(audio_path))
            self.processing_label.setText("Procesando audio...")
            self.text_chat.clear()
            
            # Iniciar procesamiento en un hilo separado
            self.processing_thread = ProcesamientoThread(audio_path, self)
            self.processing_thread.progreso.connect(self.actualizar_progreso)
            self.processing_thread.terminado.connect(self.procesamiento_completado)
            self.processing_thread.error.connect(self.mostrar_error)
            self.processing_thread.start()

    def actualizar_progreso(self, val):
        self.processing_label.setText(f"Procesando... {val}%")

    def procesamiento_completado(self, audio_path):
        self.processing_label.setText("")
        try:
            output_dir = os.path.join("outputs", os.path.splitext(os.path.basename(audio_path))[0])
            # Mostrar chat desde transcripcion_assembly.json
            transcripcion_path = os.path.join(output_dir, "transcripcion_assembly.json")
            with open(transcripcion_path, "r", encoding="utf-8") as f:
                transcripcion = json.load(f)
            utterances = transcripcion.get("utterances", [])
            if utterances:
                transcripcion_html = ""
                for utt in utterances:
                    speaker = "Agente" if utt.get("speaker") == "A" else "Cliente"
                    texto = utt.get("text", "")
                    transcripcion_html += f"<div style='margin-bottom: 8px;'><b>{speaker}:</b> {texto}</div>"
                self.text_chat.setHtml(transcripcion_html)
            else:
                self.text_chat.setText("No hay transcripción disponible.")
            # No generar ni mostrar el resumen ni el reporte aquí
            self._resumen = ""
            self._protocolo = ""
        except Exception as e:
            self.text_chat.setText(f"Error al cargar el análisis: {str(e)}")
            self._resumen = "Error al cargar el análisis"
            self._protocolo = "Error al cargar el análisis"

    def mostrar_error(self, msg):
        self.processing_label.setText("")
        QMessageBox.critical(self, "Error", f"Error al procesar audio: {msg}")

    def mostrar_resumen(self, force=False):
        output_dir = os.path.join("outputs", os.path.splitext(os.path.basename(self.audio_path))[0])
        report_path = os.path.join(output_dir, "reporte.json")
        transcripcion_path = os.path.join(output_dir, "transcripcion_assembly.json")
        try:
            # Leer la transcripción para obtener el texto original
            with open(transcripcion_path, "r", encoding="utf-8") as f:
                transcripcion = json.load(f)
            texto = transcripcion.get("text", "")
            utterances = transcripcion.get("utterances", [])
            tokenizer = Tokenizer()
            tokens = tokenizer.tokenize(texto, self)
            palabras_no_validas = [t for t in tokens if not t["valido"]]
            #print("DEBUG palabras_no_validas:", palabras_no_validas)
            if palabras_no_validas and not force:
                # Mostrar pantalla de corrección antes de cualquier análisis
                self.ventana_principal.mostrar_correccion_lexemas(palabras_no_validas, tokens, transcripcion, report_path)
                return
            # Solo aquí se genera el reporte.json
            sentiment_analyzer = SentimentAnalyzer(tokens)
            sentiment_result = sentiment_analyzer.analyze()
            protocol_analyzer = ProtocolAnalyzer(tokens, utterances)
            protocol_result = protocol_analyzer.analyze()
            report_generator = ReportGenerator(sentiment_result, protocol_result)
            report_generator.generate_report(report_path)
            with open(report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            self._resumen = f"""
            <b>Sentimiento general:</b> {report['sentiment_analysis']['sentiment']} ({report['sentiment_analysis']['score']})<br>
            <b>Palabras positivas:</b> {report['sentiment_analysis']['positive_words_count']}<br>
            <b>Palabras negativas:</b> {report['sentiment_analysis']['negative_words_count']}<br>
            """
            if report['sentiment_analysis']['most_positive']['word']:
                self._resumen += f"<b>Palabra más positiva:</b> {report['sentiment_analysis']['most_positive']['word']} ({report['sentiment_analysis']['most_positive']['score']})<br>"
            if report['sentiment_analysis']['most_negative']['word']:
                self._resumen += f"<b>Palabra más negativa:</b> {report['sentiment_analysis']['most_negative']['word']} ({report['sentiment_analysis']['most_negative']['score']})<br>"
            # Protocolo
            prohibited = report['protocol_analysis']['prohibited_words']
            self._protocolo = f"""
            <b>Fase de saludo:</b> {report['protocol_analysis']['greeting']['status']}<br>
            <b>Identificación del cliente:</b> {report['protocol_analysis']['identification']['status']}<br>
            """
            if prohibited['status'] == 'OK' and prohibited['found'] == ["Ninguna detectada"]:
                self._protocolo += f"<b>Uso de palabras prohibidas:</b> Ninguna detectada<br>"
            else:
                self._protocolo += f"<b>Uso de palabras prohibidas:</b> {prohibited['status']}<br>"
                if prohibited['found'] and prohibited['found'] != ["Ninguna detectada"]:
                    self._protocolo += f"<b>Palabras prohibidas encontradas:</b> {', '.join(prohibited['found'])}<br>"
            self._protocolo += f"<b>Despedida amable:</b> {report['protocol_analysis']['farewell']['status']}<br>"
            # Mostrar el resumen como pantalla
            self.ventana_principal.mostrar_resumen(self._resumen, self._protocolo)
        except Exception as e:
            self._resumen = f"Error al cargar el análisis: {str(e)}"
            self._protocolo = "Error al cargar el análisis"
            self.ventana_principal.mostrar_resumen(self._resumen, self._protocolo)

    def volver_lista(self):
        self.reproductor.cleanup()
        if self.ventana_principal:
            self.ventana_principal.stacked.setCurrentWidget(self.ventana_principal.pantalla_lista)

class ReproductorAudio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        style = QApplication.style()
        self.icon_play = style.standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.icon_pause = style.standardIcon(QStyle.StandardPixmap.SP_MediaPause)
        self.icon_stop = style.standardIcon(QStyle.StandardPixmap.SP_MediaStop)
        self.btn_play = QPushButton()
        self.btn_play.setIcon(self.icon_play)
        self.btn_play.setIconSize(QSize(28, 28))
        self.btn_play.setFixedSize(40, 40)
        self.btn_play.setFlat(True)
        self.btn_play.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_play.setStyleSheet("""
            QPushButton {
                background-color: #e3eafc;
                border: none;
                border-radius: 20px;
                margin: 0 2px;
            }
            QPushButton:hover {
                background-color: #bbdefb;
            }
        """)
        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_stop = QPushButton()
        self.btn_stop.setIcon(self.icon_stop)
        self.btn_stop.setIconSize(QSize(28, 28))
        self.btn_stop.setFixedSize(40, 40)
        self.btn_stop.setFlat(True)
        self.btn_stop.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #e3eafc;
                border: none;
                border-radius: 20px;
                margin: 0 2px;
            }
            QPushButton:hover {
                background-color: #bbdefb;
            }
        """)
        self.btn_stop.clicked.connect(self.stop)
        layout.addStretch()
        layout.addWidget(self.btn_play)
        layout.addWidget(self.btn_stop)
        layout.addStretch()
        self.setLayout(layout)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.player.errorOccurred.connect(self.on_error)
        self.audio_path = None
    def set_audio(self, audio_path):
        self.audio_path = audio_path
        if audio_path:
            ruta_abs = os.path.abspath(audio_path)
            if os.path.isfile(ruta_abs):
                self.player.setSource(QUrl.fromLocalFile(ruta_abs))
            else:
                self.player.setSource(QUrl())
        else:
            self.player.setSource(QUrl())
    def toggle_play(self):
        if self.player.source().isEmpty():
            QMessageBox.critical(self, "Error", "No se puede reproducir el audio. Archivo no encontrado o ruta inválida.")
            return
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.btn_play.setIcon(self.icon_play)
        else:
            self.player.play()
            self.btn_play.setIcon(self.icon_pause)
    def stop(self):
        self.player.stop()
        self.btn_play.setIcon(self.icon_play)
    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.btn_play.setIcon(self.icon_play)
    def on_error(self, error, error_string):
        if error != QMediaPlayer.Error.NoError:
            QMessageBox.critical(self, "Error de reproducción", f"No se pudo reproducir el audio: {error_string}")
            self.btn_play.setIcon(self.icon_play)
    def cleanup(self):
        self.player.stop()
        self.player.setSource(QUrl())

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador de Llamadas")
        self.resize(900, 600)
        icon_path = os.path.join(os.path.dirname(__file__), "../data/call_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.stacked = QStackedWidget()
        self.pantalla_bienvenida = PantallaBienvenida()
        self.pantalla_lista = PantallaLista()
        self.pantalla_analisis = PantallaAnalisis()
        self.pantalla_analisis.ventana_principal = self
        self.pantalla_lista.ventana_principal = self
        self.stacked.addWidget(self.pantalla_bienvenida)
        self.stacked.addWidget(self.pantalla_lista)
        self.stacked.addWidget(self.pantalla_analisis)
        layout = QVBoxLayout()
        layout.addWidget(self.stacked)
        self.setLayout(layout)
        # Conexiones
        self.pantalla_bienvenida.archivos_seleccionados.connect(self.cargar_audios)
        self.pantalla_lista.audio_seleccionado.connect(self.mostrar_analisis)
        # Progreso
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.progress.hide()
        self.audios_procesados = []
        self.pantalla_correccion = None
        self.pantalla_resumen = None

    def cargar_audios(self, archivos):
        self.audios_procesados = archivos
        self.pantalla_lista.set_audios(self.audios_procesados)
        self.stacked.setCurrentWidget(self.pantalla_lista)

    def mostrar_analisis(self, audio_path):
        self.pantalla_analisis.mostrar_analisis(audio_path)
        self.stacked.setCurrentWidget(self.pantalla_analisis)

    def mostrar_correccion_lexemas(self, palabras_no_validas, tokens, transcripcion, report_path):
        # Filtrar palabras no válidas para que solo haya lexemas únicos
        lexemas_vistos = set()
        palabras_unicas = []
        for palabra in palabras_no_validas:
            lex = palabra["lexema"]
            if lex not in lexemas_vistos:
                palabras_unicas.append(palabra)
                lexemas_vistos.add(lex)
        def on_finish(correcciones):
            tokenizer = Tokenizer()
            for corr in correcciones:
                tokenizer.dictionary[corr["lexema"]] = {
                    "puntaje": corr["puntaje"],
                    "token": corr["token"]
                }
            with open(tokenizer.dictionary_path, "w", encoding="utf-8") as f:
                json.dump(tokenizer.dictionary, f, ensure_ascii=False, indent=2)
            # Actualizar tokens
            for token in tokens:
                for corr in correcciones:
                    if token["lexema"] == corr["original"]:
                        token["lexema"] = corr["lexema"]
                        token["valido"] = True
                        token["sentiment"] = int(corr["puntaje"])
                        token["token"] = str(corr["token"])
            self.stacked.setCurrentWidget(self.pantalla_analisis)
            self.pantalla_analisis.mostrar_resumen(force=True)
        pantalla_correccion = PantallaCorreccionLexemas(palabras_unicas, on_finish, self)
        pantalla_correccion.setMinimumSize(600, 400)
        self.pantalla_correccion = pantalla_correccion
        for i in range(self.stacked.count()):
            if self.stacked.widget(i) == pantalla_correccion:
                self.stacked.removeWidget(pantalla_correccion)
        self.stacked.addWidget(pantalla_correccion)
        self.stacked.setCurrentWidget(pantalla_correccion)
        self.stacked.update()

    def mostrar_resumen(self, resumen, protocolo):
        def on_close():
            self.stacked.setCurrentWidget(self.pantalla_analisis)
        self.pantalla_resumen = PantallaResumen(resumen, protocolo, on_close, self)
        if self.stacked.indexOf(self.pantalla_resumen) == -1:
            self.stacked.addWidget(self.pantalla_resumen)
        self.stacked.setCurrentWidget(self.pantalla_resumen)

class Tokenizer(TokenizerBase):
    def __init__(self, dictionary_path: str = None):
        super().__init__(dictionary_path or "diccionario/tabla_simbolos.json")

def main():
    app = QApplication(sys.argv)
    # Cargar estilos externos
    try:
        with open(os.path.join(os.path.dirname(__file__), "estilos.qss"), "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"No se pudo cargar el archivo de estilos: {e}")
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 