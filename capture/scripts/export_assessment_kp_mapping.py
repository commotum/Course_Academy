#!/usr/bin/env python3
"""Read-only, fixed-basis export of assessed question membership and lesson order.

Run from the repository root with ``python3 -m capture.scripts.export_assessment_kp_mapping``.
Retained query/input/result EDN files make each mapping auditable. No writer is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import threading

from .config import Config
from .database.client import EDBClient
from .database.edn import dumps, loads


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')


def ref(value):
    return value.get(':db/id') if isinstance(value, dict) else value


def select(root):
    tasks = []
    for path in sorted((root / 'reference/mathacademy/capture').glob('*/*/activity.json')):
        activity = json.loads(path.read_text())
        if activity.get('kind') != 'assessment':
            continue
        content_path = path.parent / 'content.json'
        completion_path = path.parent / 'capture-complete.json'
        if not content_path.exists() or not completion_path.exists():
            continue
        raw = content_path.read_bytes()
        content = json.loads(raw)
        tasks.append(dict(account=path.parent.parent.name, task_id=path.parent.name,
            title=content.get('title', activity.get('title')),
            course_id=str(content.get('course_id') or activity.get('course_id') or '') or None,
            source_file=str(content_path.relative_to(root)), source_sha256=hashlib.sha256(raw).hexdigest(),
            questions=[dict(question_id=q.get('math_academy_id'),
                topic_id=str(q.get('topic_id') or content.get('topic_id') or '') or None,
                source_kp_id=str(q.get('knowledge_point_id') or '') or None,
                source_kp_title=q.get('knowledge_point'), source_example_id=q.get('source_example_id'))
                for q in content.get('questions', [])]))
    return tasks


QUESTION_PULL = '''[:db/id :question/id :question/math-academy-id
 {[:knowledge-point/_questions :limit nil] [:db/id]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id]}]'''
TOPIC_PULL = '''[:db/id :topic/id :topic/math-academy-id :topic/title
 {[:topic/knowledge-points :limit nil] [:db/id :knowledge-point/id :knowledge-point/title
 {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}
 {[:knowledge-point/questions :limit nil] [:db/id :question/math-academy-id]}]}]'''
ACTIVITY_PULL = '''[:db/id :activity/id :activity/math-academy-id :activity/title
 {:activity/type [:db/id :db/ident]} {:activity/scope [:db/id :topic/math-academy-id]}
 :activity/first-step
 {[:activity/steps :limit nil] [:db/id :step/next
 {:step/content [:db/id :knowledge-point/id :knowledge-point/title :tutorial/id
 :question/id :question/math-academy-id
 {[:knowledge-point/_canonical-example :limit nil] [:db/id]}]}]}]'''


def read_database(client, directory, selection, basis=None):
    previous_identity = json.loads((directory / 'identity.json').read_text()) if (directory / 'identity.json').exists() else None
    identity = client.status()
    if basis is not None:
        if basis > identity['basis']:
            raise ValueError('Requested basis is newer than the database')
        identity['basis'] = basis
    basis = identity['basis']
    dump(directory / 'identity.json', identity)
    qids = sorted({q['question_id'] for t in selection for q in t['questions']
                   if isinstance(q['question_id'], str) and re.fullmatch(r'q-\d+', q['question_id'])})
    topic_ids = {int(q['topic_id']) for t in selection for q in t['questions'] if q['topic_id']}

    def query(name, source, inputs):
        output = directory / (name + '.edn')
        query_path, input_path = directory / (name + '-query.edn'), directory / (name + '-inputs.edn')
        if (previous_identity == identity and output.exists() and query_path.exists() and input_path.exists()
                and query_path.read_text() == source and input_path.read_text() == dumps(inputs)):
            return loads(output.read_text())
        return client.query(source, inputs, directory, name, basis)

    def batches(name, source, values, size=75):
        groups = [(offset, values[offset:offset + size]) for offset in range(0, len(values), size)]
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(lambda g: query(name + '-' + str(g[0]), source, [g[1]]), groups))
        return [row for group in results for row in group]

    questions = [row[0] for row in batches('questions',
        '[:find (pull ?q ' + QUESTION_PULL + ') :in $ [?id ...] :where [?q :question/math-academy-id ?id]]', qids)]
    membership_kps = sorted({ref(kp) for q in questions
        for attr in (':knowledge-point/_questions', ':knowledge-point/_canonical-example') for kp in q.get(attr, [])})
    additional = batches('membership-topics', '''[:find ?kp ?id :in $ [?kp ...]
        :where [?t :topic/knowledge-points ?kp] [?t :topic/math-academy-id ?id]]''', membership_kps)
    topic_ids.update(row[1] for row in additional)
    topics = [row[0] for row in batches('topics', '[:find (pull ?t ' + TOPIC_PULL + ''')
        :in $ [?id ...] :where [?t :topic/math-academy-id ?id]]''', sorted(topic_ids), 20)]
    # Select lesson identities once before pulling. A combined topic/type query
    # can generate a large intermediate relation before its topic filter binds.
    lesson_ids = query('lesson-identities', '''[:find ?a ?t :where
        [?a :activity/type :activity.type/lesson] [?a :activity/scope ?t]]''', [])
    topic_entities = {t[':db/id'] for t in topics}
    scoped_lessons = sorted({a for a, t in lesson_ids if t in topic_entities})
    activities = [row[0] for row in batches('lesson-entities', '[:find (pull ?a ' + ACTIVITY_PULL + ''')
        :in $ [?a ...] :where [?a :activity/id _]]''', scoped_lessons, 30)]
    courses = [row[0] for row in query('courses', '''[:find (pull ?c
        [:db/id :course/id :course/math-academy-id :course/title]) :where [?c :course/id _]]''', [])]
    membership_sources = batches('assessed-membership-sources', '''[:find ?kp ?q ?source
        :in $ [?id ...] :where [?q :question/math-academy-id ?id]
        [?kp :knowledge-point/questions ?q _ ?s] [?s :db/ident ?source]]''', qids)
    kp_ids = sorted({kp[':db/id'] for t in topics for kp in t.get(':topic/knowledge-points', [])})
    pool_sources = batches('pool-membership-sources', '''[:find ?kp ?q ?source
        :in $ [?kp ...] :where [?kp :knowledge-point/questions ?q _ ?s]
        [?q :question/math-academy-id ?id] [?s :db/ident ?source]]''', kp_ids, 40)
    raw = dict(identity=identity, topics=topics, questions=questions, activities=activities,
        courses=courses, membership_sources=membership_sources, pool_sources=pool_sources)
    dump(directory / 'raw-projections.json', raw)
    return raw


def ordered_route(activity, kp_by_entity):
    steps = {s[':db/id']: s for s in activity.get(':activity/steps', [])}
    current = ref(activity.get(':activity/first-step'))
    seen, order, errors, kp_order = set(), [], [], []
    if current is None:
        errors.append('missing_first_step')
    while current is not None:
        if current in seen:
            errors.append('cycle')
            break
        if current not in steps:
            errors.append('next_outside_owned_steps')
            break
        seen.add(current)
        step = steps[current]
        content = step.get(':step/content', {})
        kind, kp = 'unknown', None
        if ':knowledge-point/id' in content:
            kind, kp = 'knowledge_point', content[':db/id']
        elif ':tutorial/id' in content:
            kind = 'tutorial'
        elif ':question/id' in content:
            owners = sorted(ref(p) for p in content.get(':knowledge-point/_canonical-example', []))
            if len(owners) == 1:
                kind, kp = 'canonical_example', owners[0]
            else:
                kind = 'question'
                errors.append('question_content_without_unique_canonical_kp')
        else:
            errors.append('unrecognized_step_content')
        order.append(dict(step_entity=current, content_entity=ref(content), kind=kind, kp_entity=kp))
        if kp is not None:
            if kp in kp_order:
                errors.append('duplicate_kp_stage')
            if str(kp) not in kp_by_entity:
                errors.append('kp_outside_topic_export')
            kp_order.append(kp)
        current = ref(step.get(':step/next'))
    if set(steps) != seen:
        errors.append('unreachable_owned_steps')
    return dict(activity_entity=activity[':db/id'], activity_uuid=activity.get(':activity/id'),
        activity_math_academy_id=activity.get(':activity/math-academy-id'),
        title=activity.get(':activity/title'), topic_id=str(activity.get(':activity/scope', {}).get(':topic/math-academy-id')),
        ordered_steps=order, ordered_kp_entities=kp_order, complete=not errors and bool(kp_order), errors=errors)


def normalize(raw, selection):
    kps, topics, questions = {}, {}, {}
    pool_sources = {}
    for kp, q, source in raw['pool_sources']:
        pool_sources.setdefault((kp, q), set()).add(str(source))
    for topic in raw['topics']:
        mid = str(topic[':topic/math-academy-id'])
        topics[mid] = dict(entity=topic[':db/id'], id=mid, title=topic.get(':topic/title'),
            kp_entities=sorted(p[':db/id'] for p in topic.get(':topic/knowledge-points', [])), routes=[])
        for kp in topic.get(':topic/knowledge-points', []):
            eid = kp[':db/id']
            if str(eid) not in kps:
                pool = kp.get(':knowledge-point/questions', [])
                permanent = [q for q in pool if re.fullmatch(r'q-\d+', q.get(':question/math-academy-id', ''))]
                ma = [q for q in permanent if ':org/Math-Academy' in pool_sources.get((eid, q[':db/id']), set())]
                kps[str(eid)] = dict(entity=eid, uuid=kp.get(':knowledge-point/id'), title=kp.get(':knowledge-point/title'),
                    canonical_example_id=kp.get(':knowledge-point/canonical-example', {}).get(':question/math-academy-id'),
                    canonical_example_entity=ref(kp.get(':knowledge-point/canonical-example')),
                    topic_ids=[], pool_count_all=len(pool), pool_count_permanent=len(permanent),
                    pool_count_ma_attributed=len(ma), pool_ids=sorted(q[':question/math-academy-id'] for q in permanent),
                    pool_ma_attributed_ids=sorted(q[':question/math-academy-id'] for q in ma),
                    pool_completeness='captured subset; complete Math Academy question bank not established')
            kps[str(eid)]['topic_ids'].append(mid)
    for activity in raw['activities']:
        route = ordered_route(activity, kps)
        topic = topics.get(route['topic_id'])
        if topic:
            topic['routes'].append(route)
    for topic in topics.values():
        topic['routes'].sort(key=lambda r: r['activity_entity'])
        variants = {tuple(r['ordered_kp_entities']) for r in topic['routes'] if r['complete']}
        topic['order_status'] = 'unique' if len(variants) == 1 else 'conflicting' if len(variants) > 1 else 'missing_or_invalid'
        topic['ordered_kp_entities'] = list(next(iter(variants))) if len(variants) == 1 else None
        if topic['ordered_kp_entities'] is not None:
            topic['unsequenced_kp_entities'] = sorted(set(topic['kp_entities']) - set(topic['ordered_kp_entities']))
    sources = {}
    for kp, q, source in raw['membership_sources']:
        sources.setdefault((kp, q), set()).add(str(source))
    for q in raw['questions']:
        mid = q[':question/math-academy-id']
        questions[mid] = dict(entity=q[':db/id'], id=mid, uuid=q.get(':question/id'), memberships=[])
        for attr, role in ((':knowledge-point/_questions', 'practice'), (':knowledge-point/_canonical-example', 'canonical_example')):
            for kp in q.get(attr, []):
                eid = ref(kp)
                questions[mid]['memberships'].append(dict(kp_entity=eid, role=role,
                    sources=sorted(sources.get((eid, q[':db/id']), set())),
                    topic_ids=kps.get(str(eid), {}).get('topic_ids', [])))
        questions[mid]['memberships'].sort(key=lambda m: (m['kp_entity'], m['role']))
    requested = {q['question_id'] for t in selection for q in t['questions'] if q['question_id']}
    for mid in sorted(requested - questions.keys()):
        questions[mid] = dict(id=mid, entity=None, memberships=[], status='not_found_at_basis')
    courses = {str(c[':course/math-academy-id']):dict(entity=c[':db/id'], id=str(c[':course/math-academy-id']),
        title=c.get(':course/title')) for c in raw['courses'] if ':course/math-academy-id' in c}
    return dict(identity=raw['identity'], created_at=datetime.now(timezone.utc).isoformat(),
        questions=questions, topics=topics, kps=kps, courses=courses,
        summary=dict(tasks=len(selection), source_question_records=sum(len(t['questions']) for t in selection),
            unique_source_questions=len(requested), database_questions_found=sum(q['entity'] is not None for q in questions.values()),
            topics=len(topics), kps=len(kps), topic_order_status=dict(Counter(t['order_status'] for t in topics.values())),
            multiple_membership_questions=[q['id'] for q in questions.values() if len(q['memberships']) > 1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', default='reference/mathacademy/assessment-kp-position-analysis-2026-10-16/database')
    parser.add_argument('--basis', type=int)
    parser.add_argument('--reuse-export', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    directory = root / args.directory
    directory.mkdir(parents=True, exist_ok=True)
    if args.reuse_export:
        selection = json.loads((directory / 'selection.json').read_text())
        raw = json.loads((directory / 'raw-projections.json').read_text())
    else:
        selection = select(root)
        dump(directory / 'selection.json', selection)
        raw = read_database(EDBClient(Config(capture_only=True), threading.Event()), directory, selection, args.basis)
    mapping = normalize(raw, selection)
    dump(directory / 'mapping.json', mapping)
    print(json.dumps(mapping['summary'], indent=2))


if __name__ == '__main__':
    main()
