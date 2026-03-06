#!/bin/bash

#SBATCH -N1 -n1 -c12
#SBATCH --time=24:00:00
#SBATCH --mem=12000MB
#SBATCH --error %J.err
#SBATCH --output %J.out
#SBATCH --account=CNHPC_1700031_0
#SBATCH --partition=dcgp_usr_prod
#SBATCH --job-name=1

module load autoload
module load profile/chem-phys
module load g16/c02

. $g16root/g16/bsd/g16.profile

export GAUSS_SCRDIR=$CINECA_SCRATCH/g16_$SLURM_JOBID
mkdir -p $GAUSS_SCRDIR

g16 -p="12" < 1.com > 1.log
