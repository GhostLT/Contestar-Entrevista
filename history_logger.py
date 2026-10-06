"""
Módulo de Registro y Persistencia de Conversaciones (Logs de Entrevistas).
Guarda automáticamente cada pregunta y su respuesta en archivos Markdown y JSON
para que el candidato pueda repasar las preguntas formuladas después de la reunión.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
import config


# Directorio para guardar el historial
HISTORIAL_DIR = config.BASE_DIR / "historial"


class HistoryLogger:
    """
    Gestiona el guardado automático de preguntas y respuestas de cada entrevista.
    """

    def __init__(self):
        self.historial_dir = HISTORIAL_DIR
        self.historial_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo de sesión individual con fecha y hora de inicio
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_md = self.historial_dir / f"entrevista_{timestamp}.md"
        self.session_json = self.historial_dir / f"entrevista_{timestamp}.json"
        
        self.records = []
        self._init_session_files()

    def _init_session_files(self):
        """Inicializa el encabezado del archivo Markdown de la sesión."""
        if not self.session_md.exists():
            fecha_legible = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            header = f"""# 📝 Registro de Entrevista - {fecha_legible}

Este archivo contiene el historial completo de las preguntas detectadas y las respuestas generadas durante la sesión de entrevista.

---

"""
            self.session_md.write_text(header, encoding="utf-8")

        if not self.session_json.exists():
            self.session_json.write_text("[]", encoding="utf-8")

    def log_interaction(
        self,
        question: str,
        answer: str,
        provider: str = "Gemini",
        original_audio_text: Optional[str] = None
    ):
        """
        Registra una interacción (pregunta + respuesta) tanto en formato Markdown como en JSON.
        """
        question = question.strip()
        answer = answer.strip()

        # No guardar si está vacío o fue ignorado
        if not question or not answer or answer == "[IGNORAR]":
            return

        hora = datetime.now().strftime("%H:%M:%S")

        # 1. Guardar en Markdown legible
        md_entry = f"""### 🕒 [{hora}] Pregunta:
> **"{question}"**
*(Motor: {provider.capitalize()})*

#### ⚡ Respuesta:
{answer}

---

"""
        try:
            with open(self.session_md, "a", encoding="utf-8") as f:
                f.write(md_entry)
        except Exception as e:
            print(f"Error escribiendo en log Markdown: {e}")

        # 2. Guardar en JSON estructurado
        record = {
            "hora": hora,
            "timestamp": datetime.now().isoformat(),
            "pregunta": question,
            "respuesta": answer,
            "proveedor": provider,
            "audio_original": original_audio_text or question
        }
        self.records.append(record)

        try:
            with open(self.session_json, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error escribiendo en log JSON: {e}")

    def get_session_file_path(self) -> Path:
        return self.session_md

    def open_history_folder(self):
        """Abre la carpeta del historial en el explorador de archivos de Windows."""
        try:
            os.startfile(str(self.historial_dir))
        except Exception as e:
            print(f"Error abriendo carpeta de historial: {e}")
