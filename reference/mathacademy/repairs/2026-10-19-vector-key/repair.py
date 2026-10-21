"""Bounded, separately attributed q-104098 correction; originals stay intact.

Run from the repository with PYTHONPATH=capture and the capture virtualenv.
Each phase uses the normal preview, durable request, receipt and pinned readback.
No source answer key or learner outcome is inferred.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import threading
import uuid

from scripts.config import Config
from scripts.database.client import EDBClient, QUESTION_PULL
from scripts.database.commit import Committer
from scripts.database.edn import dumps, loads, kw
from scripts.database.math_content import prose, value
from scripts.database.prepare import Plan, Snapshot, source_uuid, digest
from scripts.storage import atomic_json, atomic_text, file_lock, read_json

ROOT = Path(__file__).resolve().parent
SOURCE_HASH = '2bb65f4679e11987c2a2e9f49ea6b15e11fb5d1d38c14d9bbe2cec30c49c2a50'
MID = 'q-104098'
AUTHOR = ':agent/codex'
QUESTION = source_uuid('question', MID)
FIELD = source_uuid('answer-field', str(QUESTION) + ':' + digest(['selection', 'radio']))
CORRECT_ID = uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:repair:q-104098:correct-cross-product')
CORRECT = r'r\times \begin{bmatrix}4 \\ 9 \\ 5\end{bmatrix}=-41i+31j-23k'


def inputs():
    path = ROOT / 'source-question.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == SOURCE_HASH
    evidence = read_json(ROOT / 'evidence.json')
    for name, expected in evidence['original_source_files'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, name
    q = read_json(path)
    assert q['math_academy_id'] == MID and str(q['topic_id']) == '1800'
    assert q['source_example_id'] == 'e-4922'
    f, = q['answer_fields']
    assert f['type'] == 'radio' and f['key'] == 'selection' and len(f['choices']) == 5
    return q


RAW = inputs()
CHOICES = [{'type': c['type'], 'value': value(c['type'], c['value'])} for c in RAW['answer_fields'][0]['choices']]
for c in CHOICES:
    c['uuid'] = source_uuid('answer', str(FIELD) + ':' + digest([c['type'], c['value']]))
assert len({c['value'] for c in CHOICES}) == 5 and CORRECT not in {c['value'] for c in CHOICES}
ORIGINAL_SOLUTION = prose(RAW['worked_solution'])
SOLUTION = prose(r'''Local correction by Codex. The five original Math Academy choices are retained; the additional correct equation is locally authored. Math Academy's grading key for the original bank is unconfirmed.

We need a vector parallel to the line. Using the two given points,

$$
v=q-p=\begin{bmatrix}1\\8\\9\end{bmatrix}-\begin{bmatrix}-3\\-1\\4\end{bmatrix}
=\begin{bmatrix}4\\9\\5\end{bmatrix}.
$$

Starting with $(r-p)\times v=0$, we obtain $r\times v=p\times v$. Expanding the cross product gives

$$
p\times v=\begin{vmatrix}i&j&k\\-3&-1&4\\4&9&5\end{vmatrix}
=(-5-36)i-( -15-16)j+(-27+4)k=-41i+31j-23k.
$$

Thus the equation is

$$
r\times\begin{bmatrix}4\\9\\5\end{bmatrix}=-41i+31j-23k.
$$

Both given points satisfy this equation: $P\times v=Q\times v=(-41,31,-23)$. None of the five original choices does.

Original Math Academy explanation (preserved verbatim below; its concluding signs are incorrect):

''' + ORIGINAL_SOLUTION)
SOLUTION_BEFORE_FORMAT = SOLUTION
SOLUTION = SOLUTION.replace(
    r'p\times v=\begin{vmatrix}i&j&k\\-3&-1&4\\4&9&5\end{vmatrix}' + '\n' +
    r'=(-5-36)i-( -15-16)j+(-27+4)k=-41i+31j-23k.',
    r'\begin{aligned}' + '\n' +
    r'p\times v&=\begin{vmatrix}i&j&k\\-3&-1&4\\4&9&5\end{vmatrix}\\' + '\n' +
    r'&=(-5-36)i-(-15-16)j+(-27+4)k\\' + '\n' +
    r'&=-41i+31j-23k.' + '\n' + r'\end{aligned}')
assert SOLUTION != SOLUTION_BEFORE_FORMAT


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def math_proof():
    p, q, v = (-3,-1,4), (1,8,9), (4,9,5)
    # Each entry is the complete equation in the corresponding captured choice.
    equations = [(v,(31,-41,23)), (p,(23,31,-41)), (v,(41,-31,23)),
                 (p,(41,-31,23)), (p,(23,-41,-31))]
    proof = [{'option': c['option'], 'value': c['value'],
              'P_cross_left_vector': cross(p, left), 'Q_cross_left_vector': cross(q, left),
              'right_vector': right, 'valid': cross(p,left) == right and cross(q,left) == right}
             for c, (left,right) in zip(RAW['answer_fields'][0]['choices'], equations)]
    assert not any(c['valid'] for c in proof)
    assert cross(p,v) == cross(q,v) == (-41,31,-23)
    atomic_json(ROOT/'mathematical-verification.json', {'original_choices':proof,
        'correct_direction':v, 'correct_constant':cross(p,v), 'method_source':'context/teaching-context.edn',
        'template':'Subtract the two position vectors, then expand p cross v, as in e-4922.',
        'canonical_parameters':{'P':[4,-7,9], 'Q':[3,-5,8]},
        'target_parameters':{'P':p, 'Q':q}, 'no_MA_key_inferred':True})


def snapshot(client, directory):
    basis = client.basis()
    data = client.snapshot({'questions':[RAW], 'canonical_examples':[{'math_academy_id':'e-4922','topic_id':1800}]}, directory, basis)
    # Phase one saves the original answer values before a field can validly own
    # them. Read those exact UUIDs too; later phases link, rather than recreate.
    rows = client.query('[:find (pull ?a [*]) :in $ [?id ...] :where [?a :answer/id ?id]]',
        [[c['uuid'] for c in CHOICES] + [CORRECT_ID]], directory, 'original-and-local-answers', basis)
    known = {e[':db/id'] for e in data['entities']}
    extra = [r[0] for r in rows if r[0][':db/id'] not in known]
    data['entities'].extend(extra)
    if extra:
        data['facts'].extend(client.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]',
            [[e[':db/id'] for e in extra]], directory, 'extra-answer-facts', basis))
    assert AUTHOR in Snapshot(data).idents
    return data


def existing(snap, attr, val):
    rows = snap.find(attr, val)
    assert len(rows) <= 1, (attr,val)
    return rows[0] if rows else None


def prepare(phase, data):
    snap = Snapshot(data)
    plan = Plan(snap, source=AUTHOR if phase in ('02-local-correction','04-format-correction') else ':org/Math-Academy')
    old = existing(snap, 'question/math-academy-id', MID)
    if old:
        assert old[':question/id'] == QUESTION
        assert old[':question/problem'] == prose(RAW['problem'])
    if phase == '04-format-correction':
        assert old[':question/worked-solution'] in (SOLUTION_BEFORE_FORMAT,SOLUTION)
        plan.set(old[':db/id'],old,'question/worked-solution',SOLUTION)
        return plan.finish()
    if phase == '01-originals':
        assert old is None, 'Original import is one-time; recover its saved receipt instead of revising content.'
        qt = plan.entity('question', QUESTION)
        for attr, val in [('question/math-academy-id', MID), ('question/problem',prose(RAW['problem'])),
                          ('question/worked-solution',ORIGINAL_SOLUTION),
                          ('question/difficulty',kw('question.difficulty/moderate'))]:
            plan.set(qt,None,attr,val)
        for c in CHOICES:
            assert existing(snap,'answer/id',c['uuid']) is None
            at = plan.entity('answer',c['uuid'])
            plan.set(at,None,'answer/type',kw('answer.type/'+c['type']))
            plan.set(at,None,'answer/value',c['value'])
        # No practice or activity link is installed while the question is fieldless.
    else:
        assert old
        previous_fields = old.get(':question/answer-fields',[])
        previous = previous_fields[0] if previous_fields else None
        if previous:
            assert len(previous_fields) == 1 and previous[':answer-field/id'] == FIELD
        ft = plan.entity('answer-field',FIELD,previous)
        originals = []
        for c in CHOICES:
            a = existing(snap,'answer/id',c['uuid'])
            assert a and a[':answer/value'] == c['value']
            originals.append(a[':db/id'])
        if phase == '02-local-correction':
            assert not previous_fields and old[':question/worked-solution'] == ORIGINAL_SOLUTION
            assert existing(snap,'answer/id',CORRECT_ID) is None
            at = plan.entity('answer',CORRECT_ID)
            plan.set(at,None,'answer/type',kw('answer.type/math'))
            plan.set(at,None,'answer/value',CORRECT)
            plan.set(at,None,'answer/feedback','Locally authored correction by Codex; this option was absent from the original Math Academy bank.')
            plan.set(ft,previous,'answer-field/correct',at)
            plan.set(ft,previous,'answer-field/choices',originals+[at],many=True)
            plan.set(old[':db/id'],old,'question/worked-solution',SOLUTION)
        else:
            assert phase == '03-original-controls'
            assert old[':question/worked-solution'] == SOLUTION
            local = existing(snap,'answer/id',CORRECT_ID)
            assert previous[':answer-field/correct'][':db/id'] == local[':db/id']
            assert {a[':db/id'] for a in previous[':answer-field/choices']} == set(originals+[local[':db/id']])
            # Claim only observed original controls/ownership under MA. The new
            # answer, key and corrected solution retain Codex attribution only.
            plan.set(ft,previous,'answer-field/choices',originals,many=True)
            points = [e for e in data['entities'] if e.get(':knowledge-point/title') == RAW['knowledge_point']]
            assert len(points) == 1
            point = points[0]
            assert str(point[':knowledge-point/id']) == 'fecaf27b-659c-59dd-887f-f154d5f83bd4'
            plan.set(point[':db/id'],point,'knowledge-point/questions',[old[':db/id']],many=True)
        plan.set(ft,previous,'answer-field/key','selection')
        plan.set(ft,previous,'answer-field/type',kw('answer-field.type/radio'))
        plan.set(old[':db/id'],old,'question/answer-fields',[ft],many=True)
    return plan.finish()


def run_phase(client, config, phase):
    folder = ROOT/phase
    committer = Committer(config,client,folder)
    pending = committer.pending()
    if not pending and read_json(folder/'verification.json',{}).get('status') == 'verified':
        return read_json(folder/'verification.json')
    if pending:
        assert pending['content_sha256'] == digest([SOURCE_HASH,phase,SOLUTION,CORRECT])
    else:
        data = snapshot(client,folder/'before')
        batch = prepare(phase,data)
        atomic_text(folder/'batch.edn',dumps(batch))
        committer.preview(batch,data)
        pending = committer.save_request(batch,data,digest([SOURCE_HASH,phase,SOLUTION,CORRECT]))
    receipt = committer.submit(pending)
    proof = committer.verify_receipt(pending,receipt)
    basis = receipt[':edb/db-after-t']
    data = snapshot_at(client,folder/'after',basis)
    expected = loads(pending['batch_edn'])
    snap = Snapshot(data)
    tempids = receipt.get(':edb/tempids',{})
    def resolve(v):
        return tempids.get(v,snap.idents.get(str(v),v)) if isinstance(v,str) else v
    for e,a,v in expected['assertions']:
        eid = resolve(e)
        types = {str(r[1]):str(r[2]) for r in data['attributes']}
        val = resolve(v) if types[str(a)] == ':db.type/ref' else v
        assert snap.sourced(eid,str(a).lstrip(':'),val,expected['source']), (e,a,v)
    result = {'status':'verified','phase':phase,'basis_before':pending['basis'],'basis_after':basis,'receipt':proof}
    atomic_json(folder/'verification.json',result)
    committer.retire(pending,'verified',result)
    print(json.dumps(result),flush=True)
    return result


def snapshot_at(client, directory, basis):
    data = client.snapshot({'questions':[RAW]},directory,basis)
    rows = client.query('[:find (pull ?a [*]) :in $ [?id ...] :where [?a :answer/id ?id]]',
        [[c['uuid'] for c in CHOICES]+[CORRECT_ID]],directory,'all-answer-values',basis)
    known = {e[':db/id'] for e in data['entities']}
    extra = [r[0] for r in rows if r[0][':db/id'] not in known]
    data['entities'].extend(extra)
    if extra:
        data['facts'].extend(client.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]',
            [[e[':db/id'] for e in extra]],directory,'extra-facts',basis))
    return data


def main():
    math_proof()
    config = Config(); client = EDBClient(config,threading.Event())
    with file_lock(config.database_lock):
        proofs = [run_phase(client,config,phase) for phase in
                  ('01-originals','02-local-correction','03-original-controls','04-format-correction')]
        data = snapshot_at(client,ROOT/'final',proofs[-1]['basis_after'])
        snap = Snapshot(data); q = existing(snap,'question/math-academy-id',MID)
        field, = q[':question/answer-fields']; local = field[':answer-field/correct']
        assert q[':question/worked-solution'] == SOLUTION
        assert len(field[':answer-field/choices']) == 6 and local[':answer/value'] == CORRECT
        assert snap.sourced(field[':db/id'],'answer-field/correct',local,AUTHOR)
        assert not snap.sourced(field[':db/id'],'answer-field/correct',local,':org/Math-Academy')
        assert snap.sourced(local[':db/id'],'answer/value',CORRECT,AUTHOR)
        assert not snap.sourced(local[':db/id'],'answer/value',CORRECT,':org/Math-Academy')
        for c in CHOICES:
            a = existing(snap,'answer/id',c['uuid'])
            assert snap.sourced(a[':db/id'],'answer/value',c['value'],':org/Math-Academy')
        inputs()  # All frozen capture, checkpoint and completion bytes are unchanged.
        proof = {'status':'verified','question_id':MID,'question_eid':q[':db/id'],
            'field_eid':field[':db/id'],'local_correct_answer_eid':local[':db/id'],
            'basis':data['basis'],'phases':proofs,'original_choices_preserved':5,'local_choices_added':1,
            'source_key':'unconfirmed','correction_source':AUTHOR,'original_capture_hashes_unchanged':True,
            'learner_and_engine_facts_unchanged':True}
        atomic_json(ROOT/'verification.json',proof)
        print(json.dumps(proof),flush=True)


if __name__ == '__main__':
    main()
