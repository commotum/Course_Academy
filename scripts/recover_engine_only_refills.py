#!/usr/bin/env python3
"""Reopen refills blocked only by the removed engine-version approval gate."""
import argparse
from collections import defaultdict
import fcntl
import json
from pathlib import Path
import time

from inventory_jobs import save

ENGINE_REASONS = {'approval_engine_changed', 'engine_changed'}


def reason(job):
    value = job.get('outcome', {}).get('reason')
    return value.get('code') if isinstance(value, dict) else None


def pipeline_directory(path, job):
    return path.with_suffix('.pipeline') / str(job.get('cycle', 1))


def publication_pending(path, job):
    directory = pipeline_directory(path, job)
    if any((directory / 'publication' / name).exists()
           for name in ('request.json', 'verification.json')):
        return True
    state = directory / 'job.json'
    return state.exists() and json.loads(state.read_text()).get('stage') == 'push'


def recover(directory, *, apply=False):
    """Preserve failed cycles; normal refill admission rechecks the actual package."""
    directory = Path(directory).resolve()
    result = {'applied': apply, 'reopened_refills': [], 'withdrawn_reviews': [],
              'locked_kps': [], 'preserved_publications': []}
    with (directory / 'jobs.lock').open('a') as queue_lock:
        fcntl.flock(queue_lock, fcntl.LOCK_EX)
        records = [(path, json.loads(path.read_text())) for path in directory.glob('*.json')
                   if path.name != 'cursor.json']
        records = [(path, job) for path, job in records if isinstance(job.get('request'), dict)]
        grouped = defaultdict(list)
        for path, job in records:
            request = job['request']
            if (request.get('jobKind') == 'refill' and job.get('state') == 'repair-needed'
                    and reason(job) in ENGINE_REASONS):
                grouped[request['knowledgePoint']].append((path, job))
        for kp, refills in grouped.items():
            with (directory / f'kp-{kp}.lock').open('a') as kp_lock:
                try:
                    fcntl.flock(kp_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    result['locked_kps'].append(kp)
                    continue
                reopened_packages = set()
                for path, job in refills:
                    if publication_pending(path, job):
                        result['preserved_publications'].append(str(path))
                        continue
                    old_cycle = job.get('cycle', 1)
                    cycle = old_cycle + 1
                    while (path.with_suffix('.pipeline') / str(cycle)).exists():
                        cycle += 1
                    event = {'time': time.time(), 'reason': 'Engine builds no longer invalidate generator approval.',
                             'previous_cycle': old_cycle, 'previous_outcome': job.get('outcome')}
                    if apply:
                        save(path, {**job, 'state': 'pending', 'cycle': cycle,
                                    'attempts': 0, 'processFailures': 0, 'replenishments': 0,
                                    'retryAt': 0, 'completedAt': 0, 'error': None, 'outcome': {},
                                    'recoveryOnly': False,
                                    'recovery_events': [*job.get('recovery_events', []), event]})
                    result['reopened_refills'].append({'kp': kp, 'path': str(path),
                                                      'previous_cycle': old_cycle, 'cycle': cycle})
                    reopened_packages.add(job['request'].get('script'))
                for path, job in records:
                    request = job['request']
                    package = request.get('script')
                    if (request.get('knowledgePoint') != kp or package not in reopened_packages
                            or request.get('jobKind', 'build') != 'build'
                            or request.get('stage') != 'review-generator' or job.get('state') != 'pending'
                            or job.get('error') or job.get('outcome', {}).get('reason')
                            or pipeline_directory(path, job).exists()):
                        continue
                    # Only unstarted reviews whose same-package failures are
                    # exclusively engine-version checks are redundant. Keep all
                    # authored work, real content failures and unresolved writes.
                    other_failure = any(
                        other['request'].get('knowledgePoint') == kp
                        and other['request'].get('script') == package
                        and other['request'].get('jobKind') == 'refill'
                        and other.get('state') in {'repair-needed', 'rejected', 'blocked'}
                        and (reason(other) not in ENGINE_REASONS or publication_pending(other_path, other))
                        for other_path, other in records)
                    if other_failure:
                        continue
                    if apply:
                        save(path, {**job, 'state': 'withdrawn', 'recoveryOnly': False,
                                    'withdrawal_reason': 'Only obsolete engine-version refill failures requested this unstarted review.'})
                    result['withdrawn_reviews'].append({'kp': kp, 'path': str(path)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--apply', action='store_true', help='Apply recovery; otherwise report proposed changes.')
    args = parser.parse_args()
    print(json.dumps(recover(args.directory, apply=args.apply), indent=2))


if __name__ == '__main__':
    main()
