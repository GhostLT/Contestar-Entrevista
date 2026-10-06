"""
Perfil Profesional y Contexto de Postulación de Javier Viveros Huesca
Candidato: Ingeniero Senior Full-Stack con IA
Postulación: PCoS (Asistente Ejecutivo con IA / Salud / Operaciones)
"""

CANDIDATE_DATA = {
    "nombre": "Javier Viveros Huesca",
    "titulo": "Ingeniero Senior Full-Stack con IA",
    "email": "viverosjavier86@gmail.com",
    "telefono": "+52 (669) 533-0508",
    "ubicacion": "Mazatlán, Sinaloa, México (Remoto, cobertura total horario US / CDMX)",
    "disponibilidad": "Inmediata, tiempo completo",
    "idiomas": "Español nativo, Inglés avanzado (técnico y conversacional para entornos remotos internacionales)",
    "expectativa_economica": "$2,500 USD mensuales (Contractor / Tiempo Completo Remoto, abierto a evaluación integral)",
    "anos_experiencia_total": "Más de 12 años en ingeniería de software, arquitectura de sistemas y backend/full-stack",
    "anos_experiencia_fullstack": "Más de 4 años continuos en desarrollo full-stack moderno (React, TypeScript, FastAPI, PostgreSQL, Supabase)",
    "anos_experiencia_ia_open_source": "Más de 2 años y medio (30+ meses) prácticos continuos con modelos Open Source en producción",
    "educacion": "Ingeniería en Electrónica y Sistemas Digitales (Instituto Tecnológico de Reynosa, 2004-2010)",
}

