#!/bin/bash

source setup-env.sh

source_files=/usr/local/database_scripts/src/glamod_ingest/src/query/counts.land.[023].txt
input_file=./land-counts.txt

head -1 /usr/local/database_scripts/src/glamod_ingest/src/query/counts.land.0.txt > $input_file

cat $source_files | grep -v report_type, >> $input_file
echo "[INFO] Wrote input file: $input_file of length $(wc -l $input_file)"

output_file=./constraints-land.json

python minimise-constraints.py -v -i $input_file -o $output_file

input_file=/usr/local/database_scripts/src/glamod_ingest/src/query/counts.marine.0.txt
output_file=./constraints-marine.json

python minimise-constraints.py -i $input_file -o $output_file

