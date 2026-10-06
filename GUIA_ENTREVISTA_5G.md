# 📡 Guía Maestra de Entrevista: 5G Network Engineer & AI Developer
## Speridian Technologies | Richardson, TX | Candidato: Javier Viveros Huesca

Esta guía está diseñada para preparar y superar con éxito las fases del proceso de selección para la vacante de **5G Network Engineer** con **Shubham de Speridian Technologies** y su cliente en **Richardson, TX** (1 entrevista técnica por video y 1 entrevista presencial / onsite).

---

## 📌 Ficha de la Posición y Dinámica del Proceso

| Campo | Detalle |
| :--- | :--- |
| **Puesto** | **5G Network Engineer** |
| **Reclutador** | **Shubham** (Speridian Technologies) |
| **Modalidad / Ubicación** | Richardson, TX Online / Fulltime |
| **Proceso de Selección** | **1 Video Entrevista** técnica inicial + **1 Onsite Entrevista** con el cliente final |
| **Equipo de Trabajo** | 2 ingenieros de 5G Core existentes en planta |
| **Objetivo Clave** | Operar y evolucionar la plataforma 5G Core Open Source (Open5GS / free5GC) potenciándola con **Inteligencia Artificial (Codex, Groq, LLMs)** para acelerar el desarrollo y despliegue de funcionalidades |

---

## 🎙️ Fase 1: Llamada Inicial con el Reclutador (Shubham)

### 1. Elevator Pitch en Inglés (60 segundos)
> *"Hi Shubham, thank you for reaching out. I'm Javier Viveros Huesca. I have over 12 years of core telecommunications and systems engineering experience, coupled with over 2.5 years of Applied AI and open-source software development.*
>
> *I hold an Engineering degree in Electronics and Digital Systems from Instituto Tecnológico de Reynosa. Throughout my career—including more than 9 years at AT&T where I led architecture and availability for over 120 mission-critical network platforms under strict 99.999% SLA standards—I have specialized in telecom core signaling, high availability, SCTP, Diameter, and HTTP/2 Service-Based Architectures.*
>
> *In 5G Core, I design, operate, and debug both Standalone (SA) and Non-Standalone (NSA) architectures across AMF, SMF, UPF, NRF, PCF, AUSF, and UDM. I perform end-to-end call flow debugging across N1 to N12 interfaces, and implement SEPP for secure inter-PLMN roaming.*
>
> *What makes this role a perfect fit: I actively use generative AI coding assistants like Codex, Groq, and LLMs to write, optimize, and extend C/Go code for open-source 5G cores such as Open5GS and free5GC. I can seamlessly team up with your two existing core engineers to accelerate code delivery and customer features."*

### 2. Checklist Rápido de Preguntas de Filtro (Screening)
* **¿Tienes disponibilidad para Richardson, TX?**: *"Yes, I am fully committed to the role and available for the online process and the customer onsite round in Richardson, TX."*
* **¿Cuál es tu disponibilidad de inicio?**: *"Immediate availability (disponibilidad inmediata)."*
* **¿Tienes experiencia con los 2 ingenieros de core existentes?**: *"Yes, I have led and collaborated in engineering teams of 4 to 7 engineers. My role here will be a technical force multiplier, using AI and deep telecom core experience to develop and test features alongside them."*

---

## ⚙️ Fase 2: Video Entrevista Técnica con el Cliente (1 Video)

### Pregunta 1: Arquitectura 5G Core (SA vs NSA)
* **Pregunta**: *"Can you explain the main architectural differences between 5G SA (Option 2) and NSA (Option 3x), and how the Core Network Functions interact?"*
* **Respuesta Maestra**:
  * **Option 3x (NSA)**: Utiliza el EPC (4G Core) como ancla de plano de control (MME/SGW). El gNodeB (NR) se conecta a la eNodeB vía X2 y el tráfico de plano de usuario (N3/S1-U) se divide hacia el gNodeB para máximo throughput sin requerir un 5GC completo de inmediato.
  * **Option 2 (SA)**: Arquitectura nativa 5G Core basada en microservicios (**Service-Based Architecture - SBA**) sobre HTTP/2 con payloads JSON:
    * **AMF**: Termina N1 (NAS) y N2 (NGAP sobre SCTP). Gestiona autenticación, movilidad y registro del UE.
    * **SMF**: Controla la sesión PDU, asigna IP del UE y programa las reglas del UPF vía N4 (PFCP).
    * **UPF**: Enrutador del plano de usuario. Recibe tráfico GTP-U por N3 y lo entrega a la red de datos por N6 con políticas de QoS (5QI).
    * **NRF**: Repositorio de registro y descubrimiento de NFs vía API REST.
    * **UDM / AUSF**: Manejo de credenciales de suscriptor (SUPI/SUCI) con autenticación 5G-AKA o EAP-AKA'.

