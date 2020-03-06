#!/bin/bash

while getopts ":w:c:" options; do
    case "$options" in
	w)
	    WORKSPACE="$OPTARG"
	   ;;
	c)
	    COMMAND="$OPTARG"
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

if [ ! -f $WORKSPACE/oe-init-build-env ]; then
    echo "Unable to locate $WORKSPACE/oe-init-build-env"
    exit 1
fi

. $WORKSPACE/oe-init-build-env $WORKSPACE/build

eval $COMMAND
