import os
from dotenv import load_dotenv

# Source: https://stackoverflow.com/questions/17801300/how-to-run-a-method-before-all-tests-in-all-classes


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    test_env_file = "{}/open_lisa/config/test.env".format(
        os.path.dirname(__file__))
    load_dotenv(test_env_file)


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
