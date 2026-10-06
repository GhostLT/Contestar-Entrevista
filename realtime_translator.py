"""
Módulo de Traducción en Tiempo Real de Conversaciones (Inglés a Español).
Optimizado para baja latencia (<250ms), sin consumo de cuota de API,
con fallback resiliente a AICopilot (Gemini / DeepSeek).
"""

from typing import Optional, Any
import httpx


def translate_en_to_es(
    text: str,
    source_lang: str = "auto",
    copilot_fallback: Optional[Any] = None
) -> str:
    """
    Traduce texto en tiempo real al español con alta fidelidad y rapidez.
    
    1. Intenta traducción directa de baja latencia mediante endpoint público (sin cuota).
    2. Si ocurre un fallo de conexión, recurre al motor AICopilot configurado.
    """
    cleaned_text = text.strip()
    if not cleaned_text:
        return ""

    # Intentar traducción ultra rápida (<200 ms)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        }
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": "es",
            "dt": "t",
            "q": cleaned_text,
        }
        with httpx.Client(timeout=3.5, headers=headers) as client:
            resp = client.get("https://translate.googleapis.com/translate_a/single", params=params)
            if resp.status_code == 200:
                data = resp.json()
                if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    translated_segments = [
                        segment[0] for segment in data[0]
                        if segment and isinstance(segment, list) and len(segment) > 0 and segment[0]
                    ]
                    translated_result = "".join(translated_segments).strip()
                    if translated_result:
                        return translated_result
    except Exception:
        pass

    # Fallback con el copiloto si está disponible
    if copilot_fallback and hasattr(copilot_fallback, "translate_text_stream"):
        try:
            res = copilot_fallback.translate_text_stream(text=cleaned_text, target_lang="es")
            if res and not res.startswith("❌") and not res.startswith("⚠️"):
                return res.strip()
        except Exception:
            pass

    return cleaned_text
