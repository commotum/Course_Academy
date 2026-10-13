"""Validate frozen bank replay, rendered mathematics, solution steps and native grading."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import uuid
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, default=str) + '\n')

def expr(text):
    return g.expression(text)

def parse(problem):
    return g.fingerprint_text(problem)

def primitive(e, variable):
    table = {sp.csc(variable)**2: -sp.cot(variable), sp.sin(variable): -sp.cos(variable), sp.cos(variable): sp.sin(variable),
             sp.sec(variable)*sp.tan(variable): sp.sec(variable),
             sp.csc(variable)*sp.cot(variable): -sp.csc(variable)}
    result = 0
    for term in sp.Add.make_args(sp.expand(e)):
        coefficient, function = term.as_coeff_Mul()
        assert function in table, ('unsupported integral term', function)
        result += coefficient * table[function]
    assert g.reduced(sp.diff(result, variable) - e) == 0
    return result

def evaluated(text, variable):
    def replace(m):
        return '(' + str(primitive(expr(m[1]), variable)) + ')'
    text = re.sub(r'\\int\s+(.*?)\\text\{d\}\s*(?:\\theta|[xy])', replace, text)
    return expr(text.strip().rstrip('.,'))

def bank_check(question):
    fields = question.get(':question/answer-fields', [])
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/key'] == 'selection'
    ftype = f[':answer-field/type']
    assert (ftype.get(':db/ident') if isinstance(ftype, dict) else ftype) == ':answer-field.type/radio'
    choices = f[':answer-field/choices']
    assert len(choices) == 5
    correct = f[':answer-field/correct']
    cid = str(correct[':answer/id']) if isinstance(correct, dict) else correct[1]
    assert sum(str(a[':answer/id']) == cid for a in choices) == 1
    problem = question[':question/problem']
    integrand = g.integrand(problem)
    variables = integrand.free_symbols
    assert len(variables) == 1
    variable = next(iter(variables))
    values = [expr(a[':answer/value']) for a in choices]
    valid = [g.reduced(sp.diff(e, variable) - integrand) == 0 for e in values]
    assert sum(valid) == 1, ('ambiguous/incorrect source bank', valid)
    assert choices[valid.index(True)][':answer/id'] == cid or str(choices[valid.index(True)][':answer/id']) == cid
    assert not any(g.reduced(e-v) == 0 for i,e in enumerate(values) for v in values[:i])
    return variable, integrand

def solution_check(question):
    variable, integrand = bank_check(question)
    text = question[':question/worked-solution']
    displays = re.findall(r'\$\$\n(.*?)\n\$\$', text, re.S)
    assert len(displays) == 2
    count = 0
    for i, display in enumerate(displays):
        display = re.sub(r'\\(?:begin|end)\{aligned\}', '', display)
        previous = None
        for line in display.split(r'\\'):
            left, right = line.replace('&', '').split('=')
            if left.strip():
                lhs = evaluated(left, variable)
                previous = lhs
            else:
                assert previous is not None
                lhs = previous
            rhs = evaluated(right, variable)
            delta = g.reduced(lhs-rhs)
            assert not delta.free_symbols - {sp.Symbol('C', real=True)}, ('bad solution step', line, delta)
            if i == 1:
                assert g.reduced(sp.diff(rhs, variable)-integrand) == 0, line
            previous = rhs
            count += 1
    return count

def independent(record):
    q, m = record['question'], record['generation']
    assert record['knowledge_point']['db_id'] == g.KP_ID and record['knowledge_point']['id'] == g.KP_UUID
    level = q[':question/difficulty'].split('/')[-1]
    assert level in g.SUPPORTED_LEVELS
    assert record == g.generate(level, m['seed'], m['template'], m['parameters'], m['bank_profile'])
    assert parse(q[':question/problem']) == m['parameter_fingerprint']
    steps = solution_check(q)
    f = q[':question/answer-fields'][0]
    ids = [q[':question/id'], f[':answer-field/id']] + [a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(set(ids)) == len(ids)
    for x in ids:
        uuid.UUID(x)
    for text in (q[':question/problem'], q[':question/worked-solution']):
        assert text.count('$') % 2 == 0 and text.count('{') == text.count('}')
        assert '{a}' not in text and '{b}' not in text and '{sum}' not in text
    assert '{{' not in q[':question/problem']
    return steps

def checks(record):
    f = record['question'][':question/answer-fields'][0]
    return [{'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
             'purpose': 'Select every owned option through actual learner radio grading'} for a in f[':answer-field/choices']]

def main():
    import itertools
    source=json.loads((HERE/'source.json').read_text())
    qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    records=[];cases=[];reviews=[];steps=0
    for mid,t in g.TEMPLATES.items():
        r=g.generate(t['difficulty'],template=mid,parameters=t['parameters'])
        steps+=independent(r);records.append(r)
        if mid!='hard-extension':
            q=qs[mid];f=q[':question/answer-fields'][0]
            assert q[':question/problem']==r['question'][':question/problem']
            assert q[':question/worked-solution']==r['question'][':question/worked-solution']
            vals=[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert sorted(vals)==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
            assert vals[t['correct_index']]==f[':answer-field/correct'][':answer/value']
            cases.append({'source':mid,'profile':mid,'matched_values':5,'total_values':5,'matched_distractors':4,'total_distractors':4,'exact_prompt':True,'exact_solution':True,'missing_options':[],'extra_options':[]})
        else:
            q=qs['q-113958']
            assert r['question'][':question/problem']==q[':question/problem']
            assert r['question'][':question/worked-solution']==q[':question/worked-solution'].replace(r'\int sin\,',r'\int sin x\,')
            cases.append({'source':'q-113958','profile':mid,'exact_prompt':True,'solution':'Exact except justified missing-x repair in recall formula','bank':'Authored extension; no original field or options to replay'})
        reviews.append('## '+mid+' source replay / extension\n\n'+g.markdown(r))
        keys=list(t['parameters']);bound=range(2,10) if mid=='q-71663' else range(1,10)
        for vals in itertools.product(bound,repeat=len(keys)):
            p=dict(zip(keys,vals));r=g.generate(t['difficulty'],971,mid,p)
            steps+=independent(r)
            assert r['question']==g.generate(t['difficulty'],11,mid,p)['question']
            records.append(r)
    negative=0
    for level,mid,p in [('invalid',None,None),('easy','q-71663',{'a':1}),('hard','hard-extension',{'a':0,'b':1,'c':1}),('moderate','q-49121',{'a':10,'b':2})]:
        try:g.generate(level,template=mid,parameters=p)
        except ValueError:negative+=1
        else:raise AssertionError('invalid parameter accepted')
    for part in ('answer','solution'):
        r=copy.deepcopy(records[0]);q=r['question']
        if part=='answer':
            f=q[':question/answer-fields'][0];next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']='0'
        else:q[':question/worked-solution']=q[':question/worked-solution'].replace('=-5cot','=-8cot')
        try:solution_check(q)
        except (ValueError,AssertionError):negative+=1
        else:raise AssertionError('corruption accepted')
    sizes={}
    for level in g.SUPPORTED_LEVELS:
        rows=g.batch(level,1000,71);sizes[level]=len(rows)
        assert len({parse(r['question'][':question/problem']) for r in rows})==len(rows)
        reviews.append('## '+level+' variant\n\n'+g.markdown(rows[0]))
    save('source-cases.json',cases)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
    binary=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    (HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n')
    save('validation.json',{'status':'pass','source_basis':source['basis'],'lineage':source['lineage'],'supported_levels':list(g.SUPPORTED_LEVELS),'source_coverage':{'supported_banks_matched':4,'supported_bank_total':4,'matched_values':20,'total_values':20,'matched_distractors':16,'total_distractors':16,'missing_options':[],'extra_options':[],'hard':'Authored extension, not original bank fidelity'},'mathematics':{'records_checked':len(records),'rendered_solution_steps':steps,'negative_controls':negative,'finite_distinct_parameter_tasks':sizes},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'templates.json',binary)}})
    print(json.dumps({'status':'pass','finite_tasks':sizes,'records':len(records),'steps':steps}))

if __name__=='__main__':main()
