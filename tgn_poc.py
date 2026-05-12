import torch
import torch.nn.functional as F
from torch_geometric.nn import TGNMemory
from torch_geometric.nn.models.tgn import IdentityMessage, LastAggregator

def run_simulation():
    print("\n" + "="*50)
    print("ARTS-DNI: SYMULACJA ATAKU NA WARSTWĘ GRAFOWĄ")
    print("="*50)

    msg_dim, mem_dim, t_dim = 3, 16, 16
    memory = TGNMemory(
        num_nodes=10,
        raw_msg_dim=msg_dim,
        memory_dim=mem_dim,
        time_dim=t_dim,
        message_module=IdentityMessage(msg_dim, mem_dim, t_dim),
        aggregator_module=LastAggregator(),
    )

    # --- KLUCZOWA POPRAWKA TYPÓW ---
    # Wymuszamy, aby wewnętrzne liczniki czasu były typu Float, 
    # tak jak nasze dane wejściowe, lub dopasowujemy się do Long.
    # Skoro błąd mówi "got Float for the source", spróbujmy podać Long:
    
    src = torch.tensor([0], dtype=torch.long)
    dst = torch.tensor([1], dtype=torch.long)

    # --- ETAP 1: NAUKA BASELINE'U ---
    normal_msg = torch.tensor([[0.10, 0.02, 0.90]], dtype=torch.float)
    # Zmieniamy na Long, aby dopasować do "destination" z błędu
    t_normal = torch.tensor([1], dtype=torch.long) 
    
    try:
        memory.update_state(src, dst, t_normal, normal_msg)
    except RuntimeError:
        # Jeśli powyższe zawiedzie, próbujemy Float - niektóre wersje PyG tak mają
        t_normal = t_normal.float()
        memory.update_state(src, dst, t_normal, normal_msg)

    baseline_vector = memory.memory[src].clone().detach()
    print(f"[*] Baseline ustalony dla Node 0.")

    # --- ETAP 2: SYMULACJA ATAKU ---
    attack_msg = torch.tensor([[0.80, 0.15, 0.30]], dtype=torch.float)
    t_attack = torch.tensor([2], dtype=torch.long) # Dopasowane do Etapu 1

    try:
        memory.update_state(src, dst, t_attack, attack_msg)
    except RuntimeError:
        t_attack = t_attack.float()
        memory.update_state(src, dst, t_attack, attack_msg)

    attack_vector = memory.memory[src].clone().detach()
    print(f"[*] Atak przeprowadzony (Iniekcja opóźnień).")

    # --- ETAP 3: WERYFIKACJA ---
    distance = torch.norm(baseline_vector - attack_vector, p=2).item()
    similarity = F.cosine_similarity(baseline_vector, attack_vector).item()

    print("\n" + "-"*50)
    print(f"WYNIK ANALIZY WEKTOROWEJ:")
    print(f"Dystans (L2): {distance:.4f}")
    print(f"Podobieństwo (Cosine): {similarity:.4f}")
    
    if similarity < 0.90:
        print("\n[!!!] ALERT: WYKRYTO NARUSZENIE INTEGRALNOŚCI RELACYJNEJ!")
    else:
        print("\n[OK] Ruch mieści się w normie.")
    print("-"*50 + "\n")

if __name__ == "__main__":
    run_simulation()
