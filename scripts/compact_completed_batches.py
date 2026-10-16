#!/usr/bin/env python3
"""Remove verified duplicate snapshots and split completed import records in two."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'capture'))
from scripts.database.archive import compact_completed_batch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directories', nargs='+', type=Path)
    args = parser.parse_args()
    for directory in args.directories:
        print(json.dumps(compact_completed_batch(directory), indent=2))


if __name__ == '__main__':
    main()
