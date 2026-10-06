# 🎙️ Copiloto de Entrevistas en Tiempo Real (Gemini 3.8 Flash)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%203.8%20Flash-orange.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://microsoft.com/windows)

Un copiloto y teleprompter inteligente de escritorio diseñado para escuchar en vivo las preguntas de un entrevistador durante una reunión virtual (**Google Meet, Microsoft Teams, Zoom, Skype, Discord, etc.**) y generar respuestas estructuradas, precisas y de alto nivel técnico al instante mediante el SDK oficial de **Google Gemini 3.8 Flash**.

---

## 🌟 Características Destacadas

- 🌐 **Pantalla Dividida y Traductor de Conversación en Vivo (Inglés ➔ Español en Tiempo Real)**:
  - **División Vertical Ergonómica (`ttk.PanedWindow`)**: La ventana principal del copiloto está dividida en dos secciones con un divisor ajustable:
    - **Panel Superior (Teleprompter IA)**: Pregunta detectada/editable y la respuesta estructurada del copiloto IA en vivo.
    - **Panel Inferior (Traductor Simultáneo)**: Muestra en tiempo real el diálogo continuo de la entrevista con columnas lado a lado:
      - `🇬🇧 Audio Original Detectado (English)`: Transcribe cada frase o pregunta que dice el entrevistador en inglés con marca de tiempo `[HH:MM:SS]`.
      - `🇪🇸 Traducción al Español (Tiempo Real)`: Muestra la traducción instantánea al español con ultra baja latencia (<250ms), sin consumir cuota ni tokens de tus APIs de IA.
  - **Selector de Reconocimiento de Voz (`🎙️ Voz: 🇺🇸 Inglés (en-US) / 🇪🇸 Español (es-ES)`)**: Cambia al instante el idioma de captura del micrófono o audio loopback de la reunión.
  - **Herramientas de Conversación**: Botón `📋 Copiar Conversación` (copia el diálogo bilingüe completo), `⏸️ Pausar/Reanudar` y `🗑️ Limpiar Conversación`.
  - **Persistencia Completa**: Cada turno traducido se guarda automáticamente en los registros de sesión en `historial/`.
- 🎯 **Pestaña de Pitch Personal y Formación Multi-Rol (F2)**: Pestaña interactiva organizada en 2 filas dedicadas para responder con total maestría según el tipo de entrevista técnica:
  - **Fila 1: 📡 5G Network Engineer (Speridian Technologies | Shubham - Richardson TX)**:
    - **`🇺🇸 5G Pitch (60s)`**: Guión de alto impacto para la llamada con el reclutador (Shubham) y la entrevista de video con el cliente en Richardson TX, integrando +12 años de experiencia, +9 años en AT&T (99.999% SLA), 5GC (SA/NSA), AMF/SMF/UPF, SEPP y desarrollo open source asistido por IA (Codex/Groq).
    - **`⚙️ 5GC Call-Flows & AI`**: Deep dive técnico en call flows end-to-end (interfaces N1 a N12 con Wireshark/tshark), roaming inter-PLMN con SEPP sobre N32 (N32-c TLS y N32-f PRINS), y uso de IA generativa para agregar código a plataformas Open5GS y free5GC.
    - **`🇪🇸 5G Core Español`**: Guión en español para presentar solvencia en redes móviles críticas, señalización SCTP/Diameter/HTTP-2 y arquitecturas cloud-native en Kubernetes.
  - **Fila 2: 💻 Full-Stack con IA (PCoS / Hireline)**:
    - **`🇪🇸 Completo (60–90s)`**: Presentación profesional profunda con trayectoria, vLLM en AWS GPU (-65% costos), RAG con pgvector y sinergia con PCoS.
    - **`⚡ Rápido (30s)`**: Elevator pitch ultra conciso de 30 segundos.
    - **`🇺🇸 English (60s)`**: Walkthrough en inglés profesional para clientes internacionales.
    - **`🎓 Formación & Certs`**: Título en Ingeniería en Electrónica y Sistemas Digitales (Instituto Tecnológico de Reynosa) y especializaciones continuas.
    - **`🎯 Por qué PCoS`**: Los 3 pilares técnicos de fit inmediato (estrategia Open Source, RLS en Supabase y flujos agénticos).
  - **⚡ Botón "Al Teleprompter"**: Carga cualquier pitch seleccionado en el teleprompter principal del copiloto con 1 solo clic.
  - **Teclas Rápidas**: `F1` para volver al Copiloto en Vivo y `F2` para abrir tu Pitch en cualquier momento.
