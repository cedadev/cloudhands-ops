..  Titling
    ##++::==~~--''``

Integration tests
=================

These instructions help check that the JASMIN portal can be correctly deployed
and integrated with other subsystems. The integration tests should be
performed in the Reference environment and are a gate to promotion into
Production.

.. note::

   You can perform these tests in the development environment, but all URLs
   will have their root at http://jasmin-cloud.jc.rl.ac.uk:8080, not as
   specified below.

JVO Onboarding
~~~~~~~~~~~~~~

This procedure begins with a fresh database. It tests that a new JVO can be
created along with its administrator account.

0. Prerequisites
----------------

    * Access to your on-site email account.
    * A running portal with a fresh database.
    * LDAP cleared of any previous test data.

1. Verify guest access
----------------------

0. Prerequisites

    * Web portal is running.
    * Identity controller is running.

1. Visit https://jasmin-cloud.jc.rl.ac.uk

    * The home page is displayed.
    * The `Organisations` menu has no entries.

2. Add a JVO admin with the `orgadmin` script
---------------------------------------------

0. Prerequisites

    * You are logged in to the management node as a devops user.
    * You have installed the devops tools according the site-specific
      documentation.

1. Invoke the `orgadmin` script to create a fictional user and JVO, supplying your
   own email address for activation::

        ~/pyops-3.3/bin/cloudhands-orgadmin \
        --host=jasmin-cloud.jc.rl.ac.uk --identity=~/.ssh/id_rsa-jasminvm.pub \
        --db=/home/jasminportal/jasmin-web.sl3 \
        --account=bcumberbat \
        --email=<your_email_address> \
        --surname=Cumberbatch \
        --organisation=stfc-managed-m \
        --public=172.26.9.70/31 \
        --activator=/usr/local/bin/activator.sh \
        --providers=cloudhands.jasmin.vcloud.ref-portalTest-M.cfg

   * The utility runs and emits a log trace similar to the following::

        2014-09-29 15:43:06,935 INFO    cloudhands.ops.orgadmin|Sending from jasmin-cloud.jc.rl.ac.uk.
        2014-09-29 15:43:08,565 INFO    cloudhands.ops.orgadmin|('user', '1fe4d56051ba48ed86f3b21ce878775d', 'bcumberbat')
        2014-09-29 15:43:08,696 INFO    cloudhands.ops.orgadmin|('provider', '0460735f622247b198b7e3f60c9e9379', 'cloudhands.jasmin.vcloud.ref-portalTest-M.cfg')
        2014-09-29 15:43:08,696 INFO    cloudhands.ops.orgadmin|('subscription', '6dd7ff10e8f14f308ac39c367b82d51b')
        2014-09-29 15:43:08,696 INFO    cloudhands.ops.orgadmin|('organisation', '3c26b7c8b3b44428988c310d2de877da', 'stfc-managed-m')
        2014-09-29 15:43:08,725 INFO    cloudhands.ops.orgadmin|('membership', 'e805f7939a8a4418a0261ed6d6cb5fab', 'admin')
        2014-09-29 15:43:08,752 INFO    cloudhands.ops.orgadmin|('registration', '5f84cc5d9863447a9b38a5e16ab9b90e')
        2014-09-29 15:43:08,758 INFO    cloudhands.ops.orgadmin|('subscription', '6dd7ff10e8f14f308ac39c367b82d51b', 'maintenance', 'org.orgadmin', [])
        2014-09-29 15:43:08,760 INFO    cloudhands.ops.orgadmin|('subscription', '6dd7ff10e8f14f308ac39c367b82d51b', 'maintenance', 'org.orgadmin', [('ipaddress', '170.16.151.70')])
        2014-09-29 15:43:08,763 INFO    cloudhands.ops.orgadmin|('subscription', '6dd7ff10e8f14f308ac39c367b82d51b', 'maintenance', 'org.orgadmin', [('ipaddress', '170.16.151.71')])
        2014-09-29 15:43:08,765 INFO    cloudhands.ops.orgadmin|('subscription', '6dd7ff10e8f14f308ac39c367b82d51b', 'unchecked', 'org.orgadmin', [])

3. Activate the administrator account
-------------------------------------

1. Visit your email account and check the Inbox

    * The Inbox contains a new message entitled `JASMIN notification`.
    * The message contains a link to a resource under
      https://jasmin-cloud.jc.rl.ac.uk/membership.
       
      *NB: messages can take several minutes to be delivered*.

2. Click the activation link.

    * The linked page redirects you to a resource under
      https://jasmin-cloud.jc.rl.ac.uk/registration. The page is entitled
      `bcumberbat`.
    * The `Organisations` menu has the entry `stfc-managed-m`.
    * A form is displayed with the title `Set your password`.
      It has a `Password` field and a `Change` button.

3. Enter a password for the user account.

    * Password: ``Cumb3rb@tch``

