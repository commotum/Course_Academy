#!/usr/bin/env python3
"""Prepare source-separated learner history; this script never transacts."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
from uuid import UUID

from migrate_learner_history import connection, dumps, loads, kw, refs, Tagged, json_write

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'reference/edb-math/imports/learner-history/2026-10-11'
OUT = ROOT / 'reference/edb-math/imports/learner-history/2026-10-11-separated'
AUTHORED = ROOT / 'reference/edb-math/imports/authored-answer-fields/2026-10-11'
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
OLD_BASIS = 2892
BASELINE_BASIS = 74


def read_edn(path):
    return loads('\n'.join(line for line in path.read_text().splitlines()
                           if not line.lstrip().startswith(';')))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    db = connection()
    basis = db.basis()
    schema_rows = db.query('[:find ?a ?type ?card :where [?e :db/ident ?a] '
                          '[?e :db/valueType ?t] [?t :db/ident ?type] '
                          '[?e :db/cardinality ?c] [?c :db/ident ?card]]',
                          [], OUT / 'new', 'schema', basis)
    schema = {str(a): (str(t), str(c)) for a, t, c in schema_rows}
    unique_rows = db.query('[:find ?a :where [?e :db/ident ?a] [?e :db/unique _]]',
                           [], OUT / 'new', 'unique-attributes', basis)
    unique = {str(row[0]) for row in unique_rows}
    sources = db.query('[:find ?ident ?e :in $ [?ident ...] :where [?e :db/ident ?ident]]',
                       [[kw(x) for x in ['org/Math-Academy', 'application/ca-engine',
                                         'person/jake', 'agent/gpt-6.1-sol-high']]],
                       OUT / 'new', 'source-identities', basis)
    sources = {str(ident): eid for ident, eid in sources}
    assert len(sources) == 4, ('missing transaction sources', sources)
    learner_ref = [kw('learner/id'), LEARNER]
    learner_rows = db.query('[:find (pull ?e [:db/id :learner/id :learner/course '
                           ':learner/activity :learner/knowledge-profile :learner/performance]) '
                           ':in $ ?id :where [?e :learner/id ?id]]',
                           [LEARNER], OUT / 'new', 'destination-learner', basis)
    assert len(learner_rows) == 1
    target = learner_rows[0][0]
    assert not any(target.get(a) for a in [':learner/activity', ':learner/knowledge-profile',
                                          ':learner/performance', ':learner/course']), target
    reviewed = json.loads((ARCHIVE / 'supplemental-mapping.json').read_text())['answer_maps']
    question_ids = sorted({r['question_ma_id'] for r in reviewed.values()})
    response_pattern = ('[:db/id :question/id :question/math-academy-id :question/problem '
                        '{:question/answer-fields [:db/id :answer-field/id :answer-field/key '
                        '{:answer-field/type [:db/id :db/ident]} '
                        '{:answer-field/choices [:db/id :answer/id :answer/value '
                        '{:answer/type [:db/id :db/ident]}]} '
                        '{:answer-field/correct [:db/id :answer/id :answer/value]}]}]')
    db.query('[:find ?id (pull ?e ' + response_pattern + ') :in $ [?id ...] '
             ':where [?e :question/math-academy-id ?id]]',
             [question_ids], OUT / 'new', 'response-questions', basis)

    owned = {r[':db/id']: r for r in read_edn(ARCHIVE / 'source-records.edn')}
    cache = {}
    for folder in [ARCHIVE / 'old', OUT / 'old']:
        for path in sorted(folder.glob('*.edn')):
            if path.name.endswith(('-query.edn', '-inputs.edn')) or 'history' in path.name:
                continue
            for row in read_edn(path):
                if isinstance(row, list):
                    for r in row:
                        if isinstance(r, dict) and ':db/id' in r:
                            cache[r[':db/id']] = r
    cache.update(owned)
    old_learner = next(r for r in cache.values() if r.get(':learner/id') == LEARNER)
    baseline = {r[':db/id']: r for r in read_edn(OUT / 'baseline-records.edn')}
    expected = json.loads((ROOT / '.local/edb/learner-profile-import/expected.json').read_text())
    expected = {r['progress_id']: r for r in expected['topics']}
    assert len(baseline) == len(expected) == 1039
    for r in baseline.values():
        assert set(r) == {':db/id', ':progress/id', ':progress/topic', ':progress/repetitions'}
        e = expected[r[':progress/id']]
        assert r[':progress/repetitions'] == e['repetitions']
        topic = cache[refs(r[':progress/topic'])[0]]
        assert str(topic[':topic/id']) == e['topic_id']
        assert topic[':topic/math-academy-id'] == e['source_id']

    progress = {e: r for e, r in owned.items() if ':progress/id' in r}
    tasks = {e: r for e, r in owned.items() if ':learner-task/id' in r}
    items = {e: r for e, r in owned.items() if ':task-item/id' in r}
    topics = {e: r for e, r in owned.items() if ':topic/id' in r}
    policies = {e: r for e, r in owned.items() if ':policy/id' in r}
    performance = {e: r for e, r in owned.items() if any(a.startswith(':performance/') for a in r)}
    assert (len(progress), len(tasks), len(items), len(topics), len(policies), len(performance)) == (1041, 10, 88, 6, 1, 1)
    policy_eid, policy = next(iter(policies.items()))
    weights = policy[':policy/question-selection-weights']
    assert len(weights) == 2
    for weight in weights:
        cache[weight[':db/id']] = weight

    def scalar(a, value):
        typ, _ = schema[a]
        if typ == ':db.type/uuid':
            return UUID(str(value))
        if typ == ':db.type/instant':
            return Tagged('inst', value)
        return value

    # Each identity is stable across files. Existing entities use unique lookup refs.
    identities = {}
    for e, r in cache.items():
        if ':db/ident' in r:
            identities[e] = kw(r[':db/ident'])
        elif ':question/math-academy-id' in r:
            identities[e] = [kw('question/math-academy-id'), r[':question/math-academy-id']]
        else:
            attrs = [a for a in r if a in unique and a.endswith('/id')]
            if len(attrs) == 1:
                a = attrs[0]
                identities[e] = [kw(a), scalar(a, r[a])]
    for group in [topics, progress, tasks, items, policies]:
        for e, r in group.items():
            a = next(a for a in r if a in unique and a.endswith('/id'))
            identities[e] = [kw(a), scalar(a, r[a])]
    identities[old_learner[':db/id']] = learner_ref

    local_refs = {}

    def reference(e):
        assert e in identities, ('unmapped reference', e, cache.get(e))
        return local_refs.get(e, identities[e])

    def translate(a, value):
        typ, card = schema[a]
        if typ != ':db.type/ref':
            return scalar(a, value)
        mapped = [reference(e) for e in refs(value)]
        return mapped if card == ':db.cardinality/many' else mapped[0]

    def form(r, entity=None, exclude=(), ensure=None):
        result = {kw('db/id'): entity if entity is not None else reference(r[':db/id'])}
        for a, value in r.items():
            if a != ':db/id' and a not in exclude:
                assert a in schema, ('attribute not in current schema', a)
                result[kw(a)] = translate(a, value)
        if ensure:
            result[kw('db/ensure')] = kw(ensure)
        return result

    # Assert that all referenced shared identities exist, except these six sparse topics.
    shared = set()
    for group in [progress, tasks, items, policies]:
        for r in group.values():
            for a, v in r.items():
                if a != ':db/id' and a in schema and schema[a][0] == ':db.type/ref':
                    if a in [':task-item/responses', ':policy/question-selection-weights']:
                        continue
                    shared.update(refs(v))
    shared.update(refs(old_learner[':learner/course']))
    created = set(topics) | set(progress) | set(tasks) | set(items) | set(policies)
    grouped = defaultdict(list)
    for e in sorted(shared - created):
        ref = reference(e)
        if isinstance(ref, list):
            grouped[str(ref[0])].append((e, ref[1]))
        else:
            grouped[':db/ident'].append((e, ref))
    for a, values in grouped.items():
        found = set()
        for offset in range(0, len(values), 150):
            chunk = values[offset:offset + 150]
            rows = db.query('[:find ?v ?e :in $ [?v ...] :where [?e ' + a + ' ?v]]',
                            [[v for _, v in chunk]], OUT / 'new',
                            'dependencies-' + a[1:].replace('/', '-') + '-' + str(offset), basis)
            found.update(v for v, _ in rows)
        assert found == {v for _, v in values}, ('missing shared dependencies', a, {str(v) for _, v in values if v not in found})
    for a, group in [(':topic/id', topics), (':topic/math-academy-id', topics),
                     (':progress/id', progress), (':learner-task/id', tasks),
                     (':task-item/id', items), (':policy/id', policies)]:
        values = [scalar(a, r[a]) for r in group.values()]
        rows = db.query('[:find ?v ?e :in $ [?v ...] :where [?e ' + a + ' ?v]]',
                        [values], OUT / 'new', 'collisions-' + a[1:].replace('/', '-'), basis)
        assert not rows, ('destination identity collision', a, rows)

    stages = []

    def save(filename, forms, source, description, **extra):
        header = f';; {description}\n;; Transaction source: {source} (supply once via --source).\n;; Prepared only; do not transact without the user\'s go-ahead.\n'
        text = header + '[\n' + '\n'.join(' ' + dumps(f) for f in forms) + '\n]\n'
        path = OUT / filename
        path.write_text(text)
        # The codec reads instants as strings; normalize that representation only.
        def normalized(value):
            if isinstance(value, Tagged):
                assert value.tag == 'inst'
                return value.value
            if isinstance(value, dict):
                return {k: normalized(v) for k, v in value.items()}
            if isinstance(value, list):
                return [normalized(v) for v in value]
            return value
        assert read_edn(path) == normalized(forms)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        stage = {'file': filename, 'source': source, 'source_eid': sources[source],
                 'sha256': digest, 'request_key': 'learner-history-' + digest,
                 'description': description, **extra}
        stages.append(stage)

    topic_forms = [form(r, f'missing-topic-{r[":topic/math-academy-id"]}', ensure='topic/identity-validate')
                   for _, r in sorted(topics.items())]
    save('01-missing-topics.edn', topic_forms, ':org/Math-Academy',
         'Six original sparse topic records; preserve original UUIDs, MA IDs, and titles.', topics=6)

    baseline_forms = []
    for e, r in sorted(baseline.items()):
        baseline_forms.append(form(r, f'baseline-{e}'))
    baseline_forms.append({kw('db/id'): learner_ref,
                           kw('learner/knowledge-profile'): [f'baseline-{e}' for e in sorted(baseline)],
                           kw('db/ensure'): kw('learner/validate')})
    save('02-color-baseline.edn', baseline_forms, ':application/ca-engine',
         'Original 1,039 records at old basis 74; preserve imported color-derived repetitions without initializing retention.',
         progress_records=1039, original_basis=74)

    weight_forms = []
    for weight in weights:
        weight_forms.append(form(weight, f'policy-weight-{weight[":db/id"]}', ensure='question-weights/validate'))
    policy_form = form(policy, f'policy-{policy_eid}', exclude=[':policy/question-selection-weights'], ensure='policy/validate')
    policy_form[kw('policy/question-selection-weights')] = [f'policy-weight-{r[":db/id"]}' for r in weights]
    save('03-engine-configuration.edn', weight_forms + [policy_form], ':application/ca-engine',
         'Original FIRe policy and its two owned question-selection weight records.', policies=1, question_weight_records=2)

    # Newly authored content is a prerequisite with its own actual author source.
    current_questions = {row[0]: row[1] for row in read_edn(OUT / 'new/response-questions.edn')}
    content_prerequisites = []
    for question in ['q-96676', 'q-11914']:
        path = AUTHORED / (question + '.edn')
        assert ':agent/gpt-6.1-sol-high' in path.read_text()
        expected_fields = [r for r in read_edn(path) if ':answer-field/id' in r]
        actual_fields = current_questions[question].get(':question/answer-fields', [])
        if actual_fields:
            assert {f[':answer-field/id'] for f in actual_fields} == {f[':answer-field/id'] for f in expected_fields}
            expected_answers = {r[':db/id']: r for r in read_edn(path) if ':answer/id' in r}
            for expected_field in expected_fields:
                actual = next(f for f in actual_fields if f[':answer-field/id'] == expected_field[':answer-field/id'])
                assert actual[':answer-field/key'] == expected_field[':answer-field/key']
                assert actual[':answer-field/type'][':db/ident'] == expected_field[':answer-field/type']
                assert actual[':answer-field/correct'][':answer/id'] == expected_answers[expected_field[':answer-field/correct']][':answer/id']
                assert {a[':answer/id']: a[':answer/value'] for a in actual[':answer-field/choices']} == {
                    expected_answers[a][':answer/id']: expected_answers[a][':answer/value'] for a in expected_field[':answer-field/choices']}
            content_prerequisites.append({'question': question, 'already_present': True, 'verified_basis': basis,
                                           'field_ids': [str(f[':answer-field/id']) for f in actual_fields]})
            continue
        stages.append({'file': '../../authored-answer-fields/2026-10-11/' + path.name,
                       'source': ':agent/gpt-6.1-sol-high', 'source_eid': sources[':agent/gpt-6.1-sol-high'],
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'request_key': 'authored-answer-fields-' + hashlib.sha256(path.read_bytes()).hexdigest(),
                       'description': 'Newly authored answer fields; required before migrating these responses.'})

    updated = {e: r for e, r in progress.items() if e not in baseline or r != baseline[e]}
    assert len(updated) == 8 and len(set(progress) - set(baseline)) == 2
    local_refs.update({e: f'task-{e}' for e in tasks})
    local_refs.update({e: f'item-{e}' for e in items})
    local_refs.update({e: f'new-progress-{e}' for e in set(progress) - set(baseline)})
    engine_forms = []
    for e, r in sorted(updated.items()):
        engine_forms.append(form(r, reference(e) if e in baseline else f'new-progress-{e}', ensure='progress/validate'))
    for e, r in sorted(tasks.items()):
        engine_forms.append(form(r, f'task-{e}', ensure='learner-task/validate'))
    for e, r in sorted(items.items()):
        engine_forms.append(form(r, f'item-{e}', exclude=[':task-item/responses'], ensure='task-item/validate'))
    perf_eid, perf = next(iter(performance.items()))
    engine_forms.append(form(perf, f'performance-{perf_eid}', ensure='performance/validate'))
    engine_forms.append({kw('db/id'): learner_ref,
                         kw('learner/knowledge-profile'): [f'new-progress-{e}' for e in sorted(set(progress) - set(baseline))],
                         kw('learner/activity'): [f'task-{e}' for e in sorted(tasks)],
                         kw('learner/performance'): f'performance-{perf_eid}',
                         kw('db/ensure'): kw('learner/validate')})
    changed_attrs = sorted({a for e, r in updated.items() if e in baseline
                            for a, v in r.items() if a != ':db/id' and a in baseline[e] and v != baseline[e][a]})
    save('04-engine-activity.edn', engine_forms, ':application/ca-engine',
         'Later progress, ten lesson attempts, 88 presentations, original judgments, durations, XP, and overall performance.',
         allow_retractions=changed_attrs, updated_baseline_records=6, additional_progress_records=2,
         lesson_tasks=10, presentation_records=88)
    local_refs.clear()

    old_answers = {r[0][':db/id']: r[0] for r in read_edn(OUT / 'old/all-saved-answers.edn')}
    authored_forms = {q: read_edn(AUTHORED / (q + '.edn')) for q in ['q-96676', 'q-11914']}
    authored_answers = {q: {r[':db/id']: r for r in fs if ':answer/id' in r} for q, fs in authored_forms.items()}
    authored_fields = {q: [r for r in fs if ':answer-field/id' in r] for q, fs in authored_forms.items()}
    response_forms, response_audit, entered = [], [], set()
    entered_tempids = {}
    for e, item in sorted(items.items()):
        saved = refs(item.get(':task-item/responses', []))
        if not saved:
            continue
        assert len(saved) == 1, ('unexpected old response cardinality', e, saved)
        answer_eid = saved[0]
        answer = old_answers[answer_eid]
        reconciliation = reviewed[str(answer_eid)]
        question = reconciliation['question_ma_id']
        destination_answers = []
        if question in authored_fields:
            old_q = cache[refs(item[':task-item/content'])[0]]
            old_field = old_q[':question/answer-fields'][0]
            assert answer_eid == refs(old_field[':answer-field/correct'])[0]
            assert cache[refs(item[':task-item/status'])[0]][':db/ident'] == kw('task-item.status/correct')
            if question == 'q-96676':
                assert answer[':answer/value'] == 'II and III only'
                expected_values = {'I': 'false', 'II': 'true', 'III': 'true', 'None': 'false'}
                for field in authored_fields[question]:
                    selected = authored_answers[question][field[':answer-field/correct']]
                    assert selected[':answer/value'] == expected_values[field[':answer-field/key']]
                    destination_answers.append([kw('answer/id'), selected[':answer/id']])
                reason = 'Original explicit selection II and III only maps to I=false, II=true, III=true, None=false.'
            else:
                field = authored_fields[question][0]
                selected = authored_answers[question][field[':answer-field/correct']]
                assert answer[':answer/value'] == selected[':answer/value']
                destination_answers.append([kw('answer/id'), selected[':answer/id']])
                reason = 'Original selected correct derivative exactly matches the new radio answer.'
        else:
            current = current_questions[question]
            field_id = UUID(reconciliation['new_field_id'])
            fields = [f for f in current[':question/answer-fields'] if f[':answer-field/id'] == field_id]
            assert len(fields) == 1, ('current field changed', question, field_id)
            field = fields[0]
            if reconciliation['action'] == 'create_answer':
                assert str(field[':answer-field/type'][':db/ident']) == ':answer-field.type/blank'
                assert str(answer[':answer/id']) == reconciliation['old_answer_id']
                assert answer[':answer/value'] == reconciliation['answer_value']
                answer_ref = [kw('answer/id'), scalar(':answer/id', answer[':answer/id'])]
                choices = field[':answer-field/choices']
                assert all(c[':answer/id'] != answer_ref[1] and c[':answer/value'] != answer[':answer/value'] for c in choices)
                identities[answer_eid] = answer_ref
                entered_tempids[str(answer_ref[1])] = f'entered-answer-{answer_eid}'
                if answer_eid not in entered:
                    response_forms.append(form(answer, f'entered-answer-{answer_eid}', ensure='answer/validate'))
                    response_forms.append([kw('db/add'), [kw('answer-field/id'), field_id], kw('answer-field/choices'), f'entered-answer-{answer_eid}'])
                    response_forms.append([kw('db/ensure'), [kw('answer-field/id'), field_id], kw('answer-field/validate')])
                    entered.add(answer_eid)
                destination_answers.append(answer_ref)
                reason = 'Preserved verbatim learner-entered answer and original answer UUID; attached to the corresponding current blank field.'
            else:
                assert reconciliation['action'] == 'reuse_answer'
                selected_id = UUID(reconciliation['new_answer_id'])
                selected = [a for a in field[':answer-field/choices'] if a[':answer/id'] == selected_id]
                assert len(selected) == 1, ('saved selection missing from current bank', question, selected_id)
                if 'new_answer_value' in reconciliation:
                    assert selected[0][':answer/value'] == reconciliation['new_answer_value']
                elif reconciliation.get('reason') == 'stable UUID':
                    assert selected[0][':answer/value'] == answer[':answer/value']
                destination_answers.append([kw('answer/id'), selected_id])
                reason = reconciliation.get('reason', 'Reviewed current-field answer identity mapping.')
        response_forms.append({kw('db/id'): reference(e),
                               kw('task-item/responses'): [entered_tempids.get(str(ref[1]), ref) for ref in destination_answers],
                               kw('db/ensure'): kw('task-item/validate')})
        response_audit.append({'item_id': str(item[':task-item/id']), 'question': question,
                               'old_answer_id': str(answer[':answer/id']), 'old_answer_value': answer[':answer/value'],
                               'new_answer_ids': [str(ref[1]) for ref in destination_answers], 'reason': reason})
    assert len(entered) == 7 and len(response_audit) == 44
    assert sum(len(r['new_answer_ids']) for r in response_audit) == 47
    response_forms.append({kw('db/id'): learner_ref, kw('learner/course'): reference(refs(old_learner[':learner/course'])[0]),
                           kw('db/ensure'): kw('learner/validate')})
    save('05-jake-responses-and-course.edn', response_forms, ':person/jake',
         'Seven verbatim entered answers, all 44 saved submissions mapped to current fields (47 answer references), and saved course choice.',
         entered_answer_records=7, saved_submissions=44, answer_references=47)
    json_write(OUT / 'response-mapping.json', response_audit)
    summary = {'missing_topics': 6, 'baseline_progress': 1039, 'updated_baseline_records': 6,
               'new_progress_records': 2, 'final_progress': 1041, 'policies': 1, 'question_weights': 2,
               'completed_lessons': 4, 'paused_lessons': 6, 'presentations': 88, 'saved_submissions': 44,
               'answer_references': 47, 'entered_answers': 7, 'correct': 40, 'incorrect': 4,
               'xp': sum(r.get(':learner-task/xp-earned', 0) for r in tasks.values()),
               'seconds': sum(r[':learner-task/elapsed-seconds'] for r in tasks.values()),
               'explicit_progress_instants': sum(schema[a][0] == ':db.type/instant' for r in progress.values() for a in r if a != ':db/id')}
    assert summary['xp'] == 37 and abs(summary['seconds'] - 8344.367) < 1e-6 and summary['explicit_progress_instants'] == 16
    manifest = {'committed': False, 'source_database': 'course-academy-v2', 'source_basis': OLD_BASIS,
                'original_baseline_basis': BASELINE_BASIS, 'destination_database': 'math', 'destination_basis': basis,
                'learner': LEARNER, 'transactions': stages, 'content_prerequisites': content_prerequisites,
                'summary': summary,
                'timing': 'Preserve all 16 explicit progress instants and saved durations. Original lifecycle and intermediate progress transaction times are archived, not backdated into the destination. Destination transaction times will be import times.',
                'identity_note': 'Original domain UUID/string identities are preserved for topics, progress, policy, tasks, items, and entered answers. Numeric EIDs are database-local and are not copied.',
                'excluded': ['470 local request journals', 'untouched task queue', 'old paused assignment', 'legacy answer fields and their banks']}
    json_write(OUT / 'manifest.json', manifest)
    json_write(OUT / 'baseline-verification.json', {'original_basis': 74, 'records': 1039,
                'exact_original_import_match': True, 'repetition_distribution': dict(Counter(str(r[':progress/repetitions']) for r in baseline.values())),
                'retention_initialization_added': False, 'verification_source': '.local/edb/learner-profile-import/expected.json'})
    assert db.basis() == basis, 'Destination advanced during preparation; reprepare before previewing.'
    print(json.dumps({'destination_basis': basis, **summary}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except __import__('subprocess').CalledProcessError as error:
        print(error.stderr, file=sys.stderr)
        raise
