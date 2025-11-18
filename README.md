# CSC 746 CP6 — Distributed Sobel Filter with Halo Cells  
**Author:** Guiran Liu  
**Course:** CSC 746, Fall 2025 — San Francisco State University  

---

##  Overview
This project extends the **mpi-2dmesh-harness-instructional** framework to implement a distributed-memory **Sobel edge-detection filter** using MPI.  
It evaluates three domain decomposition strategies — **row-slab**, **column-slab**, and **tiled** — across eight concurrency levels (4–81 ranks).  
An extended **halo-cell implementation** eliminates visible seams at tile boundaries and validates correctness with minimal communication overhead.  
All performance results in the accompanying report  
**_Performance and Correctness Analysis of Distributed Sobel Stencil Operations with Halo Cells_**  
were obtained using this halo-enabled version.

---

##  Environment (NERSC Perlmutter)
```bash
module load cpu
module load python
export CC=cc
export CXX=CC
export MPICH_GPU_SUPPORT_ENABLED=0
```
**Hardware:** 4 Perlmutter CPU nodes (Dual AMD EPYC 7763)  
**Compiler:** g++/mpic++ (GNU 7.5.0)  
**OS:** Ubuntu 22.04 / NERSC CPU partition  

---

##  Build Instructions
```bash
mkdir build && cd build
cmake ..
make -j
```
If rebuilding after an environment change, remove the `build/` directory first.  

---

## 🚀 Running the Program

### Example interactive run on one node
```bash
salloc --nodes 1 --qos interactive --time 00:30:00 --constraint cpu --account=m3930
srun -n 16 ./mpi_2dmesh -i ../data/zebra-gray-int8-4x -x 7112 -y 5146 -g 3
```

### Batch automation (to reproduce all report results)
```bash
bash ../scripts/run_script.sh ./mpi_2dmesh
```
The script iterates over all concurrencies (4–81) and decompositions (1=row, 2=column, 3=tiled).  
Timing logs and output images are written to `../results/`.

Example output filenames:
```
../results/output_tiled_81procs.raw
../results/timing_tiled_81procs.log
```

---

## Input Data
Input files are from the HW6 harness data directory:
```
../data/zebra-gray-int8-4x  (7112 × 5146 grayscale)
```
Large data files are excluded from the submission but can be reused from the course harness.

---

##  Output and Visualization
To visualize the output `.raw` images in grayscale:
```bash
python ../scripts/imshow.py ../results/output_tiled_81procs.raw 7112 5146
```
>  Make sure to enable X11 tunneling when connecting to Perlmutter:  
> `ssh -Y username@perlmutter-p1.nersc.gov`

---

## Extra Credit — Halo Cells Implementation
The halo-enabled version expands each tile’s input buffer by one pixel on all sides.  
During the **scatter** phase, Rank 0 sends `(width+2) × (height+2)` buffers including halo padding.  
Each rank processes its tile using halo coordinates `(i+1, j+1)`, and the **gather** phase returns only the core `(width × height)` region.  
This eliminates seams at tile boundaries and increases scatter payloads by less than 3 %, with no measurable runtime cost.


---

##  Reproducing Report Results
1. **Build** the project as described above.  
2. **Submit batch runs** using `../scripts/run_script.sh`.  
3. **Collect timing logs** from `../results/timing_*.log`.  
4. (Optional) **Visualize** halo correctness using  
   ```bash
   python ../scripts/imshow.py ../results/output_tiled_81procs.raw 7112 5146
   ```

---

##  References
1. [NERSC Perlmutter System Overview (CPU Partition)](https://www.nersc.gov/users/systems/perlmutter/)  
2. [SFSU Bethel Instructional MPI 2D Mesh Harness](https://github.com/SFSU-Bethel-Instructional/mpi_2dmesh_harness_instructional)

---

##  Notes
This project satisfies all requirements of **CSC 746 CP6** including the extra-credit halo implementation.  
Please refer to the accompanying PDF report for detailed performance data, analysis, and figures.