4. Click the button `Change`.

    * You are redirected to the login page.
    * A form is displayed with the title `User login`.
      It has two fields and a `Log in` button.
      The fields are `Username`, and `Password`.
    * The Username field has the value `bcumberbat` and is styled green.
    * The Password field is empty and styled red.

5. Enter the account password.

    * Password: ``Cumb3rb@tch``
    * The Password field is styled green.

6. Click `Log in`.

    * You are redirected to the home page.

User registration
~~~~~~~~~~~~~~~~~

This procedure tests various paths through the user registration process.

0. Prerequisites
----------------

* Set up a `free external email address`_.
  You should record login details and store them in a protected location
  (not in a public code repository as this example does)::

    Address: dominic.enderby@contractor.net
    Customer number: 211828816
    Gender: Male
    Date of birth: 01/04/1984
    Country: UK
    Password: D0m1n1c_Enderby
    Security question: What city where you born in?
    Security answer: Harwell

* Perform `JVO onboarding`_ of an administrator.

1. Login (administrator)
------------------------

1. Visit https://jasmin-cloud.jc.rl.ac.uk/login.

    * A form is displayed with two fields and a `Log in` button.
      The fields are `Username`, `Password`.

2. Enter the adminstrator username: ``bcumberbat``.

    * The Username field is styled green.

3. Enter the password for the account: ``Cumb3rb@tch``.

    * The Password field is styled green.

4. Click `Log in`.

    * You are redirected to the home page.

2. Successful invitation
------------------------

1. From the `Organisations` dropdown, select `stfc-managed-m`.

    * You are sent to the stfc-managed-m JVO page.
    * A form is displayed with three fields and a `Create` button.
      The fields are `Username`, `Surname`, and `Email`.
    * The Username field is styled red and asks for a name 8 - 10 characters
      long.
    * The Email field is styled red.

2. Enter the username: `denderby`.

    * The Username field is styled green

3. Enter the surname: `Enderby`. Enter the email: `dominic.enderby@contractor.net`.

    * The Email field is styled green.

4. Click `Create`.

    * You are redirected to a confirmation page.
    * You can navigate by link to the home page.

5. Click the button `Logout`.

3. Successful activation
--------------------------

0. Prerequisites
    * `1. Login (administrator)`_.
    * `2. Successful invitation`_.

1. Visit email account and check Inbox

    * The Inbox contains a new message entitled `JASMIN notification`.
       
      *NB: messages can take several minutes to be delivered*.

    .. image:: _static/invitation_email-dev.png

2. Click the activation link.

    * The linked page redirects you to a resource under
      https://jasmin-cloud.jc.rl.ac.uk/registration. The page is entitled
      `denderby`.
    * The `Organisations` menu has the entry `stfc-managed-m`.
    * A form is displayed with the title `Set your password`.
      It has a `Password` field and a `Change` button.

3. Enter a password for the user account.

    * Password: ``D0m1n1c_Enderby``

4. Click the button `Change`.

    * You are redirected to the login page.
    * A form is displayed with the title `User login`.
      It has two fields and a `Log in` button.
      The fields are `Username`, and `Password`.
    * The Username field has the value `denderby` and is styled green.
    * The Password field is empty and styled red.

5. Enter the account password.

    * Password: ``D0m1n1c_Enderby``
    * The Password field is styled green.

6. Click `Log in`.

    * You are redirected to the home page.

4. Successful login
-------------------

0. Prerequisites
    * `1. Login (administrator)`_.
    * `2. Successful invitation`_.
    * `3. Successful activation`_.
    * You are logged out.

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

5. Unsuccessful login (password)
--------------------------------

0. Prerequisites
    * `1. Login (administrator)`_.
    * `2. Successful invitation`_.
    * `3. Successful activation`_.

1. Proceed with `4. Successful login`_, stopping before step 3.

2. Enter a false password which conforms to the password criteria.
   Example: ``N0t_MyPa55w0rd``.

    * The Password field is styled green.

3. Click `Log in`.
    * A yellow message appears: `Login failed. Please try again`.
    * The Username field is empty and styled red.
    * The Password field is empty and styled red.

6. LDAP entry created on first login
------------------------------------

0. Prerequisites
    * `1. Login (administrator)`_.
    * `2. Successful invitation`_.
    * `3. Successful activation`_.
    * `4. Successful login`_.

1. View LDAP record for `denderby`. Use the `ldapvi` program like this::

    ldapvi -Z -v -d -h ldap-ref.jc.rl.ac.uk -w <password> \
    --user "cn=jasminportal,ou=software,ou=People,o=hpc,dc=rl,dc=ac,dc=uk"

   Use the `G` key to navigate to the end of the file.

    * An LDAP record has been created as follows (numbers and password will
      vary)::

        cn=denderby,ou=jasmin2,ou=People,o=hpc,dc=rl,dc=ac,dc=uk
        mail: dominic.enderby@contractor.net
        objectClass: organizationalPerson
        objectClass: inetOrgPerson
        objectClass: person
        objectClass: top
        objectClass: posixAccount
        description: cluster:jasmin-login
        description: jvo:stfc-managed-m
        cn: denderby
        sn: Enderby
        userPassword: {SSHA}JHLH0mEzaxDCFlzk4h55Vpeqp06lyHCK
        homeDirectory: /home/denderby
        uid: denderby
        gecos: denderby <dominic.enderby@contractor.net>
        gidNumber: 7010002
        uidNumber: 7010002
        loginShell: /bin/bash

