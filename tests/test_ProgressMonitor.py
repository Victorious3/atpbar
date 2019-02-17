# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from atpbar.monitor import ProgressMonitor
from atpbar.reporter import ProgressReporter
from atpbar.report import ProgressReport

##__________________________________________________________________||
@pytest.fixture()
def presentation():
    ret = mock.Mock()
    return ret

@pytest.fixture()
def obj(presentation):
    return ProgressMonitor(presentation)

##__________________________________________________________________||
def test_repr(obj):
    repr(obj)

def test_daemon(obj, presentation):
    presentation.active.return_value = False
    obj.begin()
    assert obj.pickup.daemon
    # end() doesn't need to be called because the pickup is a daemon

def test_begin_end(obj, presentation):
    presentation.active.return_value = False
    obj.begin()
    obj.end()

def test_create_reporter(obj):
    reporter = obj.create_reporter()
    assert isinstance(reporter, ProgressReporter)

def test_send_report(obj, presentation):
    presentation.active.return_value = True
    obj.begin()
    reporter = obj.create_reporter()
    report = ProgressReport('task1', 0, 3)
    reporter.report(report)
    obj.end()

##__________________________________________________________________||