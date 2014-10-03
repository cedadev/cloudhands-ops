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

The build environment
=====================

First follow these procedures:

* `Install platform requirements`_
* `Create a non-privileged account`_

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

    $ ./build.sh --novenv --nopush --nosign

The administration environment
===============================

First follow these procedures:

* `Install platform requirements`_
* `Create a non-privileged account`_

* $ check.sh
* $ build.sh
* $ publish with droopy
* $ wget http://wget http://130.246.189.180:8000/jasmin-bundle.tar
* $ mkdir deploy
* $ tar xvf jasmin-bundle.tar -C deploy/
* $ untar setuptools,tar -xzvf setuptools-5.7.tar.gz install
 $ untar pip, install
* cd ~ 
* ~/jasmin-py3.3/bin/pip install --upgrade --use-wheel --no-index -f
file:///home/jasminportal/deploy -r deploy/requirements.txt
* ~/jasmin-py3.3/bin/pip install --upgrade --use-wheel --no-index -f
file:///home/jasminportal/deploy cloudhands-ops cloudhands-web cloudhands-burst cloudhands-jasmin

::

    cloudhands-orgadmin --host=jasmin-ref-portal01.jc.rl.ac.uk
    --identity=~/.ssh/id_rsa.pub --user=jasminportal
    --db=/home/jasminportal/jasmin-web.sl3
    --account=cjllewellyn --email=charlie.j.llewellyn@gmail.com --surname=Llewellyn
    --organisation='Portal Test Organisation'
    --activator=/root/un-managed-post-cust.sh
    --providers=cloudhands.jasmin.vcloud.ref-portalTest-U.cfg

::

    2014-09-29 09:03:17,152 INFO    cloudhands.ops.orgadmin|Sending from jasmin-ref-portal01.jc.rl.ac.uk.
    2014-09-29 09:03:17,233 INFO    cloudhands.ops.orgadmin|('user', '536f9d385be64e8b89967c9f370d2fc2', 'cjllewellyn')
    2014-09-29 09:03:17,256 INFO    cloudhands.ops.orgadmin|('provider', '1e6d8ac3130246a6b6964eaf1d4f3515',
    'cloudhands.jasmin.vcloud.ref-portalTest-U.cfg') 2014-09-29 09:03:17,256 INFO    cloudhands.ops.orgadmin|('subscription',
    'd504222102d94e449024c090549e039e') 2014-09-29 09:03:17,256 INFO    cloudhands.ops.orgadmin|('organisation',
    '63c0f3bc3a3c4c8ab37bbe034ec6c91b', 'Portal Test Organisation') 2014-09-29 09:03:17,268 INFO    cloudhands.ops.orgadmin|('membership',
    '2ba8010aad6448828dee2e4f6d139e66', 'admin') 2014-09-29 09:03:17,280 INFO    cloudhands.ops.orgadmin|('registration',
    'e5834448f23947e8acd2136d3ebcd67d') 2014-09-29 09:03:17,286 INFO    cloudhands.ops.orgadmin|('subscription',
    'd504222102d94e449024c090549e039e', 'maintenance', 'org.orgadmin', [])

::

    ~/jasmin-py3.3/bin/cloud-demoserve -v --port=8080 --db=jasmin-web.sl3
    --log=cloud-demoserve.log

cloudhands.burst.membership|'cloudhands.jasmin.vcloud.ref-portalTest-U.cfg'
2014-10-01 17:51:38,788 ERROR   cloudhands.web.login_update|'NoneType' object
has no attribute 'value'
cloudhands.burst.session.token|'NoneType' object is not subscriptable

Portal host
===========

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

