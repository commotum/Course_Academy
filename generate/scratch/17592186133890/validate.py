#!/usr/bin/env python3
"""Fail-closed prompt, endpoint, displayed stages, full-bank and native QA."""
import importlib.util, json, re, sys, subprocess, hashlib
from functools import lru_cache
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('cartesian_ftli',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def normalize(v):
    v=re.sub(r'\\operatorname\{(ln|sin|cos)\}',lambda m:'\\'+m[1],v)
    v=v.replace('\u2061','').replace(r'\u2061','').replace(r'\dfrac',r'\frac').replace(r'\left','').replace(r'\right','')
    v=re.sub(r'(?<=\})\\(ln|sin|cos)',r'\\cdot \\\1',v)
    v=v.replace('}(',r'}\cdot (')
    v=re.sub(r'(?<=\})(?=[a-z])',r'\\cdot ',v)
    v=re.sub(r'([xyz])(?=\{[xyz]\})',r'\1\\cdot ',v)
    v=re.sub(r'(?<=[xyz0-9)])\\(sin|cos|ln)',r'\\cdot \\\1',v)
    v=re.sub(r'\\(sin|cos|ln|log)\s*((?:[0-9]+)?\\pi|[a-z]|[0-9]+)',lambda m:'\\'+m[1]+'('+m[2]+')',v)
    matches=list(re.finditer(r'\\(?:sin|cos|ln|log)\(',v))
    for mm in reversed(matches):
        depth=1;end=mm.end()
        while depth:
            if v[end]=='(':depth+=1
            if v[end]==')':depth-=1
            end+=1
        v=v[:mm.start()]+'{'+v[mm.start():end]+'}'+v[end:]
    v=v.strip().rstrip('.,').replace(r'\pi','P')
    v=re.sub(r'(?<=[ePxyz])\s*(?=\()',r'\\cdot ',v)
    return v

@lru_cache(None)
def parse(v):
    z=parse_latex(normalize(v),backend='lark')
    if isinstance(z,Tree):
        vals=[child for child in z.children if isinstance(child,s.Basic)]
        assert vals and all(s.simplify(vals[0]-t)==0 for t in vals),(v,z)
        z=vals[0]
    return z.subs({a:({'e':s.E,'P':s.pi,'x':g.X,'y':g.Y,'t':g.T}.get(a.name,a)) for a in z.free_symbols})

def equal(a,b):return s.simplify(s.expand(a-b))==0

def check(r):
    q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
    f=parse(re.search(r'Let \$f\(x,y\)=(.*?)\.\$',prompt)[1])
    curve=re.search(r'curve \$(.*?)\$ for',prompt)[1];lhs,rhs=curve.split('=');relation=parse(lhs)-parse(rhs)
    var,a,b=re.search(r'\$([xy])\\in \[(.*?),(.*?)\]',prompt).groups();a,b=parse(a),parse(b)
    xt,yt=re.search(r'r\(t\)\s*=⟨(.*?),(.*?)⟩',sol).groups();xt,yt=parse(xt),parse(yt)
    assert equal(xt if var=='x' else yt,g.T)
    assert equal(relation.subs({g.X:xt,g.Y:yt}),0),(curve,xt,yt)
    A=(s.simplify(xt.subs(g.T,a)),s.simplify(yt.subs(g.T,a)));B=(s.simplify(xt.subs(g.T,b)),s.simplify(yt.subs(g.T,b)))
    endpoint_block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[0]
    displayed=re.findall(r'r\((.*?)\)\s*& =⟨(.*?),(.*?)⟩',endpoint_block)
    assert len(displayed)==2
    for (t,x,y),tt,P in zip(displayed,[a,b],[A,B]):
        assert equal(parse(t),tt) and equal(parse(x),P[0]) and equal(parse(y),P[1]),displayed
    D=s.simplify(f.subs({g.X:B[0],g.Y:B[1]})-f.subs({g.X:A[0],g.Y:A[1]}))
    tail=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1]
    rows=tail.split(r'\\')
    rhsrows=[row.split('& =')[1].strip().rstrip('.') for row in rows]
    coords=re.fullmatch(r'f\((.*?),(.*?)\)-f\((.*?),(.*?)\)',rhsrows[1]);assert coords,rhsrows[1]
    assert all(equal(parse(v),actual) for v,actual in zip(coords.groups(),(*B,*A)))
    for row in rhsrows[2:]:assert equal(parse(row),D),(r['generation']['template'],row,D,parse(row))
    field=q[':question/answer-fields'][0];answers=field[':answer-field/choices'];ids=[z[':answer/id'] for z in answers]
    assert len(answers)==5 and len(set(ids))==5 and field[':answer-field/correct'][1] in ids
    assert not any('cosh' in z[':answer/value'] or 'sinh' in z[':answer/value'] for z in answers)
    vals=[parse(z[':answer/value']) for z in answers]
    assert not any(equal(vals[i],vals[j]) for i in range(5) for j in range(i)),vals
    flags=[equal(v,D) for v in vals];assert flags.count(True)==1
    assert flags[ids.index(field[':answer-field/correct'][1])]
    for text in (prompt,sol):
        assert text.count('$')%2==0 and text.count('{')==text.count('}'),text
        assert not any(term in text for term in ['source_id','bank_profile','underidentified'])
    return len(rhsrows)-2

