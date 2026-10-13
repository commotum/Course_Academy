#!/usr/bin/env python3
"""Independent displayed-math/fidelity/grader/scope/identity checks; writes evidence."""
import hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
freeze=HERE/'freeze.json'
if freeze.exists():
    for name,digest in json.loads(freeze.read_text())['file_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,('Frozen artifact changed',name)
source=json.loads((HERE/'source.json').read_text());qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};cases=json.loads((HERE/'source-cases.json').read_text())

def parse(text):
    """Read actual simple rendered exact-number expressions, not generation values."""
    s=text.strip().rstrip('.,').replace('π',r'\pi').replace('⁡','').replace(' ','')
    def group(at):
        assert s[at]=='{', (s,at)
        depth=1;j=at+1
        while depth:
            if s[j]=='{':depth+=1
            elif s[j]=='}':depth-=1
            j+=1
        return s[at+1:j-1],j
    while '\\frac' in s or '\\sqrt' in s:
        hits=[(s.find(cmd),cmd) for cmd in (r'\frac',r'\sqrt') if cmd in s];i,cmd=min(hits)
        a,j=group(i+len(cmd))
        if cmd==r'\frac':b,k=group(j);value='('+str(parse(a))+')/('+str(parse(b))+')';j=k
        else:value='sqrt('+str(parse(a))+')'
        s=s[:i]+value+s[j:]
    s=s.replace(r'\cdot','*').replace(r'\pi','pi')
    s=re.sub(r'pi(?=\()',r'pi*',s)
    s=re.sub(r'(\d|\))(?=pi|sqrt|\()',r'\1*',s)
    return sp.sympify(s,locals={'pi':sp.pi})

def balanced(text):
    assert text.count('$')%2==0,text
    depth=0
    for c in text:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0,text
    assert depth==0,text
    assert r'\picos' not in text and '--' not in text and '+-' not in text,text

def validate_record(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];meta=r['generation'];prompt=q[':question/problem'];lev=meta['level'];f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    balanced(prompt)
    # Parse the given and full requested target directly from printed prompt.
    spans=re.findall(r'\$([^$]*)\$',prompt);assert len(spans)==2
    given=spans[0].replace(r'\cos','cos').replace('⁡','');left,right=given.split('=',1)
    m=re.fullmatch(r'cos\s*([xatu])',left.strip());assert m,given
    v=m[1];c=parse(right)
    target=spans[1].rstrip('=').strip().replace(r'\cos','cos').replace('⁡','').replace('π',r'\pi').replace('cos (','cos(')
    cm=re.search(r'cos\(([^)]*)\)',target);assert cm,target
    arg=cm[1].replace(' ','').replace(r'\pi','pi')
    arg=re.sub(r'(\d)(?=pi)',r'\1*',arg)
    variable=sp.Symbol(v,real=True);xarg=sp.sympify(arg,locals={v:variable,'pi':sp.pi})
    assert sp.expand(xarg).coeff(variable)==-1
    shift=sp.simplify((xarg+variable)/(2*sp.pi));assert shift.is_Integer
    assert (lev=='easy' and shift==0) or (lev!='easy' and shift!=0)
    # Symbolically verify the actual cosine identity for all real x.
    assert sp.trigsimp(sp.cos(xarg)-sp.cos(variable))==0
    full=target[:cm.start()]+'('+str(c)+')'+target[cm.end():]
    expected=parse(full)
    bank=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(bank)==5 and all(sp.simplify(a-b)!=0 for i,a in enumerate(bank) for b in bank[i+1:])
    matching=[a for a,b in zip(f[':answer-field/choices'],bank) if sp.simplify(b-expected)==0];assert len(matching)==1
    if meta['raw_missing_key_and_solution']:
        assert ':answer-field/correct' not in f and ':question/worked-solution' not in q
    else:
        assert f[':answer-field/correct']==[':answer/id',matching[0][':answer/id']]
        solution=q[':question/worked-solution'];balanced(solution)
        assert 'cos⁡(-x)=cos⁡x.' in solution
        rows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
        assert len(rows)==({'easy':1,'moderate':2,'hard':3}[lev])
        # Verify exact actual ordered negative-argument / period / evenness rows.
        norm=lambda s:s.replace('⁡','').replace(' ','')
        en=norm(rows[0 if lev=='easy' else 1]);assert en.startswith('cos(-'+v+')&=cos'+v+r'\\&=')
        last=en.split('&=')[-1].rstrip('.')
        assert sp.simplify(parse(last)-c)==0
        if lev!='easy':
            per=norm(rows[0]);parts=per.split('&=');assert len(parts)==3
            first=parts[0];second=parts[1].split(r'\\')[0];third=parts[2].rstrip('.')
            for co in (first,second):
                aa=re.search(r'cos\((.*?)\)',co)[1].replace(r'\cdot','*').replace(r'\pi','pi')
                aa=re.sub(r'(\d)(?=pi)',r'\1*',aa)
                aa=re.sub(r'(pi)(?=\d)',r'\1*',aa)
                assert sp.simplify(sp.sympify(aa,locals={v:variable,'pi':sp.pi})-xarg)==0
            assert third=='cos(-'+v+')'
        if lev=='hard':
            stages=re.split(r'&\s*=',rows[2]);assert len(stages)==4
            assert norm(stages[0])==norm(target)
            sub=stages[1].split(r'\\')[0];prod=stages[2].split(r'\\')[0];final=stages[3].rstrip('.')
            for stage in (sub,prod,final):assert sp.simplify(parse(stage)-expected)==0
            assert r'\cdot' in sub and r'\cdot' not in prod
    return expected

