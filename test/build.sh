#!/bin/bash
if [[ -z ${1} ]]; then
    echo "Missing the configuration argument."
    echo "./build.sh <config> <build>"
    exit 1
fi
if [[ -z ${2} ]]; then
    echo "Missing the build directory argument."
    echo "./build.sh <config> <build>"
    exit 1
fi

./test/mini-mcf.py -c test/conf/${1} -d ${2} || exit 1
source /tmp/meta-shift-repos-sunggon82.kim/poky/oe-init-build-env ${2}
export BB_ENV_EXTRAWHITE="$BB_ENV_EXTRAWHITE DL_DIR SSTATE_DIR"
bitbake core-image-minimal -c fetchall
bitbake core-image-minimal
bitbake core-image-minimal -c reportall
bitbake core-image-minimal -c populate_sdk
