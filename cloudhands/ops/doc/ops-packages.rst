..  Titling
    ##++::==~~--''``

Delivering the code
:::::::::::::::::::

Repositories
============

+-------------------+------------------------------------------+-----------------------------+
| Package           | Repository URL                           | Description                 |
+===================+==========================================+=============================+
| cloudhands-common | git@proj.badc.rl.ac.uk:cloudhands-common | Common types, utilities and |
|                   |                                          | database schema             |
+-------------------+------------------------------------------+-----------------------------+
| cloudhands-web    | git@proj.badc.rl.ac.uk:cloudhands-web    | LDAP indexer and Web portal |
|                   |                                          | application                 |
+-------------------+------------------------------------------+-----------------------------+
| cloudhands-jasmin | git@proj.badc.rl.ac.uk:cloudhands-jasmin | Site-specific configuration |
|                   |                                          | for JASMIN infrastructure   |
|                   |                                          | (private)                   |
+-------------------+------------------------------------------+-----------------------------+
| cloudhands-ops    | git@proj.badc.rl.ac.uk:cloudhands-ops    | Contains this manual, some  |
|                   |                                          | operations scripts and all  |
|                   |                                          | third-party dependencies    |
+-------------------+------------------------------------------+-----------------------------+

This guide assumes the source repositories are checked out under a common
directory `src` as shown::

    src
    |-- cloudhands-burst
    |   `-- cloudhands
    |       `-- burst
    |           |-- main.py
    |           `-- test
    |-- cloudhands-common
    |   `-- cloudhands
    |       `-- common
    |           `-- test
    |-- cloudhands-jasmin
    |   `-- cloudhands
    |       `-- jasmin
    |-- cloudhands-ops
    |   |-- build.sh
    |   |-- check.sh
    |   |-- cloudhands
    |   |   `-- ops
    |   |       `-- doc
    |   |-- design
    |   `-- vendor
    `-- cloudhands-web
        `-- cloudhands
            `-- web
                |-- demo.py
                |-- indexer.py
                |-- main.py
                |-- static
                |   |-- css
                |   `-- img
                |-- templates
                `-- test

The working directory for the operations scripts is ``src/cloudhands-ops``.

Tests and checks
================

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
* Web server application (``cloud-webserve``) 
* Web server demo (``cloud-demoserve``) 

Packaging
=========

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

Staging
=======

Revisions and Versions
~~~~~~~~~~~~~~~~~~~~~~

* A revision is a commit reference in a code repository (ie: git).
* A version is package metadata which complies with PEP-0386. 

The Bundle
~~~~~~~~~~

A bundle consists of the following:

The Release
    A Python source distribution (tar.gz) for each of the namespace packages in
    the JASMIN project.
 
Vendor packages
    A copy of all Python dependency packages (these are to be found in the
    'vendor' directory of ​git@proj.badc.rl.ac.uk:cloudhands-ops) 

How to deploy the bundle?

1. Create a fresh Python virtualenv
2. Install setuptools and pip from bundle
3. Install cloudhands-jasmin package via pip 

Platform requirements
~~~~~~~~~~~~~~~~~~~~~

* Python 3.3
* A reverse proxy cache suitable for a RESTful API (must do etags)
* A process management service (eg: upstart, supervisord) 
