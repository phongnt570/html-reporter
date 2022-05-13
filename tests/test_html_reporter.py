#!/usr/bin/env python

"""Tests for `html_reporter` package."""

import unittest

from html_reporter import HTMLTestRunner


class TestHtmlReporter(unittest.TestCase):
    """Tests for `html_reporter` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_constructor(self):
        """Test something."""
        try:
            runner = HTMLTestRunner(report_filepath='/tmp/test_report.html')
            runner.run(unittest.TestSuite())
        except Exception as e:
            raise e

        self.assertEqual(runner.title, "Unit Test Report")
        self.assertEqual(runner.description, "Unit Test Report Description")
