..  Titling
    ##++::==~~--''``

Data Model
==========

The data model has been developed along traditional lines in order to
accomodate a relational database back-end. The model is defined
as a schema in third-normal form using the SQLAlchemy_ ORM.

.. _SQLAlchemy: http://docs.sqlalchemy.org

There are about 20 tables in the database schema. Of these, four fundamental
types provide the basis for implementing business logic:

* Actors_
* Artifacts_
* Resources_
* States_

Typically, a change to application state is modelled as:

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

Resources have a base type, `Touch` which carries no contextual data
but which can be used to signal changes in States_.

.. autoclass:: cloudhands.common.schema.Touch

States
~~~~~~

The nature of Artifacts_ is that they take some effort to establish, and they
change over time. Each artifact table has its own State class so that business
logic can make transitions and persist state in the database.
 
.. autoclass:: cloudhands.common.states.MembershipState
   :members: table, values
   :undoc-members:

.. autoclass:: cloudhands.common.states.HostState
   :members: table, values
   :undoc-members:

Categories
~~~~~~~~~~

.. autoclass:: cloudhands.common.schema.Organisation

