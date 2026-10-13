"""Audit eight captured retake pairs and surrounding source queues, without writes to EDB."""
from pathlib import Path
from datetime import datetime
import collections
import csv
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text()) if path.exists() else {}


def csv_rows(name):
    with (OUT / name).open() as f:
        return list(csv.DictReader(f))


def completed_at(state, kind):
    value = state.get('knowledge_snapshots', {}).get(kind + '-completed', {}).get('finished_at')
    return datetime.fromisoformat(value) if value else None


def inspect_reviews(task, questions):
    directory = ROOT / Path(task['source_file']).parent
    after = read(directory / 'queue-after.json')
    missed = {q['topic_mid'] for q in questions if q['grade'].lower() == 'incorrect'}
    reviews = [q for q in after.get('queue', []) if q.get('task_type') == 'review'
               and str(q.get('topic_id')) in missed]
    evidence = []
    for review in reviews:
        path = directory.parent / str(review['task_id'])
        state = read(path / 'state.json')
        after_review = read(path / 'queue-after.json')
        evidence.append({
            'review_task_id': review['task_id'], 'topic_mid': str(review['topic_id']),
            'complete': bool(state.get('review_complete') or state.get('activity_complete')),
            'completion_capture_at': completed_at(state, 'review').isoformat() if completed_at(state, 'review') else None,
            'after_queue_exists': (path / 'queue-after.json').exists(),
            'queue_after': [{k: q.get(k) for k in ['task_id', 'task_type', 'title',
                                                 'assessment_requirement', 'optional_xp_remaining']}
                           for q in after_review.get('queue', [])],
            'review_state_source': str((path / 'state.json').relative_to(ROOT)),
            'review_queue_source': str((path / 'queue-after.json').relative_to(ROOT)),
        })
    return after, evidence


tasks = {t['task_id']: t for t in csv_rows('assessment-tasks.csv')}
questions = collections.defaultdict(list)
for q in csv_rows('assessment-questions.csv'):
    questions[q['task_id']].append(q)
pairs = read(OUT / 'remediation-summary.json')['retake_pairs']
pair_evidence = []
for pair in pairs:
    original = tasks[pair['original']]
    retake = tasks[pair['retake']]
    a = {q['topic_mid']: q for q in questions[pair['original']]}
    b = {q['topic_mid']: q for q in questions[pair['retake']]}
    directory = ROOT / Path(retake['source_file']).parent
    queue = read(directory / 'assessment-queue.json')
    state = read(directory / 'state.json')
    before_queue = read(directory / 'selection/queue.json')
    _, review_evidence = inspect_reviews(original, questions[pair['original']])
    start = state.get('assessment_pacing', {}).get('started_at')
    original_state = read(ROOT / Path(original['source_file']).parent / 'state.json')
    capture_end = completed_at(original_state, 'assessment')
    completion_interval = None
    if pair['stream'] == 'human-history':
        completion_interval = (datetime.fromisoformat(retake['completed_at']) -
                               datetime.fromisoformat(original['completed_at'])).total_seconds() / 60
    offered_after = [e for e in review_evidence if any(str(q['task_id']) == pair['retake']
                                                     for q in e['queue_after'])]
    assert not ({q['question_mid'] for q in a.values()} & {q['question_mid'] for q in b.values()})
    assert set(b) <= set(a)
    assert all(q['kp_href'] == a[topic]['kp_href'] for topic, q in b.items())
    pair_evidence.append({
        **pair,
        'original_correct': sum(q['grade'].lower() == 'correct' for q in a.values()),
        'original_score_percent': None if pair['expired_unanswered_original'] else
                                  100 * sum(q['grade'].lower() == 'correct' for q in a.values()) / len(a),
        'retake_correct': sum(q['grade'].lower() == 'correct' for q in b.values()),
        'same_knowledge_points': len(b),
        'retested_previously_correct_topics': sum(a[topic]['grade'].lower() == 'correct' for topic in b),
        'omitted_original_topics': [{'topic_mid': topic, 'title': q['topic_title'], 'grade': q['grade']}
                                    for topic, q in a.items() if topic not in b],
        'retake_requirement': queue.get('assessment_requirement'),
        'retake_notice': queue.get('assessment_notice'),
        'retake_optional_xp_remaining': queue.get('optional_xp_remaining'),
        'capture_worker_selection_reason': queue.get('selection_reason'),
        'other_tasks_offered_before_retake_start': [q['task_id'] for q in before_queue.get('queue', [])
                                                    if str(q['task_id']) != pair['retake']],
        'retake_queue_source': str((directory / 'assessment-queue.json').relative_to(ROOT)) if queue else None,
        'retake_before_queue_source': str((directory / 'selection/queue.json').relative_to(ROOT)) if before_queue else None,
        'original_to_retake_completion_minutes_human': completion_interval,
        'original_completion_capture_to_retake_start_minutes':
            (start - capture_end.timestamp()) / 60 if start and capture_end else None,
        'remedial_review_evidence': review_evidence,
        'first_offer_in_followup_review_queue': offered_after,
        'post_retake_review_evidence': inspect_reviews(retake, questions[pair['retake']])[1],
    })

