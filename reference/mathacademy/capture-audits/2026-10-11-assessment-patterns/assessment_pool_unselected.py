"""Read-only comparison of historical aged topics with assessment selection.

Output is derived evidence, never a reconstruction of internal eligibility.
Prerequisite ancestry is explicitly not an encompassing-credit relationship.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
evidence = json.loads((OUT / 'evidence.json').read_text())
ages = json.loads((OUT / 'topic-age-evidence.json').read_text())


def content_directory(account, task):
    for part in [f'capture/{account}', 'question-capture' if account == 'foundations' else f'question-capture-workers/{account}']:
        path = ROOT / 'reference/mathacademy' / part / task
        if (path / 'content.json').exists():
            return path
    raise FileNotFoundError((account, task))


def diagnostic_probes(account, task):
    path = content_directory(account, task)
    content = json.loads((path / 'content.json').read_text())
    state = json.loads((path / 'state.json').read_text()) if (path / 'state.json').exists() else None
    return [{'topic_id': str(q['topic_id']), 'result': q.get('result') or state['questions'][q['math_academy_id']].get('actual_result')}
            for q in content['questions']]


def graph(account, cid):
    metric = next(x for x in evidence['xp_topic_membership_metrics'] if x['account'] == account and x['course_id'] == cid)
    source = Path(metric['membership_source']).parent / 'Prerequisites.csv'
    edges = defaultdict(set)
    for row in csv.DictReader(source.open()):
        edges[row['topic']].add(row['requires'])
    def ancestors(topic):
        result = set()
        todo = list(edges[topic])
        while todo:
            node = todo.pop()
            if node not in result:
                result.add(node)
                todo.extend(edges[node])
        return result
    return ancestors, str(source)


def snapshot(account, task, cid):
    path = ROOT / f'reference/mathacademy/capture/{account}/{task}/post-activity.json'
    data = json.loads(path.read_text())['observations']
    course = next(c for c in data['courses'] if c['course_id'] == cid)
    return {t['topic_id']: t for t in course['topics']}, course['captured_at'], str(path.relative_to(ROOT))


results = []
for account, cid, diag_task, last_task, quiz in [
    ('multivariable', '155', '14111253', '14124541', None),
    ('differential', '145', '14110945', '14123491', None),
    ('foundations', '154', '14070857', '14114793', '14116310'),
]:
    diag = next(x for x in evidence['diagnostics'] if x['account'] == account and x['task_id'] == diag_task)
    current, clock, source = snapshot(account, last_task, cid)
    if quiz:
        clock = next(r['assessment_time'] for r in ages['rows'] if r['quiz_id'] == quiz)
        diag_path = content_directory(account, diag_task) / 'knowledge-state/diagnostic-completed.json'
        diag_doc = json.loads(diag_path.read_text())
        baseline = {str(t['topic_id']): t for c in diag_doc['courses'] if str(c['course_id']) == cid for t in c['topics']}
        diag_source = str(diag_path.relative_to(ROOT))
    else:
        baseline, _, diag_source = snapshot(account, diag_task, cid)
    records = [r for r in evidence['records'] if r['account'] == account and r.get('completed_at') and r['complete'] and r['completed_at'] < clock]
    lesson_history = defaultdict(list)
    review_history = defaultdict(list)
    for r in sorted(records, key=lambda r: r['completed_at']):
        if r['kind'] == 'lesson':
            lesson_history[r['topic_id']].append(r)
        elif r['kind'] == 'review':
            review_history[r['topic_id']].append(r)
    probes = diagnostic_probes(account, diag_task)
    correct = {p['topic_id'] for p in probes if p['result'] == 'Correct'}
    ancestors, graph_source = graph(account, cid)
    selected = {r['topic_id'] for r in ages['rows'] if r['quiz_id'] == quiz} if quiz else set()
    prior_quizzed = {r['topic_id'] for r in ages['rows'] if r['account'] == account and r['assessment_time'] < diag['completed_at']}
    rows = []
    for topic, lessons in lesson_history.items():
        if topic not in current or clock - lessons[0]['completed_at'] < 48 * 3600:
            continue
        rows.append({
            'topic_id': topic, 'title': current[topic]['title'],
            'historical_first_lesson_id': lessons[0]['task_id'],
            'historical_first_lesson_age_hours': (clock - lessons[0]['completed_at']) / 3600,
            'latest_lesson_id': lessons[-1]['task_id'],
            'latest_lesson_age_hours': (clock - lessons[-1]['completed_at']) / 3600,
            'latest_lesson_before_diagnostic': lessons[-1]['completed_at'] < diag['completed_at'],
            'post_diagnostic_band': baseline[topic]['display_band'],
            'current_band': current[topic]['display_band'],
            'prior_review_count': len(review_history[topic]),
            'prior_review_ids': [r['task_id'] for r in review_history[topic]],
            'previous_captured_quiz_topic': topic in prior_quizzed,
            'selected_in_first_quiz': topic in selected,
            'direct_diagnostic_results': [p['result'] for p in probes if p['topic_id'] == topic],
            'correct_diagnostic_probes_with_topic_as_self_or_prerequisite_ancestor': sorted(p for p in correct if topic == p or topic in ancestors(p)),
        })
    focus = [r for r in rows if r['post_diagnostic_band'] > 0 and not r['previous_captured_quiz_topic'] and r['latest_lesson_before_diagnostic']]
    results.append({
        'account': account, 'course_id': cid, 'diagnostic_task_id': diag_task,
        'snapshot_task_id': last_task, 'quiz_id': quiz, 'clock': clock,
        'snapshot_source': source, 'diagnostic_snapshot_source': diag_source,
        'prerequisite_graph_source': graph_source,
        'historically_aged_native_topics': rows,
        'persistently_blue_old_unquizzed_focus_summary': {
            'count': len(focus),
            'current_bands': dict(Counter(r['current_band'] for r in focus)),
            'at_least_one_prior_direct_review': sum(r['prior_review_count'] > 0 for r in focus),
            'directly_correct_on_diagnostic': sum('Correct' in r['direct_diagnostic_results'] for r in focus),
            'self_or_ancestor_of_correct_diagnostic_probe': sum(bool(r['correct_diagnostic_probes_with_topic_as_self_or_prerequisite_ancestor']) for r in focus),
            'topic_ids': [r['topic_id'] for r in focus],
        },
    })

proof_probes = diagnostic_probes('linear', '14095701')
proof_ancestors, proof_graph = graph('linear', '76')
proof_correct = {p['topic_id'] for p in proof_probes if p['result'] == 'Correct'}
proof = [{
    'topic_id': r['topic_id'],
    'direct_diagnostic_results': [p['result'] for p in proof_probes if p['topic_id'] == r['topic_id']],
    'correct_diagnostic_probes_with_topic_as_self_or_prerequisite_ancestor': sorted(p for p in proof_correct if r['topic_id'] == p or r['topic_id'] in proof_ancestors(p)),
} for r in ages['rows'] if r['quiz_id'] == '14097922']
payload = {
    'courses': results,
    'proof_quiz1_diagnostic_ancestry_counterexample': proof,
    'limitations': [
        'No offered quiz does not identify individual topic ineligibility; whole-quiz assembly can fail.',
        'Display bands are not exact repetitions or mastery.',
        'Prerequisite ancestry is not an encompassing relationship and does not establish diagnostic credit propagation.',
        'Diagnostic capture outcomes can include duplicate probes; all observed results are retained.',
        'Historical lesson age may differ from current knowledge episode age after another diagnostic.',
    ],
}
(OUT / 'assessment-pool-unselected-evidence.json').write_text(json.dumps(payload, indent=2) + '\n')
print(json.dumps([{'account': c['account'], 'course_id': c['course_id'], 'historically_aged_native_count': len(c['historically_aged_native_topics']), **c['persistently_blue_old_unquizzed_focus_summary']} for c in results], indent=2))
