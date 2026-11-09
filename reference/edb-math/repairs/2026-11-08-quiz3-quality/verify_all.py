"""Read-only final ownership, answer-binding, and study-availability checks."""
import concurrent.futures
import json
from pathlib import Path
import re
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from migrate_learner_history import connection

IDS = [17592186000000 + n for n in [
    48535, 48459, 48202, 50537, 50677, 50032, 50426, 48257, 50150,
    49102, 50895, 49370, 50522, 48391, 50557, 48289, 50433, 50040, 49099]]


def availability(tid):
    with urllib.request.urlopen(
            f'http://127.0.0.1:8765/api/topic-study-availability?topicId={tid}', timeout=120) as response:
        value = json.load(response)
    return {k: v for k, v in value.items() if k != 'idAliases'}


def main():
    out = HERE / 'final'
    out.mkdir(exist_ok=True)
    db = connection()
    basis = db.basis()
    query = (ROOT / 'reference/edb-math/audits/2026-11-08-topic-17592186048459/topic-before-query.edn').read_text()
    # Keep each observation below the database's value-byte budget.
    topics = {}
    for tid in IDS:
        rows = db.query(query, [tid], out, f'topic-{tid}', basis)
        topics[tid] = rows[0][0]
        print(f'Read {topics[tid][":topic/title"]} at basis {basis}', flush=True)
    assert set(topics) == set(IDS), sorted(set(IDS) - set(topics))
    summaries, defects, all_questions = [], [], {}
    lesson_query = (ROOT / 'reference/edb-math/audits/2026-11-08-topic-17592186048459/lessons-before-query.edn').read_text()
    tutorial_ids, step_ids = set(), set()
    for tid in IDS:
        topic = topics[tid]
        lessons = db.query(lesson_query, [tid], out, f'lessons-{tid}', basis)
        if not lessons:
            defects.append({'topic': tid, 'kind': 'missing_lesson_activity'})
        topic_kps = {kp[':db/id'] for kp in topic[':topic/knowledge-points']}
        lesson_kps = set()
        for row in lessons:
            activity = row[0]
            steps = {s[':db/id']: s for s in activity.get(':activity/steps', [])}
            step_ids.update(steps)
            cursor = activity.get(':activity/first-step', {}).get(':db/id')
            visited = set()
            while cursor is not None and cursor in steps and cursor not in visited:
                visited.add(cursor)
                content = steps[cursor].get(':step/content', {})
                if ':tutorial/content' in content:
                    tutorial_ids.add(content[':db/id'])
                if ':knowledge-point/id' in content:
                    lesson_kps.add(content[':db/id'])
                cursor = steps[cursor].get(':step/next', {}).get(':db/id')
            if cursor is not None or visited != set(steps):
                defects.append({'topic': tid, 'activity': activity[':db/id'], 'kind': 'invalid_lesson_route',
                                'cursor': cursor, 'visited_steps': len(visited), 'owned_steps': len(steps)})
        if lesson_kps != topic_kps:
            defects.append({'topic': tid, 'kind': 'lesson_kp_coverage_mismatch',
                            'topic_kps': sorted(topic_kps), 'lesson_kps': sorted(lesson_kps)})
        questions = {q[':db/id']: q for kp in topic[':topic/knowledge-points']
                     for q in [kp.get(':knowledge-point/canonical-example')] + kp.get(':knowledge-point/questions', []) if q}
        all_questions.update(questions)
        for qid, q in questions.items():
            if not q.get(':question/problem', '').strip():
                defects.append({'topic': tid, 'question': qid, 'kind': 'missing_prompt'})
            if not q.get(':question/worked-solution', '').strip():
                defects.append({'topic': tid, 'question': qid, 'kind': 'missing_solution'})
            fields = q.get(':question/answer-fields', [])
            keys = [f.get(':answer-field/key') for f in fields]
            if len(keys) != len(set(keys)):
                defects.append({'topic': tid, 'question': qid, 'kind': 'duplicate_field_keys', 'keys': keys})
            for f in fields:
                correct = f.get(':answer-field/correct')
                if not correct or ':answer/value' not in correct:
                    defects.append({'topic': tid, 'question': qid, 'field': f[':db/id'], 'kind': 'missing_correct'})
                elif correct[':db/id'] not in [a[':db/id'] for a in f.get(':answer-field/choices', [])]:
                    defects.append({'topic': tid, 'question': qid, 'field': f[':db/id'], 'kind': 'correct_outside_bank'})
            tokens = set(re.findall(r'\{\{(?:answer-field:)?([^{}]+)\}\}', q.get(':question/problem', '')))
            if tokens and tokens != set(keys):
                defects.append({'topic': tid, 'question': qid, 'kind': 'prompt_binding_mismatch',
                                'tokens': sorted(tokens), 'keys': keys})
        summaries.append({'entity': tid, 'title': topic[':topic/title'],
                          'knowledge_points': len(topic[':topic/knowledge-points']), 'questions': len(questions)})
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        available = dict(zip(IDS, pool.map(availability, IDS)))
    for s in summaries:
        s['availability'] = available[s['entity']]
    report = {'basis': basis, 'read_only': True, 'topic_count': len(topics),
              'distinct_questions': len(all_questions), 'topics': summaries, 'defects': defects,
              'distinct_tutorials': len(tutorial_ids), 'distinct_lesson_steps': len(step_ids),
              'content_bindings_passed': not defects,
              'all_topics_available': all(v.get('available') for v in available.values())}
    (out / 'verification.json').write_text(json.dumps(report, default=str, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('topics', 'defects')}
                     | {'defect_count': len(defects), 'first_defects': defects[:12]}, indent=2))


if __name__ == '__main__':
    main()