records=[];source_results=[];coverage={'banks':0,'options':0,'distractors':0,'prompts':0,'full_solutions':0,'designations':0,'available_designations':5,'available_solutions':5,'available_declared_distractors':20,'options_total':30,'banks_total':6,'prompts_total':6,'missing_designations':1,'missing_solutions':1,'mathematically_derived_unrated_distractors':4,'practice_sources':6,'unrated_sources':1}
for case in cases:
    raw=qs[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);records.append(r);validate_record(r)
    q=r['question'];rf=raw[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
    assert q[':question/problem']==raw[':question/problem'],(case['source_id'],q[':question/problem'],raw[':question/problem'])
    assert q.get(':question/worked-solution')==raw.get(':question/worked-solution'),case['source_id']
    assert len(rf[':answer-field/choices'])==len(gf[':answer-field/choices'])
    for a in rf[':answer-field/choices']:
        assert sum(sp.simplify(parse(a[':answer/value'])-parse(b[':answer/value']))==0 for b in gf[':answer-field/choices'])==1,(case,a)
    if ':answer-field/correct' in rf:
        correct=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
        assert sp.simplify(parse(correct[':answer/value'])-parse(rf[':answer-field/correct'][':answer/value']))==0
        coverage['designations']+=1;coverage['full_solutions']+=1;coverage['distractors']+=4
    else:assert ':answer-field/correct' not in gf
    coverage['banks']+=1;coverage['options']+=5;coverage['prompts']+=1
    source_results.append({'source_id':case['source_id'],'bank_matches':5,'prompt_exact':True,'solution_exact':':question/worked-solution' in raw,'correct_designation_match':':answer-field/correct' in rf})
    if 'normal_repair_profile' in case:
        repaired=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['normal_repair_profile']);validate_record(repaired);records.append(repaired)

# Complete profiles under varied parameters; no profile is skipped.
changed=[]
for profile,template in g.PROFILES.items():
    fingerprints=set()
    for seed in range(12):
        r=g.generate(g.TEMPLATES[template],seed,template=template,profile=profile);validate_record(r);records.append(r);fingerprints.add(r['generation']['parameter_fingerprint'])
    assert len(fingerprints)>=8,(profile,len(fingerprints))
    changed.append({'profile':profile,'instances':12,'distinct_mathematical_tasks':len(fingerprints)})

