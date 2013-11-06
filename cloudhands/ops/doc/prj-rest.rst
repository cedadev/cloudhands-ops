..  Titling
    ##++::==~~--''``


RESTful design
==============

API elaboration
~~~~~~~~~~~~~~~

* Design the landing page from the human perspective of workflow
* Each widget is a client of a resource
* Workflow use of resources drives navigation schema
* Each returned object has a 'self' link
* Forms are identified via their 'doc' URL and fragment

User interface
~~~~~~~~~~~~~~

* Picked colours from the `image of LOTUS in the JASMIN data centre`_.
* Created a corresponding `yui skin`_ using the online `YUI skin builder`_.
 
.. _image of LOTUS in the JASMIN data centre: http://proj.badc.rl.ac.uk/cedaservices/attachment/wiki/JASMIN/LOTUS/LOTUS.jpg
.. _yui skin: http://yui.github.io/skinbuilder/?mode=pureindex.html?opt=jasmin,26408C,E3E2DE,0.72,0.8,2,2.3&h=349,95,58&n=213,57,55&l=277,95,36&b=0,-80,-71&mode=pure
.. _YUI skin builder: http://yui.github.io/skinbuilder/
.. _Pencil wireframe tool: http://pencil.evolus.vn/
.. _Fielding dissertation: http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm
.. _hypermedia APIs: http://oredev.org/2010/sessions/hypermedia-apis
.. _Requests library can send JSON encoded data: http://www.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
.. _Pyramid can accept JSON encoded data: http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/webob.html#dealing-with-a-json-encoded-request-body
