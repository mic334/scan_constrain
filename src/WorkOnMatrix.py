import  numpy as np
import math

import math

class WorkOnMatrix:
    def calc_dist(self, matrice, atomo1, atomo2):
        # Estrai le coordinate dei due atomi
        x1, y1, z1 = matrice[atomo1][1], matrice[atomo1][2], matrice[atomo1][3]
        x2, y2, z2 = matrice[atomo2][1], matrice[atomo2][2], matrice[atomo2][3]
        
        # Calcolo distanza euclidea
        distanza = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        print(f"Distanza attuale: {distanza}")
        return distanza, atomo1, atomo2 

    def passi(self, num_step, dimensione_step):
        """
        Calcola lo spostamento totale (delta) basato su:
        num_step: quanti movimenti fare
        dimensione_step: quanto è lungo ogni movimento (es. 0.05)
        """
        delta = num_step * dimensione_step
        print(f"Spostamento totale calcolato (delta): {delta}")
        return delta

    def new_row(self, matrice, distanza, delta, atomo1, atomo2):
        x1, y1, z1 = matrice[atomo1][1], matrice[atomo1][2], matrice[atomo1][3]
        x2, y2, z2 = matrice[atomo2][1], matrice[atomo2][2], matrice[atomo2][3]
        
        # Vettore unitario (direzione da atomo1 verso atomo2)
        # Nota: per andare VERSO atomo2, il vettore deve essere (x2-x1)
        ux = (x2 - x1) / distanza
        uy = (y2 - y1) / distanza
        uz = (z2 - z1) / distanza
        
        # Nuovo punto spostato
        matrice[atomo1][1] = x1 + delta * ux
        matrice[atomo1][2] = y1 + delta * uy
        matrice[atomo1][3] = z1 + delta * uz
        
        return matrice    


