#!/usr/bin/env bash

set -xe

# TODO: Remove GCP Account Credentials if empty to use default.

# Check for ML models
shopt -s nullglob dotglob # To include hidden files
files=($SKIPTHOUGHTS_MODELS_PATH*)
if [ ${#files[@]} -gt 0 ]; then 
  echo "Models volume is mounted." 
else
  # Mount GCS bucket.
  gcsfuse \
    -o nonempty \
    -o allow_other \
    "$GCS_BUCKET" "$GCS_MOUNT_ROOT"

  echo "Downloading models to container..."
  cp -r "$GCS_MOUNT_ROOT/models" "$SKIPTHOUGHTS_MODELS_PATH";
fi

python main.py