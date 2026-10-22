"""Reproduce the retained original import failure, then test the current closure."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from validate import relocation

W = Path(__file__).resolve().parents[1]

def main():
    with tempfile.TemporaryDirectory(prefix='retained-import-failure-') as folder:
        package = Path(folder)
        shutil.copyfile(W/'evidence/original-generator.py', package/'17592186184172.py')
        (package/'17592186184172').mkdir()
        shutil.copyfile(W/'17592186184172/source.json', package/'17592186184172/source.json')
        command = [sys.executable, str(package/'17592186184172.py'),
                   '--difficulty', 'moderate', '--count', '5', '--seed', '0']
        result = subprocess.run(command, cwd=package,
                                env={**os.environ, 'PYTHONPATH': ''},
                                capture_output=True, text=True)
        assert result.returncode != 0, 'Original counterexample no longer reproduces'
        assert 'StopIteration' in result.stderr
        assert 'scripts/generator_policy.py' in result.stderr
        report = {'command': command, 'exit_code': result.returncode,
                  'stderr': result.stderr, 'expected_failure_reproduced': True}
    report['current_package'] = relocation()
    (W/'evidence/retained-failure-reproduced.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print('Original import failure reproduced; current relocated package passes both bands.')

if __name__ == '__main__':
    main()
