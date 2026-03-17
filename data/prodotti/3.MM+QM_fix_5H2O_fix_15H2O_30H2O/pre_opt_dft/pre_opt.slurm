#!/bin/bash

#SBATCH -N1 -n1 -c24
#SBATCH --time=12:00:00
#SBATCH --mem=24GB
#SBATCH --error %J.err
#SBATCH --output %J.out
#SBATCH --account=CNHPC_1700031_0
#SBATCH --partition=dcgp_usr_prod
#SBATCH --job-name=pre_opt

module load autoload
module load profile/chem-phys
module load g16/c02

. $g16root/g16/bsd/g16.profile

export GAUSS_SCRDIR=$CINECA_SCRATCH/g16_$SLURM_JOBID
mkdir -p $GAUSS_SCRDIR

g16 -p="24" < pre_opt.com > pre_opt.log
