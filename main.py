"""
Punto de Entrada Principal - Copiloto de Entrevistas en Tiempo Real
Uso:
  python main.py                     -> Inicia la ventana flotante (GUI Always-on-Top)
  python main.py --cli               -> Inicia en modo terminal / consola
  python main.py --test-question "texto" -> Prueba una pregunta directamente con Gemini
"""

import sys
import argparse

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Copiloto de Entrevistas con Gemini 3.8 Flash")
    parser.add_argument("--cli", action="store_true", help="Ejecutar en modo consola / terminal en vez de ventana flotante")
    parser.add_argument("--test-question", type=str, help="Probar una pregunta directamente con Gemini y mostrar respuesta")
    args = parser.parse_args()

    if args.test_question:
        from gemini_copilot import GeminiCopilot
        from history_logger import HistoryLogger
        copilot = GeminiCopilot()
        logger = HistoryLogger()
        print(f"\nProbando pregunta: '{args.test_question}'\n")
        
        chunks = []
        def _stream(chunk):
            chunks.append(chunk)
            sys.stdout.write(chunk)
            sys.stdout.flush()

        res = copilot.answer_question_stream(args.test_question, on_chunk=_stream)
        full_ans = "".join(chunks) if chunks else res
        logger.log_interaction(args.test_question, full_ans, provider=copilot.provider)
        print(f"\n\nPrueba finalizada con éxito. (Registrado en historial/{logger.get_session_file_path().name})")
        return

    if args.cli:
        from cli_prompter import run_cli
        run_cli()
    else:
        from gui_prompter import run_gui
        run_gui()


if __name__ == "__main__":
    main()
