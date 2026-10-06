"""
Módulo de Integración con Motores de IA para Entrevistas en Tiempo Real
Soporta:
1. Google Gemini (con conmutación por error automática ante saturación 503)
2. DeepSeek (api.deepseek.com / deepseek-chat)
3. OpenRouter (Modelos DeepSeek R1 Gratuitos)
"""

import json
from typing import Callable, Optional, List, Dict, Any
import httpx
from google import genai
from google.genai import types
import config


# Lista de modelos de respaldo en orden de prioridad para evitar el error 503 de alta demanda
GEMINI_FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",  # Más rápido, altamente disponible y sin saturación
    "gemini-3.1-flash-lite",  # Respaldo ultra veloz
    "gemini-3.8-flash",       # Modelo avanzado
]


class AICopilot:
    """
    Cliente inteligente multi-proveedor (Gemini y DeepSeek).
    """

    def __init__(self):
        self.provider = config.AI_PROVIDER  # 'gemini', 'deepseek', 'openrouter'
        self.gemini_key = config.GEMINI_API_KEY
        self.deepseek_key = config.DEEPSEEK_API_KEY
        self.openrouter_key = config.OPENROUTER_API_KEY
        self.gemini_client: Optional[genai.Client] = None
        self._init_gemini()

    def _init_gemini(self):
        if self.gemini_key and self.gemini_key != "tu_clave_de_gemini_aqui":
            try:
                self.gemini_client = genai.Client(api_key=self.gemini_key)
            except Exception as e:
                print(f"Error inicializando Gemini: {e}")
                self.gemini_client = None
        else:
            self.gemini_client = None

    def set_provider(self, provider: str):
        self.provider = provider.lower()

    def set_gemini_key(self, key: str):
        self.gemini_key = key.strip()
        self._init_gemini()

    def set_deepseek_key(self, key: str):
        self.deepseek_key = key.strip()

    def set_openrouter_key(self, key: str):
        self.openrouter_key = key.strip()

    def is_configured(self) -> bool:
        """Verifica y recarga claves desde .env automáticamente."""
        self._reload_env_if_needed()
        if self.provider == "gemini":
            return self.gemini_client is not None and bool(self.gemini_key) and self.gemini_key != "tu_clave_de_gemini_aqui"
        elif self.provider == "deepseek":
            return bool(self.deepseek_key)
        elif self.provider == "openrouter":
            return bool(self.openrouter_key)
        return False

    def _reload_env_if_needed(self):
        try:
            import os
            from dotenv import load_dotenv
            env_file = config.BASE_DIR / ".env"
            if env_file.exists():
                load_dotenv(dotenv_path=env_file, override=True)
                gkey = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
                if gkey and gkey != "tu_clave_de_gemini_aqui" and gkey != self.gemini_key:
                    self.set_gemini_key(gkey)
                
                dkey = os.getenv("DEEPSEEK_API_KEY") or ""
                if dkey and dkey != self.deepseek_key:
                    self.set_deepseek_key(dkey)

                okey = os.getenv("OPENROUTER_API_KEY") or ""
                if okey and okey != self.openrouter_key:
                    self.set_openrouter_key(okey)
        except Exception as e:
            print(f"Error recargando .env: {e}")

    def answer_question_stream(
        self,
        question: str,
        on_chunk: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Enruta la pregunta al proveedor seleccionado con streaming continuo.
        """
        self._reload_env_if_needed()

        if self.provider == "deepseek":
            return self._stream_deepseek(question, on_chunk, on_complete, on_error)
        elif self.provider == "openrouter":
            return self._stream_openrouter(question, on_chunk, on_complete, on_error)
        else:
            return self._stream_gemini_with_fallback(question, on_chunk, on_complete, on_error)

    # ----------------- PROVEEDOR 1: GOOGLE GEMINI CON AUTO-FALLBACK -----------------

    def _stream_gemini_with_fallback(
        self,
        question: str,
        on_chunk: Optional[Callable[[str], None]],
        on_complete: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[str], None]],
    ) -> str:
        if not self.gemini_client:
            msg = "⚠️ Falta la API Key de Gemini. Configúrala en la aplicación o archivo .env."
            if on_error:
                on_error(msg)
            return msg

        prompt = f"Pregunta o intervención del entrevistador:\n\"{question}\""
        config_params = types.GenerateContentConfig(
            system_instruction=config.SYSTEM_INSTRUCTION,
            temperature=0.25,
            max_output_tokens=500,
        )

        # Generar lista de modelos a probar (modelo configurado primero, luego respaldos)
        candidate_models = [config.GEMINI_MODEL] + GEMINI_FALLBACK_MODELS
        # Deduplicar manteniendo orden
        seen = set()
        models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

        last_error = ""

        for model_name in models_to_try:
            full_text = ""
            is_ignorable = False
            received_any = False

            try:
                response_stream = self.gemini_client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                    config=config_params,
                )

                for chunk in response_stream:
                    if chunk.text:
                        received_any = True
                        full_text += chunk.text

                        if "[IGNORAR]" in full_text:
                            is_ignorable = True
                            break

                        if on_chunk:
                            on_chunk(chunk.text)

                if is_ignorable:
                    return "[IGNORAR]"

                if received_any:
                    if on_complete:
                        on_complete(full_text)
                    return full_text

            except Exception as e:
                err_str = str(e)
                last_error = err_str

                # Si es error 503 UNAVAILABLE (alta demanda temporal), cambiar de modelo de inmediato
                if "503" in err_str or "UNAVAILABLE" in err_str or "high demand" in err_str:
                    print(f"Aviso: Modelo {model_name} con alta demanda (503). Cambiando a modelo alternativo...")
                    continue
                else:
                    # Si es error de credencial o formato, reportar de inmediato
                    break

        # Si llegamos aquí, reportar el error final de forma limpia
        if "API_KEY_INVALID" in last_error or "API key not valid" in last_error:
            msg = "❌ Error: La API Key de Gemini no es válida. Revísala en https://aistudio.google.com/"
        elif "RESOURCE_EXHAUSTED" in last_error:
            msg = "⚠️ Cuota temporal de Gemini excedida. Por favor espera unos segundos."
        elif "503" in last_error:
            msg = "⚠️ Servidores de Gemini temporalmente saturados. Intenta de nuevo o cambia a DeepSeek."
        else:
            msg = f"❌ Error conectando con Gemini: {last_error}"

        if on_error:
            on_error(msg)
        return msg

    # ----------------- PROVEEDOR 2: DEEPSEEK (OFICIAL) -----------------

    def _stream_deepseek(
        self,
        question: str,
        on_chunk: Optional[Callable[[str], None]],
        on_complete: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[str], None]],
    ) -> str:
        if not self.deepseek_key:
            msg = "⚠️ Falta la API Key de DeepSeek. Obtenla en https://platform.deepseek.com/"
            if on_error:
                on_error(msg)
            return msg

        return self._stream_openai_compatible(
            url="https://api.deepseek.com/chat/completions",
            api_key=self.deepseek_key,
            model="deepseek-chat",
            question=question,
            provider_name="DeepSeek",
            on_chunk=on_chunk,
            on_complete=on_complete,
            on_error=on_error,
        )

    # ----------------- PROVEEDOR 3: OPENROUTER (DEEPSEEK R1 GRATIS) -----------------

    def _stream_openrouter(
        self,
        question: str,
        on_chunk: Optional[Callable[[str], None]],
        on_complete: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[str], None]],
    ) -> str:
        if not self.openrouter_key:
            msg = "⚠️ Falta la API Key de OpenRouter. Obtenla gratis en https://openrouter.ai/keys"
            if on_error:
                on_error(msg)
            return msg

        return self._stream_openai_compatible(
            url="https://openrouter.ai/api/v1/chat/completions",
            api_key=self.openrouter_key,
            model="deepseek/deepseek-chat:free",
            question=question,
            provider_name="OpenRouter (DeepSeek)",
            on_chunk=on_chunk,
            on_complete=on_complete,
            on_error=on_error,
        )

    # ----------------- HELPER STREAMING OPENAI-COMPATIBLE -----------------

    def _stream_openai_compatible(
        self,
        url: str,
        api_key: str,
        model: str,
        question: str,
        provider_name: str,
        on_chunk: Optional[Callable[[str], None]],
        on_complete: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[str], None]],
    ) -> str:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/GhostLT/Contestar-Entrevista",
            "X-Title": "Copiloto de Entrevistas",
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": config.SYSTEM_INSTRUCTION},
                {"role": "user", "content": f"Pregunta de entrevista:\n\"{question}\""}
            ],
            "temperature": 0.25,
            "max_tokens": 500,
            "stream": True,
        }

        full_text = ""
        is_ignorable = False

        try:
            with httpx.Client(timeout=30.0) as client:
                with client.stream("POST", url, headers=headers, json=payload) as resp:
                    if resp.status_code != 200:
                        err_content = resp.read().decode("utf-8", errors="ignore")
                        msg = f"❌ Error en {provider_name} (HTTP {resp.status_code}): {err_content[:150]}"
                        if on_error:
                            on_error(msg)
                        return msg

                    for line in resp.iter_lines():
                        line = line.strip()
                        if not line or line == "data: [DONE]":
                            continue

                        if line.startswith("data: "):
                            raw_json = line[6:]
                            try:
                                data = json.loads(raw_json)
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    full_text += content
                                    if "[IGNORAR]" in full_text:
                                        is_ignorable = True
                                        break
                                    if on_chunk:
                                        on_chunk(content)
                            except Exception:
                                continue

            if is_ignorable:
                return "[IGNORAR]"

            if on_complete:
                on_complete(full_text)
            return full_text

        except Exception as e:
            msg = f"❌ Error de conexión con {provider_name}: {e}"
            if on_error:
                on_error(msg)
            return msg

    def answer_question(self, question: str) -> str:
        """Método sincrónico sin streaming."""
        chunks = []
        self.answer_question_stream(question, on_chunk=lambda c: chunks.append(c))
        return "".join(chunks)


# Alias de retrocompatibilidad
GeminiCopilot = AICopilot
