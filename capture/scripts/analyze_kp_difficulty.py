"""Read-only analysis: EDB pool inventory first, captured lesson positions second.

Run database export separately at one fixed basis. No database writes occur here.
"""
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
from pathlib import Path
import re

LEVELS = ('easy', 'moderate', 'hard')


def read(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def collect(root, folder):
    candidates = [(p, 'legacy-unlabelled') for p in sorted(
        (root / 'reference/mathacademy/question-capture').glob('*/content.json'))]
    candidates += [(p, p.parent.parent.name) for p in sorted(
        (root / 'reference/mathacademy/capture').glob('*/*/content.json'))]

    def extract(pair):
        path, account = pair
        raw = path.read_bytes()
        content = json.loads(raw)
        task = dict(account=account, task_id=str(content['task_id']),
                    kind=content.get('task_type', content.get('kind')),
                    topic_id=content.get('topic_id'), source_file=str(path.relative_to(root)),
                    source_sha256=hashlib.sha256(raw).hexdigest(), questions=[], examples=[],
                    ordered_examples=[], position_evidence=None, complete=False)
        for example in content.get('canonical_examples', []):
            task['examples'].append(dict(example=example.get('math_academy_id'),
                raw_kp=str(example.get('knowledge_point_id')), title=example.get('knowledge_point')))
        for q in content.get('questions', []):
            task['questions'].append(dict(question=q.get('math_academy_id'),
                raw_kp=str(q.get('knowledge_point_id')), title=q.get('knowledge_point'),
                level=q.get('difficulty'), source_example=q.get('source_example_id'),
                authored=bool(q.get('difficulty_provenance'))))
        if task['kind'] != 'lesson':
            return task
        definition = content.get('lesson_definition', {})
        if definition.get('complete'):
            task['ordered_examples'] = ['e-' + str(s['content_id']) for s in
                sorted(definition['steps'], key=lambda s: s['position'])
                if s['type'] in ('example', 'knowledge-point')]
            task['position_evidence'] = 'complete explicit lesson definition'
            task['complete'] = True
        elif account == 'legacy-unlabelled':
            state_path = path.parent / 'state.json'
            state_raw = state_path.read_bytes()
            state = json.loads(state_raw)
            task['state_file'] = str(state_path.relative_to(root))
            task['state_sha256'] = hashlib.sha256(state_raw).hexdigest()
            by_kp = {e['raw_kp']: e['example'] for e in task['examples']}
            order = [by_kp.get(k) for k in state.get('kps', {})]
            if order and all(order) and len(set(order)) == len(order) and state.get('lesson_complete'):
                task['ordered_examples'] = order
                task['complete'] = True
                task['position_evidence'] = 'completed lesson; KP checkpoint insertion order'
                meta_path = path.parent / 'activity-metadata.json'
                if meta_path.exists():
                    meta_raw = meta_path.read_bytes()
                    task['metadata_file'] = str(meta_path.relative_to(root))
                    task['metadata_sha256'] = hashlib.sha256(meta_raw).hexdigest()
                    metadata = {r['id'].replace('question-', 'q-'): r for r in json.loads(meta_raw)}
                    checks = []
                    for q in task['questions']:
                        row = metadata.get(q['question'], {})
                        match = re.match(r'^KP\s+(\d+)\.', row.get('kp_title', ''))
                        if match and q['raw_kp'] in by_kp:
                            checks.append(int(match[1]) == order.index(by_kp[q['raw_kp']]) + 1)
                    if checks and all(checks):
                        task['position_evidence'] += '; verified against numbered history KP labels'
                    elif checks:
                        task['complete'] = False
                        task['position_evidence'] = 'order conflict with numbered history labels'
        return task

    with ThreadPoolExecutor(max_workers=3) as pool:
        tasks = list(pool.map(extract, candidates))
    dump(folder / 'capture-projections.json', tasks)
    print('Captured tasks:', len(tasks), flush=True)


def summaries(rows, key):
    grouped = defaultdict(list)
    for r in rows:
        grouped[str(key(r))].append(r)
    result = {}
    for label, group in sorted(grouped.items()):
        totals = {level: sum(r['counts'][level] for r in group) for level in LEVELS}
        n = sum(totals.values())
        result[label] = dict(kps=len(group), questions=n, counts=totals,
            question_percent={l: 100 * totals[l] / n if n else None for l in LEVELS},
            kp_mean_percent={l: 100 * sum(r['counts'][l] / r['rated_questions']
                for r in group if r['rated_questions']) / sum(bool(r['rated_questions']) for r in group)
                if any(r['rated_questions'] for r in group) else None for l in LEVELS},
            zero_counts={l: sum(r['counts'][l] == 0 for r in group) for l in LEVELS})
    return result


def analyze(root, folder):
    points = read(folder / 'database/pool-inventory.json')
    tasks = read(folder / 'capture-projections.json')
    ma_rated = set(read(folder / 'database/math-academy-rated-question-entities.json'))
    db_examples = {p[':db/id']: p.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id')
                   for p in points}
    db_kp_ids = {str(identity): db_examples.get(entity)
                 for entity, identity in read(folder / 'database/kp-identities.json')}
    # Identity comes from canonical example IDs, never from a title-only match.
    bridge = defaultdict(set)
    for task in tasks:
        for e in task['examples']:
            if e['example']:
                bridge[e['raw_kp']].add(e['example'])
    task_ids = defaultdict(list)
    for task in tasks:
        task_ids[task['task_id']].append(task)
    tasks = [max(group, key=lambda t: (t['account'] != 'legacy-unlabelled',
              t['position_evidence'] == 'complete explicit lesson definition', len(t['questions'])))
             for group in task_ids.values()]
    positions = defaultdict(list)
    capture_ratings = defaultdict(lambda: defaultdict(set))
    occurrences = defaultdict(dict)
    diagnostics = Counter()
    for task in tasks:
        order = task['ordered_examples'] if task['complete'] else []
        for index, example in enumerate(order):
            positions[example].append(dict(task_id=task['task_id'], account=task['account'],
                topic_id=str(task['topic_id']), position=index + 1, lesson_kps=len(order),
                relative_position=index / (len(order) - 1) if len(order) > 1 else None,
                source_file=task['source_file'], evidence=task['position_evidence']))
        for q in task['questions']:
            if not isinstance(q['question'], str) or not q['question'].startswith('q-'):
                diagnostics['nonordinary_questions'] += 1
                continue
            options = bridge.get(q['raw_kp'], set())
            example = q['source_example'] or db_kp_ids.get(q['raw_kp']) or ('e-' + q['raw_kp'] if q['raw_kp'].isdigit()
                      else next(iter(options)) if len(options) == 1 else None)
            if not example:
                diagnostics['unresolved_capture_kp_occurrences'] += 1
                continue
            if q['level'] in LEVELS and not q['authored']:
                capture_ratings[example][q['question']].add(q['level'])
            occurrences[example][(task['task_id'], q['question'])] = dict(
                task_id=task['task_id'], account=task['account'], kind=task['kind'],
                question=q['question'], level=q['level'], source_file=task['source_file'],
                local_position=order.index(example) + 1 if example in order else None)
    database_by_example = defaultdict(list)
    for p in points:
        e = p.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id')
        database_by_example[e].append(p)
    capture_by_task = defaultdict(list)
    for example, group in occurrences.items():
        for occurrence in group.values():
            capture_by_task[occurrence['task_id']].append((example, occurrence['level']))
    rows = []
    for p in points:
        example = p.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id')
        pool = p.get(':knowledge-point/questions', [])
        counts = Counter(q.get(':question/difficulty', {}).get(':db/ident', '').split('/')[-1]
                         for q in pool)
        mids = {q.get(':question/math-academy-id') for q in pool}
        ma_counts = Counter(q.get(':question/difficulty', {}).get(':db/ident', '').split('/')[-1]
                           for q in pool if q[':db/id'] in ma_rated)
        observed_positions = positions.get(example, [])
        position_pairs = Counter((r['position'], r['lesson_kps']) for r in observed_positions)
        position_set = {r['position'] for r in observed_positions}
        latest = max(observed_positions, key=lambda r: int(r['task_id'])) if observed_positions else None
        captured = capture_ratings.get(example, {})
        extra = {mid: sorted(levels) for mid, levels in captured.items() if mid not in mids}
        conflicts = {mid: sorted(levels) for mid, levels in captured.items() if len(levels) > 1}
        distinct_captured = {level: sum(levels == {level} for levels in captured.values()) for level in LEVELS}
        n = sum(counts[l] for l in LEVELS)
        occurrence_rows = list(occurrences.get(example, {}).values())
        account_counts = {}
        for account in sorted({r['account'] for r in occurrence_rows}):
            relevant = [r for r in occurrence_rows if r['account'] == account]
            ids = {r['question'] for r in relevant}
            account_counts[account] = dict(unique_questions=len(ids), tasks=len({r['task_id'] for r in relevant}),
                distinct_by_level={level: len({r['question'] for r in relevant if r['level'] == level}) for level in LEVELS},
                kinds=dict(Counter(r['kind'] for r in relevant)))
        row = dict(kp_entity=p[':db/id'], example_id=example, title=p.get(':knowledge-point/title'),
            topics=[dict(id=t.get(':topic/math-academy-id'), title=t.get(':topic/title'))
                    for t in p.get(':topic/_knowledge-points', [])], total_questions=len(pool),
            rated_questions=n, counts={l: counts[l] for l in LEVELS}, unknown_questions=len(pool) - n,
            math_academy_counts={l: ma_counts[l] for l in LEVELS},
            distinct_capture_counts=distinct_captured, extra_captured_questions=extra,
            conflicting_capture_ratings=conflicts, positions=observed_positions,
            latest_position=latest, stable_position=len(position_set) == 1,
            position_variants=[dict(position=a, lesson_kps=b, tasks=c) for (a,b),c in sorted(position_pairs.items())],
            occurrence_count=len(occurrence_rows), distinct_capture_tasks=len({r['task_id'] for r in occurrence_rows}),
            account_evidence=account_counts, question_ids=sorted(mid for mid in mids if mid),
            missing_levels=[l for l in LEVELS if counts[l] == 0])
        row['other_kps_with_level_in_same_lesson_tasks'] = {
            level: sorted({p['task_id'] for p in observed_positions
                           if any(other != example and rating == level
                                  for other, rating in capture_by_task[p['task_id']])}, key=int)
            for level in LEVELS if counts[level] == 0}
        # Claims of absence concern the scraped MA bank, rather than authored questions.
        row['assessments'] = {}
        for level in LEVELS:
            if counts[level]:
                verdict = 'observed in database'
            elif distinct_captured[level]:
                verdict = 'exists in captures; database pool incomplete'
            elif n >= 30 and sum(ma_counts[l] for l in LEVELS) >= 30 and row['distinct_capture_tasks'] >= 2:
                verdict = 'strong best guess: unavailable'
            elif n >= 20 and sum(ma_counts[l] for l in LEVELS) >= 20:
                verdict = 'best guess: unavailable'
            elif n >= 10:
                verdict = 'tentative absence'
            else:
                verdict = 'insufficient sampling'
            row['assessments'][level] = dict(verdict=verdict,
                zero_observation_likelihood_at_10_percent=(.9 ** n if counts[level] == 0 else None),
                zero_observation_likelihood_at_5_percent=(.95 ** n if counts[level] == 0 else None),
                iid_zero_success_95_percent_upper_bound=(1 - .05 ** (1 / n) if n and counts[level] == 0 else None))
        rows.append(row)
    dump(folder / 'kp-inventory.json', rows)
    dump(folder / 'capture-occurrences.json', [dict(example_id=e, **r) for e, group in occurrences.items() for r in group.values()])
    known = [r for r in rows if r['latest_position']]
    primary = [r for r in known if r['stable_position']]
    def band(r):
        p = r['latest_position']
        return 'single' if p['lesson_kps'] == 1 else 'first' if p['position'] == 1 else 'last' if p['position'] == p['lesson_kps'] else 'middle'
    summary = dict(basis=read(folder / 'database/identity.json'), database_kps=len(rows),
        total_questions=sum(r['total_questions'] for r in rows), rated_questions=sum(r['rated_questions'] for r in rows),
        unique_database_questions=len({q[':db/id'] for p in points for q in p.get(':knowledge-point/questions', [])}),
        level_totals={l: sum(r['counts'][l] for r in rows) for l in LEVELS},
        missing_level_kps={l: sum(not r['counts'][l] for r in rows) for l in LEVELS},
        missing_level_verdicts={l: dict(Counter(r['assessments'][l]['verdict'] for r in rows if not r['counts'][l])) for l in LEVELS},
        kps_with_positions=len(known), kps_with_stable_positions=len(primary),
        kps_with_changing_positions=sum(not r['stable_position'] for r in known),
        canonical_example_duplicates=sum(example is not None and len(group)>1
                                        for example, group in database_by_example.items()),
        capture_tasks=len(tasks), complete_position_lessons=sum(bool(t['complete']) for t in tasks),
        complete_lesson_accounts=dict(Counter(t['account'] for t in tasks if t['complete'])),
        capture_diagnostics=dict(diagnostics),
        all_positions=summaries(primary, lambda r:r['latest_position']['position']),
        role=summaries(primary,band),
        well_sampled_role=summaries([r for r in primary if r['rated_questions'] >= 20],band),
        sample_sizes=summaries(rows,lambda r:'30+' if r['rated_questions']>=30 else '20–29' if r['rated_questions']>=20 else '10–19' if r['rated_questions']>=10 else '5–9' if r['rated_questions']>=5 else '0–4'),
        generated_at=datetime.now(timezone.utc).isoformat())
    dump(folder / 'summary.json', summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('all_positions','role','well_sampled_role')}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('collect', 'analyze'))
    parser.add_argument('--folder', default='reference/mathacademy/kp-difficulty-analysis-2026-10-12')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    folder = root / args.folder
    folder.mkdir(parents=True, exist_ok=True)
    globals()[args.action](root, folder)


if __name__ == '__main__':
    main()
