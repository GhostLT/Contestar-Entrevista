# 🎙️ Copiloto de Entrevistas en Tiempo Real (Gemini 3.8 Flash)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%203.8%20Flash-orange.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://microsoft.com/windows)

Un copiloto y teleprompter inteligente de escritorio diseñado para escuchar en vivo las preguntas de un entrevistador durante una reunión virtual (**Google Meet, Microsoft Teams, Zoom, Skype, Discord, etc.**) y generar respuestas estructuradas, precisas y de alto nivel técnico al instante mediante el SDK oficial de **Google Gemini 3.8 Flash**.

---

## 🌟 Características Destacadas

- ⚡ **Teleprompter Dual Dividido Horizontalmente (🇪🇸 Español Arriba / 🇺🇸 Inglés Abajo)**:
  - **Pantalla Superior**: Muestra la respuesta directa y sintetizada en **Español** (`🇪🇸`), lista para leer en voz alta de inmediato con viñetas técnicas, parámetros y casos reales.
  - **Pantalla Inferior**: Muestra la respuesta correspondiente en **Inglés** (`🇺🇸`), ideal para entrevistas técnicas en video o cuando el cliente internacional realiza la llamada en inglés.
  - **Generación en Vivo Simultánea**: En llamadas con el entrevistador, los motores de IA (Gemini / DeepSeek) generan y transmiten en tiempo real ambos bloques de idioma a sus paneles respectivos sin demora.
  - **Inyección Bilingüe desde Cualquier Pestaña**: Al hacer clic en *"Al Teleprompter"* desde la pestaña de Pitch (`2`) o la Guía Word (`3`), la aplicación carga automáticamente la versión en español arriba y la versión en inglés abajo.
  - **Acciones Rápidas en Cabecera**: Botones independientes `📋 Copiar ES`, `📋 Copiar EN`, `📜 Historial` y `🗑️ Limpiar`.
- ⌨️ **Nuevos Atajos Rápidos Ergonómicos (`1`, `2`, `3`)**:
  - **`1`**: Ir a **🎙️ Copiloto en Vivo (Teleprompter Dual)**.
  - **`2`**: Ir a **🎯 Mi Pitch & Formación (Javier Viveros Huesca)**.
  - **`3`**: Ir a **📖 Guía Entrevista Word (31 temas ES / 33 temas EN)**.
  - **Salvaguarda Inteligente de Escritura**: Si estás editando una pregunta en el recuadro editable, buscando en la guía Word o pegando texto en la barra manual, presionar `1`, `2` o `3` escribe el número normalmente sin cambiar de pestaña.
  - *(Se mantiene también compatibilidad con las teclas `F1`, `F2`, `F3` y teclado numérico `KP_1`, `KP_2`, `KP_3`)*.
- 🎯 **Pestaña de Pitch Personal y Formación Multi-Rol (2)**: Pestaña interactiva organizada en 2 filas dedicadas para responder con total maestría según el tipo de entrevista técnica:
  - **Fila 1: 📡 RF Optimization Engineer (Ericsson RAN | Arturo Ramírez - México / Remoto)**:
    - **`🇪🇸 RF Pitch (60–90s)`**: Pitch principal en español con +15 años de experiencia en RAN, optimización de LTE L15, Baseband 5212/5216/6630, Radio Dot, NodeB/eNodeB/gNodeB y auditoría de KPIs críticos (RTWP, PIM, DCR, Handover).
    - **`🇺🇸 RF Pitch (60s)`**: Guión en inglés para clientes globales y fabricantes con terminología técnica estándar 3GPP.
    - **`⚙️ Deep Dive Ericsson & KPIs`**: Análisis técnico profundo de resolución de interferencias, pilot pollution, colisiones/confusiones PCI mod 3/mod 30, eventos de handover A1-A5/B1-B2 y Layer 3 signaling.
    - **`⚡ RF Rápido (30s)`**: Elevator pitch ultra conciso de 30 segundos.
    - **`🎓 Formación & Certs`**: Ingeniería en Electrónica (IT Reynosa) + MBA (Tecmilenio) + Certificación Oficial Ericsson LTE Configuration.
    - 📖 **[Guía Maestra RF Ericsson](GUIA_ENTREVISTA_RF_ERICSSON.md)**: Banco completo con 8 preguntas y respuestas técnicas avanzadas y matriz de parámetros Ericsson LTE.
  - **Fila 2: 🌐 Telecom (5G Core Speridian) & 💻 Full-Stack con IA (PCoS / Hireline)**:
    - **`🇺🇸 5G Pitch (Speridian)`**: Guión en inglés para la posición de 5G Network Engineer con call-flows N1-N12, roaming SEPP y desarrollo open source asistido por IA.
    - **`⚙️ 5GC Call-Flows`**: Deep dive en interfaces 5G Core, N32-c/f, SCTP y Kubernetes.
    - **`💻 Full-Stack IA (PCoS)`**: Pitch de arquitectura Full-Stack con FastAPI, vLLM en AWS GPU (-65% costo) y RAG con pgvector.
    - **`🎯 Fit PCoS`**: Los 3 pilares técnicos de fit inmediato (estrategia Open Source, RLS y flujos agénticos).
    - 📖 **[Guía Maestra 5G](GUIA_ENTREVISTA_5G.md)** y **[Guía Perfil Candidato](PERFIL_CANDIDATO.md)**.
  - **⚡ Botón "Al Teleprompter"**: Carga cualquier pitch seleccionado en el teleprompter dual del copiloto (Español arriba, Inglés abajo) con 1 solo clic.
  - **Teclas Rápidas**: `1` para volver al Copiloto en Vivo, `2` para abrir tu Pitch y `3` para la Guía Word.
