#!bash

# This sets up some common variables and functions for both check.sh and build.sh
# and is source'd at the top of both scripts.

echoerr() { echo "$@" 1>&2 ; }
die() { s=${1:-1} ; shift ; echo "${@:-died}" 2>&1 ; exit "$s" ; }

#Find python 3.3 or 3.4.
PYTHON=`{ which python3.3 || which python3.4 ; } | tail -n 1`
[ -x "$PYTHON" ] || die 1 "Python 3.3 or 3.4 not found."
[[ $PYTHON =~ [0-9.]*$ ]] && PYVERS=$BASH_REMATCH

#Comment from Tim:
#If a suitable Python.h is not found, installation is going to choke while
#trying to compile bcrypt for cloudhands-web.
#On Debian/Ubuntu I had to apt-get install libpython3.4-dev but I don't know a generic
#way to test if a given installation of Python is ready have C compiled for it. - Eg.
#which "python$PYVERS-config" >&/dev/null || die 1 "No suitable python-config found."

PYENV=~/cloudhands-pyops-$PYVERS
SETUPTOOLS=setuptools-5.7
PIP=pip-1.4.1

# Stop the egg cache from colliding with the default one.
export PYTHON_EGG_CACHE="$PYENV"/.python-eggs

# Assume base dir for cloudhands-* is one above the dir containing this script.
DIR=$( cd "$( dirname "$0" )" && pwd )
PARENT=$(readlink -e "$DIR"/..)
