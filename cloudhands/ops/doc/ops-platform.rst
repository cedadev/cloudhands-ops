..  Titling
    ##++::==~~--''``

Establishing operations environments
::::::::::::::::::::::::::::::::::::

There are two working environments required for operating a `cloudhands`
installation:

1. `The build environment`_ is a place to build software packages. This is
   necessary whenever:

    * new code is to be released
    * a provider configuration changes
    * you write or modify an operations script.

2. `The administration environment`_ is a place from which to monitor and
   administer a running installation.

.. _build-environment:

The build environment
=====================

First follow these procedures:

* :ref:`install-platform`
* :ref:`portal-account`
*  Log in as non-privileged user

Check out the source code of the following packages from the locations shown
at the beginning of the :ref:`operations-guide`:

* cloudhands-burst
* cloudhands-common
* cloudhands-jasmin
* cloudhands-ops
* cloudhands-web

Change directory to the `cloudhands-ops` package::

    $ cd src/cloudhands-ops

Run the `check.sh`_ script to establish a working build environment::

    $ ./check.sh --nolint --nopep8 --notest

Run the `build.sh`_ script to create the documentation::

    $ ./build.sh --novenv --nopush --nosign --nobundle

The administration environment
===============================

First follow these procedures:

* :ref:`install-platform`
* :ref:`portal-account`
*  Log in as non-privileged user

Check out the source code of the following packages from the locations shown
at the beginning of the :ref:`operations-guide`:

* cloudhands-common
* cloudhands-jasmin
* cloudhands-ops

Create a Python virtual environment, and visit the cloudhands-ops `vendor`
directory::

    $ python3.3 -m venv pyops-3.3
    $ cd ~/src/cloudhands-ops/vendor

Install `setuptools` from the vendor directory::

    $ tar -xzvf setuptools-5.7.tar.gz
    $ cd setuptools-5.7
    $ ~/pyops3.3/bin/python3 setup.py install

Install `pip` from the vendor directory::

    $ tar -xzvf /pip-1.4.1.tar.gz
    $ cd pip-1.4.1
    $ ~/pyops3.3/bin/python3 setup.py install

Install the packages required for cloudhands administration::

    $ ~/pyops3.3/bin/pip install --use-wheel --no-index \
      -f file:///home/jasminportal/src/cloudhands-ops/vendor \
      -r ops-requirements.txt

Reference
=========

.. _check-script:

Check.sh
~~~~~~~~

The `check.sh` script creates a Python virtual environment and installs the
JASMIN software along with all its dependencies. It then runs Unit Tests and
PEP8 checks.

Options
-------

.. program:: check.sh

.. option:: --novenv

   Disables the creation of a fresh virtual environment.

.. option:: --nopep8

   Disables the PEP8 checks.

.. option:: --notest

   Disables the unit tests.

Outcome
-------

The following JASMIN executables will be installed in ``~/pyops-3.3/bin``:

* LDAP indexer (``cloud-index``)
* Burst controller (``cloud-burst``)
* Identity controller (``cloud-identity``)
* Web server application (``cloud-webserve``) 
* Web server demo (``cloud-demoserve``) 

.. _build-script:

Build.sh
~~~~~~~~

The `build.sh` script creates the HTML version of this manual and builds a
source distribution for each of the JASMIN packages.

Options
-------

.. program:: build.sh

.. option:: --novenv

   Disables the creation of a fresh virtual environment.

.. option:: --nopush

   Disables pushing source trees back to Git repositories.

.. option:: --nosign

   Disables GPG signing of packages.

.. option:: --nobundle

   Disables the creation of the bundle.

Outcome
-------

The `dist` directory of each JASMIN package will contain a Python source
distribution (`tar.gz`).

