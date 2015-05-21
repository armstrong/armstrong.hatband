armstrong.hatband
=================
Provides an enhanced Django admin interface and utilities for use in
`Armstrong`_.

Notably it brings `VisualSearch.js`_ for fast content lookup, `CKEditor`_
as a fully featured rich-text editor and other features like drag 'n drop
JavaScript for easy programming of orderable content (like lists).

.. _VisualSearch.js: http://documentcloud.github.io/visualsearch/
.. _CKEditor: http://ckeditor.com/


Usage
-----

**TODO**


Installation & Configuration
----------------------------
Supports Django 1.3, 1.4, 1.5, 1.6 on Python 2.6 and 2.7.

#. ``pip install armstrong.hatband``

#. Add ``armstrong.hatband`` to your ``INSTALLED_APPS``

#. In ``urls.py`` replace the normal admin with Hatband,
   ``from armstrong import hatband as admin``.

   The rest of the URL configuration stays identical to what is expected for
   the traditional Django admin.


Contributing
------------
Development occurs on Github. Participation is welcome!

* Found a bug? File it on `Github Issues`_. Include as much detail as you
  can and make sure to list the specific component since we use a centralized,
  project-wide issue tracker.
* Testing? ``pip install tox`` and run ``tox``
* Have code to submit? Fork the repo, consolidate your changes on a topic
  branch and create a `pull request`_. The `armstrong.dev`_ package provides
  tools for testing, coverage and South migration as well as making it very
  easy to run a full Django environment with this component's settings.
* Questions, need help, discussion? Use our `Google Group`_ mailing list.

.. _Github Issues: https://github.com/armstrong/armstrong/issues
.. _pull request: http://help.github.com/pull-requests/
.. _armstrong.dev: https://github.com/armstrong/armstrong.dev
.. _Google Group: http://groups.google.com/group/armstrongcms


State of Project
----------------
`Armstrong`_ is an open-source news platform that is freely available to any
organization. It is the result of a collaboration between the `Texas Tribune`_
and `Bay Citizen`_ and a grant from the `John S. and James L. Knight
Foundation`_. Armstrong is available as a complete bundle and as individual,
stand-alone components.

.. _Armstrong: http://www.armstrongcms.org/
.. _Bay Citizen: http://www.baycitizen.org/
.. _Texas Tribune: http://www.texastribune.org/
.. _John S. and James L. Knight Foundation: http://www.knightfoundation.org/
