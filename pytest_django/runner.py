import os
from optparse import make_option

import pytest


class PyTestRunner(object):
    """
    Runs py.test to discover and run tests.
    """
    option_list = (
        make_option('-k', '--keepdb',
                    action='store_true', dest='keepdb', default=False,
                    help='Preserves the test DB between runs.'),
    )

    def __init__(self, verbosity=1, interactive=True, failfast=False,
                 keepdb=False, settings=None, **kwargs):
        self.verbosity = verbosity
        self.interactive = interactive
        self.failfast = failfast
        self.keepdb = keepdb
        self.ds = settings or os.environ['DJANGO_SETTINGS_MODULE']

    def run_tests(self, test_labels):
        """
        Run py.test and returns the exitcode.
        """

        # Translate arguments
        argv = ['--ds', self.ds]
        if self.verbosity == 0:
            argv.append('--quiet')
        if self.verbosity == 2:
            argv.append('--verbose')
        if self.failfast:
            argv.append('--exitfirst')
        if self.keepdb:
            argv.append('--nomigrations')

        argv.extend(test_labels)
        return pytest.main(argv)
