#!/bin/bash

# Remote destinations
DESTS=("austin@10.0.0.2" "austin@10.0.0.11" "austin@10.0.0.13" "austin@10.0.0.9" "austin@10.0.0.25")

# Remote directory
REMOTE_DIR="/home/austin/Desktop/canary3"

# Loop through each destination and execute the command
for DEST in "${DESTS[@]}"; do
    echo "Accessing $DEST and running python3 control.py"
    ssh $DEST "cd $REMOTE_DIR && python3 control.py"
done