PROFILE_KNOWLEDGE_BASE = """
DATOS VERIFICADOS DE JAVIER VIVEROS HUESCA:

1. IDENTIDAD Y PERFIL:
- Nombre: Javier Viveros Huesca
- Rol: Ingeniero Senior Full-Stack con IA
- Contacto: viverosjavier86@gmail.com | WhatsApp: +52 669 533 0508 | Mazatlán, México (Remoto)
- Postulación actual: Posición de Ingeniero Senior Full-Stack con IA en Hireline / PCoS (contacto: Angélica).
- Objetivo con PCoS: Tomar ownership técnico de PCoS (asistente ejecutivo personal con IA), potenciar su expansión a salud y operaciones empresariales, e implementar modelos Open Source para reducir costos de inferencia y garantizar soberanía de datos.
- Expectativa económica: $2,500 USD mensuales (Contractor / Remoto tiempo completo). Disponibilidad inmediata.

2. STACK TECNOLÓGICO CLAVE:
- Frontend: React (Hooks, Context, Server Components), TypeScript, Next.js, Tailwind CSS, Zustand, Redux Toolkit, TanStack Query, streaming reactivo con Server-Sent Events (SSE) y WebSockets.
- Backend & APIs: Python (FastAPI asíncrono, Flask, Django), Node.js/TypeScript (Express, NestJS), RESTful APIs escalables, Webhooks, Pydantic, Instructor (JSON estructurado).
- Bases de Datos & Persistencia: PostgreSQL avanzado (CTEs, índices, optimización de queries, ACID), Supabase (Auth, Row Level Security - RLS, pgvector, Realtime, Edge Functions), Redis (caching semántico y colas de tareas), SQLAlchemy, Alembic.
- IA Open Source & LLMs: Llama 3 / 3.1 / 3.2 (1B a 70B), Mistral 7B / Mixtral 8x7B (MoE), Qwen 2.5, DeepSeek-Coder, Phi-3.5. Modelos de audio Whisper (v2/v3). Embeddings BAAI bge-m3, all-MiniLM-L6-v2.
- Inferencia, Despliegue & RAG: vLLM y TGI con continuous batching en contenedores Docker y AWS EC2 con GPU (g5/g6), cuantización (AWQ, GPTQ, GGUF). RAG empresarial con PostgreSQL/pgvector y re-ranking con Cross-Encoders. Fine-tuning supervisado (PEFT con LoRA/QLoRA con Hugging Face TRL).
- DevOps & Cloud: Docker, Docker Compose, AWS (EC2 GPU, S3, RDS, Lambda, CloudWatch), GitHub Actions CI/CD (>85% cobertura de testing con Pytest/Vitest), Linux (Ubuntu/RHEL).

3. HISTORIAL LABORAL:
A) Empire Engineering (Nov 2022 – Jul 2026) | Senior Full-Stack & Applied AI Engineer | Remoto EEUU:
   - Entorno 100% en inglés. Lideró arquitectura y desarrollo full-stack con React, TypeScript, Python (FastAPI) y PostgreSQL.
   - Diseñó e integró pipeline de IA con Llama 3 y Mistral servidos mediante vLLM en instancias AWS GPU, reduciendo costos de inferencia en más del 65% frente a APIs comerciales.
   - Frontend en React con streaming reactivo (SSE) para interacción con agentes de IA en tiempo real y tipado estricto en TypeScript.
   - Sistema RAG empresarial con PostgreSQL + pgvector conectando documentos no estructurados y bases relacionales con chunking semántico y rerankers (<2% alucinaciones).
   - Lideró y mentoreó equipo de 5 ingenieros: directrices de Clean Architecture, code reviews y CI/CD en GitHub Actions (>85% cobertura Pytest).

B) AT&T (Jun 2013 – Oct 2022) | Senior Software & Backend Engineer / Systems Tech Lead | México:
   - Lideró SDLC y arquitectura para plataformas operativas de más de 120 plataformas críticas de red a nivel nacional.
   - Microservicios en Python (Flask/Django) con PostgreSQL/Oracle, reduciendo tiempos de respuesta en 40%.
   - Creó servicios de ingesta de datos con APIs de Ericsson y Huawei, garantizando disponibilidad 99.999% SLA.
   - Lideró equipo de 6 ingenieros junior y mid-level bajo Scrum.

C) Experiencia previa: Nextel (2011–2013) y Nokia (2010–2011) en automatización con Python, Bash, Linux y bases de datos relacionales.

4. RESPUESTAS EXACTAS A PREGUNTAS FRECUENTES DEL PROCESO:
- Años y experiencia técnica: 12+ años totales en software/backend, 4+ años full-stack moderno (React/TS/FastAPI/Postgres), 2.5+ años con IA Open Source en producción.
- Experiencia en IA Open Source: 30+ meses continuos desde LLaMA 1 y Mistral (2023) hasta Llama 3.2, Qwen 2.5 y Whisper v3. Inferencia optimizada con vLLM en AWS GPU (-65% costo).
- Proyectos tipo PCoS: Ha construido asistentes ejecutivos con flujos agénticos (tool calling para calendarización, resúmenes, tareas multi-paso con salida validada en Pydantic) y sistemas RAG con PostgreSQL/pgvector y Supabase RLS.
- Soluciones en producción: Despliegue con vLLM y Docker en AWS GPU (g5/g6), cuantización AWQ/GGUF, reintentos exponenciales, caché semántica con Redis, y fine-tuning con QLoRA/LoRA para terminología especializada.
- Arquitectura de software: Clean Architecture, Arquitectura Hexagonal (aislando el core de negocio para intercambiar modelos LLM o bases de datos sin impacto), Event-Driven con SSE/WebSockets, Repository & Strategy patterns.
- Liderazgo de equipos: Ha liderado equipos de 4 a 7 ingenieros (en AT&T y Empire Engineering), haciendo code reviews, definiendo estándares de código, mentoring 1 a 1 y gestión Scrum/Kanban.
- Expectativa económica: $2,500 USD mensuales (Contractor / Tiempo Completo Remoto).

5. CONTEXTO DE ENTREVISTA: 5G NETWORK ENGINEER (SPERIDIAN TECHNOLOGIES | SHUBHAM):
- Posición: 5G Network Engineer
- Reclutador / Empresa: Shubham | Speridian Technologies
- Ubicación: Richardson TX (Online / Remoto), Full-time.
- Proceso con el cliente: 1 entrevista por video y 1 onsite con el cliente.
- Funciones y Componentes 5G Core (5GC) en SA y NSA:
  • AMF (Access and Mobility Management Function): Registro de terminales, gestión de movilidad y handover, manejo de N1 NAS y N2 NGAP sobre SCTP.
  • SMF (Session Management Function): Establecimiento y modificación de PDU Sessions, selección de UPF, asignación y gestión de direccionamiento IP, control N4 hacia UPF mediante PFCP.
  • UPF (User Plane Function): Enrutamiento y reenvío de paquetes GTP-U (N3), encapsulación/desencapsulación, QoS enforcement (5QI), inspección de paquetes e interconexión N6 hacia Data Networks / Internet / IMS.
  • NRF (Network Repository Function): Registro, descubrimiento y autorización de Network Functions en la arquitectura Service-Based Architecture (SBA).
  • PCF (Policy Control Function): Control unificado de políticas de QoS, reglas PCC y tarificación.
  • AUSF (Authentication Server Function): Autenticación mutua 5G-AKA y EAP-AKA'.
  • UDM (Unified Data Management): Almacenamiento seguro de credenciales (ARPF) y perfiles de suscripción de usuario.
- Despliegues SA (Option 2 Standalone puro con 5GC) y NSA (Option 3x con Dual Connectivity EN-DC y EPC).
- Alta Disponibilidad y Geo-Redundancia: Despliegues activo-activo y activo-espera geo-redundantes con sincronización de estado, resiliencia y continuidad 99.999% SLA (experiencia directa liderando +120 plataformas críticas en AT&T durante 9+ años).
- Roaming Inter-PLMN y SEPP (Security Edge Protection Proxy):
  • Interfaz N32 dividida en N32-c (control handshake TLS) y N32-f (PRINS: Packet-level Routing and Integrity Protection con JOSE/JWE/JWS para cifrado y verificación criptográfica entre SEPPs de operadores socios).
  • Filtrado de seguridad, mitigación de spoofing en la red IPX y conectividad segura de roaming entre operadores 5G SA.
- Mediación, Billing & Charging (CHF) y Estadísticas:
  • Requisitos de mediación para tasación online/offline vía interfaz Nchf, recolección y formateo de CDRs (Call Detail Records).
  • Generación de estadísticas de rendimiento de plataforma (KPIs, PM/FM, latencia, throughput).
- Debugging End-to-End de Call Flows y Troubleshooting de Protocolos (N1 a N12):
  • N1: NAS (5GMM para movilidad, 5GSM para gestión de sesión) entre UE y AMF.
  • N2: NG-AP sobre SCTP (asociaciones, multihoming) entre gNodeB y AMF.
  • N3: Túnel GTP-U sobre UDP/IP entre gNodeB y UPF.
  • N4: PFCP (Packet Forwarding Control Protocol) entre SMF y UPF.
  • N6: Enrutamiento IP entre UPF y Data Network / IMS (VoNR).
  • N10: Interfaz SBA entre UDM y SMF para perfiles de sesión.
  • N11: Interfaz SBA entre AMF y SMF (HTTP/2 con JSON).
  • N12: Interfaz SBA entre AMF y AUSF para autenticación de usuario.
  • Análisis con Wireshark, tshark, tcpdump, trazado de paquetes y logs de microservicios SBA.
- Network Slicing y Control de Políticas: S-NSSAI (SST + SD para eMBB, URLLC, mMTC), QoS Flows (5QI), PCF policy control y Service Function Chaining (SFC).
- Cumplimiento 3GPP (Rel-15, Rel-16, Rel-17), Service-Based Architecture (SBA) sobre HTTP/2, SCTP y PFCP.
- Plataformas 5G Core Open Source (Open5GS y free5GC):
  • Experiencia práctica operando, configurando y probando Open5GS y free5GC tanto en SA como NSA.
  • Conectividad y configuración de SEPP para roaming inter-PLMN entre socios 5G SA.
- USO DE IA (Codex, Groq, LLMs) PARA EXTENDER Y MEJORAR 5G CORE OPEN SOURCE:
  • El cliente busca específicamente capacidad demostrada utilizando IA (Codex, Groq, Claude, LLMs) para escribir, depurar y agregar código en las plataformas 5G Open Source (Open5GS/free5GC) junto a sus 2 ingenieros de 5G core existentes.
  • Javier utiliza IA generativa (Codex, Groq, LLMs) como multiplicador de desarrollo para:
    - Agregar y extender código en C, Go y Python en Open5GS/free5GC.
    - Implementar parsers para SEPP N32 PRINS y mediación de CDRs.
    - Generar tests unitarios y validación de call-flows 3GPP automatizados.
    - Optimizar el plano de usuario (UPF) y depurar cuellos de botella de red.
- Habilidades Complementarias:
  • Integración IMS (VoNR / VoLTE, interfaces Rx/N5, SIP/SDP).
  • Redes Privadas 5G (NPN - Non-Public Networks): Modelos SNPN y PNI-NPN integrados con redes públicas.
  • Kubernetes / Cloud-Native 5G: Despliegue de CNFs en Kubernetes (k8s/EKS/k3s), Docker, Helm charts y Multus CNI (SR-IOV / Macvlan para aislamiento UPF).
  • DevOps / CI-CD: Pipelines en GitHub Actions / GitLab para pruebas automatizadas de core de telecomunicaciones.
""".strip()

