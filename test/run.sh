#!/bin/bash

if [ -z $1 ]; then
    echo "POKY_DIR path is required"
    exit 1
fi

POKY_DIR="$1"
BUILD_RES="$HOME/build-res"
POKY_URL="git://git.yoctoproject.org/poky.git"
POKY_BUNDLE="$BUILD_RES/poky.bundle"
CPUS="$(nproc --all)"
SCRIPTFILE=$(realpath $0)
META_TESTING_DIR="$(dirname $(dirname $SCRIPTFILE))"
META_TEST_DIR="$(dirname $(dirname $SCRIPTFILE))/test/meta-test"

if [ -d $POKY_DIR ]; then
    echo "Remove the existing directory. ($POKY_DIR)"
    rm -rf $POKY_DIR
fi

echo "$0: Prepare poky bundle"
if [ ! -f $POKY_BUNDLE ]; then
    echo "Unable to locate the poky bundle."
    TEMPDIR=$(mktemp -d)
    git clone $POKY_URL $TEMPDIR
    git --git-dir=$TEMPDIR/.git bundle create $POKY_BUNDLE --all
    rm -rf $TEMPDIR
fi

echo "$0: Clone the poky workspace"
git clone $POKY_BUNDLE $POKY_DIR

echo "$0: sourcing the oe-init-build-env"
. $POKY_DIR/oe-init-build-env

bitbake-layers add-layer $META_TESTING_DIR
bitbake-layers add-layer $META_TEST_DIR

echo "$0: update conf/local.conf"
{
    echo "MACHINE = \"qemuarm64\""
    echo "DL_DIR = \"${BUILD_RES}/downloads\""
    echo "SSTATE_DIR = \"${BUILD_RES}/sstate-cache\""
    echo "BB_GENERATE_MIRROR_TARBALLS = \"1\""
    echo "BB_NUMBER_THREADS = \"${CPUS}\""
    echo "PARALLEL_MAKE = \"-j ${CPUS}\""
} >> ./conf/local.conf

echo "$0: populate the sdk"
bitbake core-image-minimal -c populate_sdk
