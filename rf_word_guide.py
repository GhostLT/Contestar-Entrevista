# -*- coding: utf-8 -*-
"""
Gestor de la Guía Maestra de Entrevista RF Optimization (Ericsson 4G/5G)
Permite:
- Cargar y parsear las guías bilingües (Español 10 Módulos / Inglés 11 Módulos).
- Extraer preguntas, estrategias, respuestas modelo, fórmulas y tablas de comandos.
- Búsqueda en tiempo real por palabras clave (RTWP, PIM, A3, VoLTE, Moshell, etc.).
- Lanzar los documentos oficiales en Microsoft Word (.docx) o visor Markdown (.md).
"""

import os
import re
import sys
import subprocess
from typing import List, Dict, Any, Optional, Tuple

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DESKTOP_DIR = os.path.join(os.path.expanduser("~"), "Desktop")

DOCS_PATHS = {
    "es": {
        "md": [
            os.path.join(PROJECT_DIR, "Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.md"),
            os.path.join(DESKTOP_DIR, "Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.md"),
        ],
        "docx": [
            os.path.join(PROJECT_DIR, "Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.docx"),
            os.path.join(DESKTOP_DIR, "Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.docx"),
        ],
    },
    "en": {
        "md": [
            os.path.join(PROJECT_DIR, "Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.md"),
            os.path.join(DESKTOP_DIR, "Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.md"),
        ],
        "docx": [
            os.path.join(PROJECT_DIR, "Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.docx"),
            os.path.join(DESKTOP_DIR, "Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.docx"),
        ],
    }
}


def get_existing_file(candidates: List[str]) -> Optional[str]:
    for path in candidates:
        if os.path.isfile(path):
            return path
    return None


class QuestionItem:
    def __init__(self, q_num: int, title: str, raw_text: str, module_title: str):
        self.num = q_num
        self.title = title.strip()
        self.raw_text = raw_text.strip()
        self.module_title = module_title.strip()
        self.strategy = ""
        self.answer = ""
        self.extra_sections: List[Tuple[str, str]] = []
        self._parse_sections()

    def _parse_sections(self):
        # Extraer subtítulos ####
        parts = re.split(r'\n(?=#### )', self.raw_text)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            lines = part.splitlines()
            header = lines[0].lstrip('#').strip()
            body = "\n".join(lines[1:]).strip()
            
            header_lower = header.lower()
            if "estrategia" in header_lower or "strategy" in header_lower:
                self.strategy = body
            elif "respuesta" in header_lower or "answer" in header_lower or "fórmula" in header_lower or "tabla" in header_lower:
                if not self.answer:
                    self.answer = body
                else:
                    self.extra_sections.append((header, body))
            else:
                self.extra_sections.append((header, body))

    @property
    def short_title(self) -> str:
        # Simplificar título para el árbol o lista
        t = self.title
        # Quitar 'Pregunta X:' o 'Question X:'
        t = re.sub(r'^(Pregunta|Question)\s*\d+:\s*', '', t, flags=re.IGNORECASE)
        t = t.strip('"\'')
        if len(t) > 55:
            return f"Q{self.num}: {t[:52]}..."
        return f"Q{self.num}: {t}"

    @property
    def clean_answer_for_teleprompter(self) -> str:
        # Extraer texto de respuesta sin bloques markdown pesados para leer en voz alta
        ans = self.answer
        if not ans and self.extra_sections:
            ans = "\n\n".join(f"{h}:\n{b}" for h, b in self.extra_sections)
        # Limpiar citas '>'
        lines = []
        for line in ans.splitlines():
            clean_l = re.sub(r'^\s*>\s?', '', line)
            lines.append(clean_l)
        return "\n".join(lines).strip()


class ModuleItem:
    def __init__(self, mod_num: int, title: str, intro_text: str):
        self.num = mod_num
        self.title = title.strip()
        self.intro_text = intro_text.strip()
        self.questions: List[QuestionItem] = []


