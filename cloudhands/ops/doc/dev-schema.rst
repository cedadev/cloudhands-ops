..  Titling
    ##++::==~~--''``

Database schema
===============

There are about 20 tables in the database schema. Of these, four fundamental
types provide the basis for implementing business logic:

* Actors_
* Artifacts_
* Resources_
* States_

Actors
~~~~~~

Every change to application state can be attributed to an Actor. The most
common subtype is `User`, but each `Component` of the system also has an
identity too.

.. autoclass:: cloudhands.common.schema.Actor

.. autoclass:: cloudhands.common.schema.User

.. autoclass:: cloudhands.common.schema.Component


Artifacts
~~~~~~~~~

An Artifact is an output of the system. Artifacts are constructed at the
request of the user. They can be complex, compound objects. 

.. autoclass:: cloudhands.common.schema.Artifact

.. autoclass:: cloudhands.common.schema.Membership

.. autoclass:: cloudhands.common.schema.Host


Resources
~~~~~~~~~

Resources are real-world items which are allocated and de-allocated by the
system. Their existence is transitory, and has to be continually verified.

.. autoclass:: cloudhands.common.schema.Resource

.. autoclass:: cloudhands.common.schema.Node

.. autoclass:: cloudhands.common.schema.IPAddress

.. autoclass:: cloudhands.common.schema.EmailAddress


States
~~~~~~

.. automodule:: cloudhands.common.discovery
   :members:

.. _discoverable permissions: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#using-pyramid-security-with-url-dispatch

Operations
~~~~~~~~~~

.. automodule:: cloudhands.common.tricks
   :members: create_user_from_email

