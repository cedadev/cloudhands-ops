.. Cloudhands documentation master file, created by
   sphinx-quickstart on Mon Oct 21 16:49:26 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

..  Titling
    ##++::==~~--''``

Top level
+++++++++

This manual is documentation for the software which operates the UK STFC
JASMIN cloud infrastructure. JASMIN provides a federated storage and computing
platform for scientific applications.

The software is written in Python_. Componentisation is a key architectural
feature, allowing contributors to extend the core functionality by writing
packages which conform to one of the JASMIN plugin APIs.

.. _Python: http://python.org

.. toctree::
   :maxdepth: 3

   dev-guide
   ops-guide

Python packages
:::::::::::::::

The software is distributed as several separate packages.

cloudhands-common
    Common types, utilities and database schema

cloudhands-web
    User interface and Web portal application

cloudhands-jasmin
    Site-specific configuration for the JASMIN infrastructure (private)

cloudhands-ops
    Contains this manual, some operations scripts and experimental code.

References
::::::::::

The software runs as a web application portal. It uses the Pyramid web
framework and the SQLAlchemy ORM. The following material has informed the design.

* `Pyramid security model`_
* `Multiple authentication methods`_
* `Persona policy configuration`_

.. _XRDS specification: http://docs.oasis-open.org/xri/2.0/specs/xri-resolution-V2.0.html
.. _Persona policy configuration: http://douglatornell.ca/blog/category/persona-authentication/
.. _Pyramid security model: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#security
.. _multiple authentication methods: http://www.rfk.id.au/blog/entry/securing-pyramid-persona-macauth/

Indexes
=======

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

