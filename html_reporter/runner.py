"""This module contains the HTMLTestRunner class."""

import datetime
import os
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Type, Union

from jinja2 import Template

from .result import HTMLTestResult, TestCaseResult
from .status import TestStatus

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(
    __file__), "templates", "report_template.html")


@dataclass
class TestCaseReport:
    """Class to keep track of a test case report which is used by the ``Jinja2``
    template.

    :param tid: HTML test case ID (e.g., 'pt1.1', 'ft1.1', 'et1.1', 'st1.1')
    :type tid: str
    :param desc: test case description
    :type desc: str
    :param status: test case status
    :type status: TestStatus
    :param detail: test case detail
    :type detail: str"""
    tid: str
    desc: str
    status: TestStatus
    detail: str


@dataclass
class TestGroupReport:
    """Class to keep track of a test group report which is used by the
    ``Jinja2`` template.

    :param cid: HTML test group ID (e.g., 'c1')
    :type cid: str
    :param desc: test group description
    :type desc: str
    :param pass_count: number of passed test cases
    :type pass_count: int
    :param fail_count: number of failed test cases
    :type fail_count: int
    :param error_count: number of error test cases
    :type error_count: int
    :param skip_count: number of skipped test cases
    :type skip_count: int
    :param test_cases: list of test case reports
    :type test_cases: List[TestCaseReport]"""
    cid: str
    desc: str
    pass_count: int
    fail_count: int
    error_count: int
    skip_count: int
    test_cases: List[TestCaseReport]

    def total_count(self):
        return self.pass_count + self.fail_count \
               + self.fail_count + self.skip_count


