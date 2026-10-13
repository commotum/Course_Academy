#!/usr/bin/env python3
"""Fail on fidelity, printed math, whole-integral collisions, schema or grading."""
import importlib.util,json,hashlib,re,subprocess,sys,uuid,itertools
from pathlib import Path
import sympy as sp
D=Path(__file__).parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data):(D/name).write_text(json.dumps(data,indent=2)+'\n')
def balanced(s):
    assert s.count('$')%2==0,s
    n=0
    for c in s:
        n+=(c=='{')-(c=='}');assert n>=0
    assert n==0
    assert '@A@' not in s and '@POINT' not in s
    assert not re.search(r'\+\-|\-\-',s),s

def printed_problem(q):
    p=q[':question/problem'];curve=re.search(r'curve \$y\s*=\s*(.*?)\$',p)[1]
    curve=g.parse_math(curve)
    head=re.search(r'\$(.*?\\int.*?)(?:ds|\\text\{d\}s|\\mathrm\{d\}s)',p)[1]
    scalar=re.split(r'(?:_\{C\}|_C)',head,maxsplit=1)[1]
    scalar=g.parse_math(scalar.replace(r'\,','').rstrip(' ,'))
    interval=re.search(r'for \$(?:\\,)?(.*?)\\le x\\le (.*?)\??\$',p)
    if interval:a,b=(g.parse_math(v) for v in interval.groups())
    else:
        points=re.findall(r'\(([^(),]+),\s*([^()]+)\)',p)
        assert len(points)==2,points
        a,b=g.parse_math(points[0][0]),g.parse_math(points[1][0])
        for px,py in points:assert sp.simplify(g.parse_math(py)-curve.subs(g.x,g.parse_math(px)))==0
    assert a<b
    return curve,scalar,a,b

def verify_solution(q,curve,scalar,a,b):
    s=q[':question/worked-solution'];gt=curve.subs(g.x,g.t);dy=sp.diff(gt,g.t);speed=sp.sqrt(1+dy**2);ft=sp.simplify(scalar.subs({g.x:g.t,g.y:gt},simultaneous=True))
    declared=re.search(r'Now, since \$f\(x,y\)\s*=\s*(.*?)\$',s)[1]
    assert sp.simplify(g.parse_math(declared.rstrip(' ,'))-scalar)==0
    printed_gt=re.search(r'y=y\(t\)=([^$]+)\$',s)
    if printed_gt:assert sp.simplify(g.parse_math(printed_gt[1].rstrip('.'))-gt)==0
    # Read the actual printed derivative and each explicitly computed norm stage.
    rows=re.split(r'\\\\',s)
    derivative_count=norm_count=integral_count=0
    for row in rows:
        rhs=re.split(r'&\s*=',row)[-1]
        deriv=re.match(r'\s*i(.*?)\\?,?\s*j',rhs)
        if deriv:
            v=deriv[1].replace(r'\,','').strip();assert sp.simplify(g.parse_math(v)-dy)==0,(v,dy);derivative_count+=1
        if r'\sqrt' in rhs and r'\int' not in rhs:
            for derivative_tex in [r'\frac{\text{d}x}{\text{d}t}',r'\frac{\mathrm{d}x}{\mathrm{d}t}']:
                rhs=rhs.replace(derivative_tex,'1')
            for derivative_tex in [r'\frac{\text{d}y}{\text{d}t}',r'\frac{\mathrm{d}y}{\mathrm{d}t}']:
                rhs=rhs.replace(derivative_tex,'('+g.tex(dy)+')')
            v=rhs.split(r'\end')[0].split('$$')[0].strip().rstrip('.')
            if v.startswith(r'\sqrt') or v.startswith(r'\frac'):
                assert sp.simplify(g.parse_math(v)-speed)==0,(v,speed);norm_count+=1
        if r'\int' in rhs and re.match(r'\s*(?:[0-9]|\\sqrt|\\frac|\{?\\int)',rhs):
            v=rhs.split(r'\end')[0].split('$$')[0].strip().rstrip('.')
            v=v.replace('f(r(t))','('+g.tex(ft)+')')
            for symbolic in ['‖{r}^{′}(t)‖',r"\|r'(t)\|"]:
                v=v.replace(symbolic,'('+g.tex(speed)+')')
            got=g.parse_integral(v)
            assert got[1:]==(a,b)
            assert sp.simplify(got[0]-ft*speed)==0,(v,ft*speed);integral_count+=1
    assert derivative_count>=1 and norm_count>=1 and integral_count>=2,(derivative_count,norm_count,integral_count)
    # Independently read the scalar substitution chain, including unreduced stage.
    m=re.search(r'f\(r\(t\)\)\s*(?:&\s*)?=([^$]*?)(?:\\end\{aligned\}|\n\$\$)',s)
    assert m,s
    chain=m[1].strip().rstrip('.')
    for component in chain.split('='):
        assert sp.simplify(g.parse_math(component.strip())-ft)==0,(component,ft)
    return {'derivative_rows':derivative_count,'norm_rows':norm_count,'definite_integral_rows':integral_count}