# Check observed offers after remediation, not merely absence of completed retake
# records. An offer counts only when its title matches the original quiz title.
trigger_comparisons = []
for task in tasks.values():
    if task['stream'] not in ('older-automated', 'recent-automated') or task['retake'] == 'True':
        continue
    qs = questions[task['task_id']]
    missed = {q['topic_mid'] for q in qs if q['grade'].lower() == 'incorrect'}
    _, evidence = inspect_reviews(task, qs)
    if not missed or {e['topic_mid'] for e in evidence} != missed:
        continue
    if not all(e['complete'] and e['after_queue_exists'] for e in evidence):
        continue
    title = task['title'] + ' (Retake)'
    offers = [q for e in evidence for q in e['queue_after'] if q['title'] == title]
    correct = sum(q['grade'].lower() == 'correct' for q in qs)
    trigger_comparisons.append({
        'task_id': task['task_id'], 'title': task['title'], 'stream': task['stream'],
        'correct': correct, 'questions': len(qs), 'score_percent': 100 * correct / len(qs),
        'missed_topics': len(missed), 'completed_missed_topic_reviews': len(evidence),
        'retake_offered': bool(offers), 'retake_offer_ids': sorted({q['task_id'] for q in offers}),
        'original_source_file': task['source_file'], 'review_evidence': evidence,
    })

yes = [r for r in trigger_comparisons if r['retake_offered']]
no = [r for r in trigger_comparisons if not r['retake_offered']]
summary = {
    'captured_completed_retakes': len(pair_evidence),
    'human_retakes': sum(p['stream'] == 'human-history' for p in pair_evidence),
    'automated_retakes': sum(p['stream'] == 'older-automated' for p in pair_evidence),
    'retake_questions': sum(p['retake_topics'] for p in pair_evidence),
    'shared_original_question_ids': 0,
    'all_retake_questions_use_original_knowledge_points': True,
    'full_topic_set_retakes': sum(p['original_topics'] == p['retake_topics'] for p in pair_evidence),
    'subset_topic_retakes': sum(p['original_topics'] != p['retake_topics'] for p in pair_evidence),
    'originally_correct_topics_retested': sum(p['retested_previously_correct_topics'] for p in pair_evidence),
    'fully_observed_post_review_trigger_sequences': len(trigger_comparisons),
    'retake_offer_sequences': len(yes),
    'no_retake_offer_sequences': len(no),
    'highest_score_with_observed_retake_offer': max(r['score_percent'] for r in yes),
    'lowest_score_without_observed_retake_offer': min(r['score_percent'] for r in no),
    'inferred_threshold': 'A cutoff near 75% is consistent; 71.43% offered, 76.92% not offered. No exact boundary case.',
    'required_retake_transition_observed': False,
    'pairs': pair_evidence,
    'trigger_comparisons': trigger_comparisons,
    'limits': [
        'Eight completed retakes are not an inventory of all offers or all possible retakes.',
        'Five automated retakes were selected immediately by our worker, which prioritizes them independently of requirement status.',
        'Their source-backed requirement labels are unknown, with no optional-XP countdown; all five had other offered tasks at start.',
        'Human completion history does not record offer/unlock timestamps or required status.',
        'Automated timing uses capture completion observations and a worker-recorded start timestamp; it is not an exact server unlock time.',
        'The expired original was recovered later. Its recovery timestamp must not be used as its completion time.',
        'No captured retake was left available long enough here to establish whether it later became required.',
    ],
}
(OUT / 'retake-behavior.json').write_text(json.dumps(summary, indent=2) + '\n')
simple = [{k: v for k, v in r.items() if k != 'review_evidence'} for r in trigger_comparisons]
with (OUT / 'retake-trigger-comparison.csv').open('w') as f:
    writer = csv.DictWriter(f, fieldnames=list(simple[0]))
    writer.writeheader()
    writer.writerows(simple)
print(json.dumps({k: v for k, v in summary.items() if k not in ('pairs', 'trigger_comparisons')}, indent=2))
