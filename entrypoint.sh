#!/usr/bin/env bash

set -xe

## DISABLED: Due to `cp: error reading '/mnt/gcsfuse/models/bi_skip.npz': Input/output error`
## Check for ML models
# shopt -s nullglob dotglob # To include hidden files
# files=($SKIPTHOUGHTS_MODELS_PATH*)
# if [ ${#files[@]} -gt 0 ]; then 
#   echo "Models volume is mounted." 
# else
#   # Mount GCS bucket.
#   gcsfuse \
#     -o nonempty \
#     -o allow_other \
#     "$GCS_BUCKET" "$GCS_MOUNT_ROOT"

#   echo "Downloading models to container..."
#   cp -r "$GCS_MOUNT_ROOT/models" "$SKIPTHOUGHTS_MODELS_PATH";
# fi

## GPU Enabled
# THEANO_FLAGS='floatX=float32,device=cuda,gpuarray.preallocate=1,force_device=True' 

python main.py