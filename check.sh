#!/bin/bash

# Installs Cloudhands within a local venv. Runs unit tests and PEP8 checks unless
# you say otherwise.
# eg:
# $ ./check.sh --novenv --nopep8

source "$( dirname "$0" )"/common.sh

cd "$PARENT"/cloudhands-ops || die

if [[ "$*" != *--novenv* ]];
then
    echoerr "Creating venv in $PYENV ..."
    #For Python >=3.4 we need the "--without-pip" flag but 3.3 chokes on it
    if [[ $PYVERS = "3.3" ]] ; then
	$PYTHON -m venv $PYENV || die 1 "Creating venv failed."
    else
	$PYTHON -m venv $PYENV --without-pip || die 1 "Creating venv failed."
    fi
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

    if [[ "$*" != *--nopep8* ]] ; then
	$PYENV/bin/pip install --pre \
	    --no-index -f file://$PARENT/cloudhands-ops/vendor/ \
	    pep8 || die "pep8 install failed"
    fi

    #for i in docutils SQLAlchemy pyramid_persona WebTest; do
    for i in docutils SQLAlchemy pyramid Whoosh; do
        $PYENV/bin/pip install --pre \
	    --no-index -f file://$PARENT/cloudhands-ops/vendor/ \
	    $i || die "$i install failed"
    done
fi

for i in cloudhands-common cloudhands-burst cloudhands-web \
    cloudhands-jasmin; do
    cd "$PARENT"/$i || die 1  "Cannot find $i to install"

    # Note that at this point dependencies may be fetched from on-line repos and
    # installed into $PYENV by the setup.py routines.
    version=`$PYENV/bin/python setup.py --version`
    echoerr "Installing $i $version from source ..."
    $PYENV/bin/python setup.py install > /dev/null

    if [[ "$*" != *--nopep8* ]];
    then
	echo "Running pep8 in `pwd`"
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
