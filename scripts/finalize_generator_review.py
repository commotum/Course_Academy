#!/usr/bin/env python3
"""Regenerate the exact final candidate for the active verifier to inspect."""
import argparse
import json
from pathlib import Path

from generator_pipeline import Pipeline, read


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job', type=Path, required=True)
    parser.add_argument('--evidence-root', type=Path, required=True)
    args = parser.parse_args(argv)
    # The parent holds the worker lock and waits on this verifier. No database
    # reads or writes are needed: all source/inventory evidence is already saved.
    state = read(args.job / 'job.json')
    pipeline = Pipeline(args.job, state['request'], None)
    if state['stage'] != 'validate':
        raise ValueError('Finalization belongs to the active verification phase')
    print(json.dumps(pipeline.finalize_review(args.evidence_root), sort_keys=True))


if __name__ == '__main__':
    main()
