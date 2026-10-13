#!/usr/bin/env python3
"""Read printed functions, vectors and ordered rows independently; native grader."""
import importlib.util,json,re,sys,subprocess,hashlib,difflib,itertools,uuid
from pathlib import Path
from functools import lru_cache
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
I,J=s.symbols('axis_i axis_j',real=True)

@lru_cache(None)
def parse(tex):
    q=tex.strip().rstrip('.,').replace('⁡','').replace(r'\text{ }','').replace(r'\left','').replace(r'\right','')
    q=re.sub(r'\\operatorname\{(\w+)\}',r'\\\1',q)
    q=re.sub(r'\{(sin|cos|tan|sec)\}',r'\\\1',q)
    q=q.replace(r'\,i',' axis_i ').replace(r'\,j',' axis_j ').replace(r'\cdot',' * ')
    # Source-style bare function arguments, including pi*t and xy.
    q=re.sub(r'\\(sin|cos|tan|sec|ln|arctan)(?:\^\{(-?\d+)\})?\s*((?:-?\d+)?\\pi\s*t|(?:-?\d+)?t|xy|x|y)(?![A-Za-z])',lambda m:'('+m[1]+'('+m[3]+')'+('**('+m[2]+')' if m[2] else '')+')',q)
    def group(text,start):
        assert text[start]=='{',(text,start)
        depth=1;i=start+1
        while depth:
            if text[i]=='{':depth+=1
            if text[i]=='}':depth-=1
            i+=1
        return text[start+1:i-1],i
    while r'\frac' in q:
        start=q.rfind(r'\frac');a,end=group(q,start+5);b,last=group(q,end);q=q[:start]+'(('+a+')/('+b+'))'+q[last:]
    q=q.replace(r'\pi',' pi ').replace(r'\ln','log').replace('ln(','log(').replace(r'\arctan','atan').replace('arctan(','atan(')
    for f in ('sin','cos','tan','sec'):q=q.replace('\\'+f,f)
    q=q.replace('^','**').replace('{','(').replace('}',')')
    q=re.sub(r'\be\b','E',q)
    if '\\' in q:raise AssertionError(('Unparsed command',tex,q))
    return parse_expr(q,local_dict={'x':g.X,'y':g.Y,'t':g.T,'E':s.E,'pi':s.pi,'axis_i':I,'axis_j':J,'log':s.log,'atan':s.atan,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec},transformations=standard_transformations+(implicit_multiplication_application,))

def eq(a,b):
    delta=a-b;delta=delta.xreplace({e:(s.sin(e.args[0])/s.cos(e.args[0]) if e.func==s.tan else 1/s.cos(e.args[0])) for e in delta.atoms(s.tan,s.sec)});E=s.Symbol('oracle_exp',positive=True)
    delta=delta.xreplace({e:E**(e.args[0]/g.T) for e in delta.atoms(s.exp) if (e.args[0]/g.T).is_Integer})
    # All displayed oracle comparisons here need no trig identities; retain a
    # separate exact trig simplification fallback for complete bank eligibility.
    z=s.cancel(delta)
    if z==0:return True
    trig=z.atoms(s.sin,s.cos)
    if any(z.has(s.sin(e.args[0])**2) and z.has(s.cos(e.args[0])**2) for e in trig):return s.trigsimp(z)==0
    return False
def vecparse(v):
    z=s.expand(parse(v));assert z.subs({I:0,J:0})==0,(v,z)
    a=z.coeff(I);b=z.coeff(J);assert eq(z,a*I+b*J),(v,z)
    return a,b

def blocks(q):return re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
def rows(b):return [row.split('& =')[1].strip() for row in b.split(r'\\')]
def formatting(text):
    assert text.count('$$')==10,(text.count('$$'),text)
    inline=re.sub(r'\$\$.*?\$\$','',text,flags=re.S);assert inline.count('$')%2==0
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text
    assert r'\pit' not in text

