import pytest
import os


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    print("\nremoving local SQL database...\n")
    os.remove("tests/files/cars.db")