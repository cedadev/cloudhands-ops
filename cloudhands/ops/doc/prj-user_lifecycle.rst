..  Titling
    ##++::==~~--''``

User lifecycle
==============

One of the tasks of the portal is to hide from the user the complexity of
managing credentials required by:

* funding bodies who control access to on-site resources
* the authentication systems implemented by VM operating systems
* back-end providers (VMWare, Azure, Amazon, etc)

Organisation membership
~~~~~~~~~~~~~~~~~~~~~~~

Membership of an organisation is administered by a named individual (typically
the `principal investigator` of the project). That individual has the authority
to admit others to the organisation, giving them use of the resources allocated
to it.

In order to identify a prospective member, the administrator must at a
miniumum:

* know the surname of the individual
* know an email address where he can be reached

.. seqdiag::

   seqdiag {
    default_fontsize = 14;
    Guest; Registration; Membership; Administrator;
    Administrator -> Membership [label="create"];
    Membership --> Guest [rightnote="Invitation"];
    Membership <<-- Guest [rightnote="Activation"];
    Membership -> Registration [label="create"];
    Registration -> Registration [note="EmailAddress"];
    Registration -> Registration [note="BcryptedPassword"];
   }

Account properties
~~~~~~~~~~~~~~~~~~

.. seqdiag::

   seqdiag {
    default_fontsize = 14;
    User; Registration; LDAP;
    User -> Registration [label="edit"];
    Registration -> LDAP [label="query"];
    Registration <-- LDAP;
    Registration -> Registration [note="PosixUId"];
    Registration -> Registration [note="PosixUIdNumber"];
    Registration -> Registration [note="PosixGIdNumber"];
    User <-- Registration;
    User -> Registration [label="edit"];
    Registration -> Registration [note="PublicKey"];
    Registration -> LDAP [label="add"];
    Registration <-- LDAP;
    User <-- Registration;
   }

Session credentials
~~~~~~~~~~~~~~~~~~~

Elaboration
~~~~~~~~~~~

* PI requires Membership with admin role
* PI searches for new user from LDAP records
* PI selects user and generates an invitation
* (Out of band) PI sends to user a link to the invitation
* New user signs on with email address

LDAP
~~~~