### Pregunta 2: Call Flows de Registro y Sesión PDU (N1 a N12)
* **Pregunta**: *"Walk me through the end-to-end call flow when a UE powers on, registers, and establishes an Internet PDU session."*
* **Flujo Paso a Paso**:
  1. **N1 / N2 (Registration Request)**: El UE envía `Registration Request` encapsulado en RRC hacia el gNodeB. El gNodeB envía el mensaje `NGAP Initial UE Message` sobre SCTP por la interfaz **N2** al **AMF**.
  2. **N12 (Authentication)**: El AMF consulta al **AUSF** (`Nausf_UEAuthentication_AuthenticateRequest`). AUSF consulta a **UDM** (`Nudm_UEAuthentication_GetRequest`) para obtener vectores de autenticación 5G-AKA (RAND, AUTN, HXRES*).
  3. **N8 (Subscription)**: El AMF obtiene datos de acceso y suscripción desde **UDM** (`Nudm_SDM_Get`).
  4. **N1 / N2 (Registration Accept & Security)**: AMF envía `NAS Security Mode Command` y finalmente `Registration Accept`.
  5. **N1 / N11 (PDU Session Establishment)**: UE envía `PDU Session Establishment Request` por N1 NAS. AMF lo redirige al **SMF** seleccionado vía N11 (`Nsmf_PDUSession_CreateSMContext`).
  6. **N10 / N7 (Session Rules)**: SMF consulta datos de sesión en UDM (N10) y políticas de QoS en **PCF** (N7 `Npcf_SMPolicyControl_Create`).
  7. **N4 (PFCP Session Establishment)**: SMF programa el **UPF** mediante PFCP sobre UDP puerto 8805:
     * **PDR (Packet Detection Rule)**: Identifica paquetes entrantes gNodeB / N6.
     * **FAR (Forwarding Action Rule)**: Define reenvío / encapsulación GTP-U.
     * **URR (Usage Reporting Rule)**: Contabilización para facturación.
     * **QER (QoS Enforcement Rule)**: Asigna 5QI, MBR y GBR.
  8. **N2 / N3 (Tunnel Activation)**: AMF envía `NGAP PDU Session Resource Setup Request` al gNodeB con el GTP-TEID e IP del UPF. El gNodeB responde con su GTP-TEID de downlink hacia el UPF.
  9. **N6**: El túnel de datos queda activo; tráfico de usuario fluye desde el UE -> gNodeB -> N3 (GTP-U) -> UPF -> N6 -> Internet / IMS.

### Pregunta 3: Inter-PLMN Roaming y SEPP (Security Edge Protection Proxy)
* **Pregunta**: *"How does 5G inter-PLMN roaming work and what role does SEPP play over N32?"*
* **Respuesta Maestra**:
  * En 5G SA, las interfaces SBI (HTTP/2) no deben exponerse desprotegidas en Internet ni en redes de carrier IPX.
  * **SEPP (Security Edge Protection Proxy)** actúa como gateway de frontera de seguridad entre la V-PLMN (Visitada) y la H-PLMN (Home):
    * **N32-c (Control)**: Establece una conexión TLS directa entre los c-SEPPs para negociar parámetros de seguridad, suites criptográficas e IEs a proteger.
    * **N32-f (Forwarding)**: Utiliza **PRINS** (Packet-level Routing and Integrity Protection using JOSE standards: JWE para cifrado de campos sensibles y JWS para firmas criptográficas e integridad). Permite que los proveedores IPX intermedios lean cabeceras de enrutamiento sin descifrar ni alterar la carga útil del suscriptor.
    * **Filtrado de IEs**: SEPP descarta mensajes con SUPIs o atributos manipulados, neutralizando ataques de spoofing y tracking de abonados.

### Pregunta 4: Mediación de Facturación / Charging (CHF) y CDRs
* **Pregunta**: *"How do you handle charging and billing mediation on 5G Core?"*
* **Respuesta Maestra**:
  * Mediante la función **CHF (Charging Function)** y la interfaz Service-Based **Nchf**:
    * **Converged Charging**: Soporte tanto para Offline Charging (generación diferida de CDRs para pospago) como Online Charging (control de cuota en tiempo real con reserva de unidades para prepago).
    * El SMF reporta el consumo de datos recopilado desde el UPF (vía PFCP URR) hacia el CHF usando `Nchf_ConvergedCharging_Create` y `Update`.
    * En el core de código abierto (Open5GS), implemento y extiendo mediadores en Python/Go asistidos por IA para transformar CDRs en formatos ASN.1, CSV o eventos JSON hacia Kafka para los sistemas BSS/OSS corporativos.

