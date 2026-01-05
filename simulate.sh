#! /bin/bash
rm -rf results
mkdir -p results
python3 simulator_runner.py
./genplots.sh
Rscript graph_summary.R
