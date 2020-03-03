#!/bin/bash

if [ -z $1 ]; then
    echo "POKY_DIR path is requried"
    exit 1
fi

POKY_DIR="$1"

. $POKY_DIR/oe-init-build-env
bitbake -s

