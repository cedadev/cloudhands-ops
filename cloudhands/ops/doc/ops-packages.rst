..  Titling
    ##++::==~~--''``

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

cloudhands-jasmin
    Site-specific configuration for the JASMIN infrastructure (private)

cloudhands-ops
    Contains this manual, some operations scripts and experimental code.

Tests and checks
================


.. program:: check.sh

.. option:: --novenv

   Disables the creation of a fresh virtual environment.

Packaging
=========


Staging
=======

Revisions and Versions

    A revision is a commit reference in a code repository (ie: git).
    A version is package metadata which complies with PEP-0386. 

What is a bundle?

A bundle consists of the following:

The Release
    A Python source distribution (tar.gz) for each of the namespace packages in
    the JASMIN project. 
Vendor packages
    A copy of all Python dependency packages (these are to be found in the
    'vendor' directory of ​git@proj.badc.rl.ac.uk:cloudhands-ops) 

How to deploy the bundle?

    Create a fresh Python virtualenv
    Install setuptools and pip from bundle
    Install cloudhands-jasmin package via pip 

What processes to set running?

    LDAP indexer (cloud-index)
    Burst controller (cloud-burst)
    Web server application (cloud-serve) 

Platform requirements

    Python 3.3
    A reverse proxy cache suitable for a RESTful API (must do etags)
    A process management service (eg: upstart, supervisord) 

The software is distributed as several separate packages.

