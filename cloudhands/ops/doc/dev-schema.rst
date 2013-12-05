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

A change to application state is modelled as:

* linking an artifact with an actor
* linking an artifact with a resource
* changing the state of an artifact

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

.. autoclass:: cloudhands.common.schema.PosixUId

.. autoclass:: cloudhands.common.schema.PosixGId


States
~~~~~~

The nature of Artifacts_ is that they take some effort to establish, and they
change over time. Each artifact table has its own State class so that business
logic can make transitions and persist state in the database.
 
.. autoclass:: cloudhands.common.fsm.MembershipState
   :members: table, values
   :undoc-members:

.. autoclass:: cloudhands.common.fsm.HostState
   :members: table, values
   :undoc-members:
