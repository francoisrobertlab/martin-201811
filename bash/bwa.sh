#!/bin/bash
#SBATCH --account=def-robertf
#SBATCH --time=24:00:00
#SBATCH --array=0-0
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --mail-user=christian.poitras@ircm.qc.ca
#SBATCH --mail-type=ALL
#SBATCH --output=bwa-%A_%a.out
#SBATCH --error=bwa-%A_%a.out

if [ -z "$SLURM_ARRAY_TASK_ID" ]
then
  SLURM_ARRAY_TASK_ID=0
fi

# Index FASTA file first
# bwa index sacCer3.fa
runbwa --threads 4 --index $SLURM_ARRAY_TASK_ID $@
