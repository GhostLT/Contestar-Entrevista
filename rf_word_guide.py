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
import unicodedata
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

    def match_question(self, query: str, min_threshold: int = 15) -> Optional[Dict[str, Any]]:
        """
        Analiza inteligentemente una consulta o pregunta detectada por el copiloto
        y encuentra la mejor coincidencia temática dentro de la guía Word oficial.
        Retorna un diccionario con detalles del módulo, pregunta, score y palabras clave.
        """
        def _norm(txt: str) -> str:
            if not txt:
                return ""
            txt = txt.lower()
            txt = unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')
            return re.sub(r'[^a-z0-9\s\-_]', ' ', txt)

        q_norm = _norm(query)
        stop_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'a', 'al', 'en', 'con',
            'por', 'para', 'que', 'como', 'cual', 'cuales', 'es', 'son', 'fue', 'era', 'tu', 'tus',
            'mi', 'mis', 'su', 'sus', 'me', 'te', 'se', 'nos', 'le', 'les', 'sobre', 'este', 'esta',
            'estos', 'estas', 'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'about', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
            'does', 'did', 'how', 'what', 'why', 'when', 'where', 'which', 'who', 'tell', 'explain',
            'explica', 'cuentame', 'dime', 'hablame', 'describe', 'sabes', 'conoces', 'experiencia'
        }
        q_tokens = [w for w in q_norm.split() if w not in stop_words and len(w) > 1]
        if not q_tokens:
            return None

        tech_keywords = {
            'moshell': 15, 'amos': 15, 'kpi': 10, 'kpis': 10, 'handover': 12, 'ho': 8,
            'drop': 12, 'drop rate': 15, 'retainability': 12, 'retenibilidad': 12,
            'accessibility': 12, 'accesibilidad': 12, 'mobility': 10, 'movilidad': 10,
            'throughput': 12, 'integridad': 10, 'integrity': 10, 'availability': 10,
            'disponibilidad': 10, 'sleeping': 12, 'dormidas': 12, 'durmientes': 12,
            'carrier aggregation': 18, 'agregacion': 12, 'ca': 8, 'mimo': 14,
            'massive mimo': 18, 'beamforming': 16, 'dss': 16, 'dynamic spectrum': 16,
            'mlb': 16, 'load balancing': 16, 'balanceo': 12, '5g': 8, 'nsa': 12, 'option 3x': 16,
            'opcion 3x': 16, 'endc': 15, 'en-dc': 15, 'sgnb': 16, 'x2': 12, 'prach': 12,
            'pci': 14, 'collision': 14, 'colision': 14, 'confusion': 14, 'rtwp': 18,
            'pim': 18, 'interferencia': 12, 'interference': 12, 'pre-post': 16, 'pre post': 16,
            'star': 12, 'python': 14, 'sql': 14, 'enm': 14, 'oss': 12, 'hardware': 10,
            'bb6630': 15, 'bb5216': 15, 'dus': 12, 'radio 4415': 15, 'radio 2219': 15,
            'air 3264': 15, 'air 6449': 15, 'volte': 12, 'srvcc': 14, 'qci': 10, '5qi': 10,
            'cqi': 12, 'mcs': 12, 'bler': 12, 'prb': 12, 'sinr': 10, 'rsrp': 10, 'rsrq': 10,
            'a1': 10, 'a2': 10, 'a3': 14, 'a4': 10, 'a5': 10, 'b1': 14, 'b2': 12,
            'trayectoria': 12, 'amdocs': 12, 'metodologia': 10, 'fit': 10, 'desacuerdos': 12,
            'preguntas entrevistador': 14
        }

        best_q = None
        best_score = 0
        best_reasons = []

        for q in self.all_questions:
            score = 0
            reasons = []

            title_norm = _norm(q.title)
            strat_norm = _norm(q.strategy)
            ans_norm = _norm(q.clean_answer_for_teleprompter)
            raw_norm = _norm(q.raw_text)

            # 1. Coincidencias de palabras clave técnicas con límites de palabra completa
            for kw, weight in tech_keywords.items():
                kw_norm = _norm(kw)
                pattern = r'\b' + re.escape(kw_norm) + r'\b' if len(kw_norm) <= 3 else re.escape(kw_norm)
                if re.search(pattern, q_norm):
                    if re.search(pattern, title_norm):
                        score += weight * 3
                        reasons.append(kw)
                    elif re.search(pattern, strat_norm) or re.search(pattern, ans_norm):
                        score += weight * 2
                        reasons.append(kw)
                    elif re.search(pattern, raw_norm):
                        score += weight
                        reasons.append(kw)

            # 2. Solapamiento de tokens con el título
            title_tokens = set(title_norm.split())
            overlap = set(q_tokens).intersection(title_tokens)
            if overlap:
                score += len(overlap) * 8
                for tok in overlap:
                    if tok not in reasons:
                        reasons.append(tok)

            # 3. Frases exactas de 2 o más palabras
            for length in range(min(4, len(q_tokens)), 1, -1):
                for i in range(len(q_tokens) - length + 1):
                    phrase = " ".join(q_tokens[i:i+length])
                    if phrase in title_norm:
                        score += 25
                        if phrase not in reasons:
                            reasons.append(phrase)
                    elif phrase in strat_norm or phrase in ans_norm:
                        score += 15
                        if phrase not in reasons:
                            reasons.append(phrase)

            if score > best_score:
                best_score = score
                best_q = q
                best_reasons = reasons

        if best_q and best_score >= min_threshold:
            # Encontrar número de módulo
            mod_num = 1
            for m in self.modules:
                if any(x.num == best_q.num for x in m.questions):
                    mod_num = m.num
                    break

            return {
                "question": best_q,
                "q_num": best_q.num,
                "module_num": mod_num,
                "module_title": best_q.module_title,
                "title": best_q.title,
                "short_title": best_q.short_title,
                "score": best_score,
                "matched_keywords": list(dict.fromkeys(best_reasons))[:5]
            }

        return None

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
