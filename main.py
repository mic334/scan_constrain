import os
import copy
import sys

# --- Aggiungi la cartella src al path per importare le classi ---
sys.path.append("src")  # cartella dove si trovano LetturaScrittura e WorkOnMatrix

# --- Import dalle tue classi ---
from LetturaScrittura import LetturaScrittura
from WorkOnMatrix import WorkOnMatrix

if __name__ == "__main__":
    # --- Parametri iniziali ---
    file_xyz = "/Users/michele/source_git/mie_repo/pub/scan/data/water.xyz"  # file XYZ iniziale
    atomo1 = 0
    atomo2 = 1
    n_steps = 2
    output_folder = "steps"

    # --- Crea oggetti dalle tue classi ---
    lettura = LetturaScrittura(file_xyz)
    work = WorkOnMatrix()

    # --- Controlli ---
    if not lettura.matrix:
        raise ValueError("La matrice è vuota!")
    if atomo1 < 0 or atomo1 >= len(lettura.matrix):
        raise IndexError(f"atomo1={atomo1} fuori range")
    if atomo2 < 0 or atomo2 >= len(lettura.matrix):
        raise IndexError(f"atomo2={atomo2} fuori range")
    if n_steps <= 0:
        raise ValueError(f"Il numero di passi deve essere >0, trovato {n_steps}")

    # --- Calcola distanza e delta ---
    distanza, a1, a2 = work.calc_dist(lettura.matrix, atomo1, atomo2)
    delta = work.passi(atomo1, atomo2, n_steps, distanza)

    # --- Header per Gaussian (opzionale) ---
    head = lettura.testa(funzionale="M062x", basis_set="def2svp", carica="1", molteplicità="2")

    # --- Crea cartella principale ---
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # --- Loop sui passi ---
    for step in range(1, n_steps + 1):
        # Copia profonda della matrice iniziale
        nuova_matrice = copy.deepcopy(lettura.matrix)

        # Aggiorna posizione dell'atomo1
        nuova_matrice = work.new_row(nuova_matrice, distanza, delta * step, atomo1, atomo2)

        # Crea cartella per il passo
        step_folder = os.path.join(output_folder, str(step))
        if not os.path.exists(step_folder):
            os.makedirs(step_folder)

        # --- Usa la funzione scrivi_input ---
        com_string = lettura.scrivi_input(head, nuova_matrice)

        # Salva il file
        file_path = os.path.join(step_folder, f"{step}.com")
        with open(file_path, "w") as f:
            f.write(com_string)

        print(f"Salvato step {step} → {file_path}")