cases=[];review=[];fidelity=[];stages=0;engine=[]
def add_engine(r,label):
    f=r['question'][':question/answer-fields'][0]
    engine.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Select each displayed option through native radio grading'} for a in f[':answer-field/choices']]})

for name,q in g.QUESTIONS.items():
    level=g.LEVELS[name];case={'source_id':q[':question/id'],'math_academy_id':name,'template':name,'parameters':{'scale':1},'bank_profile':'observed','difficulty':level};cases.append(case)
    print('Checking source '+name,flush=True)
    r=g.generate(level,template=name,parameters=case['parameters'],profile='observed');stages+=check(r);review.append({'label':'original replay '+name,'record':r});add_engine(r,name+' original')
    f=q[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
    original=sorted(a[':answer/value'] for a in f[':answer-field/choices']);generated=sorted(a[':answer/value'] for a in gf[':answer-field/choices']);assert original==generated
    assert r['question'][':question/problem']==q[':question/problem']
    original_solution=q[':question/worked-solution']
    repaired=original_solution.replace(')-f(0,0)',')-f(0,-1)').replace(r'-{0}^{2}\cdot 0',r'-{0}^{2}\cdot (-1)') if name=='q-39749' else original_solution
    assert r['question'][':question/worked-solution']==repaired
    gc=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert gc[':answer/value']==f[':answer-field/correct'][':answer/value']
    fidelity.append({'source':name,'bank_choices_matched':5,'distractors_matched':4,'prompt_exact':True,'correct_designation_exact':True,'raw_solution_exact':name!='q-39749','repaired_solution_exact':True,'arithmetic_row_count':len(re.findall(r'& =',repaired[repaired.rindex(r'\begin{aligned}'):]))-2})
    for k in (2,-3):
        v=g.generate(level,template=name,parameters={'scale':k});stages+=check(v);review.append({'label':'generated observed-bank variant '+name+' scale '+str(k),'record':v});add_engine(v,name+' scale '+str(k))
        # Each original stage is visibly preserved, multiplied by coefficient.
        source_tail=repaired[repaired.rindex(r'\begin{aligned}'):];variant_tail=v['question'][':question/worked-solution'][v['question'][':question/worked-solution'].rindex(r'\begin{aligned}'):]
        assert len(source_tail.split(r'\\'))==len(variant_tail.split(r'\\'))
for level,name in g.DEFAULTS.items():
    seen=set()
    print('Checking authored '+level,flush=True)
    for seed in range(16):
        r=g.generate(level,seed);stages+=check(r);seen.add(r['generation']['parameter_fingerprint']);add_engine(r,level+' authored seed '+str(seed))
        if seed<2:review.append({'label':'generated authored '+level+' seed '+str(seed),'record':r})
        same=g.generate(level,seed+991,template=name,parameters=r['generation']['parameters']);assert same['question'][':question/id']==r['question'][':question/id']
        assert same['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
    assert len(seen)>=12,(level,len(seen))
# Invalid explicit parameters must fail rather than silently resample.
invalid=[('easy','authored_direct',{'k':1,'m':1,'c':0,'a':0,'b':2}),('moderate','authored_inverse',{'k':2,'m':1,'c':0,'a':1,'b':5}),('hard','authored_mixed',{'k':2,'ell':1,'m':1,'n':2,'c':2,'a':1,'b':2})]
for level,name,p in invalid:
    try:g.generate(level,template=name,parameters=p)
    except ValueError:pass
    else:raise AssertionError('Invalid explicit inputs accepted')
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
engine_report=json.loads((HERE/'engine-validation.json').read_text())
report={'passed':True,'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_questions':12,'original_complete_banks_matched':12,'source_choices_matched':60,'source_distractors_matched':48,'correct_designations_matched':12,'raw_solutions_exact':11,'minimally_repaired_solutions_exact':12,'source_repairs':[{'source':'q-39749','raw':'f(0,0) and 0^2*0','repair':'f(0,-1) and 0^2*(-1)','final_answer_unchanged':True}],'fidelity':fidelity,'displayed_arithmetic_stages_checked':stages,'generated_source_variants':24,'authored_variants_checked':48,'authored_levels':['easy','moderate','hard'],'identity_checks':48,'native':{k:engine_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'grader_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'parser_dependency':'read-only cached lark 1.2.2; SymPy '+s.__version__,'remaining_findings':['Observed homogeneous banks reproduce evidence but source error intent remains underidentified; excluded from authored defaults.'],'database_writes':0}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Source and generated review','Raw originals are retained in source.json; original replay q-39749 has the documented minimal correction. Each source profile has two changed-coefficient variants. Authored defaults are separately labeled.']
for item in review:
    name=item['record']['generation']['template'];lines+=['\n## '+item['label']]
    if item['label'].startswith('original'):
        q=g.QUESTIONS[name];lines+=['### Raw captured source',q[':question/problem'],q[':question/worked-solution'],'Source bank: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']), '### Normal generator replay']
    lines+=[g.markdown(item['record'])]
(HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
print(json.dumps({'passed':True,'banks':12,'choices':60,'stages':stages,'native':report['native']},indent=2))
