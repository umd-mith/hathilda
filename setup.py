import sys

from setuptools import setup, Command

dependencies = open('requirements.txt').read().split()

class PyTest(Command):
    """
    A command to convince setuptools to run pytests.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        errno = pytest.main("test.py")
        sys.exit(errno)

setup(
    name = 'hathilda',
    version = '0.0.12',
    url = 'http://github.com/umd_mith/hathild',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['hathilda'],
    description = 'Turn HathiTrust Data into JSON-LD',
    cmdclass = {'test': PyTest},
    install_requires = dependencies,
    tests_require=['pytest'],
    scripts = ['hathilda.py'],
)
