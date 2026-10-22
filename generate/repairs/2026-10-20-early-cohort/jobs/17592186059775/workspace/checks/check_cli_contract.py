"""Reproduce runner record decoding against an isolated current runtime package."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

W = Path(__file__).resolve().parents[1]


def runner_records(value):
    # generator_pipeline.py sample decoder; deliberately no `instances` alias.
    if isinstance(value, dict):
        value = value.get('records', value.get('questions', [value] if 'question' in value else None))
    return value


def main():
    manifest = json.loads((W/'package.json').read_text())
    cases = []
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        for name in manifest['files']:
            target = dest/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(W/name, target)
        def hashes():
            return {name: hashlib.sha256((dest/name).read_bytes()).hexdigest() for name in manifest['files']}
        before = hashes()
        for band, count, seed in [('easy', 5, 0), ('easy', 0, 17), ('easy', 1, 17), ('moderate', 5, 0)]:
            command = [sys.executable, '-E', '-s', '-B', str(dest/manifest['entrypoint']),
                       '--difficulty', band, '--count', str(count), '--seed', str(seed), '--format', 'json']
            run = subprocess.run(command, cwd=dest, env={**os.environ,
                'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(dest/'assets')}, capture_output=True, text=True)
            assert run.returncode == 0, run.stderr
            output = json.loads(run.stdout)
            records = runner_records(output)
            assert isinstance(records, list) and len(records) == count, (
                'Runner record-count failure', band, count, type(output).__name__,
                list(output) if isinstance(output, dict) else None)
            assert all(isinstance(r.get('question'), dict) for r in records)
            assert all(r['question'][':question/difficulty'] == ':question.difficulty/'+band for r in records)
            assert len({r['question'][':question/id'] for r in records}) == count
            if count == 5:
                repeat = subprocess.run(command, cwd=dest, capture_output=True, text=True, check=True)
                assert repeat.stdout == run.stdout, 'Nondeterministic CLI output'
            cases.append({'difficulty': band, 'count': count, 'seed': seed, 'decoded_count': len(records)})
        command = [sys.executable, '-E', '-s', '-B', str(dest/manifest['entrypoint']),
                   '--difficulty', 'easy', '--count', '1000000', '--seed', '0', '--format', 'json']
        exceeded = subprocess.run(command, cwd=dest, capture_output=True, text=True)
        assert exceeded.returncode != 0 and 'Finite variant limit:' in exceeded.stderr
        assert not exceeded.stdout.strip(), 'Must not silently deliver a truncated batch'
        assert hashes() == before, 'Runtime package files were modified'
    report = {'passed': True, 'runtime_only_relocation': True, 'runner_decoder': 'generator_pipeline.py sample',
              'cases': cases, 'finite_limit_error': exceeded.stderr.strip().splitlines()[-1],
              'package_unchanged': True}
    (W/'evidence/cli-contract.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
