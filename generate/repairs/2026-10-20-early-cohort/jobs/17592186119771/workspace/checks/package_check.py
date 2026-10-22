#!/usr/bin/env python3
"""Verify the declared runtime alone works from a relocated directory."""
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT/'package.json').read_text())
    assert manifest['dependencies']['python'] == sys.version.split()[0]
    for name, version in manifest['dependencies']['packages'].items():
        assert importlib.metadata.version(name) == version
    assert 'package.json' not in manifest['files']
    with tempfile.TemporaryDirectory(dir=ROOT/'evidence') as directory:
        target = Path(directory)
        for relative in manifest['files']:
            path = Path(relative)
            assert not path.is_absolute() and '..' not in path.parts
            (target/path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/path, target/path)
        cmd = [sys.executable, str(target/manifest['entrypoint']), '--difficulty',
               'easy', '--count', '5', '--seed', '0', '--format', 'json']
        result = subprocess.run(cmd, cwd=target, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == json.loads((ROOT/'evidence/samples.json').read_text())
    report = {'manifest_runtime_files': manifest['files'],
              'dependencies': manifest['dependencies'], 'relocation': 'passed',
              'five_record_deterministic_comparison': 'passed'}
    (ROOT/'evidence/relocation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__': main()
