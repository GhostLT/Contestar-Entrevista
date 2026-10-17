# 🎙️ Copiloto de Entrevistas en Tiempo Real (Gemini 3.8 Flash)

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini%203.8%20Flash-orange.svg)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://microsoft.com/windows)

Un copiloto y teleprompter inteligente de escritorio diseñado para escuchar en vivo las preguntas de un entrevistador durante una reunión virtual (**Google Meet, Microsoft Teams, Zoom, Skype, Discord, etc.**) y generar respuestas estructuradas, precisas y de alto nivel técnico al instante mediante el SDK oficial de **Google Gemini 3.8 Flash**, con soporte multi-motor (**DeepSeek** y **OpenRouter**).

Especializado en **Senior RF Optimization & Performance Engineer (Ericsson 4G/5G)**, integrando la Guía Oficial de Entrevista (10 Módulos / 31 Preguntas maestras) con sincronización bilingüe en paralelo (Español / Inglés).

---

## 🌟 Características Destacadas

### 1. 📖 Vinculación Inteligente en Vivo Copiloto ➔ Guía Word (Multi-Coincidencias)
- **Detección Automática por Palabras Clave**: Cuando el copiloto escucha una pregunta o cuando escribes en la caja de preguntas o en la barra manual, el motor semántico analiza los conceptos técnicos en tiempo real (`<KeyRelease>`).
- **Soporte de Términos Individuales**: Reconoce palabras clave técnicas individuales sin exigir frases exactas completas (por ejemplo: `dynamic`, `B2`, `RTWP`, `handover`, `A3`, `PRACH`, `carrier aggregation`, `5G`, `MIMO`, etc.).
- **Múltiples Posibilidades Interactivas (Multi-Match)**:
  - Si un término técnico abarca varios tópicos (por ejemplo, `B2` aplica para **Eventos de Handover B1/B2** en el Módulo 3 y para **Carrier Aggregation con Banda 2** en el Módulo 5), el copiloto presenta **todas las opciones detectadas como botones interactivos directos**.
  - Ejemplo visual:
    ```
    📖 COINCIDENCIAS EN GUÍA WORD (2 POSIBILIDADES ENCONTRADAS):
    [ 📖 Q10: Handover B1/B2 (Mód 3) ➔ ]   [ 📖 Q17: Carrier Aggregation B2 (Mód 5) ➔ ]
    ```
- **Navegación Instantánea con 1 Clic (`_jump_to_matched_word_question`)**:
  - Al hacer clic en cualquiera de los botones/chips, la interfaz se traslada automáticamente a la **Pestaña 3 (Guía Word)**.
  - Selecciona de forma autónoma el módulo correspondiente en el selector.
  - Resalta y enfoca la pregunta exacta en el índice lateral.
  - Carga y posiciona ambas hojas (Español e Inglés) desde el inicio para lectura inmediata.

---

### 2. ⚡ Teleprompter Dual Dividido Horizontalmente (🇪🇸 Español Arriba / 🇺🇸 Inglés Abajo)
- **Pantalla Superior**: Muestra la respuesta directa y sintetizada en **Español** (`🇪🇸`), lista para leer en voz alta de inmediato con viñetas técnicas, parámetros y casos reales.
- **Pantalla Inferior**: Muestra simultáneamente la respuesta correspondiente en **Inglés** (`🇺🇸`), ideal para entrevistas bilingües, clientes internacionales o videollamadas técnicas.
- **Generación Simultánea en Vivo**: Los motores de IA generan y transmiten en tiempo real ambos bloques de idioma en streaming token a token.
- **Caja de Pregunta Limpia y 100% Editable**: Recuadro de pregunta vacío y listo para editar al instante (sin textos de placeholder molestos que haya que borrar manualmente).
- **Acciones Rápidas Ergonómicas Reubicadas**: Botones `🗑️ Limpiar`, `📜 Historial`, `📋 Copiar ES`, `📋 Copiar EN` y `📋 Copiar Ambos` situados estratégicamente debajo de la pregunta para acceso inmediato sin tapar la respuesta.
- **Selección y Copiado Total (`Ctrl + C`)**: Soporte nativo para seleccionar cualquier fragmento de texto con el cursor y copiarlo con el atajo de teclado `Ctrl + C`, `Ctrl + A` o mediante menú contextual de clic derecho en todas las pantallas.

