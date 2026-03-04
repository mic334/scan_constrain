import os
import copy
import sys

# --- 1. CONFIGURAZIONE PATH E IMPORT ---
sys.path.append("../src") 

from LetturaScrittura import LetturaScrittura
from WorkOnMatrix import WorkOnMatrix

# --- 2. PARAMETRI DI INPUT ---
file_xyz = "/Users/michele/source_git/mie_repo/pub/scan/data/water.xyz"
atomo1 = 0  
atomo2 = 1  
atomi_da_congelare_X = [2, 3] 
# puoi usare anche range(20,27) ricora che in questo caso i numeri saranno da 20 a 26 poi gli sommi piu uno quindi i numeri partono da 20 e arrivano a 27, morale della favola range(atomo iniziale -1, atomo_finale)

n_steps = 5            
ampiezza_passo = -0.05  
output_folder = "steps"
nproc = 24
tempo = "24:00:00"
memoria = "24000MB"

funzionale = "M062X"
basis_set = "def2svp"
carica = "1"
molteplicità= "2"

# --- 3. CREAZIONE OGGETTI ---
lettura = LetturaScrittura(file_xyz)
work = WorkOnMatrix()

# --- 4. CALCOLO DISTANZA INIZIALE ---
risultato_dist = work.calc_dist(lettura.matrix, atomo1, atomo2)
dist_iniziale = risultato_dist[0] 
print(f"--- Distanza iniziale: {dist_iniziale:.4f} Å ---")

os.makedirs(output_folder, exist_ok=True)

# --- 4b. STEP 0 (punto di partenza) ---
print(f"Step 0: Distanza iniziale {dist_iniziale:.4f} Å")

step0_dir = os.path.join(output_folder, "0")
os.makedirs(step0_dir, exist_ok=True)

head = lettura.testa(funzionale, basis_set, carica, molteplicità,nproc,memoria[:2],solvent="water",dispersion="GD3")
com_con_bond = lettura.scrivi_input(head, lettura.matrix, atomo1, atomo2)
com_finale = lettura.aggiungi_vincoli_coda(com_con_bond, atomi_da_congelare_X)

# Salvataggio file .com per step 0
com_path = os.path.join(step0_dir, "0.com")
with open(com_path, "w") as f:
    f.write(com_finale)
print(f"File .com salvato in: {com_path}")

# Salvataggio script SLURM per step 0
slurm_string = lettura.genera_slurm("0.com",nproc,tempo,memoria)
slurm_path = os.path.join(step0_dir, "0.sh")
with open(slurm_path, "w") as f:
    f.write(slurm_string)
print(f"File SLURM salvato in: {slurm_path}")

# --- 5. LOOP GENERAZIONE STEP 1..n ---
for step in range(1, n_steps + 1):
    # Copia della matrice
    nuova_matrice = copy.deepcopy(lettura.matrix)

    # Calcolo spostamento
    spostamento_attuale = ampiezza_passo * step
    nuova_matrice = work.new_row(nuova_matrice, dist_iniziale, spostamento_attuale, atomo1, atomo2)

    # Verifica distanza per il print
    nuova_dist = work.calc_dist(nuova_matrice, atomo1, atomo2)[0]
    print(f"Step {step}: Nuova Distanza {nuova_dist:.4f} Å")

    # --- Costruzione input Gaussian ---
    head = lettura.testa(funzionale, basis_set, carica, molteplicità,nproc,memoria[:2],solvent="water",dispersion="GD3")
    com_con_bond = lettura.scrivi_input(head, nuova_matrice, atomo1, atomo2)
    com_finale = lettura.aggiungi_vincoli_coda(com_con_bond, atomi_da_congelare_X)

    # --- Creazione cartella step ---
    step_dir = os.path.join(output_folder, str(step))
    os.makedirs(step_dir, exist_ok=True)

    # --- Salvataggio file .com ---
    com_path = os.path.join(step_dir, f"{step}.com")
    with open(com_path, "w") as f:
        f.write(com_finale)
    print(f"File .com salvato in: {com_path}")

    # --- Salvataggio script SLURM ---
    slurm_string = lettura.genera_slurm(f"{step}.com",nproc,tempo,memoria)
    slurm_path = os.path.join(step_dir, f"{step}.sh")
    with open(slurm_path, "w") as f:
        f.write(slurm_string)
    print(f"File SLURM salvato in: {slurm_path}")

print(f"\n✅ Operazione completata con successo!")
