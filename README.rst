armstrong.hatband
=================
Provides administrative interface and utilities for use in `Armstrong`_.


Usage
-----

**TODO**

Installation & Configuration
----------------------------
You can install the latest release of ``armstrong.hatband`` using `pip`_:

::

    pip install armstrong.hatband

Make sure to add ``armstrong.hatband`` and ``django.contrib.admin`` to your
``INSTALLED_APPS``.  You can add this however you like.  This works as a
copy-and-paste solution:

::

	INSTALLED_APPS += ["armstrong.hatband", "django.contrib.admin", ]

Once installed, you must run ``syncdb`` in order to install Django's admin
models.  This is only required if you did not have Django's admin already
installed and configured.

Finally, you must alter your URL configuration.  At the top of your ``urls``
module (``urls.defaults`` in an Armstrong project), make sure to change this
line:

::

    from django.contrib import admin

To:

::
    from armstrong import hatband as admin

The rest of the URL configuration stays identical to what is expected for the
traditional Django admin.

.. _pip: http://www.pip-installer.org/
.. _South: http://south.aeracode.org/


Contributing
------------

* Create something awesome -- make the code better, add some functionality,
  whatever (this is the hardest part).
* `Fork it`_
* Create a topic branch to house your changes
* Get all of your commits in the new topic branch
* Submit a `pull request`_

.. _Fork it: http://help.github.com/forking/
.. _pull request: http://help.github.com/pull-requests/


State of Project
----------------
Armstrong is an open-source news platform that is freely available to any
organization.  It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_, and a grant from the `John S. and James L. Knight
Foundation`_.

To follow development, be sure to join the `Google Group`_.

``armstrong.hatband`` is part of the `Armstrong`_ project.  You're probably
looking for that.

.. _Texas Tribune: http://www.texastribune.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
.. _Google Group: http://groups.google.com/group/armstrongcms
.. _Armstrong: http://www.armstrongcms.org/


License
-------
Copyright 2011-2012 Bay Citizen and Texas Tribune

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