---

### 3. 📖 Guía Word Dividida al 50/50 Vertical con Scroll Sincronizado
- **División Vertical al 50/50**:
  - **Lado Izquierdo (50% - 🇪🇸 Español)**: Hoja de Microsoft Word con la pregunta, estrategia de respuesta, respuesta modelo y comandos/tablas en español.
  - **Lado Derecho (50% - 🇺🇸 English)**: Hoja simétrica idéntica con el contenido equivalente traducido y adaptado profesionalmente al inglés técnico.
- **🔄 Scroll Sincronizado Bidireccional**: Al desplazar la rueda del ratón o la barra de scroll en el lado español, el lado en inglés se mueve exactamente al mismo tiempo y proporción (y viceversa), permitiendo comparar párrafos y tablas técnicas sin desfasarse jamás.
- **Estilo Ejecutivo Microsoft Word**: Páginas en fondo blanco con encabezado institucional (`AMDOCS MX | Senior RF Optimization Engineer – Ericsson 4G/5G`), cajas de estrategia verdes (`🎯 Estrategia y Tono`), cajas de respuesta modelo azul marino (`💬 Respuesta Modelo`), y bloques en tipografía `Consolas` para comandos Moshell y tablas de parámetros.
- **Índice Lateral Colapsable**: Panel lateral interactivo con las 31 preguntas maestras ordenadas por módulo, con botón **`📑 Ocultar / Mostrar Índice`** para maximizar el área de lectura a pantalla completa.
- **Navegación Rápida**: Botones **`◀ Ant`** y **`Sig ▶`** para saltar de pregunta en pregunta.
- **⚡ Botón "Al Teleprompter"**: Inyecta en 1 solo clic la respuesta de la guía en el teleprompter dual del copiloto (`1`).
- **📄 Botón "Abrir Word"**: Abre el archivo original `.docx` en Microsoft Word con integración nativa en Windows.

---

### 4. 🎯 Pestaña de Pitch Personal Dual (2)
- **Estructura Dividida en 2 Paneles**:
  - **Panel Superior (🇪🇸 Español)**: Pitch principal en español destacando +15 años de trayectoria en RAN, optimización LTE L15, Baseband Ericsson 5212/5216/6630, Radio Dot y auditoría de KPIs críticos (RTWP, PIM, DCR, Handover).
  - **Panel Inferior (🇺🇸 English)**: Versión técnica equivalente en inglés (60s) con terminología estándar 3GPP.
- **Opciones de Guión Rápido**:
  - **`📡 RF Pitch (Dual ES / EN)`**: Carga el pitch principal en español arriba y el pitch profesional en inglés abajo.
  - **`⚙️ KPIs & Ericsson Tech`**: Análisis técnico profundo de interferencias, pilot pollution, colisión/confusión PCI mod 3/mod 30, eventos de handover A1-A5/B1-B2 y Layer 3 signaling.
  - **`⚡ RF Rápido (30s)`**: Elevator pitch ultra conciso de 30 segundos.
  - **`🎓 Formación & MBA`**: Trayectoria académica (Ingeniería en Electrónica + MBA en Finanzas y Estrategia + Certificación Oficial Ericsson LTE Configuration).
- **Enfoque 100% Especializado**: Eliminación de postulaciones irrelevantes para mantener un perfil sólido, coherente y de máxima autoridad técnica en Ericsson RF.

---

### 5. ⌨️ Atajos Rápidos Ergonómicos (`1`, `2`, `3`)
- **`1`**: Ir a **🎙️ Copiloto en Vivo (Teleprompter Dual)**.
- **`2`**: Ir a **🎯 Mi Pitch & Formación (Javier Viveros Huesca)**.
- **`3`**: Ir a **📖 Guía Entrevista Word (31 temas ES / EN)**.
- **Salvaguarda Inteligente de Escritura**: Si estás escribiendo en el recuadro de pregunta o en la barra manual, presionar `1`, `2` o `3` escribe el número normalmente sin cambiar de pestaña.
- *(Mantiene compatibilidad total con `F1`, `F2`, `F3` y el teclado numérico `KP_1`, `KP_2`, `KP_3`)*.

