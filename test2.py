import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# --- KROK 1: GENERATOR DANYCH Z SZUMEM I CICHYM ATAKIEM ---
def generate_advanced_traffic(ticks, attack_start):
    data = []
    for t in range(ticks):
        # Normalny profil: Baza + Jitter + Dryf sezonowy
        base = 0.010
        noise = np.random.normal(0, 0.0015)
        drift = 0.002 * np.sin(t / 15)
        
        latency = base + noise + drift
        
        # Atak "Low-and-Slow" - celowo bardzo małe przesunięcie (0.004s)
        if t >= attack_start:
            latency += 0.004 + np.random.normal(0, 0.0005)
            
        data.append(latency)
    return np.array(data)

# --- KONFIGURACJA ---
TICKS = 400
ATTACK_START = 200

# 1. Generowanie danych
raw_latency = generate_advanced_traffic(TICKS, ATTACK_START)
df = pd.DataFrame({'latency': raw_latency})

# 2. Feature Engineering: Opóźnienie + Zmienność (std dev)
df['variance'] = df['latency'].rolling(window=10).std().fillna(0)
features = df[['latency', 'variance']].values

# 3. ML: Isolation Forest (Trening na pierwszej połowie - "czystej")
model = IsolationForest(contamination=0.01, random_state=42)
model.fit(features[:100])

# 4. Obliczanie surowego wyniku anomalii
df['raw_anomaly_score'] = -model.decision_function(features)

# --- KLUCZOWA INNOWACJA: TEMPORAL RISK INTEGRATION ---
# Wygładzamy wynik, aby pozbyć się "pików" (fałszywych alarmów)
df['smoothed_risk'] = df['raw_anomaly_score'].ewm(span=20).mean()

# Automatyczny próg (98 percentyl z okresu treningowego)
threshold = np.percentile(df['smoothed_risk'][:100], 98) + 0.02

# --- WIZUALIZACJA ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Wykres 1: Sygnał Fizyczny
ax1.plot(df.index, df['latency'], color='gray', alpha=0.4, label='Surowe opóźnienie (ms)')
ax1.axvline(x=ATTACK_START, color='red', linestyle='--', label='Początek Infiltracji (MITM)')
ax1.set_title("Warstwa Fizyczna: Sygnały Surowe", fontsize=14)
ax1.legend()

# Wykres 2: Wynik ARTS-DNI
ax2.plot(df.index, df['smoothed_risk'], color='blue', lw=2, label='ARTS-DNI Risk Index')
ax2.axhline(y=threshold, color='orange', linestyle=':', label='Dynamiczny Próg Zaufania')
ax2.fill_between(df.index, df['smoothed_risk'], threshold, 
                 where=(df['smoothed_risk'] > threshold), color='red', alpha=0.3, label='ALARM: Relational Drift')
ax2.axvline(x=ATTACK_START, color='red', linestyle='--')
ax2.set_title("Warstwa Analityczna: Poziom Ryzyka Relacyjnego", fontsize=14)
ax2.set_xlabel("Interakcje (Ticks)")
ax2.set_ylabel("Risk Score")
ax2.legend()

plt.tight_layout()
plt.show()

# Wynik testu
detected = df['smoothed_risk'][ATTACK_START:].max() > threshold
print(f"STATUS DETEKCJI: {'SUKCES - Wykryto cichy atak' if detected else 'PORAŻKA - Atak niewykryty'}")
