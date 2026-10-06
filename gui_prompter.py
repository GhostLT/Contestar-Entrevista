"""
Interfaz Gráfica Flotante (Teleprompter / Copiloto de Entrevistas)
Desarrollada con Tkinter nativo para máximo rendimiento, 0% consumo de CPU,
soporte Always-on-Top (siempre visible sobre Zoom/Teams/Meet) y modo oscuro elegante.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import queue
import time
from typing import Optional, List, Dict, Any

import config
from audio_listener import AudioListener, get_audio_devices, get_default_device_index
from gemini_copilot import GeminiCopilot


class InterviewPrompterApp:
    """
    Ventana flotante de teleprompter para entrevistas técnicas.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Copiloto de Entrevistas | Gemini 3.8 Flash")
        self.root.geometry("680x620+350+80")
        self.root.minsize(480, 420)

        # Configuración de apariencia
        self.bg_main = "#121214"
        self.bg_card = "#1c1c21"
        self.bg_card_inner = "#26262d"
        self.text_color = "#f4f4f6"
        self.text_dim = "#9da1b0"
        self.accent_green = "#22c55e"
        self.accent_blue = "#3b82f6"
        self.accent_yellow = "#eab308"
        self.accent_red = "#ef4444"

        self.root.configure(bg=self.bg_main)

        # Always-on-top y opacidad inicial
        self.is_topmost = config.ALWAYS_ON_TOP
        self.opacity = config.WINDOW_OPACITY
        self.root.attributes("-topmost", self.is_topmost)
        try:
            self.root.attributes("-alpha", self.opacity)
        except Exception:
            pass

        # Componentes lógicos
        self.copilot = GeminiCopilot()
        self.devices = get_audio_devices()
        default_dev = get_default_device_index(prefer_loopback=False)

        self.listener = AudioListener(
            device_index=default_dev,
            language=config.AUDIO_LANGUAGE,
            on_text=self._on_speech_recognized,
            on_status=self._on_listener_status,
            on_error=self._on_listener_error,
        )

        # Cola para comunicación entre hilos y Tkinter
        self.msg_queue = queue.Queue()

        # Historial de preguntas
        self.history = []
        self.history_index = -1

        # Construir interfaz
        self._setup_ui()

        # Iniciar ciclo de mensajes de hilos
        self.root.after(100, self._process_queue)

        # Iniciar escucha automáticamente si hay API key
        if self.copilot.is_configured():
            self.listener.start()
        else:
            self._update_status("⚠️ Configura tu API Key de Gemini para comenzar", self.accent_yellow)

    def _setup_ui(self):
        # 1. BARRA SUPERIOR (Estado y controles de ventana)
        top_bar = tk.Frame(self.root, bg=self.bg_main, padx=12, pady=8)
        top_bar.pack(fill=tk.X)

        # Indicador de estado (Badge)
        self.lbl_status = tk.Label(
            top_bar,
            text="🟢 Iniciando...",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_card,
            fg=self.accent_green,
            padx=10,
            pady=4,
            relief=tk.FLAT
        )
        self.lbl_status.pack(side=tk.LEFT)

        # Botón de Pausar / Reanudar Escucha
        self.btn_pause = tk.Button(
            top_bar,
            text="⏸️ Pausar",
            command=self._toggle_pause,
            bg=self.bg_card,
            fg=self.text_color,
            activebackground=self.bg_card_inner,
            activeforeground=self.text_color,
            relief=tk.FLAT,
            padx=8,
            pady=2,
            font=("Segoe UI", 9)
        )
        self.btn_pause.pack(side=tk.LEFT, padx=(10, 0))

        # Botón Always-on-Top (Pin)
        self.btn_topmost = tk.Button(
            top_bar,
            text="📌 Fijar Arriba: SÍ" if self.is_topmost else "📌 Fijar Arriba: NO",
            command=self._toggle_topmost,
            bg=self.accent_blue if self.is_topmost else self.bg_card,
            fg="#ffffff" if self.is_topmost else self.text_dim,
            relief=tk.FLAT,
            padx=8,
            pady=2,
            font=("Segoe UI", 9, "bold" if self.is_topmost else "normal")
        )
        self.btn_topmost.pack(side=tk.RIGHT)

        # Botón de Configuración de API Key
        self.btn_apikey = tk.Button(
            top_bar,
            text="🔑 API Key",
            command=self._open_apikey_dialog,
            bg=self.bg_card,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=8,
            pady=2,
            font=("Segoe UI", 9)
        )
        self.btn_apikey.pack(side=tk.RIGHT, padx=6)

        # 2. SELECTOR DE DISPOSITIVOS DE AUDIO
        dev_bar = tk.Frame(self.root, bg=self.bg_main, padx=12, pady=4)
        dev_bar.pack(fill=tk.X)

        lbl_dev = tk.Label(
            dev_bar,
            text="Dispositivo:",
            bg=self.bg_main,
            fg=self.text_dim,
            font=("Segoe UI", 9)
        )
        lbl_dev.pack(side=tk.LEFT, padx=(0, 6))

        self.device_var = tk.StringVar()
        device_options = [d["label"] for d in self.devices] if self.devices else ["No se detectaron dispositivos"]
        
        # Encontrar índice seleccionado
        selected_label = device_options[0] if device_options else ""
        if self.listener.device_index is not None:
            for d in self.devices:
                if d["index"] == self.listener.device_index:
                    selected_label = d["label"]
                    break
        self.device_var.set(selected_label)

        self.opt_devices = ttk.Combobox(
            dev_bar,
            textvariable=self.device_var,
            values=device_options,
            state="readonly",
            width=50
        )
        self.opt_devices.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.opt_devices.bind("<<ComboboxSelected>>", self._on_device_changed)

        btn_refresh = tk.Button(
            dev_bar,
            text="🔄",
            command=self._refresh_devices,
            bg=self.bg_card,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 9),
            padx=6
        )
        btn_refresh.pack(side=tk.LEFT, padx=(6, 0))

        # 3. TARJETA DE PREGUNTA DETECTADA
        q_frame = tk.Frame(self.root, bg=self.bg_card, padx=12, pady=10)
        q_frame.pack(fill=tk.X, padx=12, pady=(8, 4))

        q_header = tk.Frame(q_frame, bg=self.bg_card)
        q_header.pack(fill=tk.X)

        lbl_q_title = tk.Label(
            q_header,
            text="PREGUNTA DETECTADA EN LA REUNIÓN",
            bg=self.bg_card,
            fg=self.accent_blue,
            font=("Segoe UI", 9, "bold")
        )
        lbl_q_title.pack(side=tk.LEFT)

        self.lbl_time = tk.Label(
            q_header,
            text="",
            bg=self.bg_card,
            fg=self.text_dim,
            font=("Segoe UI", 8)
        )
        self.lbl_time.pack(side=tk.RIGHT)

        self.txt_question = tk.Label(
            q_frame,
            text="Esperando que el entrevistador haga una pregunta...",
            bg=self.bg_card,
            fg=self.text_color,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=640
        )
        self.txt_question.pack(fill=tk.X, pady=(6, 0))

        # 4. TARJETA TELEPROMPTER DE RESPUESTA GEMINI
        ans_frame = tk.Frame(self.root, bg=self.bg_card, padx=12, pady=10)
        ans_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        ans_header = tk.Frame(ans_frame, bg=self.bg_card)
        ans_header.pack(fill=tk.X, pady=(0, 6))

        lbl_ans_title = tk.Label(
            ans_header,
            text="RESPUESTA DIRECTA (GEMINI 3.8 FLASH)",
            bg=self.bg_card,
            fg=self.accent_green,
            font=("Segoe UI", 9, "bold")
        )
        lbl_ans_title.pack(side=tk.LEFT)

        btn_copy = tk.Button(
            ans_header,
            text="📋 Copiar",
            command=self._copy_answer,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=6
        )
        btn_copy.pack(side=tk.RIGHT)

        btn_clear = tk.Button(
            ans_header,
            text="🗑️ Limpiar",
            command=self._clear_screen,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=6
        )
        btn_clear.pack(side=tk.RIGHT, padx=6)

        # Área de texto de respuesta con scroll
        self.txt_answer = tk.Text(
            ans_frame,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=12,
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            spacing1=3,
            spacing3=3,
        )
        self.txt_answer.pack(fill=tk.BOTH, expand=True)
        self.txt_answer.insert(
            tk.END,
            "💡 Tu respuesta aparecerá aquí en tiempo real de forma breve y concisa para que puedas leerla fluidamente en la reunión."
        )
        self.txt_answer.config(state=tk.DISABLED)

        # 5. BARRA DE ENTRADA MANUAL (Por si escriben en el chat de la llamada)
        input_bar = tk.Frame(self.root, bg=self.bg_main, padx=12, pady=8)
        input_bar.pack(fill=tk.X)

        self.entry_manual = tk.Entry(
            input_bar,
            bg=self.bg_card,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
        )
        self.entry_manual.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 6))
        self.entry_manual.insert(0, "O pega/escribe una pregunta del chat aquí...")
        self.entry_manual.bind("<FocusIn>", self._clear_placeholder)
        self.entry_manual.bind("<Return>", lambda e: self._send_manual_question())

        self.btn_send = tk.Button(
            input_bar,
            text="Preguntar ⚡",
            command=self._send_manual_question,
            bg=self.accent_green,
            fg="#000000",
            activebackground="#16a34a",
            relief=tk.FLAT,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=3
        )
        self.btn_send.pack(side=tk.RIGHT)

    # ------------------ EVENTOS Y CALLBACKS ------------------

    def _clear_placeholder(self, event):
        if self.entry_manual.get() == "O pega/escribe una pregunta del chat aquí...":
            self.entry_manual.delete(0, tk.END)

    def _toggle_topmost(self):
        self.is_topmost = not self.is_topmost
        self.root.attributes("-topmost", self.is_topmost)
        if self.is_topmost:
            self.btn_topmost.config(text="📌 Fijar Arriba: SÍ", bg=self.accent_blue, fg="#ffffff")
        else:
            self.btn_topmost.config(text="📌 Fijar Arriba: NO", bg=self.bg_card, fg=self.text_dim)

    def _toggle_pause(self):
        is_paused = self.listener.toggle_pause()
        if is_paused:
            self.btn_pause.config(text="▶️ Reanudar")
            self._update_status("⏸️ Escucha pausada", self.accent_yellow)
        else:
            self.btn_pause.config(text="⏸️ Pausar")
            self._update_status("🟢 Escuchando la reunión...", self.accent_green)

    def _on_device_changed(self, event):
        selection = self.device_var.get()
        for dev in self.devices:
            if dev["label"] == selection:
                self.listener.set_device(dev["index"])
                tipo = "Loopback de Reunión" if dev["is_loopback"] else "Micrófono"
                self._update_status(f"🟢 Escuchando desde {tipo}", self.accent_green)
                break

    def _refresh_devices(self):
        self.devices = get_audio_devices()
        options = [d["label"] for d in self.devices]
        self.opt_devices["values"] = options
        if options:
            self._update_status("Dispositivos actualizados", self.accent_blue)

    def _update_status(self, text: str, color: Optional[str] = None):
        self.lbl_status.config(text=text)
        if color:
            self.lbl_status.config(fg=color)

    def _copy_answer(self):
        content = self.txt_answer.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self._update_status("📋 ¡Respuesta copiada al portapapeles!", self.accent_blue)

    def _clear_screen(self):
        self.txt_question.config(text="Esperando que el entrevistador haga una pregunta...")
        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.delete("1.0", tk.END)
        self.txt_answer.insert(tk.END, "Esperando nueva intervención...")
        self.txt_answer.config(state=tk.DISABLED)

    # ------------------ MANEJO DE COLA DE HILOS ------------------

    def _on_speech_recognized(self, text: str):
        self.msg_queue.put(("SPEECH", text))

    def _on_listener_status(self, status: str):
        self.msg_queue.put(("STATUS", status))

    def _on_listener_error(self, err: str):
        self.msg_queue.put(("ERROR", err))

    def _process_queue(self):
        try:
            while not self.msg_queue.empty():
                kind, data = self.msg_queue.get_nowait()
                if kind == "STATUS":
                    color = self.accent_green if "Escuchando" in data else self.accent_yellow
                    if "Error" in data or "❌" in data:
                        color = self.accent_red
                    self._update_status(data, color)
                elif kind == "ERROR":
                    self._update_status(f"⚠️ {data[:35]}", self.accent_red)
                elif kind == "SPEECH":
                    self._handle_detected_text(data)
                elif kind == "STREAM_CHUNK":
                    self._append_answer_chunk(data)
                elif kind == "STREAM_DONE":
                    self._update_status("🟢 Escuchando la reunión...", self.accent_green)
                elif kind == "STREAM_IGNORED":
                    # Frase casual ignorada silenciosamente
                    self._update_status("🟢 Escuchando la reunión...", self.accent_green)
        except Exception as e:
            print(f"Error procesando cola: {e}")

        self.root.after(80, self._process_queue)

    def _handle_detected_text(self, text: str):
        # Actualizar tarjeta de pregunta
        now = time.strftime("%H:%M:%S")
        self.lbl_time.config(text=now)
        self.txt_question.config(text=f"❓ \"{text}\"")
        self._update_status("⚡ Consultando a Gemini 3.8 Flash...", self.accent_blue)

        # Preparar respuesta
        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.delete("1.0", tk.END)
        self.txt_answer.config(state=tk.DISABLED)

        # Disparar llamada a Gemini en hilo secundario para no congelar la GUI
        threading.Thread(target=self._ask_gemini_worker, args=(text,), daemon=True).start()

    def _send_manual_question(self):
        query = self.entry_manual.get().strip()
        if not query or query == "O pega/escribe una pregunta del chat aquí...":
            return
        self.entry_manual.delete(0, tk.END)
        self._handle_detected_text(query)

    def _ask_gemini_worker(self, question: str):
        first_chunk = True

        def _on_chunk(chunk):
            nonlocal first_chunk
            if first_chunk:
                first_chunk = False
            self.msg_queue.put(("STREAM_CHUNK", chunk))

        res = self.copilot.answer_question_stream(
            question=question,
            on_chunk=_on_chunk,
        )

        if res == "[IGNORAR]":
            self.msg_queue.put(("STREAM_IGNORED", None))
        else:
            self.msg_queue.put(("STREAM_DONE", None))

    def _append_answer_chunk(self, chunk: str):
        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.insert(tk.END, chunk)
        self.txt_answer.see(tk.END)
        self.txt_answer.config(state=tk.DISABLED)

    # ------------------ CONFIGURACIÓN DE API KEY ------------------

    def _open_apikey_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuración de Gemini API Key")
        dialog.geometry("480x220")
        dialog.configure(bg=self.bg_main)
        dialog.attributes("-topmost", True)
        dialog.transient(self.root)
        dialog.grab_set()

        lbl_desc = tk.Label(
            dialog,
            text="Ingresa tu Google Gemini API Key:\n(Puedes obtener una gratis en https://aistudio.google.com/)",
            bg=self.bg_main,
            fg=self.text_color,
            font=("Segoe UI", 9),
            justify=tk.LEFT
        )
        lbl_desc.pack(padx=16, pady=(16, 8), anchor="w")

        entry_key = tk.Entry(
            dialog,
            bg=self.bg_card,
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Segoe UI", 10),
            width=50
        )
        entry_key.pack(padx=16, pady=8, fill=tk.X)
        if self.copilot.api_key:
            entry_key.insert(0, self.copilot.api_key)

        def _save():
            new_key = entry_key.get().strip()
            if not new_key:
                messagebox.showwarning("Aviso", "Por favor ingresa una API Key válida.", parent=dialog)
                return

            self.copilot.set_api_key(new_key)
            # Guardar en archivo .env
            try:
                env_file = config.BASE_DIR / ".env"
                lines = []
                if env_file.exists():
                    lines = env_file.read_text(encoding="utf-8").splitlines()
                
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith("GEMINI_API_KEY="):
                        lines[i] = f"GEMINI_API_KEY={new_key}"
                        updated = True
                        break
                if not updated:
                    lines.append(f"GEMINI_API_KEY={new_key}")

                env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            except Exception as e:
                print(f"Error guardando .env: {e}")

            self._update_status("🟢 API Key guardada y lista", self.accent_green)
            if not self.listener._running:
                self.listener.start()
            dialog.destroy()

        btn_save = tk.Button(
            dialog,
            text="Guardar y Conectar",
            command=_save,
            bg=self.accent_green,
            fg="#000000",
            relief=tk.FLAT,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=4
        )
        btn_save.pack(pady=12)


def run_gui():
    root = tk.Tk()
    app = InterviewPrompterApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