- 📖 **Pestaña de Guía Maestra de Entrevista en Formato Word (3)**: Visor de lectura interactivo diseñado idéntico a las especificaciones visuales de un documento formal de **Microsoft Word**, integrando los 10 módulos en español y 11 en inglés:
  - **Diseño Estilo Microsoft Word**: Página en blanco con encabezado institucional (`AMDOCS MX | Senior RF Optimization Engineer – Ericsson 4G/5G`), márgenes ejecutivos, cajas de estrategia verde (`🎯 Estrategia y Tono`), cajas de respuesta modelo azul marino (`💬 Respuesta Modelo`), y bloques monospace en `Consolas` para comandos Moshell y tablas de parámetros.
  - **Selector Bilingüe**: Alterna al instante entre `🇪🇸 Español (10 Módulos - 31 Temas)` y `🇺🇸 English (11 Modules - 33 Topics)`.
  - **Navegador Lateral de Preguntas**: Índice interactivo con las 31 preguntas en español / 33 en inglés para saltar a cualquier tema en 1 clic.
  - **Buscador en Tiempo Real**: Filtra preguntas por términos técnicos (`RTWP`, `PIM`, `Handover`, `A3`, `PRACH`, `DCR`, `VoLTE`, `MOM`, `Moshell`).
  - **⚡ Botón "Al Teleprompter"**: Extrae la respuesta modelo seleccionada y carga simultáneamente la respuesta en español en el panel superior y la respuesta en inglés en el panel inferior (`1`).
  - **📄 Botón "Abrir Word"**: Abre directamente el archivo `.docx` oficial en Microsoft Word mediante integración nativa con Windows.
  - **Teclas Rápidas**: `1` (Copiloto Dual), `2` (Mi Pitch & Formación), `3` (Guía Word).
- 👤 **Alter Ego y Perfil Profesional Integrado (Javier Viveros Huesca)**: El copiloto está preconfigurado con el historial verificado: +15 años en optimización de radiofrecuencia (RF) y RAN en carriers Tier-1 (AT&T, Nextel, Empire), certificación oficial de Ericsson en LTE Configuration, MBA de Tecmilenio e Ing. en Electrónica (IT Reynosa), además de experiencia en 5G Core (Open5GS/free5GC) y Full-Stack con IA (FastAPI/vLLM), respondiendo siempre en primera persona ("yo") con autoridad técnica senior.
- 🌐 **Soporte Bilingüe Simultáneo y Selector de Modo (Dual / ES / EN)**:
  - **Selector de Modo**: Permite elegir entre `⚡ Dual (ES + EN)`, `🇪🇸 Solo Español` o `🇺🇸 Only English`.
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
    A["Audio de Reunión (Zoom / Meet / Teams)"] -->|Micrófono o WASAPI Loopback| B["audio_listener.py (VAD + SpeechRecognition)"]
    B -->|Texto Transcrito en Vivo| C["gemini_copilot.py (Gemini / DeepSeek)"]
    C -->|Filtro Casual| D{"¿Pregunta Técnica?"}
    D -->|No (Saludos/Ruidos)| E["[IGNORAR]"]
    D -->|Sí| F["Generación Streaming (Token-a-Token)"]
    F --> G["Teleprompter Flotante (gui_prompter.py)"]
    G --> H["history_logger.py (Guardado en historial/ .md y .json)"]
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

