"""
Módulo de Integración con Google Gemini 3.8 Flash
Diseñado para generar respuestas ultra-rápidas, breves y de alto impacto
para entrevistas de trabajo en tiempo real.
"""

from typing import Callable, Optional, Generator
from google import genai
from google.genai import types
import config


class GeminiCopilot:
    """
    Cliente de Gemini optimizado para respuestas en vivo durante entrevistas.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.model = model or config.GEMINI_MODEL
        self.client: Optional[genai.Client] = None
        self._init_client()

    def _init_client(self):
        if self.api_key and self.api_key != "tu_clave_de_gemini_aqui":
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Error inicializando cliente Gemini: {e}")
                self.client = None
        else:
            self.client = None

    def set_api_key(self, new_key: str):
        self.api_key = new_key.strip()
        self._init_client()

    def is_configured(self) -> bool:
        if self.client is None or not self.api_key or self.api_key == "tu_clave_de_gemini_aqui":
            # Recargar automáticamente desde .env si fue modificado
            try:
                import os
                from dotenv import load_dotenv
                env_file = config.BASE_DIR / ".env"
                if env_file.exists():
                    load_dotenv(dotenv_path=env_file, override=True)
                    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
                    if key and key != "tu_clave_de_gemini_aqui":
                        self.set_api_key(key)
            except Exception as e:
                print(f"Error recargando .env: {e}")

        return self.client is not None and bool(self.api_key) and self.api_key != "tu_clave_de_gemini_aqui"

    def answer_question_stream(
        self,
        question: str,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Envía la pregunta a Gemini 3.8 Flash con streaming token a token.
        Si la respuesta es [IGNORAR], la descarta automáticamente.
        """
        if not self.is_configured():
            err_msg = "⚠️ Falta la API Key de Gemini. Configúrala en el archivo .env o en la aplicación."
            if on_error:
                on_error(err_msg)
            return err_msg

        full_text = ""
        is_ignorable = False

        prompt = f"Pregunta o intervención del entrevistador:\n\"{question}\""

        try:
            config_params = types.GenerateContentConfig(
                system_instruction=config.SYSTEM_INSTRUCTION,
                temperature=0.25,  # Baja temperatura para respuestas directas y precisas
                max_output_tokens=500,
            )

            response_stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config=config_params,
            )

            for chunk in response_stream:
                if chunk.text:
                    full_text += chunk.text
                    
                    # Si el modelo determinó que debe ignorarse la frase casual
                    if "[IGNORAR]" in full_text:
                        is_ignorable = True
                        break

                    if on_chunk:
                        on_chunk(chunk.text)

            if is_ignorable:
                return "[IGNORAR]"

            if on_complete:
                on_complete(full_text)

            return full_text

        except Exception as e:
            error_str = str(e)
            if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
                msg = "❌ Error: La API Key de Gemini no es válida. Por favor revísala en https://aistudio.google.com/"
            elif "RESOURCE_EXHAUSTED" in error_str:
                msg = "⚠️ Límite de cuota excedido temporalmente en Gemini. Intenta en unos segundos."
            else:
                msg = f"❌ Error conectando con Gemini: {error_str}"

            if on_error:
                on_error(msg)
            return msg

    def answer_question(self, question: str) -> str:
        """Versión sincrónica sin callbacks."""
        result = []
        def _collect(chunk):
            result.append(chunk)
        self.answer_question_stream(question, on_chunk=_collect)
        return "".join(result)
