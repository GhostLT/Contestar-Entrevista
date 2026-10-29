# GUÍA MAESTRA DE PREPARACIÓN PARA ENTREVISTA TÉCNICA
## PUESTO: SENIOR RF OPTIMIZATION ENGINEER – ERICSSON 4G/5G
**Candidato:** Javier Viveros Huesca  
**Cliente / Proyecto:** AMDOCS MX (Operaciones de Redes Móviles en México)  
**Agencia:** Link Consulting Services  
**Tecnologías Clave:** Ericsson LTE (4G) & 5G NR (NSA / Option 3x)  
**Enfoque:** RAN Configuration, KPI Performance Forensics & RF Optimization  

---

## 📌 FICHA TÉCNICA DEL CANDIDATO Y ESTRATEGIA DE ENTREVISTA
- **Nombre:** Javier Viveros Huesca
- **Experiencia:** Más de 14 años en ingeniería de optimización de redes móviles de operadores carrier-grade (Nextel México 2011–2013, AT&T México 2013–2022).
- **Herramientas de Dominio Diario:** Ericsson ENM, Ericsson ENIQ / PM, moshell / amos, CNA / Bulk CM, TEMS / Nemo, Python, SQL, Power BI.
- **Especialidad:** Diagnóstico de causas raíz (RCA) de degradación de KPIs en tiempo récord, auditoría profunda de parámetros MOM de Ericsson, scripting y ejecución de MOPs en ventanas de mantenimiento, y optimización de redes 4G y 5G NSA (EN-DC).
- **Tarifa y Disponibilidad:** USD 3,000 / mes, disponibilidad inmediata para integración en Ciudad de México.

---

# MÓDULO 1: PRESENTACIÓN PROFESIONAL, FIT Y ESTRATEGIA INICIAL

### Pregunta 1: "Cuéntame sobre ti, tu trayectoria y tu experiencia con tecnología Ericsson 4G/5G."
*(Tell me about yourself, your background, and your experience with Ericsson 4G and 5G NR networks)*

#### 🎯 Estrategia y Tono:
Debes proyectar la seguridad de un ingeniero senior con más de una década de experiencia práctica en "trincheras" de operadores reales. Destaca que no eres un optimizador pasivo que solo mira gráficas, sino un especialista hands-on que maneja ENM, Moshell a bajo nivel, analiza trazas L3, domina el modelo de objetos (MOM) de Ericsson y automatiza procesos con Python/SQL.

#### 💬 Respuesta Modelo (Lo que debes responder):
> *"Muchas gracias. Soy Javier Viveros Huesca, Ingeniero de Optimización RF y Rendimiento RAN Senior con más de 14 años de experiencia directa en redes de operadores carrier-grade en México, habiendo trabajado extensamente en las operaciones de Nextel y AT&T México.*
> 
> *A lo largo de mi carrera me he especializado profundamente en el ecosistema Ericsson, abarcando desde las versiones de software L15 hasta las más recientes L21/L22 tanto en 4G LTE como en despliegues 5G NR en arquitectura NSA EN-DC Opción 3x.*
> 
> *Mi trabajo diario se basa en un enfoque riguroso de ingeniería de rendimiento: audito y gestiono la configuración RAN a través de Ericsson ENM, utilizo moshell/amos para análisis forense a nivel de nodo, extraigo contadores de desempeño en Ericsson ENIQ, y diseño acciones correctivas para los 5 pilares de KPIs: Accesibilidad, Retenibilidad, Movilidad, Integridad de Throughput y Disponibilidad.*
> 
> *Adicionalmente, un diferenciador clave de mi perfil es que no dependo de procesos manuales lentos: desarrollo scripts en Python y consultas SQL avanzadas para correlacionar contadores PM, identificar clusters de celdas degradadas (Worst Cells) y validar análisis Pre y Post en minutos. Vengo listo para integrarme de inmediato al equipo de Amdocs MX y aportar valor técnico desde el primer día."*

---

### Pregunta 2: "¿Por qué quieres incorporarte a este proyecto con Amdocs MX y qué valor inmediato puedes aportar?"
*(Why do you want to join this Amdocs MX project and what immediate value will you bring?)*

#### 🎯 Estrategia:
Demuestra que conoces la reputación de Amdocs como integrador global de servicios de telecomunicaciones y su rol crítico con los operadores líderes de México. Enfócate en tu capacidad de autonomía y resolución inmediata sin requerir curva de aprendizaje.

#### 💬 Respuesta Modelo:
> *"Amdocs es un referente indiscutible en la integración y gestión de servicios críticos de telecomunicaciones a nivel global y en México. Conozco perfectamente las exigencias de calidad y los estrictos Acuerdos de Nivel de Servicio (SLAs) que los operadores móviles requieren en proyectos gestionados por Amdocs.*
> 
> *Mi valor inmediato radica en tres puntos:*
> 1. **Cero curva de aprendizaje técnica:** Domino la arquitectura de Ericsson, la estructura de objetos gestionados (MOM), las herramientas ENM/ENIQ y la línea de comandos moshell, por lo que puedo asumir la gestión de clusters inmediatamente.
> 2. **Metodología probada de RCA (Análisis de Causa Raíz):** Sé diferenciar rápidamente si una degradación de KPI se debe a un problema de RF (interferencia, tilts, sobrecobertura), una mala configuración de parámetros, fallas de transporte X2/S1, o congestión de control de admisión.
> 3. **Velocidad de ejecución y automatización:** Mi experiencia programando rutinas de auditoría en Python y paneles de telemetría en Power BI acelerará las entregas de reportes técnicos y análisis pre/post para los clientes de Amdocs."*

---

### Pregunta 3: "¿Cuál es tu metodología diaria de trabajo cuando recibes un cluster degradado o una lista de Top Worst Cells?"
*(What is your day-to-day workflow when troubleshooting degraded clusters or Top Worst Cells?)*

#### 🎯 Estrategia:
El entrevistador busca comprobar si tienes un método estructurado y disciplinado, o si cambias parámetros "a ciegas". Explica tu flujo de 6 pasos.

#### 💬 Respuesta Modelo:
> *"Mi metodología es siempre estructurada y va de lo físico/infraestructura hacia lo lógico/parámetros:*
> 1. **Filtro de Alarmas y Disponibilidad (FM):** Lo primero es consultar en ENM si las celdas tienen alarmas activas de hardware (Baseband, Radio Unit), fallas ópticas SFP, desadaptación de impedancia VSWR o problemas de sincronía de reloj (GPS/PTP). Nunca se intenta optimizar por software una celda físicamente rota.
> 2. **Análisis de Congestión y Capacidad:** Verifico el uso de PRBs en DL/UL, número de usuarios RRC activos y si se alcanzaron licencias de capacidad en el nodo.
> 3. **Auditoría de Parámetros y Cambios Recientes (CM):** Reviso si hubo modificaciones recientes de software, activaciones de nuevas features o scripts de MOP ejecutados en la ventana previa que pudieran haber causado discrepancias respecto a la línea base ('Golden Parameters').
> 4. **Análisis Forense de Contadores PM (ENIQ/moshell):** Desgloso los contadores específicos de la falla. Por ejemplo, en caídas de llamada, si la causa principal es pérdida de sincronía (UeLost), problemas de Handover o fallas en la interfaz S1/X2.
> 5. **Correlación de RF y Calidad:** Reviso perfiles de interferencia (RSSI en UL), distribución de RSRP/RSRQ, histogramas de Timing Advance (TA) para detectar sobrecobertura y dominancia de celdas.
> 6. **Implementación de MOP y Validación Pre-Post:** Si es un problema de parámetros, elaboro el script de cambio para la ventana de mantenimiento y realizo el seguimiento durante las 24 a 72 horas posteriores para confirmar la recuperación del KPI frente a la línea base."*

---

# MÓDULO 2: ECOSISTEMA ERICSSON, HERRAMIENTAS OSS/ENM Y HARDWARE

### Pregunta 4: "¿Qué herramientas de Ericsson utilizas en tu día a día y cuál es tu nivel de dominio en ENM, ENIQ y Moshell?"
*(What Ericsson tools do you use daily and what is your level of expertise in ENM, ENIQ, and moshell?)*

#### 💬 Respuesta Modelo:
> *"Utilizo a diario la suite completa de gestión de Ericsson:*
> - **Ericsson ENM (Ericsson Network Manager):** Utilizo sus aplicaciones web y CLI para supervisión de alarmas (Alarm Monitor), gestión de configuración masiva (CNA, Bulk Configuration, CLI scripts con cmedit), verificación topológica y gestión de trazas (Trace Manager para CTR y UETR).
> - **Ericsson ENIQ / PM:** Es mi herramienta principal para la extracción masiva de contadores de rendimiento a nivel de celda, nodo y cluster. Con ella genero perfiles de horas pico (Busy Hour), curvas de tendencia semanal y cruces multidimensionales de KPIs.
> - **Moshell / Amos:** Tengo dominio total a nivel de terminal CLI para interactuar directamente con los nodos eNodeB y gNodeB. Lo utilizo para diagnósticos en tiempo real, consultas de parámetros (`get`), auditorías de hardware (`inv`, `lh`), comprobación de interfaces de fibra (`cabx`), pruebas de contadores en vivo (`kpiget`, `pmx`) y ejecución de scripts de MOP con rollback asegurado (`pcr`, `cvcu`)."*

---

### Pregunta 5: "¿Cuáles son los comandos esenciales de Moshell/Amos que utilizas para auditar, diagnosticar celdas y cambiar parámetros?"
*(What are the essential moshell/amos commands you use to audit, troubleshoot, and tune parameters?)*

#### 💬 Respuesta y Tabla de Referencia Rápida:
> *"En una sesión de moshell típica sobre un nodo LTE o 5G, estos son mis comandos habituales de diagnóstico y gestión:"*

| Comando Moshell | Propósito Técnico y Caso de Uso |
| :--- | :--- |
| `lt all` o `lt cmedit` | Carga el modelo de gestión (MOM) completo del nodo en la memoria de la sesión para permitir comandos de consulta y edición. |
| `get EUtranCellFDD <param>` | Consulta el valor actual de parámetros de celda LTE (ej. `get EUtranCellFDD a3offset`, `cellRange`, `qRxLevMin`). |
| `set <MO> <param> <valor>` | Modifica el valor de un parámetro en un objeto gestionado específico. |
| `bl / deb <MO>` | Bloquea administrativamente (`bl` = block) o desbloquea (`deb` = deblock) celdas, sectores o unidades de radio. |
| `inv` | Despliega el inventario completo de hardware del nodo (números de parte, número de serie de Baseband y Radios). |
| `lhsh 000100` / `lh` | Permite ejecutar diagnósticos a bajo nivel sobre placas específicas (Baseband o DUL/DUS). |
| `cabx` | Diagnostica el estado de enlaces ópticos de cable de fibra CPRI/eCPRI, niveles de potencia óptica Rx/Tx y alarmas SFP. |
| `kpiget` / `pmx -kpi` | Extrae en tiempo real los contadores de desempeño y cálculo de KPIs de la celda directamente del nodo en vivo. |
| `ue print -ad` | Muestra en tiempo real las sesiones de UE activas en la celda, con sus valores de RSRP, SINR, CQI, modulación y tráfico. |
| `cvcu` / `cvls` | Crea copias de seguridad de la configuración (Configuration Version - Backup) antes de aplicar cambios y lista los backups existentes. |
| `pcr <archivo.mos>` | Ejecuta un script de comandos moshell en modo batch para aplicar cambios masivos con registro de log. |

---

### Pregunta 6: "¿Cómo está estructurado el Modelo de Objetos Gestionados (MOM) de Ericsson para 4G y 5G NR?"
*(How is the Ericsson Managed Object Model (MOM) structured for 4G LTE and 5G NR?)*

#### 💬 Respuesta Modelo:
> *"La arquitectura MOM de Ericsson es una jerarquía de clases de objetos gestionados (Managed Objects - MOs) donde cada nivel representa una función lógica o física:*
> - **En 4G LTE:**
>   - `ManagedElement`: El nodo raíz del eNodeB.
>   - `ENodeBFunction`: La función lógica del eNodeB y sus parámetros globales de red.
>   - `EUtranCellFDD` / `EUtranCellTDD`: Representa la celda de radio LTE individual (contiene ancho de banda, frecuencias `earfcn`, potencia `partOfSectorPower`, `cellRange`, parámetros de control de acceso `qRxLevMin`).
>   - `EUtranCellRelation`: Representa la relación de vecindad hacia otra celda LTE (contiene `cellIndividualOffset`, `qOffsetCell`, estado de movilidad `isHoAllowed`).
>   - `UtranCellRelation` / `GeranCellRelation`: Relaciones de vecindad hacia tecnologías 3G / 2G para IRAT.
>   - `EUtranFreqRelation`: Define las reglas de búsqueda entre portadoras inter-frecuencia (`cellReselectionPriority`, `threshXHigh`, `threshXLow`).
> - **En 5G NR (Arquitectura CU/DU Desagregada):**
>   - `GNBDUFunction`: Función de la Unidad Distribuida (DU), encargada de las capas RLC, MAC y PHY.
>   - `NRCellDU`: La celda física 5G gestionada por la DU (parámetros de RF, ancho de banda, SSB, PRACH).
>   - `GNBCUCPFunction`: Función del Plano de Control de la Unidad Central (CU-CP), encargada de la capa RRC y control de PDCP.
>   - `NRCellCU`: Representa la celda a nivel de plano de control en la CU.
>   - `TermPointToEnb` / `TermPointToGnb`: Puntos de terminación de enlaces de señalización e interfaces X2 (LTE-NR para NSA) o Xn (NR-NR para SA)."*

---

### Pregunta 7: "¿Qué experiencia tienes con el hardware de Ericsson (Baseband 5216/6630/6648, Radios 4415/2219, AIR 6449/3268) y cómo diagnosticas fallas físicas o de transporte?"
*(What is your experience with Ericsson hardware and how do you diagnose physical or transport faults?)*

#### 💬 Respuesta Modelo:
> *"He trabajado ampliamente con la evolución de hardware de Ericsson:*
> - **Basebands:** Desde las generaciones anteriores DUL/DUS hasta las modernas Baseband 5216, Baseband 6630 y 6648 para 5G de alta capacidad. Sé verificar la carga de procesamiento de CPU en placas mediante `lhsh`, el balance de tráfico entre tarjetas y la disponibilidad de slots.
> - **Radios:** Modelos estándar como Radio 4415 (4T4R multi-banda), Radio 2219 (2T2R) y antenas integradas Massive MIMO como AIR 6449 y AIR 3268 (64T64R y 32T32R para banda n78 / 3.5 GHz).
> - **Diagnóstico de Enlaces Ópticos y VSWR:** 
>   - Con el comando `cabx` en moshell verifico si hay degradación de señal óptica (potencia Rx en SFP por debajo de -15 dBm indica fibra doblada, sucia o transceptor defectuoso).
>   - Si una celda tiene alarmas de VSWR o Return Loss bajo (< 15 dB), coordino cuadrilla para inspeccionar jumpers, conectores dañados por agua o problemas de antena, ya que el VSWR elevado genera potencia reflejada, intermodulación pasiva (PIM) y destrucción de la cobertura en enlace ascendente."*

