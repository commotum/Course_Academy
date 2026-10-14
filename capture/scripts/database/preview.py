"""Build native capture helpers against explicit deployed EDB dependencies."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

from ..runtime import check_stop
from ..storage import atomic_json

ROOT = Path(__file__).resolve().parents[3]
SOURCE_FILES = ('capture/scripts/database/preview.rs', 'capture/scripts/database/preview.py',
                'engine/edb/answer_fields.rs', 'engine/edb/configuration.rs', 'engine/edb/progress.rs')
BUILD_FLAGS = ['--edition=2024', '-O']


def _library(config):
    explicit = os.environ.get('EDB_CORE_RLIB')
    if explicit:
        library = Path(explicit).expanduser().resolve()
    else:
        manifests = sorted((Path(config.math_root) / 'bin/source').glob('*/build.json'))
        if len(manifests) != 1:
            raise ValueError('Native preview needs one deployed writer build.json or explicit EDB_CORE_RLIB')
        build = json.loads(manifests[0].read_text())
        if Path(build.get('executable', '')).resolve() != (Path(config.math_root) / 'bin/course-academy-transactor').resolve():
            raise ValueError('Writer build manifest does not identify the configured math writer; set EDB_CORE_RLIB')
        library = Path(build['edb_library']).resolve()
    if not library.is_file() or not library.name.startswith('libedb_core') or library.suffix != '.rlib':
        raise ValueError('Native preview EDB_CORE_RLIB must identify an existing edb_core release library')
    return library


def _digest(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _compile(command, stop_event):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    deadline = time.monotonic() + 120
    try:
        while True:
            check_stop(stop_event)
            if time.monotonic() >= deadline:
                raise subprocess.TimeoutExpired(command, 120)
            try:
                stdout, stderr = process.communicate(timeout=0.25)
                break
            except subprocess.TimeoutExpired:
                pass
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode, command, stdout, stderr)
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def native_executable(config, stop_event, source_files, prefix):
    """Build against the deployed writer library and cache by input hashes."""
    check_stop(stop_event)
    library = _library(config)
    sources = {name: _digest(ROOT / name) for name in source_files}
    build = {'sources': sources, 'edb_library': str(library), 'edb_sha256': _digest(library),
             'flags': BUILD_FLAGS, 'compiler': os.environ.get('RUSTC', 'rustc')}
    fingerprint = hashlib.sha256(json.dumps(build, sort_keys=True).encode()).hexdigest()
    output = Path(config.repo_root) / '.local/edb/capture-runtime' / (prefix + '-' + fingerprint)
    if output.is_file():
        return output
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.' + prefix + '-', dir=output.parent)
    os.close(descriptor)
    try:
        command = [build['compiler'], *BUILD_FLAGS, str(ROOT / source_files[0]),
                   '--extern', 'edb_core=' + str(library), '-L', 'dependency=' + str(library.parent),
                   '-o', temporary]
        _compile(command, stop_event)
        check_stop(stop_event)
        # Do not label a build with pre-build hashes if source/library bytes changed.
        if any(_digest(ROOT / name) != digest for name, digest in sources.items()) or _digest(library) != build['edb_sha256']:
            raise RuntimeError('Native preview inputs changed during compilation; retry the build')
        os.replace(temporary, output)
        atomic_json(output.with_suffix('.json'), build)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return output


def preview_executable(config, stop_event):
    """Return an explicit override or a noncommitting native preview build."""
    check_stop(stop_event)
    if getattr(config, 'preview_bin', None) is not None:
        return Path(config.preview_bin)
    return native_executable(config, stop_event, SOURCE_FILES, 'native-preview')


def submission_executable(config, stop_event):
    return native_executable(config, stop_event,
        ('capture/scripts/database/submission.rs', 'capture/scripts/database/preview.py'), 'native-submit')


if __name__ == '__main__':
    import threading
    from ..config import Config
    print(preview_executable(Config(), threading.Event()))
