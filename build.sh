#! /bin/bash

# Builds Cloudhands packages to go. Outputs the source package names.
# eg:
# $ build.sh --novenv --nopush --nosign > build.out

PYTHON=/usr/local/bin/python3.3
PYENV=~/pyops-3.3
SETUPTOOLS=setuptools-1.3.1
PIP=pip-1.4.1

DIR=$( cd "$( dirname "$0" )" && pwd )
PARENT=$(readlink -e $DIR/..)

echoerr() { echo "$@" 1>&2; }

cd $PARENT/cloudhands-ops

if [[ "$*" != *--nopush* ]];
then
    echo git push
fi

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
        Sphinx

    for i in execnet radon; do
        $PYENV/bin/pip install \
        --no-index -f file://$PARENT/cloudhands-ops/vendor/ \
        $i
    done
fi

echoerr "Installing Ops package to $PYENV ..."
$PYENV/bin/python3 setup.py install > /dev/null

echoerr "Building Ops guide ..."
$PYENV/bin/sphinx-build -c $PARENT/cloudhands-ops/cloudhands/ops/doc \
    $PARENT/cloudhands-ops/cloudhands/ops/doc \
    $PARENT/cloudhands-ops/cloudhands/ops/doc/html

#echoerr "Creating web guide ..."
#$PYENV/bin/python3 -m cloudhands.ops.scripts.webdoc --parent=$PARENT \
#    > $PARENT/cloudhands-web/cloudhands/web/static/html/guide.html

echoerr "Creating source packages ..."
for i in cloudhands-common cloudhands-burst cloudhands-jasmin cloudhands-web; do
    cd $PARENT/$i
    rm -rf dist
    rm -rf build

    if [[ "$*" != *--nopush* ]];
    then
        git push
    fi

    proj=$(basename `pwd`)
    $PYENV/bin/python3 setup.py sdist > /dev/null
    for pkg in `ls dist/$proj*.tar.gz`; do
        echo `basename $pkg`

        if [[ "$*" != *--nosign* ]];
        then
            gpg --armor --detach-sign --yes $pkg
        fi

    done
done
