#!/bin/bash

dr=../../glamod-ingest
source_files=${dr}/counts.lite_2_0.land.[023].txt
input_file=./land-counts.txt

first_file=$(echo $source_files | cut -d' ' -f1)

head -1 $first_file > $input_file

cat $source_files | grep -v report_type, >> $input_file
echo "[INFO] Wrote input file: $input_file of length $(wc -l $input_file)"

output_file=./constraints-land.json

python minimise-constraints.py -v -i $input_file -o $output_file

#input_file=${dr}/counts.marine.0.txt
#output_file=./constraints-marine.json

#python minimise-constraints.py -i $input_file -o $output_file

