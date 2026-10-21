"""Reproduce saved engine blockers without database writes or generator jobs."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ENGINE = ROOT / 'generate/runs/current/check-engine'
SOURCES = {
    17592186096617: ['workspace/evidence/author-2/log-required-input.json'],
    17592186096618: ['workspace/evidence/repair/required-grader-input.json'],
    17592186092261: ['workspace/evidence/repair/post-delivery-grading-limit-input.json'],
    17592186096842: ['workspace/evidence/grader-domain-input.json',
        'workspace/evidence/repair-2/grading-blocker-input.json',
        'workspace/evidence/repair-2/zero-blocker-input.json'],
}


def main():
    candidates = json.loads((HERE / 'sources.json').read_text())
    results = []
    for kp, suffixes in SOURCES.items():
        candidate = next(r for r in candidates if int(r['kp']) == kp)
        sources = [ROOT / candidate['pipeline'] / suffix for suffix in suffixes]
        records = [item for source in sources for item in json.loads(source.read_text())]
        if kp == 17592186096842:
            records[0]['checks'].append({'submitted': '0', 'expected': 'rejected',
                'purpose': 'nonzero derivative must reject zero'})
        checks = []
        for record in records:
            for check in record['checks']:
                item = copy.deepcopy(record)
                check = copy.deepcopy(check)
                if check['expected'] == 'unresolved':
                    check['expected'] = 'accepted'
                item['checks'] = [check]
                prefix = f'{kp}-{len(checks):02}'
                input_file = HERE / f'{prefix}-input.json'
                report_file = HERE / f'{prefix}-report.json'
                input_file.write_text(json.dumps([item], indent=2) + '\n')
                run = subprocess.run([str(ENGINE), str(input_file), str(report_file)],
                    text=True, capture_output=True, timeout=30, cwd=ROOT)
                checks.append({'label': record['label'], 'check': check,
                    'passed': run.returncode == 0, 'exit_code': run.returncode,
                    'diagnostic': run.stderr.strip(),
                    'report': json.loads(report_file.read_text()) if run.returncode == 0 else None})
        results.append({'kp': kp, 'topic': candidate['topic'], 'sources': [str(s.relative_to(ROOT)) for s in sources],
            'title': records[0]['record']['knowledge_point']['title'], 'checks': checks,
            'current_engine_blocked': any(not c['passed'] for c in checks)})
    report = {'engine_sha256': hashlib.sha256(ENGINE.read_bytes()).hexdigest(),
        'database_writes': 0, 'generator_jobs_launched': 0, 'results': results}
    (HERE / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    for r in results:
        print(r['kp'], r['title'], 'BLOCKED' if r['current_engine_blocked'] else 'PASS')
        for c in r['checks']:
            if not c['passed']:
                print(' ', c['check']['submitted'], c['diagnostic'])


if __name__ == '__main__':
    main()
