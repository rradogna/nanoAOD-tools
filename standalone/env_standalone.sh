#!/bin/bash

# Please setup python 2.7 and ROOT into your environment first

CWD=$PWD
if [ ${0:0:1} == "/" ]; then
    FULLPATH=$0
else
    FULLPATH=$PWD/$0
fi
cd ${FULLPATH/%env_standalone.sh/}/..

if [ -f standalone/env_standalone.sh ]; then
    if [ ! -d build ]; then
	if [ x${1} = 'xbuild' ]; then
            mkdir -p build/lib/python/PhysicsTools
            ln -s ../../../../python build/lib/python/PhysicsTools/NanoAODTools
	    echo "Build directory created, please source again standalone/env_standalone.sh without the build argument."
	else
	    echo "Build directory is not yet present, please source again standalone/env_standalone.sh with the build argument."
	fi
    else
	if [ x${1} = 'xbuild' ]; then
	    echo "Build directory is already present, please source again standalone/env_standalone.sh without the build argument."
	else
	    find build/lib/python python -type d -execdir touch '{}/__init__.py' \;
	    export NANOAODTOOLS_BASE=${PWD}
	    export PYTHONPATH=${NANOAODTOOLS_BASE}/build/lib/python:${PYTHONPATH}
	    echo "Standalone environment set."
	fi
    fi
    cd $CWD
else
    echo "Error in moving to the NanoAODTools directory to setup the standalone environment"
    cd $CWD
fi

