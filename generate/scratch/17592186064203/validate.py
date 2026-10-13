"""Exact rendered polynomial mathematics, frozen bank fidelity and native grading."""
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

def save(name, x):
    (HERE/name).write_text(json.dumps(x, indent=2, default=str)+'\n')

def parse(text):
    return g.fingerprint_text(text)

def bank_check(q):
    fs = q[':question/answer-fields']
    assert len(fs) == 1
    f = fs[0]
    ft = f[':answer-field/type']
    assert (ft.get(':db/ident') if isinstance(ft,dict) else ft) == ':answer-field.type/radio'
    assert f[':answer-field/key'] == 'selection'
    choices = f[':answer-field/choices']
    assert len(choices) == 5
    cid = f[':answer-field/correct']
    cid = str(cid[':answer/id']) if isinstance(cid,dict) else cid[1]
    e = g.integrand(q[':question/problem'])
    values = [g.expression(a[':answer/value']) for a in choices]
    valid = [sp.expand(sp.diff(a,g.X)-e) == 0 for a in values]
    assert sum(valid) == 1 and str(choices[valid.index(True)][':answer/id']) == cid
    assert len({sp.srepr(sp.expand(a)) for a in values}) == 5
    return e

def evaluated(text):
    text = text.strip().rstrip('.,').replace('✓','')
    # Evaluate the actual integrals and derivative calls in rendered equations.
    text = re.sub(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\[([^\[\]]*)\]',
        lambda m: '('+str(sp.diff(g.expression(m[1]),g.X))+')', text)
    text = re.sub(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\(([^()]*)\)',
        lambda m: '('+str(sp.diff(g.expression(m[1]),g.X))+')', text)
    text = re.sub(r'\\int\s*(.*?)\\text\{d\}([xu])',
        lambda m: '('+str(sp.integrate(g.expression(m[1]),g.X if m[2]=='x' else g.U))+')', text)
    return g.expression(text)

def solution_check(q):
    e = bank_check(q)
    displays = re.findall(r'\$\$\n(.*?)\n\$\$', q[':question/worked-solution'], re.S)
    assert len(displays) == 3
    let = re.search(r'Let \$u=(.*?)\.\$', q[':question/worked-solution'])
    assert let
    inner = g.expression(let[1])
    slope = sp.diff(inner,g.X)
    assert slope != 0 and sp.diff(slope,g.X) == 0
    slope_latex = sp.latex(slope)
    expected = r'\frac{\text{d}u}{\text{d}x}='+slope_latex+r'\,⟹\,\text{d}x='+sp.latex(1/slope)+r'\text{d}u.'
    assert re.sub(r'\s','',displays[0]) == re.sub(r'\s','',expected), (displays[0],expected)
    steps = 1
    for display in displays[1:]:
        display = re.sub(r'\\(?:begin|end)\{aligned\}', '', display)
        previous = None
        for line in display.split(r'\\'):
            left,right = line.replace('&','').split('=')
            lhs = evaluated(left) if left.strip() else previous
            assert lhs is not None
            rhs = evaluated(right)
            # The substitution u=inner is valid across every real interval.
            delta = sp.expand((lhs-rhs).subs(g.U,inner))
            if r'\int' in left or r'\int' in right:
                # Independent indefinite integration can choose different
                # additive constants before/after the u substitution.
                assert sp.diff(delta,g.X) == 0, (line,delta)
            else:
                assert delta in (0,g.C,-g.C), (line,delta)
            previous = rhs
            steps += 1
    assert sp.expand(previous.subs(g.U,inner)-e) == 0
    return steps

def independent(r):
    q,m = r['question'],r['generation']
    assert r['knowledge_point']['db_id'] == g.KP_ID and r['knowledge_point']['id'] == g.KP_UUID
    level = q[':question/difficulty'].split('/')[-1]
    assert r == g.generate(level,m['seed'],m['template'],m['parameters'],m['bank_profile'])
    assert parse(q[':question/problem']) == m['parameter_fingerprint']
    f=q[':question/answer-fields'][0]
    ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(set(ids)) == len(ids)
    for i in ids:uuid.UUID(i)
    for text in (q[':question/problem'],q[':question/worked-solution']):
        assert text.count('$')%2 == 0 and text.count('{') == text.count('}')
    return solution_check(q)

def checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],
        'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
        'purpose':'Every field-owned option tested with actual learner grade_field'} for a in f[':answer-field/choices']]

def main():
    originals={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
    cases=[];rows=[];review=[];steps=0
    for mid,t in g.TEMPLATES.items():
        q=originals[mid];r=g.generate(t['difficulty'],template=mid,parameters={'b':t['source_b']})
        steps+=independent(r)
        assert r['question'][':question/problem']==q[':question/problem']
        assert r['question'][':question/worked-solution']==q[':question/worked-solution']
        bank=r['question'][':question/answer-fields'][0];old=q[':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in bank[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
        assert bank[':answer-field/choices'][t['correct_index']][':answer/value']==old[':answer-field/correct'][':answer/value']
        cases.append({'source':mid,'profile':mid,'matched_values':5,'total_values':5,'matched_distractors':4,'total_distractors':4,'exact_prompt':True,'exact_solution':True,'missing_options':[],'extra_options':[]})
        variant=g.generate(t['difficulty'],71,mid,{'b':20})
        review.append('## '+mid+' original and replay\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nGenerated source replay:\n\n'+g.markdown(r)+'\n\nChanged constant variant:\n\n'+g.markdown(variant))
        for b in g.DOMAIN:
            r=g.generate(t['difficulty'],71,mid,{'b':b});steps+=independent(r);rows.append(r)
            assert r['question']==g.generate(t['difficulty'],72,mid,{'b':b})['question']
    negative=0
    for level,profile,p in [('hard',None,None),('invalid',None,None),('easy','q-113486',{'b':0}),('easy','q-113486',{'b':21}),('easy','q-113486',{'b':True}),('easy','q-113492',{'b':5}),('easy','q-113486',{'c':2})]:
        try:g.generate(level,template=profile,parameters=p)
        except ValueError:negative+=1
        else:raise AssertionError('Invalid parameters accepted')
    for part in ('answer','solution'):
        r=copy.deepcopy(rows[0]);q=r['question']
        if part=='answer':
            f=q[':question/answer-fields'][0]
            next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']='0'
        else:q[':question/worked-solution']=q[':question/worked-solution'].replace('48','49')
        try:solution_check(q)
        except (AssertionError,ValueError):negative+=1
        else:raise AssertionError('Corruption accepted')
    sizes={level:len(g.batch(level,1000,71)) for level in g.SUPPORTED_LEVELS}
    for level,n in sizes.items():assert len({parse(r['question'][':question/problem']) for r in g.batch(level,n,72)})==n
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(rows)])
    subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-cases.json',cases)
    (HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
    save('validation.json',{'status':'pass','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],
        'source_coverage':{'supported_banks_matched':5,'supported_bank_total':5,'matched_values':25,'total_values':25,'matched_distractors':20,'total_distractors':20,'missing_options':[],'extra_options':[],'excluded_incomplete_sources':['q-12015','q-12493']},
        'mathematics':{'bounded_instances_checked':len(rows),'rendered_solution_steps':steps,'negative_controls':negative,'finite_distinct_parameter_tasks':sizes},
        'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},
        'fidelity':'Exact source prompts, solution text, full banks and correct designations; constants are changed only inside the complete linear expression.',
        'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'templates.json',HERE/'check-engine',HERE/'engine-build.json',HERE/'replenish.py')}})
    print(json.dumps({'status':'pass','instances':len(rows),'steps':steps,'finite_tasks':sizes}))

if __name__=='__main__':main()
