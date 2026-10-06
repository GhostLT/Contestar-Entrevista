# 🎙️ Copiloto de Entrevistas en Tiempo Real (Gemini 3.8 Flash)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%203.8%20Flash-orange.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://microsoft.com/windows)

Un copiloto y teleprompter inteligente de escritorio diseñado para escuchar en vivo las preguntas de un entrevistador durante una reunión virtual (**Google Meet, Microsoft Teams, Zoom, Skype, Discord, etc.**) y generar respuestas estructuradas, precisas y de alto nivel técnico al instante mediante el SDK oficial de **Google Gemini 3.8 Flash**.

---

## 🌟 Características Destacadas

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
    A["Audio de Reunión (Zoom / Meet / Teams)"] -->|Micrófono o WASAPI Loopback| B["audio_listener.py (VAD + SpeechRecognition)"]
    B -->|Texto Transcrito| C["gemini_copilot.py (google-genai SDK)"]
    C -->|Filtro Casual| D{"¿Es Pregunta Técnica?"}
    D -->|No (Saludos/Ruidos)| E["[IGNORAR]"]
    D -->|Sí| F["Gemini 3.8 Flash (Streaming Token-a-Token)"]
    F --> G["gui_prompter.py (Teleprompter Flotante Always-on-Top)"]
    F --> H["cli_prompter.py (Consola con Salida a Color)"]
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

## 📂 Estructura del Proyecto

```
Contestar-Entrevista/
├── .env.example          # Plantilla para variables de entorno
├── .gitignore            # Archivos excluidos del control de versiones
├── requirements.txt      # Dependencias oficiales de Python
├── iniciar.bat           # Lanzador rápido de la ventana flotante
├── iniciar_consola.bat   # Lanzador rápido del modo terminal
├── main.py               # Punto de entrada principal (GUI, CLI y Tests)
├── config.py             # Configuración centralizada y System Prompts
├── audio_listener.py     # Captura de audio y transcripción continua (Mic / Loopback)
├── gemini_copilot.py     # Cliente de Gemini 3.8 Flash con streaming y filtros
├── gui_prompter.py       # Interfaz gráfica flotante Always-on-Top en Tkinter
├── cli_prompter.py       # Interfaz para terminal interactiva con Colorama
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
