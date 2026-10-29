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

    def find_all_matches(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Analiza una consulta o pregunta detectada por el copiloto y encuentra
        todas las coincidencias temáticas relevantes dentro de la guía Word oficial.
        Soporta términos individuales técnicos (como 'dynamic', 'B2', 'RTWP') y
        retorna hasta `limit` opciones ordenadas por relevancia con score.
        """
        def _norm(txt: str) -> str:
            if not txt:
                return ""
            txt = txt.lower()
            txt = unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')
            return re.sub(r'[^a-z0-9\s\-_]', ' ', txt)

        q_norm = _norm(query).strip()
        if not q_norm or len(q_norm) < 2:
            return []

        stop_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'de', 'del', 'a', 'al', 'en', 'con',
            'por', 'para', 'que', 'como', 'cual', 'cuales', 'es', 'son', 'fue', 'era', 'tu', 'tus',
            'mi', 'mis', 'su', 'sus', 'me', 'te', 'se', 'nos', 'le', 'les', 'sobre', 'este', 'esta',
            'estos', 'estas', 'the', 'a', 'an', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'about', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
            'does', 'did', 'how', 'what', 'why', 'when', 'where', 'which', 'who', 'tell', 'explain',
            'explica', 'cuentame', 'dime', 'hablame', 'describe', 'sabes', 'conoces', 'experiencia'
        }

        tech_keywords = {
            'moshell': 15, 'amos': 15, 'kpi': 10, 'kpis': 10, 'handover': 15, 'ho': 10,
            'drop': 15, 'drop rate': 18, 'retainability': 12, 'retenibilidad': 12,
            'accessibility': 12, 'accesibilidad': 12, 'mobility': 12, 'movilidad': 12,
            'throughput': 12, 'integridad': 10, 'integrity': 10, 'availability': 10,
            'disponibilidad': 10, 'sleeping': 12, 'dormidas': 12, 'durmientes': 12,
            'carrier aggregation': 18, 'agregacion': 12, 'ca': 10, 'mimo': 14,
            'massive mimo': 18, 'beamforming': 16, 'dss': 16, 'dynamic': 14, 'dynamic spectrum': 18,
            'spectrum': 12, 'espectro': 12,
            'mlb': 16, 'load balancing': 16, 'balanceo': 12, '5g': 10, 'nsa': 14, 'option 3x': 16,
            'opcion 3x': 16, 'endc': 15, 'en-dc': 15, 'sgnb': 16, 'x2': 12, 'prach': 14,
            'pci': 14, 'collision': 14, 'colision': 14, 'confusion': 14, 'rtwp': 18,
            'pim': 18, 'interferencia': 14, 'interference': 14, 'pre-post': 16, 'pre post': 16,
            'star': 12, 'python': 14, 'sql': 14, 'enm': 14, 'oss': 12, 'hardware': 10,
            'bb6630': 15, 'bb5216': 15, 'dus': 12, 'radio 4415': 15, 'radio 2219': 15,
            'air 3264': 15, 'air 6449': 15, 'volte': 12, 'srvcc': 14, 'qci': 10, '5qi': 10,
            'cqi': 12, 'mcs': 12, 'bler': 12, 'prb': 12, 'sinr': 10, 'rsrp': 10, 'rsrq': 10,
            'a1': 12, 'a2': 12, 'a3': 15, 'a4': 12, 'a5': 12, 'b1': 15, 'b2': 15,
            'b4': 12, 'b7': 12, 'b28': 12, 'b66': 12, 'n78': 14, 'n77': 14,
            'vswr': 16, 'rssi': 12, 'anr': 16, 'tilt': 12, 'ret': 12, 'azimuth': 12,
            'trayectoria': 12, 'amdocs': 12, 'metodologia': 10, 'fit': 10, 'desacuerdos': 12,
            'preguntas entrevistador': 14,
            'lms': 20, 'layer management': 18, 'traffic steering': 18, 'spectral efficiency': 16,
            'eficiencia espectral': 16, 'anchor': 16, 'ancla': 16, 'anchor selection': 18,
            'en-dc mobility': 18, 'pscell': 16, 'sgnb addition': 18, 'rs power': 16,
            'reference signal power': 18, 'harq': 16, 'maxharqtx': 16,
            'case 1': 16, 'case 2': 16, 'case 3': 16, 'caso 1': 16, 'caso 2': 16, 'caso 3': 16,
            'recommendations': 14, 'recomendaciones': 14, 'rca': 16, 'root cause': 16, 'causa raiz': 16,
            'prb utilization': 16, 'utilizacion prb': 16, 'pronunciation': 14, 'pronunciacion': 14,
            'transition phrases': 14, 'frases de transicion': 14
        }

        tokens = [w for w in q_norm.split() if w not in stop_words]
        if not tokens:
            tokens = [w for w in q_norm.split() if len(w) > 1]
        if not tokens:
            return []

        is_single_term = len(tokens) == 1
        min_score = 10 if is_single_term else 15

        results = []
        for q in self.all_questions:
            title_norm = _norm(q.title)
            mod_norm = _norm(q.module_title)
            strat_norm = _norm(q.strategy)
            ans_norm = _norm(q.clean_answer_for_teleprompter)
            raw_norm = _norm(q.raw_text)

            score = 0
            matched_kws = []

            # 1. Frase exacta completa si hay más de 1 token
            if len(tokens) > 1 and q_norm in title_norm:
                score += 40
                matched_kws.append(q_norm)
            elif len(tokens) > 1 and (q_norm in strat_norm or q_norm in ans_norm):
                score += 25
                matched_kws.append(q_norm)

            # 2. Análisis por tokens individuales con frontera de palabra para abreviaturas cortas
            for tok in tokens:
                pattern = r'\b' + re.escape(tok) + r'\b' if len(tok) <= 3 else re.escape(tok)
                bonus = tech_keywords.get(tok, 0)

                # Coincidencia en título (peso mayor)
                if re.search(pattern, title_norm):
                    score += 35 + bonus
                    matched_kws.append(tok)
                # Coincidencia en estrategia
                elif re.search(pattern, strat_norm):
                    score += 15 + bonus
                    matched_kws.append(tok)
                # Coincidencia en respuesta principal
                elif re.search(pattern, ans_norm):
                    score += 12 + bonus
                    matched_kws.append(tok)
                # Coincidencia en título del módulo
                elif re.search(pattern, mod_norm):
                    score += 10 + bonus
                    matched_kws.append(tok)
                # Coincidencia en texto en crudo
                elif re.search(pattern, raw_norm):
                    score += 6 + bonus
                    matched_kws.append(tok)

            if score >= min_score:
                mod_num = 1
                for m in self.modules:
                    if any(x.num == q.num for x in m.questions):
                        mod_num = m.num
                        break

                mod_clean = re.sub(r'^M[ÓO]DULO\s+\d+:\s*', '', q.module_title, flags=re.IGNORECASE).strip()
                results.append({
                    "question": q,
                    "q_num": q.num,
                    "module_num": mod_num,
                    "module_title": q.module_title,
                    "module_title_clean": mod_clean,
                    "title": q.title,
                    "short_title": q.short_title,
                    "score": score,
                    "matched_keywords": list(dict.fromkeys(matched_kws))[:4]
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        top_matches = results[:limit]
        # Ordenar de menor a mayor por número de módulo y número de pregunta
        top_matches.sort(key=lambda x: (x.get("module_num", 0), x.get("q_num", 0)))
        return top_matches

    def match_question(self, query: str, min_threshold: int = 15) -> Optional[Dict[str, Any]]:
        """
        Analiza inteligentemente una consulta o pregunta detectada por el copiloto
        y encuentra la mejor coincidencia temática dentro de la guía Word oficial.
        """
        matches = self.find_all_matches(query, limit=1)
        return matches[0] if matches else None

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
