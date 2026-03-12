import os
import copy
import sys

from models.HydraConvexHull import HydraConvexHull
from models.LetturaScrittura import LetturaScrittura

original_xyz_path = "da_inserire.xyz"
radius = 5
nO = int(radius * 3)

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
    hamiltonian="GNF2-XTB",
    carica=0,
    molteplicità=1,
    nproc=4,
    mem=2,
    solvent="water",
    Constraint=None
)

# nome del nuovo file ORCA
orca_file_path = os.path.splitext(new_xyz_path)[0] + ".inp"

# scrivo il file ORCA
with open(orca_file_path, "w") as f:
    f.write(orca_input)

print(f"New ORCA input created at {orca_file_path}")

