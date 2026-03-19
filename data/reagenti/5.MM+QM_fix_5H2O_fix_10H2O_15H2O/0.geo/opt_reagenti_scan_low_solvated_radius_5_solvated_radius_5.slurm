#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --account=CNHPC_1700031_0
#SBATCH -p dcgp_usr_prod
#SBATCH --mem=16000MB
#SBATCH --time=12:00:00
#SBATCH --error=opt_reagenti_scan_low_solvated_radius_5_solvated_radius_5.err
#SBATCH --job-name=xtb_orca_opt

ml profile/chem-phys
ml orca/6.0.0--gcc--12.2.0

export XTBEXE=$HOME/xtb/xtb-6.6.1/bin/xtb
export PATH=$(dirname $XTBEXE):$PATH

export OMPI_MCA_opal_wanr_on_missing_libcuda=0

$ORCA_HOME/bin/orca opt_reagenti_scan_low_solvated_radius_5_solvated_radius_5.inp > opt_reagenti_scan_low_solvated_radius_5_solvated_radius_5.out
