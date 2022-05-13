=============
html-reporter
=============


.. image:: https://img.shields.io/pypi/v/html-reporter.svg
        :target: https://pypi.python.org/pypi/html-reporter

.. image:: https://img.shields.io/travis/phongnt570/html-reporter.svg
        :target: https://travis-ci.com/phongnt570/html-reporter

.. image:: https://readthedocs.org/projects/html-reporter/badge/?version=latest
        :target: https://html-reporter.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/github/license/phongnt570/html-reporter.svg
        :target: https://opensource.org/licenses/MIT
        :alt: License

.. image:: https://img.shields.io/pypi/pyversions/html-reporter.svg
        :target: https://pypi.org/project/html-reporter
        :alt: Supported Python Versions


A ``TestRunner`` for use with the Python unit testing framework. It generates a report in an HTML file to show the results
at a glance. This package was inspired by ``HTMLTestRunner`` by `Wai Yip Tung`_ and began with transforming the old code to use ``Jinja2`` template and adopting Bootstrap 5 CSS.


Getting started
---------------

Prerequisites
~~~~~~~~~~~~~

``html-reporter`` requires Python 3.7 or later.

Install
~~~~~~~

Install the package via pip:

.. code-block:: console

    $ pip install html-reporter


Usage
~~~~~

``HTMLTestRunner`` is a counterpart to ``unittest.TextTestRunner``. Instantiate an ``HTMLTestRunner`` object and use it to run
your test suite.

Example using ``unittest.main``:

.. code-block:: python

    import unittest

    from html_reporter import HTMLTestRunner

    # output to a file
    if __name__ == "main":
        runner = HTMLTestRunner(
            report_filepath="my_report.html",
            title="My unit test",
            description="This demonstrates the report output by HTMLTestRunner.",
            open_in_browser=True
        )

        # run the test
        unittest.main(testRunner=runner)

Example using ``unittest.TestSuite``:

.. code-block:: python

    import unittest
    from html_reporter import HTMLTestRunner

    # output to a file
    if __name__ == "main":
        my_test_suite = unittest.TestSuite()  # define your test suite
        # add your test cases:
        # my_test_suite.addTest(...)

        runner = HTMLTestRunner(
            report_filepath="my_report.html",
            title="My unit test",
            description="This demonstrates the report output by HTMLTestRunner.",
            open_in_browser=True
        )

        # run the test
        runner.run(my_test_suite)


* Free software: MIT license
* Documentation: https://html-reporter.readthedocs.io.


Features
--------

TODO
----

- [x] Switch to Jinja2 template
- [x] Refactor
- [x] Add support for skipped tests
- [x] Release pypi package
- [ ] Option for combine/separate report files
- [ ] Add tests
- [ ] Improve documentations


Credits
-------

- This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.
- This package was inspired by ``HTMLTestRunner`` by `Wai Yip Tung`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Wai Yip Tung`: <http://tungwaiyip.info/about.html>
