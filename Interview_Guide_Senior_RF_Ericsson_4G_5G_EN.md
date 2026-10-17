# MASTER TECHNICAL INTERVIEW PREPARATION GUIDE
## POSITION: SENIOR RF OPTIMIZATION ENGINEER – ERICSSON 4G/5G
**Candidate:** Javier Viveros Huesca  
**Client / Project:** AMDOCS MX (Tier-1 Mobile Carrier Operations in Mexico)  
**Agency:** Link Consulting Services  
**Target Technologies:** Ericsson LTE (4G) & 5G NR (NSA / Option 3x)  
**Core Domain:** RAN Configuration, KPI Performance Forensics & RF Optimization  

---

## 📌 CANDIDATE TECHNICAL PROFILE & INTERVIEW STRATEGY
- **Candidate Name:** Javier Viveros Huesca
- **Experience:** Over 14 years of carrier-grade telecommunications experience in Mexico (Nextel Mexico 2011–2013, AT&T Mexico 2013–2022).
- **Daily Toolchain:** Ericsson ENM, Ericsson ENIQ / PM, moshell / amos, CNA / Bulk CM, TEMS / Nemo, Python, SQL, Power BI.
- **Core Specialization:** Root Cause Analysis (RCA) of degraded KPIs, Ericsson MOM parameter auditing, MOP scripting for maintenance windows, and end-to-end optimization of 4G LTE and 5G NSA (EN-DC).
- **Rate & Availability:** USD 3,000 / month, available for immediate on-site/remote integration in Mexico City.

---

# MODULE 1: PROFESSIONAL PROFILE, ELEVATOR PITCH & STRATEGY

### Question 1: "Tell me about yourself, your background, and your hands-on experience with Ericsson 4G and 5G NR networks."

#### 🎯 Strategy & Delivery:
Deliver a confident, authoritative response. You have 14+ years in major carrier operations (Nextel and AT&T Mexico). Emphasize that you are a hands-on engineer who operates ENM, moshell at the node level, analyzes Layer 3 traces, masters Ericsson's Managed Object Model (MOM), and automates engineering workflows with Python and SQL.

#### 💬 Model Answer (Word-for-Word Delivery):
> *"Thank you very much. My name is Javier Viveros Huesca. I am a Senior RF Optimization and RAN Performance Engineer with over 14 years of carrier-grade experience across Tier-1 mobile networks in Mexico, having spent nearly a decade at AT&T Mexico and earlier at Nextel.*
> 
> *Throughout my career, I have specialized deeply in the Ericsson RAN ecosystem—from legacy software releases up through L20, L21, and L22—covering both LTE 4G and 5G NR deployments in Non-Standalone Option 3x (EN-DC) architecture.*
> 
> *My day-to-day work centers on rigorous performance engineering: auditing and tuning RAN parameters via Ericsson ENM, conducting deep-dive forensics using moshell and amos at the node level, extracting high-volume performance counters in Ericsson ENIQ, and troubleshooting all five key performance pillars: Accessibility, Retainability, Mobility, Integrity/Throughput, and Availability.*
> 
> *In addition, a key differentiator of my profile is my engineering automation capability: I develop custom Python scripts and advanced SQL queries to correlate PM counters, rank Top Worst Cells by failure volume, and execute statistically robust Pre- and Post-optimization evaluations in minutes. I am fully prepared to integrate immediately into the Amdocs MX team and deliver impact from day one."*

---

### Question 2: "Why do you want to join this Amdocs MX project and what immediate value will you bring?"

#### 🎯 Strategy:
Show that you understand Amdocs' critical role as a global telecom integrator and the stringent SLAs required by Mexican operators. Emphasize zero learning curve and instant autonomy.

#### 💬 Model Answer:
> *"Amdocs has a world-class reputation in managing complex telecom network transformations and mission-critical carrier operations. I am very familiar with the high standards and aggressive SLAs that Mexican operators expect from Amdocs-led projects.*
> 
> *The immediate value I bring to this project is threefold:*
> 1. **Zero Technical Ramp-Up Time:** I already possess complete mastery of Ericsson's architecture, MOM parameters, ENM/ENIQ toolchain, and moshell CLI, meaning I can take ownership of degraded clusters immediately without needing supervision.
> 2. **Proven RCA Methodology:** I know how to quickly isolate whether a KPI degradation stems from physical RF issues (interferers, PIM, tilts, overshooting), logical parameter discrepancies, transport S1/X2 packet loss, or admission control bottlenecks.
> 3. **Automation & Speed:** My background in automating data workflows with Python and building telemetry dashboards in Power BI will accelerate technical reporting, cluster acceptance audits, and MOP validation for Amdocs stakeholders."*

---

### Question 3: "What is your day-to-day workflow when troubleshooting degraded clusters or Top Worst Cells?"

#### 🎯 Strategy:
The interviewer wants to confirm that you follow a structured engineering workflow rather than randomly tweaking parameters. Walk through your 6-step diagnostic protocol.

#### 💬 Model Answer:
> *"I always follow a structured, hypothesis-driven methodology moving from physical infrastructure to logical configuration:*
> 1. **Fault Management & Alarms (FM):** First, I check ENM for active hardware alarms on the Baseband or Radio Units, optical SFP link degradation (`cabx`), VSWR impedance mismatches, or clock synchronization loss (PTP/GPS). You cannot fix broken hardware with software parameters.
> 2. **Capacity & Admission Analysis:** I check downlink and uplink PRB utilization, active RRC connected user counts, and Baseband license limits to detect traffic congestion.
> 3. **Configuration & Change Audit (CM):** I verify recent software releases, feature activations, or parameter scripts executed during previous maintenance windows against our Golden Baseline to detect configuration drifts.
> 4. **PM Counter Forensics (ENIQ / moshell):** I drill down into specific failure sub-counters. For example, on dropped calls, I isolate whether the primary failure trigger is radio link loss (`UeLost`), handover execution failure (`Ho`), or transport drop (`TransportLost`).
> 5. **RF Quality & Spatial Dominance:** I evaluate uplink interference (RSSI histograms), RSRP/RSRQ distributions, and Timing Advance (TA) profiles to identify cell overshooting, pilot pollution, and boundary overlaps.
> 6. **MOP Implementation & Validation:** I engineer the parameter change script with full rollback capability, schedule execution during approved maintenance windows, and track hourly and busy-hour KPI recovery over the subsequent 24 to 72 hours."*

---

# MODULE 2: ERICSSON ECOSYSTEM, OSS/ENM TOOLS & HARDWARE

### Question 4: "What Ericsson tools do you use daily and what is your level of proficiency in ENM, ENIQ, and moshell?"

#### 💬 Model Answer:
> *"I work daily across the full Ericsson operational software suite:*
> - **Ericsson ENM (Ericsson Network Manager):** I regularly use Alarm Monitor for real-time fault management, Bulk Configuration (CNA / CLI cmedit) for multi-site script rollouts, Topology Browser, and Trace Manager to capture Layer 3 call traces (CTR and UETR).
> - **Ericsson ENIQ / PM:** This is my primary tool for historical performance analysis. I use it to extract high-volume counter data across nodes and clusters, build customized Busy Hour formulas, track weekly KPI trends, and perform cluster acceptance audits.
> - **Moshell / Amos:** I have advanced hands-on CLI proficiency. I connect directly to eNodeB and gNodeB nodes to perform live forensics, query parameters (`get`), inspect hardware inventories (`inv`), audit optical transceiver health (`cabx`), monitor real-time KPIs (`kpiget`, `pmx`), and execute verified MOP scripts with automated rollback protection (`pcr`, `cvcu`)."*

