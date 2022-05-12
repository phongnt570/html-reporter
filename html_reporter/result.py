"""This module contains the HTMLTEstRunner class."""

import sys
from dataclasses import dataclass
from io import StringIO
from typing import List
from unittest import TestCase, TestResult

from .redirector import OutputRedirector
from .status import TestStatus

# The redirectors are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.

# e.g.
# >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
# >>>
stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


@dataclass
class TestCaseResult:
    """A dataclass representing a test case result.

    :param status: the test case status
    :type status: TestStatus
    :param test_case: the test case object
    :type test_case: unittest.TestCase
    :param output: the test case output
    :type output: str
    :param error: the test case error
    :type error: str
    """
    status: TestStatus
    test_case: TestCase
    output: str
    error: str


class HTMLTestResult(TestResult):
    """HTMLTestResult is a pure representation of results.
    It lacks the output and reporting ability compares to
    ``unittest.TextTestResult``."""

    def __init__(self, descriptions=None, verbosity: int = 1):
        """Constructor.

        :param descriptions: descriptions, defaults to None
        :type descriptions: optional
        :param verbosity: verbosity, defaults to 1
        :type verbosity: int, optional
        """
        TestResult.__init__(self)
        self.outputBuffer = None
        self.stdout0 = None
        self.stderr0 = None
        self.pass_count = 0
        self.fail_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity
        self.show_all = self.verbosity > 1
        self.descriptions = descriptions

        self.result: List[TestCaseResult] = []

    def get_description(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        """Called when the given test is about to be run."""
        TestResult.startTest(self, test)

        if self.show_all:
            sys.stderr.write(self.get_description(test))
            sys.stderr.write(" ... ")
            sys.stderr.flush()

        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        """Called when the given test has been run."""
        # Usually one of addSuccess, addError or addFailure, addSkip would have
        # been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be
        # called.
        self.complete_output()

    def addSuccess(self, test):
        """Called when a test has completed successfully."""
        self.pass_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append(TestCaseResult(TestStatus.PASS, test, output, ''))
        if self.show_all:
            sys.stderr.write("ok\n")
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append(TestCaseResult(
            TestStatus.ERROR, test, output, _exc_str))
        if self.show_all:
            sys.stderr.write("ERROR\n")
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.fail_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append(TestCaseResult(
            TestStatus.FAIL, test, output, _exc_str))
        if self.show_all:
            sys.stderr.write("FAIL\n")
        else:
            sys.stderr.write('F')

    def addSkip(self, test, reason):
        self.skip_count += 1
        TestResult.addSkip(self, test, reason)
        output = self.complete_output()
        self.result.append(TestCaseResult(
            TestStatus.SKIP, test, output, reason))
        if self.show_all:
            sys.stderr.write("skipped {0!r}\n".format(reason))
        else:
            sys.stderr.write('S')

    def total_count(self):
        return self.pass_count + self.fail_count \
            + self.error_count + self.skip_count