---

## 🏗️ Flujo de Vinculación y Arquitectura

```mermaid
flowchart TD
    subgraph AudioYEntrada["1. Captura de Audio o Texto"]
        A["Audio de Reunión (Meet / Teams / Zoom)"] -->|WASAPI Loopback o Mic| B["audio_listener.py (VAD + Speech)"]
        T["Entrada Manual / Pregunta Editada"] --> B
    end

    subgraph DeteccionTematica["2. Motor Semántico de Guía Word"]
        B -->|Texto Detectado / Escrito| W["rf_word_guide.py (find_all_matches)"]
        W -->|Palabras Clave: dynamic, B2, RTWP, etc.| M{"¿Hay coincidencias en Guía Word?"}
        M -->|1 Coincidencia| C1["[ 📖 Q20: DSS (Mód 5) ➔ ]"]
        M -->|Multi-Match| C2["[ 📖 Q10: Handover B1/B2 ➔ ] [ 📖 Q17: Carrier Aggr ➔ ]"]
        M -->|No técnico / Saludos| NH["Ocultar Banner"]
    end

    subgraph NavegacionInteractiva["3. Salto con 1 Clic a Guía Word"]
        C1 -->|Clic en Opción| G["gui_prompter.py (_jump_to_matched_word_question)"]
        C2 -->|Clic en Opción| G
        G --> Tab3["Pestaña 3: Guía Word Dividida 50/50"]
        Tab3 --> Sync["Módulo Automático + Pregunta Seleccionada + Scroll Sincronizado ES / EN"]
    end

    subgraph GeneracionDual["4. Teleprompter Dual en Tiempo Real"]
        B -->|Pregunta| AI["gemini_copilot.py (Gemini 3.8 / DeepSeek)"]
        AI -->|Streaming Simultáneo| P1["Panel Superior: 🇪🇸 Español"]
        AI -->|Streaming Simultáneo| P2["Panel Inferior: 🇺🇸 English"]
    end
```

---

## 📋 Requisitos Previos

1. **Windows 10 / 11**.
2. **Python 3.10 o superior** (probado y optimizado en Python 3.12).
3. **Clave de API de Google Gemini** (gratuita vía Google AI Studio) o **DeepSeek / OpenRouter**.

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

### 3. Configurar tu Clave de API
Copia el archivo de plantilla `.env.example` como `.env`:
```bash
copy .env.example .env
```
Edita `.env` con tu clave:
```env
GEMINI_API_KEY=AIzaSyTuClaveReal...
GEMINI_MODEL=gemini-3.8-flash
AUDIO_LANGUAGE=es-ES
ALWAYS_ON_TOP=True
WINDOW_OPACITY=0.95
```
*(También puedes configurarla directamente en la GUI haciendo clic en el botón `🔑 API Key`)*.

---

## ▶️ Modos de Ejecución

### Opción A: Doble Clic (Windows)
- Doble clic en **`iniciar.bat`**: Inicia la interfaz gráfica flotante con teleprompter dual.
- O mediante el acceso directo en tu Escritorio **`Copiloto de Entrevista`**.

### Opción B: Ejecución por Terminal
```bash
.\venv\Scripts\python.exe main.py
```

### Opción C: Modo Consola (CLI con Colores)
```bash
.\venv\Scripts\python.exe main.py --cli
```

### Opción D: Prueba Rápida con Pregunta Simulada
```bash
.\venv\Scripts\python.exe main.py --test-question "Explica cómo configuras eventos B1 y B2 para handover inter-RAT"
```

---

## 💡 Consejos de Uso Durante una Entrevista Real

1. **Ubicación de la Ventana**:
   - Arrastra la ventana flotante y colócala en el centro superior de la pantalla, justo debajo de tu cámara web.
   - Al leer las respuestas en el teleprompter, tus ojos estarán mirando fijamente a la cámara, transmitiendo total contacto visual y seguridad.
