"""Run exactly the declared runtime closure after relocation, with pinned versions."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / 'package.json').read_text())
    assert platform.python_version() == manifest['dependencies']['python']
    for name, version in manifest['dependencies']['packages'].items():
        assert importlib.metadata.version(name) == version
    with tempfile.TemporaryDirectory(prefix='relocated-generator-') as temp:
        target = Path(temp)
        for filename in manifest['files']:
            assert not Path(filename).is_absolute() and '..' not in Path(filename).parts
            dest = target / filename
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / filename, dest)
        assets = target / 'generated-assets'
        env = dict(os.environ, COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(assets))
        command = [sys.executable, str(target / manifest['entrypoint']), '--difficulty', 'moderate',
                   '--count', '5', '--seed', '0', '--format', 'json']
        process = subprocess.run(command, cwd='/tmp', env=env, check=True, capture_output=True, text=True)
        records = json.loads(process.stdout)
        assert isinstance(records, list), 'Runner requires a top-level JSON array'
        assert records == json.loads((ROOT / 'evidence/sample.json').read_text())
        assert len(records) == 5 and not assets.exists()  # This family generates no assets.
    result = {'relocation': 'pass', 'records': 5, 'dependency_versions_checked': manifest['dependencies'],
              'runtime_files': {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in manifest['files']},
              'entrypoint_arguments': ['--difficulty moderate', '--count 5', '--seed 0', '--format json'],
              'cwd': '/tmp', 'external_imports': ['sympy'], 'generated_assets': 0}
    (ROOT / 'evidence/runtime.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'relocation': 'pass', 'records': 5, 'runtime_file_count': len(manifest['files'])}))

if __name__ == '__main__':
    main()
