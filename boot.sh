#!/bin/bash

PATH_BIN_PYTHON="/usr/bin/python"
PATH_BIN_PIP="$(which pip)"

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PATH_APP="$CURRENT_DIR/app"

param_install=""
install_requirements=false

# If the install command-line param is null, go ahead with install of all
# requirements.txt dependencies

echo "[CAMERA-RPI] Booting."
cd "$PATH_APP"

# Run the service

echo "[CAMERA-RPI] Starting service."

$PATH_BIN_PYTHON boot.py
