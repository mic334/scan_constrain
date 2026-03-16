import sys
import math
import numpy as np
from scipy.spatial import ConvexHull


class WaterShellGenerator:
    """
    Classe per leggere una molecola da file XYZ, costruire il convex hull
    e aggiungere molecole d'acqua attorno alla superficie.

    IDEA PRINCIPALE DELLA CORREZIONE
    --------------------------------
    Nel codice originale c'erano tre problemi importanti:

    1) Il parametro "radius" non controllava davvero la distanza finale
       dalla molecola, perché veniva usato per generare punti sulla sfera
       ma poi la direzione veniva normalizzata.

    2) In map_to_hull() veniva usato sempre hull_vertices[0], cioè il primo
       vertice del convex hull, invece di usare la geometria vera del hull
       nella direzione desiderata.

    3) I punti della fibonacci sphere erano generati attorno all'origine,
       ma poi venivano trattati come se fossero punti assoluti e non solo
       direzioni.

    In questa versione:
    - la fibonacci sphere genera direzioni unitarie
    - per ogni direzione trovo quanto il hull si estende in quella direzione
    - aggiungo una distanza extra chiamata solvent_distance

    Quindi la distanza finale è davvero:
        distanza_superficie_lungo_direzione + solvent_distance
    """

    def __init__(self, xyz_file_path, solvent_distance=5.0, waters_per_distance=3):
        """
        Parametri
        ---------
        xyz_file_path : str
            Percorso del file XYZ originale.
        solvent_distance : float
            Distanza extra dalla superficie del convex hull.
        waters_per_distance : int o float
            Fattore per stimare quante acque aggiungere:
                n_oxygen = int(solvent_distance * waters_per_distance)
        """
        self.xyz_file_path = xyz_file_path
        self.solvent_distance = float(solvent_distance)
        self.waters_per_distance = waters_per_distance

        self.original_lines = None
        self.atom_coords = None
        self.center = None
        self.hull = None

    # ------------------------------------------------------------------
    # LETTURA DATI
    # ------------------------------------------------------------------

    def read_xyz(self):
        """
        Legge il file XYZ e salva:
        - tutte le righe originali
        - le coordinate atomiche in un array numpy
        """
        with open(self.xyz_file_path, 'r') as f:
            self.original_lines = f.readlines()

        atom_coords = []
        for line in self.original_lines[2:]:
            parts = line.split()
            if len(parts) < 4:
                continue
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            atom_coords.append([x, y, z])

        self.atom_coords = np.array(atom_coords, dtype=float)

    def calculate_molecule_center(self):
        """
        Calcola il centro geometrico della molecola.

        Qui tengo la tua idea originale: media semplice delle coordinate.
        """
        if self.atom_coords is None:
            self.read_xyz()

        # --- CODICE ORIGINALE (funzione separata) ---
        # x_sum, y_sum, z_sum = 0.0, 0.0, 0.0
        # for line in lines[2:]:
        #     parts = line.split()
        #     x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
        #     x_sum += x
        #     y_sum += y
        #     z_sum += z
        # center_x, center_y, center_z = x_sum / atom_count, y_sum / atom_count, z_sum / atom_count
        # return (center_x, center_y, center_z)

        # --- SOSTITUITO CON VERSIONE NUMPY PIÙ DIRETTA ---
        self.center = np.mean(self.atom_coords, axis=0)

    def calculate_convex_hull(self):
        """
        Costruisce il convex hull della molecola.
        """
        if self.atom_coords is None:
            self.read_xyz()

        self.hull = ConvexHull(self.atom_coords)

    def prepare_geometry(self):
        """
        Prepara tutti gli oggetti geometrici necessari:
        - lettura xyz
        - centro
        - hull
        """
        self.read_xyz()
        self.calculate_molecule_center()
        self.calculate_convex_hull()

    # ------------------------------------------------------------------
    # GENERAZIONE DIREZIONI
    # ------------------------------------------------------------------

    @staticmethod
    def fibonacci_sphere(samples):
        """
        Genera direzioni distribuite quasi uniformemente sulla sfera unitaria.

        NOTA IMPORTANTE:
        nel codice originale la funzione riceveva anche un "radius", ma poi
        quel radius veniva perso quando il vettore veniva normalizzato.

        Per questo qui genero direttamente DIREZIONI unitarie.
        """
        points = []

        if samples <= 0:
            return points

        if samples == 1:
            return [np.array([0.0, 1.0, 0.0], dtype=float)]

        phi = math.pi * (3.0 - math.sqrt(5.0))  # golden angle

        for i in range(samples):
            y = 1.0 - (i / float(samples - 1)) * 2.0
            radius_at_y = math.sqrt(max(0.0, 1.0 - y * y))

            theta = phi * i

            x = math.cos(theta) * radius_at_y
            z = math.sin(theta) * radius_at_y

            # --- CODICE ORIGINALE ---
            # points.append((x * radius, y * radius, z * radius))

            # --- SOSTITUITO ---
            # Qui NON moltiplico per il radius di solvatazione,
            # perché questi punti servono solo come direzioni.
            direction = np.array([x, y, z], dtype=float)

            norm = np.linalg.norm(direction)
            if norm < 1e-12:
                continue
            direction /= norm

            points.append(direction)

        return points

    # ------------------------------------------------------------------
    # GEOMETRIA DEL HULL
    # ------------------------------------------------------------------

    def distance_to_hull_along_direction(self, direction):
        """
        Restituisce quanto il convex hull si estende lungo una direzione.

        Qui correggo il bug più importante del codice originale.

        Invece di usare SEMPRE il primo vertice del hull, proietto tutti i
        vertici del hull sulla direzione richiesta e prendo la proiezione massima.
        """
        if self.hull is None or self.center is None:
            self.prepare_geometry()

        hull_vertices = self.hull.points[self.hull.vertices]

        projections = []
        for vertex in hull_vertices:
            v = vertex - self.center
            proj = np.dot(v, direction)
            projections.append(proj)

        return max(projections)

    def map_to_hull(self, directions):
        """
        Mappa le direzioni in punti reali attorno alla molecola.

        Formula nuova:
            mapped_point = center + (hull_distance + solvent_distance) * direction
        """
        if self.hull is None or self.center is None:
            self.prepare_geometry()

        mapped_points = []

        for direction in directions:
            direction = np.array(direction, dtype=float)
            norm = np.linalg.norm(direction)
            if norm < 1e-12:
                continue
            direction /= norm

            # --- CODICE ORIGINALE ---
            # hull_vertices = hull.points[hull.vertices]
            # direction = point - np.array(center)
            # direction /= np.linalg.norm(direction)
            # mapped_point = np.array(center) + (
            #     np.linalg.norm(hull_vertices[0] - np.array(center)) + additional_distance
            # ) * direction

            # --- SOSTITUITO ---
            # 1) non uso più point - center, perché point era già una direzione
            #    costruita attorno all'origine
            # 2) non uso più hull_vertices[0]
            # 3) uso una distanza che dipende davvero dalla direzione
            hull_distance = self.distance_to_hull_along_direction(direction)
            mapped_point = self.center + (hull_distance + self.solvent_distance) * direction

            mapped_points.append(mapped_point)

        return mapped_points

    # ------------------------------------------------------------------
    # POSIZIONAMENTO ACQUE
    # ------------------------------------------------------------------

    @staticmethod
    def place_hydrogen_atoms(oxygen_atom, oh_distance=0.96, angle=104.5):
        """
        Posiziona i due H attorno a un O.

        Tengo una versione semplice, come avevi detto:
        non oriento la molecola d'acqua rispetto alla superficie locale.
        """
        angle_rad = math.radians(angle)

        # --- CODICE ORIGINALE ---
        # v1 = np.array([1.0, 0.0, 0.0])
        # v2 = np.array([
        #     math.cos(angle_rad),
        #     math.sin(angle_rad),
        #     0.0
        # ])

        # --- TENUTO QUASI UGUALE ---
        v1 = np.array([1.0, 0.0, 0.0], dtype=float)
        v2 = np.array([math.cos(angle_rad), math.sin(angle_rad), 0.0], dtype=float)

        v1 /= np.linalg.norm(v1)
        v2 /= np.linalg.norm(v2)

        oxygen_atom = np.array(oxygen_atom, dtype=float)

        h1 = oxygen_atom + oh_distance * v1
        h2 = oxygen_atom + oh_distance * v2

        return [tuple(h1), tuple(h2)]

    def estimate_number_of_waters(self):
        """
        Stima il numero di molecole d'acqua da aggiungere.
        """
        n_oxygen = int(self.solvent_distance * self.waters_per_distance)
        return max(1, n_oxygen)

    # ------------------------------------------------------------------
    # OUTPUT
    # ------------------------------------------------------------------

    def generate_new_file_path(self):
        """
        Genera il nome del file di output.
        """
        if float(self.solvent_distance).is_integer():
            dist_str = str(int(self.solvent_distance))
        else:
            dist_str = str(self.solvent_distance).replace('.', '_')

        if self.xyz_file_path.endswith('.xyz'):
            return self.xyz_file_path[:-4] + f"_solvated_radius_{dist_str}.xyz"
        return self.xyz_file_path + f"_solvated_radius_{dist_str}.xyz"

    def create_modified_xyz(self, new_xyz_path=None):
        """
        Crea il nuovo file XYZ con acque aggiunte.

        Flusso:
        - legge il file
        - calcola centro e convex hull
        - genera direzioni con fibonacci sphere
        - mappa i punti sulla superficie + distanza extra
        - scrive il nuovo XYZ
        """
        self.prepare_geometry()

        n_oxygen = self.estimate_number_of_waters()
        directions = self.fibonacci_sphere(n_oxygen)
        oxygen_atoms = self.map_to_hull(directions)

        if new_xyz_path is None:
            new_xyz_path = self.generate_new_file_path()

        original_atom_count = int(self.original_lines[0].strip())
        total_new_atoms = original_atom_count + len(oxygen_atoms) * 3

        with open(new_xyz_path, 'w') as new_file:
            new_file.write(f"{total_new_atoms}\n")
            new_file.write("Molecule with added water molecules around convex hull\n")

            for line in self.original_lines[2:]:
                new_file.write(line)

            for oxygen in oxygen_atoms:
                new_file.write(f"O {oxygen[0]:.8f} {oxygen[1]:.8f} {oxygen[2]:.8f}\n")

                hydrogens = self.place_hydrogen_atoms(
                    oxygen_atom=oxygen,
                    oh_distance=0.96,
                    angle=104.5
                )

                for hydrogen in hydrogens:
                    new_file.write(f"H {hydrogen[0]:.8f} {hydrogen[1]:.8f} {hydrogen[2]:.8f}\n")

        return new_xyz_path

    # ------------------------------------------------------------------
    # METODO COMODO PER USO DA CODICE
    # ------------------------------------------------------------------

    def run(self, new_xyz_path=None, verbose=True):
        """
        Esegue tutta la procedura e ritorna il path del file creato.
        """
        n_oxygen = self.estimate_number_of_waters()

        if verbose:
            print(f"Solvent distance from hull = {self.solvent_distance}")
            print(f"Number of waters added = {n_oxygen}")

        out_path = self.create_modified_xyz(new_xyz_path=new_xyz_path)

        if verbose:
            print(f"New XYZ file created at {out_path}")

        return out_path


def main():
    """
    Uso da riga di comando:
        python script.py <original_xyz_file_path> [solvent_distance]
    """
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script.py <original_xyz_file_path> [solvent_distance]")
        sys.exit(1)

    xyz_file_path = sys.argv[1]
    solvent_distance = float(sys.argv[2]) if len(sys.argv) == 3 else 5.0

    generator = WaterShellGenerator(
        xyz_file_path=xyz_file_path,
        solvent_distance=solvent_distance,
        waters_per_distance=3
    )

    generator.run(verbose=True)


if __name__ == "__main__":
    main()