---

### Question 5: "What are the essential moshell/amos commands you use to audit, troubleshoot, and tune parameters?"

#### 💬 Quick Reference Table of Essential Moshell Commands:

| Moshell Command | Technical Purpose & Operational Use Case |
| :--- | :--- |
| `lt all` or `lt cmedit` | Loads the complete Managed Object Model (MOM) into session memory for live inspection and parameter manipulation. |
| `get EUtranCellFDD <param>` | Queries configuration parameters on LTE cells (e.g., `get EUtranCellFDD a3offset`, `cellRange`, `qRxLevMin`). |
| `set <MO> <param> <value>` | Modifies a specific parameter on a targeted Managed Object instance. |
| `bl / deb <MO>` | Administratively blocks (`bl`) or de-blocks (`deb`) cells, sectors, or radio units during maintenance. |
| `inv` | Displays the complete hardware inventory (board revisions, serial numbers for Baseband and Radio units). |
| `lhsh 000100` / `lh` | Executes low-level board diagnostics and processor health checks directly on specific Baseband hardware modules. |
| `cabx` | Audits optical CPRI/eCPRI fiber links, SFP transceiver levels, optical transmit/receive power, and link errors. |
| `kpiget` / `pmx -kpi` | Extracts real-time performance counters and live KPI calculations directly from the active node. |
| `ue print -ad` | Displays active connected UE sessions in real-time with RSRP, SINR, CQI, modulation rank, and throughput data. |
| `cvcu` / `cvls` | Creates configuration version backups prior to parameter deployment (`cvcu "Pre_Tune"`) and lists existing backups. |
| `pcr <script.mos>` | Executes automated moshell batch command scripts with full session logging. |

---

### Question 6: "How is the Ericsson Managed Object Model (MOM) structured for 4G LTE and 5G NR?"

#### 💬 Model Answer:
> *"The Ericsson MOM is a structured object-oriented hierarchy representing the physical and logical layers of the radio network:*
> - **In 4G LTE:**
>   - `ManagedElement`: The root node representing the physical eNodeB.
>   - `ENodeBFunction`: The logical eNodeB entity holding global radio network configurations.
>   - `EUtranCellFDD` / `EUtranCellTDD`: Represents the individual radio cell, controlling carrier frequency (`earfcn`), channel bandwidth, cell range (`cellRange`), maximum output power (`partOfSectorPower`), and access thresholds (`qRxLevMin`).
>   - `EUtranCellRelation`: Defines neighbor relationships between LTE cells, holding handover offsets (`cellIndividualOffset`, `qOffsetCell`) and mobility flags (`isHoAllowed`).
>   - `UtranCellRelation` / `GeranCellRelation`: Managed objects for inter-RAT neighbor relationships toward 3G (WCDMA) or 2G.
>   - `EUtranFreqRelation`: Defines inter-frequency measurement and cell reselection criteria (`cellReselectionPriority`, `threshXHigh`, `threshXLow`).
> - **In 5G NR (CU/DU Disaggregated Architecture):**
>   - `GNBDUFunction`: The Distributed Unit function controlling RLC, MAC, and Physical layer processing.
>   - `NRCellDU`: The physical 5G cell under the DU, holding RF channel bandwidth, SSB beam configurations, and PRACH settings.
>   - `GNBCUCPFunction`: The Central Unit Control Plane function managing RRC connection handling and PDCP control.
>   - `NRCellCU`: Represents the cell entity at the CU control-plane layer.
>   - `TermPointToEnb` / `TermPointToGnb`: Termination points for inter-node signaling links over X2 (LTE-NR for NSA) or Xn (NR-NR for SA)."*

---

### Question 7: "What is your experience with Ericsson hardware (Baseband 5216/6630/6648, Radios 4415/2219, AIR 6449/3268) and how do you diagnose physical or transport faults?"

#### 💬 Model Answer:
> *"I have extensive experience spanning multiple hardware generations:*
> - **Basebands:** From legacy DUL/DUS boards to Baseband 5216, Baseband 6630, and high-capacity 5G Baseband 6648. I use `lhsh` to inspect processor load, board memory, and inter-board CPRI/eCPRI interconnections.
> - **Radios & Massive MIMO:** Experience with multi-band remote radios such as Radio 4415 (4T4R) and Radio 2219 (2T2R), as well as integrated Massive MIMO antenna units like AIR 6449 (64T64R) and AIR 3268 (32T32R) operating in band n78 (3.5 GHz).
> - **Fronthaul & VSWR Troubleshooting:**
>   - Using `cabx` in moshell, I audit optical transceiver metrics. If Rx optical power on an SFP drops below -15 dBm, it indicates severe fiber bending, contamination, or a failing transceiver.
>   - For VSWR alarms (Return Loss < 15 dB), I evaluate whether power reflections are causing passive intermodulation (PIM) and Uplink sensitivity degradation, coordinating tower climbs to re-terminate jumpers or torque coaxial connectors."*

---

# MODULE 3: IN-DEPTH KPI FORENSICS & TROUBLESHOOTING (THE 5 PILLARS)

### Question 8: "PILLAR 1 - ACCESSIBILITY: What are the key formulas, failure counters, and troubleshooting steps for RRC, E-RAB, and 5G SgNB addition failures?"

#### 💬 Key Formulas & PM Counters:
> **1. RRC Connection Setup Success Rate (RRC Setup SR):**
> $$	ext{RRC Setup SR} = rac{	ext{pmRrcConnEstabSucc}}{	ext{pmRrcConnEstabAtt}} 	imes 100\%$$
> *(Tracked separately for Service Establishment vs Signaling / MoData vs MoSignaling).*
> 
> **2. E-RAB Setup Success Rate (E-RAB Setup SR):**
> $$	ext{E-RAB Setup SR} = rac{	ext{pmErabEstabSuccInit} + 	ext{pmErabEstabSuccAdded}}{	ext{pmErabEstabAttInit} + 	ext{pmErabEstabAttAdded}} 	imes 100\%$$
> *(Crucially analyzed by QCI: QCI 1 for VoLTE voice and QCI 9 for best-effort mobile broadband).*
> 
> **3. Call Setup Success Rate (CSSR):**
> $$	ext{CSSR} = 	ext{RRC Setup SR} 	imes 	ext{E-RAB Setup SR}$$
> 
> **4. 5G NSA SgNB Addition Success Rate:**
> $$	ext{SgNB Addition SR} = rac{	ext{pmEndcSetupSucc}}{	ext{pmEndcSetupAtt}} 	imes 100\%$$

