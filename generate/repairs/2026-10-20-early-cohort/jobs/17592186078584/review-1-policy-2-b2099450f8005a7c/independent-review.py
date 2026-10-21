"""Read-only independent revision review. Run with the context Python and -B."""
import sys
sys.dont_write_bytecode = True
import collections, hashlib, importlib.util, json, math, pathlib, re, shutil, subprocess

E = pathlib.Path(__file__).resolve().parent
J = E.parent
P = J / 'workspace'
R = pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p): return json.loads(pathlib.Path(p).read_text())
def save(n, x):
    (E/n).write_text(json.dumps(x, indent=2, ensure_ascii=False)+'\n')
def module(n,p):
    spec=importlib.util.spec_from_file_location(n,p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('current_generator',P/'17592186078584.py')
old=module('old_generator',P/'evidence/old/17592186078584.py')
source=load(J/'source/source.json')['material']['kp']
def num(a):return int(re.search(r'-?\d+',a[':answer/value'])[0])
def info(r):
    q=r['question'];f=q[':question/answer-fields'][0];c=f[':answer-field/correct']
    cid=c[1] if isinstance(c,list) else c[':answer/id'];choices=f[':answer-field/choices']
    values=[num(a) for a in choices];pos=next(i for i,a in enumerate(choices) if a[':answer/id']==cid)
    return dict(id=q[':question/id'],template=r.get('generation',{}).get('template'),answer=values[pos],values=values,rank=sorted(values).index(values[pos])+1,position=pos+1)
def norm(s):
    return re.sub(r'\s+','',s.replace('\\\\','\\').replace(r'\left','').replace(r'\right','').replace(r'\,',''))

math_results=[]
def check_math(r):
    q=r['question'];text=q[':question/problem'];sol=q[':question/worked-solution'];lv=q[':question/difficulty'].split('/')[-1]
    # All data below are parsed from displayed text, not generation metadata.
    if lv=='easy':
        k,A=re.search(r'=-([\d.]+)\(T-(\d+)\)',text).groups();A=int(A)
        I=int(re.search(r'initial temperature.*?\$\{(\d+)',text)[1]);t=int(re.search(r'after \$(\d+)\$',text)[1]);D=I-A
        x=A+D*math.exp(-float(k)*t)
        deps=[f'K & ={D}',f'T(t)={A}+{D}{{e}}^{{-{k}t}}',f'T({t})={A}+{D}{{e}}^{{-{k}\\cdot {t}}}']
        assert A<x<I
    elif lv=='moderate':
        temps=[int(v) for v in re.findall(r'\$\{(\d+)\}\^\{∘\}[CF]',text)]
        if 'Simon measures' in text:I,O,Z,A=temps[:4]
        else:I,A,O,Z=temps[:4]
        t=int(re.search(r'After \$(\d+)\$',text)[1]);D=I-A
        x=t*math.log((Z-A)/D)/math.log((O-A)/D)
        deps=[f'K & ={D}',f'T(t)={A}+{D}{{e}}^{{-kt}}',f'T({t})={O}',f'T({{t}}_{{1}}) & ={Z}']
        assert A<Z<O<I and x>t
    else:
        A,O,L,Z=[int(n) for n in re.findall(r'\$\{(\d+)\}\^\{∘\}',text)]
        a,b=[int(n) for n in re.findall(r'after \$(\d+)\$',text)]
        x=a+(b-a)*math.log((Z-A)/(O-A))/math.log((L-A)/(O-A))
        deps=[f'T({a})={O}',f'T({b})={L}',f'T({{t}}_{{1}}) & ={Z}']
        assert A<Z<L<O and x>b
    expected=math.floor(x+.5);actual=info(r)
    assert actual['answer']==expected,(actual,expected)
    assert len(set(actual['values']))==5
    assert all(d in sol for d in deps),(actual,deps)
    assert ':answer-field.type/radio'==q[':question/answer-fields'][0][':answer-field/type']
    math_results.append(dict(id=actual['id'],difficulty=lv,computed=x,expected=expected,actual=actual['answer'],solution_dependencies=deps,passed=True))

# Retained executable failures: verified original executable bytes match earlier review.
prior_hash=load(J/'review-0-policy-2-f45195d9a61ccc58/package-hashes-before.json')
assert hashlib.sha256((P/'evidence/old/17592186078584.py').read_bytes()).hexdigest()==prior_hash['17592186078584.py']
assert hashlib.sha256((P/'evidence/old/17592186078584/source.json').read_bytes()).hexdigest()==prior_hash['17592186078584/source.json']
reg=[];accept=[]
for template,p,expected in [
 ('coffee',dict(ambient=23,initial=80,rate='0.25',time=4),44),
 ('coffee',dict(ambient=21,initial=40,rate='0.06',time=4),36),
 ('body',dict(ambient=21,initial=40,rate='0.06',time=4),36),
 ('bulb',dict(ambient=23,initial=80,rate='0.25',time=4),44),
 ('body',dict(ambient=80,initial=95,rate='0.25',time=15),80),
 ('body',dict(ambient=5,initial=20,rate='0.02',time=1),20)]:
    row=dict(case='valid IVP acceptance',template=template,parameters=p,expected=expected,seed=84199)
    try: rr=old.generate('easy',84199,template,parameters=p);row['old']={'accepted':True,'record':rr}
    except Exception as ex:row['old']={'accepted':False,'error':str(ex)}
    rr=g.generate('easy',84199,template,parameters=p);check_math(rr);accept.append(rr)
    row['current']={'accepted':True,'result':info(rr)};assert info(rr)['answer']==expected
    reg.append(row)
assert not reg[0]['old']['accepted'] and not reg[1]['old']['accepted']
for profile in ['q-107121','q-107123']:
    lv='easy' if profile=='q-107121' else 'moderate';row=dict(case='missing profile',profile=profile)
    try:rr=old.generate(lv,84199,profile=profile);row['old']={'accepted':True}
    except Exception as ex:row['old']={'accepted':False,'error':str(ex)}
    rr=g.generate(lv,84199,profile=profile);check_math(rr);row['current']={'accepted':True,'result':info(rr)}
    assert not row['old']['accepted'];reg.append(row)
save('acceptance-records.json',accept)

# Replay all captured question banks; normalize only presentation and source unit typo.
replay=[];rrs=[]
for q in source[':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];lv=q[':question/difficulty'][':db/ident'].split('/')[-1]
    rr=g.generate(lv,932519,profile=sid);current=rr['question'];f=q[':question/answer-fields'][0]
    corrected=q[':question/worked-solution']
    if sid=='q-107122':corrected=corrected.replace(r'\text{C}',r'\text{F}').replace('}C','}F')
    result=dict(source_id=q[':question/id'],profile=sid,prompt_match=norm(q[':question/problem'])==norm(current[':question/problem']),solution_match=norm(corrected)==norm(current[':question/worked-solution']),complete_bank_match=sorted(norm(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in current[':question/answer-fields'][0][':answer-field/choices']),key_match=num(f[':answer-field/correct'])==info(rr)['answer'],source_correction=sid=='q-107122')
    assert all(result[k] for k in ['prompt_match','solution_match','complete_bank_match','key_match']),result
    check_math(rr);replay.append(result);rrs.append(rr)
save('source-replay.json',{'cases':replay,'canonical':{'source_id':'e3e001a8-9294-59a4-82e6-b1122afdc72f','parameters_replayed_in':'acceptance-records.json','context':'bulb','answer':44,'bank':'No captured bank; authored bank tested separately.'}})
save('source-replay-records.json',rrs)

# Small fresh regression sample across all changed bank constructors.
samples=[];coverage={};old_ranks={}
for template,lv in g.TEMPLATES.items():
    seeds=list(range(932571,932579 if lv=='easy' else 932577 if lv=='moderate' else 932575))
    rs=[g.generate(lv,seed,template) for seed in seeds]
    for rr in rs:check_math(rr)
    coverage[template]={'seeds':seeds,'count':len(rs),'ranks':dict(collections.Counter(info(r)['rank'] for r in rs)),'positions':dict(collections.Counter(info(r)['position'] for r in rs)),'attempts':dict(collections.Counter(r['generation']['attempts'] for r in rs)),'slot_values':{k:sorted({str(r['generation']['parameters'][k]) for r in rs}) for k in rs[0]['generation']['parameters']}}
    assert len(coverage[template]['ranks'])>1
    if template in old.TEMPLATES:
        ors=[old.generate(lv,seed,template) for seed in seeds]
        old_ranks[template]=dict(collections.Counter(info(r)['rank'] for r in ors))
        assert all(info(r)['rank']==(3 if lv=='easy' else 4) for r in ors)
        assert any(info(r)['rank']!=(3 if lv=='easy' else 4) for r in rs)
    samples.extend(rs)
save('fresh-samples.json',samples);save('raw-coverage.json',coverage)
save('retained-finding-tests.json',{'command':f'{sys.executable} -B {E}/independent-review.py','preflight':'Read repair-history.json, repair-preflight.json and declared checks/regressions.py. Old code matched earlier independent hashes; original failing acceptance/profile cases and fixed-rank rules reproduced. Current tests parse visible prompts and exercise changed rules independently. Author preflight not treated as certification.','tests':reg,'old_rank_distributions':old_ranks,'current_rank_distributions':{t:v['ranks'] for t,v in coverage.items()},'passed':True})

batch=load(J/'samples.json');save('runner-batch.json',batch)
for rr in batch:
    check_math(rr)
    assert g.generate('easy',rr['generation']['seed'])==rr

# Re-evaluate exact prior mathematical cases, not merely a new seed-to-template map.
historical=[]
for rr in load(J/'review-0-policy-2-f45195d9a61ccc58/runner-batch.json')+load(E/'previous-generated-records.json'):
    meta=rr['generation'];lv=rr['question'][':question/difficulty'].split('/')[-1]
    now=g.generate(lv,meta['seed'],meta['template'],parameters=meta['parameters']);check_math(now)
    assert info(now)['answer']==info(rr)['answer']
    historical.append({'before':rr,'after':now,'before_info':info(rr),'after_info':info(now)})
save('historical-counterexamples-current.json',historical)

# Controlled relevant changes (time/target) and irrelevant context/bank assignment.
p=dict(ambient=25,initial=100,rate='0.05',time=6)
m=dict(ambient=10,initial=50,observed=40,target=30,time=5)
cf=[g.generate('easy',932631,'coffee',parameters=p),g.generate('easy',932631,'coffee',parameters={**p,'time':9}),g.generate('easy',932631,'compressor',parameters=p),g.generate('moderate',932631,'bath',parameters=m),g.generate('moderate',932631,'bath',parameters={**m,'target':25}),g.generate('easy',932632,'coffee',parameters=p)]
assert [info(r)['answer'] for r in cf]==[81,73,81,12,17,81]
for rr in cf:check_math(rr)
assert cf[0]['question'][':question/problem']==cf[5]['question'][':question/problem']
assert cf[0]['question'][':question/worked-solution']==cf[5]['question'][':question/worked-solution']
save('counterfactual-records.json',cf)
save('counterfactual-results.json',{'command':'independent-review.py; real native grader and actual UI run separately on these records','results':[info(r) for r in cf],'relationships':['time6->9 decreases rounded answer81->73','coffee->compressor preserves81 at fixed numerical evidence','target30->25 increases total rounded time12->17','seed932631->932632 changes bank assignment, preserves prompt, solution and answer81'],'passed':True})

# Native grader cases are keyed by independently calculated displayed numerical values.
representatives=batch+cf+accept+rrs+[next(r for r in samples if r['generation']['template']==t) for t in g.TEMPLATES]
cases=[]
for i,rr in enumerate(representatives):
    f=rr['question'][':question/answer-fields'][0];answer=info(rr)['answer']
    cases.append({'label':f'independent-{i}','record':rr,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if num(a)==answer else 'rejected','purpose':'Independent visible-prompt calculation; every correct/wrong radio selection'} for a in f[':answer-field/choices']]})
save('grader-input.json',cases);save('math-results.json',{'count':len(math_results),'results':math_results,'passed':True})
save('render-records.json',batch+cf+[accept[2],accept[3],next(r for r in rrs if r['generation']['template']=='pork')])

# Boundary rejection and real standalone relocation, including full declared runtime files.
boundary=[]
for label,changes,expected in [('zero_time',dict(time=0),False),('equilibrium_initial',dict(initial=25),False),('negative_rate',dict(rate='-0.05'),False),('minimum_rate',dict(rate='0.02'),True),('maximum_rate',dict(rate='0.25'),True)]:
    try:rr=g.generate('easy',932641,'coffee',parameters={**p,**changes});actual=True
    except ValueError:actual=False
    assert actual==expected;boundary.append(dict(case=label,parameters={**p,**changes},expected_acceptance=expected,actual_acceptance=actual))
manifest=load(P/'package.json');rel=E/'relocated';rel.mkdir(exist_ok=True)
for n in manifest['files']:
    dest=rel/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/n,dest)
