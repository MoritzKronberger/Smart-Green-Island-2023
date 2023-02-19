#!/usr/bin/env bash
set -e

# Simple .env creation
echo \
"MOCK_IMAGE_PATH=app/assets/pool.jpg
CAMERA=0
PERSPECTIVE_CORRECTION_MARKER_ID=1
PERSPECTIVE_CORRECTION_MARKER_BUFFER_SIZE=100" \
> .env
