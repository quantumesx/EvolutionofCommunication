#!/bin/bash
#SBATCH -J c1r4
#SBATCH -o c1r4.out
#SBATCH --nodes=1
#SBATCH --mail-user=xixu@vassar.edu
#SBATCH --mail-type=ALL

echo make data directory

cd /data/xixu/Evocomm/Data
echo make data directory

mkdir Cond1Run4

echo set home directory

cd /data/xixu/Evocomm

# for every run, change this, the out file name, and the second system param
echo start: condition = 1, run = 4

srun -n 1 -N 1 -o Cond1Run4.out python3 RunExp.py 1 4
