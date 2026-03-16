import os
import copy
import sys

from models.HydraConvexHull import HydraConvexHull
from models.LetturaScrittura import LetturaScrittura

#dichiariazioen variabile
original_xyz_path = "/Users/michele/source_git/mie_repo/pub/scan/test/opt_reagenti_scan_low.xyz"
radius = 5
nO = int(radius * 3)
print(original_xyz_path)
print(os.path.exists(original_xyz_path))

# creo oggetto HydraConvexHull
hch = HydraConvexHull()

new_xyz_path = hch.generate_new_file_path(original_xyz_path, radius)
hch.create_modified_xyz(original_xyz_path, new_xyz_path, radius, nO)

print("Number of waters added =", nO)
print(f"New XYZ file created at {new_xyz_path} with additional oxygen and hydrogen atoms.")

# leggo il nuovo xyz generato
ls = LetturaScrittura(new_xyz_path)

# genero il testo dell'input ORCA
orca_input = ls.testa_orca_xtb(
    hamiltonian="GFN2-XTB",
    carica=1,
    molteplicità=2,
    nproc=8,
    mem=2,
    solvent="water",
    Constraint='C 0:81 C'
)

# nome del nuovo file ORCA
orca_file_path = os.path.splitext(new_xyz_path)[0] + ".inp"

# scrivo il file ORCA
with open(orca_file_path, "w") as f:
    f.write(orca_input)

print(f"New ORCA input created at {orca_file_path}")

programma = "orca"
input_file = orca_file_path
nproc = 8
tempo = "12:00:00"
memoria = 2

slurm_script = ls.genera_slurm(programma, input_file, nproc, tempo, memoria)

cartella = os.path.dirname(input_file)
base = os.path.splitext(os.path.basename(input_file))[0]
nome_file = os.path.join(cartella, base + ".slurm")

with open(nome_file, "w") as f:
    f.write(slurm_script)


print(f"File SLURM creato: {nome_file}")
