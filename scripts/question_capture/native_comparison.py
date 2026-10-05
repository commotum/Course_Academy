"""Bounded JSON-lines client for the engine checker; no Python algebra or builds.

Install with cargo build --offline --bin compare-question-answers. Missing native
support is an explicit unresolved comparison, never proof of a different answer.
"""
import atexit
import functools
import hashlib
import json
import os
import selectors
import subprocess
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIMEOUT = 3
_process = None
_signature = None
_lock = threading.Lock()


def binary():
    return Path(os.environ.get('COURSE_ACADEMY_MATH_COMPARE_BIN',
                               str(ROOT/'target/debug/compare-question-answers')))


@functools.lru_cache(maxsize=8)
def _binary_hash(path, modified, size):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def availability():
    path = binary()
    try:
        info = path.stat()
        return (str(path), _binary_hash(str(path),info.st_mtime_ns,info.st_size), info.st_size, info.st_mode)
    except OSError:
        return (str(path), None, None, None)


def close():
    global _process, _signature
    if _process is not None:
        _process.kill() if _process.poll() is None else None
        _process.wait()
        _process.stdin.close()
        _process.stdout.close()
    _process = _signature = None


atexit.register(close)


@functools.lru_cache(maxsize=2048)
def _compare(a, b, prompt, titles, signature):
    global _process, _signature
    request = (json.dumps(dict(a=a, b=b, prompt=prompt, kp_titles=titles))+'\n').encode()
    if len(request) > 32768:
        return {'outcome':'unresolved', 'reason':'comparison request exceeds 32768 bytes'}
    with _lock:
        try:
            if _signature != signature or _process is None or _process.poll() is not None:
                close()
                _process = subprocess.Popen([signature[0]], stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
                os.set_blocking(_process.stdin.fileno(), False)
                os.set_blocking(_process.stdout.fileno(), False)
                _signature = signature
            deadline, sent, reply_bytes = time.monotonic()+TIMEOUT, 0, b''
            with selectors.DefaultSelector() as ready:
                ready.register(_process.stdin, selectors.EVENT_WRITE)
                ready.register(_process.stdout, selectors.EVENT_READ)
                while b'\n' not in reply_bytes:
                    remaining = deadline-time.monotonic()
                    if remaining <= 0:
                        raise TimeoutError('native comparison exceeded %ss' % TIMEOUT)
                    for key, _ in ready.select(remaining):
                        if key.fileobj is _process.stdin:
                            sent += os.write(_process.stdin.fileno(), request[sent:sent+4096])
                            if sent == len(request):
                                ready.unregister(_process.stdin)
                        else:
                            chunk = os.read(_process.stdout.fileno(), 4096)
                            if not chunk:
                                raise ValueError('native helper exited without a response')
                            reply_bytes += chunk
                            if len(reply_bytes) > 32768:
                                raise ValueError('native response exceeds 32768 bytes')
            reply = json.loads(reply_bytes)
            if reply.get('outcome') not in ('equivalent','different','unresolved'):
                raise ValueError('invalid native comparison outcome')
            return reply
        except (OSError, ValueError, TypeError, AttributeError, TimeoutError) as error:
            close()
            return {'outcome':'unresolved', 'reason':'native execution failed: '+str(error)}
        except BaseException:
            close()
            raise


def compare(a, b, *, prompt='', kp_titles=()):
    return _compare(a, b, prompt, tuple(kp_titles), availability()).copy()
