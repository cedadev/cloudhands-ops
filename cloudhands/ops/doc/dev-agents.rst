..  Titling
    ##++::==~~--''``

Business Logic
==============

When the logic which drives a system is buried deep in the code, it can be
hard to adapt and maintain.

We know that as our understanding grows, we will need to change the business
rules we operate in JASMIN. And we expect that others using this software
will have entirely different logic to implement.

Operations
~~~~~~~~~~

Having explicitly created tables in the database to track the state of
:py:func:`cloudhands.common.schema.Artifact`, we build on that by formalising
the transitions between states.

Transitions are achieved through `operations`. They are Python
`function objects`_ which can be created in advance of their use. When called,
they attempt a change to the system, and if successful, return the
corresponding :py:func:`cloudhands.common.schema.Touch` object.

.. _function objects: http://docs.python.org/3/reference/datamodel.html?highlight=__call__#emulating-callable-objects

Membership operations
---------------------

.. autoclass:: cloudhands.burst.membership.Invitation
   :members: __init__, __call__
   :special-members:

Agents
~~~~~~

Agents are Python modules with responsibility for a particular task or aspect of the
system. In some cases, they are merely namespaces for a number of related
Operations_, called elsewhere by client modules.

At their most sophisticated, agent modules are autonomous and manage an
event loop within their own process. It is this level of cellular design which
permits scaling to a large distributed system.


Methods
-------

.. automodule:: cloudhands.web.tricks
   :members: create_user_from_email

