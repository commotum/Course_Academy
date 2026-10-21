"""Exercise every checkbox-capable registered CLI without database writes."""
import concurrent.futures
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MODE = sys.argv[1] if len(sys.argv) > 1 else 'baseline'

def enum(value):
    return str(value.get(':db/ident') if isinstance(value, dict) else value)

def selected(question):
    checks = []
    for field in question.get(':question/answer-fields', []):
        if enum(field[':answer-field/type']) != ':answer-field.type/checkbox': continue
        ref = field.get(':answer-field/correct')
        if isinstance(ref, dict): value = ref.get(':answer/value')
        else:
            aid = ref[1] if isinstance(ref, list) else ref
            value = next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == aid)
        assert value in ('true', 'false'), field
        checks.append(value == 'true')
    return checks

def run(record):
    output = HERE / (MODE + '-samples') / str(record['kp'])
    output.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(output / 'assets'))
    reports = []
    for level in ('easy', 'moderate', 'hard'):
        if MODE != 'baseline':
            baseline = json.loads((HERE / 'baseline-audit.json').read_text())
            prior = next(r for r in baseline if r['kp'] == record['kp'])
            state = next(r for r in prior['levels'] if r['level'] == level)
            if 'error' in state and record['kp'] not in (17592186147456,17592186179742):
                reports.append({'level': level, 'unsupported': True})
                continue
        command = [str(ROOT / '.venv/bin/python'), '-B', record['runtime_script'],
                   '--difficulty', level, '--seed', '17', '--count', '24' if MODE != 'baseline' else '8', '--format', 'json']
        try:
            result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
                                    text=True, timeout=75)
            (output / (level + '.stdout')).write_text(result.stdout)
            (output / (level + '.stderr')).write_text(result.stderr)
            if result.returncode:
                reports.append({'level': level, 'error': result.stderr[-1800:], 'returncode': result.returncode})
                continue
            records = json.loads(result.stdout)
            if isinstance(records, dict): records = records.get('records', [records])
            choices, empty = Counter(), []
            for index, value in enumerate(records):
                question = value.get('question', value)
                checks = selected(question)
                if checks:
                    choices[sum(checks)] += 1
                    if not any(checks): empty.append(index)
            reports.append({'level': level, 'records': len(records), 'checkbox_counts': dict(choices), 'empty_indices': empty})
        except Exception as error:
            reports.append({'level': level, 'error': type(error).__name__ + ': ' + str(error)})
    report = {'kp': record['kp'], 'packaged': record['packaged'], 'levels': reports}
    (output / 'audit.json').write_text(json.dumps(report, indent=2) + '\n')
    return report

if __name__ == '__main__':
    candidates = json.loads((HERE / ('checkbox-generators.json' if MODE == 'baseline' else 'patched-generators.json')).read_text())
    if MODE != 'baseline':
        for candidate in candidates: candidate['runtime_script'] = candidate['updated_script']
    reports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run, candidate) for candidate in candidates]
        for future in concurrent.futures.as_completed(futures):
            report = future.result()
            reports.append(report)
            (HERE / (MODE + '-audit.json')).write_text(json.dumps(sorted(reports, key=lambda r:r['kp']), indent=2) + '\n')
            print(json.dumps({'completed': len(reports), 'kp': report['kp'],
                              'empty': sum(len(level.get('empty_indices', [])) for level in report['levels']),
                              'errors': sum('error' in level for level in report['levels'])}), flush=True)
