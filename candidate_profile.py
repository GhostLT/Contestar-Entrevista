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
""".strip()
