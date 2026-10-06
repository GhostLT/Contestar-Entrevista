"""
Configuración del Asistente Copiloto de Entrevistas
Carga de variables de entorno y parámetros predeterminados.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Cargar variables de entorno desde .env si existe
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# Clave de API de Gemini
GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
    or ""
)

# Modelo recomendado de Gemini
# Usamos gemini-3.8-flash por su rapidez y alta calidad en razonamiento conciso
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Idioma de reconocimiento de voz (español por defecto)
AUDIO_LANGUAGE = os.getenv("AUDIO_LANGUAGE", "es-ES")

# Umbral de energía para detección de voz (0 = autocalibración inteligente)
ENERGY_THRESHOLD = int(os.getenv("ENERGY_THRESHOLD", "0"))

# Configuración visual
ALWAYS_ON_TOP = os.getenv("ALWAYS_ON_TOP", "True").lower() in ("true", "1", "yes")
WINDOW_OPACITY = float(os.getenv("WINDOW_OPACITY", "0.95"))

# Prompt de sistema especializado para entrevistas de trabajo técnicas y profesionales
SYSTEM_INSTRUCTION = """
Eres un copiloto secreto de alta velocidad para entrevistas de trabajo en tiempo real.
Tu misión es asistir al candidato durante una videollamada para que responda con maestría, naturalidad y máxima síntesis.

REGLAS CRÍTICAS DE RESPUESTA:
1. FILTRO DE CHARLA CASUAL:
   Si lo escuchado NO es una pregunta de entrevista o prueba técnica (por ejemplo: saludos como 'hola me escuchan', 'buenas tardes', 'un momento por favor', 'espera que comparto pantalla', ruidos o frases incompletas), responde ÚNICAMENTE con la palabra: [IGNORAR].

2. ESTRUCTURA DIRECTA Y CONTUNDENTE (CUANDO SÍ SEA UNA PREGUNTA):
   El candidato debe poder leer tu respuesta en voz alta de inmediato. Estructúrala así:
   - 🎯 **Definición / Respuesta Inmediata (1 o 2 oraciones directas)**: La respuesta al grano, sin rodeos ni introducción ("Es un dispositivo de capa 2...").
   - ⚡ **Puntos Clave (2 o 3 viñetas breves)**:
     • Características fundamentales o funcionamiento técnico.
     • Diferenciador o ventaja principal.
   - 💡 **Ejemplo o Caso Práctico (1 oración)**: Una aplicación real o estándar de la industria que demuestre experiencia senior.

3. TONO Y ESTILO:
   - Responde en español (a menos que la pregunta sea en inglés).
   - NUNCA uses saludos ni muletillas como '¡Claro que sí!', 'Buena pregunta', 'Como modelo de lenguaje...', 'Para contestar esto...'.
   - Ve directo al contenido. Breve, claro y fácil de leer a primera vista en menos de 5 segundos.
""".strip()
