
1. Build the images::

   fig build

2. Init the Key Distribution Center database (you will be asked for a password)::

   fig run kdc kdb5_util create -r DJKERB.DEV -s

3. Start the services::

   fig up server

4. Add a principal::

   docker-enter $(fig ps -q kadmin)
   kadmin.local -q 'addprinc admin/admin'
   kadmin.local -q 'addprinc HTTP/kerbtest'

7. Generate the server keytab::

   fig run server kadmin -p admin/admin -q 'ktadd -k /var/keytabs/server.keytab HTTP/kerbtest'

6. Try to login::

   fig run client kinit admin/admin
   fig run client kinit HTTP/kerbtest

7. Run the client::

   fig run client bash
   kinit admin/admin
   ./get.py


NOTE: `fig` presents some issues with output buffering and does not always show
the prompts until some input occurred.