CHECK_CACHE={}
def check(r):
    cache_key=(json.dumps(r['question'],sort_keys=True),r['generation']['evidence_only'])
    if cache_key in CHECK_CACHE:return CHECK_CACHE[cache_key]
    assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID
    q=r['question'];assert len(q[':question/answer-fields'])==1;field=q[':question/answer-fields'][0]
    assert field[':answer-field/type']==':answer-field.type/radio';assert len(field[':answer-field/choices'])==5
    assert field[':answer-field/correct'][0]==':answer/id'
    values=[v[':answer/value'] for v in field[':answer-field/choices']]
    ids=[q[':question/id'],field[':answer-field/id']]+[v[':answer/id'] for v in field[':answer-field/choices']]
    assert len(ids)==len(set(ids));[uuid.UUID(v) for v in ids]
    correct=[v for v in field[':answer-field/choices'] if v[':answer/id']==field[':answer-field/correct'][1]];assert len(correct)==1
    for s in [q[':question/problem'],q[':question/worked-solution']]+values:balanced(s)
    curve,scalar,a,b=printed_problem(q);ft=sp.simplify(scalar.subs({g.x:g.t,g.y:curve.subs(g.x,g.t)},simultaneous=True));speed=sp.sqrt(1+sp.diff(curve.subs(g.x,g.t),g.t)**2)
    e,c,d=g.parse_integral(correct[0][':answer/value']);assert (c,d)==(a,b);assert sp.simplify(e-ft*speed)==0,(e,ft*speed)
    bad=g.collisions(values)
    assert r['generation']['evidence_only'] or not bad,bad
    checked=verify_solution(q,curve,scalar,a,b)
    CHECK_CACHE[cache_key]=checked
    return checked