#### 🔍 Root Cause Analysis Protocol for Accessibility:
> *"When accessibility KPIs degrade, I follow a systematic decision tree:*
> 1. **If RRC Setup Fails:**
>    - **Uplink Interference / High RSSI:** If average UL RSSI rises from -115 dBm to worse than -95 dBm, incoming PRACH preambles are drowned out by the noise floor. Root causes: External RF interferers or PIM.
>    - **PRACH / PUCCH Congestion:** Check for preamble collisions due to high user density or exhausted PUCCH resource grants (`pucchDedicated`).
>    - **Admission Control Rejections:** The node rejects connection attempts if active RRC user licenses on the Baseband or physical PRB thresholds are exceeded.
> 2. **If E-RAB Setup Fails:**
>    - This typically points to transport issues on the S1-MME interface (SCTP packet drops or excessive latency) or core network rejections due to QoS profile mismatches or authentication timeouts.
> 3. **If 5G SgNB Addition Fails:**
>    - Audit the X2-C interface between the eNodeB and gNodeB: packet loss or routing delays cause the `SgNB Addition Request` timer to expire before the gNodeB can reserve resources and acknowledge."*

#### 🛠️ Key Accessibility Parameters:
- `prachConfigurationIndex`: Sets PRACH preamble periodicity, timing, and density.
- `rootSequenceIndex`: Logical root sequence for PRACH preambles (must be audited to prevent neighbor cell collisions).
- `pZeroNominalPucch` & `pZeroNominalPusch`: Nominal uplink power target to overcome the uplink noise floor.
- `cellRange`: Maximum cell radius. UEs attempting access beyond this distance are rejected by timing advance limits.

---

### Question 9: "PILLAR 2 - RETAINABILITY: How do you troubleshoot E-RAB Drop Rate for VoLTE (QCI 1) and Data (QCI 9), and how do you differentiate RF drops from Transport drops?"

#### 💬 Key Formulas & PM Counters:
> $$	ext{E-RAB Drop Rate} = rac{	ext{pmErabRelAbnormalEnb} + 	ext{pmErabRelAbnormalMme}}{	ext{pmErabRelNormalEnb} + 	ext{pmErabRelAbnormalEnb} + 	ext{pmErabRelAbnormalMme}} 	imes 100\%$$
> 
> For VoLTE (QCI 1):
> $$	ext{VoLTE Drop Rate} = rac{	ext{pmErabRelAbnormalEnbActQci1}}{	ext{pmErabRelNormalEnbQci1} + 	ext{pmErabRelAbnormalEnbActQci1}} 	imes 100\%$$

#### 🔍 Forensics: Isolating Drop Root Causes:
> *"I isolate the exact failure mechanism by breaking down Ericsson's abnormal release sub-counters:*
> - **Radio Link Failures (RF Loss - `UeLost`):**
>   - Counter: `pmErabRelAbnormalEnbActUeLost`.
>   - Cause: Expiration of timer **T310** (UE receives N310 consecutive 'out-of-sync' indications from physical layer and fails to recover). Typically caused by weak coverage at cell edges, fast fading in urban canyons, or severe pilot pollution (SINR < -5 dB with multiple overlapping non-dominant servers).
> - **Handover Execution Failures (`Ho` Drops):**
>   - Counter: `pmErabRelAbnormalEnbActHo`.
>   - Cause: Handover commands sent too late into the boundary (Late Handover), target cell admission rejection, or missing neighbor relations where the UE runs out of coverage before completing target RACH (expiration of **T304**).
> - **Transport & Core Network Losses (`TransportLost` / `CoreRelease`):**
>   - Counter: `pmErabRelAbnormalEnbActTransportLost`.
>   - Cause: If an IP backhaul link, IPsec tunnel, or S1-U GTP tunnel experiences a micro-outage or packet loss burst, the eNodeB triggers mass abnormal teardowns across all active bearers simultaneously. It affects all sectors on the site concurrently."*

#### 🛠️ Retainability Optimization Actions:
1. **Antenna Tilt Engineering (RET):** Down-tilt overshooting macro cells to pull back extended coverage lobes and eliminate pilot pollution.
2. **Neighbor Relation Audits (ANR):** Ensure 100% reciprocal neighbor definitions in `EUtranCellRelation`; missing neighbors in overlap zones guarantee drops.
3. **Radio Link Timer Tuning:** Tune `t310` (e.g., from 1000ms to 2000ms in fast-shadowing environments) and constants `n310`/`n311` to increase link resilience.

---

### Question 10: "PILLAR 3 - MOBILITY: Explain 3GPP Handover events (A1 to A5, B1, B2) and how you resolve Late Handover and Ping-Pong issues."

#### 💬 3GPP Mobility Measurement Events in Ericsson RAN:

| Event | 3GPP Trigger Condition | Typical Operational Use Case in Ericsson |
| :---: | :--- | :--- |
| **A1** | Serving cell becomes better than absolute threshold (`a1Threshold`). | Stops inter-frequency/inter-RAT measurements to conserve UE battery when serving coverage is optimal. |
| **A2** | Serving cell becomes worse than absolute threshold (`a2Threshold`). | Activates inter-frequency or inter-RAT search measurements as the UE enters marginal coverage. |
| **A3** | Neighbor becomes offset better than serving: $RSRP_{neighbor} > RSRP_{serving} + a3offset$. | **Primary trigger for Intra-frequency handover** and co-layer inter-frequency handover. |
| **A4** | Neighbor becomes better than absolute threshold. | Used for discovering secondary carrier layers and triggering Carrier Aggregation SCell addition. |
| **A5** | Serving worse than Thresh 1 **AND** Neighbor better than Thresh 2. | **Coverage-based inter-frequency handover** from high-capacity capacity layers (B4/B2) to coverage layers (B28/700MHz). |
| **B1** | Inter-RAT neighbor becomes better than absolute threshold. | **Critical for 5G NSA:** Detects 5G NR signal presence to trigger Secondary Node Addition (SgNB Addition). |
| **B2** | Serving LTE worse than Thresh 1 **AND** Inter-RAT neighbor better than Thresh 2. | Triggers fallback/redirection to 3G WCDMA when LTE coverage is entirely lost. |

#### 🔍 Resolving Mobility Anomalies:
> - **Late Handover (UE drops before receiving handover command):**
>   - **Symptoms:** Layer 3 traces show serving RSRP collapsing rapidly (-120 dBm) and high UL BLER before `RRCConnectionReconfiguration (MobilityControlInfo)` can be delivered.
>   - **Solution:** Reduce `timeToTrigger` (TTT) from 320ms to 160ms or 100ms, and decrease `a3offset` from 3 dB to 1.5–2 dB to accelerate handover execution.
> - **Ping-Pong Handover (UE rapidly oscillates between adjacent cells):**
>   - **Symptoms:** High handover attempt volume with session dwell times under 3 seconds between Cell A and Cell B.
>   - **Solution:** Increase `hysteresisA3` (e.g., from 1 dB to 2–3 dB) and/or increase `timeToTrigger`. For macro-to-small-cell boundaries, apply a positive `cellIndividualOffset` (CIO) toward the preferred capacity layer."*

---

### Question 11: "PILLAR 4 - INTEGRITY & THROUGHPUT: What factors degrade DL/UL User Throughput and how do you optimize them?"

