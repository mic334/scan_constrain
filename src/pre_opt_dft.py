import os 
import sys
import numpy as np

from models.LetturaScrittura import LetturaScrittura


# --- 2. PARAMETRI DI INPUT ---

programma = "gaussian"  # o "orca" a seconda del software che vuoi usare
pre_opt_folder = "pre_opt_dft"
file_xyz = "/Users/michele/source_git/mie_repo/pub/scan/data/prodotti/3.MM+QM_fix_5H2O_fix_15H2O_30H2O/prodotti_opt_IRC_low_solvated_radius_5_solvated_radius_10.xyz"
funzionale = "M062X"
basis_set = "def2svp"
carica = 1
molteplicità = 2
nproc = 24
memoria = "24GB"
tempo = "12:00:00"
os.makedirs(pre_opt_folder, exist_ok=True)

# Usa direttamente pre_opt_folder
step0_dir = pre_opt_folder

# --- 3. CREAZIONE OGGETTI ---
lettura = LetturaScrittura(file_xyz)
print(lettura.nato)

atomi_da_congelare_X = range(46, lettura.nato) # Congela tutti gli atomi da 46 fino all'ultimo
# +1 perché range è esclusivo, quindi range(46, lettura.nato+1) include l'ultimo atomo
head = lettura.testa(
    funzionale, basis_set, carica, molteplicità,
    nproc, memoria[:2],
    solvent="water",
    dispersion="GD3",
    addredundant=False
)

com_con_bond = lettura.scrivi_input(
    head,
    lettura.matrix,
    atomo1=46,
    atomo2=lettura.nato,
    vincolo_bond=False
)

com_finale = lettura.aggiungi_vincoli_coda(
    com_con_bond, atomi_da_congelare_X
)

# Salvataggio file .com
com_path = os.path.join(step0_dir, "pre_opt.com")
with open(com_path, "w") as f:
    f.write(com_finale)

print(f"File .com salvato in: {com_path}")

# Salvataggio script SLURM
slurm_string = lettura.genera_slurm(programma, com_path, nproc, tempo, memoria)

slurm_path = os.path.join(step0_dir, "pre_opt.slurm")
with open(slurm_path, "w") as f:
    f.write(slurm_string)

print(f"File SLURM salvato in: {slurm_path}")