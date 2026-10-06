"""
Interfaz Gráfica Flotante (Teleprompter / Copiloto de Entrevistas)
Soporta:
- Conexión con Google Gemini (con conmutación automática anti-503)
- Conexión con DeepSeek (oficial)
- Conexión con OpenRouter (DeepSeek R1 Gratis)
- Always-on-Top, soporte para micrófono y loopback de reuniones.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time
from typing import Optional, List, Dict, Any

import config
from audio_listener import AudioListener, get_audio_devices, get_default_device_index
from gemini_copilot import AICopilot


class InterviewPrompterApp:
    """
    Ventana flotante de teleprompter para entrevistas técnicas.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Copiloto de Entrevistas | Gemini & DeepSeek")
        self.root.geometry("700x640+350+80")
        self.root.minsize(500, 440)

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
        self.copilot = AICopilot()
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

        # Construir interfaz
        self._setup_ui()

        # Iniciar ciclo de mensajes de hilos
        self.root.after(100, self._process_queue)

        # Iniciar escucha automáticamente si hay API key
        if self.copilot.is_configured():
            self.listener.start()
        else:
            self._update_status("⚠️ Configura tu API Key para comenzar", self.accent_yellow)

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

        # Botón de Configuración de API Keys
        self.btn_apikey = tk.Button(
            top_bar,
            text="🔑 API Keys / Modelos",
            command=self._open_apikey_dialog,
            bg=self.bg_card,
            fg=self.text_color,
            relief=tk.FLAT,
            padx=8,
            pady=2,
            font=("Segoe UI", 9)
        )
        self.btn_apikey.pack(side=tk.RIGHT, padx=6)

        # 2. SELECTORES DE AUDIO Y MOTOR IA
        control_bar = tk.Frame(self.root, bg=self.bg_main, padx=12, pady=4)
        control_bar.pack(fill=tk.X)

        # Selector de Proveedor IA
        lbl_ai = tk.Label(control_bar, text="IA:", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_ai.pack(side=tk.LEFT, padx=(0, 4))

        self.ai_var = tk.StringVar()
        ai_options = [
            "Gemini (Ultra Rápido - Auto Respaldo)",
            "DeepSeek Oficial (api.deepseek.com)",
            "OpenRouter (DeepSeek R1 Gratis)"
        ]
        if self.copilot.provider == "deepseek":
            self.ai_var.set(ai_options[1])
        elif self.copilot.provider == "openrouter":
            self.ai_var.set(ai_options[2])
        else:
            self.ai_var.set(ai_options[0])

        self.opt_ai = ttk.Combobox(
            control_bar,
            textvariable=self.ai_var,
            values=ai_options,
            state="readonly",
            width=28
        )
        self.opt_ai.pack(side=tk.LEFT, padx=(0, 10))
        self.opt_ai.bind("<<ComboboxSelected>>", self._on_ai_provider_changed)

        # Selector de Dispositivo de Audio
        lbl_dev = tk.Label(control_bar, text="Audio:", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_dev.pack(side=tk.LEFT, padx=(0, 4))

        self.device_var = tk.StringVar()
        device_options = [d["label"] for d in self.devices] if self.devices else ["No se detectaron dispositivos"]
        
        selected_label = device_options[0] if device_options else ""
        if self.listener.device_index is not None:
            for d in self.devices:
                if d["index"] == self.listener.device_index:
                    selected_label = d["label"]
                    break
        self.device_var.set(selected_label)

        self.opt_devices = ttk.Combobox(
            control_bar,
            textvariable=self.device_var,
            values=device_options,
            state="readonly",
            width=32
        )
        self.opt_devices.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.opt_devices.bind("<<ComboboxSelected>>", self._on_device_changed)

        btn_refresh = tk.Button(
            control_bar,
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
        q_frame.pack(fill=tk.X, padx=12, pady=(6, 4))

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
            wraplength=660
        )
        self.txt_question.pack(fill=tk.X, pady=(6, 0))

        # 4. TARJETA TELEPROMPTER DE RESPUESTA
        ans_frame = tk.Frame(self.root, bg=self.bg_card, padx=12, pady=10)
        ans_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        ans_header = tk.Frame(ans_frame, bg=self.bg_card)
        ans_header.pack(fill=tk.X, pady=(0, 6))

        lbl_ans_title = tk.Label(
            ans_header,
            text="RESPUESTA DIRECTA (COPILOTO IA - EN VIVO)",
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

    def _on_ai_provider_changed(self, event):
        sel = self.ai_var.get()
        if "DeepSeek Oficial" in sel:
            self.copilot.set_provider("deepseek")
            prov_text = "DeepSeek Oficial"
        elif "OpenRouter" in sel:
            self.copilot.set_provider("openrouter")
            prov_text = "OpenRouter (DeepSeek R1 Gratis)"
        else:
            self.copilot.set_provider("gemini")
            prov_text = "Gemini (Auto-Respaldo Anti-503)"

        self._update_status(f"Motor activo: {prov_text}", self.accent_blue)

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
            self._update_status("📋 ¡Respuesta copiada!", self.accent_blue)

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
                elif kind == "STREAM_START":
                    self.txt_answer.config(state=tk.NORMAL)
                    self.txt_answer.delete("1.0", tk.END)
                    self.txt_answer.config(state=tk.DISABLED)
                elif kind == "STREAM_CHUNK":
                    self._append_answer_chunk(data)
                elif kind == "STREAM_ERROR":
                    self.txt_answer.config(state=tk.NORMAL)
                    self.txt_answer.delete("1.0", tk.END)
                    self.txt_answer.insert(tk.END, f"{data}\n\n💡 Tip: Puedes cambiar a DeepSeek o configurar tus claves en '🔑 API Keys / Modelos' arriba.")
                    self.txt_answer.config(state=tk.DISABLED)
                    self._update_status("⚠️ Error consultando IA", self.accent_red)
                elif kind == "STREAM_DONE":
                    self._update_status("🟢 Escuchando la reunión...", self.accent_green)
                elif kind == "STREAM_IGNORED":
                    self.txt_answer.config(state=tk.NORMAL)
                    self.txt_answer.delete("1.0", tk.END)
                    self.txt_answer.insert(tk.END, "🔇 Charla casual ignorada (saludo o ruido cotidiano).\nEsperando una pregunta técnica...")
                    self.txt_answer.config(state=tk.DISABLED)
                    self._update_status("🟢 Escuchando la reunión...", self.accent_green)
        except Exception as e:
            print(f"Error procesando cola: {e}")

        self.root.after(80, self._process_queue)

    def _handle_detected_text(self, text: str):
        now = time.strftime("%H:%M:%S")
        self.lbl_time.config(text=now)
        self.txt_question.config(text=f"❓ \"{text}\"")
        self._update_status("⚡ Consultando a IA...", self.accent_blue)

        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.delete("1.0", tk.END)
        self.txt_answer.insert(tk.END, "⚡ Generando respuesta instantánea...")
        self.txt_answer.config(state=tk.DISABLED)

        threading.Thread(target=self._ask_ai_worker, args=(text,), daemon=True).start()

    def _send_manual_question(self):
        query = self.entry_manual.get().strip()
        if not query or query == "O pega/escribe una pregunta del chat aquí...":
            return
        self.entry_manual.delete(0, tk.END)
        self._handle_detected_text(query)

    def _ask_ai_worker(self, question: str):
        first_chunk = True

        def _on_chunk(chunk):
            nonlocal first_chunk
            if first_chunk:
                first_chunk = False
                self.msg_queue.put(("STREAM_START", None))
            self.msg_queue.put(("STREAM_CHUNK", chunk))

        def _on_error(err):
            self.msg_queue.put(("STREAM_ERROR", err))

        res = self.copilot.answer_question_stream(
            question=question,
            on_chunk=_on_chunk,
            on_error=_on_error,
        )

        if res == "[IGNORAR]":
            self.msg_queue.put(("STREAM_IGNORED", None))
        else:
            if first_chunk and res:
                self.msg_queue.put(("STREAM_START", None))
                self.msg_queue.put(("STREAM_CHUNK", res))
            self.msg_queue.put(("STREAM_DONE", None))

    def _append_answer_chunk(self, chunk: str):
        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.insert(tk.END, chunk)
        self.txt_answer.see(tk.END)
        self.txt_answer.config(state=tk.DISABLED)

    # ------------------ CONFIGURACIÓN DE CLAVES ------------------

    def _open_apikey_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuración de Motores de IA y Claves")
        dialog.geometry("540x360")
        dialog.configure(bg=self.bg_main)
        dialog.attributes("-topmost", True)
        dialog.transient(self.root)
        dialog.grab_set()

        lbl_head = tk.Label(
            dialog,
            text="Configura tus claves de API para no quedarte nunca sin respuesta:",
            bg=self.bg_main,
            fg=self.text_color,
            font=("Segoe UI", 10, "bold")
        )
        lbl_head.pack(padx=16, pady=(14, 10), anchor="w")

        # 1. Gemini
        lbl_g = tk.Label(dialog, text="Google Gemini API Key (Gratis en aistudio.google.com):", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_g.pack(padx=16, anchor="w")
        ent_gemini = tk.Entry(dialog, bg=self.bg_card, fg=self.text_color, insertbackground=self.text_color, font=("Segoe UI", 9))
        ent_gemini.pack(padx=16, pady=(2, 8), fill=tk.X)
        if self.copilot.gemini_key:
            ent_gemini.insert(0, self.copilot.gemini_key)

        # 2. DeepSeek
        lbl_d = tk.Label(dialog, text="DeepSeek API Key (platform.deepseek.com):", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_d.pack(padx=16, anchor="w")
        ent_deepseek = tk.Entry(dialog, bg=self.bg_card, fg=self.text_color, insertbackground=self.text_color, font=("Segoe UI", 9))
        ent_deepseek.pack(padx=16, pady=(2, 8), fill=tk.X)
        if self.copilot.deepseek_key:
            ent_deepseek.insert(0, self.copilot.deepseek_key)

        # 3. OpenRouter (DeepSeek Gratis)
        lbl_o = tk.Label(dialog, text="OpenRouter API Key (openrouter.ai/keys - DeepSeek R1 Gratis):", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_o.pack(padx=16, anchor="w")
        ent_openrouter = tk.Entry(dialog, bg=self.bg_card, fg=self.text_color, insertbackground=self.text_color, font=("Segoe UI", 9))
        ent_openrouter.pack(padx=16, pady=(2, 14), fill=tk.X)
        if self.copilot.openrouter_key:
            ent_openrouter.insert(0, self.copilot.openrouter_key)

        def _save():
            g_key = ent_gemini.get().strip()
            d_key = ent_deepseek.get().strip()
            o_key = ent_openrouter.get().strip()

            if g_key:
                self.copilot.set_gemini_key(g_key)
            if d_key:
                self.copilot.set_deepseek_key(d_key)
            if o_key:
                self.copilot.set_openrouter_key(o_key)

            # Guardar en archivo .env
            try:
                env_file = config.BASE_DIR / ".env"
                lines = []
                if env_file.exists():
                    lines = env_file.read_text(encoding="utf-8").splitlines()
                
                def set_env_val(key, val):
                    nonlocal lines
                    updated = False
                    for i, l in enumerate(lines):
                        if l.startswith(f"{key}="):
                            lines[i] = f"{key}={val}"
                            updated = True
                            break
                    if not updated:
                        lines.append(f"{key}={val}")

                if g_key:
                    set_env_val("GEMINI_API_KEY", g_key)
                if d_key:
                    set_env_val("DEEPSEEK_API_KEY", d_key)
                if o_key:
                    set_env_val("OPENROUTER_API_KEY", o_key)

                env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            except Exception as e:
                print(f"Error guardando .env: {e}")

            self._update_status("🟢 Configuración guardada", self.accent_green)
            if not self.listener._running and self.copilot.is_configured():
                self.listener.start()
            dialog.destroy()

        btn_save = tk.Button(
            dialog,
            text="Guardar y Aplicar",
            command=_save,
            bg=self.accent_green,
            fg="#000000",
            relief=tk.FLAT,
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=4
        )
        btn_save.pack(pady=4)


def run_gui():
    root = tk.Tk()
    app = InterviewPrompterApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