#### 💬 Metrics, Breakdown & Optimization:
> *"User perceived throughput is a function of bandwidth, channel quality, spectral efficiency, and scheduling:*
> 
> $$	ext{Throughput} pprox 	ext{PRB Bandwidth} 	imes 	ext{Spectral Efficiency (MCS)} 	imes (1 - 	ext{BLER}) 	imes 	ext{MIMO Rank}$$
> 
> **Degradation Root Causes:**
> 1. **Poor RF Channel Quality (Low SINR / High BLER):**
>    - When SINR drops below 0 dB, link adaptation downshifts modulation from 256QAM or 64QAM to 16QAM or QPSK, drastically lowering the Modulation and Coding Scheme (MCS).
>    - Monitor **BLER (Block Error Rate)**; closed-loop target is 10% on initial transmission. Residual BLER > 2% indicates packet discard and continuous HARQ retransmissions.
> 2. **Capacity Congestion (High PRB Utilization):**
>    - When DL PRB utilization exceeds 80% during busy hours, available resource blocks are divided among dozens of active UEs, dropping individual user throughput to < 2–5 Mbps.
> 3. **MIMO Rank Collapse (Low Rank Indicator - RI):**
>    - Lack of spatial scattering or antenna cross-polarization degradation causes the system to drop from Rank 2 or Rank 4 to Rank 1 (SISO/diversity), reducing theoretical peak throughput by 50% to 75%.
> 4. **Transport / Backhaul Bottlenecks:**
>    - Transmission bandwidth throttling or MTU size mismatches between the eNodeB and IP core constrain data rates regardless of pristine RF conditions.
> 
> **Optimization Strategy:**
> - Enable and fine-tune **Carrier Aggregation (CA)** across multiple bands (e.g., AWS + PCS + 700MHz).
> - Configure **Mobility Load Balancing (MLB)** to steer traffic away from heavily congested carriers.
> - Optimize antenna down-tilts and beam patterns to contain interference and push CQI distributions into the 10–15 range."*

---

### Question 12: "PILLAR 5 - AVAILABILITY & SLEEPING CELLS: How do you measure Radio Availability and detect 'Sleeping Cells'?"

#### 💬 Model Answer:
> *"Radio Network Availability is tracked using the standard metric:*
> 
> $$	ext{Cell Availability} = \left( 1 - rac{	ext{Unplanned Outage Time}}{	ext{Total Operational Time}} ight) 	imes 100\%$$
> 
> - **Primary Outage Causes:**
>   - Transmission failures, optical SFP transceiver faults (`cabx`).
>   - Clock synchronization loss (GPS receiver unlock or IEEE 1588v2 PTP packet jitter), which automatically mutes TDD cells to prevent frame collision.
>   - Hardware failure on Radio Units (synthesizer locks, power amplifier faults).
> 
> - **Detecting 'Sleeping Cells':**
>   - **Definition:** A sleeping cell appears operational and 'green' in the Fault Management system (no active alarms, administratively de-blocked), but in reality it carries zero user traffic or fails 100% of access attempts.
>   - **Automated Detection via Python & ENIQ:**
>     - Daily batch audit filtering for cells exhibiting:
>       1. Zero RRC connection attempts (`pmRrcConnEstabAtt = 0`) during daylight hours in historically high-traffic areas.
>       2. Immediate 100% RRC setup drop rate upon access.
>       3. Zero DL/UL PDCP data volume (`pmPdcpVolDlDrb = 0`).
>     - **Resolution:** Access node via moshell, execute administrative lock (`bl`) followed by unlock (`deb`), perform a soft restart or unit restart of the Radio Unit (`lhsh`), check RF transmit power, and replace hardware if the fault persists."*

---

# MODULE 4: 5G NR NSA / EN-DC (OPTION 3X) DEEP DIVE

### Question 13: "How does 5G NSA Option 3x architecture work and what is the role of the LTE anchor cell vs the 5G NR secondary cell?"

#### 💬 Model Answer:
> *"The 5G NSA (Non-Standalone) Option 3x architecture is the industry standard deployed by leading carriers to leverage existing 4G Evolved Packet Core (EPC) infrastructure for rapid 5G rollout:*
> 
> - **Control Plane (C-Plane):** Resides entirely on the **Master eNodeB (MeNB)** in LTE. The eNodeB maintains the S1-MME signaling connection with the MME and manages the terminal's RRC state machine.
> - **User Plane (U-Plane - Split Bearer):** In Option 3x, the S1-U user-plane data interface terminates directly on the **Secondary gNodeB (SgNB)** in 5G NR.
> - **Data Offloading Mechanism:** The gNodeB receives packet data from the S-GW/UPF at the NR-PDCP layer. If 5G radio link conditions are favorable, high-speed data is scheduled directly over 5G NR carriers (NR RLC/MAC/PHY). If the UE moves into fringe 5G coverage, packets can be dynamically split or routed across the X2-U interface to the LTE eNodeB, ensuring continuous session retainability without drops."*

---

### Question 14: "Explain step-by-step the end-to-end signaling flow of SgNB Addition in 5G NSA."

#### 💬 Step-by-Step Signaling Protocol Sequence:
> *"The SgNB Addition procedure follows a strict 10-step sequence in 3GPP and Ericsson implementations:*
> 
> 1. **Initial Attach on LTE Anchor (MeNB):** The UE connects to the LTE anchor cell through standard RRC Connection Setup and registers with the EPC.
> 2. **Measurement Configuration (B1 Event):** The MeNB evaluates the UE's radio capabilities (`EndcAllowed`). If the UE supports EN-DC on the operator's 5G band (e.g., n78), the MeNB issues an `RRCConnectionReconfiguration` configuring **Event B1** with target NR frequency, `b1ThresholdRsrp`, and `timeToTriggerB1`.
> 3. **UE Measurement Report (Event B1):** The UE detects the 5G SSB beam with an RSRP exceeding `b1ThresholdRsrp` continuously for the duration of `timeToTriggerB1`, and transmits a `MeasurementReport (Event B1)` to the LTE eNodeB.
> 4. **Secondary Node Addition Request:** The MeNB transmits an `SgNB Addition Request` message to the candidate 5G gNodeB over the X2-C interface, containing UE capabilities and candidate NR cell IDs.
> 5. **5G Admission Control & Resource Allocation:** The gNodeB checks radio resource availability, Baseband processing capacity, and concurrent EN-DC user licenses.
> 6. **Addition Request Acknowledgement:** The gNodeB sends an `SgNB Addition Request Acknowledge` back to the MeNB over X2-C, containing the transparent NR RRC configuration container for the Primary Secondary Cell (**PSCell**).
> 7. **RRC Reconfiguration toward UE:** The MeNB sends `RRCConnectionReconfiguration` to the UE, encapsulating the 5G NR radio parameters, PRACH configurations, and Secondary Cell Group (SCG) setup.
> 8. **Random Access on 5G NR (PRACH):** The UE performs uplink synchronization by transmitting a PRACH preamble on the assigned PSCell.
> 9. **RRC Reconfiguration Complete:** The UE transmits `RRCConnectionReconfigurationComplete` to the LTE MeNB.
> 10. **Path Switch & Bearer Establishment:** The MeNB confirms completion to the gNodeB via `SgNB Reconfiguration Complete` over X2, and the gNodeB triggers an S1-U path switch with the EPC/S-GW to route downlink user-plane packets directly to 5G."*

---

### Question 15: "What are the most common root causes of 5G NSA SgNB Addition failures and Drops, and how do you resolve them?"

#### 💬 Troubleshooting Matrix for 5G NSA:

| Failure Mode | Common Root Cause in Ericsson RAN | Engineering Resolution |
| :--- | :--- | :--- |
| **Low SgNB Addition Success Rate (X2 Timeout)** | **X2 Transport Bottlenecks:** Packet loss or jitter on the X2-C interface causes the `SgNB Addition Request` timer to expire before the gNodeB acknowledges. | Audit IP backhaul quality, latency, and MTU between eNodeB and gNodeB. Verify `TermPointToGnb` MO availability and SCTP stream health. |
| **Low SgNB Addition Success Rate (gNB Rejection)** | **License or Admission Exhaustion:** The gNodeB rejects addition due to reaching concurrent dual-connectivity license limits or PRB congestion. | Audit admission failure counters on the gNodeB. Expand software licenses or adjust inter-frequency steering thresholds. |
| **Low SgNB Addition Success Rate (PRACH Failure)** | **Uplink Link Budget Limitation (3.5 GHz):** The UE detects adequate DL SSB RSRP, but its maximum 23 dBm uplink output cannot reach the gNodeB during random access. | Tune `b1ThresholdRsrp` to a more conservative level (e.g., from -108 dBm to -102 dBm) so only UEs with robust link margins trigger addition; optimize PRACH preamble power and tilt. |
| **High SgNB Abnormal Release Rate (Drops)** | **LTE vs NR Coverage Mismatch:** Low/mid-band LTE anchor out-penetrates 3.5 GHz mid-band NR. As the UE travels, NR signal collapses rapidly, causing **SCG Failure** (`t310-Expiry`). | Configure timely SCG releases via NR A2 measurement events before unrecoverable radio link loss occurs; optimize Massive MIMO digital tilt and azimuth. |

---

### Question 16: "How do you tune NSA mobility parameters (PSCell change, B1 threshold, SCG failure handling)?"

#### 💬 Model Answer:
> *"NSA mobility optimization revolves around three primary tuning areas:*
> 1. **Calibrating Event B1 (`b1ThresholdRsrp` & `timeToTriggerB1`):**
>    - Setting `b1ThresholdRsrp` too aggressively (e.g., -112 dBm) causes UEs to attach to 5G at extreme cell edges where uplink transmission fails, leading to instant drops.
>    - I tune `b1ThresholdRsrp` between -104 dBm and -100 dBm for 3.5 GHz (n78) to ensure 5G is only added where it delivers a substantial throughput gain over LTE.
> 2. **PSCell Change Optimization:**
>    - For mobility between 5G sectors while anchored to the same LTE cell (Intra-MeNB PSCell Change), we optimize the **NR Event A3** parameters (`a3offset` at 2–3 dB and `timeToTrigger` at 160ms) to ensure smooth sector handover.
> 3. **SCG Failure Handling:**
>    - I ensure the network is configured so that upon an SCG failure (e.g., `synchReconfigFailureSCG` or `t310-Expiry`), the UE does not terminate the call; it transmits an `SCGFailureInformation` message to the LTE eNodeB, gracefully releasing the 5G leg while maintaining uninterrupted session connectivity on LTE."*

---

# MODULE 5: ADVANCED ERICSSON RAN FEATURES

### Question 17: "CARRIER AGGREGATION (CA): How does CA work, what are the key events, and how do you optimize SCell addition and retention?"

#### 💬 Model Answer:
> *"Carrier Aggregation enables the pooling of two or more Component Carriers (CCs) to multiply user bandwidth and peak data rates:*
> 
> - **PCell (Primary Cell):** Manages RRC signaling, NAS connection, PUCCH uplink feedback, and core mobility tracking.
> - **SCell (Secondary Cell):** Additional carriers aggregated purely to augment user-plane downlink/uplink capacity.
> 
> **Key Configuration & Events in Ericsson:**
> 1. **Candidate Cell List (`sCellCandidateList`):** Configured on `EUtranCellFDD` to define allowed aggregation targets.
> 2. **Events A4 and A6:**
>    - **Event A4:** Measures absolute quality of secondary carriers in inter-band configurations (e.g., PCell on B4 and SCell on B2 or B7).
>    - **Event A6:** Measures intra-band intra-frequency neighbor cells that become an offset better than the current serving SCell.
> 3. **Buffer Activation Thresholds:** To prevent unnecessary signaling overhead and battery drain, SCells are not active continuously for idle traffic; they are triggered when data buffer volumes exceed `sCellActDeactDataThreshold`.
> 
> **Performance Tuning:**
> - Ensure reciprocal CA neighbor definitions across all co-located carrier bands.
> - Tune minimum SCell RSRP coverage thresholds to prevent adding secondary carriers with negative SINR that degrade modulation efficiency."*

---

### Question 18: "MASSIVE MIMO & BEAMFORMING: Explain the difference between SSB broadcast beams and CSI-RS traffic beams, and how antenna coverage is optimized on Ericsson AIR units."

#### 💬 Model Answer:
> *"In 5G Massive MIMO deployments (using Ericsson AIR 6449 and AIR 3268 units with 64T64R and 32T32R configurations in band n78):*
> 
> 1. **Synchronization Signal Block (SSB) Broadcast Beams:**
>    - Static or semi-static sector-wide coverage beams transmitting PSS/SSS synchronization signals and PBCH/MIB broadcast info.
>    - In mid-band (3.5 GHz), typically **4 or 8 SSB beams** sweep horizontally and vertically across the sector to guarantee that any device in the coverage area can acquire synchronization.
> 2. **CSI-RS Traffic Beams (User-Specific Beamforming):**
>    - Highly focused, dynamic pencil beams formed digitally in real time.
>    - Utilizing channel reciprocity from Uplink Sounding Reference Signals (SRS), the array steers maximum RF energy directly at the active UE's spatial coordinates, enabling high-order spatial multiplexing (MU-MIMO).
> 
> **Software-Driven Optimization in ENM:**
> - AIR antennas do not require physical climbers for minor adjustments: we adjust **`digitalTilt`** and **`digitalAzimuth`** directly via software parameters in the antenna MO.
> - We select optimized beamforming profiles (`beamformingProfile`) suited to the environment: wide-vertical profiles for urban high-rise corridors or narrow-horizontal profiles for highway macro coverage."*

---

### Question 19: "MOBILITY LOAD BALANCING (MLB): How do you configure load balancing thresholds to relieve congested carriers?"

#### 💬 Model Answer:
> *"Mobility Load Balancing (MLB) redistributes traffic across co-located frequency layers based on real-time radio resource utilization:*
> 
> - **Triggering Metrics:** Downlink/Uplink PRB utilization and active RRC connected user counts.
> - **Key Ericsson Parameters:**
>   - `lbThreshold`: The PRB utilization threshold beyond which a cell is flagged as congested (e.g., 75% or 80%).
>   - `lbActivationThreshold`: The threshold that triggers candidate offloading.
>   - `cellCapacityOffset`: Virtually offsets handover boundaries, making underutilized target cells appear more attractive to UEs.
> - **Steering Mechanisms:** Connected UEs are handed over via load-based inter-frequency handovers, and idle UEs are re-steered using modified cell reselection priorities (`cellReselectionPriority`, `threshXHigh`) in SIB broadcasts."*

---