---

# MÓDULO 3: INMERSIÓN TÉCNICA EN LOS 5 PILARES DE KPIS DE RENDIMIENTO

### Pregunta 8: "PILAR 1 - ACCESIBILIDAD: ¿Cuáles son las fórmulas, contadores de falla y metodología de resolución para caídas de RRC, E-RAB y adición 5G?"
*(PILLAR 1 - ACCESSIBILITY: Formulas, failure counters, and troubleshooting workflow for RRC, E-RAB, and 5G NSA additions)*

#### 💬 Fórmulas y Contadores Clave:
> **1. RRC Connection Setup Success Rate (RRC Setup SR):**
> $$	ext{RRC Setup SR} = rac{	ext{pmRrcConnEstabSucc}}{	ext{pmRrcConnEstabAtt}} 	imes 100\%$$
> *(Desglosado en intentos por Servicio y por Señalización / MoData vs MoSignaling).*
> 
> **2. E-RAB Setup Success Rate (E-RAB Setup SR):**
> $$	ext{E-RAB Setup SR} = rac{	ext{pmErabEstabSuccInit} + 	ext{pmErabEstabSuccAdded}}{	ext{pmErabEstabAttInit} + 	ext{pmErabEstabAttAdded}} 	imes 100\%$$
> *(Monitoreado críticamente por QCI: QCI 1 para voz VoLTE y QCI 9 para datos de usuario).*
> 
> **3. Call Setup Success Rate (CSSR):**
> $$	ext{CSSR} = 	ext{RRC Setup SR} 	imes 	ext{E-RAB Setup SR}$$
> 
> **4. 5G NSA SgNB Addition Success Rate:**
> $$	ext{SgNB Addition SR} = rac{	ext{pmEndcSetupSucc}}{	ext{pmEndcSetupAtt}} 	imes 100\%$$

#### 🔍 Diagnóstico de Causa Raíz de Accesibilidad:
> *"Cuando la Accesibilidad se degrada, sigo un diagrama de decisión claro:*
> 1. **Si falla el RRC:**
>    - **Interferencia en UL (Uplink RSSI / RTWP):** Si el RSSI promedio sube de -115 dBm a valores peores que -95 dBm, los preámbulos de PRACH son bloqueados por el piso de ruido. Causa: PIM o interferencia externa.
>    - **Congestión de PRACH / PUCCH:** Se evalúa si los preámbulos colisionan por exceso de usuarios o si los recursos de PUCCH configurados (`pucchDedicated`) están saturados.
>    - **Control de Admisión (Admission Control):** El nodo rechaza la conexión si se alcanzó el límite de usuarios concurrentes de la licencia del Baseband o saturación total de PRBs.
> 2. **Si falla el E-RAB:**
>    - Generalmente indica fallas en el transporte S1 hacia el MME/S-GW (pérdida de paquetes SCTP o retardos elevados de red de transporte) o rechazo del Core Network por falta de recursos de QoS o autenticación.
> 3. **Si falla la Adición de SgNB (5G NSA):**
>    - Se evalúa la interfaz X2 entre el eNodeB y el gNodeB: si hay pérdida de paquetes X2-C o retardos, el mensaje `SgNB Addition Request` expira antes de que el gNB responda."*

#### 🛠️ Parámetros Clave de Accesibilidad:
- `prachConfigurationIndex`: Controla la periodicidad y formato de los preámbulos RACH.
- `rootSequenceIndex`: Secuencia raíz de PRACH (debe auditarse para evitar colisiones entre vecinos).
- `pZeroNominalPucch` y `pZeroNominalPusch`: Nivel nominal de potencia en enlace ascendente para superar el piso de ruido.
- `cellRange`: Distancia máxima de acceso permitida; si un UE intenta conectarse fuera de rango, el PRACH es descartado.

---

### Pregunta 9: "PILAR 2 - RETENIBILIDAD: ¿Cómo analizas el Drop Rate (E-RAB Drop) en VoLTE (QCI 1) y Datos (QCI 9), y cómo diferencias caídas por RF vs Transporte?"
*(PILLAR 2 - RETAINABILITY: How do you troubleshoot E-RAB Drop Rate for VoLTE and Data, and differentiate RF drops from Transport drops?)*

#### 💬 Fórmulas y Contadores Clave:
> $$	ext{E-RAB Drop Rate} = rac{	ext{pmErabRelAbnormalEnb} + 	ext{pmErabRelAbnormalMme}}{	ext{pmErabRelNormalEnb} + 	ext{pmErabRelAbnormalEnb} + 	ext{pmErabRelAbnormalMme}} 	imes 100\%$$
> 
> En VoLTE (QCI 1):
> $$	ext{VoLTE Drop Rate} = rac{	ext{pmErabRelAbnormalEnbActQci1}}{	ext{pmErabRelNormalEnbQci1} + 	ext{pmErabRelAbnormalEnbActQci1}} 	imes 100\%$$

#### 🔍 Diagnóstico Forense de Caídas:
> *"Para aislar la causa raíz de las caídas, analizo los subcontadores específicos de liberación anormal en Ericsson:*
> - **Caídas por Enlace de Radio (RF Losses - `UeLost`):**
>   - Contador: `pmErabRelAbnormalEnbActUeLost`.
>   - Causa: Expiración del temporizador **T310** (el UE detecta N310 indicaciones consecutivas 'out-of-sync' y no logra recuperar sincronía). Típicamente ocurre por cobertura débil en borde de celda, cañones urbanos, zonas de desvanecimiento rápido (fast fading) o contaminación de pilotos (SINR < -5 dB con múltiples señales compitiendo con RSRP idéntico).
> - **Caídas por Falla de Handover (Handover Execution Drop):**
>   - Contador: `pmErabRelAbnormalEnbActHo`.
>   - Causa: El comando de handover se envió muy tarde cuando la señal de la celda servidora ya se había degradado completamente (Late Handover), o el UE intentó conectarse a una celda objetivo sin tener línea de vista o con parámetros de acceso incorrectos (expiración de **T304**).
> - **Caídas por Transporte / MME (`TransportLost` / `CoreRelease`):**
>   - Ocurren liberaciones masivas con causa `pmErabRelAbnormalEnbActTransportLost`. Si el enlace de transporte S1 o IPsec experimenta una micro-interrupción o pérdida de paquetes SCTP, el eNodeB libera inmediatamente todos los portadores E-RAB activos de forma simultánea. Se corrobora porque afecta a todas las celdas del sitio a la misma hora exacta."*

#### 🛠️ Acciones de Optimización de Retenibilidad:
1. **Ajuste de Antenas (RET):** Incrementar el tilt eléctrico en celdas sobrecobertoras para confinar la huella de RF y eliminar la contaminación de pilotos.
2. **Auditoría de Vecindades (ANR / Neighbor Relations):** Asegurar que las celdas adyacentes existan en `EUtranCellRelation`; una vecindad faltante en zona de solapamiento causa caída segura al 100%.
3. **Calibración de Timers de Radio Link Failure (RLF):** Ajustar `t310` (ej. de 1000ms a 2000ms en entornos de sombra rápida) y `n310`/`n311` para dar mayor resiliencia al enlace.

---

### Pregunta 10: "PILAR 3 - MOVILIDAD: Explica los eventos 3GPP de Handover (A1 a A5, B1, B2) y cómo resuelves problemas de Handover Tardío y Ping-Pong."
*(PILLAR 3 - MOBILITY: Explain 3GPP Handover events and how you resolve Late Handover and Ping-Pong issues)*

#### 💬 Tabla de Eventos de Movilidad en Ericsson LTE / 5G:

| Evento | Condición de Activación 3GPP | Aplicación Típica en Ericsson RAN |
| :---: | :--- | :--- |
| **A1** | La celda servidora se vuelve mejor que un umbral absoluto (`a1Threshold`). | Detiene las mediciones inter-frecuencia/IRAT para ahorrar batería del UE cuando la cobertura es excelente. |
| **A2** | La celda servidora se vuelve peor que un umbral absoluto (`a2Threshold`). | Dispara las mediciones periódicas o por evento hacia otras frecuencias (inter-frecuencia) o tecnologías (IRAT). |
| **A3** | Una celda vecina se vuelve un offset mejor que la servidora: $RSRP_{vecina} > RSRP_{servidora} + a3offset$. | Es el evento primordial para **Handover Intra-frecuencia** y Handover entre portadoras de la misma banda. |
| **A4** | Una celda vecina se vuelve mejor que un umbral absoluto. | Usado para descubrir mejores portadoras o para agregación de portadoras (Carrier Aggregation SCell addition). |
| **A5** | Servidora peor que Umbral 1 **Y** Vecina mejor que Umbral 2. | Evento fundamental para **Handover Inter-frecuencia por cobertura** hacia bandas de menor frecuencia (ej. de B4/B2 a B28/700MHz). |
| **B1** | Una celda vecina Inter-RAT se vuelve mejor que un umbral absoluto. | **Crítico para 5G NSA:** Utilizado para detectar la presencia de señal 5G NR y disparar la adición de SgNB. |
| **B2** | Servidora LTE peor que Umbral 1 **Y** Vecina Inter-RAT mejor que Umbral 2. | Dispara la redirección o handover hacia redes 3G (WCDMA) cuando LTE pierde cobertura totalmente. |

#### 🔍 Resolución de Problemas de Movilidad:
> - **Problema de Handover Tardío (Late Handover - UE cae antes de ejecutar el HO):**
>   - **Diagnóstico:** Trazas muestran que el UE reporta RSRP de la servidora en picada (-120 dBm) y alta interferencia sin haber recibido el mensaje `RRCConnectionReconfiguration (MobilityControlInfo)`.
>   - **Solución:** Reducir el temporizador `timeToTrigger` (TTT) de 320ms a 160ms o 100ms, y disminuir `a3offset` (ej. de 3 dB a 2 dB o 1 dB) para que la orden de handover se emita más rápido antes de que el UE pierda el enlace.
> - **Problema de Ping-Pong Handover (UE oscila continuamente entre dos celdas):**
>   - **Diagnóstico:** Alto volumen de intentos de handover con tiempo de residencia menor a 3 segundos entre las celdas A y B.
>   - **Solución:** Aumentar el margen de histéresis `hysteresisA3` (ej. de 1 dB a 2 dB o 3 dB) y/o elevar el `timeToTrigger`. Si una celda es dominante y la otra es de desborde, se configura un `cellIndividualOffset` (CIO) positivo hacia la celda preferida.

---

### Pregunta 11: "PILAR 4 - INTEGRIDAD Y THROUGHPUT: ¿Cuáles son los factores que degradan el Throughput de usuario DL/UL y cómo realizas su optimización?"
*(PILLAR 4 - INTEGRITY & THROUGHPUT: Factors degrading DL/UL User Throughput and optimization strategies)*

#### 💬 Métricas, Diagnóstico y Optimización:
> *"El Throughput a nivel de usuario depende de la combinación de ancho de banda, calidad de canal, eficiencia espectral y disponibilidad de recursos:*
> 
> $$	ext{Throughput} pprox 	ext{Ancho de Banda (PRBs)} 	imes 	ext{Eficiencia Espectral (MCS / Modulación)} 	imes (1 - 	ext{BLER}) 	imes 	ext{Capas MIMO}$$
> 
> **Causas Raíz de Degradación:**
> 1. **Baja Calidad de Radio (Bajo SINR / Alto BLER):**
>    - Si el SINR cae por debajo de 0 dB, el algoritmo de adaptación de enlace degrada la modulación de 256QAM o 64QAM a 16QAM o QPSK, y el esquema de codificación (MCS) se reduce al mínimo.
>    - Se monitorea el **BLER (Block Error Rate)**; el objetivo del bucle cerrado es 10% en primera transmisión. Si el BLER residual excede el 2%, se están perdiendo paquetes en radio, forzando retransmisiones HARQ.
> 2. **Saturación de Capacidad (Alto PRB Utilization):**
>    - Cuando la utilización de PRBs en DL supera el 80% en horas pico, los recursos de tiempo y frecuencia se comparten entre decenas de UEs activos, reduciendo el throughput individual a < 2–5 Mbps.
> 3. **Rango MIMO Pobre (Bajo Rank Indicator - RI):**
>    - Si no hay descorrelación espacial suficiente o hay falta de scattering en el canal, el sistema cae de Rank 2 o Rank 4 a Rank 1 (SISO o diversidad simple), reduciendo la tasa teórica a la mitad o a una cuarta parte.
> 4. **Limitación de Transporte / Backhaul:**
>    - Si la interfaz IP de transporte tiene un cuello de botella en ancho de banda o problemas de fragmentación de paquetes (MTU mismatch), el throughput se estanca independientemente de la excelente calidad de RF.
> 
> **Acciones de Optimización:**
> - Activar y sintonizar **Carrier Aggregation (CA)** para sumar portadoras (ej. AWS + PCS + 700MHz).
> - Implementar **Mobility Load Balancing (MLB)** para descargar usuarios de la portadora congestionada hacia capas con bajo uso de PRBs.
> - Controlar la interferencia co-canal ajustando tilts mecánicos/eléctricos para maximizar la distribución de CQI hacia valores de 10 a 15."*

---

### Pregunta 12: "PILAR 5 - DISPONIBILIDAD Y CELDAS DURMIENTES: ¿Cómo mides la Disponibilidad de Red y cuál es tu método para detectar 'Sleeping Cells'?"
*(PILLAR 5 - AVAILABILITY & SLEEPING CELLS: How do you track Availability and detect 'Sleeping Cells'?)*

#### 💬 Respuesta Modelo:
> *"La Disponibilidad de Radio se mide mediante la fórmula:*
> 
> $$	ext{Cell Availability} = \left( 1 - rac{	ext{Tiempo Fuera de Servicio Involuntario}}{	ext{Tiempo Total de Operación}} 
ight) 	imes 100\%$$
> 
> - **Causas Típicas de Indisponibilidad:**
>   - Caídas de transporte IP/SFP (`cabx` alarmas de enlace óptico).
>   - Pérdida de referencia de sincronía (GPS loss of sync, pérdida de paquetes IEEE 1588v2 PTP), lo cual es crítico en TDD donde la pérdida de reloj provoca bloqueo automático de la celda para evitar interferencia de ranura.
>   - Fallas de hardware en unidades de radio (RRU bloqueada, alarmas de sintetizador de frecuencia).
> 
> - **Detección Forense de 'Sleeping Cells' (Celdas Durmientes):**
>   - **Definición:** Una celda durmiente es una celda que en el sistema de alarmas (FM) aparece en color verde (administrativa y operacionalmente desbloqueada, sin alarmas activas), pero en la realidad no está cursando tráfico ni aceptando usuarios.
>   - **Método de Detección con Python / ENIQ:**
>     - Filtro diario en contadores PM buscando celdas con:
>       1. Cero intentos de establecimiento RRC (`pmRrcConnEstabAtt = 0`) durante horas hábiles en zonas con tráfico histórico normal.
>       2. Tasa de caída de RRC del 100% inmediata tras el acceso.
>       3. Cero volumen de datos cursados en DL/UL (`pmPdcpVolDlDrb = 0`).
>     - **Acción Correctiva:** Conexión por moshell, bloqueo administrativo (`bl`), reinicio suave o reinicio de la unidad de radio (`lhsh`), verificación de potencia de transmisión de RF y, si persiste, re-inicialización del módulo de software o reemplazo del hardware."*