cmd=[sys.executable,'-B',str(rel/manifest['entrypoint']),'--difficulty','easy','--seed','932671','--count','3','--format','json']
a=subprocess.run(cmd,cwd=E,text=True,capture_output=True);b=subprocess.run(cmd,cwd=E,text=True,capture_output=True)
assert a.returncode==b.returncode==0 and a.stdout==b.stdout,(a.stderr,b.stderr)
relrs=json.loads(a.stdout);assert relrs==[g.generate('easy',932671+i) for i in range(3)]
for rr in relrs:check_math(rr)
save('relocated-records.json',relrs)
import sympy
actual={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
assert actual==manifest['dependencies'],(actual,manifest['dependencies'])
save('packaging.json',{'dependencies':manifest['dependencies'],'actual':actual,'relocation_command':cmd,'relocation_exit':a.returncode,'deterministic':a.stdout==b.stdout,'matches_original':True,'boundary_tests':boundary,'external_outputs':'CLI JSON parsed as array; no asset writes; paths and runtime source resolved relative to relocated script.','passed':True})
save('scope-and-math.json',{'source_account':'source-analysis.json','easy':'Explicit-rate initial IVP followed by one future-temperature evaluation and integer rounding; checked all runner records and seven contexts.','moderate':'Initial and later observation determine rate; invert for target time.','hard':'Existing authored extension uses two nonzero-time observations; method unchanged by this targeted repair. Not treated as observed source support or requested easy output.','response':'One radio field with five distinct integer-unit answers; every offered answer tested separately.','limitations':['No captured hard source item; hard is retained authored extension, not used to certify easy difficulty.'],'passed':True})
(E/'session-state.md').write_text('Independent test milestone complete: source account confirmed; all retained defects reproduced with hash-matched old executable; current acceptance/profile/rank regression tests pass. Fresh90, source11, runner5 and controlled6 sampled; independent math and solution dependencies pass. Native grader, delivery, rendering, inventory verification and decision report next. Package files read only.\n')
print(json.dumps({'fresh':len(samples),'replayed':len(rrs),'batch':[info(r) for r in batch],'coverage':{t:c['ranks'] for t,c in coverage.items()},'native_cases':len(cases),'math_checks':len(math_results),'packaging':'passed'},indent=2))
