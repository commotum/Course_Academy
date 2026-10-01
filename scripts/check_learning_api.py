#!/usr/bin/env python3
"""Check durable lesson delivery using a temporary learner, then remove it.

Requires the configured local EDB database and its Course Academy writer.
The existing learner's profile is read only; all test presentations belong to
an isolated learner. This is the native backend check, independent of a browser.
"""
import argparse
import os
from pathlib import Path
import subprocess

from serve_graph_explorer import ROOT, build_learning


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', default=os.environ.get('EDB_DATABASE', 'course-academy-v2'))
    parser.add_argument('--edb-root', type=Path, default=Path(os.environ.get('EDB_ROOT', ROOT.parent / 'EDB')))
    args = parser.parse_args()
    executable = build_learning(args.edb_root.resolve(), test=True)
    environment = os.environ.copy()
    environment['EDB_DATABASE'] = args.database
    environment.setdefault('EDB_POSTGRES_URL', f"host={ROOT / '.local/edb/run'} dbname=course_academy user=edb_peer sslmode=disable")
    environment.pop('LEARNING_TEST_KEEP', None)
    subprocess.run([str(executable), '--ignored', '--nocapture'], env=environment, check=True)


if __name__ == '__main__':
    main()
