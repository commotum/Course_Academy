"""Strict current-runner regression; an uninstalled proposal cannot pass it.

Runs actual installed sample-stage control flow against current on-disk inputs.
All mutation, sampling, process-launch and service boundaries are instrumented.
Actual generator regressions run separately. No runner/package files are edited.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(REPO/'scripts'))


class Rejected(Exception):
    pass


def main():
    path = REPO/'scripts/generator_pipeline.py'
    spec = importlib.util.spec_from_file_location('installed_pipeline_check', path)
    installed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installed)
    runner = object.__new__(installed.Pipeline)
    runner.state = copy.deepcopy(installed.read(W.parent/'job.json'))
    # This is the checkpoint immediately following authoring; no state is saved.
    runner.state['stage'] = 'sample'
    runner.directory, runner.root = W.parent, REPO
    manifest = installed.read(W/'package.json')
    runtime_before = {name: hashlib.sha256((W/name).read_bytes()).hexdigest()
                      for name in ['package.json', *manifest['files']]}
    package_hash = installed.package_digest(
        W, manifest['entrypoint'], manifest['files'],
        dependencies=manifest['dependencies'])
    engine_hash = runner.engine_identity()
    runner.candidate_hash = lambda: package_hash
    runner.engine_identity = lambda: engine_hash
    calls = []

    def persist(**updates):
        runner.state.update(updates)

    def repair(reason):
        calls.append('repair')
        raise Rejected(str(reason))

    def forbidden(*args, **kwargs):
        raise AssertionError('Service or publication boundary reached')

    runner.persist, runner.repair = persist, repair
    runner.check_repair_regressions = lambda: calls.append('retained_regressions')
    runner.sample = lambda: calls.append('sample')
    runner.session = forbidden
    runner.verify_approval_inputs = forbidden
    runner.review_candidate = forbidden
    runner.admit_publication = forbidden
    rejection = None
    try:
        state = runner._run('generate')
        passed = (state['stage'] == 'validate'
                  and calls == ['retained_regressions', 'sample'])
    except Rejected as error:
        rejection = str(error)
        passed = False
    assert all(hashlib.sha256((W/n).read_bytes()).hexdigest() == h
               for n, h in runtime_before.items()), 'Runtime package changed'
    report = {
        'finding_id': '9b8cb52352b8ca3e790e', 'passed': passed,
        'installed_runner_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'package_hash': package_hash, 'engine_hash': engine_hash,
        'calls': calls, 'rejection': rejection,
        'next_stage': runner.state['stage'],
        'runtime_hashes_unchanged': runtime_before,
        'patch_installed_by_check': False,
        'scope': 'Actual installed _run; mutations and execution boundaries instrumented. '
                 'Generator, delivery and native-grader tests run separately.',
    }
    (W/'evidence/current-handoff-regression.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps({'passed': passed, 'calls': calls, 'rejection': rejection}))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
