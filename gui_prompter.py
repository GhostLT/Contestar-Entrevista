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
import candidate_profile
from audio_listener import AudioListener, get_audio_devices, get_default_device_index
from gemini_copilot import AICopilot
from history_logger import HistoryLogger
from realtime_translator import translate_en_to_es


class InterviewPrompterApp:
    """
    Ventana flotante de teleprompter para entrevistas técnicas.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Copiloto de Entrevistas | Gemini & DeepSeek")
        self.root.geometry("780x780+280+40")
        self.root.minsize(580, 520)

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

        # Estilo para divisor y pestañas
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.style.configure("TPanedwindow", background=self.bg_main)
        self.style.configure("Vertical.TPanedwindow", background=self.bg_main)
        self.style.configure("Sash", sashthickness=6, sashrelief="flat", background="#2d2d35")

        # Componentes lógicos
        self.copilot = AICopilot()
        self.logger = HistoryLogger()
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
        self.current_answer_lang = "es"
        self.active_tab = "copilot"
        self.active_pitch_key = "pitch_es_completo"
        self.pitch_buttons: Dict[str, tk.Button] = {}

        # Estado del Traductor Simultáneo de Conversación (EN -> ES)
        self.conv_translator_active = True
        self.conv_history: List[Dict[str, Any]] = []

        # Construir interfaz
        self._setup_ui()

        # Teclas rápidas para alternar pestañas
        self.root.bind("<F1>", lambda e: self._switch_tab("copilot"))
        self.root.bind("<F2>", lambda e: self._switch_tab("pitch"))

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
            width=24
        )
        self.opt_ai.pack(side=tk.LEFT, padx=(0, 10))
        self.opt_ai.bind("<<ComboboxSelected>>", self._on_ai_provider_changed)

        # Selector de Idioma de Respuesta
        lbl_lang = tk.Label(control_bar, text="Idioma:", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_lang.pack(side=tk.LEFT, padx=(0, 4))

        self.lang_var = tk.StringVar(value="🇪🇸 Español")
        self.opt_lang = ttk.Combobox(
            control_bar,
            textvariable=self.lang_var,
            values=["🇪🇸 Español", "🇺🇸 English"],
            state="readonly",
            width=11
        )
        self.opt_lang.pack(side=tk.LEFT, padx=(0, 10))
        self.opt_lang.bind("<<ComboboxSelected>>", self._on_language_changed)

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

        # 3. BARRA DE NAVEGACIÓN ENTRE PESTAÑAS (TABS)
        tab_nav = tk.Frame(self.root, bg=self.bg_main, padx=12, pady=3)
        tab_nav.pack(fill=tk.X)

        self.btn_tab_copilot = tk.Button(
            tab_nav,
            text="🎙️ Copiloto en Vivo (F1)",
            command=lambda: self._switch_tab("copilot"),
            bg=self.accent_blue,
            fg="#ffffff",
            activebackground=self.accent_blue,
            activeforeground="#ffffff",
            relief=tk.FLAT,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=3,
            cursor="hand2"
        )
        self.btn_tab_copilot.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_tab_pitch = tk.Button(
            tab_nav,
            text="🎯 Mi Pitch & Formación (F2)",
            command=lambda: self._switch_tab("pitch"),
            bg=self.bg_card,
            fg=self.text_dim,
            activebackground=self.bg_card_inner,
            activeforeground=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=3,
            cursor="hand2"
        )
        self.btn_tab_pitch.pack(side=tk.LEFT)

        # 4. CONTENEDOR PESTAÑA 1: COPILOTO EN VIVO
        self.frame_copilot = tk.Frame(self.root, bg=self.bg_main)
        self.frame_copilot.pack(fill=tk.BOTH, expand=True)

        # 5. CONTENEDOR PESTAÑA 2: MI PITCH & FORMACIÓN
        self.frame_pitch = tk.Frame(self.root, bg=self.bg_main)

        # --- CONTENIDO DE PESTAÑA 1 (COPILOTO CON PANTALLA DIVIDIDA) ---
        # Divisor vertical ajustable (PanedWindow)
        self.paned_copilot = ttk.PanedWindow(self.frame_copilot, orient=tk.VERTICAL)
        self.paned_copilot.pack(fill=tk.BOTH, expand=True, padx=12, pady=(2, 2))

        # ==============================================================
        # SECCIÓN SUPERIOR: TELEPROMPTER DE RESPUESTA IA (PREGUNTA + PROMPTER)
        # ==============================================================
        pane_top = tk.Frame(self.paned_copilot, bg=self.bg_main)

        # 4.1 TARJETA DE PREGUNTA DETECTADA (EDITABLE DIRECTAMENTE)
        q_frame = tk.Frame(pane_top, bg=self.bg_card, padx=12, pady=6)
        q_frame.pack(fill=tk.X, pady=(0, 4))

        q_header = tk.Frame(q_frame, bg=self.bg_card)
        q_header.pack(fill=tk.X, pady=(0, 4))

        lbl_q_title = tk.Label(
            q_header,
            text="PREGUNTA (EDITABLE EN VIVO SI SE ENTENDIÓ MAL):",
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

        btn_requery = tk.Button(
            q_header,
            text="⚡ Corregir y Re-preguntar (Enter)",
            command=self._requery_edited_question,
            bg=self.accent_blue,
            fg="#ffffff",
            activebackground="#2563eb",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=1
        )
        btn_requery.pack(side=tk.RIGHT, padx=10)

        # Campo de texto editable para modificar preguntas malinterpretadas
        self.txt_question = tk.Text(
            q_frame,
            height=2,
            bg=self.bg_card_inner,
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            font=("Segoe UI", 11, "bold"),
            wrap=tk.WORD,
            padx=8,
            pady=4
        )
        self.txt_question.pack(fill=tk.X, pady=(2, 0))
        self.txt_question.insert("1.0", "Esperando pregunta del entrevistador... (puedes hacer clic aquí y editar)")
        self.txt_question.bind("<Return>", self._on_question_box_enter)

        # 4.2 TARJETA TELEPROMPTER DE RESPUESTA
        ans_frame = tk.Frame(pane_top, bg=self.bg_card, padx=12, pady=8)
        ans_frame.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

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

        self.btn_translate = tk.Button(
            ans_header,
            text="🌐 Traducir a Inglés",
            command=self._translate_current_answer,
            bg=self.bg_card_inner,
            fg=self.accent_yellow,
            activebackground=self.bg_card,
            activeforeground=self.accent_yellow,
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8
        )
        self.btn_translate.pack(side=tk.RIGHT, padx=6)

        btn_hist = tk.Button(
            ans_header,
            text="📜 Historial",
            command=self._open_history,
            bg=self.bg_card_inner,
            fg=self.accent_blue,
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=6
        )
        btn_hist.pack(side=tk.RIGHT, padx=6)

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

        # Contenedor del área de respuesta con barra de desplazamiento
        ans_box_frame = tk.Frame(ans_frame, bg=self.bg_card_inner)
        ans_box_frame.pack(fill=tk.BOTH, expand=True)

        sb_ans = ttk.Scrollbar(ans_box_frame)
        sb_ans.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_answer = tk.Text(
            ans_box_frame,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=10,
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            spacing1=3,
            spacing3=3,
            yscrollcommand=sb_ans.set
        )
        self.txt_answer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_ans.config(command=self.txt_answer.yview)
        self.txt_answer.insert(
            tk.END,
            "💡 Tu respuesta aparecerá aquí en tiempo real de forma breve y concisa para que puedas leerla fluidamente en la reunión."
        )
        self.txt_answer.config(state=tk.DISABLED)

        # Agregar panel superior al divisor
        self.paned_copilot.add(pane_top, weight=3)

        # ==============================================================
        # SECCIÓN INFERIOR: TRADUCTOR DE CONVERSACIÓN EN VIVO (EN -> ES)
        # ==============================================================
        pane_bottom = tk.Frame(self.paned_copilot, bg=self.bg_main)

        conv_card = tk.Frame(pane_bottom, bg=self.bg_card, padx=10, pady=8)
        conv_card.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        conv_header = tk.Frame(conv_card, bg=self.bg_card)
        conv_header.pack(fill=tk.X, pady=(0, 6))

        lbl_conv_title = tk.Label(
            conv_header,
            text="🗣️ CONVERSACIÓN EN VIVO & TRADUCTOR SIMULTÁNEO (EN ➔ ES)",
            bg=self.bg_card,
            fg=self.accent_yellow,
            font=("Segoe UI", 9, "bold")
        )
        lbl_conv_title.pack(side=tk.LEFT)

        lbl_voice = tk.Label(conv_header, text="🎙️ Voz:", bg=self.bg_card, fg=self.text_dim, font=("Segoe UI", 8))
        lbl_voice.pack(side=tk.LEFT, padx=(10, 2))

        self.audio_lang_var = tk.StringVar(value="🇺🇸 Inglés (en-US)")
        self.opt_audio_lang = ttk.Combobox(
            conv_header,
            textvariable=self.audio_lang_var,
            values=["🇺🇸 Inglés (en-US)", "🇪🇸 Español (es-ES)"],
            state="readonly",
            width=16,
            font=("Segoe UI", 8)
        )
        self.opt_audio_lang.pack(side=tk.LEFT, padx=(0, 8))
        self.opt_audio_lang.bind("<<ComboboxSelected>>", self._on_audio_recognition_lang_changed)

        self.lbl_conv_status = tk.Label(
            conv_header,
            text="🟢 Activo",
            bg=self.bg_card_inner,
            fg=self.accent_green,
            font=("Segoe UI", 8, "bold"),
            padx=6,
            pady=1
        )
        self.lbl_conv_status.pack(side=tk.LEFT, padx=4)

        btn_clear_conv = tk.Button(
            conv_header,
            text="🗑️ Limpiar",
            command=self._clear_conversation,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=6
        )
        btn_clear_conv.pack(side=tk.RIGHT)

        self.btn_pause_conv = tk.Button(
            conv_header,
            text="⏸️ Pausar",
            command=self._toggle_conv_translator,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=6
        )
        self.btn_pause_conv.pack(side=tk.RIGHT, padx=4)

        btn_copy_conv = tk.Button(
            conv_header,
            text="📋 Copiar",
            command=self._copy_conversation,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=6
        )
        btn_copy_conv.pack(side=tk.RIGHT, padx=4)

        # Contenedor Lado a Lado (Side-by-Side Dual Columns)
        conv_body = tk.Frame(conv_card, bg=self.bg_card)
        conv_body.pack(fill=tk.BOTH, expand=True)

        # Columna 1: Audio Original en Inglés
        col_orig = tk.Frame(conv_body, bg=self.bg_card)
        col_orig.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 3))

        lbl_orig_head = tk.Label(
            col_orig,
            text="🇬🇧 Audio Original Detectado (English)",
            bg=self.bg_card,
            fg=self.accent_blue,
            font=("Segoe UI", 8, "bold")
        )
        lbl_orig_head.pack(anchor="w", pady=(0, 2))

        box_orig = tk.Frame(col_orig, bg=self.bg_card_inner)
        box_orig.pack(fill=tk.BOTH, expand=True)

        sb_orig = ttk.Scrollbar(box_orig)
        sb_orig.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_conv_orig = tk.Text(
            box_orig,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            padx=8,
            pady=6,
            spacing1=2,
            spacing3=2,
            yscrollcommand=sb_orig.set
        )
        self.txt_conv_orig.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_orig.config(command=self.txt_conv_orig.yview)
        self.txt_conv_orig.tag_configure("ts", foreground="#38bdf8", font=("Segoe UI", 8, "bold"))
        self.txt_conv_orig.insert(tk.END, "💡 La conversación del entrevistador en inglés se transcribirá aquí en tiempo real...")
        self.txt_conv_orig.config(state=tk.DISABLED)

        # Columna 2: Traducción al Español en Tiempo Real
        col_trans = tk.Frame(conv_body, bg=self.bg_card)
        col_trans.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(3, 0))

        lbl_trans_head = tk.Label(
            col_trans,
            text="🇪🇸 Traducción al Español (Tiempo Real)",
            bg=self.bg_card,
            fg=self.accent_green,
            font=("Segoe UI", 8, "bold")
        )
        lbl_trans_head.pack(anchor="w", pady=(0, 2))

        box_trans = tk.Frame(col_trans, bg=self.bg_card_inner)
        box_trans.pack(fill=tk.BOTH, expand=True)

        sb_trans = ttk.Scrollbar(box_trans)
        sb_trans.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_conv_trans = tk.Text(
            box_trans,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            padx=8,
            pady=6,
            spacing1=2,
            spacing3=2,
            yscrollcommand=sb_trans.set
        )
        self.txt_conv_trans.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_trans.config(command=self.txt_conv_trans.yview)
        self.txt_conv_trans.tag_configure("ts", foreground="#34d399", font=("Segoe UI", 8, "bold"))
        self.txt_conv_trans.tag_configure("loading", foreground=self.accent_yellow, font=("Segoe UI", 9, "italic"))
        self.txt_conv_trans.insert(tk.END, "💡 La traducción instantánea al español aparecerá aquí en tiempo real...")
        self.txt_conv_trans.config(state=tk.DISABLED)

        # Agregar panel inferior al divisor
        self.paned_copilot.add(pane_bottom, weight=2)

        # 4.3 BARRA DE ENTRADA MANUAL (Al pie de la ventana)
        input_bar = tk.Frame(self.frame_copilot, bg=self.bg_main, padx=12, pady=6)
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

        # Construir contenido de Pestaña 2 (Pitch)
        self._setup_pitch_ui()

    def _setup_pitch_ui(self):
        # 1. Sub-barra de selección de pitch y acciones
        pitch_nav = tk.Frame(self.frame_pitch, bg=self.bg_main, padx=12, pady=4)
        pitch_nav.pack(fill=tk.X)

        lbl_select = tk.Label(
            pitch_nav,
            text="Pitch:",
            bg=self.bg_main,
            fg=self.text_dim,
            font=("Segoe UI", 9)
        )
        lbl_select.pack(side=tk.LEFT, padx=(0, 4))

        pitch_options = [
            ("pitch_es_completo", "🇪🇸 Completo (60-90s)"),
            ("pitch_es_rapido", "⚡ Rápido (30s)"),
            ("pitch_en", "🇺🇸 English (60s)"),
            ("formacion_certs", "🎓 Formación & Certs"),
            ("fit_pcos", "🎯 Por qué PCoS"),
        ]

        for key, label in pitch_options:
            btn = tk.Button(
                pitch_nav,
                text=label,
                command=lambda k=key: self._load_pitch(k),
                bg=self.accent_blue if key == self.active_pitch_key else self.bg_card_inner,
                fg="#ffffff" if key == self.active_pitch_key else self.text_dim,
                activebackground=self.bg_card,
                activeforeground=self.text_color,
                relief=tk.FLAT,
                font=("Segoe UI", 8, "bold"),
                padx=8,
                pady=2,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.pitch_buttons[key] = btn

        # Acciones a la derecha
        btn_copy_pitch = tk.Button(
            pitch_nav,
            text="📋 Copiar",
            command=self._copy_pitch,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_copy_pitch.pack(side=tk.RIGHT, padx=(4, 0))

        btn_to_prompter = tk.Button(
            pitch_nav,
            text="⚡ Al Teleprompter",
            command=self._send_pitch_to_teleprompter,
            bg=self.accent_green,
            fg="#000000",
            activebackground="#16a34a",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_to_prompter.pack(side=tk.RIGHT, padx=4)

        # 2. Tarjeta contenedora de lectura
        pitch_card = tk.Frame(self.frame_pitch, bg=self.bg_card, padx=12, pady=8)
        pitch_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=(2, 4))

        # Encabezado de la tarjeta
        pitch_card_header = tk.Frame(pitch_card, bg=self.bg_card)
        pitch_card_header.pack(fill=tk.X, pady=(0, 6))

        self.lbl_pitch_title = tk.Label(
            pitch_card_header,
            text="GUIÓN DE PRESENTACIÓN | JAVIER VIVEROS HUESCA",
            bg=self.bg_card,
            fg=self.accent_yellow,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_pitch_title.pack(side=tk.LEFT)

        # Área de texto con scroll
        txt_box_frame = tk.Frame(pitch_card, bg=self.bg_card_inner)
        txt_box_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(txt_box_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_pitch = tk.Text(
            txt_box_frame,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=14,
            pady=14,
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            spacing1=4,
            spacing3=4,
            yscrollcommand=scrollbar.set,
        )
        self.txt_pitch.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.txt_pitch.yview)

        # Cargar pitch inicial
        self._load_pitch("pitch_es_completo")

        # 3. Badges inferiores con métricas rápidas
        badges_frame = tk.Frame(self.frame_pitch, bg=self.bg_main, padx=12, pady=4)
        badges_frame.pack(fill=tk.X)

        badges = [
            ("💼 +12 Años Exp Total", "#38bdf8"),
            ("⚡ +4 Años Full-Stack", "#34d399"),
            ("🤖 +2.5 Años Open Source", "#a78bfa"),
            ("💰 $2,500 USD/mes", "#facc15"),
            ("🚀 Disp. Inmediata", "#f472b6"),
            ("🎓 Ing. Electrónica y Sistemas", "#94a3b8"),
        ]
        for b_text, b_color in badges:
            lbl = tk.Label(
                badges_frame,
                text=b_text,
                bg=self.bg_card,
                fg=b_color,
                font=("Segoe UI", 8, "bold"),
                padx=8,
                pady=2,
                relief=tk.FLAT
            )
            lbl.pack(side=tk.LEFT, padx=2)

    def _switch_tab(self, tab_name: str):
        self.active_tab = tab_name
        if tab_name == "copilot":
            self.frame_pitch.pack_forget()
            self.frame_copilot.pack(fill=tk.BOTH, expand=True)
            self.btn_tab_copilot.config(bg=self.accent_blue, fg="#ffffff")
            self.btn_tab_pitch.config(bg=self.bg_card, fg=self.text_dim)
            self._update_status("🟢 Copiloto en Vivo activo (F2 para ver tu Pitch)", self.accent_green)
        else:
            self.frame_copilot.pack_forget()
            self.frame_pitch.pack(fill=tk.BOTH, expand=True)
            self.btn_tab_pitch.config(bg=self.accent_blue, fg="#ffffff")
            self.btn_tab_copilot.config(bg=self.bg_card, fg=self.text_dim)
            self._update_status("🎯 Viendo Pitch Personal (F1 para volver al Copiloto)", self.accent_blue)

    def _load_pitch(self, key: str):
        self.active_pitch_key = key
        script = candidate_profile.PITCH_SCRIPTS.get(key, "")
        self.txt_pitch.config(state=tk.NORMAL)
        self.txt_pitch.delete("1.0", tk.END)
        self.txt_pitch.insert(tk.END, script)
        self.txt_pitch.config(state=tk.DISABLED)

        # Actualizar estilo de botones del sub-selector
        for k, btn in self.pitch_buttons.items():
            if k == key:
                btn.config(bg=self.accent_blue, fg="#ffffff")
            else:
                btn.config(bg=self.bg_card_inner, fg=self.text_dim)

    def _copy_pitch(self):
        script = candidate_profile.PITCH_SCRIPTS.get(self.active_pitch_key, "")
        if script:
            self.root.clipboard_clear()
            self.root.clipboard_append(script)
            self._update_status("📋 ¡Pitch copiado al portapapeles!", self.accent_blue)

    def _send_pitch_to_teleprompter(self):
        script = candidate_profile.PITCH_SCRIPTS.get(self.active_pitch_key, "")
        if script:
            titles = {
                "pitch_es_completo": "🎙️ Pitch Completo de Presentación (Javier Viveros)",
                "pitch_es_rapido": "⚡ Elevator Pitch Rápido de 30s (Javier Viveros)",
                "pitch_en": "🇺🇸 Professional English Pitch (Javier Viveros)",
                "formacion_certs": "🎓 Formación Académica & Certificaciones (Javier Viveros)",
                "fit_pcos": "🎯 Por qué PCoS & Fit Técnico (Javier Viveros)",
            }
            self.txt_question.delete("1.0", tk.END)
            self.txt_question.insert("1.0", titles.get(self.active_pitch_key, "Mi Pitch Personal"))

            self.txt_answer.config(state=tk.NORMAL)
            self.txt_answer.delete("1.0", tk.END)
            self.txt_answer.insert(tk.END, script)
            self.txt_answer.config(state=tk.DISABLED)

            self._switch_tab("copilot")
            self._update_status("⚡ Pitch cargado en el Teleprompter principal", self.accent_green)

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
        self.txt_question.delete("1.0", tk.END)
        self.txt_question.insert("1.0", "Esperando que el entrevistador haga una pregunta...")
        self.entry_manual.delete(0, tk.END)
        self.entry_manual.insert(0, "O pega/escribe una pregunta del chat aquí...")
        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.delete("1.0", tk.END)
        self.txt_answer.insert(tk.END, "Esperando nueva intervención...")
        self.txt_answer.config(state=tk.DISABLED)
        self.current_answer_lang = "es"
        if hasattr(self, "btn_translate"):
            self.btn_translate.config(state=tk.NORMAL, text="🌐 Traducir a Inglés")

    def _on_language_changed(self, event=None):
        sel = self.lang_var.get()
        is_en = "English" in sel or "en" in sel.lower()
        lang_name = "Inglés (English)" if is_en else "Español"
        self._update_status(f"🌐 Idioma de respuesta: {lang_name}", self.accent_blue)
        next_target = "Español" if is_en else "Inglés"
        if hasattr(self, "btn_translate"):
            self.btn_translate.config(text=f"🌐 Traducir a {next_target}")

    def _translate_current_answer(self):
        content = self.txt_answer.get("1.0", tk.END).strip()
        if not content:
            return

        placeholders = [
            "💡 Tu respuesta aparecerá aquí",
            "Esperando",
            "🔇 Charla casual",
            "⚡ Generando",
            "🌐 Traduciendo"
        ]
        if any(content.startswith(p) for p in placeholders) or content.startswith("❌") or content.startswith("⚠️"):
            self._update_status("⚠️ No hay una respuesta para traducir", self.accent_yellow)
            return

        # Si el texto actual está en español, traducir a inglés; si está en inglés, a español
        target_lang = "en" if self.current_answer_lang == "es" else "es"
        target_label = "Inglés" if target_lang == "en" else "Español"
        q_text = self.txt_question.get("1.0", tk.END).strip()

        self.btn_translate.config(state=tk.DISABLED, text=f"🌐 Traduciendo...")
        self._update_status(f"🌐 Traduciendo respuesta a {target_label}...", self.accent_blue)

        threading.Thread(
            target=self._translate_worker,
            args=(content, target_lang, target_label, q_text),
            daemon=True
        ).start()

    def _translate_worker(self, text: str, target_lang: str, target_label: str, q_text: str = ""):
        first_chunk = True
        collected_chunks = []

        def _on_chunk(chunk):
            nonlocal first_chunk
            collected_chunks.append(chunk)
            if first_chunk:
                first_chunk = False
                self.msg_queue.put(("STREAM_START", None))
            self.msg_queue.put(("STREAM_CHUNK", chunk))

        def _on_error(err):
            self.msg_queue.put(("STREAM_ERROR", err))

        res = self.copilot.translate_text_stream(
            text=text,
            target_lang=target_lang,
            on_chunk=_on_chunk,
            on_error=_on_error,
        )

        if first_chunk and res and not res.startswith("❌") and not res.startswith("⚠️"):
            self.msg_queue.put(("STREAM_START", None))
            self.msg_queue.put(("STREAM_CHUNK", res))

        final_text = "".join(collected_chunks) if collected_chunks else res
        if final_text and not final_text.startswith("❌") and not final_text.startswith("⚠️"):
            self.msg_queue.put(("TRANSLATE_SUCCESS", (target_lang, final_text)))
            self.logger.log_interaction(
                question=f"[TRADUCCIÓN A {target_label.upper()}] {q_text}",
                answer=final_text,
                provider=f"{self.copilot.provider} (Traducción)"
            )
        else:
            self.msg_queue.put(("TRANSLATE_FAIL", None))

    def _on_question_box_enter(self, event):
        if event.state & 0x0001:  # Shift presionado: salto de línea
            return
        self._requery_edited_question()
        return "break"  # Evitar insertar el Enter en el recuadro

    def _requery_edited_question(self):
        edited_text = self.txt_question.get("1.0", tk.END).strip()
        if not edited_text or edited_text.startswith("Esperando pregunta"):
            return
        if edited_text.startswith("❓"):
            edited_text = edited_text.lstrip("❓").strip().strip('"')
        self._handle_detected_text(edited_text)

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
                    active_lang = data if data else "es"
                    self.current_answer_lang = active_lang
                    next_target = "Español" if active_lang == "en" else "Inglés"
                    if hasattr(self, "btn_translate"):
                        self.btn_translate.config(state=tk.NORMAL, text=f"🌐 Traducir a {next_target}")
                    self._update_status("🟢 Escuchando la reunión...", self.accent_green)
                elif kind == "TRANSLATE_SUCCESS":
                    target_lang, _ = data
                    self.current_answer_lang = target_lang
                    next_target = "Español" if target_lang == "en" else "Inglés"
                    if hasattr(self, "btn_translate"):
                        self.btn_translate.config(state=tk.NORMAL, text=f"🌐 Traducir a {next_target}")
                    self._update_status(f"🟢 Traducido con éxito a {'Inglés' if target_lang == 'en' else 'Español'}", self.accent_green)
                elif kind == "TRANSLATE_FAIL":
                    next_target = "Español" if self.current_answer_lang == "en" else "Inglés"
                    if hasattr(self, "btn_translate"):
                        self.btn_translate.config(state=tk.NORMAL, text=f"🌐 Traducir a {next_target}")
                    self._update_status("⚠️ No se pudo completar la traducción", self.accent_red)
                elif kind == "CONV_TRANSLATION_DONE":
                    turn_id, tag_name, timestamp, orig_text, trans_text = data
                    for turn in self.conv_history:
                        if turn["id"] == turn_id:
                            turn["trans"] = trans_text
                            break

                    self.txt_conv_trans.config(state=tk.NORMAL)
                    ranges = self.txt_conv_trans.tag_ranges(tag_name)
                    if ranges:
                        self.txt_conv_trans.delete(ranges[0], ranges[1])
                        self.txt_conv_trans.insert(ranges[0], f"{trans_text}\n\n", tag_name)
                    else:
                        self.txt_conv_trans.insert(tk.END, f"{trans_text}\n\n", tag_name)
                    self.txt_conv_trans.see(tk.END)
                    self.txt_conv_trans.config(state=tk.DISABLED)

                    if hasattr(self, "lbl_conv_status") and self.conv_translator_active:
                        self.lbl_conv_status.config(text="🟢 Activo", fg=self.accent_green)

                    # Persistir en historial permanente
                    self.logger.log_conversation_turn(
                        original_text=orig_text,
                        translated_text=trans_text,
                        source_lang="en",
                        target_lang="es"
                    )
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

        # Actualizar recuadro editable para que el usuario pueda modificar cualquier palabra en vivo
        self.txt_question.delete("1.0", tk.END)
        self.txt_question.insert("1.0", text)

        # Sincronizar también con la barra inferior
        self.entry_manual.delete(0, tk.END)
        self.entry_manual.insert(0, text)

        # Registrar y traducir simultáneamente en el panel inferior si está activo
        if getattr(self, "conv_translator_active", True):
            self._add_conversation_turn(text, now)

        self._update_status("⚡ Consultando a IA...", self.accent_blue)

        self.txt_answer.config(state=tk.NORMAL)
        self.txt_answer.delete("1.0", tk.END)
        self.txt_answer.insert(tk.END, "⚡ Generando respuesta instantánea...")
        self.txt_answer.config(state=tk.DISABLED)

        # Obtener idioma seleccionado en el hilo principal
        sel_lang = self.lang_var.get()
        is_en = "English" in sel_lang or "en" in sel_lang.lower()
        active_lang = "en" if is_en else "es"

        threading.Thread(target=self._ask_ai_worker, args=(text, active_lang), daemon=True).start()

    def _add_conversation_turn(self, text: str, timestamp: str):
        turn_id = int(time.time() * 1000)
        tag_name = f"turn_{turn_id}"

        # Insertar audio original (limpiando placeholder inicial si existe)
        self.txt_conv_orig.config(state=tk.NORMAL)
        current_orig = self.txt_conv_orig.get("1.0", tk.END).strip()
        if current_orig.startswith("💡 La conversación") or current_orig.startswith("💡 Conversación limpiada"):
            self.txt_conv_orig.delete("1.0", tk.END)
        self.txt_conv_orig.insert(tk.END, f"[{timestamp}] ", "ts")
        self.txt_conv_orig.insert(tk.END, f"{text}\n\n", tag_name)
        self.txt_conv_orig.see(tk.END)
        self.txt_conv_orig.config(state=tk.DISABLED)

        # Insertar placeholder temporal en la columna de traducción
        self.txt_conv_trans.config(state=tk.NORMAL)
        current_trans = self.txt_conv_trans.get("1.0", tk.END).strip()
        if current_trans.startswith("💡 La traducción") or current_trans.startswith("💡 Traducciones aparecerán"):
            self.txt_conv_trans.delete("1.0", tk.END)
        self.txt_conv_trans.insert(tk.END, f"[{timestamp}] ", "ts")
        self.txt_conv_trans.insert(tk.END, "⚡ Traduciendo...\n\n", tag_name)
        self.txt_conv_trans.see(tk.END)
        self.txt_conv_trans.config(state=tk.DISABLED)

        if hasattr(self, "lbl_conv_status") and self.conv_translator_active:
            self.lbl_conv_status.config(text="⚡ Traduciendo...", fg=self.accent_yellow)

        self.conv_history.append({
            "id": turn_id,
            "tag": tag_name,
            "time": timestamp,
            "orig": text,
            "trans": ""
        })

        # Disparar hilo de traducción en segundo plano
        threading.Thread(
            target=self._translate_conversation_worker,
            args=(turn_id, tag_name, timestamp, text),
            daemon=True
        ).start()

    def _translate_conversation_worker(self, turn_id: int, tag_name: str, timestamp: str, text: str):
        try:
            translated = translate_en_to_es(text, source_lang="auto", copilot_fallback=self.copilot)
        except Exception:
            translated = text

        self.msg_queue.put(("CONV_TRANSLATION_DONE", (turn_id, tag_name, timestamp, text, translated)))

    def _clear_conversation(self):
        self.conv_history.clear()
        self.txt_conv_orig.config(state=tk.NORMAL)
        self.txt_conv_orig.delete("1.0", tk.END)
        self.txt_conv_orig.insert(tk.END, "💡 Conversación limpiada. Esperando nuevo audio...\n\n")
        self.txt_conv_orig.config(state=tk.DISABLED)

        self.txt_conv_trans.config(state=tk.NORMAL)
        self.txt_conv_trans.delete("1.0", tk.END)
        self.txt_conv_trans.insert(tk.END, "💡 Traducciones aparecerán aquí en tiempo real...\n\n")
        self.txt_conv_trans.config(state=tk.DISABLED)

        self._update_status("🗑️ Historial de conversación en vivo limpiado", self.accent_blue)

    def _copy_conversation(self):
        if not self.conv_history:
            self._update_status("⚠️ No hay conversación para copiar", self.accent_yellow)
            return

        lines = []
        for turn in self.conv_history:
            lines.append(f"[{turn['time']}]")
            lines.append(f"🇬🇧 EN: {turn['orig']}")
            lines.append(f"🇪🇸 ES: {turn.get('trans', '')}")
            lines.append("-" * 35)

        text_to_copy = "\n".join(lines)
        self.root.clipboard_clear()
        self.root.clipboard_append(text_to_copy)
        self._update_status("📋 ¡Conversación completa copiada al portapapeles!", self.accent_green)

    def _toggle_conv_translator(self):
        self.conv_translator_active = not self.conv_translator_active
        if self.conv_translator_active:
            self.btn_pause_conv.config(text="⏸️ Pausar")
            self.lbl_conv_status.config(text="🟢 Activo", fg=self.accent_green)
            self._update_status("🟢 Traductor de conversación activado", self.accent_green)
        else:
            self.btn_pause_conv.config(text="▶️ Reanudar")
            self.lbl_conv_status.config(text="⏸️ Pausado", fg=self.accent_yellow)
            self._update_status("⏸️ Traductor de conversación pausado", self.accent_yellow)

    def _on_audio_recognition_lang_changed(self, event=None):
        sel = self.audio_lang_var.get()
        if "Español" in sel:
            new_lang = "es-ES"
            label = "Español (es-ES)"
        else:
            new_lang = "en-US"
            label = "Inglés (en-US)"
        self.listener.set_language(new_lang)
        self._update_status(f"🎙️ Reconocimiento de audio en: {label}", self.accent_blue)

    def _send_manual_question(self):
        query = self.entry_manual.get().strip()
        if not query or query == "O pega/escribe una pregunta del chat aquí...":
            return
        self.entry_manual.delete(0, tk.END)
        self._handle_detected_text(query)

    def _open_history(self):
        self.logger.open_history_folder()
        self._update_status("📂 Carpeta de historial abierta", self.accent_blue)

    def _ask_ai_worker(self, question: str, active_lang: str = "es"):
        first_chunk = True
        collected_chunks = []

        def _on_chunk(chunk):
            nonlocal first_chunk
            collected_chunks.append(chunk)
            if first_chunk:
                first_chunk = False
                self.msg_queue.put(("STREAM_START", None))
            self.msg_queue.put(("STREAM_CHUNK", chunk))

        def _on_error(err):
            self.msg_queue.put(("STREAM_ERROR", err))

        res = self.copilot.answer_question_stream(
            question=question,
            language=active_lang,
            on_chunk=_on_chunk,
            on_error=_on_error,
        )

        if res == "[IGNORAR]":
            self.msg_queue.put(("STREAM_IGNORED", None))
        else:
            if first_chunk and res:
                self.msg_queue.put(("STREAM_START", None))
                self.msg_queue.put(("STREAM_CHUNK", res))
            self.msg_queue.put(("STREAM_DONE", active_lang))

            # Guardar en archivo de historial permanente (.md y .json)
            final_text = "".join(collected_chunks) if collected_chunks else res
            if final_text and not final_text.startswith("❌") and not final_text.startswith("⚠️"):
                self.logger.log_interaction(
                    question=question,
                    answer=final_text,
                    provider=f"{self.copilot.provider} ({active_lang.upper()})"
                )

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
