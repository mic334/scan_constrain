import os 

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
        
    def testa_orca_xtb(self, hamiltonian, carica, molteplicità, nproc, mem, solvent=None, Constraint=None):
        if solvent:
            head_orca = f"!opt {hamiltonian} alpb({solvent})\n"
        else:
            head_orca = f"!opt {hamiltonian}\n"

        head_orca += f"%pal nprocs {nproc} end\n"
        head_orca += f"%maxcore {mem * 1000}\n"

        if Constraint:
            head_orca += f"%geom Constraints {{\n{Constraint}\n}}\n end\n end"

        head_orca += f"\n* xyz {carica} {molteplicità}\n"

        for atomo, x, y, z in self.matrix:
            head_orca += f"{atomo} {x} {y} {z}\n"

        head_orca += "*\n"

        return head_orca
    

    def testa(self, funzionale, basis_set, carica, molteplicità,nproc,mem,solvent=None, dispersion=None):
        
        head = f"%nproc={nproc}"
        head += f"\n%mem={mem}GB\n"
        head += f"#p opt(addredundant) {funzionale}/{basis_set}"
    
        if solvent:
            head += f" scrf=(cpcm,solvent={solvent})"
        
        if dispersion:
            head += f" empiricaldispersion={dispersion}"
    
        head += "\n\n"
        head += "Title Card Required\n\n"
        head += f"{carica} {molteplicità}\n"
    
        return head 

    def scrivi_input(self, head, matrice, atomo1, atomo2):
    
        righe_xyz = []

        # 1. Coordinate pulite (standard XYZ)
        for atomo in matrice:
            simbolo, x, y, z = atomo[0], atomo[1], atomo[2], atomo[3]
            righe_xyz.append(f"{simbolo}  {x:.6f}  {y:.6f}  {z:.6f}")

        xyz = "\n".join(righe_xyz)

        # 2. Vincolo di LEGAME (B = Bond, F = Freeze)
        # Ricorda: Gaussian conta gli atomi partendo da 1, non da 0
        coda_vincoli = f"B {atomo1 + 1} {atomo2 + 1} F"

        # 3. Composizione finale
        # Nota: Gaussian esige una riga vuota dopo le coordinate 
        # e una riga vuota dopo i vincoli per chiudere il file.
        com = f"{head}{xyz}\n\n{coda_vincoli}\n\n"
        return com
    
    def aggiungi_vincoli_coda(self, com_string, target_atomi):
        # target_atomi: iterabile di indici Python (0-based)
        #           es: [2,3] oppure range(20,27)

        # Se è un singolo int lo trasformo in lista
        if isinstance(target_atomi, int):
            target_atomi = [target_atomi]

        nuove_righe = []

        # Gaussian conta da 1
        for idx in target_atomi:
            nuove_righe.append(f"X {idx + 1} F")

        stringa_vincoli = "\n".join(nuove_righe)

        com_pulito = com_string.strip()

        # Coordinate + riga vuota + vincoli + riga vuota finale
        return f"{com_pulito}\n{stringa_vincoli}\n\n"

    def genera_slurm(self, programma,input_file, nproc, tempo, memoria):

        if programma.lower() == "gaussian":
            base_name = os.path.splitext(input_file)[0]

            script = f"""#!/bin/bash

#SBATCH -N1 -n1 -c{nproc}
#SBATCH --time={tempo}
#SBATCH --mem={memoria}
#SBATCH --error %J.err
#SBATCH --output %J.out
#SBATCH --account=CNHPC_1700031_0
#SBATCH --partition=dcgp_usr_prod
#SBATCH --job-name={base_name}

module load autoload
module load profile/chem-phys
module load g16/c02

. $g16root/g16/bsd/g16.profile

export GAUSS_SCRDIR=$CINECA_SCRATCH/g16_$SLURM_JOBID
mkdir -p $GAUSS_SCRDIR

g16 -p="{nproc}" < {input_file} > {base_name}.log
"""

        elif programma.lower() == "orca":
            base_name = os.path.splitext(input_file)[0]

            script = f"""#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node={nproc}
#SBATCH --cpus-per-task=1
#SBATCH --account=CNHPC_1700031_0
#SBATCH -p dcgp_usr_prod
#SBATCH --mem={memoria*1000}MB
#SBATCH --time={tempo}
#SBATCH --error={os.path.splitext(os.path.basename(input_file))[0]}.err
#SBATCH --job-name=xtb_orca_opt

ml profile/chem-phys
ml orca/6.0.0--gcc--12.2.0

export XTBEXE=$HOME/xtb/xtb-6.6.1/bin/xtb
export PATH=$(dirname $XTBEXE):$PATH

export OMPI_MCA_opal_wanr_on_missing_libcuda=0

$ORCA_HOME/bin/orca {os.path.basename(input_file)} > {os.path.splitext(os.path.basename(input_file))[0]}.out
"""
        return script