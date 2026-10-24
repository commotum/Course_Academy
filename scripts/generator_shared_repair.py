#!/usr/bin/env python3
"""Apply and test an agent's shared-code patch without racing another KP worker."""
import argparse
import fcntl
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def apply_repair(patch, checks, *, root=ROOT):
    root = Path(root)
    patch = Path(patch).resolve()
    if not checks or any(not isinstance(c, list) or not c or any(not isinstance(a, str) for a in c) for c in checks):
        raise ValueError('Supply at least one real regression command as a JSON argv array')
    local = root / '.local'
    local.mkdir(exist_ok=True)
    with (local / 'generator-shared-repair.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        subprocess.run(['git', 'apply', '--check', str(patch)], cwd=root, check=True)
        subprocess.run(['git', 'apply', str(patch)], cwd=root, check=True)
        try:
            for command in checks:
                subprocess.run(command, cwd=root, check=True)
        except BaseException:
            # Reverse only this patch, never reset or discard another worker's
            # changes. Conflicts leave a concrete failure for this same agent.
            subprocess.run(['git', 'apply', '--reverse', str(patch)], cwd=root, check=True)
            raise
    return {'passed': True, 'patch': str(patch), 'checks': checks}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--patch', type=Path, required=True)
    parser.add_argument('--check-json', action='append', required=True,
                        help='Regression command as a JSON argv array; repeat for multiple commands')
    args = parser.parse_args(argv)
    print(json.dumps(apply_repair(args.patch, [json.loads(c) for c in args.check_json])))


if __name__ == '__main__':
    main()
