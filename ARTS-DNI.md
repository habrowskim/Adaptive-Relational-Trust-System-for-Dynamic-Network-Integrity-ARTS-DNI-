# ARTS-DNI: Adaptive Relational Trust System for Dynamic Network Integrity

![Status](https://img.shields.io/badge/Status-Proof--of--Concept-orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

**ARTS-DNI** is a novel security architecture for distributed systems that transitions from static cryptographic authentication to continuous **Relational Identity** verification.

## 1. Abstract
Traditional security relies on point-in-time identity anchors. ARTS-DNI models trust as a **Trust Trajectory** within a temporal multigraph, integrating hardware-rooted entropy signatures with behavioral consistency metrics. The system demonstrates capability to detect MITM and "low-and-slow" attacks even when the attacker possesses valid cryptographic credentials.

## 2. Core Concepts
* **Relational Identity**: Identity defined by the temporal evolution of interaction patterns.
* **Trust Trajectory**: The path of a relationship state in a multi-dimensional feature space.
* **Continuity Integrity**: Measuring the coherence between current observed states and the learned historical trajectory.

## Notation

* $G_t$ — dynamic interaction graph  
* $V_t$ — set of nodes  
* $E_t$ — edges (communications)  
* $W_t$ — edge weights (trust state)  
* $\sigma(\cdot)$ — sigmoid function  
* $\mu_{AB}, \Sigma$ — learned behavioral distribution parameters  

## 3. Mathematical Model
The system calculates a bounded trust score $T_{AB}(t) \in [0, 1]$ for every node pair:

$$T_{AB}(t) = \sigma(\alpha L_{AB}(t) - \beta H_{AB}(t) + \gamma C_{AB}(t))$$

Where:
* $L_{AB}(t)$: Lineage consistency (historical coherence).
* $H_{AB}(t)$: Shannon entropy of interaction states (uncertainty).
* $C_{AB}(t)$: Contextual consistency (behavioral alignment via **Mahalanobis Distance**).

### Contextual Consistency Equation:
$$C_{AB}(t) = \exp(-\| x_{AB}(t) - \mu_{AB} \|^2_{\Sigma^{-1}})$$

## 4. System Architecture
The framework operates in four abstracted layers:
1.  **Physical Layer**: Extraction of raw signals (jitter, latency).
2.  **Relational Trust Layer**: Modeling the interaction multigraph $G_t = (V_t, E_t, W_t)$.
3.  **AI Analytics Layer**: Computation of anomaly scores via temporal embeddings.
4.  **Operator Layer**: Human-in-the-loop arbitration and automated mitigation.

## 5. Experimental Evaluation
Evaluation was conducted in a Dockerized environment using `tc/netem` for latency injection ($100ms \pm 20ms$).

| Window Size | Detection Rate | FP Rate | Detection Delay |
| :--- | :--- | :--- | :--- |
| **20 samples** | 100% | 4.2% | 1.2s |
| **100 samples** | 100% | 0.8% | 3.5s |

### Key Findings:
* **Adaptability**: Short windows allow for rapid response but faster "model poisoning" (adaptation to attack).
* **Stability**: Long windows provide high statistical inertia and sustained detection.
* **Bi-directional Sensitivity**: The system identifies both attack onset and attack termination as anomalies.

## 6. Threat Model
ARTS-DNI is designed to mitigate:
* **Strategic MITM (SMiTM)**: Precise delay injection within statistical noise.
* **Oscillatory Trust Attacks**: Exploiting decay constants by alternating behavior.
* **Relational Poisoning**: Building false trust capital prior to an attack.
* **The adversary is assumed to be computationally bounded but capable of full traffic observation and manipulation without cryptographic breakage.

## 7. Roadmap & Future Work
- [ ] **Temporal Graph Neural Networks (TGN)** for full relational intelligence.
- [ ] **Local Trust Communities (LTC)** for decentralized processing.
- [ ] **RF-based Entropy Integration** (Hardware Fingerprinting).
- [ ] Real-world deployment on edge IoT infrastructures.

## 8. Summary
ARTS-DNI treats network trust as a continuously evolving relational structure. By shifting the focus from "what you have" (keys) to "how you behave" (trajectory), it identifies compromises invisible to traditional encryption-only layers.


## 9. Limitations

* Evaluation is currently based on synthetic traffic generation.
* No deployment on real production networks has been performed.
* Graph neural model integration is not yet implemented in the current prototype.
---

## Reproducibility

All experiments were conducted in a controlled Docker environment using deterministic seed initialization for reproducibility.

### 🔗 Quick Links
* **Full PDF Documentation**: [ARTS-DNI.pdf](./ARTS-DNI.pdf)
* **Implementation**: [Check out the Python scripts in `/app`](./app)
