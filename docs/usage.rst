.. _usage:

=====
Usage
=====

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

