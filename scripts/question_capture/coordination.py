"""Serialize only installation of tested shared source repairs."""
import contextlib
import fcntl
from core import ROOT


@contextlib.contextmanager
def source_install_lock():
    path=ROOT/'.local/question_capture-fleet/source-install.lock'
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        yield
