"""Run retained strict tests on the captured failing runtime and revision.

All copied runtimes and redirected author outputs are under evidence_root.
"""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, pathlib, shutil, subprocess

E = pathlib.Path(__file__).resolve().parent
J = E.parent
W = J / 'workspace'
PY = '/home/jake/Developer/Course_Academy/.venv/bin/python'

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

old = E / 'failing-runtime'
(old / '17592186119847').mkdir(parents=True, exist_ok=True)
shutil.copyfile(W / 'evidence/root-cause/before-generator.py', old / '17592186119847.py')
shutil.copyfile(W / '17592186119847/source.json', old / '17592186119847/source.json')
prior = json.load(open(J / 'review-3-policy-2-092f7adc069513f2/package-before.json'))
assert hashlib.sha256((old / '17592186119847.py').read_bytes()).hexdigest() == prior['17592186119847.py']

results = []
for runtime, expected in [(old, 1), (W, 0)]:
    cmd = [PY, '-B', str(E / 'restriction-regression.py'), str(runtime)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    suffix = 'before' if runtime == old else 'current'
    (E / f'strict-{suffix}.stdout').write_text(p.stdout)
    (E / f'strict-{suffix}.stderr').write_text(p.stderr)
    assert (p.returncode != 0) == bool(expected)
    results.append(dict(command=cmd, returncode=p.returncode, expected=expected,
                        diagnostic=p.stderr[-1800:], stdout_file=f'strict-{suffix}.stdout'))

# Execute the exact preflight script using its copied dependencies, changing
# only read/write locations. Verify it fails the bound old implementation too.
sys.path.insert(0, str(E / 'retained-checks'))
cr = module(E / 'retained-checks/check_repair.py', 'check_repair')
sys.modules['check_repair'] = cr
restriction = module(E / 'retained-checks/check_restriction.py', 'restriction')
for runtime, should_pass in [(old, False), (W, True)]:
    suffix = 'before' if runtime == old else 'current'
    cr.E = E / ('preflight-' + suffix)
    (cr.E / 'root-cause').mkdir(parents=True, exist_ok=True)
    restriction.g = module(runtime / '17592186119847.py', 'g_' + suffix)
    try:
        restriction.main()
        outcome, diagnostic = True, None
    except (AssertionError, ValueError) as error:
        outcome, diagnostic = False, repr(error)
    assert outcome == should_pass
    results.append(dict(script='check_restriction.py', runtime=str(runtime),
                        passed=outcome, expected_pass=should_pass, diagnostic=diagnostic))

# Confirm historical silent truncation/envelope checks have real failing examples.
legacy = module(W / 'evidence/legacy-generator.py', 'legacy')
legacy_result = legacy.batch('easy', 13, 0)
assert len(legacy_result) == 12
cc = sys.modules['check_cli_contract']
assert cc.decode(json.dumps({'instances': [1, 2, 3, 4, 5]})) is None

# Fresh malformed/impossible domain cases should fail explicitly, without any
# generator output. This is independent of the author preflight's three cases.
g = module(W / '17592186119847.py', 'current')
invalid = []
for level, params in [
    ('easy', dict(name='Q', rows=3, columns=7, count=4, kind='pivot')),
    ('moderate', dict(name='Q', rows=3, columns=7, count=3, kind='non-pivot')),
    ('moderate', dict(name='Q', rows=4, columns=7, count=8, kind='non-pivot')),
    ('moderate', dict(name='Q', rows=4, columns=7, count=7, kind='non-pivot')),
]:
    try:
        g.generate(level, 90291, parameters=params)
    except ValueError as error:
        invalid.append(dict(level=level, parameters=params, rejected=str(error)))
    else:
        raise AssertionError(('Impossible case accepted', params))

(E / 'regression-tests.json').write_text(json.dumps(dict(
    preflight=json.load(open(J / 'repair-preflight.json')), checks=results,
    historical_count=dict(requested=13, returned=len(legacy_result)),
    historical_envelope_rejected_by_runner_decoder=True, invalid_cases=invalid,
    source='Exact retained finding and scripts; bound failing runtime hash verified.'
), indent=2) + '\n')
print(json.dumps(dict(strict_before_fails=True, strict_current_passes=True,
                     preflight_before_fails=True, preflight_current_passes=True,
                     independent_invalid_cases=len(invalid))))
