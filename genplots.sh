#! /bin/bash
rm -rf plots
mkdir -p plots
for f in `ls results/*.dat`; do
  STRATEGY=`echo "$f" | sed 's/results\///' | sed 's/\..*//'`
  Rscript graph.R $f $STRATEGY
done