---

# MÓDULO 4: ESPECIALIZACIÓN EN 5G NR NSA / EN-DC (OPCIÓN 3X)

### Pregunta 13: "¿Cómo funciona la arquitectura 5G NSA Opción 3x y cuál es la función de la celda ancla LTE vs la celda secundaria 5G NR?"
*(How does 5G NSA Option 3x architecture work and what is the role of LTE anchor vs 5G NR secondary cell?)*

#### 💬 Respuesta Modelo:
> *"La arquitectura 5G NSA (Non-Standalone) Opción 3x es el estándar adoptado por los principales operadores para desplegar 5G sobre la infraestructura existente del núcleo 4G (EPC):*
> 
> - **Plano de Control (C-Plane):** Reside 100% en el **Master eNodeB (MeNB)** de LTE. El eNodeB mantiene la conexión de señalización S1-MME con el núcleo de red y controla la máquina de estados RRC del terminal (UE).
> - **Plano de Usuario (U-Plane - Split Bearer):** En la Opción 3x, la interfaz de datos S1-U termina directamente en el **Secondary gNodeB (SgNB)** de 5G NR.
> - **Mecanismo de Descarga (Data Offload):** El gNodeB recibe el tráfico del S-GW/UPF a nivel de capa PDCP (NR-PDCP). Si las condiciones de radio 5G son óptimas, los paquetes de datos de alta velocidad se transmiten directamente al UE a través de los portadores de radio 5G (NR RLC/MAC/PHY). Si el UE entra en una zona de cobertura 5G marginal, el tráfico de datos puede dividirse (split) o conmutarse hacia el eNodeB LTE a través de la interfaz X2-U para garantizar continuidad sin caídas de sesión."*

---

### Pregunta 14: "Explica paso a paso el flujo de señalización de extremo a extremo para la adición de una celda secundaria 5G (SgNB Addition)."
*(Explain step-by-step the end-to-end signaling flow of SgNB Addition in 5G NSA)*

#### 💬 Flujo de Señalización Paso a Paso:
> *"El proceso de SgNB Addition sigue una secuencia estricta de 10 pasos en 3GPP / Ericsson:*
> 
> 1. **Establecimiento de Conexión en Portadora Ancla (LTE):** El UE se conecta a la celda ancla LTE mediante el procedimiento estándar de RRC Connection Setup y autenticación en el EPC.
> 2. **Configuración de Mediciones B1 (Measurement Configuration):** El MeNB LTE evalúa las capacidades del UE (`EndcAllowed`). Si el UE soporta EN-DC en la banda 5G del operador (ej. n78), el MeNB le envía un `RRCConnectionReconfiguration` configurando el **Evento B1** para la frecuencia NR objetivo, con los umbrales `b1ThresholdRsrp` y `timeToTriggerB1`.
> 3. **Reporte de Medición del UE (B1 Measurement Report):** El UE detecta la señal de sincronización 5G (SSB) con una potencia RSRP superior al umbral configurado de forma continua durante el `timeToTrigger` y transmite un mensaje `MeasurementReport (Event B1)` al eNodeB.
> 4. **Solicitud de Adición de Nodo Secundario (SgNB Addition Request):** El MeNB envía a través de la interfaz X2-C el mensaje `SgNB Addition Request` al gNodeB 5G correspondiente, incluyendo las capacidades del UE y la lista de celdas NR candidatas.
> 5. **Control de Admisión y Reserva de Recursos en 5G:** El gNodeB evalúa la disponibilidad de recursos de radio, capacidad de procesamiento de la tarjeta Baseband 5G y licencias concurrentes.
> 6. **Confirmación con Contenedor RRC (SgNB Addition Request Acknowledge):** El gNodeB responde afirmativamente al MeNB mediante `SgNB Addition Request Acknowledge`, incluyendo un contenedor transparente con la configuración RRC de NR para la Celda Primaria Secundaria (**PSCell**).
> 7. **Reconfiguración RRC hacia el UE:** El MeNB transmite al UE el mensaje `RRCConnectionReconfiguration` conteniendo la configuración de la celda 5G (frecuencia, ancho de banda, configuración PRACH de NR y configuración de capas de radio).
> 8. **Acceso Aleatorio en 5G (PRACH on NR):** El UE realiza el procedimiento de Random Access (PRACH) sobre la PSCell de 5G NR para sincronizarse en tiempo (Timing Advance) en enlace ascendente.
> 9. **Confirmación de Reconfiguración (RRC Reconfiguration Complete):** El UE transmite `RRCConnectionReconfigurationComplete` al MeNB LTE.
> 10. **Finalización y Conmutación de Ruta (Path Switch):** El MeNB notifica al gNB mediante `SgNB Reconfiguration Complete` a través de X2, y el gNodeB notifica al Core Network (MME/S-GW) para conmutar la ruta de datos del plano de usuario directamente hacia el gNB."*

---

### Pregunta 15: "¿Cuáles son las causas más comunes de falla en la adición o retención de 5G NSA (SgNB Addition / Drop) y cómo las solucionas?"
*(What are the most common root causes of 5G NSA SgNB Addition failures and Drops, and how do you resolve them?)*

#### 💬 Diagnóstico y Soluciones de Falla en 5G NSA:

| Escenario de Falla | Causa Raíz Típica en Redes Ericsson | Solución y Optimización de Ingeniería |
| :--- | :--- | :--- |
| **Falla en SgNB Addition (Baja Tasa de Éxito)** | **Problemas de Transporte X2:** Pérdida de paquetes SCTP o retardos excesivos en la interfaz X2-C entre el eNodeB y el gNodeB, provocando expiración de temporizadores. | Auditar calidad del enlace IP de backhaul, latencia y MTU entre nodos. Verificar disponibilidad del objeto `TermPointToGnb`. |
| **Falla en SgNB Addition (Rechazo del gNB)** | **Agotamiento de Licencias o Admisión:** El gNodeB rechaza la adición por haber alcanzado el límite de licencias de usuarios EN-DC concurrentes o saturación de PRBs en la celda NR. | Monitorear contadores de rechazo por admisión en gNodeB. Expandir licencias de software o balancear tráfico hacia otras capas. |
| **Falla en SgNB Addition (Falla de RACH NR)** | **Desbalance de Enlace UL en 3.5 GHz:** El UE detecta el SSB en DL con buen RSRP, pero su potencia de transmisión en enlace ascendente (limitada a 23 dBm) no es suficiente para alcanzar la antena del gNodeB durante el PRACH. | Calibrar el umbral `b1ThresholdRsrp` haciéndolo más conservador (ej. de -108 dBm a -102 dBm) para que solo UEs con cobertura sólida intenten conectarse; optimizar preámbulos PRACH y tilt de antena. |
| **Alta Tasa de SgNB Drop (Liberaciones Anormales)** | **Desbalance de Huella RF LTE vs NR:** La señal ancla LTE (en bandas bajas o medias como 850 MHz o AWS) tiene mucha mayor penetración que la señal de 3.5 GHz. Al desplazarse el usuario, la señal 5G se desploma súbitamente, causando expiración del temporizador T310 en NR (**SCG Failure**). | Ajustar parámetros de liberación preventiva de SCG mediante eventos A2 de NR antes de que se produzca una pérdida abrupta de radio; optimizar el azimut y tilt digital de los haces de Massive MIMO. |

---

### Pregunta 16: "¿Cómo optimizas los parámetros de movilidad en NSA (PSCell change, B1 threshold, SCG failure handling)?"
*(How do you tune NSA mobility parameters: PSCell change, B1 thresholds, and SCG failure handling?)*

#### 💬 Respuesta Modelo:
> *"La optimización de movilidad en NSA se enfoca en tres áreas estratégicas:*
> 1. **Calibración del Umbral B1 (`b1ThresholdRsrp` y `timeToTriggerB1`):**
>    - Si el umbral B1 es demasiado permisivo (ej. -112 dBm), muchos UEs intentarán agregar la portadora 5G en zonas de borde donde no hay estabilidad de enlace ascendente, elevando los fallos de RACH y las caídas inmediatas de SgNB.
>    - Sintonizo `b1ThresholdRsrp` entre -104 dBm y -100 dBm en bandas medias (n78) para asegurar que la celda 5G solo se agregue cuando pueda entregar un throughput significativamente superior al de 4G.
> 2. **Cambio de Celda Secundaria (PSCell Change Optimization):**
>    - Para movilidad entre celdas 5G mientras se mantiene la misma celda ancla LTE (Intra-MeNB PSCell Change), se optimiza el evento **A3 de NR** configurado en el gNodeB (`a3offset` de 2 a 3 dB y `timeToTrigger` de 160ms) para que el traspaso entre sectores 5G sea rápido y transparente.
> 3. **Gestión de Fallas de SCG (SCG Failure Handling):**
>    - Configuro la red para que ante una falla de radio en 5G (`synchReconfigFailureSCG` o `t310-Expiry`), el UE no corte la llamada o sesión de datos completa, sino que envíe un mensaje `SCGFailureInformation` al eNodeB LTE para liberar limpiamente la pata 5G y mantener el tráfico cursando a través de LTE sin interrupción percibida por el usuario."*

---

# MÓDULO 5: FUNCIONALIDADES AVANZADAS DE RAN ERICSSON

### Pregunta 17: "CARRIER AGGREGATION (CA): ¿Cómo funciona la agregación de portadoras, cuáles son los eventos clave y cómo optimizas la adición y retención de SCells?"
*(CARRIER AGGREGATION: How does CA work, what are the key events, and how do you optimize SCell addition/retention?)*

#### 💬 Respuesta Modelo:
> *"Carrier Aggregation permite combinar dos o más portadoras de radio (Component Carriers) para multiplicar el ancho de banda efectivo y la tasa de transferencia del usuario:*
> 
> - **PCell (Primary Cell):** Es la celda que maneja la señalización RRC, la conexión NAS, la transmisión de PUCCH y la movilidad de cobertura.
> - **SCell (Secondary Cell):** Portadoras adicionales agregadas exclusivamente para incrementar la capacidad del plano de usuario en enlace descendente y/o ascendente.
> 
> **Mecanismos y Eventos de Activación:**
> 1. **Lista de Candidatas (`sCellCandidateList`):** Se configuran las celdas y frecuencias permitidas para agregación en el objeto `EUtranCellFDD`.
> 2. **Eventos A4 y A6:**
>    - **Evento A4:** Utilizado para evaluar la calidad absoluta de portadoras secundarias en frecuencias inter-banda (ej. PCell en B4 y SCell en B2 o B7).
>    - **Evento A6:** Utilizado para eventos intra-banda donde una celda vecina en la misma frecuencia que la SCell se vuelve un offset mejor que la SCell actual.
> 3. **Umbrales de Activación por Buffer (Data Volume Threshold):** Para no saturar los recursos de señalización ni agotar la batería del UE, la SCell no se activa inmediatamente para tráfico liviano; se activa cuando el buffer de datos en RLC/PDCP supera un umbral configurable (ej. `sCellActDeactDataThreshold`).
> 
> **Optimización de Desempeño:**
> - Audito que las relaciones de CA sean bidireccionales y recíprocas entre todas las capas de frecuencia co-ubicadas.
> - Ajusto los umbrales de cobertura mínima de SCell para evitar activar celdas secundarias con SINR negativo que degraden la eficiencia de modulación."*

---

### Pregunta 18: "MASSIVE MIMO Y BEAMFORMING: Explica la diferencia entre haces SSB y haces CSI-RS, y cómo se optimiza la cobertura en antenas AIR de Ericsson."
*(MASSIVE MIMO & BEAMFORMING: Difference between SSB broadcast beams and CSI-RS traffic beams, and AIR antenna optimization)*

#### 💬 Respuesta Modelo:
> *"En los sistemas Massive MIMO 5G (como las antenas Ericsson AIR 6449 y AIR 3268 de 64T64R y 32T32R en banda n78):*
> 
> 1. **Haces de Difusión (SSB Beams - Synchronization Signal Block):**
>    - Son haces estáticos o semi-estáticos que transmiten las señales de sincronización (PSS/SSS) y la información del sistema (PBCH / MIB).
>    - En bandas medias (3.5 GHz), se configuran típicamente **4 u 8 haces SSB** que barren secuencialmente el sector en el plano horizontal (azimut) y vertical (elevación) para garantizar que cualquier terminal en el sector pueda sincronizarse y leer la red.
> 2. **Haces Dedicados de Usuario (CSI-RS Traffic Beams):**
>    - Son haces dinámicos y ultra-estrechos generados mediante formación digital de haz (digital beamforming).
>    - Utilizan las matrices de precodificación y la reciprocidad del canal (Sounding Reference Signals - SRS) para concentrar la energía de radiofrecuencia directamente en la posición espacial exacta del UE activo, logrando alta ganancia de potencia y multiplexación espacial multi-usuario (MU-MIMO).
> 
> **Optimización en Ericsson ENM / Moshell:**
> - En antenas AIR no se requiere mover mecánicamente la antena para optimizaciones finas: se ajusta el parámetro **`digitalTilt`** (tilt digital) y **`digitalAzimuth`** directamente desde el software en el objeto del modelo de antena.
> - Se seleccionan perfiles de haz (`beamformingProfile`) según la morfología del terreno: perfiles con haz vertical ancho para zonas urbanas con edificios altos (high-rise scenarios) o perfiles planos y estrechos para autopistas y cobertura macro rural."*

---

### Pregunta 19: "MOBILITY LOAD BALANCING (MLB): ¿Cómo se configuran los umbrales de balanceo de carga para descongestionar capas saturadas?"
*(MOBILITY LOAD BALANCING: Tuning load balancing thresholds to relieve congested carriers)*

#### 💬 Respuesta Modelo:
> *"El Mobility Load Balancing (MLB) redistribuye el tráfico entre portadoras de diferentes frecuencias basándose en la carga real de recursos de radio:*
> 
> - **Criterios de Carga:** Se evalúa la utilización promedio de PRBs en DL/UL y el número de UEs conectados en estado RRC.
> - **Parámetros Clave en Ericsson:**
>   - `lbThreshold`: Porcentaje de utilización de PRBs a partir del cual una celda se considera sobrecargada (ej. 75% o 80%).
>   - `lbActivationThreshold`: Umbral para activar el proceso de desborde de tráfico.
>   - `cellCapacityOffset`: Permite 'engañar' virtualmente la condición de handover de reselección o conexión, aplicando un offset que hace que las celdas objetivo con menor carga parezcan artificialmente más atractivas para los UEs.
> - **Mecanismos de Transferencia:** Se transfieren UEs en estado conectado mediante handover inter-frecuencia dirigido por carga, o se modifican los parámetros de reselección en SIB24/SIB5 (`threshXHigh`, `cellReselectionPriority`) para que los terminales en reposo (idle) acampen preferentemente en la capa con mayor capacidad."*

