import os 
import sys
import numpy as np

from models.LetturaScrittura import LetturaScrittura


# --- 2. PARAMETRI DI INPUT ---

output_folder = "pre_opt"
file_xyz = "/Users/michele/source_git/mie_repo/pub/scan/data/reagenti/2.MM+QM_fix_5H2O_15H2O_30H2O/opt_reagenti_scan_low_solvated_radius_5_solvated_radius_10.xyz"
funzionale = "M062X"
basis_set = "def2svp"
carica = "1"
molteplicità= "2"
nproc = 24
memoria = "24000MB"
tempo = "24:00:00"  

os.makedirs(output_folder, exist_ok=True)
step0_dir = os.path.join(output_folder, "0")
os.makedirs(step0_dir, exist_ok=True)

# --- 3. CREAZIONE OGGETTI ---
lettura = LetturaScrittura(file_xyz)
print(lettura.nato)

atomi_da_congelare_X = [46, lettura.nato]

head= lettura.testa(funzionale, basis_set, carica, molteplicità,nproc,memoria[:2],solvent= "water", dispersion="GD3")
com_con_bond = lettura.scrivi_input(head,lettura.matrix,atomo1=46, atomo2=lettura.nato)
com_finale =lettura.aggiungi_vincoli_coda(com_con_bond, atomi_da_congelare_X)

# Salvataggio file .com per pre-ottimizzazione
com_path = os.path.join(step0_dir, "pre_opt.com")
with open(com_path, "w") as f:
    f.write(com_finale)
print(f"File .com salvato in: {com_path}")

# Salvataggio script SLURM per pre-ottimizzazione
slurm_string = lettura.genera_slurm("pre_opt.com",nproc,tempo,memoria)
slurm_path = os.path.join(step0_dir, "pre_opt.slurm")
with open(slurm_path, "w") as f:
    f.write(slurm_string)
print(f"File SLURM salvato in: {slurm_path}")