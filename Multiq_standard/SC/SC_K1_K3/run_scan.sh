#!/bin/bash
set -e

export OMP_NUM_THREADS=1

seq 0 5 | parallel -j $(nproc) '
    mkdir -p job_{} &&
    cp in.elastic init.mod potential.mod displace.mod structure_sc.data job_{}/ &&
    cd job_{} && ../Main {} $(({}+1)) results.csv
'

head -1 job_0/results.csv > results_all.csv
tail -n +2 -q job_*/results.csv >> results_all.csv

echo "Fatto. Righe totali (incl. intestazione):"
wc -l results_all.csv

rm -rf job_*