---

### Pregunta 20: "DYNAMIC SPECTRUM SHARING (DSS): ¿Cómo funciona la compartición dinámica de espectro 4G/5G en una misma portadora y qué impacto tiene en los KPIs?"
*(DYNAMIC SPECTRUM SHARING: How does DSS share spectrum between 4G and 5G on the same carrier and what is its KPI impact?)*

#### 💬 Respuesta Modelo:
> *"DSS (Dynamic Spectrum Sharing) permite transmitir 4G LTE y 5G NR simultáneamente sobre el mismo bloque de frecuencia (ej. 20 MHz en AWS B4/n66 o 10 MHz en 700 MHz B28/n28):*
> 
> - **Principio de Operación:** En lugar de reservar espectro estático para 5G, el programador (scheduler) de la Baseband de Ericsson asigna recursos en el dominio del tiempo y de la frecuencia a nivel de sub-milisegundo según la demanda instantánea de usuarios 4G vs 5G.
> - **Técnicas de Convivencia:**
>   - **MBSFN Subframes:** Se configuran subframes de multidifusión de LTE donde LTE no transmite señales de control, dejando la ranura completamente libre para la transmisión de 5G NR.
>   - **Rate Matching sobre LTE CRS:** 5G NR adapta sus elementos de recursos para 'esquivar' las señales de referencia comunes (CRS) de LTE que se transmiten continuamente a lo largo de toda la banda.
> - **Compensaciones y Penalización de Desempeño:**
>   - **Ventaja:** Despliegue inmediato de cobertura 5G a nivel nacional sin necesidad de comprar espectro nuevo ni apagar capas LTE existentes.
>   - **Desventaja / Impacto en KPIs:** La necesidad de insertar señales de sincronización de 5G y realizar rate-matching genera un **overhead de señalización del 10% al 20% en la capacidad de LTE**. En horas de alta carga LTE, los usuarios 4G experimentan una reducción en su throughput máximo.
>   - **Optimización:** Calibrar los parámetros de prioridad del scheduler para no penalizar a los usuarios LTE en horas pico y asegurar que los terminales 5G sean transferidos a bandas dedicadas (como n78 a 3.5 GHz) tan pronto como tengan cobertura."*

---

# MÓDULO 6: CASOS PRÁCTICOS DE RESOLUCIÓN DE PROBLEMAS (ROOT CAUSE ANALYSIS - RCA)

### Pregunta 21: "CASO REAL 1: Tras una actualización masiva de software de Ericsson (ej. de L19 a L21), los Call Drops de VoLTE se disparan un 35% en un cluster urbano. ¿Cuál es tu plan de acción inmediato?"
*(REAL SCENARIO 1: Following an Ericsson software upgrade, VoLTE call drops spike by 35% across an urban cluster. What is your immediate action plan?)*

#### 💬 Respuesta Metodológica de Nivel Senior:
> *"Ante una degradación súbita tras una ventana de mantenimiento de software, actúo de forma inmediata y sistemática:*
> 
> 1. **Contención y Evaluación de Alcance:**
>    - Verifico si la degradación ocurre exclusivamente en los nodos actualizados a la nueva release o si afecta a nodos con versión anterior (para descartar problemas globales del IMS/Core de voz).
> 2. **Extracción y Desglose de Contadores Forenses:**
>    - Extraigo de inmediato los contadores detallados de liberación de QCI 1 en ENIQ y moshell:
>      - `pmErabRelAbnormalEnbActQci1` desglosado por causa: `UeLost` (RF loss), `Ho` (handover execution), `Transport` o `Core`.
> 3. **Auditoría de Parámetros Nuevos y Valores por Defecto:**
>    - En las actualizaciones de software de Ericsson, frecuentemente se introducen nuevos parámetros o cambian los valores predeterminados (default values) de control de robustez de encabezados (RoHC - Robust Header Compression), temporizadores de RLC en modo no reconocido (UM) para VoLTE, o parámetros de Smart Inactivity Timer.
>    - Comparo mediante un script de auditoría la base de datos de configuración de un nodo degradado con la versión previa.
> 4. **Análisis de Trazas de Capa 3 (CTR / UETR):**
>    - Activo trazas de usuario (UETR) en 5 celdas con el mayor volumen de caídas. Reviso los mensajes previos a la caída: si el UE envía `RRCConnectionReconfigurationComplete` o si se produce un descarte de paquetes en la capa PDCP por expiración de temporizador de descarte (`discardTimer`).
> 5. **Acción Correctiva o Plan de Rollback:**
>    - Si identifico que un parámetro nuevo tiene un valor incompatible con el perfil de los teléfonos del operador, aplico un MOP de corrección de parámetros en caliente.
>    - Si la falla es un defecto interno de software del firmware de la radio o de la capa RRC del release (software bug), activo inmediatamente el procedimiento de **Rollback** restaurando la versión de configuración previa (`cvcu` restore) en coordinación con el NOC y el equipo de soporte Ericsson NPI."*

---

### Pregunta 22: "CASO REAL 2: Una celda 5G NR n78 (3.5 GHz) tiene 100 MHz de ancho de banda configurados, pero los usuarios solo logran 40 Mbps de Throughput DL en Drive Test. ¿Cómo realizas el diagnóstico?"
*(REAL SCENARIO 2: A 5G NR n78 cell with 100 MHz bandwidth only delivers 40 Mbps DL throughput during drive tests. How do you troubleshoot?)*

#### 💬 Respuesta Modelo:
> *"Con 100 MHz de ancho de banda en n78 (TDD con patrón 4:1 o DDDSU), el throughput pico en enlace descendente debería superar fácilmente los 800 Mbps a 1 Gbps. Si solo se alcanzan 40 Mbps, el problema puede estar en RF, modulación, sincronía o transporte:*
> 
> 1. **Verificación de Sincronía TDD y Reloj (PTP / GPS):**
>    - En redes 5G TDD, si hay un desfasamiento en la sincronía de reloj de tiempo (fase y frecuencia vía IEEE 1588v2 PTP o GPS), las ranuras de enlace ascendente de celdas vecinas colisionan con las ranuras de enlace descendente de la celda bajo prueba, destruyendo el SINR co-canal. Verifico con `inv` y logs de sincronía que no haya alarmas de reloj.
> 2. **Análisis de Métricas de Radio (SINR, MCS y Modulación):**
>    - En el log del Drive Test (TEMS/Nemo) o en moshell con `ue print -ad`, analizo:
>      - **SINR:** Si el SINR es pobre (< 5 dB) a pesar de estar cerca del sitio, hay una mala orientación de los haces de Massive MIMO o interferencia severa.
>      - **Distribución de Modulación:** Verifico si el enlace está estancado en QPSK o 16QAM en lugar de 256QAM.
>      - **Capas MIMO (Rank Indicator):** Si el UE reporta constantemente Rank 1 en lugar de Rank 4, no hay multiplexación espacial.
> 3. **Configuración de Beams de Massive MIMO:**
>    - Verifico si el `digitalTilt` configurado está apuntando al horizonte o 'por encima' de la zona de usuarios, o si el perfil de beamforming no coincide con el hardware de la antena AIR instalada.
> 4. **Cuello de Botella en Enlace de Transporte / Backhaul:**
>    - Verifico el ancho de banda asignado en el puerto eCPRI/Ethernet del router de sitio (fronthaul/backhaul). Si el enlace de transmisión está limitado a 100 Mbps o saturado por tráfico de otras tecnologías, el rendimiento de radio quedará capado físicamente."*

---

### Pregunta 23: "CASO REAL 3: Una celda LTE macro presenta una degradación severa de Accesibilidad RRC (82%) y su nivel promedio de RSSI en Uplink es de -85 dBm. ¿Cómo determinas si es interferencia externa o PIM interno?"
*(REAL SCENARIO 3: A macro LTE cell shows severe RRC Accessibility degradation (82%) and average UL RSSI of -85 dBm. How do you distinguish external interference from internal PIM?)*

#### 💬 Respuesta Modelo:
> *"Un nivel de RSSI de -85 dBm (frente al piso de ruido normal de -115 a -118 dBm) representa más de 30 dB de degradación de sensibilidad en el receptor de la estación base:*
> 
> 1. **Diferenciación entre PIM e Interferencia Externa mediante Correlación con Tráfico:**
>    - **Intermodulación Pasiva (PIM Interno en Antena / Jumpers):**
>      - El PIM es un fenómeno no lineal generado por elementos metálicos oxidados, conectores mal apretados o jumpers dañados cuando pasa alta potencia de transmisión.
>      - **Firma diagnóstica:** El nivel de RSSI en UL **se correlaciona perfectamente con el tráfico y la potencia transmitida en DL**. En horas pico de la tarde, cuando la celda transmite al máximo de potencia, el RSSI se dispara a -85 dBm; en la madrugada (3:00 AM), cuando la potencia de DL cae porque casi no hay tráfico, el RSSI desciende a niveles normales (-112 dBm).
>    - **Interferencia Externa (Repetidores ilegales, cámaras de seguridad, inhibidores jammers):**
>      - **Firma diagnóstica:** El nivel de interferencia es **constante las 24 horas del día** (línea plana en -85 dBm independientemente del volumen de tráfico), o presenta patrones que no coinciden con la curva de carga del operador.
> 2. **Acciones Inmediatas de Mitigación:**
>    - Si es PIM: Verificar alarmas de VSWR y Return Loss. Enviar cuadrilla a torre con equipo analizador de PIM para inspeccionar conectores, ajustar torques y sustituir jumpers dañados.
>    - Si es Interferencia Externa: Utilizar la función de espectrograma de la radio en ENM o coordinar escaneo con analizador de espectro de campo para localizar y reportar la fuente emisora ante el regulador (IFT en México).
>    - Mitigación provisional en parámetros: Incrementar temporalmente `pZeroNominalPucch` y `pZeroNominalPusch` para compensar el piso de ruido elevado y permitir que los terminales sean escuchados por el eNodeB."*

---

### Pregunta 24: "CASO REAL 4: Se reporta una tasa de éxito de Handover (HOSR) de apenas 88% entre dos sitios contiguos sobre una avenida de alta velocidad. ¿Cómo lo resuelves?"
*(REAL SCENARIO 4: Handover Success Rate is only 88% between two adjacent sites along a high-speed avenue. How do you fix it?)*

#### 💬 Respuesta Modelo:
> *"Un HOSR del 88% en una avenida de alta velocidad generalmente indica fallas por efecto Doppler, Handover tardío o solapamiento insuficiente:*
> 
> 1. **Auditoría de Relación de Vecindad y Parámetros de Movilidad:**
>    - Verifico que exista la relación `EUtranCellRelation` bidireccional y que `isHoAllowed = TRUE`.
>    - Verifico que no existan conflictos de PCI (PCI collision o PCI confusion) entre las celdas adyacentes de ambos sitios.
> 2. **Ajuste de Parámetros de Disparo de Handover (A3):**
>    - A altas velocidades (80–120 km/h), el tiempo de permanencia del vehículo en la zona de solapamiento de radio es de escasos segundos. Si el `timeToTrigger` está configurado en 320ms o 640ms, el UE pasa de largo antes de recibir el mensaje de reconfiguración.
>    - Reduzco el `timeToTrigger` a **100ms** o **80ms**.
>    - Reduzco el `a3offset` de 3 dB a **1.5 dB o 2 dB** para disparar la preparación del handover de forma anticipada.
> 3. **Optimización de Cobertura Física:**
>    - Reviso con el histograma de Timing Advance si los lóbulos de radiación de las antenas se cruzan con suficiente margen de potencia (> 6 a 10 dB sobre el piso de corte).
>    - Si es necesario, reduzco el tilt eléctrico (upsilt) de 1 grado en la celda origen para extender la huella de cobertura a lo largo de la avenida y asegurar una zona de solapamiento continua."*

---

# MÓDULO 7: METODOLOGÍA DE ANÁLISIS PRE Y POST OPTIMIZACIÓN

### Pregunta 25: "¿Cómo estructuras un análisis Pre-Post formal para validar mejoras de KPIs tras una optimización o activación de features?"
*(How do you structure a formal Pre-Post analysis to validate KPI gains after feature rollouts or parameter tuning?)*

#### 💬 Respuesta Metodológica:
> *"Un análisis Pre-Post riguroso debe garantizar significancia estadística y eliminar variables espurias:*
> 
> 1. **Definición de Períodos de Medición Homogéneos:**
>    - Selecciono un período de **Línea Base (Pre)** de al menos 7 a 14 días completos, y un período equivalente de evaluación **Post** de 7 días, asegurando comparar días idénticos (ej. martes contra martes) para evitar variaciones estacionales o de fin de semana.
> 2. **Aislamiento de la Hora Pico (Busy Hour Analysis):**
>    - Además de los promedios de 24 horas, calculo el impacto en la **Hora Pico de Red (Network Busy Hour)**, que es donde se manifiestan los cuellos de botella de capacidad, accesibilidad y latencia.
> 3. **Normalización por Volumen de Tráfico:**
>    - Si el Throughput sube un 10%, valido que no se deba a una caída en el número de usuarios. El volumen total de datos cursados (`pmPdcpVolDlDrb`) y el número de UEs conectados deben mantenerse constantes o haber aumentado para que la mejora sea estadísticamente válida.
> 4. **Análisis de Impacto Colateral (Side-effects Check):**
>    - Valido que mejorar un KPI no haya sacrificado otro. Por ejemplo, al subir la potencia de una celda para mejorar cobertura, compruebo que no se haya incrementado el nivel de interferencia co-canal en los sitios vecinos ni deteriorado el HOSR de las celdas adyacentes.
> 5. **Generación de Reportes Ejecutivos y Telemetría:**
>    - Presento los resultados en gráficos de tendencias temporales y tablas comparativas de Delta ($\Delta$ KPI), listando claramente las celdas aceptadas, las celdas neutras y cualquier excepción que requiera ajuste fino."*

---

# MÓDULO 8: PREGUNTAS CONDUCTUALES Y DE GESTIÓN (MÉTODO STAR)

### Pregunta 26: "Cuéntame sobre una ocasión en la que tuviste que optimizar un cluster con plazos de entrega extremadamente agresivos y bajo la presión directa del cliente."
*(Tell me about a time when you had to optimize a cluster under tight deadlines and direct client pressure)*