Para las preguntas abiertas donde el entrevistador te pide presentarte (*"Háblame de ti", "Cuéntame sobre tu trayectoria profesional", "Walk me through your background"*), la aplicación incluye una pestaña dedicada con guiones preparados organizados en dos filas temáticas para conmutar con un solo clic:

1. **Fila 1: 📡 RF Optimization (Ericsson RAN / Arturo Ramírez)**:
   - **`🇪🇸 RF Pitch (60–90s)`**: Resumen profesional de +15 años en optimización de radiofrecuencia en carriers Tier-1 (AT&T, Nextel, Empire), plataformas Ericsson Baseband 5212/5216/6630, Radio Dot, LTE L15, auditoría de KPIs (RTWP, PIM, DCR, Handover) y automatización con Python/SQL.
   - **`🇺🇸 RF Pitch (60s)`**: Versión en inglés técnico para clientes internacionales o fabricantes de infraestructura celular.
   - **`⚙️ Deep Dive Ericsson & KPIs`**: Análisis técnico profundo de troubleshooting L3, interferencias, pilot pollution, colisión/confusión PCI mod 3/30 y eventos A1-A5/B1-B2.
   - **`⚡ RF Rápido (30s)`**: Elevator pitch ultra conciso de 30 segundos.
   - **`🎓 Formación & Certs`**: Título de Ing. en Electrónica (IT Reynosa), MBA (Tecmilenio) y Certificación Oficial Ericsson LTE Configuration.
2. **Fila 2: 🌐 Telecom (5G Core Speridian) & 💻 Full-Stack con IA (PCoS)**:
   - **`🇺🇸 5G Pitch (Speridian)`**: Pitch en inglés para 5G Core Network Engineer (SA/NSA, N1-N12, SEPP, Open5GS/free5GC con IA asistida).
   - **`⚙️ 5GC Call-Flows`**: Deep dive en call-flows 5G, N32-c/N32-f, SCTP y Kubernetes.
   - **`💻 Full-Stack IA (PCoS)`**: Pitch full-stack con FastAPI, vLLM en AWS GPU (-65% costos) y RAG con pgvector.
   - **`🎯 Fit PCoS`**: Los 3 pilares técnicos de ajuste inmediato para PCoS.
3. **Acciones y Navegación**:
   - **`F1` / `F2`**: Alterna al instante entre el **Copiloto en Vivo (`F1`)** y tu **Pitch (`F2`)** con una sola tecla sin mover el cursor.
   - **`⚡ Al Teleprompter`**: Carga el pitch seleccionado como respuesta activa en la ventana principal del copiloto y te regresa automáticamente a la vista de escucha.
   - **`📋 Copiar`**: Copia el texto al portapapeles por si solicitan un resumen en el chat de la videollamada.
   - **Métricas Rápidas al Pie**: Badges visuales con tus datos clave (`📶 +15 Años RF & RAN`, `📡 Ericsson Specialist`, `📊 KPIs: RTWP/PIM/DCR`, `🛠️ TEMS / Nemo / Actix`, `🎓 Ing. Electrónica + MBA`, `📜 Cert. Ericsson LTE`, `🚀 Disp. Inmediata (México)`).

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
├── rf_word_guide.py      # Gestor y parser de la Guía de Entrevista RF en formato Word/Markdown
├── PERFIL_CANDIDATO.md   # Documento de referencia con las 7 respuestas para PCoS y CV
├── GUIA_ENTREVISTA_RF_ERICSSON.md # Guía técnica de preparación para RF Optimization Engineer (Ericsson RAN)
├── Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.docx # Documento oficial Microsoft Word (10 Módulos - Español)
├── Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.md   # Fuente Markdown enriquecida (10 Módulos - Español)
├── Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.docx # Official Microsoft Word Document (11 Modules - English)
├── Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.md   # Enriched Markdown Source (11 Modules - English)
├── GUIA_ENTREVISTA_5G.md   # Guía completa de preparación técnica para 5G Network Engineer (Speridian)
├── audio_listener.py     # Captura de audio y transcripción continua (Mic / Loopback)
├── gemini_copilot.py     # Cliente multi-IA (Gemini con auto-fallback, DeepSeek y OpenRouter)
├── gui_prompter.py       # Interfaz gráfica flotante Always-on-Top con visor Word (F3) y teleprompter
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