class RFWordGuide:
    def __init__(self, lang: str = "es"):
        self.lang = lang
        self.header_text: str = ""
        self.modules: List[ModuleItem] = []
        self.all_questions: List[QuestionItem] = []
        self.load(lang)

    def load(self, lang: str = "es"):
        self.lang = lang
        self.modules = []
        self.all_questions = []
        
        md_path = get_existing_file(DOCS_PATHS[lang]["md"])
        if not md_path:
            return

        with open(md_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Separar por módulo (ES: MÓDULO, EN: MODULE)
        module_pattern = r'\n(?=#\s+(?:M[ÓO]DULO|MODULE)\s+\d+:?)'
        chunks = re.split(module_pattern, content, flags=re.IGNORECASE)
        self.header_text = chunks[0].strip()

        mod_counter = 1
        q_global_counter = 1

        for chunk in chunks[1:]:
            lines = chunk.strip().splitlines()
            if not lines:
                continue
            mod_title = lines[0].lstrip('#').strip()
            
            # Separar por pregunta o subsección principal
            # Casos: ### Pregunta X, ### Question X, ### 📊, ### 💻, ### 🎙️, ### 💬
            q_pattern = r'\n(?=###\s+(?:(?:Pregunta|Question)\s+\d+:?|📊|💻|🎙️|💬))'
            q_chunks = re.split(q_pattern, chunk, flags=re.IGNORECASE)
            
            intro = q_chunks[0].strip()
            mod_obj = ModuleItem(mod_counter, mod_title, intro)

            for q_chunk in q_chunks[1:]:
                q_lines = q_chunk.strip().splitlines()
                if not q_lines:
                    continue
                q_title = q_lines[0].lstrip('#').strip()
                
                # Extraer número de pregunta si existe
                m_num = re.search(r'(?:Pregunta|Question)\s*(\d+)', q_title, re.IGNORECASE)
                q_num = int(m_num.group(1)) if m_num else q_global_counter
                
                q_obj = QuestionItem(q_num, q_title, q_chunk, mod_title)
                mod_obj.questions.append(q_obj)
                self.all_questions.append(q_obj)
                q_global_counter += 1

            # Si el módulo no tuvo preguntas ### (por ejemplo Módulo 9 de preguntas al entrevistador),
            # creamos un QuestionItem con el contenido completo del módulo
            if not mod_obj.questions and intro:
                special_q = QuestionItem(q_global_counter, mod_title, chunk, mod_title)
                mod_obj.questions.append(special_q)
                self.all_questions.append(special_q)
                q_global_counter += 1

            self.modules.append(mod_obj)
            mod_counter += 1

    def search(self, query: str) -> List[QuestionItem]:
        q_lower = query.lower().strip()
        if not q_lower:
            return self.all_questions

        results = []
        for q in self.all_questions:
            # Puntuación de relevancia
            score = 0
            if q_lower in q.title.lower():
                score += 10
            if q_lower in q.strategy.lower():
                score += 4
            if q_lower in q.answer.lower():
                score += 5
            if q_lower in q.raw_text.lower():
                score += 2
            
            if score > 0:
                results.append((score, q))

        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results]

    def get_docx_path(self) -> Optional[str]:
        return get_existing_file(DOCS_PATHS[self.lang]["docx"])

    def get_md_path(self) -> Optional[str]:
        return get_existing_file(DOCS_PATHS[self.lang]["md"])

    def open_docx_in_word(self) -> bool:
        path = self.get_docx_path()
        if not path or not os.path.exists(path):
            return False
        try:
            os.startfile(path)
            return True
        except Exception:
            try:
                subprocess.Popen(["cmd", "/c", "start", "", path], shell=True)
                return True
            except Exception:
                return False

    def open_md_in_editor(self) -> bool:
        path = self.get_md_path()
        if not path or not os.path.exists(path):
            return False
        try:
            os.startfile(path)
            return True
        except Exception:
            try:
                subprocess.Popen(["cmd", "/c", "start", "", path], shell=True)
                return True
            except Exception:
                return False
