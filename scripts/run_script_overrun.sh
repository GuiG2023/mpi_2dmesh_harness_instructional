#!/bin/bash -l
#SBATCH --constraint=cpu
#SBATCH --nodes=4
#SBATCH --time=00:30:00
#SBATCH --qos=overrun
#SBATCH --account=m3930

export input="../data/zebra-gray-int8-4x"
export xsize=7112
export ysize=5146

mkdir -p ../results

echo "=== CSC 746 CP#6 Performance Testing ==="
echo "Start time: $(date)"

for P in 4 9 16 25 36 49 64 81
   do
   for decomp in 1 2 3
      do
       case $decomp in
          1) decomp_name="row-slab";;
          2) decomp_name="column-slab";;  
          3) decomp_name="tiled";;
      esac

      echo "=== Testing: $P processes, $decomp_name ==="
      echo " srun -n $P $1 -i $input -x $xsize -y $ysize -g $decomp  "
      
      srun -n $P $1 -i $input -x $xsize -y $ysize -g $decomp \
          -o ../results/output_${decomp_name}_${P}procs.raw \
          > ../results/timing_${decomp_name}_${P}procs.log 2>&1
      done
   done
