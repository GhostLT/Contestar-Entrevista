"""
Módulo de Captura y Transcripción de Audio en Tiempo Real.
Soporta captura desde Micrófono y captura de Audio del Sistema (WASAPI Loopback)
para escuchar directamente las preguntas del entrevistador en Meet, Teams o Zoom.
"""

import threading
import time
from typing import Callable, Optional, List, Dict, Any

try:
    import pyaudiowpatch as pyaudio
except ImportError:
    import pyaudio

import speech_recognition as sr

# Parchear SpeechRecognition para que use pyaudiowpatch (soporte nativo de Loopback en Windows)
sr.Microphone.get_pyaudio = staticmethod(lambda: pyaudio)


def get_audio_devices() -> List[Dict[str, Any]]:
    """
    Obtiene la lista de dispositivos de audio de entrada y loopback disponibles.
    Devuelve lista de diccionarios con {index, name, is_loopback, label}
    """
    devices = []
    try:
        names = sr.Microphone.list_microphone_names()
        for idx, name in enumerate(names):
            # Filtrar nombres duplicados o irrelevantes si es necesario
            is_loop = "[Loopback]" in name or "Stereo Mix" in name or "Mezcla estéreo" in name
            tipo = "[Audio Reunion (Loopback)]" if is_loop else "[Microfono]"
            devices.append({
                "index": idx,
                "name": name,
                "is_loopback": is_loop,
                "label": f"[{idx}] {tipo}: {name}"
            })
    except Exception as e:
        print(f"Error enumerando dispositivos: {e}")
    return devices


def get_default_device_index(prefer_loopback: bool = False) -> Optional[int]:
    """
    Encuentra un índice de dispositivo predeterminado sensato.
    """
    devices = get_audio_devices()
    if not devices:
        return None

    if prefer_loopback:
        for dev in devices:
            if dev["is_loopback"]:
                return dev["index"]

    # Por defecto, buscar primer micrófono válido
    for dev in devices:
        if not dev["is_loopback"] and ("Microphone" in dev["name"] or "Micrófono" in dev["name"] or "Array" in dev["name"]):
            return dev["index"]

    return devices[0]["index"] if devices else None


class AudioListener:
    """
    Escucha continua de audio en segundo plano y transcripción con Google Speech Recognition.
    """

    def __init__(
        self,
        device_index: Optional[int] = None,
        language: str = "es-ES",
        on_text: Optional[Callable[[str], None]] = None,
        on_status: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
    ):
        self.device_index = device_index
        self.language = language
        self.on_text = on_text
        self.on_status = on_status
        self.on_error = on_error

        self.recognizer = sr.Recognizer()
        # Ajustes de sensibilidad para respuestas fluidas
        self.recognizer.pause_threshold = 1.0  # Segundos de silencio para dar por finalizada la frase
        self.recognizer.non_speaking_duration = 0.5
        self.recognizer.energy_threshold = 300  # Valor base
        self.recognizer.dynamic_energy_threshold = True

        self._running = False
        self._paused = False
        self._thread: Optional[threading.Thread] = None

    def _notify_status(self, msg: str):
        if self.on_status:
            self.on_status(msg)

    def _notify_error(self, err: str):
        if self.on_error:
            self.on_error(err)

    def set_device(self, device_index: Optional[int]):
        """Cambia el dispositivo y reinicia la escucha si está corriendo."""
        was_running = self._running
        if was_running:
            self.stop()
        self.device_index = device_index
        if was_running:
            self.start()

    def set_language(self, lang: str):
        self.language = lang

    def pause(self):
        self._paused = True
        self._notify_status("⏸️ Escucha pausada")

    def resume(self):
        self._paused = False
        self._notify_status("🟢 Escuchando audio...")

    def toggle_pause(self) -> bool:
        """Pausa o reanuda y devuelve el estado actual (True si está pausado)."""
        if self._paused:
            self.resume()
        else:
            self.pause()
        return self._paused

    def start(self):
        """Inicia el hilo de escucha continua."""
        if self._running:
            return

        self._running = True
        self._paused = False
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Detiene la escucha en segundo plano."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._notify_status("⏹️ Escucha detenida")

    def _listen_loop(self):
        """Ciclo continuo de captura y transcripción."""
        try:
            mic_kwargs = {}
            if self.device_index is not None:
                mic_kwargs["device_index"] = self.device_index

            with sr.Microphone(**mic_kwargs) as source:
                self._notify_status("⚙️ Calibrando ruido ambiental...")
                try:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                except Exception as e:
                    print(f"Aviso calibración: {e}")

                self._notify_status("🟢 Escuchando la reunión...")

                while self._running:
                    if self._paused:
                        time.sleep(0.3)
                        continue

                    try:
                        # Escuchar un fragmento de audio con límite de tiempo
                        audio = self.recognizer.listen(
                            source,
                            timeout=3.0,
                            phrase_time_limit=20.0
                        )

                        if not self._running or self._paused:
                            continue

                        self._notify_status("🟡 Transcribiendo pregunta...")

                        # Transcribir con Google Speech Recognition (gratis, rápido, sin API key extra)
                        texto = self.recognizer.recognize_google(
                            audio,
                            language=self.language
                        )

                        texto = texto.strip()
                        if texto:
                            self._notify_status("🟢 Escuchando la reunión...")
                            if self.on_text:
                                self.on_text(texto)

                    except sr.WaitTimeoutError:
                        # Silencio normal entre intervenciones
                        continue
                    except sr.UnknownValueError:
                        # Audio detectado pero no se entendió con claridad (resoplidos, ruidos menores)
                        self._notify_status("🟢 Escuchando la reunión...")
                        continue
                    except sr.RequestError as e:
                        self._notify_status("⚠️ Error de conexión de reconocimiento de voz")
                        self._notify_error(f"Error en servicio de reconocimiento de voz: {e}")
                        time.sleep(2.0)
                    except Exception as e:
                        if self._running:
                            self._notify_status(f"⚠️ Error: {str(e)[:30]}")
                            self._notify_error(f"Error capturando audio: {e}")
                            time.sleep(1.0)

        except Exception as e:
            self._notify_status("❌ Error iniciando dispositivo de audio")
            self._notify_error(f"No se pudo acceder al micrófono o dispositivo: {e}")
            self._running = False
