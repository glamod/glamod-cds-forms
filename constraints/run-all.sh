#!/bin/bash

python minimise-constraints.py -v -i ../../glamod-ingest/matches.lite_2_0.land.023 -o constraints-land.json

python minimise-constraints.py -v -i ../../glamod-ingest/matches.lite_2_0.marine.0 -o constraints-marine.json