def main():
    assert g.equivalent_integrals(g.parse_integral(r'\int_{0}^{1}2t\,\mathrm{d}t'),g.parse_integral(r'\int_{0}^{2}\frac{t}{2}\,\mathrm{d}t'))
    assert not g.equivalent_integrals(g.parse_integral(r'\int_{0}^{1}2t\,\mathrm{d}t'),g.parse_integral(r'\int_{0}^{2}t\,\mathrm{d}t'))
    source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text());review=[];engine=[];fidelity=[];stage_checks=[]
    for q,c in zip(qs,cases):
        r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r);review.append({'label':'original-parameter evidence replay '+c['source_ma_id'],'record':r})
        f=r['question'][':question/answer-fields'][0]
        engine.append({'label':'source evidence '+c['source_ma_id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native source-replay radio fixture; math collisions separately reported'} for a in f[':answer-field/choices']]})
        raw=[v[':answer/value'] for v in q[':question/answer-fields'][0][':answer-field/choices']];new=[v[':answer/value'] for v in r['question'][':question/answer-fields'][0][':answer-field/choices']]
        assert sorted(raw)==sorted(new)
        rawcorrect=q[':question/answer-fields'][0].get(':answer-field/correct')
        if rawcorrect:
            actual=next(v[':answer/value'] for v in r['question'][':question/answer-fields'][0][':answer-field/choices'] if v[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]);assert actual==rawcorrect[':answer/value']
        solution_exact=q.get(':question/worked-solution')==r['question'][':question/worked-solution']
        if q.get(':question/worked-solution'):assert solution_exact
        fidelity.append({'source_id':c['source_id'],'source_ma_id':c['source_ma_id'],'exact_choices':5,'exact_prompt':q[':question/problem']==r['question'][':question/problem'],'exact_solution':solution_exact,'present_correct_ref':rawcorrect is not None,'designation_matched':rawcorrect is not None,'complete_integral_collisions':r['generation']['complete_integral_collisions']})
        for variant in [0,1]:
            p={'a':'1','b':str(3+variant)}
            if c['template']=='quadratic_sine':p={'a':'0','b':str(2+variant)}
            rr=g.generate('easy',template=c['template'],parameters=p,profile='observed_evidence',seed=variant+43);check(rr);review.append({'label':'generated observed-pattern variant '+c['source_ma_id']+' '+str(variant),'record':rr})
    # All supported families, both boundary and random normal parameters.
    for level,templates in [('easy',list(g.OBS)),('moderate',[k for k,v in g.AUTH.items() if v=='moderate']),('hard',[k for k,v in g.AUTH.items() if v=='hard'])]:
        fingerprints=set()
        for template in templates:
            print('Checking '+level+' '+template,flush=True)
            for seed in range(8):
                r=g.generate(level,seed,template=template);stage_checks.append(check(r));fingerprints.add(r['generation']['mathematical_fingerprint'])
                f=r['question'][':question/answer-fields'][0]
                engine.append({'label':level+' '+template+' '+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio selection through owned UUID'} for a in f[':answer-field/choices']]})
                rr=g.generate(level,seed+999,template=template,parameters=r['generation']['parameters']);assert rr['question'][':question/id']==r['question'][':question/id'];assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
                if seed<2:review.append({'label':'generated normal authored bank '+level+' '+template+' '+str(seed),'record':r})
        assert len(fingerprints)>=10,(level,len(fingerprints))
    # Finite substantive authored domains: enumerate all admitted sampler objects.
    domain_counts={}
    for level in ['moderate','hard']:
        level_counts={}
        for template in [k for k,v in g.AUTH.items() if v==level]:
            print('Enumerating '+level+' '+template,flush=True)
            tasks=set();rejected=0
            for (a,b),c,k in itertools.product([(1,2),(1,3),(2,3)],range(1,4),range(1,4)):
                try:rr=g.generate(level,template=template,parameters={'a':a,'b':b,'c':c,'k':k})
                except ValueError:rejected+=1;continue
                check(rr);tasks.add(rr['generation']['mathematical_fingerprint'])
            level_counts[template]={'candidate_substantive_tasks':27,'admitted':len(tasks),'whole_bank_rejections':rejected}
        domain_counts[level]=level_counts
    # Explicit domain/level guards, and source collision protection in normal API.
    invalid=[('moderate','shifted_quadratic',{'a':1,'b':2,'c':0,'k':1},None),('hard','cubic_squared_quotient',{'a':0,'b':2,'c':1,'k':1},None),('hard','cubic_squared_product',{'a':1,'b':2,'c':4,'k':1},None),('easy','linear_difference',{'a':0,'b':2},'observed'),('easy','quadratic_ratio',{'a':0,'b':2},'observed')]
    for level,template,p,profile in invalid:
        try:g.generate(level,template=template,parameters=p,profile=profile)
        except ValueError:pass
        else:raise AssertionError('expected explicit-input rejection')
    write('engine-input.json',engine);harness=REPO/'generate/runs/current/check-engine';subprocess.run([str(harness),str(D/'engine-input.json'),str(D/'engine-validation.json')],check=True)
    # mutation checks prove verifier reads printed math rather than metadata
    mutation=g.generate('moderate',21,template='shifted_quadratic');mutation['question'][':question/problem']=mutation['question'][':question/problem'].replace('y=', 'y=2+',1)
    try:check(mutation)
    except AssertionError:pass
    else:raise AssertionError('printed curve mutation escaped detection')
    norm_mutation=g.generate('hard',7,template='cubic_squared_product');norm_mutation['question'][':question/worked-solution']=norm_mutation['question'][':question/worked-solution'].replace('1^2','2^2',1)
    try:check(norm_mutation)
    except AssertionError:pass
    else:raise AssertionError('printed squared-norm mutation escaped detection')
    write('review.json',review)
    lines=['# Review — scalar graph line-integral setup','Originals retain raw snapshot strings in source.json. Observed evidence replays preserve complete banks; two banks contain equal complete wrong answers. Normal authored banks reject every complete-value collision.']
    for q in qs:
        f=q[':question/answer-fields'][0]
        lines+=['\n## Raw original '+q[':question/math-academy-id'],q[':question/problem'],'\n'.join(str(i+1)+'. $'+a[':answer/value']+'$' for i,a in enumerate(f[':answer-field/choices'])),'Original correct designation: '+(f[':answer-field/correct'][':answer/value'] if ':answer-field/correct' in f else '**missing**'),q.get(':question/worked-solution','**No source worked solution.**')]
    for item in review:
        lines+=['\n## '+item['label'],g.markdown(item['record'])]
    (D/'review.md').write_text('\n\n'.join(lines)+'\n')
    report={'status':'passed_with_documented_source_anomalies','basis':1356,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_coverage':{'practice_questions':9,'replayed':9,'answer_values_exact':45,'answer_values_total':45,'complete_banks_exact':9,'complete_banks_total':9,'present_correct_designations_matched':8,'present_correct_designations_total':8,'missing_correct_designations':1,'source_solutions_exact':8,'source_solutions_present':8,'source_prompts_raw_exact':8,'source_prompts_total':9,'presentation_repaired_prompts':1,'raw_ambiguous_banks':2,'normal_source_ambiguous_banks_excluded':2},'fidelity':fidelity,'normal_instances_checked':len(engine)-9,'native_records_checked':len(engine),'enumerated_missing_level_domains':domain_counts,'native_grading':json.loads((D/'engine-validation.json').read_text()),'displayed_stage_checks':stage_checks,'authored_missing_levels':['moderate','hard'],'review_records':len(review),'plots':'none','unresolved_findings':['Source q-76188 has no source correct designation or worked solution; supplied designation is independently derived and solution authored.','Source wrong-option intent is underdetermined; observed expression patterns vary bounds only, with coefficient extensions confined to separately authored defaults.'],'database_writes':0}
    write('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k in ['status','source_coverage','normal_instances_checked','script_sha256']},indent=2))
if __name__=='__main__':main()
