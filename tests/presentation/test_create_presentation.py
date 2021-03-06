# Tai Sakuma <tai.sakuma@gmail.com>
import sys

import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock

has_jupyter_notebook = False
try:
    import ipywidgets as widgets
    from IPython.display import display
    has_jupyter_notebook = True
except ImportError:
    pass

from atpbar.presentation.create import create_presentation

##__________________________________________________________________||
@pytest.fixture(
    params=[True, False]
)
def isatty(request, monkeypatch):
    ret = request.param
    org_stdout = sys.stdout
    f = mock.Mock(**{
        'stdout.isatty.return_value': ret,
        'stdout.write.side_effect': lambda x : org_stdout.write(x)
    })
    module = sys.modules['atpbar.presentation.create']
    monkeypatch.setattr(module, 'sys', f)
    return ret

##__________________________________________________________________||
if has_jupyter_notebook:
    is_jupyter_notebook_parames = [True, False]
else:
    is_jupyter_notebook_parames = [False]

@pytest.fixture(params=is_jupyter_notebook_parames)
def is_jupyter_notebook(request, monkeypatch):
    ret = request.param
    f = mock.Mock()
    f.return_value = ret
    module = sys.modules['atpbar.presentation.create']
    monkeypatch.setattr(module, 'is_jupyter_notebook', f)
    return ret

##__________________________________________________________________||
def test_create_presentation(isatty, is_jupyter_notebook):
    actual = create_presentation()

    if isatty:
        assert 'ProgressBar' == actual.__class__.__name__
    elif is_jupyter_notebook:
        assert 'ProgressBarJupyter' == actual.__class__.__name__
    else:
        assert 'ProgressPrint' == actual.__class__.__name__

##__________________________________________________________________||
