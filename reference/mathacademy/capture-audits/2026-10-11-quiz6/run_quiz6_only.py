"""Run the explicitly requested Methods of Proof quiz through normal capture."""
from pathlib import Path
import logging
import os
import threading
import time

from scripts.config import Config
from scripts import runner as runner_module
from scripts.database import DatabasePipeline
from scripts.outbox import DatabaseWorker
from scripts.runtime import StopRequested, shutdown_signals
from scripts.storage import atomic_json, file_lock, read_json
from scripts.terminal import process_token

TASK = '14123325'
AUDIT = Path(__file__).resolve().parent
original_read_queue = runner_module.read_queue


def quiz_only_queue(browser, directory):
    queue = original_read_queue(browser, directory)
    if read_json(directory / 'queue.json', {}).get('unreadable'):
        raise StopRequested('Cannot confirm the requested quiz from unreadable cards')
    if any(q.get('started') and q['task_id'] != TASK for q in queue):
        raise StopRequested('Another started activity needs separate reconciliation')
    selected = [q for q in queue if q['task_id'] == TASK]
    if len(selected) != 1:
        raise StopRequested('Requested quiz is not uniquely available; no other task started')
    q = selected[0]
    if (q['kind'], q['title'], str(q.get('course_id'))) != ('assessment', 'Quiz 6', '76'):
        raise StopRequested('Requested task metadata changed; no other task started')
    if str(q.get('details', {}).get('test_id')) != '596372':
        raise StopRequested('Requested quiz test identity changed')
    atomic_json(AUDIT / 'selected-original-card.json', q)
    return selected


class QuizOnlyRunner(runner_module.CaptureRunner):
    completed_requested = False

    def cycle(self, browser):
        active = read_json(self.active_path) or self._recover_orphan()
        if active and active['activity']['task_id'] != TASK:
            raise StopRequested('Preserve unrelated active selection without opening it')
        made_progress = super().cycle(browser)
        if made_progress:
            directory = self.config.output_root / TASK
            if read_json(self.active_path) is not None or not (directory / 'handoff-complete.json').exists():
                raise RuntimeError('Requested quiz did not finish its normal durable handoff')
            self.completed_requested = True
            self.stop_event.set()
        return made_progress


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    config = Config(account='linear')
    stop = threading.Event()
    record_path = config.state_root / 'worker.json'
    with file_lock(config.state_root / 'supervisor.lock', blocking=False), shutdown_signals(stop):
        old = read_json(record_path, {})
        atomic_json(AUDIT / 'previous-worker.json', old)
        record = {'pid': os.getpid(), 'process_token': process_token(os.getpid()),
                  'started_at': time.time(), 'account': 'linear',
                  'log': str(config.state_root / 'console.log'),
                  'command': ['run_quiz6_only.py'], 'restarts': 0, 'task_id': TASK}
        atomic_json(record_path, record)
        atomic_json(AUDIT / 'authorization.json', {
            'account': 'linear', 'course_id': '76', 'task_id': TASK, 'title': 'Quiz 6',
            'stop_after_requested_activity': True, 'other_accounts_authorized': False,
            'ordinary_capture_and_answer_policies': True})
        runner_module.read_queue = quiz_only_queue
        capture = QuizOnlyRunner(config, stop)
        try:
            capture.run()
            if capture.database_worker.thread:
                capture.database_worker.thread.join(timeout=30)
            if not capture.completed_requested:
                raise RuntimeError('Requested quiz has not completed; retained checkpoint')
            # Complete the ordinary durable database handoff without a browser
            # or a second activity, using a fresh shutdown event after capture.
            importing = threading.Event()
            worker = DatabaseWorker(config, importing, lambda: DatabasePipeline(config, importing))
            with shutdown_signals(importing):
                while worker.pending() and not importing.is_set():
                    result = worker.process_one()
                    atomic_json(AUDIT / 'last-database-worker-result.json', result)
                    if result.get('status') not in ('verified', 'no_changes'):
                        importing.wait(config.retry_delay)
            result = read_json(config.output_root / TASK / 'database/result.json', {})
            if result.get('status') not in ('verified', 'no_changes'):
                raise RuntimeError('Quiz completed; database handoff is still durable pending work')
            atomic_json(AUDIT / 'result.json', {
                'task_id': TASK, 'capture_completed': True, 'runner_stopped': True,
                'active': read_json(config.state_root / 'active.json'),
                'completion': read_json(config.output_root / TASK / 'checkpoint.json', {}).get('completion'),
                'database_result': result})
        finally:
            runner_module.read_queue = original_read_queue
            record.update(finished_at=time.time(), stop_requested=True)
            atomic_json(record_path, record)


if __name__ == '__main__':
    main()
