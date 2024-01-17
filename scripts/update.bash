#!/bin/bash

# Source and destination directories
SRC_DIR="/home/austin/Desktop/canary3"

DEST0="austin@10.0.0.2:/home/austin/Desktop/canary3"
DEST1="austin@10.0.0.11:/home/austin/Desktop/canary3"
DEST2="austin@10.0.0.13:/home/austin/Desktop/canary3"
DEST3="austin@10.0.0.9:/home/austin/Desktop/canary3"
DEST4="austin@10.0.0.25:/home/austin/Desktop/canary3"

# Copying files from source to destination
scp -r $SRC_DIR $DEST0
scp -r $SRC_DIR $DEST1
scp -r $SRC_DIR $DEST2
scp -r $SRC_DIR $DEST3
scp -r $SRC_DIR $DEST4
