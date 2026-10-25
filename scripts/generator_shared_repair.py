#!/usr/bin/env python3
"""Apply and test an agent's shared-code patch without racing another KP worker."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def apply_repair(patch, checks, *, root=ROOT, artifacts=()):
    root = Path(root).resolve()
    patch = Path(patch).resolve() if patch is not None else None
    if not checks or any(not isinstance(c, list) or not c or any(not isinstance(a, str) for a in c) for c in checks):
        raise ValueError('Supply at least one real regression command as a JSON argv array')
    local = root / '.local'
    local.mkdir(exist_ok=True)
    outputs = []
    for name in dict.fromkeys(('generate/runs/current/check-engine', *artifacts)):
        path = root / name
        if not path.resolve().is_relative_to(root) or path.is_symlink():
            raise ValueError('Build artifacts must be regular files within the repository')
        if path.exists() and not path.is_file():
            raise ValueError('Build artifacts must be files, not directories')
        outputs.append(path)
    with (local / 'generator-shared-repair.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if patch is not None:
            subprocess.run(['git', 'apply', '--check', str(patch)], cwd=root, check=True)
        with tempfile.TemporaryDirectory(prefix='shared-repair-', dir=local) as snapshot:
            saved = []
            for index, path in enumerate(outputs):
                backup = Path(snapshot) / str(index) if path.exists() else None
                if backup is not None:
                    shutil.copy2(path, backup)
                saved.append((path, backup))
            if patch is not None:
                subprocess.run(['git', 'apply', str(patch)], cwd=root, check=True)
            try:
                for command in checks:
                    subprocess.run(command, cwd=root, check=True)
            except BaseException:
                try:
                    # Reverse only this patch, never reset another worker's
                    # changes. The agent owns any conflict and its recovery.
                    if patch is not None:
                        subprocess.run(['git', 'apply', '--reverse', str(patch)], cwd=root, check=True)
                finally:
                    # A failed regression may have rebuilt the live grader.
                    # Restore its exact bytes and mode along with the source.
                    for path, backup in saved:
                        if backup is None:
                            path.unlink(missing_ok=True)
                            continue
                        else:
                            path.parent.mkdir(parents=True, exist_ok=True)
                            # Workspace artifacts may live on another filesystem.
                        # Stage on the destination filesystem, preserving mode,
                        # then atomically replace there instead of moving the
                        # snapshot across mount boundaries.
                        fd, restore_name = tempfile.mkstemp(prefix='.generator-restore-', dir=path.parent)
                        os.close(fd)
                        restore = Path(restore_name)
                        try:
                            shutil.copy2(backup, restore)
                            os.replace(restore, path)
                        finally:
                            restore.unlink(missing_ok=True)
                raise
    return {'passed': True, 'patch': str(patch) if patch is not None else None, 'checks': checks,
            'artifacts': [str(path.relative_to(root)) for path in outputs]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--patch', type=Path, help='Source patch; omit for a serialized artifact-only rebuild')
    parser.add_argument('--check-json', action='append', required=True,
                        help='Regression command as a JSON argv array; repeat for multiple commands')
    parser.add_argument('--artifact', action='append', default=[],
                        help='Additional repository build output to restore on failure; repeat as needed')
    args = parser.parse_args(argv)
    print(json.dumps(apply_repair(args.patch, [json.loads(c) for c in args.check_json],
                                  artifacts=args.artifact)))


if __name__ == '__main__':
    main()