#### 💬 Respuesta con Método STAR (Situación, Tarea, Acción, Resultado):
> - **Situación (S):** *"Durante un despliegue masivo en AT&T México previo a una temporada comercial de alta demanda, recibimos un cluster de 85 sitios en una zona urbana densa con KPIs por debajo del SLA contractual del operador, particularmente en tasa de éxito de Handover (89% frente al objetivo del 98%) y Accesibilidad VoLTE (94% frente al 99%). El cliente amenazó con penalizaciones económicas si no se certificaba el cluster en 5 días hábiles."*
> - **Tarea (T):** *"Como Ingeniero Senior de Optimización RF, mi responsabilidad fue liderar la auditoría forense, identificar las causas raíz de la degradación y recuperar los KPIs a los niveles exigidos antes del cierre del plazo."*
> - **Acción (A):** *"En lugar de revisar celda por celda manualmente, desarrollé un script en Python conectado a las bases de datos de ENIQ para clasificar de inmediato las 15 'Top Worst Cells' que concentraban el 80% de las fallas (Principio de Pareto). Descubrí dos problemas mayores:*
>   1. *Había 18 relaciones de vecindad críticas faltantes entre sitios recién integrados y la red existente, lo que provocaba caídas masivas al cruzar límites de sector.*
>   2. *Había colisión de secuencias raíz de PRACH y un tilt eléctrico deficiente en dos celdas altas que sobrecubrían a los sitios vecinos.*
>   *Diseñé un MOP masivo en moshell para crear las relaciones adyacentes faltantes, reasignar PCIs conflictivos y ajustar el RET de las celdas sobrecobertoras. El MOP fue ejecutado y validado en la ventana nocturna del tercer día."*
> - **Resultado (R):** *"En 72 horas logramos elevar el HOSR al 98.6% y la Accesibilidad VoLTE al 99.4%, superando los SLAs contractuales. El cluster fue aceptado formalmente por el cliente sin penalizaciones y el script de priorización que creé fue adoptado por el equipo de ingeniería como estándar para futuros clusters."*

---

### Pregunta 27: "¿Cómo manejas desacuerdos técnicos con el equipo de Core o de Transmisión cuando los KPIs se degradan y se culpan mutuamente?"
*(How do you resolve cross-functional technical disagreements with Core or Transmission teams during KPI degradation?)*

#### 💬 Respuesta Modelo:
> *"Los desacuerdos entre RAN, Transmisión y Core son muy comunes cuando caen los KPIs, pero se resuelven con datos objetivos y trazas irrebatibles, nunca con opiniones:*
> 
> 1. **Presentación de Evidencia Objetiva de Capa 3:**
>    - Si hay caídas de E-RAB masivas, no señalo culpas genéricas. Extraigo trazas CTR/UETR o logs de interfaz S1/X2. Si la traza muestra que el eNodeB envía el mensaje `S1AP E-RAB Setup Request` y nunca recibe respuesta del MME hasta que expira el temporizador, o si hay un código de causa de rechazo específico proveniente del Core (`Cause: Radio Network Layer: Unknown or already allocated MME UE S1AP ID`), demuestro con la estampa de tiempo exacta que el origen del rechazo está en el Core.
> 2. **Medición de Jitter y Pérdida de Paquetes en Transmisión:**
>    - Si sospecho de transporte, reviso los contadores de paquetes descartados en la interfaz IP de la Baseband (`pmIpPacketsLost`, latencia promedio de ping TWAMP). Si la latencia supera los 50ms o hay fluctuaciones de reloj en PTP 1588v2, presento las gráficas de transporte para que el equipo de TX ajuste la cola de QoS o el ancho de banda del enlace microondas/fibra.
> 3. **Actitud de Colaboración:**
>    - Mi enfoque en Amdocs siempre es proactivo: convoco una sesión técnica rápida, muestro la correlación cronológica de eventos en una misma gráfica y propongo una prueba conjunta controlada para resolver el problema como un solo equipo enfocado en el cliente."*

---

### Pregunta 28: "¿Cómo utilizas tus conocimientos de Python, SQL o Power BI para hacer más eficiente tu trabajo diario de optimización?"
*(How do you leverage Python, SQL, and Power BI to improve daily RF optimization efficiency?)*

#### 💬 Respuesta Modelo:
> *"La programación es mi mayor multiplicador de productividad:*
> - **Automatización con Python:** En mis proyectos anteriores desarrollé scripts que automatizan la extracción diaria de archivos XML/CSV de contadores PM de Ericsson, calculan las fórmulas complejas de KPIs de los 5 pilares, rankean automáticamente las peores celdas por volumen de impacto y generan en cuestión de minutos los comandos moshell necesarios para aplicar correcciones masivas. Un análisis que tomaba 3 a 4 horas diarias quedó reducido a 15 minutos.
> - **Consultas SQL en ENIQ:** Escribo queries optimizadas directamente sobre la base de datos de rendimiento para cruzar información de configuración (CM) con contadores históricos (PM), detectando anomalías que no son visibles en las plantillas predeterminadas de los reportes estándar.
> - **Visualización en Power BI:** Construyo dashboards interactivos para la gerencia y los líderes de proyecto de Amdocs, permitiendo visualizar mapas de calor geográfico de degradación de KPIs, cumplimiento de SLAs por región y comparativas Pre-Post con filtros dinámicos por tecnología (4G vs 5G NSA)."*

---

# MÓDULO 9: PREGUNTAS ESTRATÉGICAS QUE JAVIER DEBE HACER AL ENTREVISTADOR

> [!TIP]
> Al final de la entrevista técnica, el entrevistador te dirá: *"Do you have any questions for us?"* (¿Tienes alguna pregunta para nosotros?). Un candidato junior dice "No, me quedó todo claro". Un **Senior Lead** hace preguntas técnicas que demuestran visión estratégica, conocimiento del negocio y ganas de tener impacto inmediato.

Elige 2 o 3 de estas preguntas según el perfil del entrevistador:

1. **Sobre la Arquitectura y Release de Software del Proyecto:**
   - *"¿Cuál es la versión actual de software de Ericsson desplegada en la red del cliente (ej. L20B, L21A o L22) y qué características avanzadas de 5G NSA están priorizando optimizar en este momento (Carrier Aggregation inter-banda, DSS o Massive MIMO con antenas AIR)?"*
2. **Sobre los Desafíos Técnicos Inmediatos:**
   - *"En los clusters que voy a asumir en Ciudad de México, ¿cuál es el pilar de KPI que actualmente representa el mayor reto para los SLAs del cliente (Retenibilidad de VoLTE, Throughput en bandas medias o éxito de adición de 5G NSA)?"*
3. **Sobre las Herramientas y Nivel de Acceso:**
   - *"¿Tendremos acceso directo vía terminal a ENM CLI y moshell/amos para la ejecución de scripts y diagnóstico en vivo, o el flujo de trabajo opera a través de un equipo centralizado de Configuration Management (CM)?"*
4. **Sobre la Visión a Mediano Plazo:**
   - *"Veo que la asignación inicial es por 3 meses con visión a fases subsecuentes del proyecto. Desde la perspectiva de Amdocs, ¿cuáles serían los hitos y resultados clave que definirían el éxito de mi gestión durante este primer trimestre?"*

---

# MÓDULO 10: CHEAT SHEET RÁPIDO DE PARÁMETROS Y COMANDOS ERICSSON
*(Hoja de repaso rápido para consultar 1 hora antes de la entrevista)*

### 📊 Tabla Maestra de Parámetros Críticos de Ericsson RAN:

| Objeto Gestionado (MO) | Nombre del Parámetro | Rango / Valor Típico | Impacto en el Rendimiento y Optimización |
| :--- | :--- | :--- | :--- |
| `EUtranCellFDD` | `cellRange` | 15 – 40 km | Distancia máxima permitida para acceso RACH. Si es muy bajo, terminales lejanos no pueden conectar; si es muy alto, incrementa carga de correlador. |
| `EUtranCellFDD` | `qRxLevMin` | -124 a -118 dBm | Nivel mínimo de RSRP requerido para que un UE pueda acampar en la celda LTE. Elevarlo evita que terminales en borde con señal precaria intenten conectar. |
| `EUtranCellFDD` | `pZeroNominalPucch` | -110 a -96 dBm | Potencia nominal objetivo del canal PUCCH. Subir este valor compensa altos niveles de interferencia de uplink (RSSI elevado/PIM). |
| `EUtranCellRelation` | `a3offset` | 1 a 3 dB | Margen de potencia por el cual la celda vecina debe superar a la servidora para disparar Handover Intra-frecuencia. Reducirlo acelera el handover. |
| `EUtranCellRelation` | `timeToTrigger` (TTT) | 80, 160, 320 ms | Tiempo durante el cual la condición de A3 debe cumplirse. Reducirlo soluciona handover tardío en avenidas rápidas; aumentarlo previene ping-pong. |
| `EUtranCellRelation` | `hysteresis` | 1 a 3 dB | Margen de histéresis para evitar traspasos oscilantes continuos entre celdas adyacentes. |
| `EUtranCellRelation` | `cellIndividualOffset` (CIO) | -6 a +6 dB | Offset individual aplicado a una vecindad específica para adelantar o retrasar el traspaso hacia una celda en particular. |
| `ReportConfigEUtra` | `b1ThresholdRsrp` | -106 a -98 dBm | Umbral de RSRP para detectar la presencia de señal 5G NR y disparar la solicitud de adición de nodo secundario (SgNB Addition) en NSA. |
| `ReportConfigEUtra` | `timeToTriggerB1` | 160 a 320 ms | Tiempo de estabilidad de la señal 5G requerida antes de enviar el reporte de medición B1. |
| `EUtranCellFDD` | `lbThreshold` | 70% a 85% | Umbral de utilización de PRBs para activar el balanceo de carga (MLB) inter-frecuencia hacia portadoras menos saturadas. |
| `RLC` / `PDCP` | `t310` | 1000 a 2000 ms | Temporizador de detección de Radio Link Failure (RLF). Al expirar tras N310 fallos de sincronía consecutivos, se declara la caída de radio. |

---

### 💻 Tabla de Comandos Rápidos de Moshell / Amos:

| Tarea de Ingeniería | Comando Moshell |
| :--- | :--- |
| **Cargar modelo de gestión** | `lt all` |
| **Auditar alarmas activas del nodo** | `alt` |
| **Consultar valor de un parámetro** | `get EUtranCellFDD=<nombre_celda> <parametro>` |
| **Modificar un parámetro** | `set <MO> <parametro> <nuevo_valor>` |
| **Bloquear / Desbloquear celda** | `bl EUtranCellFDD=<celda>` / `deb EUtranCellFDD=<celda>` |
| **Revisar estado de enlaces de fibra / SFP** | `cabx` |
| **Monitorear KPIs y contadores en tiempo real** | `kpiget` / `pmx -kpi` |
| **Ver usuarios y calidad de radio activa (RSRP/SINR)** | `ue print -ad` |
| **Ver inventario de hardware y tarjetas Baseband** | `inv` |
| **Crear backup de seguridad antes de cambios** | `cvcu "Pre_Optimization_Backup"` |
| **Listar copias de seguridad existentes** | `cvls` |

---


---

# MÓDULO 11: GUÍA AVANZADA DE DOMINIO TÉCNICO Y CASOS PRÁCTICOS 5G (ERICSSON 2022–2026)

> [!IMPORTANT]
> Este módulo aborda con profundidad técnica de nivel Senior Lead los 7 tópicos cardinales solicitados en las evaluaciones de ingeniería de Ericsson y Amdocs para proyectos 2022–2026: Estrategia de Gestión de Capas (LMS), Movilidad 5G NSA / EN-DC, Interrelación de KPIs, Funcionalidades Avanzadas de Radio, Troubleshooting de Interferencias y Causa Raíz (RCA), Herramientas de Automatización (ENM/Moshell/Python/SQL) y 3 Casos Prácticos Reales estructurados bajo el método STAR con métricas cuantificadas.

---

### Pregunta 32: LMS – Layer Management Strategy, Inter-frequency Load Balancing y Traffic Steering
*(LMS Fundamentals, Inter-Frequency Load Balancing, Traffic Steering & Layer Prioritization)*

#### 🎯 Estrategia y Enfoque Senior:
- Presenta LMS como una arquitectura integral de red para maximizar la eficiencia espectral (bps/Hz) y la satisfacción del usuario, no como una simple reacción a la congestión.
- Diferencia claramente entre **Traffic Steering en Modo Reposo (Idle Mode)** mediante prioridades de reselección en SIBs y **Traffic Steering en Modo Conectado (Connected Mode)** mediante Mobility Load Balancing (MLB) y Service-Specific Load Balancing (SSLB).
- Cita los Managed Objects (MOs) y parámetros exactos de Ericsson MOM (`EUtranFreqRelation`, `EUtranCellFDD`, `ReportConfigEUtra`).

#### 💬 Respuesta Modelo para Teleprompter:
> *"La Estrategia de Gestión de Capas (LMS) es la columna vertebral del rendimiento en una red multi-banda LTE y 5G de Ericsson. Mi enfoque se estructura en cuatro niveles operativos:*
> 
> 1. **Fundamentos y Arquitectura de Capas:**
>    - Diseñamos la red clasificando las bandas según su física de propagación: bandas bajas (B28 / 700 MHz) para cobertura macro e interiores; bandas medias (B2 / 1900 MHz y B4 / AWS 2100 MHz) para cobertura urbana y capacidad base; y bandas altas (B7 / 2600 MHz y 5G NR n78 / 3.5 GHz) para inyección masiva de throughput.
>    - Sin una estrategia LMS activa, los terminales tienden a quedar atrapados en la capa de mayor cobertura (B28), provocando saturación de PRBs (>85%), degradación de modulación y colapso del throughput del clúster mientras las portadoras B4/B7 permanecen subutilizadas.
> 
> 2. **Traffic Steering en Modo Reposo (Idle Mode):**
>    - Controlamos el acampado inicial configurando `cellReselectionPriority` en `EUtranFreqRelation` transmitido en SIB4 y SIB5: asignamos prioridad 7 a B7, prioridad 6 a B4/B2 y prioridad 4 a B28.
>    - Ajustamos `threshXHigh` y `qRxLevMin` en las capas de capacidad para que el UE solo acampe en capas altas si el RSRP garantiza un SINR limpio (>3 dB), forzando el drenaje natural hacia portadoras de mayor ancho de banda antes de que el usuario inicie tráfico.
> 
> 3. **Traffic Steering en Modo Conectado y Mobility Load Balancing (MLB):**
>    - Activamos la funcionalidad de Ericsson `Mobility Load Balancing` en `EUtranCellFDD`. Configuramos el umbral `lbThreshold` en 72%–75% y `lbActivationThreshold` para determinar cuándo la celda servidora se considera congestionada.
>    - El eNodeB evalúa contadores `pmPrbUtilDl` y dispara mediciones inter-frecuencia Evento A5 (`a5Threshold1Rsrp`, `a5Threshold2Rsrp`) hacia portadoras co-ubicadas con baja ocupación, redirigiendo sesiones de datos hacia capas con menor carga sin cortar llamadas.
> 
> 4. **Priorización por Servicio y Perfil (RFSP / SPID):**
>    - Mediante `ServiceSpecificLoadBalancing` y perfiles SPID asignados por el Core MME/HSS, dirigimos el tráfico de datos pesados (QCI 9 / 5QI 9) hacia combinaciones de Carrier Aggregation en B4/B7/n78, mientras reservamos y anclamos el tráfico de voz VoLTE (QCI 1) en capas de cobertura estables (B28/B2) para evitar caídas por desvanecimiento rápido."*

