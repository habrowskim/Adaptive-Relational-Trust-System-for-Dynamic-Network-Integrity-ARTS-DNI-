import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

# --- KROK 1: GENERATOR DANYCH "REAL-WORLD" ---
def generate_network_traffic(ticks, attack_type="none"):
    data = []
    for t in range(ticks):
        # Normalny ruch: baza 10ms + jitter + sezonowe wahania CPU
        base = 0.010 
        jitter = np.random.normal(0, 0.001)
        drift = 0.002 * np.sin(t / 10) # Naturalny dryf temperatury/obciążenia
        
        latency = base + jitter + drift
        
        # Implementacja ataku "Low-and-Slow" (Cichy MITM)
        # Atakujący stara się nie przekraczać progu 20ms, aby uniknąć detekcji prostej
        if attack_type == "low_and_slow" and t >= 100:
            latency += np.random.uniform(0.003, 0.006) # Minimalne opóźnienie
            
        data.append([t, latency])
    return np.array(data)

# --- KROK 2: SILNIK ARTS-DNI (ML) ---
def run_arts_dni_test():
    TICKS = 300
    ATTACK_START = 150
    
    # Generujemy dane (Normalne vs Atak)
    clean_traffic = generate_network_traffic(ATTACK_START, attack_type="none")
    attack_traffic = generate_network_traffic(TICKS - ATTACK_START, attack_type="low_and_slow")
    full_data = np.vstack([clean_traffic, attack_traffic])
    
    # Przygotowanie cech do ML (Czas między pakietami + krocząca wariancja)
    df = pd.DataFrame(full_data, columns=['tick', 'latency'])
    df['rolling_std'] = df['latency'].rolling(window=5).std().fillna(0)
    
    # Cechy wejściowe: [opóźnienie, zmienność]
    features = df[['latency', 'rolling_std']].values
    
    # Trening Isolation Forest tylko na "zdrowych" danych (Baseline)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(features[:100]) # Uczymy się pierwszych 100 tików
    
    # Wykrywanie
    # decision_function: im niższa wartość, tym bardziej podejrzane
    df['anomaly_score'] = -model.decision_function(features)
    df['prediction'] = model.predict(features) # 1 = OK, -1 = Anomalia
    
    
    # --- KROK 3: RAPORT I WIZUALIZACJA ---
    plt.figure(figsize=(15, 7))
    
    # Wykres opóźnień
    plt.subplot(2, 1, 1)
    plt.plot(df['tick'], df['latency'], color='gray', alpha=0.5, label='Raw Latency')
    plt.axvline(x=ATTACK_START, color='red', linestyle='--', label='Start Ataku (Low-and-Slow)')
    plt.title("Analiza Sygnałów Fizycznych (Opóźnienie)")
    plt.legend()

    # Wykres Anomalii ARTS-DNI
    plt.subplot(2, 1, 2)
    plt.plot(df['tick'], df['anomaly_score'], color='blue', label='ARTS-DNI Risk Level')
    plt.fill_between(df['tick'], df['anomaly_score'], where=(df['tick'] >= ATTACK_START), 
                     color='red', alpha=0.2, label='Detected Attack Zone')
    plt.axhline(y=np.percentile(df['anomaly_score'][:100], 95), color='orange', linestyle=':', label='Dynamic Threshold')
    plt.ylabel("Anomaly Score")
    plt.xlabel("Interaction Ticks")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

    # Metryki
    y_true = [1 if t < ATTACK_START else -1 for t in range(TICKS)]
    print("\n--- RAPORT SKUTECZNOŚCI ARTS-DNI ---")
    print(classification_report(y_true, df['prediction'], target_names=['Atak', 'Normalny']))

run_arts_dni_test()
