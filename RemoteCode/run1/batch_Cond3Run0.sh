#!/bin/bash
#SBATCH -J c3r0
#SBATCH -o c3r0.out
#SBATCH --nodes=1
#SBATCH -w node1
#SBATCH --mail-user=xixu@vassar.edu
#SBATCH --mail-type=ALL

echo make data directory

cd /data/xixu/Evocomm/Data
echo make data directory

mkdir Cond3Run0

echo set home directory

cd /data/xixu/Evocomm

# for every run, change this, the out file name, and the second system param
echo start: condition = 3, run = 0

srun -n 1 -N 1 -o Cond3Run0.out python3 RunExp.py 3 0
