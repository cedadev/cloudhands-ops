..  Titling
    ##++::==~~--''``


Plugin APIs
===========

Cloudhands makes extensive use of python `entry points`_ to define interfaces
for third party plugins.

Plugins are required for these scenarios:

Site configuration
    No key material, secret tokens or credentials are supplied with the
    Cloudhands software. A portal is configured by installing these assets
    via a site-specific package which registers itself through a defined API.

Site customisation
    Cloudhands has a very modular design which allows a developer to extend its
    functionality so long as a defined architectural pattern is observed. The
    custom software uses the plugin APIs to add tables to the database and
    stateful controls to the web interface.

..  _entry points: http://pythonhosted.org/distribute/setuptools.html#dynamic-discovery-of-services-and-plugins

jasmin.component.fsm
~~~~~~~~~~~~~~~~~~~~

The Jasmin `Finite State Machine` interface allows developers to declare a new
database table which defines the permitted states of a FSM.

.. autodata:: cloudhands.common.discovery.fsm

jasmin.pyramid.settings
~~~~~~~~~~~~~~~~~~~~~~~

jasmin.libcloud.creds
~~~~~~~~~~~~~~~~~~~~~
