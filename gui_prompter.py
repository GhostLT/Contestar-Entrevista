"""
Interfaz Gráfica Flotante (Teleprompter / Copiloto de Entrevistas)
Soporta:
- Conexión con Google Gemini (con conmutación automática anti-503)
- Conexión con DeepSeek (oficial)
- Conexión con OpenRouter (DeepSeek R1 Gratis)
- Always-on-Top, soporte para micrófono y loopback de reuniones.
"""

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time
from typing import Optional, List, Dict, Any, Tuple

import config
import candidate_profile
from audio_listener import AudioListener, get_audio_devices, get_default_device_index
from gemini_copilot import AICopilot
from history_logger import HistoryLogger
from rf_word_guide import RFWordGuide, QuestionItem, ModuleItem


class InterviewPrompterApp:
    """
    Ventana flotante de teleprompter para entrevistas técnicas.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Copiloto de Entrevistas | Gemini & DeepSeek")
        self.root.geometry("1020x780+160+20")
        self.root.minsize(680, 520)

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

        # Estilo para controles y pestañas
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

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
        self.active_pitch_key = "pitch_rf_es"
        self.pitch_buttons: Dict[str, tk.Button] = {}

        # Componentes de la Guía de Entrevista Word (Bilingüe ES y EN en memoria)
        self.rf_word_guide_es = RFWordGuide("es")
        self.rf_word_guide_en = RFWordGuide("en")
        self.rf_word_guide = self.rf_word_guide_es
        self.current_word_lang = "es"
        self.selected_question_item: Optional[QuestionItem] = None
        self.displayed_questions: List[QuestionItem] = []
        self._is_syncing_word_scroll = False
        self._stream_full_text = ""

        # Construir interfaz
        self._setup_ui()

        # Teclas rápidas para alternar pestañas: 1, 2, 3 (y F1, F2, F3 como alternativa)
        self.root.bind("<KeyPress>", self._on_global_key_press)
        self.root.bind("<F1>", lambda e: self._switch_tab("copilot"))
        self.root.bind("<F2>", lambda e: self._switch_tab("pitch"))
        self.root.bind("<F3>", lambda e: self._switch_tab("word_guide"))

        # Atajos globales de copia de texto seleccionado (Ctrl+C)
        self.root.bind("<Control-c>", self._copy_selected_text)
        self.root.bind("<Control-C>", self._copy_selected_text)
        self.root.bind("<<Copy>>", self._copy_selected_text)

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
        lbl_lang = tk.Label(control_bar, text="Modo:", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 9))
        lbl_lang.pack(side=tk.LEFT, padx=(0, 4))

        self.lang_var = tk.StringVar(value="⚡ Dual (ES + EN)")
        self.opt_lang = ttk.Combobox(
            control_bar,
            textvariable=self.lang_var,
            values=["⚡ Dual (ES + EN)", "🇪🇸 Solo Español", "🇺🇸 Only English"],
            state="readonly",
            width=16
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

        # 3. BARRA DE NAVEGACIÓN ENTRE PESTAÑAS (TABS CON ATAJOS 1, 2, 3)
        tab_nav = tk.Frame(self.root, bg=self.bg_main, padx=12, pady=3)
        tab_nav.pack(fill=tk.X)

        self.btn_tab_copilot = tk.Button(
            tab_nav,
            text="🎙️ Copiloto en Vivo (1)",
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
            text="🎯 Mi Pitch & Formación (2)",
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
        self.btn_tab_pitch.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_tab_word_guide = tk.Button(
            tab_nav,
            text="📖 Guía Entrevista Word (3)",
            command=lambda: self._switch_tab("word_guide"),
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
        self.btn_tab_word_guide.pack(side=tk.LEFT)

        # 4. CONTENEDOR PESTAÑA 1: COPILOTO EN VIVO
        self.frame_copilot = tk.Frame(self.root, bg=self.bg_main)
        self.frame_copilot.pack(fill=tk.BOTH, expand=True)

        # 5. CONTENEDOR PESTAÑA 2: MI PITCH & FORMACIÓN
        self.frame_pitch = tk.Frame(self.root, bg=self.bg_main)

        # 6. CONTENEDOR PESTAÑA 3: GUÍA DE ENTREVISTA EN FORMATO WORD
        self.frame_word_guide = tk.Frame(self.root, bg=self.bg_main)

        # --- CONTENIDO DE PESTAÑA 1 (COPILOTO) ---
        # 4.1 TARJETA DE PREGUNTA DETECTADA (EDITABLE DIRECTAMENTE)
        q_frame = tk.Frame(self.frame_copilot, bg=self.bg_card, padx=12, pady=6)
        q_frame.pack(fill=tk.X, padx=12, pady=(4, 4))

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
        self.txt_question.bind("<Return>", self._on_question_box_enter)
        self.txt_question.bind("<KeyRelease>", self._on_question_key_release)

        # Banner interactivo de coincidencias temáticas con la Guía Word Oficial (Oculto hasta detectar relación)
        self.frame_word_match = tk.Frame(q_frame, bg="#0f172a", relief=tk.SOLID, bd=1, padx=10, pady=5)
        self.current_matched_word_q = None
        self.current_matched_word_list = []

        self.word_match_header_frame = tk.Frame(self.frame_word_match, bg="#0f172a")
        self.word_match_header_frame.pack(fill=tk.X, pady=(0, 4))

        self.lbl_word_match_header = tk.Label(
            self.word_match_header_frame,
            text="📖 GUÍA WORD OFICIAL:",
            bg="#0f172a",
            fg=self.accent_green,
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_word_match_header.pack(side=tk.LEFT, padx=(0, 6))

        self.lbl_word_match_hint = tk.Label(
            self.word_match_header_frame,
            text="(Haz clic en cualquier opción para ir directo a esa pregunta)",
            bg="#0f172a",
            fg="#94a3b8",
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_word_match_hint.pack(side=tk.LEFT)

        # Contenedor dinámico de chips/botones de posibilidades encontradas
        self.chips_word_container = tk.Frame(self.frame_word_match, bg="#0f172a")
        self.chips_word_container.pack(fill=tk.X)

        # 4.2 TARJETA TELEPROMPTER DE RESPUESTA DIVIDIDA EN 2 HORIZONTALMENTE
        ans_frame = tk.Frame(self.frame_copilot, bg=self.bg_card, padx=12, pady=6)
        ans_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(2, 4))

        ans_header = tk.Frame(ans_frame, bg=self.bg_card)
        ans_header.pack(fill=tk.X, pady=(0, 4))

        # Botones de acción reubicados al lado izquierdo (debajo de la pregunta / acceso rápido)
        btn_clear = tk.Button(
            ans_header,
            text="🗑️ Limpiar",
            command=self._clear_screen,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_clear.pack(side=tk.LEFT, padx=(0, 4))

        btn_hist = tk.Button(
            ans_header,
            text="📜 Historial",
            command=self._open_history,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_hist.pack(side=tk.LEFT, padx=(0, 6))

        btn_copy_es = tk.Button(
            ans_header,
            text="📋 Copiar ES",
            command=self._copy_answer_es,
            bg=self.bg_card_inner,
            fg=self.accent_green,
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_copy_es.pack(side=tk.LEFT, padx=(0, 4))

        btn_copy_en = tk.Button(
            ans_header,
            text="📋 Copiar EN",
            command=self._copy_answer_en,
            bg=self.bg_card_inner,
            fg=self.accent_blue,
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_copy_en.pack(side=tk.LEFT, padx=(0, 10))

        lbl_ans_title = tk.Label(
            ans_header,
            text="RESPUESTA DIRECTA TELEPROMPTER (DUAL ES / EN)",
            bg=self.bg_card,
            fg=self.accent_green,
            font=("Segoe UI", 9, "bold")
        )
        lbl_ans_title.pack(side=tk.RIGHT)

        # Contenedor dividido en 2 paneles simétricos al 50% de altura cada uno
        self.ans_paned = ans_frame

        # SECCIÓN SUPERIOR: RESPUESTA EN ESPAÑOL (50% de altura)
        pane_es = tk.Frame(ans_frame, bg=self.bg_card)
        pane_es.pack(fill=tk.BOTH, expand=True, pady=(0, 3))

        hdr_es = tk.Frame(pane_es, bg=self.bg_card)
        hdr_es.pack(fill=tk.X, pady=(0, 2))

        lbl_es = tk.Label(
            hdr_es,
            text="🇪🇸 RESPUESTA DIRECTA (ESPAÑOL) — Lectura rápida / Puntos clave",
            bg=self.bg_card,
            fg=self.accent_green,
            font=("Segoe UI", 8, "bold")
        )
        lbl_es.pack(side=tk.LEFT)

        box_es = tk.Frame(pane_es, bg=self.bg_card_inner)
        box_es.pack(fill=tk.BOTH, expand=True)

        sb_es = ttk.Scrollbar(box_es)
        sb_es.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_answer_es = tk.Text(
            box_es,
            height=5,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=10,
            pady=6,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            spacing1=2,
            spacing3=2,
            yscrollcommand=sb_es.set
        )
        self.txt_answer_es.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_es.config(command=self.txt_answer_es.yview)
        self.txt_answer_es.insert(
            tk.END,
            "💡 Tu respuesta en ESPAÑOL aparecerá aquí en tiempo real (puntos clave directos para leer fluidamente en la reunión)."
        )
        self.txt_answer_es.config(state=tk.DISABLED)

        # SECCIÓN INFERIOR: RESPUESTA EN INGLÉS (50% de altura)
        pane_en = tk.Frame(ans_frame, bg=self.bg_card)
        pane_en.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

        hdr_en = tk.Frame(pane_en, bg=self.bg_card)
        hdr_en.pack(fill=tk.X, pady=(0, 2))

        lbl_en = tk.Label(
            hdr_en,
            text="🇺🇸 DIRECT RESPONSE (ENGLISH) — Live technical answer for interview",
            bg=self.bg_card,
            fg=self.accent_blue,
            font=("Segoe UI", 8, "bold")
        )
        lbl_en.pack(side=tk.LEFT)

        box_en = tk.Frame(pane_en, bg=self.bg_card_inner)
        box_en.pack(fill=tk.BOTH, expand=True)

        sb_en = ttk.Scrollbar(box_en)
        sb_en.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_answer_en = tk.Text(
            box_en,
            height=5,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=10,
            pady=6,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            spacing1=2,
            spacing3=2,
            yscrollcommand=sb_en.set
        )
        self.txt_answer_en.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_en.config(command=self.txt_answer_en.yview)
        self.txt_answer_en.insert(
            tk.END,
            "💡 Your direct response in ENGLISH will appear here in real time (concise bullet points for video interview)."
        )
        self.txt_answer_en.config(state=tk.DISABLED)

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
        self.entry_manual.bind("<KeyRelease>", self._on_manual_entry_key_release)

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

        # Construir contenido de Pestaña 3 (Guía Word)
        self._setup_word_guide_ui()

        # Configurar selección visual visible, atajo Ctrl+C, Ctrl+A y menú contextual
        self._setup_text_selection_and_copy()

    def _setup_pitch_ui(self):
        # 1. Barra de Selección de Pitch RF (Ericsson RAN / Arturo Ramírez) + Acciones
        nav_row1 = tk.Frame(self.frame_pitch, bg=self.bg_main, padx=12, pady=4)
        nav_row1.pack(fill=tk.X)

        lbl_rf = tk.Label(
            nav_row1,
            text="📡 RF Optimization (Ericsson):",
            bg=self.bg_main,
            fg=self.accent_yellow,
            font=("Segoe UI", 8, "bold")
        )
        lbl_rf.pack(side=tk.LEFT, padx=(0, 4))

        options_rf = [
            ("pitch_rf_es", "📡 RF Pitch (Dual ES / EN)"),
            ("pitch_rf_tech", "⚙️ KPIs & Ericsson Tech"),
            ("pitch_rf_rapido", "⚡ RF Rápido (30s)"),
            ("formacion_rf", "🎓 Formación & MBA"),
        ]

        for key, label in options_rf:
            btn = tk.Button(
                nav_row1,
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
            btn.pack(side=tk.LEFT, padx=3)
            self.pitch_buttons[key] = btn

        # Acciones a la derecha
        btn_copy_pitch = tk.Button(
            nav_row1,
            text="📋 Copiar Ambos",
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
            nav_row1,
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

        # 2. Tarjeta contenedora de lectura dividida en 2 paneles simétricos 50/50 (ES arriba / EN abajo)
        pitch_card = tk.Frame(self.frame_pitch, bg=self.bg_card, padx=12, pady=6)
        pitch_card.pack(fill=tk.BOTH, expand=True, padx=12, pady=(2, 4))

        # ================= SECCIÓN SUPERIOR: PITCH EN ESPAÑOL (50% de altura) =================
        pane_p_es = tk.Frame(pitch_card, bg=self.bg_card)
        pane_p_es.pack(fill=tk.BOTH, expand=True, pady=(0, 3))

        hdr_p_es = tk.Frame(pane_p_es, bg=self.bg_card)
        hdr_p_es.pack(fill=tk.X, pady=(0, 2))

        self.lbl_pitch_es_title = tk.Label(
            hdr_p_es,
            text="🇪🇸 PITCH EN ESPAÑOL — Javier Viveros Huesca",
            bg=self.bg_card,
            fg=self.accent_green,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_pitch_es_title.pack(side=tk.LEFT)
        self.lbl_pitch_title = self.lbl_pitch_es_title

        btn_copy_p_es = tk.Button(
            hdr_p_es,
            text="📋 Copiar ES",
            command=self._copy_pitch_es,
            bg=self.bg_card_inner,
            fg=self.text_dim,
            activebackground=self.bg_card,
            activeforeground=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 7, "bold"),
            padx=6,
            pady=1,
            cursor="hand2"
        )
        btn_copy_p_es.pack(side=tk.RIGHT)

        box_p_es = tk.Frame(pane_p_es, bg=self.bg_card_inner)
        box_p_es.pack(fill=tk.BOTH, expand=True)

        scroll_p_es = ttk.Scrollbar(box_p_es)
        scroll_p_es.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_pitch_es = tk.Text(
            box_p_es,
            height=5,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=8,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            spacing1=2,
            spacing3=2,
            yscrollcommand=scroll_p_es.set,
        )
        self.txt_pitch_es.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_p_es.config(command=self.txt_pitch_es.yview)

        # ================= SECCIÓN INFERIOR: PITCH EN INGLÉS (50% de altura) =================
        pane_p_en = tk.Frame(pitch_card, bg=self.bg_card)
        pane_p_en.pack(fill=tk.BOTH, expand=True, pady=(3, 0))

        hdr_p_en = tk.Frame(pane_p_en, bg=self.bg_card)
        hdr_p_en.pack(fill=tk.X, pady=(0, 2))

        self.lbl_pitch_en_title = tk.Label(
            hdr_p_en,
            text="🇺🇸 PITCH IN ENGLISH (60s) — Technical & Professional",
            bg=self.bg_card,
            fg=self.accent_blue,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_pitch_en_title.pack(side=tk.LEFT)

        btn_copy_p_en = tk.Button(
            hdr_p_en,
            text="📋 Copiar EN",
            command=self._copy_pitch_en,
            bg=self.bg_card_inner,
            fg=self.text_dim,
            activebackground=self.bg_card,
            activeforeground=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 7, "bold"),
            padx=6,
            pady=1,
            cursor="hand2"
        )
        btn_copy_p_en.pack(side=tk.RIGHT)

        box_p_en = tk.Frame(pane_p_en, bg=self.bg_card_inner)
        box_p_en.pack(fill=tk.BOTH, expand=True)

        scroll_p_en = ttk.Scrollbar(box_p_en)
        scroll_p_en.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_pitch_en = tk.Text(
            box_p_en,
            height=5,
            bg=self.bg_card_inner,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            padx=12,
            pady=8,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            spacing1=2,
            spacing3=2,
            yscrollcommand=scroll_p_en.set,
        )
        self.txt_pitch_en.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_p_en.config(command=self.txt_pitch_en.yview)

        # Cargar pitch inicial (RF Optimization por defecto)
        self._load_pitch("pitch_rf_es")

        # 4. Badges inferiores con métricas rápidas de RF Optimization
        badges_frame = tk.Frame(self.frame_pitch, bg=self.bg_main, padx=12, pady=4)
        badges_frame.pack(fill=tk.X)

        badges = [
            ("📶 +15 Años RF & RAN", "#34d399"),
            ("📡 Ericsson Specialist", "#38bdf8"),
            ("📊 KPIs: RTWP/PIM/DCR", "#facc15"),
            ("🛠️ TEMS / Nemo / Actix", "#a78bfa"),
            ("🎓 Ing. Electrónica + MBA", "#f472b6"),
            ("📜 Cert. Ericsson LTE", "#38bdf8"),
            ("🚀 Disp. Inmediata (México)", "#22c55e"),
        ]
        for b_text, b_color in badges:
            lbl = tk.Label(
                badges_frame,
                text=b_text,
                bg=self.bg_card,
                fg=b_color,
                font=("Segoe UI", 8, "bold"),
                padx=6,
                pady=2,
                relief=tk.FLAT
            )
            lbl.pack(side=tk.LEFT, padx=2)

    def _switch_tab(self, tab_name: str):
        self.active_tab = tab_name
        self.frame_copilot.pack_forget()
        self.frame_pitch.pack_forget()
        self.frame_word_guide.pack_forget()

        self.btn_tab_copilot.config(bg=self.bg_card, fg=self.text_dim)
        self.btn_tab_pitch.config(bg=self.bg_card, fg=self.text_dim)
        self.btn_tab_word_guide.config(bg=self.bg_card, fg=self.text_dim)

        if tab_name == "copilot":
            self.frame_copilot.pack(fill=tk.BOTH, expand=True)
            self.btn_tab_copilot.config(bg=self.accent_blue, fg="#ffffff")
            self._update_status("🟢 Copiloto en Vivo activo (Atajos: 2 Pitch, 3 Guía Word)", self.accent_green)
        elif tab_name == "pitch":
            self.frame_pitch.pack(fill=tk.BOTH, expand=True)
            self.btn_tab_pitch.config(bg=self.accent_blue, fg="#ffffff")
            self._update_status("🎯 Viendo Pitch Personal (Atajos: 1 Copiloto, 3 Guía Word)", self.accent_blue)
        elif tab_name == "word_guide":
            self.frame_word_guide.pack(fill=tk.BOTH, expand=True)
            self.btn_tab_word_guide.config(bg=self.accent_blue, fg="#ffffff")
            self._update_status("📖 Guía de Entrevista Word activa (Atajos: 1 Copiloto, 2 Pitch)", self.accent_yellow)

    @property
    def txt_pitch(self):
        return self.txt_pitch_es

    def _load_pitch(self, key: str):
        self.active_pitch_key = key
        
        # Obtener los scripts para español (arriba) e inglés (abajo)
        es_script = candidate_profile.PITCH_SCRIPTS.get(key, "")
        en_script = candidate_profile.PITCH_SCRIPTS.get("pitch_rf_en", "")

        titles_es = {
            "pitch_rf_es": "🇪🇸 PITCH PRINCIPAL RF (60–90s) — Javier Viveros Huesca",
            "pitch_rf_tech": "⚙️ ERICSSON RAN & KPIS DEEP-DIVE — Arquitectura Técnica",
            "pitch_rf_rapido": "⚡ ELEVATOR PITCH RF RÁPIDO (30s) — Resumen Ejecutivo",
            "formacion_rf": "🎓 FORMACIÓN ACADÉMICA, MBA & CERTIFICACIONES ERICSSON",
        }
        if hasattr(self, 'lbl_pitch_es_title'):
            self.lbl_pitch_es_title.config(text=titles_es.get(key, "🇪🇸 PITCH EN ESPAÑOL"))

        # Cargar panel en español (arriba)
        self.txt_pitch_es.config(state=tk.NORMAL)
        self.txt_pitch_es.delete("1.0", tk.END)
        self.txt_pitch_es.insert(tk.END, es_script)
        self.txt_pitch_es.tag_raise("sel")
        self.txt_pitch_es.config(state=tk.DISABLED)

        # Cargar panel en inglés (abajo)
        self.txt_pitch_en.config(state=tk.NORMAL)
        self.txt_pitch_en.delete("1.0", tk.END)
        self.txt_pitch_en.insert(tk.END, en_script)
        self.txt_pitch_en.tag_raise("sel")
        self.txt_pitch_en.config(state=tk.DISABLED)

        # Actualizar estilo de botones del sub-selector
        for k, btn in self.pitch_buttons.items():
            if k == key:
                btn.config(bg=self.accent_blue, fg="#ffffff")
            else:
                btn.config(bg=self.bg_card_inner, fg=self.text_dim)

    def _copy_pitch_es(self):
        txt = self.txt_pitch_es.get("1.0", tk.END).strip()
        if txt:
            self.root.clipboard_clear()
            self.root.clipboard_append(txt)
            self._update_status("📋 ¡Pitch en Español copiado al portapapeles!", self.accent_green)

    def _copy_pitch_en(self):
        txt = self.txt_pitch_en.get("1.0", tk.END).strip()
        if txt:
            self.root.clipboard_clear()
            self.root.clipboard_append(txt)
            self._update_status("📋 ¡Pitch in English copiado al portapapeles!", self.accent_blue)

    def _copy_pitch(self):
        es_txt = self.txt_pitch_es.get("1.0", tk.END).strip()
        en_txt = self.txt_pitch_en.get("1.0", tk.END).strip()
        full_txt = f"{es_txt}\n\n{'='*50}\n\n{en_txt}" if en_txt else es_txt
        if full_txt:
            self.root.clipboard_clear()
            self.root.clipboard_append(full_txt)
            self._update_status("📋 ¡Pitch bilingüe (ES + EN) copiado al portapapeles!", self.accent_blue)

    def _send_pitch_to_teleprompter(self):
        titles = {
            "pitch_rf_es": "📡 RF Optimization Engineer (Arturo Ramírez / Ericsson RAN - ES / EN)",
            "pitch_rf_tech": "⚙️ Ericsson RAN Architecture, KPIs & Layer 3 Deep-Dive",
            "pitch_rf_rapido": "⚡ Elevator Pitch RF Optimization (30s)",
            "formacion_rf": "🎓 Formación Académica, MBA & Certificaciones Oficiales",
        }
        es_script = self.txt_pitch_es.get("1.0", tk.END).strip()
        en_script = self.txt_pitch_en.get("1.0", tk.END).strip()

        if es_script:
            self.txt_question.delete("1.0", tk.END)
            self.txt_question.insert("1.0", titles.get(self.active_pitch_key, "Mi Pitch Personal"))

            self.txt_answer_es.config(state=tk.NORMAL)
            self.txt_answer_es.delete("1.0", tk.END)
            self.txt_answer_es.insert(tk.END, es_script)
            self.txt_answer_es.config(state=tk.DISABLED)

            self.txt_answer_en.config(state=tk.NORMAL)
            self.txt_answer_en.delete("1.0", tk.END)
            self.txt_answer_en.insert(tk.END, en_script)
            self.txt_answer_en.config(state=tk.DISABLED)

            self._switch_tab("copilot")
            self._update_status("⚡ Pitch cargado en Teleprompter Dual (ES / EN)", self.accent_green)

    # ------------------ PESTAÑA 3: GUÍA DE ENTREVISTA EN FORMATO WORD ------------------

    @property
    def txt_word_doc(self):
        return self.txt_word_doc_es

    def _setup_word_guide_ui(self):
        # 1. Barra Ribbon Superior (Organizada en 2 filas ergonómicas)
        ribbon_frame = tk.Frame(self.frame_word_guide, bg=self.bg_main, padx=12, pady=4)
        ribbon_frame.pack(fill=tk.X)

        # Fila 1: Selector de Módulo y Navegación Rápida
        ribbon_row1 = tk.Frame(ribbon_frame, bg=self.bg_main)
        ribbon_row1.pack(fill=tk.X, pady=(0, 4))

        lbl_badge_dual = tk.Label(
            ribbon_row1,
            text="📖 VISTA DUAL (50% ES 🇪🇸 | 50% EN 🇺🇸):",
            bg=self.bg_main,
            fg=self.accent_green,
            font=("Segoe UI", 8, "bold")
        )
        lbl_badge_dual.pack(side=tk.LEFT, padx=(0, 6))

        lbl_w_mod = tk.Label(ribbon_row1, text="📚 Módulo:", bg=self.bg_main, fg=self.accent_yellow, font=("Segoe UI", 8, "bold"))
        lbl_w_mod.pack(side=tk.LEFT, padx=(0, 4))

        self.var_word_module = tk.StringVar()
        self.combo_word_module = ttk.Combobox(
            ribbon_row1,
            textvariable=self.var_word_module,
            state="readonly"
        )
        self.combo_word_module.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.combo_word_module.bind("<<ComboboxSelected>>", self._on_word_module_changed)

        btn_prev_q = tk.Button(
            ribbon_row1,
            text="◀ Ant",
            command=self._prev_word_question,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=7,
            pady=1,
            cursor="hand2"
        )
        btn_prev_q.pack(side=tk.LEFT, padx=2)

        btn_next_q = tk.Button(
            ribbon_row1,
            text="Sig ▶",
            command=self._next_word_question,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=7,
            pady=1,
            cursor="hand2"
        )
        btn_next_q.pack(side=tk.LEFT, padx=2)

        # Fila 2: Buscador dinámico, Toggle de Índice y Botones de acción
        ribbon_row2 = tk.Frame(ribbon_frame, bg=self.bg_main)
        ribbon_row2.pack(fill=tk.X)

        lbl_w_search = tk.Label(ribbon_row2, text="🔍 Buscar:", bg=self.bg_main, fg=self.text_dim, font=("Segoe UI", 8, "bold"))
        lbl_w_search.pack(side=tk.LEFT, padx=(0, 4))

        self.var_word_search = tk.StringVar()
        self.entry_word_search = tk.Entry(
            ribbon_row2,
            textvariable=self.var_word_search,
            bg=self.bg_card,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 9),
            width=20
        )
        self.entry_word_search.pack(side=tk.LEFT, padx=(0, 6), ipady=2)
        self.entry_word_search.bind("<KeyRelease>", self._on_word_search_changed)

        self.btn_toggle_index = tk.Button(
            ribbon_row2,
            text="📑 Ocultar Índice",
            command=self._toggle_word_nav,
            bg=self.bg_card_inner,
            fg=self.text_dim,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=6,
            pady=2,
            cursor="hand2"
        )
        self.btn_toggle_index.pack(side=tk.LEFT, padx=(0, 6))

        # Botones de Acción a la derecha
        btn_open_docx = tk.Button(
            ribbon_row2,
            text="📄 Abrir Word (.docx)",
            command=self._open_word_docx,
            bg="#1d4ed8",
            fg="#ffffff",
            activebackground="#2563eb",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_open_docx.pack(side=tk.RIGHT, padx=2)

        btn_copy_w = tk.Button(
            ribbon_row2,
            text="📋 Copiar Ambos",
            command=self._copy_word_answer,
            bg=self.bg_card_inner,
            fg=self.text_color,
            relief=tk.FLAT,
            font=("Segoe UI", 8),
            padx=7,
            pady=2,
            cursor="hand2"
        )
        btn_copy_w.pack(side=tk.RIGHT, padx=2)

        btn_to_prompt = tk.Button(
            ribbon_row2,
            text="⚡ Al Teleprompter",
            command=self._send_word_answer_to_teleprompter,
            bg=self.accent_green,
            fg="#000000",
            activebackground="#16a34a",
            relief=tk.FLAT,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=2,
            cursor="hand2"
        )
        btn_to_prompt.pack(side=tk.RIGHT, padx=2)

        # 2. Contenedor Principal (Izquierda: Navegador de preguntas | Centro/Derecha: Hoja Word Dividida al 50% Vertical)
        split_frame = tk.Frame(self.frame_word_guide, bg=self.bg_main, padx=12, pady=4)
        split_frame.pack(fill=tk.BOTH, expand=True)

        # Panel Izquierdo: Lista de Preguntas (Colapsable)
        self.left_panel = tk.Frame(split_frame, bg=self.bg_card, width=200, padx=6, pady=6)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6))
        self.left_panel.pack_propagate(False)

        self.lbl_q_nav_header = tk.Label(
            self.left_panel,
            text="📋 ÍNDICE (31):",
            bg=self.bg_card,
            fg=self.accent_blue,
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_q_nav_header.pack(fill=tk.X, pady=(0, 4))

        list_box_frame = tk.Frame(self.left_panel, bg=self.bg_card_inner)
        list_box_frame.pack(fill=tk.BOTH, expand=True)

        sb_list = ttk.Scrollbar(list_box_frame)
        sb_list.pack(side=tk.RIGHT, fill=tk.Y)

        self.list_word_questions = tk.Listbox(
            list_box_frame,
            bg=self.bg_card_inner,
            fg="#ffffff",
            selectbackground=self.accent_blue,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            activestyle="none",
            font=("Segoe UI", 9),
            yscrollcommand=sb_list.set
        )
        self.list_word_questions.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_list.config(command=self.list_word_questions.yview)
        self.list_word_questions.bind("<<ListboxSelect>>", self._on_word_question_selected)

        # Panel Derecho: Visualizador Dividido Verticalmente en 2 Mitades (ES 50% Izq | EN 50% Der)
        self.docs_container_panel = tk.Frame(split_frame, bg=self.bg_main)
        self.docs_container_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.docs_container_panel.grid_columnconfigure(0, weight=1, uniform="doc_col")
        self.docs_container_panel.grid_columnconfigure(1, weight=1, uniform="doc_col")
        self.docs_container_panel.grid_rowconfigure(0, weight=1)

        # ================= LADO IZQUIERDO: DOCUMENTO WORD EN ESPAÑOL (50% de ancho) =================
        left_doc_frame = tk.Frame(self.docs_container_panel, bg=self.bg_card, padx=4, pady=4)
        left_doc_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 3))

        page_card_es = tk.Frame(left_doc_frame, bg="#FFFFFF", padx=10, pady=8)
        page_card_es.pack(fill=tk.BOTH, expand=True)

        word_header_strip_es = tk.Frame(page_card_es, bg="#FFFFFF")
        word_header_strip_es.pack(fill=tk.X, pady=(0, 3))

        lbl_hdr_es_left = tk.Label(
            word_header_strip_es,
            text="🇪🇸 AMDOCS MX | RF Optimization (Español)",
            bg="#FFFFFF",
            fg="#166534",
            font=("Calibri", 8, "bold")
        )
        lbl_hdr_es_left.pack(side=tk.LEFT)

        btn_copy_es = tk.Button(
            word_header_strip_es,
            text="📋 Copiar ES",
            command=self._copy_word_answer_es,
            bg="#F1F5F9",
            fg="#1E293B",
            relief=tk.FLAT,
            font=("Segoe UI", 7, "bold"),
            padx=5,
            pady=0,
            cursor="hand2"
        )
        btn_copy_es.pack(side=tk.RIGHT)

        div_line_es = tk.Frame(page_card_es, bg="#CBD5E1", height=1)
        div_line_es.pack(fill=tk.X, pady=(2, 4))

        doc_box_es = tk.Frame(page_card_es, bg="#FFFFFF")
        doc_box_es.pack(fill=tk.BOTH, expand=True)

        self.sb_doc_es = ttk.Scrollbar(doc_box_es)
        self.sb_doc_es.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_word_doc_es = tk.Text(
            doc_box_es,
            width=10,
            bg="#FFFFFF",
            fg="#0F172A",
            insertbackground="#0F172A",
            relief=tk.FLAT,
            bd=0,
            font=("Calibri", 10),
            wrap=tk.WORD,
            spacing1=2,
            spacing3=2,
            yscrollcommand=self._sync_scroll_es
        )
        self.txt_word_doc_es.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sb_doc_es.config(command=self._on_word_scrollbar_scroll)

        div_line_bot_es = tk.Frame(page_card_es, bg="#CBD5E1", height=1)
        div_line_bot_es.pack(fill=tk.X, pady=(4, 2))

        lbl_foot_es = tk.Label(
            page_card_es,
            text="Javier Viveros Huesca | Formato Word Oficial (ES)",
            bg="#FFFFFF",
            fg="#94A3B8",
            font=("Calibri", 7, "italic")
        )
        lbl_foot_es.pack(fill=tk.X)

        # ================= LADO DERECHO: DOCUMENTO WORD EN INGLÉS (50% de ancho) =================
        right_doc_frame = tk.Frame(self.docs_container_panel, bg=self.bg_card, padx=4, pady=4)
        right_doc_frame.grid(row=0, column=1, sticky="nsew", padx=(3, 0))

        page_card_en = tk.Frame(right_doc_frame, bg="#FFFFFF", padx=10, pady=8)
        page_card_en.pack(fill=tk.BOTH, expand=True)

        word_header_strip_en = tk.Frame(page_card_en, bg="#FFFFFF")
        word_header_strip_en.pack(fill=tk.X, pady=(0, 3))

        lbl_hdr_en_left = tk.Label(
            word_header_strip_en,
            text="🇺🇸 AMDOCS MX | RF Optimization (English)",
            bg="#FFFFFF",
            fg="#1E40AF",
            font=("Calibri", 8, "bold")
        )
        lbl_hdr_en_left.pack(side=tk.LEFT)

        btn_copy_en = tk.Button(
            word_header_strip_en,
            text="📋 Copy EN",
            command=self._copy_word_answer_en,
            bg="#F1F5F9",
            fg="#1E293B",
            relief=tk.FLAT,
            font=("Segoe UI", 7, "bold"),
            padx=5,
            pady=0,
            cursor="hand2"
        )
        btn_copy_en.pack(side=tk.RIGHT)

        div_line_en = tk.Frame(page_card_en, bg="#CBD5E1", height=1)
        div_line_en.pack(fill=tk.X, pady=(2, 4))

        doc_box_en = tk.Frame(page_card_en, bg="#FFFFFF")
        doc_box_en.pack(fill=tk.BOTH, expand=True)

        self.sb_doc_en = ttk.Scrollbar(doc_box_en)
        self.sb_doc_en.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt_word_doc_en = tk.Text(
            doc_box_en,
            width=10,
            bg="#FFFFFF",
            fg="#0F172A",
            insertbackground="#0F172A",
            relief=tk.FLAT,
            bd=0,
            font=("Calibri", 10),
            wrap=tk.WORD,
            spacing1=2,
            spacing3=2,
            yscrollcommand=self._sync_scroll_en
        )
        self.txt_word_doc_en.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sb_doc_en.config(command=self._on_word_scrollbar_scroll)

        # Vincular rueda del ratón (MouseWheel) para scroll sincronizado simultáneo
        self.txt_word_doc_es.bind("<MouseWheel>", self._on_word_mousewheel)
        self.txt_word_doc_en.bind("<MouseWheel>", self._on_word_mousewheel)

        div_line_bot_en = tk.Frame(page_card_en, bg="#CBD5E1", height=1)
        div_line_bot_en.pack(fill=tk.X, pady=(4, 2))

        lbl_foot_en = tk.Label(
            page_card_en,
            text="Javier Viveros Huesca | Official Word Format (EN)",
            bg="#FFFFFF",
            fg="#94A3B8",
            font=("Calibri", 7, "italic")
        )
        lbl_foot_en.pack(fill=tk.X)

        # Configurar estilos de tags para ambos documentos
        self._configure_word_tags(self.txt_word_doc_es)
        self._configure_word_tags(self.txt_word_doc_en)

        # Inicializar datos en la vista (usando los módulos y preguntas en español como base sincronizada)
        self._populate_word_modules()
        self._load_word_module_questions(0)

    def _configure_word_tags(self, txt_widget: tk.Text):
        txt_widget.tag_configure("doc_main_title", font=("Calibri", 12, "bold"), foreground="#002561", spacing1=4, spacing3=2)
        txt_widget.tag_configure("doc_subtitle", font=("Calibri", 10, "bold"), foreground="#102A43", spacing1=1, spacing3=3)
        txt_widget.tag_configure("doc_meta", font=("Calibri", 8), foreground="#475569", background="#F8FAFC", lmargin1=10, lmargin2=10, rmargin=10, spacing1=2, spacing3=2)
        txt_widget.tag_configure("mod_title", font=("Calibri", 11, "bold"), foreground="#002561", background="#EEF2FF", lmargin1=6, lmargin2=6, rmargin=6, spacing1=4, spacing3=3)
        txt_widget.tag_configure("q_title", font=("Calibri", 10, "bold"), foreground="#1E3A8A", spacing1=5, spacing3=2)
        txt_widget.tag_configure("strategy_hdr", font=("Calibri", 9, "bold"), background="#F0FFF4", foreground="#166534", lmargin1=10, lmargin2=10, rmargin=10, spacing1=3, spacing3=1)
        txt_widget.tag_configure("strategy_body", font=("Calibri", 9), background="#F0FFF4", foreground="#14532D", lmargin1=10, lmargin2=10, rmargin=10, spacing1=1, spacing3=3)
        txt_widget.tag_configure("answer_hdr", font=("Calibri", 10, "bold"), background="#F0F4F8", foreground="#002561", lmargin1=10, lmargin2=10, rmargin=10, spacing1=4, spacing3=2)
        txt_widget.tag_configure("answer_body", font=("Calibri", 9), background="#F0F4F8", foreground="#0F172A", lmargin1=10, lmargin2=10, rmargin=10, spacing1=2, spacing3=4)
        txt_widget.tag_configure("sec_hdr", font=("Calibri", 9, "bold"), foreground="#1E293B", spacing1=4, spacing3=2)
        txt_widget.tag_configure("code_block", font=("Consolas", 8), background="#F1F5F9", foreground="#0F172A", lmargin1=10, lmargin2=10, rmargin=10, spacing1=2, spacing3=3)
        txt_widget.tag_configure("footer", font=("Calibri", 8, "italic"), foreground="#94A3B8", justify="center", spacing1=6)

        # Elevar la etiqueta de selección al nivel superior para que el resaltado sea visible sobre cualquier fondo
        txt_widget.tag_configure("sel", background="#2563eb", foreground="#ffffff")
        txt_widget.tag_raise("sel")

    def _on_word_scrollbar_scroll(self, *args):
        self.txt_word_doc_es.yview(*args)
        self.txt_word_doc_en.yview(*args)

    def _sync_scroll_es(self, first, last):
        if hasattr(self, 'sb_doc_es'):
            self.sb_doc_es.set(first, last)
        if not self._is_syncing_word_scroll:
            self._is_syncing_word_scroll = True
            try:
                self.txt_word_doc_en.yview_moveto(first)
                if hasattr(self, 'sb_doc_en'):
                    self.sb_doc_en.set(first, last)
            finally:
                self._is_syncing_word_scroll = False

    def _sync_scroll_en(self, first, last):
        if hasattr(self, 'sb_doc_en'):
            self.sb_doc_en.set(first, last)
        if not self._is_syncing_word_scroll:
            self._is_syncing_word_scroll = True
            try:
                self.txt_word_doc_es.yview_moveto(first)
                if hasattr(self, 'sb_doc_es'):
                    self.sb_doc_es.set(first, last)
            finally:
                self._is_syncing_word_scroll = False

    def _on_word_mousewheel(self, event):
        delta = int(-1 * (event.delta / 120))
        self.txt_word_doc_es.yview_scroll(delta, "units")
        self.txt_word_doc_en.yview_scroll(delta, "units")
        return "break"

    def _toggle_word_nav(self):
        if self.left_panel.winfo_ismapped():
            self.left_panel.pack_forget()
            self.btn_toggle_index.config(text="📑 Mostrar Índice", fg=self.accent_blue)
        else:
            self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 6), before=self.docs_container_panel)
            self.btn_toggle_index.config(text="📑 Ocultar Índice", fg=self.text_dim)

    def _prev_word_question(self):
        if not self.displayed_questions:
            return
        sel = self.list_word_questions.curselection()
        curr_idx = sel[0] if sel else 0
        new_idx = max(0, curr_idx - 1)
        self.list_word_questions.selection_clear(0, tk.END)
        self.list_word_questions.selection_set(new_idx)
        self.list_word_questions.see(new_idx)
        self._on_word_question_selected()

    def _next_word_question(self):
        if not self.displayed_questions:
            return
        sel = self.list_word_questions.curselection()
        curr_idx = sel[0] if sel else 0
        new_idx = min(len(self.displayed_questions) - 1, curr_idx + 1)
        self.list_word_questions.selection_clear(0, tk.END)
        self.list_word_questions.selection_set(new_idx)
        self.list_word_questions.see(new_idx)
        self._on_word_question_selected()

    def _populate_word_modules(self):
        mod_titles = ["📖 [Todos los Módulos (31 Preguntas) / All Topics]"]
        for m in self.rf_word_guide_es.modules:
            mod_titles.append(m.title.strip())
        self.combo_word_module.config(values=mod_titles)
        self.combo_word_module.current(1 if len(mod_titles) > 1 else 0)

    def _on_word_module_changed(self, event=None):
        idx = self.combo_word_module.current()
        if idx == 0:
            self.displayed_questions = list(self.rf_word_guide_es.all_questions)
        else:
            mod_idx = idx - 1
            if 0 <= mod_idx < len(self.rf_word_guide_es.modules):
                self.displayed_questions = list(self.rf_word_guide_es.modules[mod_idx].questions)
            else:
                self.displayed_questions = list(self.rf_word_guide_es.all_questions)
        self._populate_word_questions_list(self.displayed_questions)

    def _on_word_search_changed(self, event=None):
        q = self.var_word_search.get().strip()
        if not q:
            self._on_word_module_changed()
            return
        results = self.rf_word_guide_es.search(q)
        self.displayed_questions = results
        self._populate_word_questions_list(results)

    def _populate_word_questions_list(self, questions: List[QuestionItem]):
        self.list_word_questions.delete(0, tk.END)
        self.lbl_q_nav_header.config(text=f"📋 ÍNDICE ({len(questions)}):")
        for q in questions:
            self.list_word_questions.insert(tk.END, q.short_title)
        if questions:
            self.list_word_questions.selection_set(0)
            self._render_word_question(questions[0])

    def _on_word_question_selected(self, event=None):
        sel = self.list_word_questions.curselection()
        if not sel:
            return
        idx = sel[0]
        if 0 <= idx < len(self.displayed_questions):
            self.selected_question_item = self.displayed_questions[idx]
            self._render_word_question(self.selected_question_item)

    def _render_word_question(self, q: QuestionItem):
        self.selected_question_item = q
        q_num = q.num

        # Buscar versión en español y versión en inglés correspondiente
        q_es = next((item for item in self.rf_word_guide_es.all_questions if item.num == q_num), q)
        q_en = next((item for item in self.rf_word_guide_en.all_questions if item.num == q_num), None)

        self._render_single_doc(self.txt_word_doc_es, q_es, "es")
        self._render_single_doc(self.txt_word_doc_en, q_en, "en")

    def _render_single_doc(self, txt_widget: tk.Text, q: Optional[QuestionItem], lang: str):
        txt_widget.config(state=tk.NORMAL)
        txt_widget.delete("1.0", tk.END)

        if not q:
            msg = "⚠️ No hay versión disponible para esta pregunta en este idioma.\n" if lang == "es" else "⚠️ No English version available for this specific topic.\n"
            txt_widget.insert(tk.END, msg, "doc_meta")
            txt_widget.tag_raise("sel")
            txt_widget.config(state=tk.DISABLED)
            return

        # Módulo Header
        txt_widget.insert(tk.END, f"📌 {q.module_title}\n\n", "mod_title")

        # Título de Pregunta
        txt_widget.insert(tk.END, f"{q.title}\n\n", "q_title")

        # Estrategia y Tono
        if q.strategy:
            strat_label = "🎯 ESTRATEGIA Y TONO:\n" if lang == "es" else "🎯 STRATEGY & TONE:\n"
            txt_widget.insert(tk.END, strat_label, "strategy_hdr")
            txt_widget.insert(tk.END, f"{q.strategy}\n\n", "strategy_body")

        # Respuesta Modelo
        if q.answer:
            header_label = "💬 RESPUESTA MODELO (Lo que debes responder):\n" if lang == "es" else "💬 MODEL ANSWER (What you should say):\n"
            txt_widget.insert(tk.END, header_label, "answer_hdr")
            ans_clean = "\n".join(re.sub(r'^\s*>\s?', '', line) for line in q.answer.splitlines())
            txt_widget.insert(tk.END, f"{ans_clean}\n\n", "answer_body")

        # Secciones extra (fórmulas, tablas, comandos, troubleshooting)
        for s_title, s_body in q.extra_sections:
            s_clean = "\n".join(re.sub(r'^\s*>\s?', '', line) for line in s_body.splitlines())
            if any(k in s_title.lower() for k in ["comando", "tabla", "fórmula", "parámetro", "command", "table", "cheat", "phrases", "pronunciation"]):
                txt_widget.insert(tk.END, f"{s_title}\n", "sec_hdr")
                txt_widget.insert(tk.END, f"{s_clean}\n\n", "code_block")
            else:
                txt_widget.insert(tk.END, f"{s_title}\n", "sec_hdr")
                txt_widget.insert(tk.END, f"{s_clean}\n\n", "strategy_body")

        txt_widget.insert(tk.END, "―" * 50 + "\n", "doc_meta")
        footer_text = "Preparación Entrevista Técnica – Javier Viveros Huesca | Formato Word Oficial (ES)\n" if lang == "es" else "Technical Interview Preparation – Javier Viveros Huesca | Official Word Format (EN)\n"
        txt_widget.insert(tk.END, footer_text, "footer")
        txt_widget.tag_raise("sel")
        txt_widget.config(state=tk.DISABLED)

    def _load_word_module_questions(self, mod_idx: int):
        if 0 <= mod_idx < len(self.rf_word_guide_es.modules):
            self.displayed_questions = list(self.rf_word_guide_es.modules[mod_idx].questions)
        else:
            self.displayed_questions = list(self.rf_word_guide_es.all_questions)
        self._populate_word_questions_list(self.displayed_questions)

    def _send_word_answer_to_teleprompter(self):
        if not self.selected_question_item:
            messagebox.showinfo("Guía Word", "Selecciona una pregunta de la lista primero.")
            return

        q = self.selected_question_item
        q_num = q.num

        # Buscar versión en español y versión en inglés por número de pregunta
        q_es = next((item for item in self.rf_word_guide_es.all_questions if item.num == q_num), None)
        q_en = next((item for item in self.rf_word_guide_en.all_questions if item.num == q_num), None)

        es_text = q_es.clean_answer_for_teleprompter if q_es and q_es.clean_answer_for_teleprompter else (q_es.raw_text if q_es else q.clean_answer_for_teleprompter)
        en_text = q_en.clean_answer_for_teleprompter if q_en and q_en.clean_answer_for_teleprompter else (q_en.raw_text if q_en else q.clean_answer_for_teleprompter)

        self.txt_question.delete("1.0", tk.END)
        self.txt_question.insert("1.0", q.title)

        # Cargar panel superior (Español)
        self.txt_answer_es.config(state=tk.NORMAL)
        self.txt_answer_es.delete("1.0", tk.END)
        self.txt_answer_es.insert(tk.END, es_text)
        self.txt_answer_es.tag_raise("sel")
        self.txt_answer_es.config(state=tk.DISABLED)

        # Cargar panel inferior (Inglés)
        self.txt_answer_en.config(state=tk.NORMAL)
        self.txt_answer_en.delete("1.0", tk.END)
        self.txt_answer_en.insert(tk.END, en_text)
        self.txt_answer_en.tag_raise("sel")
        self.txt_answer_en.config(state=tk.DISABLED)

        self._switch_tab("copilot")
        self._update_status(f"⚡ Q{q.num} cargada en Teleprompter Dual (ES / EN)", self.accent_green)

    def _copy_word_answer_es(self):
        if not self.selected_question_item:
            return
        q_num = self.selected_question_item.num
        q_es = next((item for item in self.rf_word_guide_es.all_questions if item.num == q_num), self.selected_question_item)
        ans_text = q_es.clean_answer_for_teleprompter or q_es.raw_text
        self.root.clipboard_clear()
        self.root.clipboard_append(ans_text)
        self._update_status(f"📋 Respuesta Q{q_num} (Español) copiada al portapapeles", self.accent_green)

    def _copy_word_answer_en(self):
        if not self.selected_question_item:
            return
        q_num = self.selected_question_item.num
        q_en = next((item for item in self.rf_word_guide_en.all_questions if item.num == q_num), None)
        ans_text = (q_en.clean_answer_for_teleprompter if q_en else "") or (q_en.raw_text if q_en else "")
        if ans_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(ans_text)
            self._update_status(f"📋 Answer Q{q_num} (English) copied to clipboard", self.accent_blue)

    def _copy_word_answer(self):
        if not self.selected_question_item:
            return
        q_num = self.selected_question_item.num
        q_es = next((item for item in self.rf_word_guide_es.all_questions if item.num == q_num), self.selected_question_item)
        q_en = next((item for item in self.rf_word_guide_en.all_questions if item.num == q_num), None)
        es_text = q_es.clean_answer_for_teleprompter or q_es.raw_text
        en_text = (q_en.clean_answer_for_teleprompter if q_en else "") or (q_en.raw_text if q_en else "")
        full = f"=== ESPAÑOL ===\n{es_text}\n\n{'='*50}\n\n=== ENGLISH ===\n{en_text}" if en_text else es_text
        self.root.clipboard_clear()
        self.root.clipboard_append(full)
        self._update_status(f"📋 Respuestas Q{q_num} (ES + EN) copiadas al portapapeles", self.accent_blue)

    def _open_word_docx(self):
        success = self.rf_word_guide_es.open_docx_in_word()
        if success:
            self._update_status("📄 Abriendo documento oficial en Microsoft Word...", self.accent_blue)
        else:
            messagebox.showwarning("Microsoft Word", "No se encontró el archivo .docx o Microsoft Word en este equipo.")

    def _open_word_md(self):
        success = self.rf_word_guide_es.open_md_in_editor()
        if success:
            self._update_status("📑 Abriendo documento Markdown...", self.accent_blue)
        else:
            messagebox.showwarning("Markdown", "No se encontró el archivo .md.")

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

    @property
    def txt_answer(self) -> tk.Text:
        """Compatibilidad para acceder al teleprompter superior en español."""
        return self.txt_answer_es

    def _on_global_key_press(self, event):
        focused = getattr(event, "widget", None) or self.root.focus_get()
        if focused is not None:
            w_class = focused.__class__.__name__
            if isinstance(focused, (tk.Entry, tk.Text, ttk.Entry, ttk.Combobox)) or w_class in (
                "Entry", "Text", "Combobox", "TCombobox", "TEntry"
            ):
                return  # Permitir escritura normal del dígito 1, 2 o 3 en cuadros de texto

        ks = getattr(event, "keysym", "")
        ch = getattr(event, "char", "")
        if ks in ("1", "KP_1", "F1") or ch == "1":
            self._switch_tab("copilot")
            return "break"
        elif ks in ("2", "KP_2", "F2") or ch == "2":
            self._switch_tab("pitch")
            return "break"
        elif ks in ("3", "KP_3", "F3") or ch == "3":
            self._switch_tab("word_guide")
            return "break"

    def _copy_answer(self):
        self._copy_answer_es()

    def _copy_answer_es(self):
        content = self.txt_answer_es.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self._update_status("📋 ¡Respuesta en Español copiada!", self.accent_green)

    def _copy_answer_en(self):
        content = self.txt_answer_en.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self._update_status("📋 ¡Respuesta en Inglés copiada!", self.accent_blue)

    def _setup_text_selection_and_copy(self):
        """Habilita selección visible, atajo Ctrl+C, Ctrl+A y menú contextual en todos los cuadros de texto."""
        text_widgets = [
            getattr(self, "txt_question", None),
            getattr(self, "txt_answer_es", None),
            getattr(self, "txt_answer_en", None),
            getattr(self, "txt_pitch_es", None),
            getattr(self, "txt_pitch_en", None),
            getattr(self, "txt_word_doc_es", None),
            getattr(self, "txt_word_doc_en", None),
        ]
        for tw in text_widgets:
            if tw is not None:
                self._enable_text_copy_and_selection(tw)

        entry_widgets = [
            getattr(self, "entry_manual", None),
            getattr(self, "entry_word_search", None),
        ]
        for ew in entry_widgets:
            if ew is not None:
                self._enable_entry_copy_and_selection(ew)

    def _enable_text_copy_and_selection(self, widget: tk.Text):
        """Habilita selección de texto visible, atajo Ctrl+C, Ctrl+A y menú contextual con clic derecho."""
        widget.config(
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            inactiveselectbackground="#1d4ed8",
            exportselection=False
        )
        widget.tag_configure("sel", background="#2563eb", foreground="#ffffff")
        widget.tag_raise("sel")

        # Asegurar foco al hacer clic para que los atajos respondan inmediatamente
        widget.bind("<Button-1>", lambda e: widget.focus_set(), add="+")

        # Atajos directos de copia
        widget.bind("<Control-c>", self._copy_selected_text)
        widget.bind("<Control-C>", self._copy_selected_text)
        widget.bind("<<Copy>>", self._copy_selected_text)

        # Atajo para seleccionar todo
        widget.bind("<Control-a>", lambda e: self._select_all_text(widget))
        widget.bind("<Control-A>", lambda e: self._select_all_text(widget))

        # Menú contextual con clic derecho
        widget.bind("<Button-3>", lambda e: self._show_text_context_menu(e, widget))

    def _enable_entry_copy_and_selection(self, entry_widget):
        entry_widget.config(
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            exportselection=False
        )
        entry_widget.bind("<Control-a>", lambda e: (entry_widget.select_range(0, tk.END), "break")[1])
        entry_widget.bind("<Control-A>", lambda e: (entry_widget.select_range(0, tk.END), "break")[1])
        entry_widget.bind("<Button-3>", lambda e: self._show_entry_context_menu(e, entry_widget))

    def _show_text_context_menu(self, event, widget: tk.Text):
        menu = tk.Menu(self.root, tearoff=0, bg=self.bg_card, fg=self.text_color, activebackground="#2563eb", activeforeground="#ffffff")
        has_sel = False
        try:
            has_sel = bool(widget.tag_ranges("sel"))
        except Exception:
            pass

        if has_sel:
            menu.add_command(label="📋 Copiar selección  (Ctrl+C)", command=lambda: self._copy_selected_text(event=None, target_widget=widget))
        else:
            menu.add_command(label="📋 Copiar todo el texto", command=lambda: self._copy_full_widget_text(widget))

        menu.add_command(label="✨ Seleccionar todo  (Ctrl+A)", command=lambda: self._select_all_text(widget))
        menu.tk_popup(event.x_root, event.y_root)

    def _show_entry_context_menu(self, event, entry_widget):
        menu = tk.Menu(self.root, tearoff=0, bg=self.bg_card, fg=self.text_color, activebackground="#2563eb", activeforeground="#ffffff")
        if entry_widget.selection_present():
            menu.add_command(label="📋 Copiar selección  (Ctrl+C)", command=lambda: self._copy_selected_text(event=None, target_widget=entry_widget))
        else:
            menu.add_command(label="📋 Copiar todo", command=lambda: self._copy_full_entry_text(entry_widget))
        menu.add_command(label="✨ Seleccionar todo  (Ctrl+A)", command=lambda: entry_widget.select_range(0, tk.END))
        menu.tk_popup(event.x_root, event.y_root)

    def _select_all_text(self, widget: tk.Text):
        try:
            widget.tag_add("sel", "1.0", "end-1c")
            widget.tag_raise("sel")
            widget.focus_set()
        except Exception:
            pass
        return "break"

    def _copy_full_widget_text(self, widget: tk.Text):
        try:
            txt = widget.get("1.0", tk.END).strip()
            if txt:
                self.root.clipboard_clear()
                self.root.clipboard_append(txt)
                self._update_status(f"📋 Texto copiado al portapapeles ({len(txt)} caracteres)", self.accent_green)
        except Exception:
            pass

    def _copy_full_entry_text(self, entry_widget):
        try:
            txt = entry_widget.get().strip()
            if txt:
                self.root.clipboard_clear()
                self.root.clipboard_append(txt)
                self._update_status("📋 Texto copiado al portapapeles", self.accent_green)
        except Exception:
            pass

    def _copy_selected_text(self, event=None, target_widget=None):
        focused = target_widget or getattr(event, "widget", None) or self.root.focus_get()
        widgets_to_check = []
        if focused and hasattr(focused, "get"):
            widgets_to_check.append(focused)

        # Widgets de texto prioritarios en la aplicación
        candidates = [
            getattr(self, "txt_word_doc_es", None),
            getattr(self, "txt_word_doc_en", None),
            getattr(self, "txt_answer_es", None),
            getattr(self, "txt_answer_en", None),
            getattr(self, "txt_pitch_es", None),
            getattr(self, "txt_pitch_en", None),
            getattr(self, "txt_question", None),
            getattr(self, "entry_manual", None),
            getattr(self, "entry_word_search", None),
        ]
        for c in candidates:
            if c and c not in widgets_to_check:
                widgets_to_check.append(c)

        for w in widgets_to_check:
            try:
                if isinstance(w, tk.Text):
                    ranges = w.tag_ranges("sel")
                    if ranges:
                        sel = w.get(tk.SEL_FIRST, tk.SEL_LAST)
                        if sel:
                            self.root.clipboard_clear()
                            self.root.clipboard_append(sel)
                            self._update_status(f"📋 Texto copiado ({len(sel)} caracteres)", self.accent_green)
                            return "break"
                elif isinstance(w, (tk.Entry, ttk.Entry)):
                    if w.selection_present():
                        sel = w.selection_get()
                        if sel:
                            self.root.clipboard_clear()
                            self.root.clipboard_append(sel)
                            self._update_status("📋 Texto copiado", self.accent_green)
                            return "break"
            except (tk.TclError, AttributeError):
                continue

        # Intento de selección nativa del sistema
        try:
            sel = self.root.selection_get()
            if sel:
                self.root.clipboard_clear()
                self.root.clipboard_append(sel)
                self._update_status("📋 Texto copiado", self.accent_green)
                return "break"
        except (tk.TclError, AttributeError):
            pass
        return None

    def _clear_screen(self):
        self.txt_question.delete("1.0", tk.END)
        self.entry_manual.delete(0, tk.END)
        self.entry_manual.insert(0, "O pega/escribe una pregunta del chat aquí...")

        self.current_matched_word_q = None
        self.current_matched_word_list = []
        if hasattr(self, 'chips_word_container'):
            for child in self.chips_word_container.winfo_children():
                child.destroy()
        if hasattr(self, 'frame_word_match'):
            self.frame_word_match.pack_forget()

        self.txt_answer_es.config(state=tk.NORMAL)
        self.txt_answer_es.delete("1.0", tk.END)
        self.txt_answer_es.insert(tk.END, "Esperando nueva intervención...")
        self.txt_answer_es.config(state=tk.DISABLED)

        self.txt_answer_en.config(state=tk.NORMAL)
        self.txt_answer_en.delete("1.0", tk.END)
        self.txt_answer_en.insert(tk.END, "Waiting for new question...")
        self.txt_answer_en.config(state=tk.DISABLED)
        self.current_answer_lang = "dual"

    def _on_question_key_release(self, event=None):
        if event and event.keysym in ("Up", "Down", "Left", "Right", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Tab"):
            return
        text = self.txt_question.get("1.0", tk.END).strip()
        self._check_and_display_word_match(text)

    def _on_manual_entry_key_release(self, event=None):
        if event and event.keysym in ("Up", "Down", "Left", "Right", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Tab"):
            return
        text = self.entry_manual.get().strip()
        if text and text != "O pega/escribe una pregunta del chat aquí...":
            self._check_and_display_word_match(text)
        else:
            if hasattr(self, 'frame_word_match'):
                self.frame_word_match.pack_forget()

    def _check_and_display_word_match(self, text: str):
        """Busca todas las coincidencias temáticas con la Guía Word y despliega botones de enlace."""
        if not text or len(text.strip()) < 2:
            self.current_matched_word_q = None
            self.current_matched_word_list = []
            if hasattr(self, 'frame_word_match'):
                self.frame_word_match.pack_forget()
            return

        matches = self.rf_word_guide_es.find_all_matches(text, limit=4)
        if matches:
            # Ordenar de menor a mayor por módulo y número de pregunta
            matches.sort(key=lambda m: (m.get("module_num", 0), m.get("q_num", 0)))
            self.current_matched_word_list = matches
            self.current_matched_word_q = max(matches, key=lambda m: m.get("score", 0))

            # Limpiar botones/chips anteriores
            if hasattr(self, 'chips_word_container'):
                for child in self.chips_word_container.winfo_children():
                    child.destroy()

            count = len(matches)
            max_len = 22 if count >= 4 else (26 if count == 3 else 34)
            if count == 1:
                self.lbl_word_match_header.config(
                    text="📖 COINCIDENCIA EN GUÍA WORD OFICIAL:"
                )
                self.lbl_word_match_hint.config(
                    text="(Haz clic para abrir el tema en Guía Word 3)"
                )
            else:
                self.lbl_word_match_header.config(
                    text=f"📖 COINCIDENCIAS EN GUÍA WORD ({count} POSIBILIDADES ENCONTRADAS):"
                )
                self.lbl_word_match_hint.config(
                    text="(Haz clic en cualquier opción para ir directo a esa pregunta)"
                )

            for m in matches:
                q_num = m["q_num"]
                mod_num = m["module_num"]
                title_clean = re.sub(r'^(Pregunta|Question)\s*\d+:\s*', '', m["title"], flags=re.IGNORECASE)
                title_clean = title_clean.strip('"?¿!¡\' ')
                if len(title_clean) > max_len:
                    title_clean = title_clean[:max_len - 2] + "..."

                btn_text = f"📖 Q{q_num}: {title_clean} (Mód {mod_num}) ➔"

                btn_chip = tk.Button(
                    self.chips_word_container,
                    text=btn_text,
                    command=lambda qn=q_num: self._jump_to_matched_word_question(qn),
                    bg="#1e293b",
                    fg="#38bdf8",
                    activebackground=self.accent_blue,
                    activeforeground="#ffffff",
                    relief=tk.GROOVE,
                    bd=1,
                    font=("Segoe UI", 8, "bold"),
                    padx=8,
                    pady=2,
                    cursor="hand2"
                )
                btn_chip.pack(side=tk.LEFT, padx=(0, 6), pady=2)

                btn_chip.bind("<Enter>", lambda e, b=btn_chip: b.config(bg=self.accent_blue, fg="#ffffff"))
                btn_chip.bind("<Leave>", lambda e, b=btn_chip: b.config(bg="#1e293b", fg="#38bdf8"))

            self.frame_word_match.pack(fill=tk.X, pady=(3, 0))
        else:
            self.current_matched_word_q = None
            self.current_matched_word_list = []
            if hasattr(self, 'frame_word_match'):
                self.frame_word_match.pack_forget()

    def _jump_to_matched_word_question(self, q_num: Optional[int] = None):
        """Desplaza la interfaz directamente a la pregunta correspondiente en la Guía Word."""
        target_num = q_num
        if target_num is None and self.current_matched_word_q:
            target_num = self.current_matched_word_q.get("q_num")
        if not target_num:
            self._switch_tab("word_guide")
            return

        # 1. Cambiar a la pestaña de Guía Word (3)
        self._switch_tab("word_guide")

        # 2. Localizar el objeto de pregunta en español
        q_item = next((q for q in self.rf_word_guide_es.all_questions if q.num == target_num), None)
        if not q_item:
            return

        # 3. Encontrar y seleccionar el módulo correspondiente en combo_word_module
        mod_idx = 0
        for i, m in enumerate(self.rf_word_guide_es.modules):
            if any(q.num == target_num for q in m.questions):
                mod_idx = i + 1  # 1-indexed porque index 0 es "Todos los módulos"
                break

        if hasattr(self, 'combo_word_module') and 0 <= mod_idx < len(self.combo_word_module["values"]):
            self.combo_word_module.current(mod_idx)
            self._on_word_module_changed()

        # 4. Seleccionar y hacer scroll a la pregunta en el índice list_word_questions
        try:
            list_idx = next(i for i, q in enumerate(self.displayed_questions) if q.num == target_num)
            self.list_word_questions.selection_clear(0, tk.END)
            self.list_word_questions.selection_set(list_idx)
            self.list_word_questions.see(list_idx)
        except StopIteration:
            pass

        # 5. Renderizar en ambos documentos (ES y EN) y desplazar al inicio
        self._render_word_question(q_item)
        self.txt_word_doc_es.yview_moveto(0.0)
        self.txt_word_doc_en.yview_moveto(0.0)

        # 6. Notificación visual en status bar
        self._update_status(f"📖 Guía Word: Mostrando Q{target_num} ({q_item.short_title})", self.accent_green)

    def _on_language_changed(self, event=None):
        sel = self.lang_var.get()
        if "Solo Español" in sel:
            self._update_status("🌐 Modo de respuesta: Solo Español", self.accent_blue)
        elif "Only English" in sel:
            self._update_status("🌐 Mode: English only", self.accent_blue)
        else:
            self._update_status("⚡ Modo de respuesta: Teleprompter Dual (ES + EN)", self.accent_green)

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
        if not edited_text or edited_text.startswith("Esperando"):
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
                    self._stream_full_text = ""
                    self.txt_answer_es.config(state=tk.NORMAL)
                    self.txt_answer_es.delete("1.0", tk.END)
                    self.txt_answer_es.config(state=tk.DISABLED)

                    self.txt_answer_en.config(state=tk.NORMAL)
                    self.txt_answer_en.delete("1.0", tk.END)
                    self.txt_answer_en.insert(tk.END, "⏳ Generando respuesta en inglés...")
                    self.txt_answer_en.config(state=tk.DISABLED)
                elif kind == "STREAM_CHUNK":
                    self._append_answer_chunk(data)
                elif kind == "STREAM_ERROR":
                    self.txt_answer_es.config(state=tk.NORMAL)
                    self.txt_answer_es.delete("1.0", tk.END)
                    self.txt_answer_es.insert(tk.END, f"{data}\n\n💡 Tip: Puedes cambiar a DeepSeek o configurar tus claves en '🔑 API Keys / Modelos' arriba.")
                    self.txt_answer_es.config(state=tk.DISABLED)

                    self.txt_answer_en.config(state=tk.NORMAL)
                    self.txt_answer_en.delete("1.0", tk.END)
                    self.txt_answer_en.insert(tk.END, f"Error generating response: {data}\n\n💡 Tip: You can switch to DeepSeek or configure your API Keys above.")
                    self.txt_answer_en.config(state=tk.DISABLED)
                    self._update_status("⚠️ Error consultando IA", self.accent_red)
                elif kind == "STREAM_DONE":
                    # Verificar si el panel en inglés quedó poblado; si no, autotraducir en segundo plano
                    es_curr = self.txt_answer_es.get("1.0", tk.END).strip()
                    en_curr = self.txt_answer_en.get("1.0", tk.END).strip()
                    if not en_curr or en_curr.startswith("⚡") or en_curr.startswith("⏳") or en_curr.startswith("💡"):
                        self._auto_translate_to_en(es_curr)
                    self._update_status("🟢 Escuchando la reunión...", self.accent_green)
                elif kind == "STREAM_IGNORED":
                    self.txt_answer_es.config(state=tk.NORMAL)
                    self.txt_answer_es.delete("1.0", tk.END)
                    self.txt_answer_es.insert(tk.END, "🔇 Charla casual ignorada (saludo o ruido cotidiano).\nEsperando una pregunta técnica...")
                    self.txt_answer_es.config(state=tk.DISABLED)

                    self.txt_answer_en.config(state=tk.NORMAL)
                    self.txt_answer_en.delete("1.0", tk.END)
                    self.txt_answer_en.insert(tk.END, "🔇 Casual chatter ignored (greeting or background noise).\nWaiting for technical question...")
                    self.txt_answer_en.config(state=tk.DISABLED)
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

        # Detectar coincidencia temática con la Guía de Entrevista Word Oficial
        self._check_and_display_word_match(text)

        self._update_status("⚡ Consultando a IA (Dual ES / EN)...", self.accent_blue)

        self._stream_full_text = ""
        self.txt_answer_es.config(state=tk.NORMAL)
        self.txt_answer_es.delete("1.0", tk.END)
        self.txt_answer_es.insert(tk.END, "⚡ Generando respuesta en español...")
        self.txt_answer_es.config(state=tk.DISABLED)

        self.txt_answer_en.config(state=tk.NORMAL)
        self.txt_answer_en.delete("1.0", tk.END)
        self.txt_answer_en.insert(tk.END, "⚡ Generating response in English...")
        self.txt_answer_en.config(state=tk.DISABLED)

        # Obtener modo de idioma seleccionado en el hilo principal
        sel_lang = self.lang_var.get()
        if "Solo Español" in sel_lang:
            active_lang = "es"
        elif "Only English" in sel_lang:
            active_lang = "en"
        else:
            active_lang = "dual"

        threading.Thread(target=self._ask_ai_worker, args=(text, active_lang), daemon=True).start()

    def _send_manual_question(self):
        query = self.entry_manual.get().strip()
        if not query or query == "O pega/escribe una pregunta del chat aquí...":
            return
        self.entry_manual.delete(0, tk.END)
        self._handle_detected_text(query)

    def _open_history(self):
        self.logger.open_history_folder()
        self._update_status("📂 Carpeta de historial abierta", self.accent_blue)

    def _ask_ai_worker(self, question: str, active_lang: str = "dual"):
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

    def _split_dual_text(self, text: str) -> Tuple[str, str]:
        en_pattern = r'(?:\*{1,2}|#{1,4}\s*)?\[(?:ENGLISH|INGL[EÉ]S|EN)(?:\s+(?:RESPONSE|VERSION|ANSWER))?\](?:\*{1,2}|:)?'
        parts = re.split(en_pattern, text, maxsplit=1, flags=re.IGNORECASE)
        es_raw = parts[0]
        es_clean = re.sub(r'^\s*(?:\*{1,2}|#{1,4}\s*)?\[(?:ESPA[ÑN]OL|ES)(?:\s+(?:RESPUESTA|VERSI[OÓ]N))?\](?:\*{1,2}|:)?\s*', '', es_raw, flags=re.IGNORECASE)
        es_clean = re.sub(r'\[(?:E|EN|ENG|ENGL|ENGLI|ENGLIS|ENGLISH|I|IN|ING|INGL|INGLE|INGLES|INGLÉ|INGLÉS)?$', '', es_clean, flags=re.IGNORECASE).rstrip()

        en_clean = ""
        if len(parts) > 1:
            en_raw = parts[1]
            en_clean = re.sub(r'^\s*[:\*\-]*\s*', '', en_raw).strip()

        return es_clean, en_clean

    def _append_answer_chunk(self, chunk: str):
        self._stream_full_text += chunk
        es_text, en_text = self._split_dual_text(self._stream_full_text)

        self.txt_answer_es.config(state=tk.NORMAL)
        self.txt_answer_es.delete("1.0", tk.END)
        self.txt_answer_es.insert(tk.END, es_text)
        self.txt_answer_es.see(tk.END)
        self.txt_answer_es.tag_raise("sel")
        self.txt_answer_es.config(state=tk.DISABLED)

        if en_text:
            self.txt_answer_en.config(state=tk.NORMAL)
            self.txt_answer_en.delete("1.0", tk.END)
            self.txt_answer_en.insert(tk.END, en_text)
            self.txt_answer_en.see(tk.END)
            self.txt_answer_en.tag_raise("sel")
            self.txt_answer_en.config(state=tk.DISABLED)

    def _auto_translate_to_en(self, es_text: str):
        if not es_text or es_text.startswith("💡") or es_text.startswith("⚡") or es_text.startswith("🔇") or es_text.startswith("❌"):
            return

        def _worker():
            try:
                res = self.copilot.translate_text_stream(text=es_text, target_lang="en")
                if res and not res.startswith("❌") and not res.startswith("⚠️"):
                    def _update_ui():
                        self.txt_answer_en.config(state=tk.NORMAL)
                        self.txt_answer_en.delete("1.0", tk.END)
                        self.txt_answer_en.insert(tk.END, res)
                        self.txt_answer_en.see(tk.END)
                        self.txt_answer_en.tag_raise("sel")
                        self.txt_answer_en.config(state=tk.DISABLED)
                    self.root.after(0, _update_ui)
            except Exception as e:
                print(f"Error en auto-traducción a inglés: {e}")

        threading.Thread(target=_worker, daemon=True).start()

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
