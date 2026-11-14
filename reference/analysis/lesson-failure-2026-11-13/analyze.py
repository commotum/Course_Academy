"""Read-only audit of lesson failure thresholds in saved MA captures.

Run from any directory with Python and beautifulsoup4 installed. Writes only
the adjacent evidence.json. Does not infer pass/fail from XP or 'Completed'.
"""
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from itertools import groupby
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'reference/mathacademy'
OUT = Path(__file__).with_name('evidence.json')
LABELS = {'Correct': 'C', 'Full Credit': 'C', 'Incorrect': 'W', 'No Credit': 'W', 'Partial Credit': 'P'}


def read(p):
    return json.loads(p.read_bytes())


def rel(p):
    return str(p.relative_to(ROOT))


def completion_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get('text') or value.get('source_text') or ''
    return ''


def classify(text):
    if 'halted due to poor performance' in text or "You didn't pass the lesson" in text:
        return 'failed'
    if "Congratulations! You've completed the lesson" in text:
        return 'passed'
    return None


def qid(value):
    return re.sub(r'^(?:step-q|question-|q-)', '', str(value))


def groups(rows):
    return [dict(kp=kp, sequence=''.join(LABELS.get(q['result'], '?') for q in qs),
                 questions=qs)
            for kp, it in groupby(rows, lambda q: q['kp']) for qs in [list(it)]]


def modern(p):
    activity = read(p / 'activity.json') if (p / 'activity.json').exists() else {}
    if activity.get('kind') and activity['kind'] != 'lesson':
        return None
    hp = p / 'history-content.json'
    cp = p / 'content.json'
    source = hp if hp.exists() else cp
    data = read(source) if source.exists() else {}
    post = read(p / 'post-activity.json') if (p / 'post-activity.json').exists() else {}
    kind = activity.get('kind') or data.get('task_type') or (post.get('completion') or {}).get('kind')
    if kind != 'lesson':
        return None
    row = dict(task_id=p.name, account=p.parent.name, source=rel(source),
               title=activity.get('title'), family='modern', completion_evidence=[], issues=[])
    rows = [dict(id=qid(q.get('math_academy_id') or q.get('dom_id')),
                 kp=q.get('knowledge_point') or q.get('kp_id') or q.get('knowledge_point_id'),
                 result=q.get('result'), position=q.get('sequence_position'))
            for q in data.get('questions', [])]
    row['groups'] = groups(rows)
    for sp, v in [(source, data.get('completion')), (p/'post-activity.json', post.get('completion'))]:
        t = completion_text(v)
        if t:
            row['completion_evidence'].append(dict(source=rel(sp), text=t, outcome=classify(t)))
    states = {e['outcome'] for e in row['completion_evidence'] if e['outcome']}
    row['outcome'] = next(iter(states)) if len(states) == 1 else 'unknown'
    if len(states) > 1:
        row['issues'].append('conflicting completion messages')
    if not data:
        row['issues'].append('missing history/content')
        if (p/'checkpoint.json').exists():
            ck = read(p/'checkpoint.json')
            row['unfinished_checkpoint'] = dict(stage=ck.get('stage'), completed_at=ck.get('completed_at'),
                                               completion=completion_text(ck.get('completion')))
    row['history_evidence_errors'] = data.get('evidence_errors', [])
    # Cross-check every explicitly failed lesson against independent live grades
    # and the grade spans in saved source HTML, not solver's intended answers.
    if row['outcome'] == 'failed':
        ckpath = p/'checkpoint.json'
        ck = read(ckpath) if ckpath.exists() else {}
        presentations = ck.get('presentations', {})
        live = {qid(k): v.get('grade') for k, v in presentations.items() if v.get('grade')}
        checks = []
        for q, compact in zip(data.get('questions', []), rows):
            soup = BeautifulSoup(q.get('raw_html') or q.get('html') or '', 'html.parser')
            span = soup.select_one('.answerResult')
            html_grade = span.get_text(' ', strip=True) if span else None
            actual = live.get(compact['id'])
            checks.append(dict(id=compact['id'], history=compact['result'], live=actual, html=html_grade))
            for label, other in [('live', actual), ('html', html_grade)]:
                if other is not None and LABELS.get(other, other) != LABELS.get(compact['result'], compact['result']):
                    row['issues'].append(f'{compact["id"]}: {label} grade differs from history')
        row['grade_crosschecks'] = checks
        row['checkpoint_source'] = rel(ckpath)
    return row


def legacy(p):
    d = read(p)
    if d.get('task_type') != 'lesson':
        return None
    rows = []
    for key, q in d.get('questions', {}).items():
        grade = q.get('actual_result') or (q.get('after') or {}).get('result')
        rows.append(dict(id=qid(key), kp=q.get('kp_id'), result=grade))
    t = completion_text(d.get('completion'))
    outcome = classify(t) or (d.get('activity_outcome') if d.get('activity_outcome') in ('passed','failed') else 'unknown')
    row = dict(task_id=p.parent.name, account=p.parent.parent.name if 'question-capture-workers' in p.parts else 'foundations',
               family='legacy', source=rel(p), groups=groups(rows), outcome=outcome, issues=[],
               completion_evidence=[dict(source=rel(p), text=t, outcome=classify(t),
                                         activity_outcome=d.get('activity_outcome'),
                                         completion_source=d.get('completion_source'))])
    if outcome == 'failed':
        checks = []
        for key, q in d.get('questions', {}).items():
            actual = q.get('actual_result')
            after = (q.get('after') or {}).get('result')
            history = (q.get('history') or {}).get('result')
            checks.append(dict(id=qid(key), history=history, live=actual, after=after))
            if len({LABELS.get(v, v) for v in [actual, after, history] if v is not None}) > 1:
                row['issues'].append(f'{key}: actual/after/history grades differ')
        row['grade_crosschecks'] = checks
    return row


