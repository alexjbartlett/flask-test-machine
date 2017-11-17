Flask Test Engine
=================

This package provides some additional tools for use when testing
Flask applications with HTML interfaces.

It is currently in version 0.0.2 and not ready for use by anyone.

Wrap a standard Flask test client with a flasktestmachine.Browser object

    from flasktestmachine import Browser
    app = Flask()
    client = app.test_client()
    Browser(client)


Credits
-------

- `Distribute`_
- `Buildout`_
- `modern-package-template`_

.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