### Question 20: "DYNAMIC SPECTRUM SHARING (DSS): How does DSS dynamically allocate spectrum between 4G and 5G on the same carrier, and what is its KPI trade-off?"

#### 💬 Model Answer:
> *"DSS allows 4G LTE and 5G NR to operate concurrently within the same frequency carrier (e.g., 20 MHz in AWS B4/n66 or 10 MHz in 700 MHz B28/n28):*
> 
> - **Operating Principle:** Instead of static spectrum refarming, the Baseband scheduler dynamically allocates resource elements in the time and frequency domains on a sub-millisecond basis based on instantaneous traffic demand.
> - **Coexistence Mechanisms:**
>   - **MBSFN Subframes:** LTE configures multicast frames where control signals are omitted, leaving clear time slots for 5G NR transmission.
>   - **Rate Matching around LTE CRS:** 5G NR punches through and routes resource elements around LTE's omnipresent Cell-specific Reference Signals (CRS).
> - **KPI Impact & Trade-offs:**
>   - **Advantage:** Instant nationwide 5G coverage without purchasing new spectrum or decommissioning 4G.
>   - **Trade-off:** Synchronization signals and rate matching create an **overhead penalty of 10% to 20% on LTE capacity**.
>   - **Optimization:** Fine-tune scheduler priorities to protect LTE user experience during peak hours and prioritize steering 5G UEs to dedicated mid-band carriers (n78) whenever available."*

---

# MODULE 6: REAL-WORLD SCENARIOS & ROOT CAUSE ANALYSIS (RCA)

### Question 21: "REAL SCENARIO 1: Following an Ericsson software upgrade (e.g., L19 to L21), VoLTE call drops spike by 35% across an urban cluster. What is your immediate action plan?"

#### 💬 Senior Methodology & Response:
> *"When a sudden degradation occurs immediately following a maintenance window, I take swift, structured action:*
> 
> 1. **Containment & Scope Isolation:**
>    - Check whether the drop spike is confined strictly to upgraded nodes or spans the wider network (to rule out IMS core or S-GW outages).
> 2. **Sub-Counter Forensics:**
>    - Extract detailed QCI 1 abnormal release counters in ENIQ and moshell:
>      - Break down `pmErabRelAbnormalEnbActQci1` by cause: `UeLost` (RF loss), `Ho` (handover execution), `Transport`, or `Core`.
> 3. **Parameter Drift & Default Value Auditing:**
>    - New Ericsson releases often introduce new parameters or modify default settings for Robust Header Compression (RoHC), Unacknowledged Mode (UM) RLC timers, or Smart Inactivity timers.
>    - Run an automated SQL/Python audit comparing configuration parameters of the degraded nodes against the pre-upgrade Golden Baseline.
> 4. **Layer 3 Trace Inspection (UETR / CTR):**
>    - Activate UE Trace Recording (UETR) on the top 5 worst cells. Inspect call teardown signaling: check if drops are triggered by PDCP discard timer expirations or RoHC decompression failures.
> 5. **Remediation or Rollback Execution:**
>    - If an incompatible parameter default is identified, generate a corrective MOP script and deploy immediately across the cluster.
>    - If the issue stems from an unpatched radio firmware defect, initiate an immediate **Rollback** by restoring the previous configuration version (`cvcu` restore) in coordination with the NOC and Ericsson NPI teams."*

---

### Question 22: "REAL SCENARIO 2: A 5G NR n78 (3.5 GHz) cell with 100 MHz bandwidth only delivers 40 Mbps DL throughput during drive tests. How do you troubleshoot?"

#### 💬 Model Answer:
> *"With 100 MHz of bandwidth in n78 (TDD with typical 4:1 or DDDSU pattern), peak DL throughput should readily exceed 800 Mbps to 1 Gbps. A 40 Mbps result indicates a severe bottleneck:*
> 
> 1. **Audit TDD Frame Synchronization (PTP / GPS):**
>    - In 5G TDD networks, any phase or frequency synchronization drift across nodes causes neighboring uplink slots to bleed into downlink slots, destroying co-channel SINR. Verify node clock lock status via `inv` and synchronization event logs.
> 2. **Radio Channel Metrics Forensics (SINR, MCS & Rank):**
>    - Review drive test logs (TEMS/Nemo) or live traces via `ue print -ad`:
>      - **SINR:** If SINR is low (< 5 dB) near the site, suspect severe co-channel interference or cross-beam collision.
>      - **Modulation Scheme:** Check if transmission is stuck in QPSK/16QAM rather than reaching 256QAM.
>      - **MIMO Layers (Rank Indicator):** Check if the UE is restricted to Rank 1 instead of Rank 4 spatial multiplexing.
> 3. **Massive MIMO Beam Configurations:**
>    - Check `digitalTilt` and `digitalAzimuth` settings on the antenna MO. If digital tilt is over-shooting or pointed above ground level, energy misses the street level.
> 4. **Transmission & Backhaul Bandwidth:**
>    - Verify the eCPRI/Ethernet port capacity on the site router. If the backhaul interface is provisioned for 100 Mbps or shared with overloaded transport queues, throughput will cap physically."*

---

### Question 23: "REAL SCENARIO 3: A macro LTE cell shows severe RRC Accessibility degradation (82%) and average UL RSSI of -85 dBm. How do you distinguish external interference from internal PIM?"

#### 💬 Model Answer:
> *"An average RSSI of -85 dBm (compared to a normal noise floor of -115 to -118 dBm) represents more than 30 dB of desensitization:*
> 
> 1. **Correlating RSSI with Traffic Volume to Isolate PIM vs External Interference:**
>    - **Passive Intermodulation (Internal PIM in Antennas/Jumpers):**
>      - PIM is a non-linear effect generated when high-power transmit carriers mix across corroded connectors, oxidized metal, or damaged coaxial jumpers.
>      - **Signature:** Uplink RSSI **correlates directly with Downlink traffic volume and transmit power**. During peak hours (high DL power), RSSI degrades to -85 dBm. In the early morning hours (low DL power), RSSI drops back to normal noise levels (-112 dBm).
>    - **External Interference (Illegal repeaters, rogue jammers, surveillance cameras):**
>      - **Signature:** Interference level is **constant 24 hours a day** (flat line at -85 dBm regardless of traffic load) or follows an external schedule unrelated to mobile network usage.
> 2. **Remediation Actions:**
>    - If PIM: Check VSWR and Return Loss alarms. Dispatch field crews with PIM analyzers to inspect jumpers, re-torque connectors, and replace damaged RF components.
>    - If External: Use ENM RF spectrum analyzer tools to capture spectrograms, perform field hunting with directional antennas, and report the interferer to regulatory authorities (IFT in Mexico).
>    - Immediate Parameter Mitigation: Temporarily increase `pZeroNominalPucch` and `pZeroNominalPusch` to compensate for the elevated noise floor and allow UEs to be decoded."*

---

### Question 24: "REAL SCENARIO 4: Handover Success Rate is only 88% between two adjacent sites along a high-speed avenue. How do you fix it?"

