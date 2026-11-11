"""Read Codex account usage without starting a thread or inference turn.

The protocol comes from the installed ``codex app-server generate-ts`` bindings.
Only the generator supervisor calls this module; workers have no quota policy.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import time


class QuotaUnavailable(RuntimeError):
    """A cutoff cannot safely be enforced with the available account data."""


def _number(value, description):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise QuotaUnavailable(f'Codex returned an invalid {description}')
    return value


def normalise_quota(payload, *, model='gpt-6.1-sol', checked_at=None):
    """Use shared Codex limits plus any bucket explicitly belonging to our model.

    Other model quotas do not constrain this generator. Paid credits do not
    inflate the included-usage percentages the user's cutoff is protecting.
    """
    if not isinstance(payload, dict):
        raise QuotaUnavailable('Codex returned an invalid account quota response')
    buckets = payload.get('rateLimitsByLimitId')
    if buckets is None:
        buckets = {}
    if not isinstance(buckets, dict):
        raise QuotaUnavailable('Codex returned invalid account quota buckets')
    selected = {}
    shared = buckets.get('codex') or payload.get('rateLimits')
    if isinstance(shared, dict) and (shared.get('limitId') in (None, 'codex', model)
                                     or shared.get('normalModelSlug') == model):
        identity = shared.get('limitId') or 'codex'
        selected[identity] = shared
    for identity, bucket in buckets.items():
        if isinstance(bucket, dict) and (identity == model or bucket.get('normalModelSlug') == model):
            selected[identity] = bucket
    windows = []
    exhausted = payload.get('ordinaryUsageAllowed') is False
    for identity, bucket in selected.items():
        exhausted |= (bucket.get('spendControlReached') is True
                      or bucket.get('rateLimitReachedType') is not None)
        for period in ('primary', 'secondary', 'individualLimit'):
            window = bucket.get(period)
            if window is None:
                continue
            if not isinstance(window, dict):
                raise QuotaUnavailable('Codex returned an invalid quota window')
            if period == 'individualLimit':
                remaining = _number(window.get('remainingPercent'), 'remaining percentage')
            else:
                used = _number(window.get('usedPercent'), 'used percentage')
                if used < 0:
                    raise QuotaUnavailable('Codex returned a negative usage percentage')
                remaining = 100 - used
            if remaining > 100:
                raise QuotaUnavailable('Codex returned a remaining percentage above 100')
            reset_at = window.get('resetsAt')
            if reset_at is not None:
                _number(reset_at, 'quota reset time')
            duration = window.get('windowDurationMins')
            if duration is not None:
                _number(duration, 'quota window duration')
            windows.append({'name': f'{identity}:{period}',
                            'remaining_percent': max(0, remaining),
                            'reset_at': reset_at, 'duration_minutes': duration})
    if not windows:
        raise QuotaUnavailable('Codex did not supply percentage-based quota windows for this account')
    remaining = min(window['remaining_percent'] for window in windows)
    return {'remaining_percent': remaining, 'windows': windows,
            'checked_at': time.time() if checked_at is None else checked_at,
            'ordinary_usage_allowed': payload.get('ordinaryUsageAllowed'),
            'exhausted': exhausted or remaining <= 0}


def fetch_quota(*, environment=None, executable=None, timeout=30, model='gpt-6.1-sol'):
    """Bounded stdio RPC: initialize, initialized, account/rateLimits/read.

    No thread or turn is created. The subprocess owns a separate process group
    and is always reaped, including on malformed responses and timeouts. Raw
    account identifiers, credits, RPC errors, and auth diagnostics are omitted
    from the result and exceptions.
    """
    if timeout <= 0:
        raise ValueError('Quota timeout must be positive')
    env = dict(os.environ if environment is None else environment)
    executable = (executable or env.get('COURSE_ACADEMY_CODEX_EXECUTABLE')
                  or shutil.which('codex', path=env.get('PATH'))
                  or str(Path.home() / '.local/bin/codex'))
    deadline = time.monotonic() + timeout
    try:
        process = subprocess.Popen([str(executable), 'app-server', '--listen', 'stdio://'],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL, env=env, start_new_session=True)
    except OSError as error:
        raise QuotaUnavailable('Could not start the Codex account quota reader') from error
    selector = selectors.DefaultSelector()
    buffer = b''
    try:
        selector.register(process.stdout, selectors.EVENT_READ)

        def send(message):
            try:
                process.stdin.write(json.dumps(message).encode() + b'\n')
                process.stdin.flush()
            except (OSError, ValueError) as error:
                raise QuotaUnavailable('Codex quota reader closed its input') from error

        def response(request_id):
            nonlocal buffer
            received = 0
            while True:
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    try:
                        message = json.loads(line)
                    except (UnicodeDecodeError, ValueError) as error:
                        raise QuotaUnavailable('Codex quota reader returned invalid JSON') from error
                    if not isinstance(message, dict):
                        raise QuotaUnavailable('Codex quota reader returned an invalid RPC message')
                    if message.get('id') == request_id:
                        if 'error' in message:
                            raise QuotaUnavailable('Codex account quota request failed; check Codex login and connectivity')
                        if 'result' not in message:
                            raise QuotaUnavailable('Codex quota response omitted its result')
                        return message['result']
                remaining = deadline - time.monotonic()
                if remaining <= 0 or not selector.select(remaining):
                    raise QuotaUnavailable('Timed out reading Codex account quota')
                chunk = os.read(process.stdout.fileno(), 65536)
                if not chunk:
                    raise QuotaUnavailable('Codex quota reader exited before returning account quota')
                received += len(chunk)
                if received > 4 * 1024 * 1024:
                    raise QuotaUnavailable('Codex quota response exceeded its size limit')
                buffer += chunk

        send({'id': 1, 'method': 'initialize', 'params': {
            'clientInfo': {'name': 'course_academy_quota', 'title': 'Course Academy quota', 'version': '0.1.0'},
            'capabilities': {'experimentalApi': False, 'requestAttestation': False}}})
        response(1)
        send({'method': 'initialized'})
        send({'id': 2, 'method': 'account/rateLimits/read',
              'params': {'excludeResetCreditDetails': True}})
        return normalise_quota(response(2), model=model)
    finally:
        selector.close()
        try:
            process.stdin.close()
        except OSError:
            pass
        process.stdout.close()
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
