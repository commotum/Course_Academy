"""Complete two source questions and add one authored question; no generator launch."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import threading
import uuid

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.client import StaleBasis
from capture.scripts.database.commit import Committer
from capture.scripts.database.edn import dumps, loads, kw
from capture.scripts.database.prepare import Plan, Snapshot
from capture.scripts.storage import file_lock
from scripts.generator_publish import Publisher

HERE = Path(__file__).resolve().parent
KP = 17592186110593
SOURCE = ':agent/codex'
NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:authored:exact-exponential-repair-2026-10-19')


def save(name, data):
    (HERE / name).write_text(json.dumps(data, indent=2, default=str) + '\n')


def identifier(name):
    return uuid.uuid5(NAMESPACE, name)


SOLUTIONS = {
    'q-25124': r'''First, we take $\log_3$ of both sides of the equation:

$$
\begin{aligned}
3^{x-2}&=6\\
\log_3\left(3^{x-2}\right)&=\log_3(6).
\end{aligned}
$$

Using $\log_b(b^c)=c$ gives $x-2=\log_3(6)$. Adding $2$ to both sides, we obtain

$$
x=\log_3(6)+2.
$$''',
    'q-66805': r'''We take $\log_5$ of both sides of the equation:

$$
\begin{aligned}
5^x&=15\\
\log_5\left(5^x\right)&=\log_5(15).
\end{aligned}
$$

Using $\log_b(b^c)=c$, we obtain the exact solution

$$
x=\log_5(15).
$$''',
}
CORRECT_VALUES = {
    'q-25124': r'x = \log_{3} (6) + 2',
    'q-66805': r'x = \log_{5} (15)',
}


def author():
    kp = loads((HERE / 'kp.edn').read_text())[0][0]
    records = []
    repairs = []
    for original in kp[':knowledge-point/questions']:
        mid = original.get(':question/math-academy-id')
        if mid not in SOLUTIONS:
            continue
        q = deepcopy(original)
        f, = q[':question/answer-fields']
        assert ':answer-field/correct' not in f and ':question/worked-solution' not in q
        correct, = [a for a in f[':answer-field/choices'] if a[':answer/value'] == CORRECT_VALUES[mid]]
        if mid == 'q-25124':
            duplicate, = [a for a in f[':answer-field/choices'] if a[':db/id'] == 17592186108046]
            assert not duplicate.get(':task-item/_responses')
            replacement = {':answer/id': identifier('q-25124-distractor'),
                           ':answer/type': ':answer.type/math',
                           ':answer/value': r'x=\log_3(2)-3'}
            f[':answer-field/choices'] = [replacement if a is duplicate else a for a in f[':answer-field/choices']]
        f[':answer-field/correct'] = correct
        q[':question/worked-solution'] = SOLUTIONS[mid]
        repairs.append({'question': q[':db/id'], 'source_id': mid,
                        'field': f[':db/id'], 'correct': correct[':db/id'],
                        'solution': SOLUTIONS[mid]})
        records.append({'knowledge_point': {'db/id': KP, 'title': kp[':knowledge-point/title']}, 'question': q})
    assert len(repairs) == 2
    choices = [r'x=\log_4(7)-3', r'x=\log_7(4)+3', r'x=\log_4(7)+3',
               r'x=\frac{\log_4(7)}{3}', r'x=\log_4(10)']
    answers = [{':answer/id': identifier('answer-' + str(i)), ':answer/type': ':answer.type/math',
                ':answer/value': val} for i, val in enumerate(choices)]
    field = {':answer-field/id': identifier('field'), ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers,
             ':answer-field/correct': [':answer/id', answers[2][':answer/id']]}
    new = {':question/id': identifier('question'),
           ':question/problem': r'Find the exact solution of the equation $4^{x-3}=7$.',
           ':question/difficulty': ':question.difficulty/easy',
           ':question/answer-fields': [field],
           ':question/worked-solution': r'''First, we take $\log_4$ of both sides of the equation:

$$
\begin{aligned}
4^{x-3}&=7\\
\log_4\left(4^{x-3}\right)&=\log_4(7).
\end{aligned}
$$

Using $\log_b(b^c)=c$ gives $x-3=\log_4(7)$. Adding $3$ to both sides, we obtain

$$
x=\log_4(7)+3.
$$'''}
    records.append({'knowledge_point': {'db/id': KP, 'title': kp[':knowledge-point/title']}, 'question': new})
    # Normalize only the offline tool representation, retaining all stored identities and values.
    for rec in records:
        for f in rec['question'][':question/answer-fields']:
            if isinstance(f[':answer-field/type'], dict):
                f[':answer-field/type'] = f[':answer-field/type'][':db/ident']
            if isinstance(f[':answer-field/correct'], dict):
                f[':answer-field/correct'] = [':answer/id', f[':answer-field/correct'][':answer/id']]
            for a in f[':answer-field/choices']:
                if isinstance(a[':answer/type'], dict):
                    a[':answer/type'] = a[':answer/type'][':db/ident']
    save('records.json', records)
    save('repairs.json', repairs)
    cases = []
    for rec in records:
        f, = rec['question'][':question/answer-fields']
        correct_uuid = str(f[':answer-field/correct'][1])
        cases.append({'label': rec['question'].get(':question/math-academy-id', 'authored question'),
                      'record': rec, 'checks': [
                          {'submitted_answer_id': str(a[':answer/id']),
                           'expected': 'accepted' if str(a[':answer/id']) == correct_uuid else 'rejected'}
                          for a in f[':answer-field/choices']]})
    save('grader-input.json', cases)

    import sympy as sp
    L = lambda b, r: sp.log(r) / sp.log(b)
    expressions = {17592186108049:L(3,6)/2,17592186108050:L(3,6)+2,
                   str(identifier('q-25124-distractor')):L(3,2)-3,
                   17592186108047:L(3,6)-2,17592186108048:L(3,4),
                   17592186109947:L(5,sp.Rational(1,15)),17592186109948:L(5,sp.Rational(1,3)),
                   17592186109949:L(5,3),17592186109950:5*L(5,3),17592186109946:L(5,15)}
    expressions.update({str(identifier('answer-'+str(i))):v for i,v in enumerate(
        [L(4,7)-3,L(7,4)+3,L(4,7)+3,L(4,7)/3,L(4,10)])})
    candidates = [[expressions[a.get(':db/id',str(a[':answer/id']))]
                   for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
                  for rec in records]
    expected = [L(3,6)+2, L(5,15), L(4,7)+3]
    verified = []
    for rec, bank, answer in zip(records, candidates, expected):
        f, = rec['question'][':question/answer-fields']
        matches = [abs(float(sp.N(value-answer, 40))) < 1e-25 for value in bank]
        assert sum(matches) == 1
        assert str(f[':answer-field/choices'][matches.index(True)][':answer/id']) == str(f[':answer-field/correct'][1])
        verified.append({'question': str(rec['question'][':question/id']),
                         'exact_solution': str(answer), 'unique_correct': True,
                         'choice_values': [str(sp.N(v,18)) for v in bank]})
    # Independent substitution into b^(x+s)=r via b^log_b(r)=r.
    assert sp.simplify((expected[0]-2)*sp.log(3)-sp.log(6)) == 0
    assert sp.simplify(expected[1]*sp.log(5)-sp.log(15)) == 0
    assert sp.simplify((expected[2]-3)*sp.log(4)-sp.log(7)) == 0
    save('math-verification.json', {'questions': verified, 'method': 'Independent log identities and all-choice evaluation'})
    save('evidence.json', {'kind': 'authored_completion', 'contributor': SOURCE,
        'original_basis': json.loads((HERE/'identity.json').read_text())['basis'],
        'kp': KP, 'topic': 17592186049053, 'canonical_example': 'e-4067',
        'template': 'For b^(x+s)=r, take log base b, simplify x+s=log_b(r), then subtract s.',
        'source_questions': ['q-25124','q-66805','q-100163','q-66801'],
        'repairs': repairs, 'new_question': str(new[':question/id']),
        'duplicate_choice_correction': {'question':'q-25124','original_answer_eid':17592186108046,
            'original_value':r'x=\log_3(2)+3','reason':r'log_3(6)+2=log_3(2)+3, so both original options were correct.',
            'replacement_value':r'x=\log_3(2)-3','preservation':'Retain original answer entity/value; replace only unreferenced bank membership.'},
        'new_parameters': {'base':4,'rhs':7,'shift':-3},
        'attribution': 'Answer keys and solutions are locally derived, not observed MA grading keys. The new question is locally authored and has no MA identifier.',
        'scope': 'Two existing completions and one authored practice question. No generator certification or registration.'})
    print('Prepared two completions and one authored question; 15 independent choice checks.')


def snapshot(client, directory):
    identity = client.status()
    basis = identity['basis']
    original_query = (HERE/'kp-query.edn').read_text()
    kp = client.query(original_query, [KP], directory, 'kp', basis)[0][0]
    entities = {}
    def collect(obj):
        if isinstance(obj, dict):
            if ':db/id' in obj:
                entities.setdefault(obj[':db/id'], {}).update(obj)
            for v in obj.values(): collect(v)
        elif isinstance(obj, list):
            for v in obj: collect(v)
    collect(kp)
    attrs = client.query('[:find ?a ?ident ?type ?card :where [?a :db/ident ?ident] [?a :db/valueType ?vt] [?vt :db/ident ?type] [?a :db/cardinality ?c] [?c :db/ident ?card]]', [], directory, 'attributes', basis)
    idents = client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], directory, 'idents', basis)
    facts = client.query('[:find ?e ?a ?v ?s :in $ [?e ...] :where [?e ?a ?v _ ?s]]', [sorted(entities)], directory, 'facts', basis)
    data = {**identity,'entities':list(entities.values()),'attributes':attrs,'idents':idents,'facts':facts}
    (directory/'snapshot.edn').write_text(dumps(data)+'\n')
    return data, kp


def prepare(data, kp):
    snap = Snapshot(data)
    assert SOURCE in snap.idents
    plan = Plan(snap, SOURCE)
    repairs = json.loads((HERE/'repairs.json').read_text())
    extras = []
    for repair in repairs:
        q = snap.entities[repair['question']]
        f = snap.entities[repair['field']]
        frozen = next(r['question'] for r in json.loads((HERE/'records.json').read_text())
                      if r['question'].get(':question/math-academy-id') == repair['source_id'])
        assert q[':question/problem'] == frozen[':question/problem']
        assert q[':question/math-academy-id'] == repair['source_id']
        assert ':question/worked-solution' not in q and ':answer-field/correct' not in f
        assert repair['correct'] in {a[':db/id'] for a in f[':answer-field/choices']}
        if repair['source_id'] == 'q-25124':
            duplicate, = [a for a in f[':answer-field/choices'] if a[':db/id'] == 17592186108046]
            assert not duplicate.get(':task-item/_responses')
            replacement = plan.entity('answer',identifier('q-25124-distractor'))
            plan.set(replacement,None,'answer/type',kw('answer.type/math'))
            plan.set(replacement,None,'answer/value',r'x=\log_3(2)-3')
            plan.retract(f[':db/id'],'answer-field/choices',duplicate[':db/id'])
            plan.set(f[':db/id'],f,'answer-field/choices',[replacement],many=True)
        for e,a,v in [(q[':db/id'],'question/worked-solution',repair['solution']),
                      (f[':db/id'],'answer-field/correct',repair['correct'])]:
            plan.forms.append([kw('db/cas'),e,kw(a),None,v])
            extras.append([e,kw(a),v])
        for e,spec in [(q[':db/id'],'question/validate'),(f[':db/id'],'answer-field/validate')]:
            plan.forms.append([kw('db/ensure'),e,kw(spec)])
        for answer in f[':answer-field/choices']:
            plan.forms.append([kw('db/ensure'),answer[':db/id'],kw('answer/validate')])
    new = json.loads((HERE/'records.json').read_text())[-1]['question']
    assert not snap.find('question/id', new[':question/id'])
    qt = plan.entity('question', new[':question/id'])
    for attr in ['question/problem','question/worked-solution','question/difficulty']:
        val = new[':'+attr]
        plan.set(qt,None,attr,kw(val) if attr.endswith('difficulty') else val)
    f, = new[':question/answer-fields']
    ft = plan.entity('answer-field',f[':answer-field/id'])
    plan.set(ft,None,'answer-field/key',f[':answer-field/key'])
    plan.set(ft,None,'answer-field/type',kw(f[':answer-field/type']))
    answers = []
    for a in f[':answer-field/choices']:
        at = plan.entity('answer',a[':answer/id'])
        plan.set(at,None,'answer/type',kw(a[':answer/type']))
        plan.set(at,None,'answer/value',a[':answer/value'])
        if a[':answer/id'] == f[':answer-field/correct'][1]:
            plan.set(ft,None,'answer-field/correct',at)
        answers.append(at)
    plan.set(ft,None,'answer-field/choices',answers,many=True)
    plan.set(qt,None,'question/answer-fields',[ft],many=True)
    plan.set(KP,kp,'knowledge-point/questions',[qt],many=True)
    batch = plan.finish()
    batch['assertions'] += extras
    return batch


def commit():
    publisher = Publisher.from_environment(source=SOURCE)
    client = publisher.client
    committer = Committer(publisher.config, client, HERE/'publication')
    with file_lock(ROOT/'.local/capture/database.lock'):
        request = committer.pending()
        if request is None:
            data, kp = snapshot(client,HERE/'before')
            batch = prepare(data,kp)
            committer.preview(batch,data)
            request = committer.save_request(batch,data,hashlib.sha256((HERE/'records.json').read_bytes()).hexdigest())
        try:
            receipt = committer.submit(request)
        except StaleBasis:
            committer.retire(request,'rejected_stale_basis',{})
            raise
        proof = committer.verify_receipt(request,receipt)
        basis = receipt[':edb/db-after-t']
        kp = client.query((HERE/'kp-query.edn').read_text(), [KP], HERE/'after', 'kp', basis)[0][0]
        questions = {q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
        for repair in json.loads((HERE/'repairs.json').read_text()):
            q = questions[repair['source_id']]
            assert q[':question/worked-solution'] == repair['solution']
            assert q[':question/answer-fields'][0][':answer-field/correct'][':db/id'] == repair['correct']
        new, = [q for q in kp[':knowledge-point/questions'] if str(q[':question/id']) == str(identifier('question'))]
        assert new[':question/problem'] == json.loads((HERE/'records.json').read_text())[-1]['question'][':question/problem']
        assert len(kp[':knowledge-point/questions']) == 5
        retained = client.query('[:find (pull ?a [* {:task-item/_responses [:db/id]}]) :in $ ?a :where [?a :answer/id _]]',
            [17592186108046], HERE/'after', 'retained-original-answer', basis)[0][0]
        original = next(a for q in loads((HERE/'kp.edn').read_text())[0][0][':knowledge-point/questions']
                        for f in q[':question/answer-fields'] for a in f[':answer-field/choices']
                        if a[':db/id'] == 17592186108046)
        assert retained[':answer/id'] == original[':answer/id']
        assert retained[':answer/value'] == original[':answer/value']
        assert not retained.get(':task-item/_responses')
        assert all(a[':db/id'] != 17592186108046 for q in kp[':knowledge-point/questions']
                   for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])
        result = {'status':'verified','basis_before':request['basis'],'basis_after':basis,
                  'existing_questions_completed':2,'authored_questions_added':1,
                  'kp_question_count':5,'new_question_eid':new[':db/id'],'receipt':proof}
        save('verification.json',result)
        committer.retire(request,'verified',result)
        print(json.dumps(result))


if __name__ == '__main__':
    if sys.argv[1:] == ['author']: author()
    elif sys.argv[1:] == ['commit']: commit()
    else: raise SystemExit('Use author or commit')
