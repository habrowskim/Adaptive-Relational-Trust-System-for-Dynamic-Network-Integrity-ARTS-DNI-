🛡️ TGN-Based Anomaly Detection Module (Temporal Graph Networks)
This module represents the core engine of the ARTS-DNI system. It leverages state-of-the-art Deep Learning on dynamic graphs to monitor the integrity of network relationships in real-time.

How It Works
Unlike traditional Intrusion Detection Systems (IDS) that rely on static thresholds (e.g., latency > 100ms), our TGN engine builds a dynamic relational memory.

Physical Feature Extraction: Every network interaction is captured as a feature vector: [latency, jitter, entropy].

Latent Space Mapping (Embedding): The TGN engine projects these raw metrics into a 16-dimensional "relational fingerprint" (embedding).

Similarity Verification: For every subsequent interaction, the system compares the new state with the historical baseline stored in memory using Cosine Similarity.

Attack Simulation: Proof of Concept
We conducted rigorous testing to validate the engine's ability to detect Delay Injection / Man-in-the-Middle (MITM) attacks.

Experimental Results:

Baseline (Normal Traffic): The system successfully learned the device's signature under stable conditions (low latency, high data entropy).

Attack (Anomaly): The introduction of artificial delays and packet structure manipulation caused a drastic shift in the node's state vector.

Detection Metrics:

L2 Distance: 0.7715 (significant displacement in the feature space).

Cosine Similarity: 0.7013 (a ~30% drop relative to the learned pattern).

Outcome: The system accurately identified the breach of trust and triggered a security alert before the packet could be authorized.

Technology Stack
PyTorch & PyTorch Geometric: Core Deep Learning frameworks for graph operations.

TGN (Temporal Graph Networks): Advanced neural architecture for time-varying graph data.

Docker: Full containerization to ensure environment consistency and easy deployment of C++/Torch dependencies.
