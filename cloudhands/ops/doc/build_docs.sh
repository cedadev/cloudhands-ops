#! /bin/bash

# Builds Cloudhands docs to go.

PYTHON=/usr/local/bin/python3.4
PYENV=~/pyops-3.3

DIR=$( cd "$( dirname "$0" )" && pwd )
PARENT=$(readlink -e $DIR/../../../..)

echoerr() { echo "$@" 1>&2; }

cd $PARENT/cloudhands-ops

echoerr "Installing package to $PYENV ..."
$PYENV/bin/python3 setup.py install > /dev/null

echoerr "Building project documentation ..."
$PYENV/bin/sphinx-build -b html \
    -c $PARENT/cloudhands-ops/cloudhands/ops/doc \
    $PARENT/cloudhands-ops/cloudhands/ops/doc \
    $PARENT/cloudhands-ops/cloudhands/ops/doc/html


