#! /bin/bash

# Installs Cloudhands in a local venv. Runs unit tests and PEP8 checks.
# eg:
# $ check.sh --novenv --nopep8

#PYTHON=/usr/local/bin/python3.3
PYTHON=`which python3.3`
PYENV=~/pydev-3.3
SETUPTOOLS=setuptools-5.7
PIP=pip-1.4.1

DIR=$( cd "$( dirname "$0" )" && pwd )
PARENT=$(readlink -e $DIR/..)

echoerr() { echo "$@" 1>&2; }

cd $PARENT/cloudhands-ops

if [[ "$*" != *--novenv* ]];
then
    echoerr "Creating $PYENV ..."
    $PYTHON -m venv $PYENV
    #$PYTHON -m venv --clear $PYENV

    tar -xzvf vendor/$SETUPTOOLS.tar.gz
    cd $SETUPTOOLS
    $PYENV/bin/python3 setup.py install
    cd -
    rm -rf $SETUPTOOLS

    tar -xzvf vendor/$PIP.tar.gz
    cd $PIP
    $PYENV/bin/python3 setup.py install
    cd -
    rm -rf $PIP

    $PYENV/bin/pip install \
        --no-index -f file://$PARENT/cloudhands-ops/vendor/ \
    pep8

    #for i in docutils SQLAlchemy pyramid_persona WebTest; do
    for i in docutils SQLAlchemy pyramid; do
        $PYENV/bin/pip install \
        --no-index -f file://$PARENT/cloudhands-ops/vendor/ \
        $i
    done
fi

for i in cloudhands-common cloudhands-burst cloudhands-web \
    cloudhands-jasmin; do
    cd $PARENT/$i

    version=`$PYENV/bin/python setup.py --version`
    echoerr "Installing $i $version from source ..."
    $PYENV/bin/python setup.py install > /dev/null

    if [[ "$*" != *--nopep8* ]];
    then
        $PYENV/bin/pep8 \
        --exclude='.svn,CVS,.bzr,.hg,.git,__pycache__,build,dist' .
    fi

    if [[ "$*" != *--nolint* ]];
    then
        for f in `find . -name "*.py"`; do
            $PYENV/bin/python $PYENV/bin/pylint \
            --rcfile=$PARENT/cloudhands-ops/pylint.rc \
            --errors-only --reports=n $f 2> /dev/null
        done
    fi

    if [[ "$*" != *--notest* ]];
    then
        $PYENV/bin/python -m unittest discover -v cloudhands
    fi
done
