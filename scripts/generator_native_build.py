"""Build the offline native grader from identified sources, never start services."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'generate/runs/current/check-engine.rs'
BINARY = 'generate/runs/current/check-engine'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build_inputs(root=ROOT):
    root = Path(root)
    paths = [root / SOURCE, root / 'Cargo.toml', root / 'Cargo.lock']
    paths.extend(sorted((root / 'engine/rust').rglob('*.rs')))
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def ensure_native_grader(repo_root=ROOT, environment=None):
    """Reuse only a binary whose embedded build identity matches current inputs.

    Call for active work, not while deciding whether a historical approval exists.
    Cargo's locked/offline build resolves dependencies; record the actual linked
    artifacts and compiler in addition to the source/dependency lock identities.
    """
    root = Path(repo_root).resolve()
    binary = root / BINARY
    sidecar = binary.with_suffix('.build.json')
    environment = {**os.environ, **(environment or {})}
    (root / 'target').mkdir(exist_ok=True)
    with (root / 'target/generator-native-build.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        inputs = build_inputs(root)
        identity = digest(inputs)
        if binary.is_file() and sidecar.is_file():
            saved = json.loads(sidecar.read_text())
            if (saved.get('inputs') == inputs and saved.get('inputs_sha256') == identity
                    and saved.get('binary_sha256') == hashlib.sha256(binary.read_bytes()).hexdigest()):
                return saved
        environment['COURSE_ACADEMY_GRADER_INPUTS_SHA256'] = identity
        command = ['cargo', 'build', '--locked', '--offline', '--bin', 'generator-native-check', '--message-format=json']
        process = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True)
        if process.returncode:
            raise ValueError('Native grader build failed: ' + process.stderr[-6000:])
        executable, dependencies = None, {}
        for line in process.stdout.splitlines():
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue
            if message.get('reason') != 'compiler-artifact':
                continue
            if message.get('target', {}).get('name') == 'generator-native-check':
                executable = message.get('executable')
            for name in message.get('filenames', []):
                path = Path(name)
                if path.is_file() and path.suffix in {'.rlib', '.so', '.a'}:
                    dependencies[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        if not executable or not dependencies or build_inputs(root) != inputs:
            raise ValueError('Native grader build lacks dependencies or its sources changed during compilation')
        compiler = subprocess.check_output(['rustc', '-Vv'], cwd=root, env=environment, text=True).strip()
        temporary = binary.with_suffix('.building')
        shutil.copy2(executable, temporary)
        temporary.replace(binary)
        result = {'format': 'course-academy-native-build-v1', 'inputs': inputs, 'inputs_sha256': identity,
                  'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
                  'compiler': compiler, 'dependencies': dependencies, 'command': command}
        sidecar.write_text(json.dumps(result, indent=2) + '\n')
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(ensure_native_grader(args.repo_root), indent=2))
