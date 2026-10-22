"""Exercise the runner's JSON decoder against current, relocated CLI output."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def decode(output):
    # generator_pipeline.py sample(): supported public output envelopes.
    records = json.loads(output)
    if isinstance(records, dict):
        records = records.get('records', records.get(
            'questions', [records] if 'question' in records else None))
    return records


def main():
    manifest = json.loads((ROOT / 'package.json').read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix='rank-cli-contract-') as tmp:
        runtime = Path(tmp)
        for name in manifest['files']:
            target = runtime / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        for difficulty, count in [('easy', 5), ('moderate', 5), ('easy', 0)]:
            command = [sys.executable, '-E', '-s', '-B',
                       str(runtime / manifest['entrypoint']), '--difficulty',
                       difficulty, '--count', str(count), '--seed', '0',
                       '--format', 'json']
            runs = [subprocess.run(command, cwd=runtime, capture_output=True,
                                   text=True) for _ in range(2)]
            assert all(p.returncode == 0 for p in runs), runs[0].stderr
            assert runs[0].stdout == runs[1].stdout, 'Nondeterministic CLI'
            records = decode(runs[0].stdout)
            assert isinstance(records, list) and len(records) == count, (
                f'Runner cannot decode {difficulty}/count={count}: '
                f'{type(records).__name__}; top-level '
                f'{list(json.loads(runs[0].stdout))[:3]}')
            for record in records:
                assert isinstance(record.get('question'), dict)
                assert record['question'][':question/difficulty'] == (
                    ':question.difficulty/' + difficulty)
            results.append({'difficulty': difficulty, 'requested': count,
                            'runner_decoded': len(records),
                            'deterministic': True, 'relocated': True})
    (ROOT / 'evidence/cli-contract.json').write_text(json.dumps(
        {'status': 'pass', 'cases': results}, indent=2) + '\n')
    print(json.dumps({'status': 'pass', 'cases': len(results)}))


if __name__ == '__main__':
    main()
