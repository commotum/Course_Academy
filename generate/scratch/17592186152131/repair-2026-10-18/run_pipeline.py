#!/usr/bin/env python3
"""Resume the staged repair through the standard independent review/publisher."""
import argparse
import fcntl
import json
from pathlib import Path
import sys

REPAIR = Path(__file__).resolve().parent
REPO = REPAIR.parents[3]
sys.path.insert(0, str(REPO / 'scripts'))
from generator_pipeline import Pipeline
from generator_publish import Publisher, file_lock
from serve_graph_explorer import DEFAULT_LEARNER


class RepairPublisher(Publisher):
    def prepare(self, *args, **kwargs):
        # Coordinate the source/inventory reads with the same application lock
        # the standard publisher already uses for preview and commit. Keep the
        # standard basis guards and exact-request recovery unchanged.
        with file_lock(self.config.request_directory / 'api.lock'):
            return super().prepare(*args, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review-and-publish', action='store_true', required=True,
                        help='Launch the independent reviewer, then publish only if accepted.')
    parser.parse_args()
    directory = REPAIR / 'pipeline'
    state = json.loads((directory / 'job.json').read_text())
    publisher = RepairPublisher.from_environment(repo_root=REPO)
    source = json.loads((directory / 'source/source.json').read_text())
    shared = REPO / '.local/learning/inventory/math' / DEFAULT_LEARNER
    shared.mkdir(parents=True, exist_ok=True)
    with (shared / 'kp-17592186152131.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        pipeline = Pipeline(directory, state['request'], publisher, root=REPO,
                            environment=publisher.client.environment, max_attempts=state['attempt'])
        result = pipeline.run('push')
    print(json.dumps({key:result.get(key) for key in
                      ('stage','package_hash','registration','review','approval_recorded','error')},indent=2))
    return 0 if result['stage'] == 'verified' else 1


if __name__ == '__main__':
    raise SystemExit(main())