def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];uuid.UUID(q[':question/id']);prompt=q[':question/problem'];sol=q[':question/worked-solution'];formatting(sol)
    # Derive from actual printed inputs, not generation metadata.
    F=re.search(r'\$f\(x,\s*y\)\s*=\s*(.*?)\$',prompt)[1];curve=re.search(r'\$r\(t\)\s*=\s*(.*?)\$',prompt)[1].rstrip(',')
    f=parse(F)
    if r'\,i' in curve:u,v=vecparse(curve)
    else:
        u,v=re.fullmatch(r'(.*?)i \+ (.*?)j',curve).groups();u,v=parse(u),parse(v)
    fx,fy=s.diff(f,g.X),s.diff(f,g.Y);gg=[z.subs({g.X:u,g.Y:v},simultaneous=True) for z in (fx,fy)];dd=[s.diff(u,g.T),s.diff(v,g.T)]
    expected=s.diff(f.subs({g.X:u,g.Y:v},simultaneous=True),g.T)
    if r['generation']['template'] in ('log_power','log_cos'):
        argument=f.args[0].subs({g.X:u,g.Y:v},simultaneous=True)
        positive_side=s.simplify(argument.subs(g.T,s.Rational(1,10))).is_positive
        negative_side=s.simplify(argument.subs(g.T,-s.Rational(1,10))).is_positive
        assert positive_side is True and negative_side in (True,False)
        domain=r['generation']['domain']
        if r['generation']['template']=='log_power':assert domain==('t != 0' if negative_side else 't>0')
        else:assert ('*t>0' in domain)==(not negative_side)

    bb=blocks(q);assert len(bb)==4
    gr=rows(bb[0]);assert len(gr)>=2 and r'\frac{∂}{∂x}' in gr[0] and r'\frac{∂}{∂y}' in gr[0]
    operands=re.findall(r'\\frac\{∂\}\{∂([xy])\}(.*?)\\,[ij]',gr[0])
    assert len(operands)==2 and [v for v,e in operands]==['x','y']
    assert all(eq(parse(e),f) for v,e in operands),(F,operands)
    for val in gr[1:]:assert all(eq(z,w) for z,w in zip(vecparse(val),(fx,fy))),(F,val,(fx,fy))
    for val in rows(bb[1]):assert all(eq(z,w) for z,w in zip(vecparse(val),gg)),(F,curve,val,gg)
    dr=rows(bb[2]);assert len(dr)==2
    # Read each printed derivative argument; formal operator must precede both components.
    args=re.findall(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\((.*?)\)\\,[ij]',dr[0])
    assert len(args)==2,(dr[0],args)
    assert eq(parse(args[0]),u) and eq(parse(args[1]),v),(args,u,v)
    assert all(eq(z,w) for z,w in zip(vecparse(dr[1]),dd))
    tail=rows(bb[3]);assert tail[0]=='∇f(r(t))\\cdot {r}^{′}(t)' and len(tail)>=4
    lhs,rhs=tail[1].split(r'\cdot');gv=vecparse(lhs[1:-1]);dv=vecparse(rhs.strip()[1:-1]);assert all(eq(z,w) for z,w in zip(gv,gg)) and all(eq(z,w) for z,w in zip(dv,dd))
    for val in tail[2:]:assert eq(parse(val),expected),(r['generation']['template'],val,parse(val),expected)
    # Workload is read back from printed functions.
    if r['generation']['template']=='mixed_polynomial':assert len(s.Add.make_args(s.expand(fx)))==2 and fy!=0
    if r['generation']['template']=='atan_squared':assert f.has(s.atan) and s.diff(f,g.Y)!=0 and len(gr)==3 and len(rows(bb[1]))==2
    if r['generation']['template']=='atan_squared':assert r'\cdot 0' in gr[1] and '0{y}^{2}' in gr[1]
    field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio';assert field[':answer-field/key']=='selection'
    answers=field[':answer-field/choices'];assert len(answers)==5
    uuid.UUID(field[':answer-field/id'])
    ids=[a[':answer/id'] for a in answers]
    for owned_id in ids:uuid.UUID(owned_id)
    assert len(set(ids))==5
    actual=[parse(a[':answer/value']) for a in answers];assert not any(eq(z,w) for i,z in enumerate(actual) for w in actual[:i])
    correct=field[':answer-field/correct'][1];assert field[':answer-field/correct'][0]==':answer/id' and correct in ids
    assert sum(eq(z,expected) for z in actual)==1
    assert eq(actual[ids.index(correct)],expected)
    return actual

def normalized(v):return re.sub(r'\s+','',v)
def main():
    source_cases=[];replay=[];review=[];fidelity=[];engine=[]
    for name,p in g.ORIGINAL.items():
        r=g.generate('easy',template=name,parameters=p,profile='observed');check(r);raw=g.QUESTIONS[g.TEMPLATES[name]]
        source_cases.append({'source_id':raw[':question/id'],'source_db_id':raw[':db/id'],'math_academy_id':g.TEMPLATES[name],'difficulty':'easy','authored_level_assignment':name=='log_cos','template':name,'parameters':p,'bank_profile':'raw_observed' if name=='log_cos' else 'observed'})
        if name=='log_cos':
            evidence=g.generate('easy',template=name,parameters=p,profile='raw_observed')
            assert ':question/difficulty' not in evidence['question'] and ':question/worked-solution' not in evidence['question']
            assert ':answer-field/correct' not in evidence['question'][':question/answer-fields'][0]
            assert evidence['question'][':question/problem']==raw[':question/problem']
            assert sorted(a[':answer/value'] for a in evidence['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in raw[':question/answer-fields'][0][':answer-field/choices'])
            assert evidence['generation']['evidence_only'] and evidence['generation']['ineligible_for_practice']
            (HERE/'raw-anomaly-replay.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n')
        bank=[a[':answer/value'] for a in raw[':question/answer-fields'][0][':answer-field/choices']];out=[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
        assert len(bank)==len(out)==5
        for z in bank:assert sum(eq(parse(z),parse(w)) for w in out)==1
        original_correct=raw[':question/answer-fields'][0].get(':answer-field/correct');designation=None
        if original_correct:
            cf=r['question'][':question/answer-fields'][0];c=next(a for a in cf[':answer-field/choices'] if a[':answer/id']==cf[':answer-field/correct'][1]);assert eq(parse(c[':answer/value']),parse(original_correct[':answer/value']));designation=True
        exactsol=None
        if raw.get(':question/worked-solution'):
            assert normalized(raw[':question/worked-solution'])==normalized(r['question'][':question/worked-solution']),(name,'solution fidelity')
            exactsol=raw[':question/worked-solution']==r['question'][':question/worked-solution']
        assert normalized(raw[':question/problem'])==normalized(r['question'][':question/problem']),(name,'prompt fidelity')
        fidelity.append({'template':name,'source_id':raw[':question/id'],'complete_bank_matched':True,'choices_matched':5,'correct_designation_matched':designation,'prompt_raw_exact':raw[':question/problem']==r['question'][':question/problem'],'solution_raw_exact':exactsol,'bank_raw_exact':sorted(bank)==sorted(out),'presentation_normalized_complete_solution':bool(exactsol is not None)})
        replay.append(r)
        for i in range(2):review.append({'kind':'generated observed-profile variant','record':g.generate('easy',31+i,template=name,profile='observed')})
    # All authored levels/templates, changed parameter and signed-negative mathematical stages.
    math_checks=0;task_sets={l:set() for l in ('easy','moderate','hard')}
    for l in task_sets:
        for name in [n for n in g.TEMPLATES if g.LEVEL[n]==l]:
            params_catalog=([dict(a=a,b=b,c=c,k=k) for a,b,c,k in itertools.product(range(1,4),range(1,4),range(1,4),range(1,3))] if l=='moderate' else [dict(a=a,k=k,l=j) for a,k,j in itertools.product(range(1,5),range(2,6),range(2,6))] if l=='hard' else [None]*8)
            for seed,pp in enumerate(params_catalog):
                r=g.generate(l,seed,template=name,parameters=pp);check(r);math_checks+=1;task_sets[l].add(r['generation']['mathematical_fingerprint'])
                p=r['generation']['parameters'];rr=g.generate(l,seed+888,template=name,parameters=p);assert rr['question'][':question/id']==r['question'][':question/id']
                assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
                if seed<2:review.append({'kind':'generated authored-default variant','record':r})
    assert len(task_sets['moderate'])==54 and len(task_sets['hard'])==64
    # Explicit bounds cannot bypass level demand.
    for l,n,p in [('moderate','mixed_polynomial',{'a':0,'b':1,'c':1,'k':1}),('moderate','mixed_polynomial',{'a':1,'b':1,'c':4,'k':1}),('hard','atan_squared',{'a':1,'k':1,'l':2}),('hard','atan_squared',{'a':5,'k':2,'l':2}),('easy','polylog',{'a':2,'b':1,'c':3,'n':3})]:
        try:g.generate(l,template=n,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('Bounds accepted',l,n,p))
    for idx,r in enumerate(replay+[a['record'] for a in review]):
        check(r);field=r['question'][':question/answer-fields'][0];cid=field[':answer-field/correct'][1]
        engine.append({'label':str(idx)+':'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Every owned choice: native ID grading; mathematics separately verified'} for a in field[':answer-field/choices']]})
    (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
    binary=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    md=['# Review: originals and explicitly generated variants','Source math basis 1356; six full radio banks, five rated easy and one unrated.']
    for raw,r in zip(g.QUESTIONS.values(),replay):
        md+=['## Original '+raw[':question/math-academy-id'],raw[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in raw[':question/answer-fields'][0][':answer-field/choices']),raw.get(':question/worked-solution','[No captured solution or correct designation.]'),('### Parameterized completed replay — authored solution/level/designation' if r['generation']['template']=='log_cos' else '### Parameterized exact replay'),g.markdown(r)]
    for a in review:md+=['## '+a['kind']+' — '+a['record']['generation']['template'],g.markdown(a['record'])]
    (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
    report={'status':'pass','version':g.VERSION,'implementation_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_snapshot_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'database_writes':0,'practice_sources':6,'raw_exact_prompt_count':sum(f['prompt_raw_exact'] for f in fidelity),'raw_exact_bank_count':sum(f['bank_raw_exact'] for f in fidelity),'raw_exact_solution_count':sum(f['solution_raw_exact'] is True for f in fidelity),'complete_source_banks_matched':6,'source_choices_matched':30,'source_choices_total':30,'matched_correct_designations':5,'captured_correct_designations':5,'missing_designation_inferred':1,'observed_full_solutions_matched':5,'observed_full_solutions_total':5,'fidelity':fidelity,'authored_math_checks':math_checks,'unique_sample_tasks':{l:len(v) for l,v in task_sets.items()},'exhaustive_eligible_catalogues':{'moderate':54,'hard':64},'native_grading':json.loads((HERE/'engine-report.json').read_text()),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'known_limitations':['No captured worked solution, difficulty or correct designation for q-95056; easy/solution/correct are authored and separately counted.','Some observed scalar distractor interpretations underdetermined; their complete parameterized profiles remain explicit replay profiles.'],'plot_rating':'none','unresolved_findings':[]}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('native_grading','fidelity')},indent=2))
if __name__=='__main__':main()