#### 📊 Parámetros y Comandos de Referencia Ericsson:
- `EUtranFreqRelation:cellReselectionPriority` (Prioridad de frecuencia para reselección SIB4/5: 0 a 7).
- `EUtranCellFDD:lbThreshold` (Umbral de ocupación de PRB para activación de MLB: típicamente 70% a 75%).
- `EUtranCellFDD:loadBalancingTrigger` (`trafficOnly`, `subscribersOnly`, `composite`).
- `ReportConfigEUtra:a5Threshold1Rsrp` / `a5Threshold2Rsrp` (Umbrales de RSRP para handover A5 por carga).
- Comando Moshell: `get EUtranCellFDD=<celda> lb` / `set EUtranFreqRelation=<id> cellReselectionPriority 6`.

---

### Pregunta 33: 5G NSA / EN-DC Mobility, LTE Anchor Selection y Optimización de Eventos A3, A5 y B1
*(5G NSA / EN-DC Mobility, Anchor Selection, A3/A5/B1 Events & Troubleshooting)*

#### 🎯 Estrategia y Enfoque Senior:
- Enfatiza tu conocimiento práctico en la arquitectura **Option 3x (Dual Connectivity EN-DC)** con plano de control en el eNodeB (MeNB) y plano de usuario dividido (Split Bearer) a nivel de PDCP en el gNodeB (SgNB).
- Describe el rol de cada evento RRC: **A3** (movilidad intra-frecuencia), **A5** (handover inter-frecuencia de capa ancla) y **B1** (detección y adición de la celda secundaria 5G NR).
- Explica cómo resolver caídas de 5G y fallos de adición analizando la interfaz X2-C/X2-U y parámetros de estabilidad de radio.

#### 💬 Respuesta Modelo para Teleprompter:
> *"La movilidad en 5G NSA (EN-DC) requiere sintonizar con precisión quirúrgica la interacción entre la celda ancla LTE y la celda secundaria NR:*
> 
> 1. **Selección de la Celda Ancla LTE (Anchor Selection):**
>    - En Option 3x, la celda LTE actúa como Master eNodeB (MeNB), gestionando la conexión RRC con el terminal y la señalización S1-MME con el EPC.
>    - Es fundamental priorizar capas de anclaje con buen ancho de banda y cobertura continua (como B4/B66 de 20 MHz o B2) sobre B28, configurando `endcAllowed = TRUE` en `EUtranCellFDD` y asignando mayor prioridad de anclaje para evitar que UEs en celdas congestionadas o con backhaul limitado intenten levantar portadoras secundarias 5G.
> 
> 2. **Flujo de Adición de Celda Secundaria NR (SgNB Addition):**
>    - El eNodeB configura en el UE la medición del **Evento B1** (Inter-RAT) mediante `ReportConfigEUtra`.
>    - Cuando el UE reporta que la señal SSB de la celda 5G NR n78 supera el umbral `b1ThresholdRsrp` (típicamente -104 dBm) de forma estable durante `timeToTriggerB1` (160 ms), el eNodeB envía el mensaje `X2AP: SGNB ADDITION REQUEST` al gNodeB por la interfaz X2-C.
>    - El gNodeB reserva recursos radio (PRBs, PUCCH, preámbulos RACH) y responde `SGNB ADDITION REQUEST ACKNOWLEDGE`. El eNodeB envía un `RRCConnectionReconfiguration` al UE con el contenedor `nr-Config`. El UE ejecuta el procedimiento de acceso aleatorio (RACH) en la celda NR y confirma la adición exitosa.
> 
> 3. **Optimización de Eventos de Movilidad (A3, A5, B1):**
>    - **Evento A3 (Intra-LTE / Intra-NR):** Motor principal de handover. Sintonizo `a3offset` (1.5 a 2.0 dB) y `timeToTrigger` (100 a 160 ms) para evitar 'Late Handover' en avenidas rápidas y `hysteresis` (2 dB) para erradicar el ping-pong.
>    - **Evento A5 (Inter-Frequency Anchor HO):** Asegura que si el ancla LTE actual se degrada, el terminal salte a otra portadora LTE ancla con cobertura n78 antes de perder la conexión RRC.
>    - **Evento B1 (5G Addition):** Si se fija un umbral demasiado agresivo (-112 dBm), se disparan adiciones prematuras en borde que terminan en caídas inmediatas; si es muy conservador (-96 dBm), se desperdicia la cobertura 5G.
> 
> 4. **Troubleshooting de Fallas de Movilidad y Experiencia de Usuario:**
>    - **Falla en Adición SgNB (`pmEndcSetupFail`):** Correlaciono en ENM si la causa es rechazo de admisión por congestión de hardware en Baseband (`pmEndcSetupFailGnbNoRadioRes`), latencia excesiva en transporte X2, o fallas de RACH en la celda NR por discrepancia de potencia en SSB o colisión de preámbulos.
>    - **Caídas de Sesión 5G (Abnormal Releases):** La principal causa de caída en 5G NSA no suele ser la radio 5G, sino la pérdida de la celda ancla LTE (`Radio Link Failure` en MCG por expiración de T310). Optimizando la retenibilidad y cobertura del ancla LTE protegemos directamente la sesión 5G."*

#### 📊 Parámetros y Comandos de Referencia Ericsson:
- `ReportConfigEUtra:b1ThresholdRsrp` (Umbral RSRP de detección 5G NR: -106 a -100 dBm).
- `ReportConfigEUtra:timeToTriggerB1` (Tiempo de persistencia B1: 80, 160, 320 ms).
- `EUtranCellRelation:a3offset` / `timeToTrigger` / `hysteresis` (Parámetros de movilidad A3).
- `EUtranCellFDD:endcAllowed` (Habilita la celda LTE como ancla EN-DC).
- Contadores: `pmEndcSetupAtt`, `pmEndcSetupSucc`, `pmEndcSetupFailGnb`, `pmEndcRelAbnormalGnbAct`.

---

### Pregunta 34: RF Optimization KPIs: Relación de SINR, CQI, PRB Utilization, Throughput y Experiencia de Usuario
*(RF Optimization KPIs: SINR, CQI, PRBs, Spectral Efficiency, Accessibility & Customer Experience)*

#### 🎯 Estrategia y Enfoque Senior:
- Demuestra que entiendes la física del enlace descendente (downlink) y ascendente (uplink): cómo el SINR gobierna la selección de modulación (CQI/MCS), cómo esto determina la eficiencia espectral, y cómo impacta en las métricas de negocio y QoE.
- Cita las fórmulas de los 3 pilares clave de SLA (Accesibilidad, Retenibilidad, Movilidad) y relaciónalos con la percepción de servicio (streaming de video, navegación, llamadas VoLTE/VoNR).

#### 💬 Respuesta Modelo para Teleprompter:
> *"El rendimiento de una red celular se rige por una relación directa de causa y efecto desde la capa física hasta la percepción del usuario:
> 
> 1. **Relación entre SINR, CQI y Throughput:**
>    - El SINR (Signal-to-Interference-plus-Noise Ratio) es la métrica de pureza del canal radio.
>    - Con base en el SINR medido de las señales de referencia (CRS en LTE, CSI-RS/SSB en 5G), el terminal calcula y reporta el CQI (Channel Quality Indicator, del 1 al 15) hacia el scheduler del eNodeB/gNodeB.
>    - El scheduler traduce el CQI al MCS (Modulation and Coding Scheme, 0 al 28), determinando el orden de modulación: de QPSK (bajo throughput pero ultra robusto) hasta 64QAM y 256QAM (alta tasa de bits).
>    - De acuerdo con el teorema de Shannon-Hartley, elevar el SINR promedio de 3 dB a 18 dB permite al scheduler seleccionar 256QAM en lugar de QPSK/16QAM, cuadruplicando la tasa de datos de usuario con exactamente la misma cantidad de PRBs.
> 
> 2. **Utilización de PRB vs Eficiencia Espectral:**
>    - La utilización de PRB (`pmPrbUtilDl`, `pmPrbUtilUl`) mide la ocupación temporal y frecuencial de la portadora.
>    - Un sector con alta utilización de PRBs (>80%) pero con bajo throughput es el síntoma clásico de una red enferma por interferencia: los usuarios operan con MCS bajo, sufren alta tasa de retransmisiones HARQ (>10% BLER residual) y consumen muchos bloques de recursos para transmitir pocos bytes útiles.
>    - La verdadera meta de optimización es maximizar la Eficiencia Espectral (bits/segundo/Hz): logramos esto limpiando interferencias (PIM/RTWP), optimizando el tilt para aislar celdas y activando capas MIMO superiores (Rank 3 y Rank 4).
> 
> 3. **Los Tres Pilares de SLA y su Impacto en el Negocio:**
>    - **Accesibilidad (>99.5%):** RRC Setup SR $	imes$ E-RAB Setup SR $	imes$ SgNB Addition SR. Mide la probabilidad de que el cliente obtenga servicio al primer intento.
>    - **Retenibilidad (<0.8% Drop Rate datos, <0.4% VoLTE):** Mide la estabilidad de la llamada o sesión de navegación sin cortes abruptos por Radio Link Failure.
>    - **Movilidad (HOSR >98.5%):** Garantiza la continuidad fluida de sesiones mientras el usuario se desplaza a velocidad vehicular.
> 
> 4. **Traducción a la Experiencia del Cliente (Customer Experience / QoE):**
>    - Un throughput inicial deficiente y una alta latencia de RRC provocan el temido 'video buffering' y tiempos lentos de carga de páginas web.
>    - Paquetes perdidos en QCI 1/5QI 1 provocan distorsión de voz, silencios y llamadas caídas en VoLTE/VoNR. Al optimizar el SINR y balancear los PRBs, reducimos el jitter, eliminamos la latencia de encolamiento y aseguramos una experiencia premium para el suscriptor."*

#### 📊 Fórmulas y Contadores de Referencia Ericsson:
- Throughput DL: $	ext{Throughput} = rac{	ext{pmPdcpVolDlDrb} 	imes 8}{	ext{pmUeThpTimeDl}} 	ext{ [bps]}$.
- Utilización PRB: $	ext{PRB Utilization DL (\%)} = rac{	ext{pmPrbUsedDlDt}}{	ext{pmPrbAvailDl}} 	imes 100$.
- Retenibilidad E-RAB: $	ext{DCR (\%)} = rac{	ext{pmErabRelAbnormalEnbAct}}{	ext{pmErabRelAbnormalEnbAct} + 	ext{pmErabRelNormalEnb}} 	imes 100$.
- Accesibilidad RRC: $	ext{RRC SR (\%)} = rac{	ext{pmRrcConnEstabSucc}}{	ext{pmRrcConnEstabAtt}} 	imes 100$.

---

### Pregunta 35: Ericsson Advanced Features: Carrier Aggregation (CA), Massive MIMO, ANR, RS Power y HARQ
*(Carrier Aggregation, Massive MIMO, ANR, RS Power Optimization, HARQ & DSS)*

#### 🎯 Estrategia y Enfoque Senior:
- Detalla tu experiencia práctica activando, monitoreando y sintonizando las funcionalidades más avanzadas del software de radio de Ericsson (L20/L21/L22).
- Menciona los objetos de control de cada feature (`CarrierAggregationFunction`, `AnrFunctionEUtran`, `SectorCarrier`, etc.) y las mejores prácticas de campo.

#### 💬 Respuesta Modelo para Teleprompter:
> *"En los proyectos de modernización de Ericsson en los que he participado, las funcionalidades avanzadas son los motores principales de capacidad y calidad:*
> 
> 1. **Carrier Aggregation (CA):**
>    - He implementado configuraciones de 2CC hasta 4CC en downlink combinando portadoras FDD (B28 + B4 + B7) y TDD con agregación en uplink.
>    - En el MOM de Ericsson se administra en `CarrierAggregationFunction`. Configuramos la celda primaria (PCell) para señalización y agregamos celdas secundarias (SCells) basadas en medición Evento A4 (`a4ThresholdRsrp`) o mediante activación ciega (`blindScellAddition = TRUE`) cuando la cobertura entre portadoras es co-sito idéntica.
>    - Sintonizamos `caActivationThreshDl` para activar las SCells solo cuando el buffer del UE supere cierto volumen de datos, evitando sobrecarga de señalización en conexiones cortas de fondo.
> 
> 2. **Massive MIMO y Beamforming (AIR 6449 / AIR 3268):**
>    - Despliegue en 5G NR n78 (3.5 GHz) con antenas activas 64T64R y 32T32R.
>    - El beamforming digital permite concentrar la energía de radio hacia el terminal en azimut y elevación (3D Beamforming), aumentando el SINR percibido hasta en 6–8 dB en comparación con antenas pasivas tradicionales.
>    - Con Multi-User MIMO (MU-MIMO) transmitimos flujos de datos ortogonales hacia múltiples usuarios simultáneos en los mismos bloques de tiempo y frecuencia, multiplicando la capacidad del sector por 3 a 4 veces en zonas de alta densidad como centros urbanos o eventos masivos.
> 
> 3. **Automatic Neighbor Relations (ANR):**
>    - Gestionado a través de `AnrFunctionEUtran` y `AnrFunctionNR`.
>    - Habilito ANR para que los UEs decodifiquen automáticamente el CGI (Cell Global Identity) o NCGI de celdas vecinas no configuradas durante periodos de medición DRX (`si-Request`).
>    - La Baseband crea de manera autónoma las relaciones de vecindad (`EUtranCellRelation`), auditando conflictos de PCI (colisión y confusión mod 3 / mod 30) y eliminando relaciones muertas tras 30 días de inactividad, lo que reduce drásticamente el mantenimiento manual.
> 
> 4. **Optimización de Potencia de Señal de Referencia (RS Power):**
>    - Administrado en `SectorCarrier:referenceSignalPower` y los offsets de potencia PDSCH `pA` y `pB`.
>    - Típicamente ajustamos `referenceSignalPower` entre 15.2 dBm y 18.2 dBm según la potencia del radio (40W/60W/80W). Mantener una relación equilibrada con `pA = -3 dB` y `pB = 1` asegura que los símbolos de datos no sufran distorsión de potencia respecto a los pilotos, controlando el área de cobertura sin contaminar a celdas adyacentes.
> 
> 5. **HARQ y Dynamic Spectrum Sharing (DSS):**
>    - **HARQ:** Asíncrono en DL con redundancia incremental (IR) y síncrono en UL, sintonizando `maxHarqTx = 4` para limitar la latencia de retransmisión a menos de 40 ms.
>    - **DSS:** Permite la coexistencia dinámica de 4G y 5G en la misma portadora (ej. B28/n28 o B66/n66), asignando subtramas mediante patrones de tasa MBSFN o rate-matching para no interferir los CRS de LTE."*

