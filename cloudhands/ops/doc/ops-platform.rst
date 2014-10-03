..  Titling
    ##++::==~~--''``

Establishing operations environments
::::::::::::::::::::::::::::::::::::

There are two working environments required for operating a `cloudhands`
installation:

1. `The build environment`_ is a place to build software packages. This is
   necessary every time a provider configuration changes or a new operations
   script is written.

2. `The administration environment`_ is a place from which to monitor and
   administer a running installation.

.. _build-environment:

The build environment
=====================

First follow these procedures:

* `Install platform requirements`_
* `Create a non-privileged account`_
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

* `Install platform requirements`_
* `Create a non-privileged account`_
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

Common operations
=================

Install platform requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The reference platform is Red Hat Enterprise Linux 6.5 with Python 3.3 from RPMs.
To install Python 3.3 on a RHEL platform, execute the following commands::

    $ wget http://jur-linux.org/download/el-updates/6/x86_64/python3-3.3.2-2.el6.x86_64.rpm
    $ wget http://jur-linux.org/download/el-updates/6/x86_64/python3-libs-3.3.2-2.el6.x86_64.rpm

Then, as superuser::

    $ yum localinstall -y python3-3.3.2-2.el6.x86_64.rpm python3-libs-3.3.2-2.el6.x86_64.rpm

Create a non-privileged account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an account for portal operation like this::

    $ adduser jasminportal

Add your public key to ``/home/jasminportal/.ssh/authorized_keys`` to enable
`ssh` access.

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

Outcome
-------

The `dist` directory of each JASMIN package will contain a Python source
distribution (`tar.gz`).