def main():
    legacy_paths = sorted((BASE/'question-capture').glob('*/state.json')) + sorted((BASE/'question-capture-workers').glob('*/*/state.json'))
    # Union avoids relying on activity.json alone and includes incomplete captures.
    modern_dirs = sorted({p.parent for name in ['activity.json','post-activity.json','history-content.json','content.json']
                          for p in (BASE/'capture').glob('*/*/'+name)})
    work = [('legacy', p) for p in legacy_paths] + [('modern', p) for p in modern_dirs]
    print('Candidate directories/states:', len(work), flush=True)
    def extract(pair):
        kind, p = pair
        return legacy(p) if kind == 'legacy' else modern(p)
    records = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i, row in enumerate(pool.map(extract, work), 1):
            if row:
                records.append(row)
            if i % 1000 == 0:
                print('Scanned', i, flush=True)
    ids = Counter(r['task_id'] for r in records)
    assert max(ids.values()) == 1, 'Duplicate task IDs require explicit reconciliation'
    historical = []
    histpath = BASE/'progress-history-2026-10-04/observations.json'
    for t in read(histpath)['tasks']:
        if t['activity-type'] != 'Lesson':
            continue
        src = ROOT/t['source_file']
        raw = read(src)
        rows = [dict(id=qid(q['id']), kp=q.get('kp_href') or q.get('kp_title'), result=q.get('result'), position=q.get('ordinal'))
                for q in raw['questions']]
        historical.append(dict(task_id=t['task-id'], source=rel(src), title=t['topic-name'], groups=groups(rows),
                               outcome=classify(raw.get('task_text','')) or 'unknown',
                               limitation='Completed history label and positive XP do not establish pass/fail.'))
    failures = [r for r in records if r['outcome'] == 'failed']
    passed = [r for r in records if r['outcome'] == 'passed']
    # A separate early pilot is not in the account directories or progress CSV.
    standalone_path = BASE/'sum-rule-13925458/activity-capture.json'
    standalone_groups = []
    for kp in read(standalone_path)['kps']:
        soup = BeautifulSoup(kp['html'], 'html.parser')
        rows = []
        for q in soup.select('.question'):
            grade = q.select_one('.answerResult')
            rows.append(dict(id=qid(q.get('id')), kp=kp['title'], result=grade.get_text(' ',strip=True) if grade else None))
        standalone_groups.extend(groups(rows))
    standalone = [dict(task_id='13925458', source=rel(standalone_path), groups=standalone_groups, outcome='unknown')]
    contradictions = []
    for r in records + historical + standalone:
        for i, g in enumerate(r['groups']):
            s = g['sequence']
            if not s or g['kp'] is None:
                continue
            third = next((j+1 for j in range(len(s)) if s[:j+1].count('W') == 3), None)
            if third is None:
                if not(set(s)-{'C','W'}) and r['outcome'] == 'failed' and i == len(r['groups'])-1:
                    contradictions.append(dict(task_id=r['task_id'], source=r['source'], sequence=s, reason='failure before third miss'))
                continue
            if third != len(s) or i < len(r['groups'])-1 or r['outcome'] == 'passed':
                contradictions.append(dict(task_id=r['task_id'], source=r['source'], sequence=s, reason='continued or passed after third miss'))
    summary = dict(generated_at=datetime.now(timezone.utc).isoformat(),
                   method='Actual observed grades, never intended answers. Full Credit maps to C; No Credit maps to W; P=Partial Credit remains separate. Consecutive KP groups preserve source order. No pass/fail inference from XP or generic Completed labels.',
                   automated_capture_lessons=len(records), outcomes=dict(Counter(r['outcome'] for r in records)),
                   failed_lesson_records=len(failures),
                   explicit_failure_messages=sum(any(e.get('outcome') == 'failed' for e in r['completion_evidence']) for r in failures),
                   capture_flag_only_failures=[dict(task_id=r['task_id'], source=r['source'], completion_evidence=r['completion_evidence']) for r in failures if not any(e.get('outcome') == 'failed' for e in r['completion_evidence'])],
                   failure_final_kp_patterns=dict(sorted(Counter(r['groups'][-1]['sequence'] if r['groups'] else '(empty)' for r in failures).items())),
                   failure_issues=[dict(task_id=r['task_id'], issues=r['issues'], history_errors=r.get('history_evidence_errors')) for r in failures if r['issues'] or r.get('history_evidence_errors')],
                   binary_groups=sum(bool(g['sequence']) and not(set(g['sequence'])-{'C','W'}) and g['kp'] is not None for r in records for g in r['groups']),
                   partial_or_unknown_groups=sum(bool(set(g['sequence'])-{'C','W'}) or g['kp'] is None for r in records for g in r['groups']),
                   unknown_grade_groups=sum('?' in g['sequence'] for r in records for g in r['groups']),
                   passed_lessons_with_consecutive_misses=sum(any('WW' in g['sequence'] for g in r['groups']) for r in passed),
                   passed_lessons_with_three_or_more_misses_across_kps=sum(sum(g['sequence'].count('W') for g in r['groups']) >= 3 for r in passed),
                   historical_lessons=len(historical), threshold_counterexamples=contradictions,
                   standalone_history_lessons=len(standalone),
                   unknown_outcome_tasks=[dict(task_id=r['task_id'], source=r['source'], issues=r['issues'], completion_evidence=r['completion_evidence'], unfinished_checkpoint=r.get('unfinished_checkpoint')) for r in records if r['outcome']=='unknown'])
    OUT.write_text(json.dumps(dict(summary=summary, failures=failures, lessons=records, historical_lessons=historical, standalone_history=standalone), indent=2)+'\n')
    OUT.with_name('summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='unknown_outcome_tasks'}, indent=2), flush=True)


if __name__ == '__main__':
    main()
