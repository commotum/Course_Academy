"""Complete source replay, independently parsed displayed math and actual grader."""
import hashlib
import importlib.util
import json
from functools import lru_cache
from pathlib import Path
import re
import subprocess
import sys
import sympy as s
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')

@lru_cache(None)
def expr(t):
    t=t.strip().rstrip('.,').replace('{)}',')').replace(r'\,','').replace(r'\cdot','*')
    t=t.replace(r'\dfrac',r'\frac')
    z=parse_latex(t,backend='lark')
    if isinstance(z,Tree):
        vals=[v for v in z.children if isinstance(v,s.Basic)]
        assert vals and all(s.simplify(v-vals[0])==0 for v in vals),(t,z)
        z=vals[0]
    return z.subs({v:g.x for v in z.free_symbols if v.name=='x'})

def equal(a,b):return s.simplify(a-b)==0

def fingerprint(q):
    equation=next(t for t in re.findall(r'\$([^$]+)\$',q[':question/problem']) if t.startswith('f(x)'))
    fun=expr(equation.split('=',1)[1].rstrip(','))
    text=q[':question/problem']
    shape='inner-derivative-fragment' if ')=2(' in text else 'reciprocal-radical-numerator-fragment' if r'\frac{\text{d}y}' in text else 'full-derivative'
    return hashlib.sha256((s.srepr(s.expand(fun))+'|'+shape).encode()).hexdigest()

def independent(rec):
    q,md=rec['question'],rec['generation'];m=md['template'];p=md['parameters']
    assert rec==g.generate(q[':question/difficulty'].split('/')[-1],md['seed'],m,p,md['bank_profile'])
    inner,fun,expected=g.model(m,p)
    eq=next(t for t in re.findall(r'\$([^$]+)\$',q[':question/problem']) if t.startswith('f(x)'))
    displayed_fun=expr(eq.split('=',1)[1].rstrip(','))
    assert equal(displayed_fun,fun),(m,p,'function')
    derivative=s.diff(displayed_fun,g.x)
    f=q[':question/answer-fields'][0];values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
    answer=next(expr(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert equal(answer,expected),(m,p,'answer',answer,expected)
    assert sum(equal(a,expected) for a in values)==1
    assert not any(equal(a,b) for i,a in enumerate(values) for b in values[i+1:])
    # Parse the displayed multiplier surrounding the blank as well as its answer.
    if m=='q-342875':assert equal(2*inner*answer,derivative)
    elif m=='q-342891':assert equal(answer/inner**s.Rational(3,2),derivative)
    else:assert equal(answer,derivative)
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
    assert len(blocks)==2
    # Check the displayed inner/outer derivatives before their multiplication.
    rows=blocks[0].split(r'\\')
    assert len(rows)==2
    inner_derivative=expr(rows[1].split('=')[-1])
    assert equal(inner_derivative,s.diff(inner,g.x))
    G=s.Symbol('G',positive=True)
    outer=G**({'q-107293':5,'q-342804':5,'q-71954':4,'q-71956':3,'q-342875':2}.get(m,1))
    if m=='q-342883':outer=s.sqrt(G)
    elif m=='q-342891':outer=1/s.sqrt(G)
    outer_derivative=expr(rows[0].split('=')[-1])
    outer_derivative=outer_derivative.subs({v:G for v in outer_derivative.free_symbols if v.name=='g'})
    assert equal(outer_derivative,s.diff(outer,G))
    # Both explicit chain-rule multiplication and final simplification must agree.
    parts=blocks[-1].split(' & =')[2:]
    for part in parts:
        rhs=part.split(r'\\')[0].strip().rstrip('.')
        z=expr(rhs);z=z.subs({v:inner for v in z.free_symbols if v.name=='g'})
        if m=='q-342891':
            # Real-domain proof authorizes this radical identity, without a
            # global force=True simplification across arbitrary branches.
            assert p['c']>=1 and equal(inner,2*(g.x**2-s.Rational(1,4))**2+p['c']-s.Rational(1,8))
            z=z.xreplace({s.sqrt(inner**3):inner**s.Rational(3,2),
                          (inner**3)**(-s.Rational(1,2)):inner**(-s.Rational(3,2))})
        assert equal(z,derivative),(m,p,'solution',rhs,z,derivative)
    for text in (q[':question/problem'],q[':question/worked-solution']):
        assert text.count('$')%2==0 and text.count('{')==text.count('}')
    assert q[':question/problem'].count('{{field-1}}')==(1 if f[':answer-field/type']==':answer-field.type/blank' else 0)
    assert fingerprint(q)==g.task_fingerprint(m,p)
    assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==len(values)

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    if f[':answer-field/type']==':answer-field.type/radio':
        return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete bank option through actual engine'} for a in f[':answer-field/choices']]
    ans=f[':answer-field/choices'][0][':answer/value']
    return [{'field_index':0,'submitted':t,'expected':out,'purpose':'Exact/equivalent fragment or wrong answer through actual engine'} for t,out in [(ans,'accepted'),('('+ans+')+0','accepted'),('0','rejected'),('('+ans+')+1','rejected')]]

def main():
    cases=[];records=[];review=[]
    for m,p in g.DEFAULTS.items():
        old=g.SOURCES[m];level=old[':question/difficulty'][':db/ident'].split('/')[-1]
        rec=g.generate(level,template=m,parameters=p);independent(rec)
        q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        cases.append({'source':m,'profile':rec['generation']['bank_profile'],'matched_values':len(f[':answer-field/choices']),'matched_distractors':len(f[':answer-field/choices'])-1,'total_distractors':len(f[':answer-field/choices'])-1,'complete_bank':True,'exact_prompt':True,'exact_solution':True,'missing':[],'extra':[]})
        variants=[g.generate(level,template=m,parameters=pp) for pp in g.parameters_for(m)]
        for variant in variants:independent(variant)
        records.extend(variants)
        review.append('## '+m+' original\n\n'+old[':question/problem']+'\n\n'+old[':question/worked-solution']+'\n\n### Exact replay\n\n'+g.markdown(rec)+'\n\n### Boundary variants\n\n'+g.markdown(variants[0])+'\n\n'+g.markdown(variants[-1]))
    assert len({fingerprint(r['question']) for r in records})==len(records)
    save('engine-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
    binary=HERE/'reference/check-engine'
    run=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
    (HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-cases.json',cases);save('review.json',{'variants':records});(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
    save('validation.json',{'status':'pass','source_basis':json.loads((HERE/'source.json').read_text())['basis'],'complete_source_banks':len(cases),'matched_values':sum(c['matched_values'] for c in cases),'matched_distractors':sum(c['matched_distractors'] for c in cases),'total_distractors':sum(c['total_distractors'] for c in cases),'missing_options':[],'extra_options':[],'exhaustive_independent_display_checks':len(records),'fidelity':'Exact original prompts, solutions, complete banks and answer shapes at every supported source; all finite parameters independently checked. Two incomplete sources excluded.','native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary]}})
    print(run.stdout.strip());print('Exhaustive finite-parameter validation:',len(records),'distinct tasks')
if __name__=='__main__':main()