#### 📊 Parámetros y Comandos de Referencia Ericsson:
- `CarrierAggregationFunction:sCellPriority` / `caActivationThreshDl`.
- `SectorCarrier:referenceSignalPower` (Potencia de CRS por puerto de antena).
- `EUtranCellFDD:pA` (-3 dB, -4.77 dB, 0 dB) y `pB` (0, 1, 2, 3).
- `AnrFunctionEUtran:anrState` (`ACTIVATED`, `DEACTIVATED`).
- Comando Moshell: `get SectorCarrier referenceSignalPower` / `get CarrierAggregationFunction`.

---

### Pregunta 36: Troubleshooting de Interferencias: Análisis Forense de RTWP, PIM, SINR y RCA
*(Interference Troubleshooting, RTWP, PIM Detection, SINR Degradation & RCA Framework)*

#### 🎯 Estrategia y Enfoque Senior:
- Presenta tu metodología de **Análisis de Causa Raíz (RCA)** en 5 pasos lógicos y estructurados.
- Explica la diferencia técnica crucial entre **Interferencia Externa** (constante en el tiempo) e **Interferencia Pasiva Interna - PIM** (correlacionada con la potencia y el tráfico de bajada del sitio).
- Detalla los valores de referencia de RTWP y cómo resolver problemas físicos y lógicos de radiofrecuencia.

#### 💬 Respuesta Modelo para Teleprompter:
> *"La degradación de interferencia en uplink es el enemigo silencioso más dañino para la red porque destruye la accesibilidad y eleva el consumo de batería de los terminales. Mi metodología de investigación se basa en 5 pasos rigurosos:
> 
> 1. **Análisis Forense de RTWP (Received Total Wideband Power):**
>    - En condiciones normales de un sector limpio sin carga, el RTWP o nivel de interferencia por PRB oscila entre **-106 dBm y -102 dBm**.
>    - Cuando el RTWP se eleva por encima de **-95 dBm**, los UEs en borde de celda alcanzan su potencia máxima de transmisión (`pMax = 23 dBm`) y no logran cerrar el enlace de subida, disparando fallos de acceso aleatorio PRACH (`pmRrcConnEstabFail`) y caídas de sesión.
>    - En Moshell monitoreo los contadores `pmInterferencePwrReport` y desgloso la interferencia rama por rama de antena (RXA vs RXB).
> 
> 2. **Identificación y Diagnóstico de PIM (Passive Intermodulation):**
>    - El PIM se origina por no linealidades físicas en la línea de transmisión de radio: conectores corroídos, uniones sulfatadas, jumpers defectuosos o abrazaderas metálicas flojas en el campo cercano de la antena.
>    - **Prueba Definitiva de PIM:** Correlaciono en ENIQ el contador `pmInterferencePwrReport` (RTWP) contra el contador de potencia de transmisión de bajada `pmRadioTxPower` y la utilización de PRBs DL. Si el RTWP sube en horas pico en perfecta sincronía con el tráfico DL y cae durante la madrugada cuando el transmisor baja de potencia, el diagnóstico es **PIM Interno**.
>    - Si la interferencia permanece constante las 24 horas del día (incluso bloqueando el transmisor con `bl`), el origen es **Interferencia Externa** (repetidores ilegales, jammer o radiaciones espurias).
> 
> 3. **Investigación de Degradación de SINR y Pilot Pollution:**
>    - El pilot pollution ocurre cuando el terminal recibe 3 o más señales celulares con niveles de RSRP muy cercanos (diferencia <3 dB) y ningún sector dominante.
>    - Los pilotos CRS colisionan entre sí, hundiendo el SINR por debajo de -3 dB a pesar de tener una cobertura fuerte de -85 dBm RSRP.
>    - Lo solucionamos aplicando ajuste de tilt eléctrico en ENM mediante RET (`electricalAntennaTilt` en `AntennaSubunit`), cerrando el lóbulo de irradiación del sector que invade celdas adyacentes para restaurar la dominancia.
> 
> 4. **Marco de Trabajo RCA en 5 Pasos:**
>    - **Paso 1: Integridad de Hardware:** Ejecuto `alt` y `cabx` en Moshell; verifico alarmas de VSWR y atenuación de fibra óptica.
>    - **Paso 2: Correlación Estadística:** Cruzo contadores de caída con tráfico, interferencia y fallas de handover.
>    - **Paso 3: Trazas de Capa 3:** Analizo trazas CTR/UETR en ENM para identificar el mensaje exacto donde falla el enlace (ej. expiración de T310 o fallo de RACH).
>    - **Paso 4: Acción Correctiva:** Corrección lógica temporal (`pZeroNominalPucch` para superar piso de ruido transitorio) y despacho de cuadrilla con equipo Anritsu Site Master para torqueo a 25 Nm o cambio de jumper.
>    - **Paso 5: Validación a 72 Horas:** Confirmación de que el RTWP regresó a -103 dBm y el throughput se recuperó."*

#### 📊 Parámetros y Comandos de Referencia Ericsson:
- `EUtranCellFDD:pZeroNominalPucch` (Potencia nominal objetivo PUCCH: típicamente -106 a -96 dBm).
- `AntennaSubunit:electricalAntennaTilt` (Ajuste de tilt eléctrico remoto RET: 0 a 10 grados).
- Contadores: `pmInterferencePwrReport`, `pmRadioTxPower`, `pmRssiPucch`, `pmPrbUtilUl`.
- Comando Moshell: `pmx -kpi EUtranCellFDD pmInterference` / `get AntennaSubunit electricalAntennaTilt`.

---

### Pregunta 37: Herramientas Técnicas: Ericsson ENM, MOSHELL, Contadores y Automatización con Python/SQL
*(Technical Analysis Tools: Ericsson ENM, Moshell, Raw Counters, Python & SQL Automation)*

#### 🎯 Estrategia y Enfoque Senior:
- Muestra agilidad tanto en la operación interactiva en tiempo real (Moshell/AMOS en línea de comando) como en el análisis masivo de datos de red (ENM, ENIQ, Python y SQL).
- Explica tu metodología para automatizar tareas rutinarias de optimización y auditar clústeres enteros de cientos de nodos en minutos.

#### 💬 Respuesta Modelo para Teleprompter:
> *"La combinación de dominio de línea de comando de bajo nivel en Ericsson con automatización de datos a escala es mi mayor ventaja técnica en el día a día:
> 
> 1. **Ericsson Network Manager (ENM) y MOSHELL / AMOS:**
>    - En ENM opero los módulos de Configuration Management (CM) para cambios masivos, Fault Management (FM) para correlación de alarmas críticas y ENIQ para reportes de desempeño histórico.
>    - En **Moshell / AMOS**, domino la navegación ágil del MOM:
>      - `lt all` para cargar el modelo de objetos gestionados de la Baseband.
>      - `alt` para listar alarmas activas con estampa de tiempo y severidad.
>      - `get` y `set` para auditar y modificar atributos de celdas y frecuencias al instante.
>      - `cabx` para auditar interfaces ópticas CPRI/eCPRI, potencia óptica recibida en SFPs y cables de radio.
>      - `ue print -ad` para inspeccionar en vivo las sesiones activas con su RSRP, SINR, CQI y avance de tiempo (Timing Advance) en metros.
>      - `cvcu "Pre_Optimization_Backup"` para asegurar un punto de restauración antes de cualquier cambio crítico.
> 
> 2. **Procesamiento de Contadores y Archivos ROP:**
>    - Conozco la estructura de los archivos ROP (Result Output Period de 15 minutos) generados por los nodos en formato ASN.1 y XML.
>    - Distingo entre contadores de evento ('peg counters', como `pmRrcConnEstabAtt`) y contadores de estado o duración (`pmActiveUeDlMax`), aplicando agregaciones ponderadas por volumen de tráfico en lugar de promedios simples.
> 
> 3. **Automatización con Python y SQL:**
>    - **Python (pandas, paramiko, openpyxl):** Desarrollé scripts que se conectan de forma automatizada por SSH a ENM CLI o múltiples nodos en paralelo mediante `paramiko`. Mis herramientas extraen contadores nocturnos, calculan las fórmulas de los 5 pilares, generan el ranking automático de las peores celdas del clúster (Worst Cells) y producen los scripts `.mos` listos para ejecución masiva. Lo que antes tomaba 4 horas de análisis manual queda resuelto en 15 minutos.
>    - **Consultas SQL en ENIQ:** Escribo queries optimizadas que cruzan tablas de configuración (`DIM_EUTRANCELL`) con tablas históricas de rendimiento (`FACT_PM_EUTRAN`) para detectar anomalías sistémicas, como celdas con parámetros de movilidad desalineados con el baseline del clúster.
> 
> 4. **Metodología de Comparación Pre y Post Optimización:**
>    - Establezco una ventana de referencia de 7 días continuos 'Pre' y 7 días 'Post', asegurando comparar los mismos días de la semana para eliminar sesgos de estacionalidad.
>    - Normalizo los KPIs de accesibilidad, caídas y throughput contra el volumen de datos cursados (Erlangs o GigaBytes), asegurando que las mejoras sean estadísticamente significativas."*

#### 📊 Resumen de Comandos Moshell Críticos:
- `lt all` $ightarrow$ Carga completa del Managed Object Model.
- `alt` $ightarrow$ Lista alarmas activas clasificadas por severidad.
- `get EUtranCellFDD <parametro>` $ightarrow$ Consulta parámetros en vivo.
- `set <MO> <parametro> <valor>` $ightarrow$ Modificación de atributos.
- `cabx` $ightarrow$ Diagnóstico de hardware, puertos ópticos y radios.
- `ue print -ad` $ightarrow$ Monitoreo de usuarios conectados y métricas de radio.
- `kpiget` / `pmx -kpi` $ightarrow$ Monitoreo de contadores en tiempo real.
- `cvcu` / `cvls` $ightarrow$ Creación y listado de copias de seguridad de configuración.

---

### Pregunta 38: Experiencia Práctica – Caso 1: Optimización de Load Balancing / LMS en Red Ericsson Multi-Capa (2022–2026)
*(Practical Case 1: Multi-Layer LMS & Load Balancing Optimization in Ericsson Network)*

#### 🎯 Estrategia y Enfoque Senior:
- Estructura la respuesta rigurosamente bajo el **Método STAR** (Situación, Tarea, Acción, Resultado).
- Responde explícitamente a las 5 preguntas del entrevistador: Problema inicial, Herramientas/contadores, Parámetros modificados, Contribución personal, y Resultado final medible.

#### 💬 Respuesta Modelo para Teleprompter:
> *"Durante mi asignación en proyectos de optimización de red Ericsson entre noviembre de 2022 y 2026, lideré la resolución de un problema crítico de desbalance de carga multi-capa en un clúster metropolitano de alta densidad:
> 
> 1. **¿Cuál era el problema inicial?**
>    - En un clúster urbano de 45 sitios macro con cobertura multi-banda (B28 en 700 MHz, B4 en AWS 20 MHz y B7 en 2.6 GHz 20 MHz), la portadora B28 sufría una congestión severa durante la hora pico nocturna (18:00 a 22:00 horas).
>    - La utilización de PRBs en B28 superaba el **88%**, provocando una caída drástica del throughput de usuario a menos de **3.8 Mbps**, demoras en acceso y degradación de la calidad de voz VoLTE. Al mismo tiempo, las portadoras de capacidad co-ubicadas B4 y B7 operaban con menos del **28% de PRBs utilizados**, evidenciando un desperdicio masivo de espectro.
> 
> 2. **¿Qué herramientas y contadores utilicé?**
>    - Utilicé **Ericsson ENM**, **Moshell/AMOS** y consultas SQL sobre la base de datos de rendimiento **ENIQ**.
>    - Analicé los contadores `pmPrbUtilDl` (utilización de PRB en bajada), `pmActiveUeDl` (número de usuarios concurrentes activos), `pmPdcpVolDlDrb` (volumen de tráfico en bytes) y `pmErabEstabAtt` / `pmErabEstabSucc`.
> 
> 3. **¿Qué parámetros o funcionalidades modifiqué?**
>    - En `EUtranFreqRelation`: Reconfiguré las prioridades de reselección en modo reposo (`cellReselectionPriority`), elevando B7 a prioridad 7, B4 a prioridad 6 y reduciendo B28 a prioridad 4 en los bloques SIB4/SIB5.
>    - En `EUtranCellFDD`: Activé la funcionalidad de **Mobility Load Balancing (MLB)**; reduje el umbral `lbThreshold` del valor por defecto de 85% a **72%**, fijé `lbActivationThreshold` en 75% y configuré `loadBalancingTrigger = trafficOnly`.
>    - En `ReportConfigEUtra`: Sintonizamos los umbrales de medición Evento A5 (`a5Threshold1Rsrp = -105 dBm` y `a5Threshold2Rsrp = -100 dBm`) para transferir sesiones activas hacia B4/B7 de forma oportuna.
>    - Ajusté `qRxLevMin` en B4/B7 de -120 dBm a -116 dBm para asegurar que solo UEs con buen link budget acamparan en las bandas altas.
> 
> 4. **¿Cuál fue mi contribución personal?**
>    - Analicé 30 días de contadores ROP mediante un script propio en Python, demostrando que el 60% de los UEs permanecían cautivos en B28 debido a umbrales de reselección estáticos y conservadores.
>    - Diseñé el MOP integral de rebalanceo en 3 fases para mitigar riesgos; escribí los scripts automatizados de Moshell con verificación de respaldo (`cvcu Pre_LMS_Tuning`); coordiné y ejecuté la ventana de mantenimiento nocturna; y lideré la auditoría de estabilidad post-lanzamiento durante 72 horas.
> 
> 5. **¿Cuál fue el resultado final medible?**
>    - La utilización de PRB en hora pico en B28 se redujo del 88% al **54%** (-34% de congestión).
>    - Las portadoras de capacidad B4 y B7 absorbieron el tráfico, estabilizándose en una utilización equilibrada del **58% al 62%**.
>    - El throughput promedio de descarga por usuario en el clúster se incrementó en un **+72%** (subiendo de 3.8 Mbps a **6.5 Mbps** en LTE).
>    - La tasa de caídas de llamadas VoLTE se redujo de 0.42% a **0.25%**, resolviendo integralmente la queja de calidad del cliente."*

---

### Pregunta 39: Experiencia Práctica – Caso 2: Optimización de Movilidad 5G NSA / EN-DC y Selección de Anchor LTE (2022–2026)
*(Practical Case 2: 5G NSA / EN-DC Mobility & Anchor Selection Optimization)*

#### 🎯 Estrategia y Enfoque Senior:
- Presenta un caso enfocado en la tecnología de punta: **5G NSA Option 3x** en una autopista de alta velocidad.
- Responde con precisión a las 5 preguntas del entrevistador: Problema, Herramientas, Parámetros, Contribución personal y Resultados medibles.

