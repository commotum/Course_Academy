"""Independent displayed calculus, bounded variants and actual learner grading."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp

H=Path(__file__).resolve().parent
ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('cotangent_generator',H.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def check(r):
    q=r['question'];p=q[':question/problem'];s=q[':question/worked-solution']
    m=re.fullmatch(r"Find \$\{f\}\^\{'\}\(\\frac\{\\pi \}\{6\}\)\$ if \$f\(x\)=-([0-9]+)\\operatorname\{cot\}x\.\$\n\nAnswer: \{\{answer\}\}",p)
    assert m, p
    n=int(m[1]);x=sp.Symbol('x',real=True)
    # Independent sin/cos definition checks differentiation and evaluation.
    function=-n*sp.cos(x)/sp.sin(x)
    derivative=sp.trigsimp(sp.diff(function,x))
    assert sp.trigsimp(derivative-n/sp.sin(x)**2)==0
    target=sp.simplify(derivative.subs(x,sp.pi/6));assert target.is_Integer
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type']==':answer-field.type/blank' and f[':answer-field/key']=='answer'
    assert len(f[':answer-field/choices'])==1
    a=f[':answer-field/choices'][0];assert a[':answer/type']==':answer.type/math'
    assert sp.Rational(a[':answer/value'])==target
    assert f[':answer-field/correct']==[':answer/id',a[':answer/id']]
    # Read each rendered derivative/evaluation step, independently of metadata.
    initial=re.search(r'\\frac\{\\text\{d\}\}\{\\text\{d\}x\}\(-([0-9]+)\\operatorname\{cot\}x\)',s)
    signed=re.search(r'& =-([0-9]+)\(-\\csc\^\{2\}x\)',s)
    derived=re.search(r'& =([0-9]+)\\csc\^\{2\}x',s)
    evaluated=re.search(r'& =([0-9]+)\\csc\^\{2\}\(\\frac\{\\pi \}\{6\}\)',s)
    squared=re.search(r'& =([0-9]+)\{\(2\)\}\^\{2\}',s)
    final=re.search(r'& =([0-9]+)\.\\end\{aligned\}',s)
    assert all(z and int(z[1])==n for z in [initial,signed,derived,evaluated,squared])
    assert final and int(final[1])==target
    assert sp.simplify(1/sp.sin(sp.pi/6))==2
    assert q[':question/difficulty']==':question.difficulty/hard'
    assert r['generation']['mathematical_key']==g.mathematical_key(n)
    assert n in g.DOMAIN
    for text in [p,s]:assert text.count('$')%2==0 and text.count('{')==text.count('}')
    assert ':question/math-academy-id' not in q
    assert r==g.generate('hard',r['generation']['seed'],n=n)
    return n

def engine_item(label,r):
    n=check(r);value=4*n
    checks=[{'field_index':0,'submitted':str(value),'expected':'accepted','purpose':'Canonical numeric answer'},
            {'field_index':0,'submitted':r'\frac{'+str(2*value)+'}{2}','expected':'accepted','purpose':'Equivalent fraction'},
            {'field_index':0,'submitted':str(value)+'.0','expected':'accepted','purpose':'Equivalent decimal'},
            {'field_index':0,'submitted':str(-value),'expected':'rejected','purpose':'Wrong derivative sign'},
            {'field_index':0,'submitted':str(2*n),'expected':'rejected','purpose':'Missing square on cosecant'},
            {'field_index':0,'submitted':str(value+1),'expected':'rejected','purpose':'Wrong numeric answer'}]
    return {'label':label,'record':r,'checks':checks}

def main():
    rows=[g.generate('hard',1049,n=n) for n in g.DOMAIN]
    for r in rows:
        n=check(r)
        assert r['question']==g.generate('hard',103,n=n)['question']
    assert len({r['generation']['mathematical_key'] for r in rows})==24
    replay=g.generate('hard',0,n=6)
    reviewed=json.loads((H/'historical-hard-response.json').read_text())
    assert replay['question'][':question/problem']==reviewed['problem']
    assert replay['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']==reviewed['answer_fields'][0]['correct_value']=='24'
    expected=g.HARD[':question/worked-solution'].replace('{csc}',r'\csc').replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
    assert replay['question'][':question/worked-solution']==expected
    controls=0
    for level in ['easy','moderate','invalid']:
        try:g.generate(level)
        except ValueError:controls+=1
        else:raise AssertionError('Unsupported version band accepted')
    for n in [0,25,-6,True,1.5]:
        try:g.generate('hard',n=n)
        except ValueError:controls+=1
        else:raise AssertionError('Parameter boundary accepted')
    try:g.batch('hard',25,0)
    except ValueError:controls+=1
    else:raise AssertionError('Finite count exceeded')
    for key in [':question/problem',':question/worked-solution']:
        bad=copy.deepcopy(rows[0]);bad['question'][key]=bad['question'][key].replace('-1', '-2',1) if key.endswith('problem') else bad['question'][key].replace('=4.','=5.')
        try:check(bad)
        except AssertionError:controls+=1
        else:raise AssertionError('Corrupted displayed mathematics accepted')
    (H/'engine-input.json').write_text(json.dumps([engine_item(str(i),r) for i,r in enumerate(rows)],indent=2))
    subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
    engine=json.loads((H/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    (H/'review.md').write_text('## Original hard source\n\n'+g.HARD[':question/problem']+'\n\n'+g.HARD[':question/worked-solution']+'\n\n## Adapted source replay\n\n'+g.markdown(replay)+'\n\n## Variants at both bounds\n\n'+g.markdown(rows[0])+'\n\n'+g.markdown(rows[-1])+'\n')
    report={'passed':True,'source_basis':g.SOURCE['basis'],'supported_levels':['hard'],
            'finite_distinct_tasks':24,'exhaustive_mathematical_checks':24,'negative_controls':controls,
            'hard_source_function_and_solution_replayed':True,'source_numeric_response_evidence_replayed':True,
            'source_bank_fidelity':'Unavailable: original hard source has no saved field or distractors; explicitly authored blank adaptation',
            'observed_hard_source_banks':0,'invented_distractors':0,'grading':{k:engine[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},
            'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),
            'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'source.edn',H/'historical-hard-response.json',H/'check-engine',H/'capability.json']}}
    (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
