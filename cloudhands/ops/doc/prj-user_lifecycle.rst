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
minimum:

* know the surname of the individual
* know an email address where he can be reached

.. seqdiag::
   :alt: A sequence diagram is missing from your view
   :caption:    Sequence: Administrator creates Registration.
                Guest activates Registration.
                Guest logs in as User.

   seqdiag {
    default_fontsize = 14;
    Guest; User; Registration; Membership; Administrator;
    Administrator -> User [label="create"];
    Administrator <<-- User [label="uuid"];
    Administrator -> Membership [label="create"];
    Membership -> User [label="attach"];
    Membership <<-- User;
    Administrator <<-- Membership [label="uuid"];
    Administrator -> Registration [label="create"];
    Registration -> User [label="attach"];
    Registration <<-- User;
    Registration -> Registration [note="EmailAddress"];
    Administrator <<-- Registration [label="uuid"];
    Administrator ->> Guest [rightnote="Invitation (automated)"]{
        Guest -> Registration [rightnote="Activation"];
        Registration -> Registration [note="BcryptedPassword"];
        Guest <<-- Registration [label="account url"];
        Guest -> Registration [label="login"];
        Registration -->> User [label="authenticate"];
    }
   }

Account properties
~~~~~~~~~~~~~~~~~~

A new User must complete the details of his Registration before he can
make use of portal services. The information required corresponds to that
stored in an LDAP record for a POSIX account.

The portal will prompt the user with the necessary forms until the information
is supplied. Then the LDAP record is created.

Subsequent additions to the account (for example, a new SSH public key) will
cause the LDAP record to be modified.

.. seqdiag::
   :alt: A sequence diagram is missing from your view
   :caption: Sequence: User edits account. Registration writes to LDAP record.

   seqdiag {
    default_fontsize = 14;
    User; Registration; LDAP;
    User -> Registration [label="edit"];
    Registration -> LDAP [label="query"];
    Registration <-- LDAP;
    Registration -> Registration [note="PosixUId"];
    Registration -> Registration [note="PosixUIdNumber"];
    Registration -> Registration [note="PosixGIdNumber"];
    Registration -> LDAP [label="add"];
    Registration <-- LDAP;
    User <-- Registration;
    User -> Registration [label="edit"];
    Registration -> Registration [note="PublicKey"];
    Registration -> LDAP [label="modify"];
    Registration <-- LDAP;
    User <-- Registration;
   }

Session credentials
~~~~~~~~~~~~~~~~~~~

.. seqdiag::
   :alt: A sequence diagram is missing from your view
   :caption: Sequence: User session expires. Membership retains API token.

   seqdiag {
    default_fontsize = 14;
    User; Membership; Provider;
    User -> Membership [label="session", failed];
    User -> Membership [label="login"];
    Membership -> Provider [label="authenticate"];
    Membership <-- Provider [label="token"];
    Membership -> Membership [note="Token"];
   }