- 👤 **Alter Ego y Perfil Profesional Integrado (Javier Viveros Huesca)**: El copiloto está preconfigurado con el historial verificado, titulación en Ingeniería en Electrónica y Sistemas Digitales, trayectoria en AT&T (+120 plataformas críticas de red, 99.999% SLA), Empire Engineering, modelos Open Source con vLLM y desarrollo en 5G Core Open Source (Open5GS/free5GC) con IA asistida (Codex/Groq), respondiendo siempre en primera persona ("yo") con autoridad técnica senior.
- 🌐 **Soporte Bilingüe (Español 🇪🇸 / Inglés 🇺🇸) y Traducción en 1 Clic**:
  - **Selector de Idioma**: Configura el idioma de respuesta en `🇪🇸 Español` o `🇺🇸 English` desde la barra de controles para entrevistas nacionales o internacionales.
  - **Botón de Traducción Instantánea (`🌐 Traducir a Inglés` / `🌐 Traducir a Español`)**: ¿La respuesta está en español pero necesitas leerla en inglés (o viceversa)? Con un solo clic, la IA la traduce en tiempo real mediante streaming, manteniendo intacta la estructura, viñetas y emojis (`🎯`, `⚡`, `💡`).
- 📜 **Logs y Registro Automático de Conversaciones**: Cada pregunta formulada y respuesta generada se guarda automáticamente en la carpeta `historial/` en formatos **Markdown (`.md`)** y **JSON (`.json`)** con marcas de tiempo para que puedas repasar lo que te preguntaron después de la entrevista. Incluye un botón **`📜 Ver Historial`** para abrir la carpeta con un solo clic.
- ✏️ **Modificación Manual de Preguntas en Vivo**: Si el reconocimiento de voz malinterpreta un tecnicismo en inglés o audio ruidoso (por ejemplo: entendió *"ratón"* en vez de *"handover"*), el recuadro de pregunta es **100% editable directamente**. Puedes hacer clic, corregir la palabra y presionar **Enter** o el botón **`⚡ Corregir y Re-preguntar`** para obtener la respuesta correcta al instante.
- 🤖 **Multi-Motor de IA con Respaldo Automático**:
  - **Google Gemini**: Con auto-conmutación a `gemini-3.5-flash-lite` para evitar errores 503 por alta demanda.
  - **DeepSeek Oficial**: Soporte nativo para `deepseek-chat` vía API oficial (`api.deepseek.com`).
  - **OpenRouter (Gratis)**: Soporte para modelos `deepseek-r1` y `deepseek-chat` sin costo.
- ⚡ **Respuestas en Tiempo Real (Streaming)**: Las palabras aparecen progresivamente en pantalla en menos de 1 segundo mediante streaming token a token.
- 🎯 **Estructura Diseñada para Hablar en Voz Alta**:
  - **Definición Inmediata**: 1 o 2 oraciones concisas y directas para que empieces a hablar sin titubear.
  - **Puntos Clave**: 2 o 3 viñetas técnicas con los conceptos esenciales o arquitectura interna.
  - **Caso Práctico**: 1 ejemplo o estándar de la industria que proyecta experiencia senior.
