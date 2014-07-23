..  Titling
    ##++::==~~--''``

Cloudhands is a `Platform as a Service` (PaaS) framework. It gives you the
software necessary to run a private computing cloud for your business or
organisation. A key objective is support for multiple back-end providers.

This release
::::::::::::

Cloudhands is a very young project. As of Autumn 2014, it is under
heavy development and features are added daily. 

You are welcome to give `cloudhands` a try, but be aware that some parts
of the codebase lack the test coverage of a finished product. Improvements
to documentation are ongoing.

Requirements
::::::::::::

Cloudhands requires Python 3.3 or above. It uses setuptools_ for installation.

The reference platform is RHEL 6.5 with Python 3.3 from RPMs. This is assumed
by some of the deployment scripts. However, the main codebase is written always
to track the latest version of Python.

Quick start
:::::::::::

Download and unpack the source distribution (version numbrs will differ)::

    $ tar -xzvf cloudhands-ops-0.001.tar.gz
    $ cd cloudhands-ops-0.001

Run the `check` script to establish a working environment::

    $ check.sh --nolint --nopep8 --notest

Run the `build` script to create the documentation::

    $ build.sh --novenv --nopush --nosign

Consult the documentation::

    $ firefox cloudhands/ops/doc/html/index.html

Roadmap
:::::::

Cloudhands's mission is to provide a robust Pythonic framework to provision
and manage scientific analysis in the cloud.

It is developed in the UK and released to the public under a `BSD licence`_.

The API may change significantly as the project proceeds. At this early stage,
you should only use the latest release, which may not be compatible with
previous versions.

Can you help?
=============

* If you've spotted a bug in Cloudhands, please let us know so we can fix it.
* If you think Cloudhands lacks a feature, you can help drive development by
  describing your Use Case.


:author:    D Haynes
:contact:   david.e.haynes@stfc.ac.uk
:copyright: 2013 UK Science and Technology Facilities Council
:licence:   BSD

.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _BSD licence: http://opensource.org/licenses/BSD-3-Clause
