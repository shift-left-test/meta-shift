#!/bin/bash

# This is a simple helper script to prepare yocto project environment for testing purpose.

while getopts ":w:b:" options; do
    case "$options" in
	w) WORKSPACE="$OPTARG"
	   ;;
	b) TARGET_BRANCH="$OPTARG"
	   ;;
	:)
	    echo "Not enough arguments"
	    exit 1
	    ;;
	*)
	    echo "Invalid arguments"
	    exit 1
    esac
done

POKY_URL="http://mod.lge.com/hub/yocto/poky.git"
META_OE_URL="http://mod.lge.com/hub/yocto/meta-openembedded.git"
META_TEMP_URL="http://mod.lge.com/hub/yocto/meta-temp.git"
CPUS="$(nproc --all)"
TOPDIR=$(dirname $(dirname $(dirname $(realpath $0))))

if [ -d $WORKSPACE ]; then
    echo "Remove the existing workspace: $WORKSPACE"
    rm -rf $WORKSPACE
fi

echo "Clone the git repositories"
git clone $POKY_URL -b $TARGET_BRANCH $WORKSPACE
git clone $META_OE_URL -b $TARGET_BRANCH $WORKSPACE/meta-openembedded
git clone $META_TEMP_URL $WORKSPACE/meta-temp

echo "Construct meta-layers"
. $WORKSPACE/oe-init-build-env $WORKSPACE/build

bitbake-layers add-layer $WORKSPACE/meta-openembedded/meta-oe
bitbake-layers add-layer $WORKSPACE/meta-openembedded/meta-python
bitbake-layers add-layer $TOPDIR
bitbake-layers add-layer $WORKSPACE/meta-temp

echo "Update build/conf/local.conf"
{
    echo "CORE_IMAGE_EXTRA_INSTALL += \"cpp-project\""
    echo "MACHINE = \"qemuarm64\""
    echo "DL_DIR = \"$HOME/build-res/downloads\""
    echo "SSTATE_DIR = \"$HOME/build-res/sstate-cache\""
    echo "BB_GENERATE_MIRROR_TARBALLS = \"1\""
    echo "BB_NUMBER_THREADS = \"${CPUS}\""
    echo "PARALLEL_MAKE = \"-j ${CPUS}\""
} >> $WORKSPACE/build/conf/local.conf
