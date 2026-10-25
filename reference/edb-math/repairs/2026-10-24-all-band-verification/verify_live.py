"""Read-only deployment evidence: actual workers, queue scope, and approvals."""
import collections
import json
from pathlib import Path
import shlex
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
JOBS = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'


def capture():
    workers = []
    for line in subprocess.check_output(['ps', '-eo', 'pid=,args='], text=True).splitlines():
        pid, command = line.strip().split(None, 1)
        try:
            args = shlex.split(command)
        except ValueError:
            continue
        if (not args or not Path(args[0]).name.startswith('python')
                or not any(arg.endswith('/scripts/generator_pipeline.py') for arg in args)
                or '--inventory-job' not in args):
            continue
        path = Path(args[args.index('--inventory-job') + 1])
        outer = json.loads(path.read_text())
        directory = path.with_suffix('.pipeline') / str(outer.get('cycle', 1))
        state = json.loads((directory / 'job.json').read_text())
        events = list(directory.rglob('events.jsonl'))
        latest = max((p.stat().st_mtime for p in events), default=None)
        workers.append({'pid': int(pid), 'kp': state['request']['kp'], 'stage': state['stage'],
                        'verification_policy': state.get('verification_policy_version'),
                        'sampled_bands': sorted(state.get('verification_batches', {})),
                        'sampling_errors': state.get('sampling_errors', {}),
                        'last_agent_event_seconds': round(time.time() - latest, 1) if latest else None,
                        'job': str(directory / 'job.json')})
    reviews, blocked = [], []
    for path in JOBS.glob('*.json'):
        value = json.loads(path.read_text())
        request = value.get('request', {})
        if request.get('stage') == 'review-generator' and value.get('state') in {'pending', 'running'}:
            reviews.append({'kp': request['knowledgePoint'], 'bands': request.get('verification_bands', []),
                            'reuse_pipeline': request.get('reuse_pipeline')})
        if value.get('state') == 'blocked':
            blocked.append({'kp': request.get('knowledgePoint'), 'reason': value.get('outcome', {}).get('reason')})
    approvals = collections.Counter()
    for path in Path('/media/jake/SSD/EDB/math/generators/approvals').glob('*/*.json'):
        value = json.loads(path.read_text())
        approvals[value.get('format')] += 1
    service = subprocess.check_output(['systemctl', '--user', 'show', 'course-academy.service',
                                      '-p', 'ActiveState', '-p', 'MainPID', '-p', 'NRestarts'], text=True)
    with urllib.request.urlopen('http://127.0.0.1:8765/', timeout=10) as response:
        status = response.status
    return {'time': time.time(), 'http_status': status, 'service': service.splitlines(),
            'workers': workers, 'queued_reviews': len(reviews),
            'all_band_queued_reviews': sum(set(row['bands']) == {'easy', 'moderate', 'hard'} for row in reviews),
            'reusing_completed_work': sum(bool(row['reuse_pipeline']) for row in reviews),
            'duplicate_queued_review_kps': [kp for kp, count in collections.Counter(row['kp'] for row in reviews).items() if count > 1],
            'approval_formats': dict(approvals), 'blocked': blocked}


if __name__ == '__main__':
    result = capture()
    Path(__file__).with_name('live-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
