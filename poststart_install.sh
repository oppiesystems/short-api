#!/usr/bin/env bash

set -xe

mkdir -p /mnt/models
gcsfuse --foreground --debug_gcs --debug_http --debug_fuse --debug_invariants -o nonempty breef-models /mnt/models