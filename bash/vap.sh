#!/bin/bash
#SBATCH --account=def-robertf
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-user=christian.poitras@ircm.qc.ca
#SBATCH --mail-type=ALL

runvap
runvap -s merge.txt
