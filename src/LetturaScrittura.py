class LetturaScrittura:
    def __init__(self, file_name):
        self.matrix = []  # attributo accessibile dall’esterno
        self.leggi(file_name)

    def leggi(self, file_name):
        """Legge un file XYZ e salva i dati in self.matrix"""
        with open(file_name, 'r') as f:
            lines = f.readlines()
        
        # Salta le prime due righe (numero atomi + commento)
        for line in lines[2:]:
            parts = line.strip().split()
            if len(parts) == 4:
                atomo = parts[0]
                x, y, z = map(float, parts[1:4])
                self.matrix.append([atomo, x, y, z])
        
    def testa(self, funzionale, basis_set, carica, molteplicità, solvent=None, dispersion=None):
    
        head = f"#p opt {funzionale}/{basis_set}"
    
        if solvent:
            head += f" scrf=(cpcm,solvent={solvent})"
        
        if dispersion:
            head += f" empiricaldispersion={dispersion}"
    
        head += "\n\n"
        head += "Title Card Required\n\n"
        head += f"{carica} {molteplicità}\n"
    
        return head 
    
    def scrivi_input(self, head, matrice):
    
        righe_xyz = []
    
        for atomo in matrice:
            simbolo = atomo[0]
            x = atomo[1]
            y = atomo[2]
            z = atomo[3]
        
            righe_xyz.append(f"{simbolo}  {x:.6f}  {y:.6f}  {z:.6f}")
    
        xyz = "\n".join(righe_xyz)
    
        com = head + xyz + "\n\n"   # riga vuota finale obbligatoria per Gaussian
    
        return com