7. Successful key add to account
--------------------------------

0. Prerequisites
    * `1. Login (administrator)`_.
    * `2. Successful invitation`_.
    * `3. Successful activation`_.
    * `4. Successful login`_.

1. Visit the `Account` page.

    * The account shows a `UId`.
    * The account shows a `Name`.
    * The account shows a `Email`.
    * The account shows a `Password` (obscured).
    * The account has a form entitled `Paste your key`.

2. Paste a `ssh-rsa` key into the form and click `Add`.

    * The key is added to the account.

Appliance lifecycle
~~~~~~~~~~~~~~~~~~~

This procedure allows a test of the integration with the VMWare back end. It
is only available in the `Ref` environment.

1. Login (demo user)
--------------------

0. Prerequisites
    * Demo portal is running

1. Visit https://jasmin-cloud.jc.rl.ac.uk/login.

    * A form is displayed with two fields and a `Log in` button.
      The fields are `Username`, `Password`.

2. Enter the admin username for the demo: ``denderby``.

    * The Username field is styled green.

3. Enter the password for the demo: ``D0m1n1c_Enderby``.

    * The Password field is styled green.

4. Click `Log in`.

    * You are redirected to the home page.

2. Launch an item from the catalogue
------------------------------------

0. Prerequisites
    * `1. Login (demo user)`_.

1. From the `Organisations` dropdown, select `stfc-managed-m`.

    * You are sent to the stfc-managed-m JVO page.

2. From the breadcrumb menu, select `Catalogue`.

    * The catalogue page is populated with two items.
    * Clicking each item shows a name in bold, a description, and an `OK`
      button.

3. Select a catalogue item and click `OK`.

    * You are sent to the `Configure appliance` page. Note this URL for later.
    * There is a form called `General information` with two fields and an
      `OK` button. The fields are `Name`, and `Description`.

4. Create a new appliance by filling the fields as follows:

    * Name: ``test_01``
    * Description: ``test appliance``

5. Click the button `OK`.

    * You are redirected to the stfc-managed-m JVO page.

3. Monitor the appliance lifecycle
----------------------------------

0. Prerequisites
    * `1. Login (demo user)`_.
    * `2. Launch an item from the catalogue`_.

1. Note the initial state

    * The appliance begins in the `pre_provision` state.

2. Observe state updates.

    * The appliance state updates itself to show `provisioning` (~5s).
    * The appliance state updates itself to show `operational` (~60s).
    * The appliance item has a `Stop` and a `Check` button.
    * The appliance has a non-routable IP address. Note this value.

4. Check the deployed appliance
-------------------------------

0. Prerequisites
    * `1. Login (demo user)`_.
    * `2. Launch an item from the catalogue`_.
    * `3. Monitor the appliance lifecycle`_.

1. Check the VApp in the `vCloud Director` GUI.

    * The vApp called `test_01` exists.
    * The vApp state is `Stopped`.

2. Check the customization script as follows:

   #. Click the vApp named `test_01`.
   #. Select the `Virtual Machine` tab.
   #. Click on the name of the VM inside the vApp.
   #. Click the `Guest OS Customization` tab.
   #. Scroll down to the `Customization Script` section.

    * The script invokes ``/usr/local/bin/activator.sh``
    * The script passes an argument which is the URL you noted above.

3. Check the Edge gateway in the `vCloud Director` GUI as follows:

   #. Click the `Administration` tab and select the item named `stfcmanaged-M-std-compute`.
   #. Click the `Edge Gateways` tab and select the one beginning
      `stfcmanaged-M`.
   #. Click the dropdown settings menu and select `Edge Gateway Services...`

    * The `NAT` tab shows a DNAT rule for the IP address you noted in
      `3. Monitor the appliance lifecycle`_ above. It allows any port over TCP.
      Note the public IP it routes to.
    * The `Firewall` tab shows a rule for the routable IP you noted here.
      It allows all ports over TCP.

5. Set the appliance running
----------------------------

0. Prerequisites
    * `1. Login (demo user)`_.
    * `2. Launch an item from the catalogue`_.
    * `3. Monitor the appliance lifecycle`_.
    * `4. Check the deployed appliance`_.

1. Click the button `Start`.

    * The appliance state updates itself to show `pre_start`.
    * The appliance state updates itself to show `running` (~2s).
    * The buttons are displayed as follows; `Stop`, `Check`.

1. Refresh the view `vCloud Director` GUI. Check the VApp status.

    * The vApp state is `Running`.

.. _free external email address: http://www.mail.com/int/
.. _resource exhaustion: https://www.owasp.org/index.php/Resource_exhaustion 
