#!/bin/bash
#SBATCH -p all
#SBATCH --ntasks=256
#SBATCH --job-name=bagpipes
#SBATCH --time=24:00:00
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=NONE
#SBATCH --mail-user=adamc@roe.ac.uk

module purge
cd /home/adamc
source .bash_profile

cd ${SLURM_SUBMIT_DIR}

mpirun -n 256 python fit_egs_vary_redshifts.py