- 🔇 **Filtro Inteligente Anti-Ruido**: Discrimina automáticamente la charla casual y los saludos cotidianos (*"¿me escuchas?", "buenos días", "espera que comparto pantalla"*) para evitar spam en pantalla.
- 🔊 **Captura de Audio Dual (Micrófono o Loopback)**:
  - **Modo Micrófono**: Captura tu voz o el sonido ambiente si escuchas la reunión por altavoces.
  - **Modo Audio de Reunión (WASAPI Loopback)**: Captura directamente el audio digital que sale por tus audífonos o altavoces sin captar eco ni ruidos de tu habitación.
- 📌 **Teleprompter Flotante (Always-on-Top)**: Ventana compacta con tema oscuro que permanece siempre visible sobre Zoom o Teams. Colócala justo debajo de la lente de tu cámara web para mantener contacto visual continuo con el entrevistador.
- 💬 **Barra de Entrada Manual**: Si el entrevistador escribe la pregunta en el chat de la videollamada, puedes pegarla en la barra inferior y presionar `Enter` para responder de inmediato.
- 💻 **Modo Terminal / Consola**: También incluye un modo CLI con texto a color para programadores que prefieran trabajar desde la terminal.

---

## 🏗️ Arquitectura del Sistema

```mermaid
flowchart TD
    A["Audio de Reunión (Zoom / Meet / Teams)"] -->|Micrófono o WASAPI Loopback| B["audio_listener.py (VAD + SpeechRecognition en-US / es-ES)"]
    B -->|Texto Transcrito en Vivo| C{"Despacho Dual"}
    
    C -->|Flujo 1: Conversación en Vivo| D["realtime_translator.py (Ultra Rápido <250ms)"]
    D -->|Audio EN + Traducción ES| E["Panel Inferior: Conversación & Traducción Simultánea"]
    
    C -->|Flujo 2: Copiloto Asistente| F["gemini_copilot.py (Gemini / DeepSeek)"]
    F -->|Filtro Casual| G{"¿Pregunta Técnica?"}
    G -->|No (Saludos/Ruidos)| H["[IGNORAR]"]
    G -->|Sí| I["Generación Streaming (Token-a-Token)"]
    I --> J["Panel Superior: Teleprompter de Respuestas"]
    
    E --> K["history_logger.py (Guardado en historial/ .md y .json)"]
    J --> K
```

---

## 📋 Requisitos Previos

1. **Windows 10 / 11**.
2. **Python 3.10 o superior** (probado y optimizado en Python 3.12).
3. **Clave de API de Google Gemini** (gratuita).

---

## 🔑 Cómo Obtener tu API Key de Gemini Gratis

