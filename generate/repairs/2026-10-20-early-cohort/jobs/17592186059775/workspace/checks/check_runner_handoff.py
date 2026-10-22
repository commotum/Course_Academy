"""Exercise original/patched runner sample control flow without writes/services.

This validates a proposed external fix, not an installed repair. Real package,
source, engine, report and binding are read; mutation boundaries are tripwires.
The separate registered regressions test the actual generator and delivery.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = W.parent
sys.path.insert(0, str(REPO/'scripts'))


def module(name, source, filename):
    spec = importlib.util.spec_from_loader(name, loader=None)
    result = importlib.util.module_from_spec(spec)
    result.__file__ = str(filename)
    exec(compile(source, str(filename), 'exec'), result.__dict__)
    return result


class Repaired(Exception):
    pass


def main():
    spec = importlib.util.spec_from_file_location('stage_patch', W/'runner-fix/stage_patch.py')
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)
    source = stage.RUNNER.read_text()
    proposed = stage.build(source)
    metadata = json.loads((W/'runner-fix/patch.json').read_text())
    assert hashlib.sha256(source.encode()).hexdigest() == metadata['base_sha256']
    assert hashlib.sha256(proposed.encode()).hexdigest() == metadata['proposed_sha256']
    assert hashlib.sha256((W/'runner-fix/evidence-only-rejection.patch').read_bytes()).hexdigest() == metadata['patch_sha256']
    with tempfile.TemporaryDirectory() as td:
        checkout = Path(td)
        (checkout/'scripts').mkdir()
        target = checkout/'scripts/generator_pipeline.py'
        target.write_text(source)
        # Only the disposable checkout is patched. Confirm the distributable
        # diff produces the same source used by the control-flow tests.
        applied = subprocess.run(['patch', '--batch', '-p1', '-d', str(checkout), '-i',
                                  str(W/'runner-fix/evidence-only-rejection.patch')],
                                 text=True, capture_output=True, check=True)
        assert target.read_text() == proposed, applied.stdout
    old = module('original_pipeline_handoff', source, stage.RUNNER)
    new = module('proposed_pipeline_handoff', proposed, stage.RUNNER)
    snapshot = json.loads((JOB/'job.json').read_text())
    manifest = json.loads((W/'package.json').read_text())
    runtime_before = {name: hashlib.sha256((W/name).read_bytes()).hexdigest()
                      for name in ['package.json', *manifest['files']]}
    package_hash = old.package_digest(W, manifest['entrypoint'], manifest['files'],
                                      dependencies=manifest['dependencies'])
    assert package_hash == snapshot['last_rejected_package']
    assert old.digest(old.read(JOB/'source/source.json')) == snapshot['last_rejected_source']
    previous_path = Path(snapshot['previous_review']['directory'])/'result.json'
    previous = old.read(previous_path)
    old.validate_review(previous, previous_path.parent)
    results = []

    def exercise(label, implementation, change_state=None, change_report=None,
                 regression_failure=False, expect_allowed=False):
        runner = object.__new__(implementation.Pipeline)
        runner.state = copy.deepcopy(snapshot)
        runner.state['stage'] = 'sample'
        runner.directory, runner.root = JOB, REPO
        if change_state:
            change_state(runner.state)
        # Establish actual native-engine identity, not a copied expected hash.
        actual_engine = runner.engine_identity()
        assert actual_engine == snapshot['last_rejected_engine']
        calls = []
        runner.candidate_hash = lambda: package_hash
        runner.engine_identity = lambda: actual_engine
        def persist(**updates):
            runner.state.update(updates)
        def repair(reason):
            calls.append('repair')
            raise Repaired(str(reason))
        def regressions():
            calls.append('retained_regressions')
            if regression_failure:
                raise ValueError('Retained finding persists')
        def sample():
            calls.append('sample')
        def forbidden(*args, **kwargs):
            raise AssertionError('External service or publication boundary reached')
        runner.persist, runner.repair = persist, repair
        runner.check_repair_regressions, runner.sample = regressions, sample
        runner.session = forbidden
        runner.verify_approval_inputs = forbidden
        runner.review_candidate = forbidden
        runner.admit_publication = forbidden
        original_read = implementation.read
        def read_report(path):
            result = original_read(path)
            if Path(path) == previous_path and change_report:
                result = copy.deepcopy(result)
                change_report(result)
            return result
        implementation.read = read_report
        try:
            state = runner._run('generate')
            allowed = state['stage'] == 'validate'
            assert allowed and calls == ['retained_regressions', 'sample']
        except Repaired as error:
            allowed = False
            rejection = str(error)
        finally:
            implementation.read = original_read
        assert allowed == expect_allowed, (label, calls)
        if not allowed:
            assert 'sample' not in calls, (label, calls)
            if regression_failure:
                assert calls == ['retained_regressions', 'repair'], (label, calls)
                assert 'Retained finding persists' in rejection
            else:
                assert calls == ['repair'] and 'byte-identical' in rejection, (label, calls, rejection)
        results.append({'case': label, 'reaches_fresh_review': allowed, 'calls': calls,
                        **({} if allowed else {'rejection': rejection})})

    exercise('exact original repeated-candidate failure', old)
    exercise('actual evidence-only report with unchanged complete binding', new, expect_allowed=True)
    for kind in ('decision_shortcut', 'grading', 'math', 'scope'):
        exercise('content finding: '+kind, new,
                 change_report=lambda r, k=kind: r['findings'][0].update(kind=k))
    exercise('mixed evidence and shortcut findings', new,
             change_report=lambda r: r['findings'].append({**r['findings'][0], 'kind': 'decision_shortcut'}))
    exercise('empty findings', new, change_report=lambda r: r.update(findings=[]))
    exercise('accepted report cannot be used as an exemption', new,
             change_report=lambda r: r.update(verdict='accepted'))
    exercise('invalid report paths', new,
             change_report=lambda r: r['source_analysis'].update(evidence_paths=['absent-provenance.json']))
    exercise('missing independent report', new,
             change_state=lambda s: s['previous_review'].update(directory=str(W/'absent-review')))
    exercise('report root escapes this job', new,
             change_state=lambda s: s['previous_review'].update(directory='/tmp/absent-review'))
    for key in ('package_hash', 'batch_hash', 'source_hash', 'inventory_hash', 'engine_hash',
                'assets', 'effective_difficulty', 'policy_version'):
        exercise('prior binding mismatch: '+key, new,
                 change_state=lambda s, k=key: s['previous_review']['binding'].update({k: 'changed'}))
    exercise('failed retained regression still blocks', new, regression_failure=True)
    exercise('postpublication use is excluded', new,
             change_state=lambda s: s.update(review_after_publication=True))
    exercise('refill use is excluded', new,
             change_state=lambda s: s['request'].update(job_kind='refill'))
    assert all(hashlib.sha256((W/n).read_bytes()).hexdigest() == h for n,h in runtime_before.items())
    assert hashlib.sha256(stage.RUNNER.read_bytes()).hexdigest() == metadata['base_sha256']
    report = {'passed': True, 'cases': results, 'runtime_hashes_unchanged': runtime_before,
              'installed_runner_unchanged': True, 'patch_installed': False,
              'distributable_patch_applied_in_temporary_checkout': True,
              'scope': 'Actual original/patched _run control flow; writes, regression launch, sampling and services instrumented. Generator regressions run separately.'}
    (W/'evidence/runner-handoff-regression.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'passed': True, 'cases': len(results), 'fresh_review_allowed': sum(r['reaches_fresh_review'] for r in results),
                      'patch_installed': False, 'package_unchanged': True}))


if __name__ == '__main__':
    main()
