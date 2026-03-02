import  numpy as np
import math

class WorkOnMatrix:
    def calc_dist(self, matrice, atomo1, atomo2):
        """
        Calcola la distanza euclidea tra due atomi nella matrice.
        matrice   : lista di liste [[atomo, x, y, z], ...]
        atomo1    : indice del primo atomo
        atomo2    : indice del secondo atomo
        intero    : se True ritorna la distanza come int, altrimenti float
        """
        # estrai le coordinate dei due atomi
        x1, y1, z1 = matrice[atomo1][1], matrice[atomo1][2], matrice[atomo1][3]
        x2, y2, z2 = matrice[atomo2][1], matrice[atomo2][2], matrice[atomo2][3]

        # calcolo distanza euclidea
        distanza = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        print(distanza)
        return distanza, atomo1, atomo2 
    
    def passi (self,atomo1, atomo2,passo,distanza):
        delta = distanza/passo
        if not isinstance(delta, int):
            print (f'non è un intero {delta}')
        return delta

    def new_row(self,matrice,distanza,delta,atomo1, atomo2):
        x1, y1, z1 = matrice[atomo1][1], matrice[atomo1][2], matrice[atomo1][3]
        x2, y2, z2 = matrice[atomo2][1], matrice[atomo2][2], matrice[atomo2][3]
        # vettore unitario
        ux, uy, uz = (x1-x2)/distanza, (y1-y2)/distanza, (z1-z2)/distanza
        # nuovo punto spostato verso coord2
        matrice[atomo1][1] = matrice[atomo1][1] + delta * ux
        matrice[atomo1][2] = matrice[atomo1][2] + delta * uy
        matrice[atomo1][3] = matrice[atomo1][3] + delta * uz

        return matrice