1. Ingresa a 👉 **[Google AI Studio](https://aistudio.google.com/)** con tu cuenta de Google.
2. En la parte superior o menú lateral, haz clic en **"Get API key"** (Obtener clave de API).
3. Haz clic en **"Create API key in new project"** (Crear clave de API en un nuevo proyecto).
4. Copia la clave generada (comienza por `AIzaSy...`).

---

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/GhostLT/Contestar-Entrevista.git
cd Contestar-Entrevista
```

### 2. Configurar el Entorno Virtual
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar tu API Key
Copia el archivo de plantilla `.env.example` como `.env`:
```bash
copy .env.example .env
```
Edita `.env` con tu editor favorito y coloca tu clave:
```env
GEMINI_API_KEY=AIzaSyTuClaveReal...
GEMINI_MODEL=gemini-3.8-flash
AUDIO_LANGUAGE=es-ES
ALWAYS_ON_TOP=True
WINDOW_OPACITY=0.95
```
*(También puedes configurarla directamente desde la interfaz gráfica haciendo clic en el botón `🔑 API Key`)*.

---

## ▶️ Modos de Ejecución

### Opción A: Doble Clic (Windows)
- Haz doble clic en **`iniciar.bat`**: Abre la ventana flotante en modo Teleprompter.
- O doble clic en el acceso directo de tu Escritorio **`Copiloto de Entrevista`**.

### Opción B: Ventana Flotante por Terminal
```bash
.\venv\Scripts\python.exe main.py
```

### Opción C: Modo Consola (CLI con Colores)
```bash
.\venv\Scripts\python.exe main.py --cli
# O doble clic en iniciar_consola.bat
```

### Opción D: Prueba Directa sin Micrófono
```bash
.\venv\Scripts\python.exe main.py --test-question "¿Qué es un switch Cisco?"
```

---

## 💡 Consejos de Uso Durante una Entrevista Real

1. **Posición de la Ventana**:
   - Arrastra la ventana flotante y colócala en el centro superior de tu pantalla, justo debajo de tu webcam.
   - De esta manera, cuando estés leyendo la respuesta, tus ojos estarán mirando casi directo a la cámara, transmitiendo total seguridad y atención.
2. **Selección del Dispositivo**:
   - **Si usas audífonos en la llamada**: En el menú desplegable de la aplicación, elige la opción que dice `[Audio Reunion (Loopback)]` (por ejemplo: *Speakers/Headphones (Realtek(R) Audio) [Loopback]*). Esto permitirá que el programa escuche lo que dice el entrevistador por tus audífonos sin captar ruidos de tu casa.
   - **Si usas altavoces**: Selecciona tu micrófono habitual (`[Microfono]`).
3. **Flujo de Lectura Natural**:
   - En cuanto aparezca la primera frase en verde, empieza a leerla pausadamente en voz alta.
   - Mientras terminas de decir esa frase, tus ojos pueden escanear las viñetas técnicas para complementar tu respuesta con total naturalidad y autoridad.

---

## 🎯 Pestaña de Pitch de Presentación y Formación (F2)

Para las preguntas abiertas donde el entrevistador te pide presentarte (*"Háblame de ti", "Cuéntame sobre tu trayectoria profesional", "Walk me through your background"*), la aplicación incluye una pestaña dedicada con guiones preparados listos para leer en voz alta con total fluidez:

1. **Guiones Disponibles**:
   - **`🇪🇸 Completo (60–90s)`**: Resumen profesional profundo con trayectoria de +12 años, stack moderno (React, TypeScript, FastAPI, Supabase), inferencia de modelos Open Source con vLLM en AWS GPU (-65% costos), RAG con pgvector y visión con PCoS.
   - **`⚡ Rápido (30s)`**: Elevator pitch ultra conciso para respuestas directas o rondas de selección rápidas.
   - **`🇺🇸 English (60s)`**: Walkthrough en inglés profesional de nivel senior para entrevistas internacionales o clientes de EE. UU.
   - **`🎓 Formación & Certs`**: Detalle del título universitario en Ingeniería en Electrónica y Sistemas Digitales (Instituto Tecnológico de Reynosa) y credenciales especializadas (Generative AI, vLLM, Full-Stack, Supabase, AWS, Clean Architecture).
   - **`🎯 Por qué PCoS`**: Los 3 argumentos técnicos definitivos de por qué eres el candidato ideal (estrategia Open Source, soberanía de datos con RLS en salud/operaciones y experiencia en asistentes ejecutivos con flujos agénticos).
2. **Acciones y Navegación**:
   - **`F1` / `F2`**: Alterna al instante entre el **Copiloto en Vivo (`F1`)** y tu **Pitch (`F2`)** con una sola tecla sin mover el cursor.
   - **`⚡ Al Teleprompter`**: Carga el pitch seleccionado como respuesta activa en la ventana principal del copiloto y te regresa automáticamente a la vista de escucha.
   - **`📋 Copiar`**: Copia el texto al portapapeles por si solicitan un resumen en el chat de la videollamada.
   - **Métricas Rápidas al Pie**: Badges visuales con tus datos clave (+12 años exp, +4 años full-stack, +2.5 años IA Open Source, $2,500 USD/mes, disponibilidad inmediata) para responder cualquier duda en un parpadeo.

---

## 🌐 Manejo Bilingüe (Español / Inglés) y Traducción en Vivo

Diseñado especialmente para candidatos que aplican a empresas internacionales o vacantes con rondas técnicas mixtas:

1. **Preselección de Idioma**:
   - En la barra de controles, junto al selector de IA, dispones del selector **`Idioma:`** con las opciones **`🇪🇸 Español`** y **`🇺🇸 English`**.
   - Si seleccionas `🇺🇸 English`, el copiloto generará todas las respuestas futuras en inglés técnico nativo con vocabulario y sintaxis senior.
2. **Traducción Instantánea de Respuestas Existentes**:
   - Si una respuesta se generó en español y necesitas decirla en inglés (o viceversa), presiona el botón **`🌐 Traducir a Inglés`** (o **`🌐 Traducir a Español`**) en la cabecera de la respuesta.
   - La IA traducirá el texto en vivo vía streaming preservando intactas las viñetas, emojis (`🎯`, `⚡`, `💡`) y precisión técnica sin perder tiempo.
   - Ambas versiones (original y traducción) quedan registradas en tu historial para repaso posterior.

---

## 📜 Historial y Registro Automático de Conversaciones

Cada vez que el entrevistador hace una pregunta y se genera una respuesta, la sesión se guarda **automáticamente en segundo plano** dentro del directorio `historial/`:

- **Formato Markdown (`.md`)**: Notas legibles con fecha, hora, pregunta formulada, motor de IA utilizado y la respuesta generada con viñetas. Ideal para abrir con Obsidian, Notion, VS Code o el Bloc de notas.
- **Formato JSON (`.json`)**: Estructura de datos completa para análisis o integraciones futuras.
- **Acceso Directo en 1 Clic**: En la cabecera de la respuesta dentro de la aplicación, haz clic en el botón azul **`📜 Ver Historial`** y se abrirá la carpeta de tus entrevistas en el Explorador de Windows.
- **100% Privado**: Tus registros se almacenan exclusivamente en tu computadora local y están excluidos en `.gitignore` para no compartirse jamás en GitHub.

---

## 📂 Estructura del Proyecto

```
Contestar-Entrevista/
├── .env.example          # Plantilla para variables de entorno
├── .gitignore            # Archivos excluidos del control de versiones (protege .env y historial)
├── requirements.txt      # Dependencias oficiales de Python
├── iniciar.bat           # Lanzador rápido de la ventana flotante
├── iniciar_consola.bat   # Lanzador rápido del modo terminal
├── main.py               # Punto de entrada principal (GUI, CLI y Tests)
├── config.py             # Configuración centralizada y System Prompts
├── candidate_profile.py  # Perfil y base de conocimiento técnico de Javier Viveros Huesca
├── PERFIL_CANDIDATO.md   # Documento de referencia con las 7 respuestas para PCoS y CV
├── audio_listener.py     # Captura de audio y transcripción continua (Mic / Loopback)
├── gemini_copilot.py     # Cliente multi-IA (Gemini con auto-fallback, DeepSeek y OpenRouter)
├── gui_prompter.py       # Interfaz gráfica flotante Always-on-Top con edición en vivo
├── cli_prompter.py       # Interfaz para terminal interactiva con Colorama
├── history_logger.py     # Motor de guardado y persistencia en Markdown y JSON
├── historial/            # Carpeta local privada con las notas de cada entrevista
└── README.md             # Esta documentación
```

---

## ⚙️ Tecnologías Utilizadas

- **[Google GenAI SDK](https://github.com/googleapis/python-genai)** (`google-genai`): Integración oficial con Gemini 3.8 Flash.
- **[SpeechRecognition](https://github.com/Uberi/speech_recognition)**: Detección y transcripción de voz en tiempo real.
- **[PyAudioWPatch](https://github.com/s0d3s/PyAudioWPatch)**: Soporte nativo para captura de bucle invertido (WASAPI Loopback) en Windows.
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)**: Interfaz gráfica nativa ultraligera (0% consumo de CPU).
- **[Colorama](https://github.com/tartley/colorama)**: Formato de consola para PowerShell y CMD.

---

## 📄 Licencia

Este proyecto está distribuido bajo la licencia MIT. Diseñado con fines educativos y de asistencia personal en procesos de selección.
