#!/usr/bin/env python3
"""Repair historical multistep containment, or withdraw source-incomplete parts.

Default: save a guarded preview. --apply commits the frozen intent, then verifies
at its exact resulting basis. Never creates learner tasks or changes answers.
"""
import argparse
import hashlib
import json
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw

DEFAULT_OUT = ROOT / 'reference/edb-math/repairs/2026-10-22-multistep-context'
SOURCE = ':agent/gpt-6.1-sol-high'
PATTERN = '''[* {:step/_content [:db/id {:multistep/_steps [:db/id :multistep/context]}]}
 {:knowledge-point/_questions [:db/id {:topic/_knowledge-points [:db/id]}]}]'''


def save(path, value):
    path.write_text(json.dumps(value, default=str, indent=2) + '\n')


def identity(kind, task):
    # The historical task ID identifies this local recovery, not an MA content ID.
    return uuid.uuid5(uuid.NAMESPACE_URL, f'course-academy:recovered-history:{task}:{kind}')


def containment(question):
    return [step for step in question.get(':step/_content', []) if step.get(':multistep/_steps')]


def discover(history):
    result = []
    for path in sorted(history.glob('*.json')):
        record = json.loads(path.read_text())
        if not isinstance(record, dict):
            continue
        if not record.get('task_text', '').strip().startswith('Multistep\n'):
            continue
        questions = record['questions']
        ordinals = [q['ordinal'] for q in questions]
        if ordinals != list(range(1, len(questions) + 1)):
            raise ValueError('Historical parts are not in complete source order: ' + str(path))
        ids = [q['id'].replace('question-', 'q-') for q in questions]
        if len(set(ids)) != len(ids):
            raise ValueError('Repeated historical part: ' + str(path))
        result.append({'task_id': str(record['task_id']),
                       'title': record['task_text'].strip().splitlines()[2],
                       'source_file': str(path.relative_to(ROOT)),
                       'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'questions': ids})
    return result


def read_questions(db, tasks, out, name, basis):
    ids = sorted({q for task in tasks for q in task['questions']})
    rows = db.query('[:find (pull ?q ' + PATTERN + ') :in $ [?id ...] '
                    ':where [?q :question/math-academy-id ?id]]', [ids], out, name, basis)
    result = {q[0][':question/math-academy-id']: q[0] for q in rows}
    if set(result) != set(ids):
        raise ValueError('Historical questions missing; do not invent source content')
    return result


def forms_for(tasks, questions, contexts):
    forms, restored, withdrawn, existing = [], [], [], []
    for task in tasks:
        tid = task['task_id']
        parts = [questions[mid] for mid in task['questions']]
        placed = [bool(containment(q)) for q in parts]
        if all(placed):
            existing.append(tid)
            continue
        if any(placed):
            raise ValueError('Partially placed activity requires explicit reconciliation: ' + tid)
        if tid not in contexts:
            for question in parts:
                if question.get(':question/retired') is not True:
                    forms.append([kw('db/add'), question[':db/id'], kw('question/retired'), True])
            withdrawn.append({**task, 'reason': 'Original shared graphs/setup are absent from retained history; no substitute variant is inferred.'})
            continue
        context = contexts[tid]['context']
        if not context.strip() or not set(contexts[tid]['evidence_questions']) <= set(task['questions']):
            raise ValueError('Context review does not match its source activity')
        steps = [f'history-{tid}-step-{i}' for i in range(len(parts))]
        for i, (step, question) in enumerate(zip(steps, parts)):
            form = {kw('db/id'): step, kw('step/id'): identity(f'step-{i}', tid),
                    kw('step/content'): question[':db/id'], kw('db/ensure'): kw('step/validate')}
            if i + 1 < len(steps):
                form[kw('step/next')] = steps[i + 1]
            forms.append(form)
            # Only remove retirement added by the current-session emergency repair.
            if tid == '13408988' and question.get(':question/retired') is True:
                forms.append([kw('db/retract'), question[':db/id'], kw('question/retired'), True])
        multi, problem, outer, activity = [f'history-{tid}-{kind}' for kind in ('multistep', 'problem', 'outer', 'activity')]
        topics = sorted({t[':db/id'] for q in parts for kp in q.get(':knowledge-point/_questions', [])
                         for t in kp.get(':topic/_knowledge-points', [])})
        forms.extend([
            {kw('db/id'): multi, kw('multistep/id'): identity('multistep', tid),
             kw('multistep/context'): context, kw('multistep/steps'): steps,
             kw('multistep/first-step'): steps[0], kw('db/ensure'): kw('multistep/validate')},
            {kw('db/id'): problem, kw('assigned-problem/id'): identity('problem', tid),
             kw('assigned-problem/content'): multi, kw('assigned-problem/topic-coverage'): topics,
             kw('db/ensure'): kw('assigned-problem/validate')},
            {kw('db/id'): outer, kw('step/id'): identity('outer', tid), kw('step/content'): problem,
             kw('db/ensure'): kw('step/validate')},
            {kw('db/id'): activity, kw('activity/id'): identity('activity', tid),
             kw('activity/title'): task['title'], kw('activity/type'): kw('activity.type/assignment'),
             kw('activity/steps'): [outer], kw('activity/first-step'): outer,
             kw('db/ensure'): kw('activity/validate')},
        ])
        restored.append({**task, 'activity_uuid': str(identity('activity', tid)), 'context': contexts[tid]})
    return forms, {'restored': restored, 'withdrawn': withdrawn, 'existing': existing}


def verify(db, out, receipt, intent):
    basis = receipt[':edb/db-after-t']
    questions = read_questions(db, intent['tasks'], out, 'questions-after', basis)
    before_rows = loads((out / 'questions-before.edn').read_text())
    before = {r[0][':question/math-academy-id']: r[0] for r in before_rows}
    for mid, q in questions.items():
        assert containment(q) or q.get(':question/retired') is True, mid
        exclude = {':step/_content', ':question/retired'}
        assert {k:v for k,v in q.items() if k not in exclude} == {
            k:v for k,v in before[mid].items() if k not in exclude}, ('changed question content or KP', mid)
    activity_pattern = '''[:db/id :activity/id :activity/first-step
      {:activity/steps [:db/id :step/id {:step/content [:db/id
        {:assigned-problem/content [:db/id :multistep/context :multistep/first-step
          {:multistep/steps [:db/id :step/next {:step/content [:db/id :question/math-academy-id]}]}]}]}]}]'''
    activities = []
    for task in intent['summary']['restored']:
        rows = db.query('[:find (pull ?a '+activity_pattern+') :in $ ?id :where [?a :activity/id ?id]]',
                        [uuid.UUID(task['activity_uuid'])], out, 'activity-after-'+task['task_id'], basis)
        a = rows[0][0]; outer = a[':activity/steps']
        assert len(outer) == 1 and a[':activity/first-step'][':db/id'] == outer[0][':db/id']
        m = outer[0][':step/content'][':assigned-problem/content']
        assert m[':multistep/context'] == task['context']['context']
        steps = {s[':db/id']:s for s in m[':multistep/steps']}
        cursor, ordered, visited = m[':multistep/first-step'][':db/id'], [], set()
        while cursor is not None:
            assert cursor in steps and cursor not in visited
            visited.add(cursor); step = steps[cursor]
            ordered.append(step[':step/content'][':question/math-academy-id'])
            cursor = step.get(':step/next', {}).get(':db/id')
        assert visited == set(steps) and ordered == task['questions']
        assert outer[0][':db/id'] not in steps
        activities.append({'task_id':task['task_id'], 'activity_eid':a[':db/id'], 'part_count':len(ordered)})
    attrs = dict(db.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], out, 'attribute-idents', basis))
    allowed = {'db/txInstant', 'question/retired'}
    allowed_prefixes = ('activity/', 'step/', 'multistep/', 'assigned-problem/')
    for _, attr, *_ in receipt[':edb/tx-data']:
        name = str(attrs[attr]).lstrip(':')
        assert name in allowed or name.startswith(allowed_prefixes), name
    remaining, _ = forms_for(intent['tasks'], questions, intent['contexts'])
    assert not remaining, 'Repair is not idempotent'
    report = {'basis':basis, 'historical_parts_checked':len(questions),
              'all_excluded_from_standalone_practice':True,
              'structurally_contained':sum(bool(containment(q)) for q in questions.values()),
              'withdrawn_without_source_setup':sum(not containment(q) for q in questions.values()),
              'restored_activities':activities, 'question_content_answers_and_kp_links_unchanged':True,
              'learner_and_progress_facts_unchanged':True, 'reimport_is_noop':True}
    save(out/'verification.json', report)
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args(); out = args.output; out.mkdir(parents=True, exist_ok=True)
    db = Database(SimpleNamespace(edb_bin=str(ROOT.parent/'EDB/target/release/edb'), database='math'))
    intent_file, tx = out/'intent.json', out/'transaction.edn'
    if not intent_file.exists():
        tasks = discover(ROOT/'reference/mathacademy/progress-history-2026-10-04')
        contexts = json.loads((out/'reviewed-contexts.json').read_text())['contexts']
        basis = db.basis()
        assert db.query('[:find ?e :in $ ?ident :where [?e :db/ident ?ident]]', [kw(SOURCE)], out, 'source', basis)
        questions = read_questions(db, tasks, out, 'questions-before', basis)
        forms, summary = forms_for(tasks, questions, contexts)
        tx.write_text(dumps(forms)+'\n')
        preview = db.command('with', '--file', tx, '--source', SOURCE)
        (out/'preview.edn').write_text(preview)
        result = loads(preview)
        assert result[':edb/db-before-t'] == basis and result[':edb/committed'] is False
        intent = {'basis':basis, 'source':SOURCE, 'key':'historical-multistep-repair-'+str(uuid.uuid4()),
                  'sha256':hashlib.sha256(tx.read_bytes()).hexdigest(), 'tasks':tasks,
                  'contexts':contexts, 'summary':summary}
        save(intent_file, intent)
    intent = json.loads(intent_file.read_text())
    assert hashlib.sha256(tx.read_bytes()).hexdigest() == intent['sha256']
    if not args.apply:
        print(json.dumps({'basis':intent['basis'], 'restore_activities':len(intent['summary']['restored']),
                          'withdraw_activities':len(intent['summary']['withdrawn']),
                          'already_structured':len(intent['summary']['existing'])}, indent=2)); return
    receipt_file = out/'receipt.edn'
    if not receipt_file.exists():
        receipt = db.command('transact', '--file', tx, '--source', intent['source'],
                             '--request-key', intent['key'], '--basis', intent['basis'],
                             '--endpoint', '/tmp/edb-math/writer.sock')
        receipt_file.write_text(receipt)
    receipt = loads(receipt_file.read_text())
    assert receipt[':edb/committed'] is True
    verify(db, out, receipt, intent)


if __name__ == '__main__':
    main()