#### 💬 Model Answer:
> *"An 88% HOSR along a high-speed arterial typically stems from Doppler spread, late handovers, or insufficient overlap:*
> 
> 1. **Neighbor Relation & Parameter Audit:**
>    - Verify reciprocal `EUtranCellRelation` entries with `isHoAllowed = TRUE`.
>    - Check for PCI collisions or confusions between surrounding neighbor sites.
> 2. **Tuning Event A3 Handover Triggers:**
>    - At vehicular speeds (80–120 km/h), UEs traverse coverage overlap zones in 1–2 seconds. If `timeToTrigger` (TTT) is set to 320ms or 640ms, the signal collapses before the UE receives the handover command.
>    - Reduce `timeToTrigger` to **100ms** or **80ms**.
>    - Lower `a3offset` from 3 dB to **1.5 dB or 2 dB** to initiate handover preparation earlier.
> 3. **Physical Coverage Realignment:**
>    - Analyze Timing Advance histograms to evaluate coverage overlap depth.
>    - If coverage abruptly drops, reduce electrical tilt (up-tilt by 1 degree) on the serving sector to extend coverage lobes along the road corridor, creating a stable handover zone."*

---

# MODULE 7: PRE- AND POST-OPTIMIZATION METHODOLOGY

### Question 25: "How do you structure a formal Pre-Post analysis to validate KPI gains after feature rollouts or parameter tuning?"

#### 💬 Structured Engineering Protocol:
> *"A rigorous Pre-Post analysis must guarantee statistical validity and eliminate external variables:*
> 
> 1. **Homogeneous Evaluation Windows:**
>    - Establish a **Pre-Baseline** of at least 7 to 14 consecutive days and a matching **Post-Evaluation** window of 7 days, comparing like-for-like days (e.g., Tuesday vs Tuesday) to eliminate weekend/seasonal traffic skews.
> 2. **Busy Hour (BH) Statistical Isolation:**
>    - In addition to 24-hour averages, evaluate performance during the **Network Busy Hour**, where capacity, latency, and accessibility bottlenecks are most pronounced.
> 3. **Traffic Volume Normalization:**
>    - If throughput increases by 10%, verify that traffic did not drop. Total carried payload (`pmPdcpVolDlDrb`) and connected user counts must remain constant or increase for throughput gains to be declared valid.
> 4. **Side-Effect Auditing:**
>    - Verify that boosting one KPI did not degrade another. For instance, increasing cell transmit power must not increase co-channel uplink interference or degrade neighbor handover success rates.
> 5. **Executive Telemetry Reporting:**
>    - Deliver results through delta comparison tables ($\Delta$ KPI) and visual trend curves in Power BI, clearly categorizing accepted cells, neutral cells, and any exceptions requiring localized tuning."*

---

# MODULE 8: BEHAVIORAL & PROJECT MANAGEMENT QUESTIONS (STAR METHOD)

### Question 26: "Tell me about a time when you had to optimize a cluster under tight deadlines and direct client pressure."

#### 💬 STAR Method Response (Situation, Task, Action, Result):
> - **Situation (S):** *"During a network expansion project at AT&T Mexico ahead of a major commercial event, we integrated 85 new LTE sites into a dense urban cluster. Initial performance was failing contractual SLAs: Handover Success Rate was at 89% (target 98%) and VoLTE Accessibility was at 94% (target 99%). The client gave us 5 business days to bring the entire cluster to SLA compliance before applying financial penalties."*
> - **Task (T):** *"As the Senior RF Optimization Engineer, I was tasked with leading the forensic investigation, determining root causes, and executing remediation to restore all KPIs to contractual targets before the deadline."*
> - **Action (A):** *"Rather than auditing 85 sites manually, I developed a Python script connected to the ENIQ database to rank the 'Top Worst Cells' by failure volume (Pareto Principle). The automated analysis revealed two core issues:*
>   1. *18 missing neighbor relations between newly added sites and existing perimeter sites, causing immediate call drops at cell edges.*
>   2. *Severe PRACH root sequence collisions and un-optimized electrical down-tilts on two high-elevation macro sites that were overshooting into neighboring sectors.*
>   *I generated batch moshell scripts to create missing neighbor relations, resolve PCI/PRACH conflicts, and adjust RET down-tilts by 2 degrees. The MOP was executed and verified during the night maintenance window on day three."*
> - **Result (R):** *"Within 72 hours, HOSR rose to 98.6% and VoLTE Accessibility reached 99.4%, comfortably exceeding SLA targets. The client accepted the cluster with zero penalties, and the automated script I built was adopted across the wider team for subsequent cluster acceptance workflows."*

---

### Question 27: "How do you resolve cross-functional technical disagreements with Core or Transmission teams during KPI degradation?"

#### 💬 Model Answer:
> *"Technical disagreements between RAN, Transmission, and Core are common during network outages, but they are solved with objective Layer 3 traces and factual data, never subjective opinions:*
> 
> 1. **Present Objective Layer 3 Signaling Traces:**
>    - During mass E-RAB establishment drops, I capture CTR/UETR traces on the S1-AP interface. If the trace proves that the eNodeB sent an `S1AP E-RAB Setup Request` and received no response from the MME until timer expiry, or if the Core rejected with `Cause: Unknown or already allocated MME UE S1AP ID`, I present timestamped packet captures proving the failure originates in the Core.
> 2. **Isolate Transport Layer Jitter and Packet Drops:**
>    - If backhaul issues are suspected, I extract Baseband IP interface counters (`pmIpPacketsLost`, TWAMP latency graphs, and IEEE 1588v2 PTP clock jitter). If latency spikes beyond 50ms or optical frame loss occurs, I provide this concrete evidence to Transmission teams so they can adjust QoS queue scheduling or upgrade link capacity.
> 3. **Collaborative Problem-Solving Mindset:**
>    - My approach at Amdocs is always professional and solution-oriented. I convene a brief cross-team war room, align all parties around synchronized time-series data, and coordinate a controlled test call to validate the fix as a unified team."*

---

### Question 28: "How do you leverage Python, SQL, and Power BI to improve daily RF optimization efficiency?"

#### 💬 Model Answer:
> *"Engineering automation is my single biggest productivity driver:*
> - **Python Automation:** In previous carrier roles, I developed scripts that automate the daily parsing of raw PM XML/CSV counter dumps, calculate end-to-end 5-pillar KPI formulas, automatically isolate Top Worst Cells, and generate ready-to-run moshell/amos parameter modification scripts. Workflows that previously took 3 to 4 hours of manual spreadsheet manipulation were reduced to under 15 minutes.
> - **SQL Querying in ENIQ:** I write optimized SQL queries against historical performance databases to correlate configuration parameters (CM) with traffic counters (PM), exposing hidden configuration drift and sleeping cells across thousands of sectors.
> - **Power BI Executive Telemetry:** I build interactive visual dashboards for Amdocs stakeholders and carrier executives, providing geospatial heatmaps of KPI degradation, SLA compliance tracking, and dynamic Pre- vs Post-optimization performance comparisons."*

---

# MODULE 9: STRATEGIC QUESTIONS FOR JAVIER TO ASK THE INTERVIEWER

> [!TIP]
> At the conclusion of the interview, the panel will ask: *"Do you have any questions for us?"*  
> A junior engineer says: *"No, everything is clear."* A **Senior Lead** asks strategic, technically sharp questions that establish authority, curiosity, and project alignment.

Select 2 or 3 of these questions depending on the panel:

