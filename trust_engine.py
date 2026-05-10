import subprocess
import time
import re
import numpy as np
from scipy.spatial import distance

# Konfiguracja
TARGET_IP = "127.0.0.1" # Pingujemy siebie dla pewności testu
WINDOW_SIZE = 20
history = []

print("ARTS-DNI: Adaptive Monitoring Started...")

while True:
    try:
        # Próba pingu z timeoutem 1s (-W 1)
        start_t = time.time()
        output = subprocess.check_output(
            f"ping -c 1 -W 1 {TARGET_IP}", 
            shell=True, 
            stderr=subprocess.STDOUT
        ).decode()
        
        # Wyciąganie latencji
        ms = float(re.search(r"time=([\d.]+)", output).group(1))
    except Exception:
        # Jeśli ping zawiedzie (np. przez silny atak tc), ustawiamy wysoką karę
        ms = 500.0

    history.append([ms])
    
    risk_score = 0.0
    status = "SAFE"

    # Logika ARTS (Mahalanobis) startuje po zebraniu WINDOW_SIZE próbek
    if len(history) > WINDOW_SIZE:
        data = np.array(history[-WINDOW_SIZE:])
        current_sample = np.array([ms])
        
        # Obliczanie średniej i macierzy kowariancji
        mean = np.mean(data, axis=0)
        cov = np.cov(data.T)
        
        # DODATEK: Regularyzacja (zapobiega zawieszaniu się przy 20. próbce)
        cov += 1e-6 

        try:
            # Obliczanie dystansu Mahalanobisa
            inv_cov = np.linalg.inv(np.atleast_2d(cov))
            d_mahal = distance.mahalanobis(current_sample, mean, inv_cov)
            risk_score = d_mahal
        except:
            risk_score = 0.0

        if risk_score > 3.0:
            status = "ALERT!"
        
        # Usuwamy najstarszą próbkę, by zachować okno czasowe (Adaptive)
        history.pop(0)

    print(f"Time: {time.strftime('%H:%M:%S')} | Latency: {ms:>6.2f}ms | Risk: {risk_score:>6.2f} | [{status}]")
    
    # Czekamy 1s do następnej próby, ale odejmujemy czas wykonania pingu
    time.sleep(max(0, 1 - (time.time() - start_t)))
