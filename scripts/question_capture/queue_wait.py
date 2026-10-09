"""Persist queue exhaustion separately from capture process liveness."""
import json
import os
import time

from core import atomic_json
from solver import process_token


def waiting_tasks(output, queue):
    tasks = []
    for item in queue:
        try:
            state = json.loads((output/str(item['task_id'])/'state.json').read_text())
        except (OSError, ValueError):
            state = {}
        error = state.get('deferred_error', {})
        tasks.append({'task_id': item['task_id'], 'task_type': item.get('task_type'),
                      'title': item.get('title'), 'deferred': bool(error),
                      'reason': error.get('message') or 'No eligible capture or saved recovery'})
    return tasks


def clear_queue_wait(state_dir):
    (state_dir/'selection/queue-wait.json').unlink(missing_ok=True)


def record_queue_wait(args, queue):
    # Called only after both repair and saved-resume selection find no work.
    record = {'worker_pid': os.getpid(), 'process_token': process_token(os.getpid()),
              'observed_at': time.time(), 'tasks': waiting_tasks(args.output, queue)}
    atomic_json(args.state_dir/'selection/queue-wait.json', record)
    return record