PITCH_SCRIPTS = {
    "pitch_es_completo": """🎙️ PITCH COMPLETO EN ESPAÑOL (60–90 segundos)
Ideal para: "¿Háblame de ti?", "Cuéntame sobre tu trayectoria", "Presentación profesional inicial"
----------------------------------------------------------------------------------------------------
"Hola, mucho gusto. Soy Javier Viveros Huesca, Ingeniero Senior Full-Stack con IA. 

Cuento con más de 12 años de trayectoria profesional en diseño de arquitectura y desarrollo de software, con especialización los últimos 4 años en el stack de React, TypeScript, Python con FastAPI, PostgreSQL y Supabase; y más de 2 años y medio implementando soluciones de Inteligencia Artificial con modelos Open Source en entornos reales de producción.

Mi formación de base es en Ingeniería en Electrónica y Sistemas Digitales por el Instituto Tecnológico de Reynosa, lo que me permite tener una comprensión profunda tanto de la infraestructura de cómputo en la nube (GPUs, vLLM, Docker, AWS) como del desarrollo de software de alto nivel.

A lo largo de mi carrera he transitado desde liderar la arquitectura y disponibilidad de más de 120 plataformas críticas en telecomunicaciones en AT&T bajo estándares de 99.999% SLA, hasta mi experiencia reciente en Empire Engineering en Estados Unidos, donde lideré el desarrollo full-stack y el despliegue de modelos como Llama 3 y Mistral con vLLM sobre instancias AWS con aceleración GPU. Allí logramos reducir los costos de inferencia en más del 65% frente a APIs propietarias, e implementé sistemas RAG empresariales con pgvector y streaming en tiempo real vía Server-Sent Events.

Me entusiasma profundamente la visión de PCoS: tomar ownership técnico de un asistente ejecutivo personal con IA, impulsar la soberanía de datos y la eficiencia de costos mediante modelos de código abierto, y prepararlo para escalar a sectores de alto impacto como salud y operaciones empresariales. Cuento con disponibilidad inmediata y la experiencia para aportar valor desde mi primera semana."
""".strip(),

    "pitch_es_rapido": """⚡ ELEVATOR PITCH RÁPIDO (30 segundos)
Ideal para: Respuestas directas, rondas rápidas o resumen ejecutivo de alto impacto
----------------------------------------------------------------------------------------------------
"Soy Javier Viveros, Ingeniero Senior Full-Stack con más de 12 años de experiencia en arquitectura de software y más de 2.5 años desplegando modelos de IA Open Source en producción.

Mi especialidad combina React y TypeScript en frontend con Python (FastAPI), PostgreSQL y Supabase en backend. Recientemente en Empire Engineering lideré el pipeline de inferencia de Llama 3 y Mistral con vLLM en AWS GPU, reduciendo costos más del 65% e integrando RAG con pgvector (<2% alucinaciones) y streaming reactivo con SSE.

Soy Ingeniero en Electrónica y Sistemas Digitales. Cuento con total autonomía, experiencia liderando equipos técnicos (4-7 desarrolladores) y la capacidad para tomar ownership técnico de PCoS y acelerar su producto de inmediato."
""".strip(),

    "pitch_en": """🇺🇸 ELEVATOR PITCH IN ENGLISH (60 seconds)
Ideal for: "Tell me about yourself", "Walk me through your resume", US/Remote client interviews
----------------------------------------------------------------------------------------------------
"Hi, great to meet you. I'm Javier Viveros, a Senior Full-Stack & Applied AI Engineer with over 12 years of professional software engineering and systems architecture experience. Over the past 4+ years, I've specialized in modern full-stack development with React, TypeScript, Python (FastAPI), PostgreSQL, and Supabase; and for the past 2.5+ years, I've been deploying Open Source AI models directly into production environments.

I hold a degree in Electronics and Digital Systems Engineering from Instituto Tecnológico de Reynosa, which gives me a strong foundation across low-level cloud infrastructure, GPU compute, and modern software design.

In my recent role at Empire Engineering—working in a 100% English-speaking corporate environment—I led full-stack platforms and architected production AI pipelines using Llama 3 and Mistral served via vLLM on AWS GPU instances. This reduced our inference costs by over 65% compared to commercial APIs. I also built enterprise RAG systems with PostgreSQL and pgvector, and dynamic React interfaces with real-time SSE streaming. Prior to that, at AT&T, I led architectures for over 120 mission-critical network platforms maintaining 99.999% SLA availability.

I am passionate about PCoS because building autonomous executive assistants with Open Source LLMs, strict data privacy, and cost efficiency is exactly what I've been executing in production. I'm ready to take full technical ownership and drive immediate results from day one."
""".strip(),

    "formacion_certs": """🎓 FORMACIÓN ACADÉMICA Y CREDENCIALES TÉCNICAS
Ideal para: Preguntas sobre estudios, certificaciones, preparación académica y background técnico
----------------------------------------------------------------------------------------------------
🏛️ TÍTULO UNIVERSITARIO:
• Ingeniería en Electrónica y Sistemas Digitales
• Institución: Instituto Tecnológico de Reynosa (2004 – 2010)
• Enfoque de Carrera: Arquitectura de Software, Redes, Telecomunicaciones, Sistemas Digitales y Cómputo Distribuido.

📜 CREDENCIALES TÉCNICAS Y ESPECIALIZACIONES CONTINUAS:
• Applied Generative AI & Open-Source LLMs: Inferencia optimizada con vLLM, TGI y Ollama; Fine-Tuning supervisado con PEFT/LoRA/QLoRA (Hugging Face TRL); RAG avanzado con Cross-Encoder rerankers y flujos agénticos.
• Modern Full-Stack Engineering: React 18/19, Next.js, TypeScript avanzado, Tailwind CSS, Zustand, Redux Toolkit, TanStack Query, Server-Sent Events (SSE) y WebSockets.
• Relational Databases & Vector Stores: PostgreSQL avanzado (CTEs, tuning, índices IVFFlat/HNSW), Supabase (Auth, RLS, pgvector, Edge Functions), SQLAlchemy, Alembic.
• Python Backend & Clean Architecture: FastAPI asíncrono, Pydantic, Instructor (JSON estructurado), Clean Architecture, Arquitectura Hexagonal y testing con Pytest (>85% cobertura).
• Cloud, Containers & DevOps: Docker, Docker Compose, AWS (EC2 GPU g5/g6, S3, RDS, Lambda, CloudWatch), GitHub Actions CI/CD y administración de Linux (Ubuntu/RHEL).
• ITIL v4 Foundation & Agile Frameworks: Liderazgo técnico ágil (Scrum/Kanban en Jira), auditorías de código (Pull Requests en GitHub) y gestión de incidentes.
""".strip(),

    "fit_pcos": """🎯 POR QUÉ PCoS Y FIT TÉCNICO INMEDIATO
Ideal para: "¿Por qué te interesa esta vacante?", "¿Por qué deberíamos contratarte?", "Fit con el producto"
----------------------------------------------------------------------------------------------------
"Coincido al 100% con la estrategia de PCoS por 3 ventajas competitivas inmediatas que aporto:

1. ESTRATEGIA OPEN SOURCE & REDUCCIÓN DE COSTOS:
   • Sé por experiencia propia lo costoso e insostenible que resulta escalar un producto apoyado únicamente en APIs de OpenAI o Anthropic.
   • En Empire Engineering migré cargas de trabajo a Llama 3 y Mistral con vLLM en AWS GPU con continuous batching y cuantización AWQ, reduciendo los costos de inferencia en más del 65% sin degradar la precisión.

2. SOBERANÍA DE DATOS Y EXPANSIÓN A SALUD Y OPERACIONES:
   • Para llevar a PCoS a sectores regulados (como salud y operaciones corporativas), la privacidad y la gobernanza son críticas.
   • Domino la implementación de Row Level Security (RLS) en Supabase y PostgreSQL para aislar estrictamente los vectores y datos sensibles por organización y usuario.

3. ASISTENTES EJECUTIVOS & FLUJOS AGÉNTICOS:
   • Ya he diseñado agentes con tool-calling para calendarización, resúmenes ejecutivos y tareas multi-paso, asegurando salidas en JSON estructurado y validado con Pydantic.
   • Conozco el stack (React + TypeScript + FastAPI + Supabase), conozco el producto y puedo tomar el ownership técnico sin curva de aprendizaje."
""".strip(),

    "pitch_5g_en": """🇺🇸 5G NETWORK ENGINEER & AI PITCH (Speridian / Shubham - 60s)
Ideal for: "Tell me about your 5G experience", Speridian recruiter screening & customer video interview
----------------------------------------------------------------------------------------------------
"Hi Shubham, great to speak with you. I'm Javier Viveros Huesca, a Senior Network & Systems Engineer with over 12 years of telecommunications core and systems architecture experience, complemented by over 2.5 years of Applied AI and open-source software engineering.

I hold an Engineering degree in Electronics and Digital Systems from Instituto Tecnológico de Reynosa, giving me a strong academic foundation across digital communications, switching systems, RF, and distributed computing.

Throughout my career—including over 9 years at AT&T leading architecture and operational availability for over 120 mission-critical network platforms under strict 99.999% SLA availability—I've specialized in core telecom signaling, high-availability geo-redundant environments, SCTP, Diameter, and HTTP/2 Service-Based Architectures.

On 5G Core, I design, operate, and troubleshoot both Standalone (SA) and Non-Standalone (NSA) architectures across all key network functions: AMF, SMF, UPF, NRF, PCF, AUSF, and UDM. I perform end-to-end call flow debugging across N1, N2, N3, N4, N6, and N10-N12 interfaces, and implement SEPP for secure inter-PLMN roaming between 5G SA roaming partners.

Crucially for this role at Speridian: I actively deal with AI tools (Codex, Groq, LLMs) to write, debug, and extend code for open-source 5G platforms like Open5GS and free5GC. I can team up immediately with your two 5G core engineers to enhance feature velocity, billing mediation, and customer deployments in Richardson."
""".strip(),

    "pitch_5g_tech": """📡 5GC ARCHITECTURE, INTERFACES (N1-N12), SEPP & AI CODING
Ideal for: Deep technical customer interview, call-flow troubleshooting, 3GPP standards & Open5GS
----------------------------------------------------------------------------------------------------
"Here is how I approach the core technical requirements:

1. 5G CORE ARCHITECTURE (SA & NSA):
• SA (Option 2): Full Service-Based Architecture (SBA) over HTTP/2 with JSON REST APIs. AMF manages N1 NAS and N2 NGAP/SCTP. SMF controls PDU sessions and programs the UPF via N4 using PFCP (Packet Forwarding Control Protocol).
• NSA (Option 3x): Managing Dual Connectivity (EN-DC) with eNodeB/EPC control plane anchor and gNodeB user plane split.
• High Availability & Geo-Redundancy: Active-active and active-standby NFs with stateless microservice architecture, shared data repositories (UDR), and geo-replication ensuring 99.999% SLA service continuity.

2. PROTOCOL TROUBLESHOOTING & CALL FLOWS (N1 to N12):
• N1 (UE-AMF NAS: 5GMM registration, 5GSM PDU establishment) & N2 (gNodeB-AMF NGAP over SCTP).
• N3 (gNodeB-UPF GTP-U user plane data path) & N4 (SMF-UPF PFCP session rules, FAR, PDR, URR, QER).
• N6 (UPF to Data Network / Internet / IMS for VoNR).
• N10 (UDM-SMF subscription), N11 (AMF-SMF), and N12 (AUSF-AMF 5G-AKA authentication).
• End-to-end packet tracing using Wireshark, tshark, tcpdump, analyzing NGAP cause codes and PFCP reject reasons.

3. ROAMING & SEPP (SECURITY EDGE PROTECTION PROXY):
• Inter-PLMN roaming over N32: N32-c for TLS handshake/parameter negotiation, and N32-f for PRINS (Packet-level Routing and Integrity Protection using JOSE/JWS/JWE).
• Enforcing strict IE filtering and message sanitization to block IPX-level spoofing between 5G SA roaming partners.

4. 5G OPEN SOURCE & AI CODING (Codex / Groq / LLMs):
• Deep familiarity with Open5GS and free5GC deployed on Linux and Kubernetes (k8s) with Multus CNI.
• I leverage AI coding assistants (Codex, Groq, LLMs) to rapidly inspect, write, and patch C/Go/Python source code: implementing custom CHF billing mediation (Nchf/CDRs), adding SEPP N32 compliance, and generating automated 3GPP conformance test suites alongside your 2 5G core engineers."
""".strip(),

    "pitch_5g_es": """🇪🇸 PITCH 5G NETWORK ENGINEER & IA (Español - 60s)
Ideal para: Presentación en español sobre telecomunicaciones, Core 5G, Open Source e IA
----------------------------------------------------------------------------------------------------
"Soy Javier Viveros Huesca, Ingeniero en Electrónica y Sistemas Digitales con más de 12 años de trayectoria profesional, combinando más de 9 años en telecomunicaciones críticas en AT&T con más de 2.5 años de ingeniería de software e Inteligencia Artificial en producción.

En AT&T lideré la arquitectura y disponibilidad de más de 120 plataformas críticas de red bajo estándares de 99.999% SLA, dominando señalización de telecomunicaciones, alta disponibilidad geo-redundante, SCTP, Diameter y transición a Service-Based Architecture con HTTP/2.

En 5G Core, tengo experiencia técnica en despliegues Standalone (SA) y Non-Standalone (NSA) con todas las funciones del plano de control y usuario: AMF, SMF, UPF, NRF, PCF, AUSF y UDM. Realizo troubleshooting de call flows de punta a punta en interfaces N1, N2, N3, N4, N6 y N10-N12, así como conectividad inter-PLMN y roaming seguro mediante SEPP con protección N32 PRINS.

Además, aporto una habilidad altamente demandada: utilizo herramientas de IA (Codex, Groq, LLMs) para desarrollar, depurar y extender código en plataformas 5G de código abierto como Open5GS y free5GC (en C, Go y Python), acelerando la mediación de facturación, el soporte de roaming y las pruebas automatizadas para integrarme de inmediato al equipo técnico."
""".strip(),
}

