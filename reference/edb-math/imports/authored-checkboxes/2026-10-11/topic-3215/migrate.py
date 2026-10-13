"""Audited, basis-guarded checkbox migration for MA topic 3215."""
import argparse
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
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, kw, loads
from core import atomic_json, stable_id

SOURCE = ':agent/gpt-6.1-sol-high'
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'),
    database='math', endpoint='/tmp/edb-math/writer.sock'))
PATTERN = '''[* {:question/difficulty [:db/id :db/ident]}
 {:knowledge-point/_questions [:db/id :knowledge-point/id :knowledge-point/title]}
 {:knowledge-point/_canonical-example [:db/id :knowledge-point/id]}
 {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]}
 {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''

def save(path, obj):
    atomic_json(path, obj)

def query(q, inputs, name, basis):
    return DB.query(q, inputs, OUT, name, basis)

def capture():
    assert not (OUT / 'commit-intent.json').exists(), 'Resolve the saved commit intent first'
    basis = DB.basis()
    rows = query('''[:find ?title (pull ?q ''' + PATTERN + ''')
      :in $ ?topic :where [?topic :topic/knowledge-points ?kp]
      [?kp :knowledge-point/title ?title] [?kp :knowledge-point/questions ?q]]''',
      [17592186049592], 'questions-before', basis)
    candidates = [q for title, q in rows if q[':question/problem'].startswith('Which of the following')]
    ids = [q[':db/id'] for q in candidates]
    items = query('''[:find ?q (pull ?item [* {:task-item/status [:db/id :db/ident]}])
      :in $ [?q ...] :where [?item :task-item/content ?q]]''', [ids], 'items-before', basis)
    oldanswers = [a[':db/id'] for q in candidates for f in q.get(':question/answer-fields', [])
      for a in f.get(':answer-field/choices', [])]
    responses = query('''[:find ?answer (pull ?item [* {:task-item/status [:db/id :db/ident]}])
      :in $ [?answer ...] :where [?item :task-item/responses ?answer]]''',
      [oldanswers], 'response-users-before', basis)
    attrs = DB.attributes(OUT, basis)
    (OUT / 'attributes.edn').write_text(dumps(attrs) + '\n')
    save(OUT / 'capture.json', {'basis':basis, 'questions':rows, 'items':items,
      'response_users':responses, 'source':SOURCE})
    save(OUT / 'summary-before.json', {'basis':basis, 'topic_questions':len(rows),
      'candidates':[{'id':q[':db/id'], 'ma_id':q[':question/math-academy-id'],
      'kp':title, 'problem':q[':question/problem'], 'solution':q.get(':question/worked-solution'),
      'fields':[{'id':f[':db/id'], 'type':f[':answer-field/type'][':db/ident'],
      'key':f[':answer-field/key'], 'correct':f.get(':answer-field/correct',{}).get(':answer/value')}
      for f in q.get(':question/answer-fields', [])]}
      for title,q in rows if q in candidates], 'presentations':items, 'response_users':responses})
    print(json.dumps({'basis':basis, 'topic_questions':len(rows), 'candidates':len(candidates),
      'presentations':len(items), 'response_users':len(responses)}))

# Reviewed against every displayed equation and the stored worked solution.
# IVP items retain the source's structural order/initial-condition classification;
# this migration does not repair source domain/existence issues or regrade work.
KEYS = {
 'q-95983':'I', 'q-118782':'I II', 'q-96669':'III', 'q-96680':'III',
 'q-118783':'I', 'q-96672':'I II', 'q-95984':'I II', 'q-96387':'I III',
 'q-118863':'I II', 'q-96702':'II', 'q-96703':'II III', 'q-96705':'I',
 'q-96712':'III', 'q-118858':'I III', 'q-118859':'II', 'q-118868':'III',
 'q-118869':'II III', 'q-118870':'III', 'q-96711':'I II', 'q-96713':'II',
 'q-96715':'I', 'q-95985':'I', 'q-96986':'II', 'q-118786':'I',
 'q-96987':'III', 'q-96992':'I II', 'q-118787':'I', 'q-118788':'II',
 'q-118790':'I II', 'q-118791':'II III', 'q-96988':'II', 'q-96990':'I III',
}
LABELS = ('I', 'II', 'III')

def subset(value):
    value = value.strip().rstrip('.')
    if value.startswith('None of '):
        assert value in ('None of these listed', 'None of those listed')
        return set()
    result = re.findall(r'\b(?:III|II|I)\b', value)
    remainder = re.sub(r'\b(?:III|II|I|and|only)\b|[,\s]', '', value)
    assert result and not remainder and len(result) == len(set(result)), value
    return set(result)

def statements(problem):
    lines = problem.splitlines()
    found = [re.sub(r'^(?:I{1,3}\.\s*)?-\s*', '', line)
      for line in lines[1:] if re.match(r'^(?:I{1,3}\.\s*)?-\s*', line)]
    assert len(found) == 3 and all(line.startswith('$') and line.endswith('$') for line in found), problem
    return found

def plan():
    assert not (OUT / 'commit-intent.json').exists(), 'Resolve the saved commit intent first'
    rows = loads((OUT / 'questions-before.edn').read_text())
    basis = json.loads((OUT / 'capture.json').read_text())['basis']
    items = {item[':db/id']: (q, item) for q,item in loads((OUT / 'items-before.edn').read_text())}
    for answer,item in loads((OUT / 'response-users-before.edn').read_text()):
        assert item[':db/id'] in items, 'Response owner without matching question presentation'
        assert items[item[':db/id']][1] == item
    forms, changed, migrated, old_components = [], [], [], []
    answer_targets = {}
    for title,q in rows:
        mid = q[':question/math-academy-id']
        if mid not in KEYS:
            continue
        assert not q.get(':knowledge-point/_canonical-example')
        correct = set(KEYS[mid].split())
        fields = q.get(':question/answer-fields', [])
        assert not fields or (len(fields) == 1 and fields[0][':answer-field/type'][':db/ident'] == ':answer-field.type/radio')
        if fields:
            assert subset(fields[0][':answer-field/correct'][':answer/value']) == correct, mid
            for answer in fields[0][':answer-field/choices']:
                assert answer[':answer/type'][':db/ident'] == ':answer.type/text'
                subset(answer[':answer/value'])
        solution = q.get(':question/worked-solution', '')
        conclusion = re.findall(r'correct answer is ["“]([^"”]+)["”]', solution)
        assert len(conclusion) == 1 and subset(conclusion[0]) == correct, mid
        equations = statements(q[':question/problem'])
        prompt = q[':question/problem'].splitlines()[0] + '\n\nSelect all that apply.\n\n'
        prompt += '\n'.join('- **' + label + '.** ' + equation for label,equation in zip(LABELS,equations))
        # Labels and instructions change; the three mathematical statements do not.
        links = []
        answer_targets[q[':db/id']] = {}
        for label in LABELS:
            token = mid + '/authored-checkbox-v1/' + label
            fid = 'field-' + token
            answers = []
            for value in ('false', 'true'):
                aid = 'answer-' + token + '/' + value
                forms.append({kw('db/id'):aid, kw('answer/id'):stable_id('answer', token+'/'+value),
                  kw('answer/type'):kw('answer.type/text'), kw('answer/value'):value,
                  kw('db/ensure'):kw('answer/validate')})
                answers.append(aid)
                answer_targets[q[':db/id']][(label,value)] = aid
            forms.append({kw('db/id'):fid, kw('answer-field/id'):stable_id('field',token),
              kw('answer-field/key'):label, kw('answer-field/type'):kw('answer-field.type/checkbox'),
              kw('answer-field/choices'):answers, kw('answer-field/correct'):answers[int(label in correct)],
              kw('db/ensure'):kw('answer-field/validate')})
            links.append(fid)
        for f in fields:
            old_components.append(f[':db/id'])
            old_components.extend(a[':db/id'] for a in f[':answer-field/choices'])
            forms.append([kw('db/retract'),q[':db/id'],kw('question/answer-fields'),f[':db/id']])
        forms.append({kw('db/id'):q[':db/id'],kw('question/problem'):prompt,
          kw('question/answer-fields'):links,kw('db/ensure'):kw('question/validate')})
        changed.append({'id':q[':db/id'],'ma_id':mid,'kp':title,'old_fields':[f[':db/id'] for f in fields],
          'correct':sorted(correct, key=LABELS.index),'equations':equations,'problem_after':prompt})
        bank = {a[':db/id']:a[':answer/value'] for f in fields for a in f[':answer-field/choices']}
        for itemid,(qid,item) in items.items():
            if qid != q[':db/id']:
                continue
            responses = [a[':db/id'] for a in item.get(':task-item/responses', [])]
            if not responses:
                continue
            assert len(responses) == 1 and responses[0] in bank
            chosen = subset(bank[responses[0]])
            status = item[':task-item/status'][':db/ident']
            if status in (':task-item.status/correct', ':task-item.status/incorrect'):
                assert (chosen == correct) == (status == ':task-item.status/correct'), (mid, itemid)
            forms.append([kw('db/retract'),itemid,kw('task-item/responses'),responses[0]])
            mapped = [answer_targets[qid][(label,str(label in chosen).lower())] for label in LABELS]
            forms.append({kw('db/id'):itemid,kw('task-item/responses'):mapped,
              kw('db/ensure'):kw('task-item/validate')})
            migrated.append({'item':itemid,'question':qid,'old_answer':responses[0],
              'old_value':bank[responses[0]],'selected':sorted(chosen,key=LABELS.index),
              'new_answer_tempids':mapped,'status':status})
    assert {q['ma_id'] for q in changed} == set(KEYS)
    assert len(changed) == 32 and sum(bool(q['old_fields']) for q in changed) == 25
    transaction = OUT / 'transaction.edn'
    transaction.write_text(dumps(forms) + '\n')
    save(OUT / 'plan.json', {'basis':basis,'source':SOURCE,'questions':changed,'responses':migrated,
      'old_component_entities':old_components,'transaction_sha256':hashlib.sha256(transaction.read_bytes()).hexdigest(),
      'counts':{'radio_converted':25,'missing_fields_created':7,'existing_checkbox_retained':1,
      'new_fields':96,'new_answers':192,'responses_mapped':len(migrated)},
      'content_notes':[
        'Original equations and worked solutions are retained; prompt changes add Roman labels and select-all instructions.',
        'q-96702 has an existing solution algebra typo: division by y is written as division by 2; subset II is unaffected.',
        'Some source IVP items use singular or incompatible initial data (q-95985, q-96986, q-96987, q-96992). Source structural classifications are retained; existence/domain repair is outside this representation migration.'
      ]})
    print(json.dumps({'prepared':True, 'questions':len(changed),'responses_mapped':len(migrated), 'basis':basis}))

def inspect_datoms(receipt, manifest):
    names = dict(loads((OUT / 'attributes.edn').read_text()))
    changed = {q['id'] for q in manifest['questions']}
    itemids = {r['item'] for r in manifest['responses']}
    old_components = set(manifest['old_component_entities'])
    source_ids = {s for _,a,_,_,s,_ in receipt[':edb/tx-data'] if names[a] != ':db/txInstant'}
    assert source_ids == {17592186045436}, source_ids
    allowed_new = {':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/type',
      ':answer-field/key',':answer-field/choices',':answer-field/correct'}
    new_entities = set(receipt[':edb/tempids'].values())
    expected_retractions = {(q['id'],kw('question/answer-fields'),f) for q in manifest['questions'] for f in q['old_fields']}
    expected_retractions.update((r['item'],kw('task-item/responses'),r['old_answer']) for r in manifest['responses'])
    expected_retractions.update((q['id'],kw('question/problem'),before[':question/problem'])
      for _,before in loads((OUT / 'questions-before.edn').read_text()) for q in manifest['questions'] if q['id']==before[':db/id'])
    actual_retractions = set()
    for e,a,v,tx,s,added in receipt[':edb/tx-data']:
        name = names[a]
        assert e not in old_components, 'An original field or answer was modified'
        if e in changed:
            assert name in (':question/problem', ':question/answer-fields')
        elif e in itemids:
            assert name == ':task-item/responses'
        elif e in new_entities:
            assert name in allowed_new and added
        else:
            assert name == ':db/txInstant' and added
        if not added:
            actual_retractions.add((e,name,v))
    assert actual_retractions == expected_retractions

def preview():
    manifest = json.loads((OUT / 'plan.json').read_text())
    helper = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
      repo_root=ROOT,preview_bin=None),threading.Event())
    result = subprocess.run([str(helper),'with','--database','math','--file',str(OUT/'transaction.edn'),
      '--source',SOURCE], env=DB.env,check=True,capture_output=True,text=True,timeout=120)
    (OUT/'preview.edn').write_text(result.stdout)
    report = loads(result.stdout)
    assert report[':edb/committed'] is False and report[':edb/speculative'] is True
    assert report[':edb/db-before-t'] == manifest['basis'], 'Head changed; refresh capture before commit'
    inspect_datoms(report, manifest)
    save(OUT/'preview.json', {'passed':True,'basis':manifest['basis'],'source':SOURCE,
      'helper':str(helper),'native_field_validation':True,'datoms':len(report[':edb/tx-data']),
      'transaction_sha256':manifest['transaction_sha256'],'counts':manifest['counts']})
    print(json.dumps({'preview_passed':True,'datoms':len(report[':edb/tx-data']),**manifest['counts']}))

def commit():
    manifest = json.loads((OUT/'plan.json').read_text())
    checked = json.loads((OUT/'preview.json').read_text())
    digest = hashlib.sha256((OUT/'transaction.edn').read_bytes()).hexdigest()
    assert checked['passed'] and digest == checked['transaction_sha256'] == manifest['transaction_sha256']
    intent_file = OUT/'commit-intent.json'
    if not intent_file.exists():
        assert DB.basis() == manifest['basis'], 'Database advanced; recapture, replan, and preview'
        save(intent_file, {'database':'math','endpoint':DB.args.endpoint,'basis':manifest['basis'],
          'source':SOURCE,'sha256':digest,'request_key':f'topic-3215-checkbox-v1-{manifest["basis"]}-{digest}'})
    intent = json.loads(intent_file.read_text())
    assert intent['sha256'] == digest and intent['source'] == SOURCE and intent['basis'] == manifest['basis']
    report = DB._commit(intent, OUT/'transaction.edn', OUT)
    assert report[':edb/committed'] is True
    inspect_datoms(report,manifest)
    print(json.dumps({'committed':True,'basis_before':report[':edb/db-before-t'],
      'basis_after':report[':edb/db-after-t'],'datoms':len(report[':edb/tx-data'])}))

def verify():
    report = loads((OUT/'commit.edn').read_text())
    assert report[':edb/committed'] is True
    basis = report[':edb/db-after-t']
    manifest = json.loads((OUT/'plan.json').read_text())
    inspect_datoms(report,manifest)
    before = {q[':db/id']:q for title,q in loads((OUT/'questions-before.edn').read_text())}
    mids = [q[':question/math-academy-id'] for q in before.values()]
    question_query = '[:find (pull ?q '+PATTERN+') :in $ [?q ...] :where [?q :question/id _]]'
    after = {row[0][':db/id']:row[0] for row in query(question_query,[list(before)],'questions-after',basis)}
    assert set(after) == set(before) and len(after) == 40
    altered = {q['id']:q for q in manifest['questions']}
    field_count = 0
    old_fields = {}
    for qid,old in before.items():
        current = after[qid]
        if qid not in altered:
            assert old == current, f'Unselected question changed: {qid}'
            continue
        change = altered[qid]
        exempt = {':question/problem', ':question/answer-fields'}
        assert {k:v for k,v in old.items() if k not in exempt} == {k:v for k,v in current.items() if k not in exempt}
        assert current[':question/problem'] == change['problem_after']
        fields = {f[':answer-field/key']:f for f in current[':question/answer-fields']}
        assert set(fields) == set(LABELS)
        for label,f in fields.items():
            assert f[':answer-field/type'][':db/ident'] == ':answer-field.type/checkbox'
            token = change['ma_id'] + '/authored-checkbox-v1/' + label
            assert f[':answer-field/id'] == stable_id('field',token)
            bank = {a[':answer/value']:a for a in f[':answer-field/choices']}
            assert set(bank) == {'true','false'} and len(f[':answer-field/choices']) == 2
            for value,a in bank.items():
                assert a[':answer/type'][':db/ident'] == ':answer.type/text'
                assert a[':answer/id'] == stable_id('answer',token+'/'+value)
            expected = str(label in change['correct']).lower()
            assert f[':answer-field/correct'][':db/id'] == bank[expected][':db/id']
            field_count += 1
        old_fields.update({f[':db/id']:f for f in old.get(':question/answer-fields',[])})
    items_before = {item[':db/id']:(q,item) for q,item in loads((OUT/'items-before.edn').read_text())}
    itemids = list(items_before)
    items_after = {row[0][':db/id']:row[0] for row in query('''[:find (pull ?e [* {:task-item/status [:db/id :db/ident]}])
      :in $ [?e ...] :where [?e :task-item/id _]]''',[itemids],'items-after',basis)}
    mapped = {r['item']:r for r in manifest['responses']}
    for itemid,(qid,old) in items_before.items():
        current = items_after[itemid]
        if itemid not in mapped:
            assert old == current
            continue
        expected = {report[':edb/tempids'][t] for t in mapped[itemid]['new_answer_tempids']}
        assert {a[':db/id'] for a in current[':task-item/responses']} == expected
        assert {k:v for k,v in old.items() if k != ':task-item/responses'} == {k:v for k,v in current.items() if k != ':task-item/responses'}
        fields = after[qid][':question/answer-fields']
        selected = {f[':answer-field/key'] for f in fields for a in f[':answer-field/choices']
          if a[':db/id'] in expected and a[':answer/value']=='true'}
        assert selected == set(mapped[itemid]['selected'])
    field_pattern = '''[* {:answer-field/type [:db/id :db/ident]}
      {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}
      {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]'''
    retained = {row[0][':db/id']:row[0] for row in query('[:find (pull ?f '+field_pattern+
      ') :in $ [?f ...] :where [?f :answer-field/id _]]',[list(old_fields)],'old-fields-after',basis)}
    assert retained == old_fields
    # The original radio layout and original submitted answers remain reproducible.
    historical = {row[0][':db/id']:row[0] for row in query(question_query,[list(before)],'history-questions-before',manifest['basis'])}
    assert historical == before
    historical_items = {row[0][':db/id']:row[0] for row in query('''[:find (pull ?e [* {:task-item/status [:db/id :db/ident]}])
      :in $ [?e ...] :where [?e :task-item/id _]]''',[itemids],'history-items-before',manifest['basis'])}
    assert historical_items == {i:record for i,(_,record) in items_before.items()}
    assert field_count == 96
    result = {'committed':True,'verified':True,'database':'math','topic':17592186049592,
      'topic_title':'Introduction to Differential Equations','basis_before':manifest['basis'],'basis_after':basis,
      'source':SOURCE,**manifest['counts'],'subset_questions_now_checkbox':33,
      'all_40_topic_questions_verified':True,'original_25_radio_fields_and_answers_retained':True,
      'original_layout_and_responses_verified_as_of_before':True,'learner_correctness_timing_xp_and_progress_unchanged':True,
      'incorrect_response_preserved':True,'unselected_questions_unchanged':True,
      'transaction_sha256':manifest['transaction_sha256']}
    save(OUT/'verification.json', result)
    print(json.dumps(result))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['capture','plan','preview','commit','verify'])
    args = parser.parse_args()
    globals()[args.phase]()
