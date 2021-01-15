Django cookie consent
=====================

![PyPI - License](https://img.shields.io/pypi/l/django-cookie-consent)

This is a fork of [django-cookie-consent](https://pypi.org/project/django-cookie-consent/).

django-cookie-consent is a reusable application for managing various
cookies and visitors consent for their use in Django project.

support ranges from django 2.2 and python 3.7

Features:

* cookies and cookie groups are stored in models for easy management
  through Django admin interface

* support for both opt-in and opt-out cookie consent schemes

* removing declined cookies (or non accepted when opt-in scheme is used)

* logging user actions when they accept and decline various cookies

* easy adding new cookies and seamlessly re-asking for consent for new cookies

Documentation
-------------

https://django-cookie-consent.readthedocs.org/en/latest/


Configuration
-------------

1. Add ``cookie_consent`` to your ``INSTALLED_APPS``.

2. Add ``django.template.context_processors.request``
   to ``TEMPLATE_CONTEXT_PROCESSORS`` if it is not already added.

3. Include django-cookie-consent urls in ``urls.py``::

    path('cookies/', include('cookie_consent.urls'))

4. Run ``migrate`` django management command.