#### 💬 Respuesta Modelo para Teleprompter:
> *"En un proyecto reciente de optimización de red 5G de Ericsson (2022–2026), resolví una falla crítica de estabilidad de movilidad en 5G NSA a lo largo de un corredor vial interurbano de alta velocidad (100–120 km/h):
> 
> 1. **¿Cuál era el problema inicial?**
>    - Los usuarios que se desplazaban a velocidad vehicular experimentaban una severa degradación en sesiones de datos 5G: la tasa de éxito de adición de celda secundaria 5G (`SgNB Addition Success Rate`) caía hasta el **85.2%** (con 14.8% de fallas) y la tasa de caídas de sesiones 5G alcanzaba un inaceptable **3.9%**.
>    - El drive test revelaba un continuo 'ping-pong' de handover entre las celdas ancla LTE y adiciones prematuras a celdas 5G NR n78 (3.5 GHz) seguidas de desconexión inmediata por desvanecimiento de señal.
> 
> 2. **¿Qué herramientas y contadores utilicé?**
>    - Realicé drive tests continuos con **Nemo Outdoor** y analizadores de señalización de Capa 3 con **Nemo Analyze** y **Actix Analyzer**.
>    - Extraje trazas CTR (Cell Trace Recording) en **Ericsson ENM** y las analicé con **Wireshark** decodificando los mensajes X2AP y RRC.
>    - Monitoreé los contadores `pmEndcSetupAtt`, `pmEndcSetupSucc`, `pmEndcSetupFailEnb`, `pmEndcSetupFailGnb`, `pmEndcRelAbnormalGnbAct` y `pmHoExeSucc`.
> 
> 3. **¿Qué parámetros o funcionalidades modifiqué?**
>    - En `ReportConfigEUtra` (Evento B1 de adición 5G): Elevé el umbral `b1ThresholdRsrp` de -112 dBm a **-105 dBm** para impedir que el UE intentara agregar celdas 5G lejanas en zonas de cobertura marginal; y aumenté el temporizador `timeToTriggerB1` de 80 ms a **160 ms** para asegurar estabilidad de radio antes de emitir el reporte de medición.
>    - En `EUtranCellRelation` (Movilidad de celdas ancla LTE): Reduje `a3offset` de 3.0 dB a **1.5 dB** y disminuí `timeToTrigger` de 320 ms a **100 ms** en las celdas directas del corredor vial para acelerar el handover del ancla LTE y prevenir caídas por 'Late Handover'.
>    - En `UeMeasControl`: Ajusté el filtro L3 `filterCoefficientRSRP` a valor 4 para suavizar variaciones rápidas por velocidad vehicular.
>    - Reconfiguré B66 como la banda de anclaje prioritaria para EN-DC sobre B2 mediante las prioridades de ancla en la Baseband.
> 
> 4. **¿Cuál fue mi contribución personal?**
>    - Correlacioné las estampas de tiempo de los archivos de drive test con las trazas de señalización X2AP en ENM, descubriendo que la causa raíz era que el eNodeB intentaba la adición 5G justo en el momento en que el ancla LTE estaba perdiendo señal antes de completar su propio handover A3.
>    - Diseñé el nuevo plan de parámetros de movilidad LTE/NR para el corredor de 25 km; generé los scripts de Moshell; lideré la ejecución del cambio en ventana nocturna; y efectué el drive test de verificación final.
> 
> 5. **¿Cuál fue el resultado final medible?**
>    - La tasa de éxito de adición SgNB aumentó de 85.2% a **98.7%** (+13.5% de mejora).
>    - La tasa de caídas de sesiones 5G se redujo de 3.9% a **0.58%**.
>    - Las sesiones continuas de streaming y datos 5G sin interrupción a lo largo de los 25 km de autopista se incrementaron en más de un **+60%**."*

---

### Pregunta 40: Experiencia Práctica – Caso 3: Resolución de Causa Raíz de Interferencia (RTWP/PIM) y Mejora de Throughput (2022–2026)
*(Practical Case 3: Root Cause Resolution of Uplink Interference / PIM & Throughput Recovery)*

#### 🎯 Estrategia y Enfoque Senior:
- Presenta un caso de alto nivel técnico donde la causa del problema combinó análisis estadístico forense, diagnóstico diferencial de PIM y resolución física y lógica de radio.
- Responde estrictamente las 5 preguntas requeridas con métricas concretas.

#### 💬 Respuesta Modelo para Teleprompter:
> *"En otro proyecto clave de optimización en red Ericsson entre 2022 y 2026, enfrenté y resolví una degradación crítica de interferencia en subida y colapso de throughput en el distrito financiero central de la ciudad:
> 
> 1. **¿Cuál era el problema inicial?**
>    - Cuatro sectores macro que brindaban servicio a oficinas corporativas y centros bancarios sufrieron un incremento súbito de interferencia de subida: el nivel de **RTWP** se disparó a **-86 dBm**, más de 17 dB por encima del piso térmico normal de -104 dBm.
>    - El throughput promedio de subida colapsó a menos de **1.2 Mbps**, la tasa de caídas de E-RAB subió a **2.1%** y la accesibilidad RRC se degradó a **95.8%**, generando quejas directas de clientes corporativos por videollamadas congeladas.
> 
> 2. **¿Qué herramientas y contadores utilicé?**
>    - Monitoreé en tiempo real con **Moshell / AMOS** utilizando comandos `pmx -kpi` y `kpiget`.
>    - Utilicé **Ericsson ENM** para alarmas y contadores históricos; y en campo coordiné el uso de analizadores **Anritsu Site Master** para barrido de VSWR, Return Loss y pruebas de Intermodulación Pasiva (PIM).
>    - Contadores analizados: `pmInterferencePwrReport` (desglosado por rama RXA y RXB), `pmRadioTxPower`, `pmPrbUtilUl`, `pmErabRelAbnormalEnbActUeLost` y `pmRrcConnEstabFail`.
> 
> 3. **¿Qué parámetros o acciones ejecuté?**
>    - **Diagnóstico Diferencial:** Demostré que el RTWP se elevaba en sincronía milimétrica con el tráfico de bajada `pmRadioTxPower`, confirmando **PIM Pasivo Interno** y descartando interferencia externa.
>    - **Intervención Física:** Despaché cuadrilla técnica a torre con orden de trabajo específica. Se detectaron 2 conectores 7/16 DIN oxidados y con torque flojo en la bajante de radio, además de un soporte metálico sulfatado que generaba intermodulación armónica de 3er orden ($2f_1 - f_2$) cayendo directo en la banda de recepción. Se reemplazaron jumpers, se sellaron herméticamente y se aplicó torque de 28 Nm con torquímetro calibrado.
>    - **Ajustes Lógicos en Radio:**
>      - Temporalmente elevé `pZeroNominalPucch` de -106 dBm a **-98 dBm** para permitir que los terminales superaran el piso de ruido transitorio mientras se completaban los trabajos en torre.
>      - Ajusté el tilt eléctrico RET (`electricalAntennaTilt`) de 2° a **4°** en el sector adyacente para eliminar pilot pollution y reducir el solapamiento de señales en la zona afectada.
> 
> 4. **¿Cuál fue mi contribución personal?**
>    - Lideré el análisis forense correlacionando la potencia transmitida con la interferencia recibida para aislar inequívocamente la causa PIM sin perder tiempo buscando jammers inexistentes.
>    - Emití la orden de despacho técnico con las especificaciones exactas del sector; supervisé los trabajos de campo; reconfiguré los parámetros en Moshell; y efectué el monitoreo de 72 horas para confirmar la solución definitiva.
> 
> 5. **¿Cuál fue el resultado final medible?**
>    - El nivel de RTWP se normalizó de -86 dBm a **-103.8 dBm** (piso de ruido perfectamente limpio).
>    - El throughput promedio de subida aumentó en un **+260%** (subiendo de 1.2 Mbps a **4.3 Mbps**).
>    - La accesibilidad RRC se restableció a un impecable **99.85%**.
>    - La tasa de caídas de llamadas E-RAB descendió de 2.1% a **0.31%**, recuperando los SLAs comprometidos con el cliente."*

---

### Pregunta 41: Recomendaciones Finales y Metodología Estratégica para la Entrevista Técnica Senior
*(Final Recommendations, Hands-On Delivery Mindset & Strategic Interview Methodology)*

#### 🎯 Estrategia y Enfoque Senior:
- Guía táctica interna para Javier Viveros Huesca sobre cómo comunicarse con autoridad, convicción y liderazgo técnico durante la entrevista con los ingenieros de Amdocs y Ericsson.

#### 💬 Respuesta Modelo para Teleprompter:
> *"Para proyectar la máxima autoridad técnica y cerrar con éxito la evaluación como Senior RF Optimization Engineer, aplico las siguientes cinco directrices estratégicas:
> 
> 1. **Voz Activa y Autoridad 'Hands-On' (Manos a la Obra):**
>    - Hablo siempre en primera persona del singular: *"Yo analicé los contadores...", "Yo identifiqué la correlación en ENIQ...", "Yo redacté el script en Moshell...", "Yo diseñé la ventana de mantenimiento..."*.
>    - Evito explicaciones abstractas de manual o de libro de texto; cada concepto teórico lo aterrizo de inmediato con un caso real de campo, un parámetro de Ericsson o un comando de consola.
> 
> 2. **Enfoque Temporal Específico (Noviembre 2022 a Octubre 2026):**
>    - Enfatizo mi involucramiento continuo en tecnologías Ericsson 4G LTE y 5G NR durante los últimos 4 años: optimización de releases de software L20/L21/L22, plataformas Baseband 6630/6648, antenas AIR 6449 para n78, despliegues EN-DC y C-RAN.
>    - Esto demuestra vigencia tecnológica absoluta y familiaridad inmediata con los problemas actuales de las redes en producción.
> 
> 3. **Estructura de Respuesta Directa y Concisa:**
>    - Comienzo siempre con una definición ejecutiva de 2 oraciones que responde con exactitud a la pregunta.
>    - Desarrollo 2 o 3 puntos técnicos específicos mencionando parámetros y Managed Objects (MOs) del MOM.
>    - Concluyo con una métrica cuantificada de impacto en el negocio (porcentajes de mejora, dB, Mbps o reducción de DCR).
> 
> 4. **Metodología Forense cuando no se recuerda un parámetro exacto:**
>    - Si el entrevistador pregunta por un contador o parámetro sumamente oscuro cuyo nombre literal no tengo en memoria, jamás titubeo ni adivino: explico mi **metodología de deducción sistemática**:
>      - *"No tengo presente el mnemónico exacto de ese atributo de memoria, pero en Moshell lo localizo de inmediato ejecutando `get EUtranCellFDD <palabra_clave>` o revisando el MOM con `lt all`. Metodológicamente, para resolver ese problema evalúo primero las alarmas activas (`alt`), audito los contadores de acceso y caídas en ENIQ, analizo trazas de capa 3 CTR/UETR para aislar el mensaje de fallo, y aplico la corrección con punto de restauración `cvcu`."*
>    - Los paneles técnicos senior valoran infinitamente más la solidez del criterio analítico de causa raíz que la memorización estéril de manuales.
> 
> 5. **Cierre Estratégico Proactivo:**
>    - Al final de la entrevista, aprovecho la oportunidad de preguntas para demostrar visión de negocio y liderazgo: pregunto sobre el release actual del cliente en México, los retos específicos de interoperabilidad en el clúster asignado y los objetivos clave para el primer trimestre."*

---

# MÓDULO 12: GUÍA DE FLUIDEZ EN INGLÉS TÉCNICO, PRONUNCIACIÓN Y FRASES DE TRANSICIÓN

### Pregunta 42: Guía de Pronunciación Fonética de Términos de Telecomunicaciones
*(Telecom Terminology Pronunciation Cheat Sheet)*

#### 🎯 Estrategia y Enfoque Senior:
- Muchos hispanohablantes tienen acento comprensible pero tropiezan con palabras técnicas clave. Esta tabla fonética ayuda a pronunciar términos con soltura y seguridad nativa.

#### 💬 Respuesta Modelo para Teleprompter:
> *"Para proyectar máxima autoridad en llamadas con clientes en inglés, cuido la pronunciación exacta de estos 10 términos técnicos de uso diario:*
> 
> 1. **Throughput:** /ˈθruːˌpʊt/ (*'THROO-put'*, con 'th' suave y 'u' corta).
> 2. **Retainability:** /rɪˌteɪ.nəˈbɪl.ə.ti/ (*'ree-tay-nuh-BILL-uh-tee'*).
> 3. **Hysteresis:** /ˌhɪs.təˈriː.sɪs/ (*'hiss-tuh-REE-sis'*).
> 4. **Azimuth:** /ˈæz.ɪ.məθ/ (*'AZ-ih-muth'*).
> 5. **Interference:** /ˌɪn.təˈfɪə.rəns/ (*'in-ter-FEER-ens'*).
> 6. **Carrier Aggregation:** /ˈkær.i.ər ˌæɡ.rɪˈɡeɪ.ʃən/ (*'KARE-ee-er ag-rih-GAY-shun'*).
> 7. **Beamforming:** /ˈbiːmˌfɔː.mɪŋ/ (*'BEEM-for-ming'*).
> 8. **Hierarchy:** /ˈhaɪə.rɑː.ki/ (*'HY-er-ar-kee'*).
> 9. **Discrepancy:** /dɪˈskrep.ən.si/ (*'dih-SKREP-uhn-see'*).
> 10. **Rollback:** /ˈroʊl.bæk/ (*'ROHL-bak'*)."*

---

### Pregunta 43: Frases Estratégicas de Transición en Inglés (Cómo Ganar 3 Segundos para Pensar)
*(Strategic Transition Phrases: How to Buy 3 Seconds to Formulate Answers)*

#### 🎯 Estrategia y Enfoque Senior:
- Si el entrevistador formula una pregunta compleja y requieres 3 segundos para organizar mentalmente la respuesta, **nunca te quedes en silencio ni digas 'ehhh...'**. Utiliza una de estas frases de transición nativas:

#### 💬 Respuesta Modelo para Teleprompter:
> *"Utilizo estas frases de transición naturales para ganar tiempo mientras estructuro mi respuesta:*
> - *"That is a very practical operational question. Let me walk you through how I approach this systematically..."* (Esa es una pregunta operativa muy práctica. Permíteme explicarte cómo abordo esto sistemáticamente...)
> - *"Looking at that scenario from both an RF physical layer and a signaling protocol perspective..."* (Mirando ese escenario tanto desde la capa física de RF como desde el protocolo de señalización...)
> - *"In the Ericsson MOM architecture, we typically isolate that issue by checking three distinct layers..."* (En la arquitectura MOM de Ericsson, típicamente aislamos ese problema verificando tres capas distintas...)
> - *"In my previous experience handling similar KPI degradations, the first step was always..."* (En mi experiencia previa resolviendo degradaciones similares de KPI, el primer paso siempre fue...)
> - *"To answer that accurately, we have to distinguish between an RF coverage limitation versus an admission control bottleneck..."* (Para responder eso con exactitud, debemos distinguir entre una limitación de cobertura RF y un cuello de botella de control de admisión...)"*

---