### Pregunta 5: Potenciación de 5G Core con IA (Codex, Groq, LLMs)
* **Pregunta**: *"The job description mentions using AI (Codex, Groq, LLMs) to add code to open-source 5G platforms. How do you practically do that with 2 existing core engineers?"*
* **Respuesta Maestra**:
  * *"I use AI coding tools as an accelerator, not a black box:*
    1. **Code Comprehension & Feature Extension**: Open5GS está escrito en **C** de alto rendimiento y free5GC en **Go**. Uso LLMs de baja latencia con **Groq** y **Codex** para analizar rápidamente estructuras de datos de la pila 3GPP (ej. decodificadores ASN.1 para NGAP o parsers OpenAPI para SBI).
    2. **Implementación de Requerimientos Específicos**: Escribir módulos de extensión en C/Go, como nuevos endpoints REST en NRF, formateo de CDRs en SMF, o validaciones de certificados en SEPP.
    3. **Generación de Pruebas Unitarias y Conformance 3GPP**: Crear suites de pruebas automáticas con pytest y scapy para simular paquetes SCTP/NGAP o peticiones HTTP/2 y validar que el nuevo código cumpla con los estándares 3GPP Rel-16.
    4. **Sinergia con el Equipo**: Los 2 ingenieros de core tienen el dominio de la arquitectura interna de la empresa; mi valor añadido es acelerar la entrega de código de calidad, auditar pull requests y resolver cuellos de botella en minutos en lugar de semanas."*

---

## 🏢 Fase 3: Entrevista Onsite en Richardson, TX (1 Onsite)

### 1. Dinámica de Pizarra (Whiteboarding Session)
* **Dibuja la SBA**:
  * Dibuja el bus central HTTP/2 (SBA).
  * Conecta arriba: NRF, UDM, AUSF, PCF, CHF.
  * Conecta al centro: AMF y SMF.
  * Dibuja la separación de planos: AMF hacia gNodeB por N2 (SCTP); SMF hacia UPF por N4 (PFCP UDP 8805).
  * Dibuja el plano de usuario abajo: UE -> gNodeB -> N3 (GTP-U) -> UPF -> N6 -> DN (Internet / VoNR).
  * Dibuja en la frontera: SEPP interconectando por N32-c y N32-f hacia otra PLMN.

### 2. Filtros Esenciales de Wireshark / TShark para la Prueba Práctica

```bash
# Filtrar señalización NGAP (N2) entre gNodeB y AMF
ngap

# Filtrar señalización PFCP (N4) entre SMF y UPF
pfcp

# Filtrar tráfico GTP-U (N3) de plano de usuario
gtp

# Filtrar tráfico Service-Based Architecture (HTTP/2 REST)
http2

# Filtrar llamadas a autenticación AUSF
http2.headers.path contains "/nausf-auth/"

# Filtrar establecimiento de sesión en SMF
http2.headers.path contains "/nsmf-pdusession/"

# Filtrar asociaciones SCTP
sctp

# Filtrar paquetes Diameter (en caso de interworking 4G/EPC o IMS)
diameter
```

---

## 📊 Matriz de Acrónimos 5G Core para Memorizar

| Acrónimo | Nombre Completo | Función Clave |
| :--- | :--- | :--- |
| **AMF** | Access and Mobility Management Function | Control de acceso, registro, movilidad (N1/N2). |
| **SMF** | Session Management Function | Gestión de sesiones PDU, asignación de IP, control de UPF (N4). |
| **UPF** | User Plane Function | Enrutamiento de paquetes de usuario GTP-U (N3/N6), QoS (5QI). |
| **UDM** | Unified Data Management | Gestión unificada de credenciales y perfiles de usuario. |
| **AUSF** | Authentication Server Function | Servidor de autenticación 5G-AKA / EAP-AKA'. |
| **NRF** | Network Repository Function | Descubrimiento y registro dinámico de microservicios NF. |
| **PCF** | Policy Control Function | Reglas de políticas de red y tarificación. |
| **SEPP** | Security Edge Protection Proxy | Proxy de seguridad de frontera para roaming inter-PLMN (N32). |
| **CHF** | Charging Function | Motor de tarificación y facturación convergente (Nchf / CDRs). |
| **PFCP** | Packet Forwarding Control Protocol | Protocolo sobre UDP 8805 en interfaz N4 (SMF-UPF). |
| **S-NSSAI** | Single Network Slice Selection Assistance Info | Identificador de slice (SST: Slice/Service Type + SD: Slice Differentiator). |
| **PRINS** | Packet-level Routing & Integrity Protection | Seguridad criptográfica en N32-f con estándares JOSE (JWE/JWS). |
