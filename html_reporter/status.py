"""This module contains the TestStatus class."""

import enum


class TestStatus(enum.Enum):
    """ Test status code. """
    PASS = 1
    FAIL = 2
    ERROR = 3
    SKIP = 4
