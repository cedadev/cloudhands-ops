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

Style templates
===============

Considered the frameworks mentioned in reviews at webgranth_ and codegeekz_ against these
criteria:

* Driven by open standards (HTML5 and CSS3).
* Styled for desktop rather than mobile platforms.
* Favouring a RESTful architecture rather than one-page web apps.
* Compatible with a Python framework (not tied to back ends like node.js or PHP).

Shortlist
---------

* https://sprresponsive.com/sprinvoice/
    A single-page template for an invoice document.
* http://52framework.com/
    A grid layout system with some templates and typography.
* http://purecss.io/
    An extensible framework containing widgets and layouts.
* http://www.markupframework.org/
    Typography and layouts.
* http://thesquaregrid.com/
    A CSS grid layout.
* http://thatcoolguy.github.io/gridless-boilerplate/
    Simple styling for widgets with some typography.
* http://code.google.com/p/css3-action-framework/
    A library of CSS effects.

.. _webgranth: http://www.webgranth.com/best-html5-and-css3-frameworks-you-would-know-ever
.. _codegeekz: http://codegeekz.com/css-frameworks-for-accelerated-development/

Indexes
=======

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

