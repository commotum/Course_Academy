"""Run the existing Python engine tests as an oracle for the Rust port.

Records real calls made by those tests, then executes the same captured inputs
through the Rust binary. No Python is invoked by the Rust implementation.
"""
import dataclasses
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import unittest
from collections.abc import Mapping
from datetime import datetime
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engine import schema, runtime
from engine.fire.core import FireEngine

CASES = []
DEPTH = 0

def encode(value):
    if isinstance(value, schema.Keyword): return {'$keyword': str(value)}
    if isinstance(value, UUID): return {'$uuid': str(value)}
    if isinstance(value, datetime): return {'$instant': schema.instant(value).isoformat(timespec='milliseconds').replace('+00:00', 'Z')}
    if dataclasses.is_dataclass(value): return {f.name: encode(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, Mapping): return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)): return [encode(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value): return {'$float': str(value)}
    return value

def snapshot_payload(snapshot):
    return {'entities': encode(snapshot.entities), 'basis_t': snapshot.basis_t,
            'status_history': encode(snapshot.status_history)}

def snap(loaded):
    return {'snapshot': snapshot_payload(loaded.snapshot),
            'learner_eid': loaded.learner_eid, 'policy_eid': loaded.policy_eid, 'engine': encode(loaded.engine.snapshot())}

def wrap(owner, name, request, response):
    original = getattr(owner, name)
    def wrapped(*args, **kwargs):
        global DEPTH
        outer = DEPTH == 0
        entry = request(*args, **kwargs) if outer else None
        DEPTH += 1
        try:
            result = original(*args, **kwargs)
        except (ValueError, TypeError, KeyError) as error:
            if outer: CASES.append({'input': entry, 'error': str(error)})
            raise
        else:
            if outer: CASES.append({'input': entry, 'expected': response(result, *args, **kwargs)})
            return result
        finally:
            DEPTH -= 1
    setattr(owner, name, wrapped)

def engine_request(name):
    def request(engine, *args, **kwargs):
        value = {'op': name, 'engine': encode(engine.snapshot())}
        if name.startswith('apply'): value['event'] = encode(args[0])
        else:
            value.update(learner=args[0], at=args[1])
            if name == 'rank': value['candidates'] = encode(args[2])
        return value
    return request

for name in ('apply', 'apply_accuracy', 'apply_retention', 'due', 'rank'):
    wrap(FireEngine, name, engine_request(name),
         lambda result, engine, *a, **k: {'output': encode(result), 'engine': encode(engine.snapshot())})

for name in ('complete_item', 'expire_task'):
    wrap(runtime, name,
         lambda loaded, target, _name=name, **kw: {'op': _name, **snap(loaded), 'target': target, 'options': encode(kw)},
         lambda actual, *a, **k: {'transaction': encode(actual.transaction), 'delivery': encode(actual.delivery), 'engine': encode(actual.engine.snapshot())})

wrap(runtime, 'transition_item',
     lambda loaded, target, status, at: {'op': 'transition_item', **snap(loaded),
                                       'target': target, 'status': status, 'at': encode(at)},
     lambda actual, *a, **k: {'transaction': encode(actual)})

for name in ('completion_transaction', 'task_transaction'):
    wrap(schema, name,
         lambda loaded, target, at, changes, engine, _name=name: {'op': _name, **snap(loaded), 'target': target, 'completed_at': encode(at), 'changes': encode(changes), 'updated_engine': encode(engine.snapshot())},
         lambda actual, *a, **k: {'transaction': encode(actual)})

wrap(schema, 'load_runtime',
     lambda snapshot, learner, policy: {'op': 'load_runtime', 'snapshot': snapshot_payload(snapshot), 'learner_eid': learner, 'policy_eid': policy},
     lambda actual, *a, **k: {'engine': encode(actual.engine.snapshot())})

def equivalent(expected, actual, path=''):
    # Fingerprints identify serialized configurations/events. The typed Rust
    # API normalizes integer-vs-float spellings. Compare their full payloads.
    ignored = {'event_hash', 'policy_id', 'graph_id', 'difficulty_id', 'neighborhood_id', 'edn'}
    if isinstance(expected, dict):
        assert isinstance(actual, dict), (path, type(expected), actual)
        ek, ak = set(expected) - ignored, set(actual) - ignored
        assert ek == ak, (path, ek ^ ak)
        for key in ek: equivalent(expected[key], actual[key], path + '/' + key)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(expected) == len(actual), (path, len(expected), actual)
        for i, (x, y) in enumerate(zip(expected, actual)): equivalent(x, y, f'{path}/{i}')
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        assert isinstance(actual, (int, float)) and not isinstance(actual, bool), (path, expected, actual)
        assert math.isclose(expected, actual, rel_tol=2e-12, abs_tol=2e-12), (path, expected, actual)
    else: assert expected == actual, (path, expected, actual)

def main():
    suite = unittest.TestSuite()
    for pattern in ('test_fire_core.py', 'test_engine_activities.py', 'test_fire_calibration.py', 'test_engine_schema.py', 'test_engine_runtime.py'):
        suite.addTests(unittest.defaultTestLoader.discover(str(ROOT/'tests'), pattern=pattern))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful(): return 1
    binary = os.environ.get('FIRE_BIN', str(ROOT/'target/debug/fire'))
    completed = subprocess.run([binary, 'batch'], input=''.join(json.dumps(c['input'], allow_nan=False)+'\n' for c in CASES), text=True, capture_output=True)
    if completed.returncode: raise RuntimeError(completed.stderr)
    outputs = [json.loads(line) for line in completed.stdout.splitlines()]
    assert len(outputs) == len(CASES), (len(outputs), len(CASES), completed.stderr)
    failures = []
    for index, (case, output) in enumerate(zip(CASES, outputs)):
        try:
            if 'error' in case: assert 'error' in output, ('expected rejection', case['error'], output)
            else:
                assert 'ok' in output, output
                equivalent(case['expected'], output['ok'])
        except AssertionError as error: failures.append((index, case['input']['op'], str(error)))
    for failure in failures[:20]: print('PARITY FAILURE', *failure)
    Path('/tmp/course-academy-rust-parity.json').write_text(json.dumps(CASES, allow_nan=False))
    print(f'{len(CASES)-len(failures)}/{len(CASES)} Python/Rust differential cases agree.')
    return bool(failures)

if __name__ == '__main__': sys.exit(main())