# Seed only changes option ordering for explicit fixed inputs, not content IDs.
for case in cases:
    a=g.generate(case['level'],1,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);b=g.generate(case['level'],9,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
    assert a['question'][':question/id']==b['question'][':question/id']
    assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
original=g.generate('easy',parameters={'c':'-1/3','variable':'a'},profile='q-136545')
authored=g.generate('easy',parameters={'c':'-1/3','variable':'a'})
aliased=g.generate('easy',parameters={'c':'-1/3','variable':'x'},profile='q-136545')
assert original['generation']['parameter_fingerprint']==authored['generation']['parameter_fingerprint']==aliased['generation']['parameter_fingerprint']
assert len({original['question'][':question/id'],authored['question'][':question/id'],aliased['question'][':question/id']})==3
assert len({next(i for i,a in enumerate(g.generate('easy',s)['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==g.generate('easy',s)['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for s in range(20)})>=3
# Full-period shift aliases change presentation, not the assessed task.
period_aliases=[g.generate('moderate',parameters={'c':'1/3','variable':'x','n':n}) for n in (-20,-3,1,17)]
assert len({r['generation']['parameter_fingerprint'] for r in period_aliases})==1
assert len({r['question'][':question/id'] for r in period_aliases})==4
# Explicit inputs must fail rather than escaping level/domain restrictions.
invalid=[('easy',{'c':'2','variable':'x'}),('moderate',{'c':'1/3','variable':'x','n':0}),('moderate',{'c':'1/3','variable':'x','n':21}),('hard',{'c':'1/3','variable':'x','n':2,'scale':'1','offset':'1/2'}),('hard',{'c':'1/3','variable':'x','n':2,'scale':'2','offset':'0'}),('easy',{'c':'0','variable':'x'})]
for lev,p in invalid:
    try:g.generate(lev,parameters=p)
    except ValueError:pass
    else:raise AssertionError(('invalid explicit input accepted',lev,p))
# Meaningful finite arithmetic catalog rather than aliases or bank-count inflation.
counts={}
for lev in ('easy','moderate','hard'):
    rs=[g.generate(lev,s) for s in range(100)];tasks={r['generation']['parameter_fingerprint'] for r in rs};assert len(tasks)>=60
    counts[lev]={'sampled':100,'distinct_mathematical_tasks':len(tasks)}
    records.extend(rs[:10])

# Review every source template / bank and at least two normal examples per level.
review=[];md=['# Cosine evenness review','', 'All source sections show immutable originals and parameterized replay. Normal variants are labeled authored bank extensions.','']
for case in cases:
    raw=qs[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);review.append(r)
    md+=['## Original '+case['source_id'],'',raw[':question/problem'],'','Source choices: '+', '.join('$'+a[':answer/value']+'$' for a in raw[':question/answer-fields'][0][':answer-field/choices']),'',raw.get(':question/worked-solution','**No captured key, difficulty or worked solution.**'),'','### Parameterized original-profile replay','',g.markdown(r),'','### Generated changed-parameter variant of the same observed bank','']
    variant=g.generate(case['level'],71,template=case['template'],profile=case.get('normal_repair_profile',case['bank_profile']));validate_record(variant);review.append(variant);md+=[g.markdown(variant),'']
for lev in ('easy','moderate','hard'):
    for seed in (8,9):
        r=g.generate(lev,seed);validate_record(r);review.append(r);md+=['## Authored default bank: '+lev+', seed '+str(seed),'',g.markdown(r),'']
(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(HERE/'review.md').write_text('\n'.join(md)+'\n')
fixtures=[]
for i,r in enumerate(records):
    if r['generation']['raw_missing_key_and_solution']:continue
    f=r['question'][':question/answer-fields'][0]
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual requested scalar value for every owned radio choice'} for a in f[':answer-field/choices']]
    fixtures.append({'label':str(i)+'-'+r['generation']['profile'],'record':r,'checks':checks})
(HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
engine=ROOT/'generate/runs/current/check-engine';proc=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
report={'status':'pass' if proc.returncode==0 else 'fail','version':g.VERSION,'source_fidelity':coverage,'source_results':source_results,'source_format_repairs':[{'source_id':'q-136634','raw_missing':['difficulty','correct designation','worked solution'],'assigned_level':'moderate','repair':'Derived unique scalar c=-11/24; retained all five options; supplied exact common moderate solution. Original absent designation is not counted matched.'}],'mathematical_source_repairs':0,'notation_normalization':'Answer choices retain full mathematical equivalence; source spaces and Unicode π may normalize to standard TeX. Prompt and all available complete solutions are byte-exact.','correctness':{'displayed_prompts_banks_and_ordered_stages':True,'profile_variation':changed,'default_variety':counts,'invalid_inputs_rejected':len(invalid)},'native_grader':{'exit_code':proc.returncode,'fixtures':len(fixtures),'checks':sum(len(f['checks']) for f in fixtures),'stdout':proc.stdout,'stderr':proc.stderr,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'raw_unrated_grading':'No key; preserved public raw profile is intentionally ungradeable. Separate minimal repair tested.'}
(HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report,indent=2))
if proc.returncode:sys.exit(proc.returncode)
