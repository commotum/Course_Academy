"""Prepare and preview the straightforward finder candidates. No commit command."""
import argparse
import collections
import concurrent.futures
import hashlib
import json
import re
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
OUT = Path(__file__).resolve().parent
AUDIT = ROOT / 'generate/runs/checkbox-audit-2026-10-12/report.json'
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, kw, loads
from core import atomic_json, stable_id

SOURCE = ':agent/gpt-6.1-sol-high'
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'),
    database='math', endpoint='/tmp/edb-math/writer.sock'))
ROMAN = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII')
BLOCKING = {'no_stored_correct_answer_or_worked_solution',
    'no_answer_fields_reconstruct_key_from_worked_solution',
    'duplicate_selection_fields_reconcile_before_migration',
    'normalize_OCR_l_and_ll_to_I_and_II'}
QUESTION = '''[* {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
  {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
  {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM = '[* {:task-item/status [:db/id :db/ident]} {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]}]'
CASE_LINE = re.compile(r'(?m)^([ \t]*)(?:-\s+|[1-9][.)]\s+|(?:IV|III|II|I)[.)]\s+)([^\n]+)$')
GRAPH_IDS = {'q-108581', 'q-108605', 'q-36063', 'q-66510',
             'q-36905', 'q-66508', 'q-66509', 'q-66514'}

def save(name, data):
    atomic_json(OUT / name, data)

def read(query, inputs, name, basis):
    return DB.query(query, inputs, OUT / 'evidence', name, basis)

def batches(query, ids, name, basis, size=16):
    groups = [ids[i:i+size] for i in range(0, len(ids), size)]
    def one(group):
        return read(query, [group], name + '-' + str(group[0]), basis)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        return [row for part in pool.map(one, groups) for row in part]

def capture():
    assert not (OUT / 'commit-intent.json').exists() and not (OUT / 'commit.edn').exists(), 'Resolve the retained submission first'
    audit = json.loads(AUDIT.read_text())
    candidates = [q for kp in audit['direct_candidates'] for q in kp['questions']]
    ids = sorted(q['id'] for q in candidates)
    basis = DB.basis()
    questions = batches('[:find (pull ?q ' + QUESTION + ''') :in $ [?q ...]
        :where [?q :question/id _]]''', ids, 'questions', basis)
    assert {row[0][':db/id'] for row in questions} == set(ids)
    tentative = {q['id'] for q in candidates if not (BLOCKING & set(q['review_flags']))}
    assert len(tentative) == 220
    items = batches('[:find ?q (pull ?item ' + ITEM + ''') :in $ [?q ...]
        :where [?item :task-item/content ?q]]''', sorted(tentative), 'items', basis, 64)
    answers = sorted({a[':db/id'] for row in questions if row[0][':db/id'] in tentative
        for f in row[0].get(':question/answer-fields', [])
        for a in f.get(':answer-field/choices', [])})
    users = batches('[:find ?answer (pull ?item ' + ITEM + ''') :in $ [?answer ...]
        :where [?item :task-item/responses ?answer]]''', answers, 'response-users', basis, 128)
    attrs = DB.attributes(OUT / 'evidence', basis)
    source = read('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',
                  [kw(SOURCE)], 'source', basis)
    assert len(source) == 1 and source[0][0][':db/ident'] == SOURCE
    (OUT / 'snapshot.edn').write_text(dumps({'basis': basis, 'questions': questions,
        'items': items, 'response_users': users, 'attributes': attrs, 'source': source}) + '\n')
    save('capture.json', {'basis': basis, 'audit_basis': audit['basis'],
        'audit_sha256': hashlib.sha256(AUDIT.read_bytes()).hexdigest(),
        'candidate_questions': len(ids), 'tentative_easy_questions': len(tentative),
        'presentations': len(items), 'response_links': len(users), 'source': SOURCE})
    print(json.dumps({'captured': True, 'basis': basis, 'questions': len(ids),
                      'presentations': len(items), 'response_links': len(users)}), flush=True)

def subset(value):
    value = value.strip().rstrip('.').replace('$', '').replace('**', '').strip()
    if re.fullmatch(r'None(?: of (?:the given statements are true|the statements are true|those listed|the listed|these listed))?', value):
        return set()
    found = re.findall(r'\b(?:VIII|VII|VI|IV|III|II|I|[A-Z])\b', value)
    remainder = re.sub(r'\b(?:VIII|VII|VI|IV|III|II|I|[A-Z]|and|only)\b|[,\s]', '', value)
    if not found or remainder or len(found) != len(set(found)):
        raise ValueError('Unambiguous subset required: ' + value)
    return set(found)

def labels_and_prompt(q, field):
    original = q[':question/problem']
    assert 'Select all that apply.' not in original
    lines = list(CASE_LINE.finditer(original))
    universe = set().union(*(subset(a[':answer/value']) for a in field[':answer-field/choices']))
    if lines:
        labels = list(ROMAN[:len(lines)])
        if not 2 <= len(lines) <= 4 or not universe <= set(labels):
            raise ValueError('Listed cases and bank labels disagree')
        counter = iter(labels)
        prompt = CASE_LINE.sub(lambda m: m[1] + '- **' + next(counter) + '.** ' + m[2], original)
        first = prompt.index('- **' + labels[0] + '.** ')
        prompt = prompt[:first].rstrip() + '\n\nSelect all that apply.\n\n' + prompt[first:]
        # The exact list contents and all surrounding mathematical text survive.
        def bare(s):
            s = re.sub(r'(?m)^([ \t]*)- \*\*(?:IV|III|II|I)\.\*\* ', r'\1', s)
            s = CASE_LINE.sub(lambda m: m[1] + m[2], s)
            return re.sub(r'\s+', ' ', s.replace('Select all that apply.', '')).strip()
        assert bare(prompt) == bare(original)
    elif q[':question/math-academy-id'] in GRAPH_IDS:
        # All eight images were inspected: each contains four graphs, including
        # q-36063 and q-36905 whose radio banks never mention IV.
        labels = list(ROMAN[:4])
        assert universe <= set(labels)
        prompt = original.rstrip() + '\n\nSelect all that apply.'
    else:
        labels = re.findall(r'\b([A-Z])\s*=', original)
        if len(labels) != 3 or len(set(labels)) != 3 or universe != set(labels):
            raise ValueError('Named matrix labels require review')
        head, sep, tail = original.partition('\n\n')
        assert sep and '?' in head
        prompt = head + '\n\nSelect all that apply.\n\n' + tail
    return labels, prompt

def plan():
    assert not (OUT / 'commit-intent.json').exists() and not (OUT / 'commit.edn').exists(), 'Resolve the retained submission first'
    snapshot = loads((OUT / 'snapshot.edn').read_text())
    audit = json.loads(AUDIT.read_text())
    original_rows = {q['id']: q for kp in audit['direct_candidates'] for q in kp['questions']}
    questions = {r[0][':db/id']: r[0] for r in snapshot['questions']}
    items_by_question = collections.defaultdict(dict)
    for qid, item in snapshot['items']:
        items_by_question[qid][item[':db/id']] = item
    incoming = collections.defaultdict(dict)
    for aid, item in snapshot['response_users']:
        incoming[aid][item[':db/id']] = item
    forms, converted, mapped, deferred, retained = [], [], [], [], []
    for qid, audit_row in sorted(original_rows.items()):
        flags = sorted(BLOCKING & set(audit_row['review_flags']))
        if flags:
            deferred.append({'id': qid, 'ma_id': audit_row['ma_id'], 'kp': audit_row['kp'], 'reasons': flags})
            continue
        q = questions[qid]
        try:
            fields = q.get(':question/answer-fields', [])
            if len(fields) != 1 or fields[0][':answer-field/type'][':db/ident'] != ':answer-field.type/radio':
                raise ValueError('Current answer-field structure changed')
            f = fields[0]
            if q[':question/problem'] != audit_row['problem']:
                raise ValueError('Prompt changed since audit')
            if q.get(':knowledge-point/_canonical-example'):
                raise ValueError('Practice question also used as a canonical example')
            if audit_row['kp'] not in {k[':db/id'] for k in q.get(':knowledge-point/_questions', [])}:
                raise ValueError('KP membership changed')
            labels, prompt = labels_and_prompt(q, f)
            bank = {a[':db/id']: a for a in f[':answer-field/choices']}
            correct = f[':answer-field/correct']
            if correct[':db/id'] not in bank or bank[correct[':db/id']] != correct:
                raise ValueError('Canonical answer does not match owned bank')
            key = subset(correct[':answer/value'])
            if not key <= set(labels):
                raise ValueError('Correct answer references an unlisted case')
            for a in bank.values():
                if a[':answer/type'][':db/ident'] != ':answer.type/text' or not subset(a[':answer/value']) <= set(labels):
                    raise ValueError('Choice cannot be mapped exactly')
            conclusions = re.findall(r'correct answer is ["“]([^"”]+)["”]', q.get(':question/worked-solution') or '')
            if conclusions and any(subset(c) != key for c in conclusions):
                raise ValueError('Worked solution disagrees with stored key')
            responses = []
            for itemid, item in sorted(items_by_question[qid].items()):
                old = [a[':db/id'] for a in item.get(':task-item/responses', [])]
                if not old:
                    continue
                if len(old) != 1 or old[0] not in bank:
                    raise ValueError('Saved response is not one owned radio choice')
                if incoming[old[0]].get(itemid) != item:
                    raise ValueError('Response capture is inconsistent')
                selected = subset(bank[old[0]][':answer/value'])
                status = item.get(':task-item/status', {}).get(':db/ident')
                if status in (':task-item.status/correct', ':task-item.status/incorrect') and (selected == key) != (status == ':task-item.status/correct'):
                    raise ValueError('Saved grading disagrees with canonical key')
                responses.append({'item': itemid, 'question': qid, 'old_answer': old[0],
                    'old_value': bank[old[0]][':answer/value'], 'selected': [l for l in labels if l in selected], 'status': status})
        except (ValueError, KeyError, TypeError) as error:
            deferred.append({'id': qid, 'ma_id': audit_row['ma_id'], 'kp': audit_row['kp'], 'reasons': [str(error)]})
            continue
        links, targets = [], {}
        for label in labels:
            token = q[':question/math-academy-id'] + '/authored-checkbox-v1/' + label
            fid = 'field-' + token
            aids = []
            for value in ('false', 'true'):
                aid = 'answer-' + token + '/' + value
                forms.append({kw('db/id'): aid, kw('answer/id'): stable_id('answer', token + '/' + value),
                    kw('answer/type'): kw('answer.type/text'), kw('answer/value'): value,
                    kw('db/ensure'): kw('answer/validate')})
                aids.append(aid)
                targets[(label, value)] = aid
            forms.append({kw('db/id'): fid, kw('answer-field/id'): stable_id('field', token),
                kw('answer-field/key'): label, kw('answer-field/type'): kw('answer-field.type/checkbox'),
                kw('answer-field/choices'): aids, kw('answer-field/correct'): aids[int(label in key)],
                kw('db/ensure'): kw('answer-field/validate')})
            links.append(fid)
        retained.extend([f[':db/id'], *bank])
        forms.append([kw('db/retract'), qid, kw('question/answer-fields'), f[':db/id']])
        forms.append([kw('db/cas'), qid, kw('question/problem'), q[':question/problem'], prompt])
        forms.append({kw('db/id'): qid, kw('question/answer-fields'): links, kw('db/ensure'): kw('question/validate')})
        for response in responses:
            answer_tempids = [targets[(l, str(l in response['selected']).lower())] for l in labels]
            forms.append([kw('db/retract'), response['item'], kw('task-item/responses'), response['old_answer']])
            forms.append({kw('db/id'): response['item'], kw('task-item/responses'): answer_tempids,
                kw('db/ensure'): kw('task-item/validate')})
            response['new_answer_tempids'] = answer_tempids
            mapped.append(response)
        converted.append({'id': qid, 'ma_id': q[':question/math-academy-id'], 'kp': audit_row['kp'],
            'kp_title': audit_row['kp_title'], 'labels': labels, 'correct': [l for l in labels if l in key],
            'old_field': f[':db/id'], 'new_field_tempids': links, 'problem_before': q[':question/problem'],
            'problem_after': prompt, 'choice_mapping': [{'old_answer': aid, 'old_value': a[':answer/value'],
                'selected': [l for l in labels if l in subset(a[':answer/value'])],
                'new_answer_tempids': [targets[(l, str(l in subset(a[':answer/value'])).lower())] for l in labels]}
                for aid, a in sorted(bank.items())]})
    assert converted, 'No straightforward candidates remain'
    transaction = OUT / 'transaction.edn'
    transaction.write_text('[\n' + '\n'.join(' ' + dumps(f) for f in forms) + '\n]\n')
    digest = hashlib.sha256(transaction.read_bytes()).hexdigest()
    counts = {'questions': len(converted), 'knowledge_points': len({q['kp'] for q in converted}),
        'new_checkbox_fields': sum(len(q['labels']) for q in converted),
        'new_boolean_answers': 2 * sum(len(q['labels']) for q in converted),
        'saved_responses_mapped': len(mapped), 'presentations': sum(len(items_by_question[q['id']]) for q in converted),
        'direct_candidates_deferred': len(deferred), 'secondary_candidates_deferred': audit['counts']['secondary_questions']}
    save('plan.json', {'basis': snapshot['basis'], 'source': SOURCE, 'transaction_sha256': digest,
        'counts': counts, 'questions': converted, 'responses': mapped, 'deferred': deferred,
        'retained_original_entities': sorted(set(retained)),
        'notes': ['Preserves imported correct subsets, worked solutions, equations, images, KP/topic membership, and all learner grading and progress.',
            'Normalizes text lists to bold Roman labels and adds Select all that apply.; named matrix labels and graph images are preserved.',
            'None maps to every checkbox false; no separate None checkbox is created.',
            'Eight invertible-function images inspected: four cases each even when IV is absent from the radio bank.',
            'New fields and Boolean answers are owned per question; old fields and answer entities and historical facts remain retained.',
            'The prepared request uses a full basis guard and prompt CAS. Refresh capture/plan/preview if the basis advances before submission.']})
    save('prepared-request.json', {'state': 'prepared_not_submitted', 'database': 'math', 'endpoint': DB.args.endpoint,
        'basis': snapshot['basis'], 'source': SOURCE, 'sha256': digest,
        'request_key': 'finder-easy-checkbox-v1-' + str(snapshot['basis']) + '-' + digest,
        'transaction_file': str(transaction), 'must_use_basis_guard': True})
    print(json.dumps({'prepared': True, 'basis': snapshot['basis'], **counts}), flush=True)

def verify_preview(report, committed=False):
    manifest = json.loads((OUT / 'plan.json').read_text())
    snapshot = loads((OUT / 'snapshot.edn').read_text())
    assert report[':edb/committed'] is committed
    if not committed:
        assert report[':edb/speculative'] is True
    assert report[':edb/db-before-t'] == manifest['basis'], 'Database advanced; recapture, replan, and preview'
    assert hashlib.sha256((OUT / 'transaction.edn').read_bytes()).hexdigest() == manifest['transaction_sha256']
    attributes = dict(snapshot['attributes'])
    source_id = snapshot['source'][0][0][':db/id']
    ids = report[':edb/tempids']
    new = set(ids.values())
    assert len(new) == manifest['counts']['new_checkbox_fields'] + manifest['counts']['new_boolean_answers']
    old = set(manifest['retained_original_entities'])
    changes = {q['id']: q for q in manifest['questions']}
    response_changes = {r['item']: r for r in manifest['responses']}
    expected_retractions = {(q['id'], ':question/answer-fields', q['old_field']) for q in changes.values()}
    expected_retractions.update((q['id'], ':question/problem', q['problem_before']) for q in changes.values())
    expected_retractions.update((r['item'], ':task-item/responses', r['old_answer']) for r in response_changes.values())
    actual_retractions = set()
    additions = collections.defaultdict(lambda: collections.defaultdict(set))
    for entity, attribute, value, tx, source, added in report[':edb/tx-data']:
        name = str(attributes[attribute])
        assert source == source_id, 'Unexpected transaction source'
        assert entity not in old, 'Original field or answer was mutated'
        if entity in changes:
            assert name in (':question/problem', ':question/answer-fields')
        elif entity in response_changes:
            assert name == ':task-item/responses'
        elif entity in new:
            assert added and name in {':answer/id', ':answer/type', ':answer/value', ':answer-field/id',
                ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct'}
        else:
            assert name == ':db/txInstant' and added, 'Unrelated entity changed'
        if added:
            additions[entity][name].add(value)
        else:
            actual_retractions.add((entity, name, value))
    assert actual_retractions == expected_retractions
    # Check every field, Boolean bank, key, prompt, question link and response,
    # using preview's own entity IDs rather than treating them as durable IDs.
    enum = {str(v): a for a, v in read('[:find ?e ?ident :in $ [?ident ...] :where [?e :db/ident ?ident]]',
        [[kw('answer-field.type/checkbox'), kw('answer.type/text')]], 'preview-enums', manifest['basis'])}
    for q in manifest['questions']:
        assert additions[q['id']][':question/problem'] == {q['problem_after']}
        assert additions[q['id']][':question/answer-fields'] == {ids[t] for t in q['new_field_tempids']}
        for label, temp in zip(q['labels'], q['new_field_tempids']):
            token = q['ma_id'] + '/authored-checkbox-v1/' + label
            field = additions[ids[temp]]
            assert field[':answer-field/id'] == {stable_id('field', token)}
            assert field[':answer-field/key'] == {label}
            assert field[':answer-field/type'] == {enum[':answer-field.type/checkbox']}
            boolean_ids = {}
            for value in ('false', 'true'):
                aid = ids['answer-' + token + '/' + value]
                answer = additions[aid]
                assert answer[':answer/id'] == {stable_id('answer', token + '/' + value)}
                assert answer[':answer/type'] == {enum[':answer.type/text']}
                assert answer[':answer/value'] == {value}
                boolean_ids[value] = aid
            assert field[':answer-field/choices'] == set(boolean_ids.values())
            assert field[':answer-field/correct'] == {boolean_ids[str(label in q['correct']).lower()]}
    for r in manifest['responses']:
        assert additions[r['item']][':task-item/responses'] == {ids[t] for t in r['new_answer_tempids']}
    save('commit-validation.json' if committed else 'preview.json', {'passed': True, 'committed': committed, 'speculative': not committed, 'basis': manifest['basis'],
        'source': SOURCE, 'transaction_sha256': manifest['transaction_sha256'],
        'datoms': len(report[':edb/tx-data']), 'counts': manifest['counts'],
        'verification': ['Native application entity specs and checkbox predicates passed.',
            'Every new field, Boolean answer, canonical key, prompt and saved-response mapping checked.',
            'Exact expected retractions; no original field/answer facts or unrelated entities changed.',
            'All datoms attributed to the existing agent source.']})
    print(json.dumps({'commit_validation_passed' if committed else 'preview_passed': True, 'basis': manifest['basis'],
        'datoms': len(report[':edb/tx-data']), **manifest['counts']}), flush=True)

def preview():
    helper = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
        repo_root=ROOT, preview_bin=None), threading.Event())
    result = subprocess.run([str(helper), 'with', '--database', 'math', '--file', str(OUT / 'transaction.edn'),
        '--source', SOURCE], env=DB.env, check=True, capture_output=True, text=True, timeout=120)
    (OUT / 'preview.edn').write_text(result.stdout)
    verify_preview(loads(result.stdout))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['capture', 'plan', 'preview'])
    globals()[parser.parse_args().action]()
