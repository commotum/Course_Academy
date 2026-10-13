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

from serve_graph_explorer import ROOT, DEFAULT_DATABASE, build_learning, database_environment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', default=os.environ.get('EDB_DATABASE', DEFAULT_DATABASE))
    parser.add_argument('--edb-root', type=Path, default=Path(os.environ.get('EDB_ROOT', ROOT.parent / 'EDB')))
    args = parser.parse_args()
    executable = build_learning(args.edb_root.resolve(), test=True)
    environment = database_environment(args.database)
    environment['EDB_DATABASE'] = args.database
    environment.pop('LEARNING_TEST_KEEP', None)
    subprocess.run([str(executable), '--ignored', 'durable_', '--test-threads=1', '--nocapture'], env=environment, check=True)


if __name__ == '__main__':
    main()