2. **Selección del Dispositivo de Audio**:
   - **Con audífonos puestos**: Selecciona la opción que contenga `[Loopback]` (por ejemplo: *Speakers/Headphones [Loopback]*). El sistema capturará con nitidez digital lo que dice el entrevistador sin captar ruido ambiental ni eco de tu cuarto.
   - **Con altavoces externos**: Selecciona tu micrófono (`[Microfono]`).
3. **Uso de la Guía Word en Vivo**:
   - Cuando el entrevistador mencione conceptos como `B2`, `handover`, `RTWP` o `dynamic spectrum`, observa la barra interactiva que aparece debajo de la pregunta.
   - Si deseas consultar la fórmula, los comandos Moshell o la tabla técnica exacta de la guía oficial, haz clic sobre el chip correspondiente y repasa la respuesta modelo mientras la IA formula la respuesta en el copiloto.
4. **Copiado Rápido al Chat**:
   - Si el entrevistador solicita compartir texto o comandos por el chat de Zoom/Teams, utiliza los botones `📋 Copiar ES` o `📋 Copiar EN`, o bien selecciona el fragmento y presiona `Ctrl + C`.

---

## 📂 Estructura del Proyecto

```
Contestar-Entrevista/
├── .env.example          # Plantilla para variables de entorno
├── .gitignore            # Archivos excluidos (protege .env e historial privado)
├── requirements.txt      # Dependencias oficiales de Python
├── iniciar.bat           # Lanzador rápido de la ventana flotante
├── iniciar_consola.bat   # Lanzador rápido del modo terminal
├── main.py               # Punto de entrada principal (GUI, CLI y Tests)
├── config.py             # Configuración centralizada y System Prompts bilingües
├── candidate_profile.py  # Base de conocimiento y perfil de Senior RF Engineer (Javier Viveros)
├── rf_word_guide.py      # Motor de indexación, parsing y matching multi-coincidencia de Guía Word
├── GUIA_ENTREVISTA_RF_ERICSSON.md # Guía técnica de preparación para RF Optimization Engineer
├── Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.docx # Documento oficial Microsoft Word (10 Módulos - ES)
├── Guia_Entrevista_Senior_RF_Ericsson_4G_5G_ES.md   # Fuente Markdown enriquecida (10 Módulos - ES)
├── Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.docx # Official Microsoft Word Document (11 Modules - EN)
├── Interview_Guide_Senior_RF_Ericsson_4G_5G_EN.md   # Enriched Markdown Source (11 Modules - EN)
├── audio_listener.py     # Captura de audio y transcripción continua (Mic / Loopback)
├── gemini_copilot.py     # Cliente multi-IA (Gemini con auto-fallback, DeepSeek y OpenRouter)
├── gui_prompter.py       # GUI flotante con teleprompter dual, visor Word 50/50 y enlaces dinámicos
├── cli_prompter.py       # Interfaz para terminal interactiva con Colorama
├── history_logger.py     # Registro automático en Markdown y JSON
├── historial/            # Carpeta local privada con las notas de cada entrevista
└── README.md             # Documentación exhaustiva del sistema
```

---

## ⚙️ Tecnologías Utilizadas

- **[Google GenAI SDK](https://github.com/googleapis/python-genai)** (`google-genai`): Integración con Gemini 3.8 Flash.
- **[SpeechRecognition](https://github.com/Uberi/speech_recognition)**: Detección y transcripción continua de voz.
- **[PyAudioWPatch](https://github.com/s0d3s/PyAudioWPatch)**: Captura digital de bucle invertido (WASAPI Loopback) sin eco en Windows.
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)**: Interfaz gráfica nativa ultraligera de baja latencia.
- **[Colorama](https://github.com/tartley/colorama)**: Formato de consola para PowerShell y CMD.

---

## 📄 Licencia

Este proyecto está distribuido bajo la licencia MIT. Diseñado con fines educativos y de asistencia técnica en tiempo real durante entrevistas laborales de alta exigencia.
