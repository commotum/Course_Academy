"""Independent value checks, representation regressions, and exact repair plan."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from native_comparison import compare


def load(kp):
    path = H / 'product-log-package/generator.py' if kp == 17592186096618 else ROOT / f'generate/scratch/{kp}.py'
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location('generator_' + str(kp), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def keyed(record):
    f = record['question'][':question/answer-fields'][0]
    return next(a[':answer/value'] for a in f[':answer-field/choices']
                if a[':answer/id'] == f[':answer-field/correct'][1])


def equivalent(old, new):
    outcome = compare(old, new)
    assert outcome['outcome'] == 'equivalent', (old, new, outcome)


def current_record(kp, question):
    q = copy.deepcopy(question)
    if ':question/difficulty' in q:
        q[':question/difficulty'] = q[':question/difficulty'][':db/ident']
    for f in q[':question/answer-fields']:
        f[':answer-field/type'] = f[':answer-field/type'][':db/ident']
        f[':answer-field/correct'] = [':answer/id', f[':answer-field/correct'][':answer/id']]
        for a in f[':answer-field/choices']:
            a[':answer/type'] = a[':answer/type'][':db/ident']
    return {'knowledge_point': {'db_id': kp[':db/id'], 'title': kp[':knowledge-point/title']},
            'question': q, 'generation': {'template': 'stored-repair'}}


def plan():
    before = json.loads((H / 'before.json').read_text())['records']
    before.append(json.loads((H / 'inequality-before.json').read_text()))
    generators = {kp: load(kp) for kp in (17592186124470, 17592186129268, 17592186198361, 17592186096618)}
    source_paths = {
        17592186124470: 'generate/scratch/17592186124470/reference/replenishment/basis-2689/generated.json',
        17592186129268: 'generate/scratch/17592186129268/reference/replenishment/basis-2574/generated.json',
        17592186198361: 'generate/scratch/17592186198361/reference/replenishment/basis-2590/generated.json',
        17592186096618: 'generate/repairs/2026-10-19-engine-generators/17592186096618/review-1-policy-2-27f074a972f68aa2/batch-delivery/accepted.json'}
    historical = {kp: {r['question'][':question/id']: r for r in json.loads((ROOT / path).read_text())}
                  for kp, path in source_paths.items()}
    targets = {17592186555990, 17592186555998, 17592186539371, 17592186539380,
               17592186537006, 17592186657612, 17592186657613, 17592186657619,
               17592186657623, 17592186157736}
    changes, prospective, grading = [], [], []
    for kp in before:
        kid = kp[':db/id']
        for question in kp[':knowledge-point/questions']:
            qid = question[':db/id']
            if qid not in targets:
                continue
            record = current_record(kp, question)
            q = record['question']
            f = q[':question/answer-fields'][0]
            old_values = {a[':answer/id']: a[':answer/value'] for a in f[':answer-field/choices']}
            value_pairs = []
            if qid == 17592186157736:
                correct = f[':answer-field/correct'][1]
                value_pairs = [(old_values[correct], r'-\frac12\log_{8}(6)')]
            else:
                g = generators[kid]
                history = historical[kid][q[':question/id']]
                m = history['generation']; p = m['parameters']; t = m['template']
                if kid == 17592186124470:
                    for old in old_values.values():
                        new = g.final_solution_value(q[':question/worked-solution']) if old == keyed(record) else g.choice_tex(g.read_scalar(old), t, p)
                        assert g.equal(g.read_scalar(old), g.read_scalar(new))
                        value_pairs.append((old, new))
                elif kid == 17592186198361:
                    values, _, _ = g.bank(t, p, m['profile'])
                    reader=generators[17592186124470]
                    for old in old_values.values():
                        matches=[new for new in values if g.sp.expand_log(reader.read_scalar(new)-reader.read_scalar(old))==0]
                        assert len(matches)==1,('Ratio bank mismatch',old,matches)
                        value_pairs.append((old,matches[0]))
                elif kid == 17592186129268:
                    # Only the endpoint changes; bounds and substituted density stay intact.
                    correct = keyed(record)
                    s = q[':question/worked-solution']
                    start = s.rindex(' & =') + len(' & =')
                    q[':question/worked-solution'] = s[:start] + correct + r'.\end{aligned}' + '\n$$'
                    assert g.sp.trigsimp(g.sp.sin(2*g.theta) - 2*g.sp.sin(g.theta)*g.sp.cos(g.theta)) == 0
                else:
                    pr, sol, bank, u, v, rows = g.build(t, p)
                    if t.endswith('radio'):
                        if t == 'log_log_radio':
                            b = p['b']
                            for a in m['window']:
                                half = g.tex(g.s.Rational(a, 2))
                                shown = r'\left('+half+r'\right)\left(\frac{\log_{'+str(b)+r'}(x)}{x}\right)+\left('+half+r'\right)\left(\frac{\ln(x)}{x\ln('+str(b)+r')}\right)'
                                value_pairs.append((g.tex(a*g.s.log(g.X)/(g.X*g.s.log(b))), shown))
                        else:
                            n, b = p['n'], p['b']
                            L = g.X**(n-1)*v; R = g.X**(n-1)/g.s.log(b)
                            for a, bcoef in m['coefficient_pairs']:
                                old = r'\left('+str(a)+r'\right)\left('+g.tex(L)+r'\right)+\left('+str(bcoef)+r'\right)\left('+g.tex(R)+r'\right)'
                                new = r'\left('+str(a)+r'\right)\left('+g.source_log_tex(L,t,p)+r'\right)+\left('+str(bcoef)+r'\right)\left('+g.source_log_tex(R,t,p)+r'\right)'
                                value_pairs.append((old, new))
                    else:
                        new_prompt, bank = g.remask(pr, u, v, m['target'], t, p)
                        q[':question/problem'] = g.normalize_prose(g.clean(new_prompt))
                        value_pairs = [(next(iter(old_values.values())), bank[0][0])]
                    value_pairs = [(g.normalize_tex(g.clean(a)), g.normalize_tex(g.clean(b))) for a,b in value_pairs]
            for answer in f[':answer-field/choices']:
                old = answer[':answer/value']
                matches = [new for candidate, new in value_pairs if candidate == old]
                if not matches and value_pairs:
                    matches = [new for candidate,new in value_pairs if compare(candidate, old)['outcome'] == 'equivalent']
                if matches:
                    assert len(matches) == 1, ('Ambiguous repair', qid, old)
                    new = matches[0]
                    if kid not in (17592186124470,17592186198361):  # Radio families have exact scalar proofs above.
                        equivalent(old, new)
                    if old != new:
                        changes.append({'entity': answer[':db/id'], 'question': qid, 'attribute': 'answer/value', 'before': old, 'after': new})
                        answer[':answer/value'] = new
            for attr in (':question/problem', ':question/worked-solution'):
                if q[attr] != question[attr]:
                    changes.append({'entity': qid, 'question': qid, 'attribute': attr[1:], 'before': question[attr], 'after': q[attr]})
            checks = []
            if f[':answer-field/type'].endswith('/radio'):
                checks = [{'field_index': 0, 'submitted_answer_id': a[':answer/id'],
                           'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected'}
                          for a in f[':answer-field/choices']]
            else:
                checks = [{'field_index': 0, 'submitted': keyed(record), 'expected': 'accepted'},
                          {'field_index': 0, 'submitted': old_values[f[':answer-field/correct'][1]], 'expected': 'accepted'},
                          {'field_index': 0, 'submitted': '987654321', 'expected': 'rejected'}]
            grading.append({'label': str(qid), 'record': record, 'checks': checks})
            prospective.append(record)
    assert {r['question'][':db/id'] for r in prospective} == targets
    assert {c['question'] for c in changes} == targets
    # Imported assignment: logarithm laws are ordinary algebra here. Show the
    # actual endpoint conversion, leaving the existing key and grading intact.
    assignment=json.loads((H/'assignment-before.json').read_text())
    record=current_record({':db/id':0,':knowledge-point/title':'Fundamental Theorem of Line Integrals'},assignment)
    q=record['question'];old=q[':question/worked-solution']
    suffix=('\n\nSince $557$ and $93$ are positive, the power and quotient rules for logarithms give\n\n'
            r'$$\ln\sqrt{557}-\ln\sqrt{93}=\frac12\ln557-\frac12\ln93=\frac12\ln\left(\frac{557}{93}\right).$$')
    q[':question/worked-solution']=old+suffix
    sp=generators[17592186124470].sp
    assert sp.expand_log(sp.log(sp.sqrt(557))-sp.log(sp.sqrt(93))-sp.log(sp.Rational(557,93))/2,force=True)==0
    changes.append({'entity':q[':db/id'],'question':q[':db/id'],'attribute':'question/worked-solution','before':old,'after':old+suffix})
    prospective.append(record)
    grading.append({'label':str(q[':db/id']),'record':record,'checks':[
        {'field_index':0,'submitted':keyed(record),'expected':'accepted'},
        {'field_index':0,'submitted':'987654321','expected':'rejected'}]})
    (H / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
    (H / 'prospective.json').write_text(json.dumps(prospective, indent=2) + '\n')
    (H / 'grading-input.json').write_text(json.dumps(grading, indent=2) + '\n')
    subprocess.run([str(ROOT / 'generate/scratch/17592186064281/check-engine'),
                    str(H/'grading-input.json'), str(H/'grading-report.json')], check=True)
    print(json.dumps({'questions':len(prospective), 'changed_values':len(changes)}))


if __name__ == '__main__':
    plan()