1. **On Network Architecture & Software Baseline:**
   - *"What is the current Ericsson software release deployed across the client's network (e.g., L20B, L21A, or L22), and what specific 5G NSA advanced features are you actively prioritizing for optimization—such as inter-band Carrier Aggregation, DSS, or Massive MIMO beamforming on AIR units?"*
2. **On Immediate Technical Challenges:**
   - *"In the Mexico City clusters I will be managing, which KPI pillar currently represents the biggest challenge for client SLAs—VoLTE Retainability in high-density corridors, mid-band User Throughput, or 5G NSA SgNB Addition Success Rates?"*
3. **On Operational Tooling & Node Access:**
   - *"Will we have direct CLI access to ENM and moshell/amos for live node-level forensics and script execution, or is parameter deployment routed through a centralized Configuration Management (CM) team?"*
4. **On Project Success & Milestones:**
   - *"The initial assignment is for a 3-month period with multi-phase expansion. From Amdocs' perspective, what are the primary milestones and deliverables that will define a successful performance evaluation for this initial quarter?"*

---

# MODULE 10: QUICK REFERENCE PARAMETER & MOSHELL COMMAND CHEAT SHEET
*(Quick-reference review sheet to consult 1 hour before the interview)*

### 📊 Master Table of Critical Ericsson RAN Parameters:

| Managed Object (MO) | Parameter Name | Typical Range / Value | Performance Impact & Tuning Use Case |
| :--- | :--- | :--- | :--- |
| `EUtranCellFDD` | `cellRange` | 15 – 40 km | Maximum cell radius for RACH access. Setting too low blocks distant UEs; setting too high increases preamble search overhead. |
| `EUtranCellFDD` | `qRxLevMin` | -124 to -118 dBm | Minimum RSRP required for a UE to camp on the cell. Raising it prevents weak edge UEs from attempting access and degrading retainability. |
| `EUtranCellFDD` | `pZeroNominalPucch` | -110 to -96 dBm | Target nominal power on PUCCH uplink channel. Increasing it helps overcome high uplink noise floors (high RSSI / PIM). |
| `EUtranCellRelation` | `a3offset` | 1 to 3 dB | Offset by which neighbor RSRP must exceed serving cell to trigger intra-frequency handover. Lowering it accelerates handovers. |
| `EUtranCellRelation` | `timeToTrigger` (TTT) | 80, 160, 320 ms | Time condition must persist before sending measurement report. Decreasing it prevents late handovers; increasing it suppresses ping-pong. |
| `EUtranCellRelation` | `hysteresis` | 1 to 3 dB | Hysteresis margin preventing continuous ping-pong oscillation between boundary cells. |
| `EUtranCellRelation` | `cellIndividualOffset` (CIO) | -6 to +6 dB | Individual offset applied to a specific neighbor relation to artificially accelerate or delay handovers toward a specific cell. |
| `ReportConfigEUtra` | `b1ThresholdRsrp` | -106 to -98 dBm | Minimum RSRP threshold to detect 5G NR signal and trigger SgNB Addition in 5G NSA (EN-DC). |
| `ReportConfigEUtra` | `timeToTriggerB1` | 160 to 320 ms | Required duration of stable 5G coverage before issuing B1 measurement report. |
| `EUtranCellFDD` | `lbThreshold` | 70% to 85% | PRB utilization threshold triggering inter-frequency Mobility Load Balancing (MLB) to unburden the carrier. |
| `RLC` / `PDCP` | `t310` | 1000 to 2000 ms | Radio Link Failure (RLF) timer. Expiration declares radio link loss after N310 consecutive out-of-sync indications. |

---

### 💻 Master Table of Essential Moshell / Amos Commands:

| Engineering Operational Task | Moshell Command |
| :--- | :--- |
| **Load Managed Object Model** | `lt all` |
| **Audit active node alarms** | `alt` |
| **Query parameter value** | `get EUtranCellFDD=<cell_name> <parameter>` |
| **Modify parameter value** | `set <MO> <parameter> <new_value>` |
| **Block / Unblock cell administratively** | `bl EUtranCellFDD=<cell>` / `deb EUtranCellFDD=<cell>` |
| **Audit optical fiber & SFP transceivers** | `cabx` |
| **Monitor live KPIs and counters** | `kpiget` / `pmx -kpi` |
| **Audit active connected UEs and RF metrics** | `ue print -ad` |
| **Inspect Baseband & Radio hardware inventory** | `inv` |
| **Create pre-deployment backup configuration** | `cvcu "Pre_Optimization_Backup"` |
| **List existing configuration backups** | `cvls` |

---

# MODULE 11: TECHNICAL ENGLISH FLUENCY, TRANSITION PHRASES & PRONUNCIATION GUIDE

### 🎙️ Telecom Terminology Pronunciation Cheat Sheet:
Non-native English speakers commonly trip over specific telecommunications words. Practice these phonetic pronunciations out loud:

| Technical Term | Common Mispronunciation | Correct Phonetic Pronunciation |
| :--- | :--- | :--- |
| **Throughput** | *"troo-poot"* | **/ˈθruːˌpʊt/** (*"THROO-put"* — soft 'th', short 'u') |
| **Retainability** | *"re-ten-shon"* | **/rɪˌteɪ.nəˈbɪl.ə.ti/** (*"ree-tay-nuh-BILL-uh-tee"*) |
| **Hysteresis** | *"hister-esis"* | **/ˌhɪs.təˈriː.sɪs/** (*"hiss-tuh-REE-sis"*) |
| **Azimuth** | *"asi-moot"* | **/ˈæz.ɪ.məθ/** (*"AZ-ih-muth"*) |
| **Interference** | *"inter-fe-rens"* | **/ˌɪn.təˈfɪə.rəns/** (*"in-ter-FEER-ens"*) |
| **Carrier Aggregation** | *"aggre-gashon"* | **/ˈkær.i.ər ˌæɡ.rɪˈɡeɪ.ʃən/** (*"KARE-ee-er ag-rih-GAY-shun"*) |
| **Beamforming** | *"beem-for-ming"* | **/ˈbiːmˌfɔː.mɪŋ/** (*"BEEM-for-ming"*) |
| **Hierarchy** | *"yer-ar-kee"* | **/ˈhaɪə.rɑː.ki/** (*"HY-er-ar-kee"*) |
| **Discrepancy** | *"dis-cre-pan-see"* | **/dɪˈskrep.ən.si/** (*"dih-SKREP-uhn-see"*) |
| **Rollback** | *"ro-ll-bak"* | **/ˈroʊl.bæk/** (*"ROHL-bak"*) |

---

### 💬 Strategic Transition Phrases (How to Buy 3 Seconds of Thinking Time):
If the interviewer asks a complex technical question and you need 3 seconds to organize your thoughts, **never stay silent or say "uhhh..."**. Use one of these natural native bridging phrases:

- *"That is a very practical operational question. Let me walk you through how I approach this systematically..."*
- *"Looking at that scenario from both an RF physical layer and a signaling protocol perspective..."*
- *"In the Ericsson MOM architecture, we typically isolate that issue by checking three distinct layers..."*
- *"In my previous experience handling similar KPI degradations at AT&T Mexico, the first step was always..."*
- *"To answer that accurately, we have to distinguish between an RF coverage limitation versus an admission control bottleneck..."*

---
