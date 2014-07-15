..  Titling
    ##++::==~~--''``

Integration tests
=================

These instructions help check that the JASMIN portal is correctly deployed
and integrated with other subsystems. The integration tests should be
performed in the Reference environment and are a gate to promotion in to
Production.

User registration
~~~~~~~~~~~~~~~~~

This procedure tests various paths through the user registration process.

0. Prerequisites
----------------

* Set up a `free external email address`_.
  You should record login details and store them in a protected location,
  eg::

    Address: dominic.enderby@contractor.net
    Customer number: 211828816
    Gender: Male
    Date of birth: 01/04/1984
    Country: UK
    Password: D0m1n1c_Enderby
    Security question: What city where you born in?
    Security answer: Harwell

1. Successful registration
--------------------------

1. Visit the JASMIN home page and click on the `Register` link.
    
    * The link takes you to https://jasmin-cloud.jc.rl.ac.uk/register
    * A form is displayed with three fields and a `Register me` button.
      The fields are `Username`, `Password`, `Email`.

2. Enter registration details for a new user.

    * Username: ``denderby``
    * Password: ``D0m1n1c_Enderby``
    * Email: ``dominic.enderby@contractor.net``

3. Click the button `Register me`.

    * You are redirected to the home page.

2. Successful confirmation
--------------------------

0. Prerequisites
    * `1. Successful registration`_.


1. Visit email account and check Inbox

    * The Inbox contains a new message entitled `JASMIN notification`.

    .. image:: _static/register_confirm_email-lab.png

2. Click the confirmation link.

    * The link takes you to https://jasmin-cloud.jc.rl.ac.uk/login.

3. Successful login
-------------------

0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.

1. Visit https://jasmin-cloud.jc.rl.ac.uk/login.

    * A form is displayed with two fields and a `Log in` button.
      The fields are `Username`, `Password`.
    * The Username field is styled red and asks for a name 8 - 10 characters
      long.
    * The Password field is styled red and asks for a name 8 - 20 characters
      long.

        * at least one lowercase letter
        * at least one uppercase letter
        * at least one numeric digit
        * at least one special character
        * no whitespace.

2. Enter a valid username.

    * The Username field is styled green

3. Enter a valid password.

    * The Password field is styled green.

4. Click `Log in`.

    * You are redirected to the home page.

4. Unsuccessful login (password)
--------------------------------

0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.

1. Proceed with `3. Successful login`_, stopping before step 3.

2. Enter a false password which conforms to the password criteria.
   Example: ``N0t_MyPa55w0rd``.

    * The Password field is styled green.

3. Click `Log in`.
    * A yellow message appears: `Login failed. Please try again`.
    * The Username field is empty and styled red.
    * The Password field is empty and styled red.

5. LDAP entry created on first login
------------------------------------

.. important::

   The behaviour described in this section is undesirable on a public facing
   network as it constitutes `resource exhaustion`_ of unique `cn` names
   and (ultimately) `uidNumbers`.
 
0. Prerequisites
    * `1. Successful registration`_.
    * `2. Successful confirmation`_.
    * `3. Successful login`_.

1. View LDAP record for `denderby`. Use the `ldapvi` program like this::

    ldapvi -d -h ldap-test.jc.rl.ac.uk -w password \
    --user "cn=dehaynes,ou=ceda,ou=People,o=hpc,dc=rl,dc=ac,dc=uk"

   Use the `G` key to navigate to the end of the file.

    * An LDAP record has been created as follows::

        cn=denderby,ou=jasmin2,ou=People,o=hpc,dc=rl,dc=ac,dc=uk
        cn: denderby
        description: JASMIN2 vCloud registration
        mail: dominic.enderby@contractor.net
        objectClass: inetOrgPerson
        objectClass: person
        objectClass: top
        objectClass: organizationalPerson
        sn: UNKNOWN

.. _free external email address: http://www.mail.com/int/
.. _resource exhaustion: https://www.owasp.org/index.php/Resource_exhaustion 