class HTMLTestRunner(object):
    """ The main HTMLTestRunner class. """

    def __init__(self,
                 report_filepath: Union[str, Path],
                 verbosity: int = 1,
                 title: str = "Unit Test Report",
                 description: str = "Unit Test Report Description",
                 template: Union[str, Path] = None,
                 open_in_browser: bool = False):
        """Constructor.

        :param report_filepath: path to the report output file
        :type report_filepath: Union[str, Path]
        :param verbosity: verbosity, defaults to 1
        :type verbosity: int, optional
        :param title: HTML page title, defaults to "Unit Test Report"
        :type title: str, optional
        :param description: description of the report,
            defaults to "Unit Test Report Description"
        :type description: str, optional
        :param template: path to the template file,
            if nothing is given, it uses the default template, defaults to None
        :type template: Union[str, Path], optional
        :param open_in_browser: option to open the report file in browser
            after rendering, defaults to False
        :type open_in_browser: bool, optional"""

        self.report_filepath = Path(report_filepath)
        self.verbosity = verbosity

        self.title = title
        self.description = description

        self.template = template
        self.open_in_browser = open_in_browser

        self.start_time = datetime.datetime.now()
        self.stop_time = None

    def run(self, test: Union[unittest.TestCase, unittest.TestSuite]) \
            -> HTMLTestResult:
        """Run the given test case or test suite.
        It calls :py:meth:`~generate_report` to render the HTML report.

        :param test: test case or test suite
        :type test: Union[unittest.TestCase, unittest.TestSuite]
        :return: an HTML test result
        :rtype: HTMLTestResult"""
        try:
            result = HTMLTestResult(verbosity=self.verbosity)
            test(result)
            self.stop_time = datetime.datetime.now()

            self.generate_report(result)

            sys.stderr.write(
                f"\nTime Elapsed: {self.stop_time - self.start_time}\n")

            if self.open_in_browser:
                import webbrowser
                sys.stderr.write("Opening file in browser...\n")
                webbrowser.open_new_tab(
                    f"file://{self.report_filepath.absolute()}")
        finally:
            pass
        return result

    def generate_report(self, result: HTMLTestResult) -> None:
        """Render the HTML report using ``self.template`` template file.
        The following variables are available to the template:

        - ``title``: HTML page title
        - ``description``: description of the report
        - ``result``: the :class:`HTMLTestResult` object
        - ``start_time``: start time of the test run
        - ``stop_time``: stop time of the test run
        - ``test_groups``: list of test groups
            (type: List[:class:`TestGroupReport`])

        :param result: the HTMLTestResult object
        :type result: HTMLTestResult
        """
        test_groups = self.generate_report_table(result)

        output = self._render_html(
            self.template,
            title=self.title,
            description=self.description,
            result=result,
            start_time=self.start_time,
            stop_time=self.stop_time,
            test_groups=test_groups,
        )

        with open(self.report_filepath, "w+") as fp:
            fp.write(output)

    def generate_report_table(self, result: HTMLTestResult) \
            -> List[TestGroupReport]:
        """Generate a list of test group reports.

        :param result: the HTMLTestResult object
        :type result: HTMLTestResult
        :return: list of test group reports
        :rtype: List[TestGroupReport]
        """
        test_groups = []
        sorted_result = self._sort_result(result.result)
        for cid, (cls, cls_results) in enumerate(sorted_result):
            # subtotal for a class
            num_passes = num_fails = num_errors = num_skipped = 0
            for test_case_result in cls_results:
                test_status = test_case_result.status
                if test_status == TestStatus.PASS:
                    num_passes += 1
                elif test_status == TestStatus.FAIL:
                    num_fails += 1
                elif test_status == TestStatus.ERROR:
                    num_errors += 1
                elif test_status == TestStatus.SKIP:
                    num_skipped += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = f"{cls.__module__}.{cls.__name__}"
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and f"{name}: {doc}" or name

            # test cases
            test_cases = []
            for tid, test_case_result in enumerate(cls_results):
                test_cases.append(self.generate_test_case_report(
                    cid, tid, test_case_result))

            test_groups.append(TestGroupReport(
                cid=f"c{cid + 1}",
                desc=desc,
                pass_count=num_passes,
                fail_count=num_fails,
                error_count=num_errors,
                skip_count=num_skipped,
                test_cases=test_cases
            ))

        return test_groups

    def generate_test_case_report(self, cid: int, tid: int,
                                  test_case_result: TestCaseResult) \
            -> TestCaseReport:
        """Generate a test case report.

        :param cid: test group index
        :type cid: int
        :param tid: test case index
        :type tid: int
        :param test_case_result: test case result
        :type test_case_result: TestCaseResult
        :return: test case report
        :rtype: TestCaseReport
        """

        test_status = test_case_result.status
        test_case = test_case_result.test_case
        test_output = test_case_result.output
        test_error = test_case_result.error

        # HTML test case ID, e.g. 'pt1.1', 'ft1.1', 'et1.1', etc
        test_code = "p"
        if test_status == test_status.FAIL:
            test_code = "f"
        elif test_status == test_status.ERROR:
            test_code = "e"
        elif test_status == test_status.SKIP:
            test_code = "s"
        test_case_id = f"{test_code}t{cid + 1}.{tid + 1}"

        # get name of the test method only
        name = test_case.id().split('.')[-1]
        doc = test_case.shortDescription() or ""
        desc = f"{name}: {doc}" if doc else name

        detail = None
        if test_output or test_error:
            detail = f"{test_case_id}: {test_output + test_error}"

        return TestCaseReport(
            tid=test_case_id,
            desc=desc,
            status=test_status,
            detail=detail,
        )

    @staticmethod
    def _sort_result(result_list: List[TestCaseResult]) \
            -> List[Tuple[Type[unittest.TestCase], List[TestCaseResult]]]:
        """ Group and sort test results by class. """
        # unittest does not seem to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for test_case_result in result_list:
            cls = test_case_result.test_case.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append(test_case_result)
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    @staticmethod
    def _load_template(template):
        """ Try to read a file from a given path, if file
            does not exist, load default one. """
        file = None
        try:
            if template:
                with open(template, "r") as f:
                    file = f.read()
        except Exception as err:
            print("Error: Your Template wasn't loaded",
                  err, "Loading Default Template", sep="\n")
        finally:
            if not file:
                with open(DEFAULT_TEMPLATE, "r") as f:
                    file = f.read()
            return file

    def _render_html(self, template, **kwargs):
        """ Render a template with given arguments. """
        template_file = self._load_template(template)
        if template_file:
            template = Template(template_file)
            return template.render(**kwargs)
