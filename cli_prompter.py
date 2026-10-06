"""
Modo Consola / Terminal para el Copiloto de Entrevistas.
Permite ejecutar el programa directamente desde PowerShell o CMD con salida a color.
"""

import sys
import time
from colorama import init, Fore, Style

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import config
from audio_listener import AudioListener, get_audio_devices, get_default_device_index
from gemini_copilot import GeminiCopilot

init(autoreset=True)


def run_cli():
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN} 🎙️  COPILOTO DE ENTREVISTAS EN TIEMPO REAL - GEMINI 3.8 FLASH")
    print(f"{Fore.CYAN}{'='*60}")

    copilot = GeminiCopilot()
    if not copilot.is_configured():
        print(f"{Fore.YELLOW}⚠️  No se encontró GEMINI_API_KEY en las variables de entorno.")
        api_key = input("Introduce tu API Key de Gemini: ").strip()
        if not api_key:
            print(f"{Fore.RED}Se requiere una API Key para continuar.")
            sys.exit(1)
        copilot.set_api_key(api_key)

    devices = get_audio_devices()
    print(f"\n{Fore.MAGENTA}Dispositivos de Audio Disponibles:")
    for d in devices:
        mark = " (Recomendado)" if d["is_loopback"] or "Microphone Array" in d["name"] else ""
        print(f"  [{d['index']}] {d['name']}{mark}")

    default_idx = get_default_device_index(prefer_loopback=False)
    dev_input = input(f"\nSelecciona el número de dispositivo [{default_idx}]: ").strip()
    selected_idx = int(dev_input) if dev_input.isdigit() else default_idx

    print(f"\n{Fore.GREEN}🟢 Iniciando escucha en segundo plano...")
    print(f"{Fore.WHITE}El entrevistador puede hablar en la reunión. Presiona Ctrl+C para salir.\n")

    def on_status(msg):
        # Mostrar estado en una sola línea discreta
        sys.stdout.write(f"\r{Fore.YELLOW}{msg:<40}{Style.RESET_ALL}")
        sys.stdout.flush()

    def on_question(text):
        print(f"\n\n{Fore.CYAN}{'─'*50}")
        print(f"{Fore.CYAN}❓ PREGUNTA DETECTADA:{Style.RESET_ALL} {text}")
        print(f"{Fore.GREEN}⚡ RESPUESTA GEMINI 3.8 FLASH:{Style.RESET_ALL}")
        
        first = True
        def on_chunk(chunk):
            nonlocal first
            if first:
                first = False
            sys.stdout.write(chunk)
            sys.stdout.flush()

        res = copilot.answer_question_stream(
            question=text,
            on_chunk=on_chunk,
        )

        if res == "[IGNORAR]":
            print(f"\r{Fore.LIGHTBLACK_EX}[Conversación casual ignorada]{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}{'─'*50}\n")
            print(f"{Fore.YELLOW}🟢 Escuchando la reunión...{Style.RESET_ALL}")

    listener = AudioListener(
        device_index=selected_idx,
        language=config.AUDIO_LANGUAGE,
        on_text=on_question,
        on_status=on_status,
        on_error=lambda err: print(f"\n{Fore.RED}Error: {err}{Style.RESET_ALL}"),
    )

    listener.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Deteniendo asistente...{Style.RESET_ALL}")
        listener.stop()
        print(f"{Fore.GREEN}¡Hasta luego! Éxito en tu entrevista.")


if __name__ == "__main__":
    run_cli()
