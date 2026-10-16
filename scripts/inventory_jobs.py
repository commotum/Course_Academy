"""Durable, deduplicated handoff from scheduler inventory to generator workers.

The creator runs the documented generation pipeline. A job completes only when
a subsequent captured inventory confirms replenishment, not when a process exits.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class InventoryJobs:
    def __init__(self, root: Path, directory: Path, learner: str, environment: dict | None = None):
        self.root, self.directory, self.learner = root, directory, learner
        self.environment = dict(os.environ if environment is None else environment)
        directory.mkdir(parents=True, exist_ok=True)

    def creator_executable(self) -> str:
        return (self.environment.get('COURSE_ACADEMY_CODEX_EXECUTABLE')
                or shutil.which('codex', path=self.environment.get('PATH', os.defpath))
                or str(Path.home() / '.local/bin/codex'))

    def accept(self, inventory: dict) -> None:
        """Cursor advances only after durable jobs are accepted at this basis."""
        with (self.directory / 'jobs.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            cursor_path = self.directory / 'cursor.json'
            cursor = json.loads(cursor_path.read_text()) if cursor_path.exists() else {}
            lineage = inventory['lineage']
            if cursor.get('lineage', lineage) != lineage:
                raise ValueError('Inventory database lineage changed; reconcile existing jobs before retargeting')
            if inventory['basis'] < cursor.get('basis', 0):
                raise ValueError('Inventory basis regressed')
            current = set()
            for request in inventory['jobs']:
                key = hashlib.sha256(json.dumps([self.learner, request['knowledgePoint'], request['difficulty']]).encode()).hexdigest()
                current.add(key)
                path = self.directory / f'{key}.json'
                old = json.loads(path.read_text()) if path.exists() else {}
                # Restore an interrupted worker; unchanged rejected requests wait
                # for new evidence instead of repeating impossible generation.
                changed = any(old.get('request', {}).get(k) != request.get(k) for k in ('stage', 'missing', 'script'))
                state = old.get('state', 'pending')
                cycle = old.get('cycle', 1)
                # The service manager may lack the interactive shell's PATH.
                # Installing/finding the executable is new operational evidence,
                # not a reason to retain a content-capability rejection.
                if state == 'rejected' and old.get('error') == "[Errno 2] No such file or directory: 'codex'" and Path(self.creator_executable()).is_file():
                    state = 'pending'
                    old = {**old, 'attempts': 0, 'retryAt': 0, 'error': None}
                if state == 'awaiting-verification' and old.get('retryAt', 0) <= time.time():
                    state = 'pending' if old.get('replenishments', 0) < 3 else 'rejected'
                    if state == 'pending':
                        cycle += 1
                if state in {'verified', 'withdrawn'} or state == 'rejected' and changed:
                    state = 'pending'
                    cycle += 1
                    old = {**old, 'attempts': 0, 'replenishments': 0, 'retryAt': 0}
                if state != old.get('state') or {k:v for k,v in request.items() if k != 'basis'} != {k:v for k,v in old.get('request', {}).items() if k != 'basis'}:
                    save(path, {**old, 'key': key, 'learner': self.learner, 'lineage': lineage, 'request': request, 'state': state, 'cycle': cycle})
            for path in self.directory.glob('*.json'):
                if path.stem in current or path.name == 'cursor.json':
                    continue
                old = json.loads(path.read_text())
                if 'request' in old:
                    state = 'verified' if old['request']['topic'] in inventory['qualifyingTopics'] else 'withdrawn'
                    if old.get('state') != state:
                        save(path, {**old, 'state': state, 'verifiedBasis': inventory['basis']})
            save(self.directory / 'cursor.json', {'basis': inventory['basis'], 'lineage': lineage, 'assessmentStatus': inventory.get('assessmentStatus')})

    def finish(self, path: Path, updates: dict, *, cycle=None) -> None:
        with (self.directory / 'jobs.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            current = json.loads(path.read_text())
            if current['state'] not in {'verified', 'withdrawn'} and (cycle is None or current.get('cycle', 1) == cycle):
                save(path, {**current, **updates})

    def run_one(self) -> bool:
        """One worker; bounded content repairs and resumable transport failures."""
        with (self.directory / 'worker.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            jobs = []
            for path in self.directory.glob('*.json'):
                job = json.loads(path.read_text())
                if job.get('state') in {'pending', 'running'} and job.get('retryAt', 0) <= time.time():
                    jobs.append((path, job))
            if not jobs:
                return False
            path, job = min(jobs, key=lambda pair: (pair[1]['state'] != 'running', pair[1]['request']['urgency'], pair[1]['request']['proximity'], -pair[1]['request'].get('priority', 0), pair[1]['key']))
            # An interrupted process has an unknown outcome; recover the same
            # attempt and scratch package rather than spend another failure retry.
            attempts = max(1, job.get('attempts', 0) + (job['state'] != 'running'))
            cycle = job.get('cycle', 1)
            self.finish(path, {'state': 'running', 'attempts': attempts, 'error': None}, cycle=cycle)
            result_path = path.with_suffix('.result')
            if result_path.exists():
                result_path.replace(path.with_suffix(f'.result.previous-{attempts}'))
            from generator_pipeline import python_executable
            command = [python_executable(self.root, self.environment),
                       str(self.root / 'scripts/generator_pipeline.py'),
                       '--inventory-job', str(path), '--inventory-cycle', str(cycle),
                       '--database', self.directory.parent.name]
            override = self.environment.get('COURSE_ACADEMY_GENERATOR_COMMAND')
            if override:
                command = json.loads(override) + [str(path)]
            try:
                with path.with_suffix('.log').open('a') as log:
                    completed = subprocess.run(command, cwd=self.root, stdout=log, stderr=subprocess.STDOUT, timeout=21600, check=False, env=self.environment, pass_fds=(lock.fileno(),))
                outcome = json.loads(result_path.read_text()) if result_path.exists() else {}
                state = 'rejected' if outcome.get('outcome') in {'unsupported', 'finite-limit', 'failed'} else 'awaiting-verification' if completed.returncode == 0 else 'pending'
                self.finish(path, {'state': state, 'attempts': attempts,
                                  'replenishments': job.get('replenishments', 0) + (state == 'awaiting-verification'),
                                  'retryAt': time.time() + min(300, 10 * 2 ** min(attempts, 5)),
                                  'exitCode': completed.returncode, 'outcome': outcome}, cycle=cycle)
            except (OSError, subprocess.SubprocessError, ValueError) as error:
                self.finish(path, {'state': 'pending', 'attempts': attempts, 'retryAt': time.time() + min(300, 10 * 2 ** min(attempts, 5)), 'error': str(error)}, cycle=cycle)
            return True
