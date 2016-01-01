from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd


def test_pep8():
    print("Checking PEP-8 conformity")
    local("pep8 --ignore=E114,E111,E501 .")


def unit_tests():
    print("Running Unit Tests")
    local("python ./cmplync_tests.py")


def test():
    test_pep8()
    unit_tests()

def run():
    local("python cmplync.py")
