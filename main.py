import os
import copy
import sys

# --- Aggiungi la cartella src al path ---
sys.path.append("src") 

from LetturaScrittura import LetturaScrittura
from WorkOnMatrix import WorkOnMatrix

if __name__ == "__main__":
    # --- Parametri iniziali ---
    file_xyz = "/Users/michele/source_git/mie_repo/pub/scan/data/water.xyz"
    atomo1 = 0
    atomo2 = 1
    n_steps = 10          # Numero di file/step che vuoi generare
    ampiezza_passo = 0.05  # Ogni step sposta l'atomo di 0.05 Angstrom
    output_folder = "steps"

    # --- Crea oggetti ---
    lettura = LetturaScrittura(file_xyz)
    work = WorkOnMatrix()

    # --- Controlli di sicurezza ---
    if not lettura.matrix:
        raise ValueError("La matrice è vuota!")
    if atomo1 >= len(lettura.matrix) or atomo2 >= len(lettura.matrix):
        raise IndexError("Indici atomi fuori range")

    # --- Calcolo Distanza iniziale ---
    # Ci serve ancora per definire la direzione del movimento in new_row
    distanza, a1, a2 = work.calc_dist(lettura.matrix, atomo1, atomo2)

    # --- Calcolo Delta ---
    # Modificato: ora passiamo l'ampiezza fissa. 
    # 'delta' qui rappresenterà lo spostamento di un singolo step.
    delta_unitario = work.passi(n_steps, ampiezza_passo)

    # --- Header per Gaussian ---
    head = lettura.testa(funzionale="M062x", basis_set="def2svp", carica="1", molteplicità="2")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # --- Loop sui passi ---
    for step in range(1, n_steps + 1):
        # Copia la matrice originale ogni volta per evitare errori cumulativi
        nuova_matrice = copy.deepcopy(lettura.matrix)

        # Calcoliamo lo spostamento totale per questo specifico step
        # Esempio: step 1 = 0.05, step 2 = 0.10, ecc.
        spostamento_attuale = delta_unitario * step

        # Aggiorna posizione dell'atomo1 verso l'atomo2
        nuova_matrice = work.new_row(nuova_matrice, distanza, spostamento_attuale, atomo1, atomo2)

        # Gestione cartelle e file
        step_folder = os.path.join(output_folder, str(step))
        if not os.path.exists(step_folder):
            os.makedirs(step_folder)
        com_string = lettura.scrivi_input(head, nuova_matrice)
        file_path = os.path.join(step_folder, f"{step}.com")
        
        with open(file_path, "w") as f:
            f.write(com_string)

        print(f"Generato step {step}: spostamento totale {spostamento_attuale:.3f} Å → {file_path}")