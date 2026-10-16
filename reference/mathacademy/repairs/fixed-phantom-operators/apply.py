"""Apply source-checked fixed-phantom repairs through the existing import pipeline."""
import copy
import hashlib
import json
import pathlib
import sys
import threading
import time

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.config import Config
from scripts.database.pipeline import DatabasePipeline
from scripts.storage import atomic_json, file_lock
from scripts.outbox import target_id

directory = pathlib.Path(__file__).resolve().parent
rows = json.loads((directory / 'plan.json').read_text())
if not rows or not all(row['supported'] for row in rows):
    raise ValueError('Every planned source repair must have complete extraction')
groups = {}
for row in rows:
    groups.setdefault((row['account'], row['task_id']), []).append(row)

with file_lock(Config().database_lock):
    # Recover unresolved exact writes before applying any new source intent.
    for path in Config().spool_root.glob('*.json'):
        item = json.loads(path.read_text())
        capture = pathlib.Path(item['capture_directory'])
        if item['status'] not in ('verified', 'no_changes') and (capture / 'database/request.json').exists():
            result = DatabasePipeline(Config(account=item['account']), threading.Event()).process(capture)
            if result['status'] not in ('verified', 'no_changes'):
                raise ValueError('Unresolved prior write: ' + str(result))
            item.update(status=result['status'], result=result, last_attempt_at=time.time())
            item.pop('error', None)
            atomic_json(path, item)
            atomic_json(capture / 'import-status.json', item)
    for (account, task), repairs in groups.items():
        config = Config(account=account)
        capture = config.output_root / task
        path = capture / 'content.json'
        content = json.loads(path.read_text())
        for row in repairs:
            before, after = row['before'], row['after']
            for source in row['sources']:
                if hashlib.sha256(pathlib.Path(source['file']).read_bytes()).hexdigest() != source['sha256']:
                    raise ValueError('Archived source changed')
            if any(before.get(key) != after.get(key) for key in ('problem', 'worked_solution', 'answer_fields')):
                raise ValueError('Repair must retain source text and answers exactly')
            current = next(q for q in content[row['bucket']] if q['math_academy_id'] == row['question_id'])
            if current not in (before, after):
                raise ValueError('Captured content changed after staging')
            content[row['bucket']][content[row['bucket']].index(current)] = copy.deepcopy(after)
        archive = directory / account / task
        if not (archive / 'original-content.json').exists():
            atomic_json(archive / 'original-content.json', json.loads(path.read_text()))
        atomic_json(path, content)
        # Reopen only the affected completed import; preserve ordering and
        # receipts. A restart can recover the saved exact pipeline request.
        item_path = next(p for p in config.spool_root.glob('*.json')
            if (item := json.loads(p.read_text())).get('capture_directory') == str(capture)
            and item.get('target_id') == target_id(config))
        item = json.loads(item_path.read_text())
        item.update(status='pending', next_attempt_at=0)
        item.pop('error', None)
        item.pop('result', None)
        atomic_json(item_path, item)
        result = DatabasePipeline(config, threading.Event()).process(capture)
        atomic_json(archive / 'result.json', result)
        item.update(status=result['status'] if result['status'] in ('verified','no_changes') else 'pending',
                    result=result, last_attempt_at=time.time(), attempts=item.get('attempts',0)+1)
        atomic_json(item_path, item)
        atomic_json(capture / 'import-status.json', item)
        print(account, task, result['status'], 'omissions', len(result.get('omissions', [])),
              'reason', result.get('reason'), flush=True)
        if result['status'] not in ('verified','no_changes'):
            raise ValueError('Repair import remains pending: ' + str(result))
