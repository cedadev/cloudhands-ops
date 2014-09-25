#! /bin/bash

# Builds Cloudhands packages to go. Outputs the source package names.
# eg:
# $ build.sh --novenv --nopush --nosign > build.out

source "$( dirname "$0" )"/common.sh

cd $PARENT/cloudhands-ops

if [[ "$*" != *--nopush* ]];
then
    echo git push
fi

# --novenv means don't try to create the venv or install Sphinx/execnet/radon.
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

    for i in sphinx-argparse execnet radon; do
        $PYENV/bin/pip install \
        --no-index -f file://$PARENT/cloudhands-ops/vendor/ \
        $i
    done
fi

$PYENV/bin/pip uninstall -y cloudhands-ops
echoerr "Installing Ops package to $PYENV ..."
$PYENV/bin/python3 setup.py install > /dev/null
$PYENV/bin/python3 -m unittest cloudhands.ops.test.test_orgadmin

echoerr "Building Ops guide ..."
rm -rf $PARENT/cloudhands-ops/cloudhands/ops/doc/html
$PYENV/bin/sphinx-build -c $PARENT/cloudhands-ops/cloudhands/ops/doc \
    $PARENT/cloudhands-ops/cloudhands/ops/doc \
    $PARENT/cloudhands-ops/cloudhands/ops/doc/html

#echoerr "Creating web guide ..."
#$PYENV/bin/python3 -m cloudhands.ops.scripts.webdoc --parent=$PARENT \
#    > $PARENT/cloudhands-web/cloudhands/web/static/html/guide.html

if [[ "$*" != *--nobundle* ]];
then
    BUNDLE=jasmin-bundle.tar
    echoerr "Gathering vendor packages."
    tar -cf $PARENT/cloudhands-ops/$BUNDLE -C $PARENT/cloudhands-ops/vendor .
fi

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
        distrbn=`basename $pkg`
        echo $distrbn

        if [[ "$*" != *--nosign* ]];
        then
            gpg --armor --detach-sign --yes $pkg
        fi

        if [[ "$*" != *--nobundle* ]];
        then
            tar -rf $PARENT/cloudhands-ops/$BUNDLE -C $PARENT/$i/dist $distrbn
        fi

    done
done
