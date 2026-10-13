#!/usr/bin/env python3
"""Independent parser checks the actual learner strings, source fidelity and native radio grading."""
import hashlib, importlib.util, json, re, subprocess, uuid, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('open_interval_generator',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(g)

def clean(text):
    text=re.sub(r'\{\\color\{(?:red|blue)\}\{([^{}]*)\}\}',r'\1',text)
    return text.replace(r'\,','').strip().replace('$','')

def num(text):
    text=text.strip().replace('−','-').replace(' ','')
    if text in ('-∞',r'-\infty'): return -s.oo
    text=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    out=s.sympify(text)
    assert out.is_Rational or out==-s.oo, text
    return out

def interval(text):
    text=clean(text)
    if '∈' in text: text=text.split('∈')[1].strip()
    if r'\in' in text: text=text.split(r'\in')[1].strip()
    assert text[0] in '([' and text[-1] in ')]',text
    a,b=map(num,text[1:-1].split(','))
    assert a<b
    return s.Interval(a,b,left_open=text[0]=='(',right_open=text[-1]==')')

def inequality(text):
    text=clean(text)
    if ' or ' in text:
        match=re.fullmatch(r'([xyzt])\s*<\s*(.*?)\s+or\s+\1\s*>\s*(.*)',text); assert match,text
        return s.Union(s.Interval.open(-s.oo,num(match[2])),s.Interval.open(num(match[3]),s.oo))
    match=re.fullmatch(r'(.*?)\s*(\\le|<)\s*([xyzt])\s*(\\le|<)\s*(.*)',text); assert match,text
    a,b=num(match[1]),num(match[5]); assert a<b
    return s.Interval(a,b,left_open=match[2]=='<',right_open=match[4]=='<')

def math_object(text):
    t=clean(text)
    return interval(t) if '∈' in t or r'\in' in t or t[0] in '([' and ',' in t else inequality(t)

def formatting(text):
    assert text.count('$')%2==0
    stack=0
    for c in text:
        if c=='{': stack+=1
        elif c=='}': stack-=1; assert stack>=0
    assert stack==0
    assert '\\\\' not in text

def inspect(record,raw=False):
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question']; f=q[':question/answer-fields'][0]; answers=f[':answer-field/choices']; assert len(answers)==5
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    uuid.UUID(q[':question/id']); uuid.UUID(f[':answer-field/id'])
    for a in answers: uuid.UUID(a[':answer/id']); formatting(a[':answer/value'])
    assert len({a[':answer/id'] for a in answers})==5
    formatting(q[':question/problem'])
    actual_identity={'version':g.VERSION,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted((a[':answer/value'],a[':answer/type'].split('/')[-1]) for a in answers),'correct':None if raw else next(a[':answer/value'] for a in answers if a[':answer/id']==f[':answer-field/correct'][1])}
    identity=g.digest(actual_identity)
    assert identity==record['generation']['content_fingerprint']
    assert q[':question/id']==g.uid('question',identity)
    prompt_math=re.findall(r'\$(.*?)\$',q[':question/problem'])[0]
    expected=math_object(prompt_math)
    assert expected.left_open and expected.right_open and expected.start!=-s.oo and expected.end!=s.oo
    assert (str(expected.start),str(expected.end)) in g.catalog(record['generation']['difficulty'])
    template='inequality_to_interval' if 'The inequality' in q[':question/problem'] else 'interval_to_inequality'
    assert template==record['generation']['template']
    assert record['generation']['mathematical_fingerprint']==g.digest({'template':template,'a':str(expected.start),'b':str(expected.end)})
    sets=[math_object(a[':answer/value']) for a in answers]
    assert len(set(sets))==5
    assert sum(obj==expected for obj in sets)==1
    if raw:
        assert ':answer-field/correct' not in f and ':question/difficulty' not in q and ':question/worked-solution' not in q
        return
    correct=f[':answer-field/correct']; assert correct[0]==':answer/id'
    index=next(i for i,a in enumerate(answers) if a[':answer/id']==correct[1]); assert sets[index]==expected
    assert q[':question/difficulty']==':question.difficulty/'+record['generation']['difficulty']
    sol=q[':question/worked-solution']; formatting(sol)
    rows=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    assert len(rows)==(3 if 'The inequality' in q[':question/problem'] else 2)
    for row in rows:
        assert math_object(row)==expected, row
        assert re.findall('[xyzt]',re.sub(r'\\[a-z]+','',clean(row)))==[re.search(r'([xyzt])',prompt_math)[1]] if '<' in row or '\\in' in row else True
    # Introductory endpoint prose is separately checked, preventing stale slots.
    if 'The inequality' in q[':question/problem']:
        assert f'endpoints ${g.tex(str(expected.start))}$ and ${g.tex(str(expected.end))}$' in sol
    assert '*not* included' in sol

source=json.loads((ROOT/'source.json').read_text())
assert source['basis']==1356
questions=source['record'][':knowledge-point/questions']
cases=json.loads((ROOT/'source-cases.json').read_text())
assert len(cases)==len(questions)==2
fidelity=[]; inputs=[]
for case,original in zip(cases,questions):
    assert case['source_id']==original[':question/math-academy-id']
    raw=g.generate('easy',seed=17,template=case['template'],parameters=case['parameters'],profile='source_raw'); inspect(raw,True)
    rq=raw['question']; assert rq[':question/problem']==original[':question/problem']
    original_field=original[':question/answer-fields'][0]; raw_field=rq[':question/answer-fields'][0]
    original_bank=sorted((a[':answer/value'],a[':answer/type'][':db/ident']) for a in original_field[':answer-field/choices'])
    assert original_bank==sorted((a[':answer/value'],a[':answer/type']) for a in raw_field[':answer-field/choices'])
    assert original_field[':answer-field/type'][':db/ident']==raw_field[':answer-field/type']
    assert original_field[':answer-field/key']==raw_field[':answer-field/key']
    assert ':answer-field/correct' not in original_field and ':question/worked-solution' not in original and ':question/difficulty' not in original
    repaired=g.generate('easy',template=case['template'],parameters=case['parameters']); inspect(repaired)
    fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'bank_values_types_exact':5,'missing_original_correct_ref':True,'missing_original_solution':True,'raw_replay_public_api':True,'derived_correct_unique':True})
    inputs.append(repaired)
canonical=source['record'][':knowledge-point/canonical-example']
canonical_solution=g.generate_easy(template='interval_to_inequality',parameters={'a':1,'b':5})['question'][':question/worked-solution']
assert canonical_solution==canonical[':question/worked-solution']
assert canonical[':question/worked-solution'].count('\\\\')==0
counts={}; tested=0
# Enumerate every meaningful endpoint pair in all levels and both directions.
for level in ('easy','moderate','hard'):
    fingerprints=set()
    for template in g.TEMPLATES:
        for a,b in g.catalog(level):
            rec=g.generate(level,template=template,parameters={'a':a,'b':b})
            inspect(rec); fingerprints.add(rec['generation']['mathematical_fingerprint']); tested+=1
    counts[level]=len(fingerprints)
    for template in g.TEMPLATES:
        for seed in (7,19):
            rec=g.generate(level,seed,template=template); inputs.append(rec)
            for profile in g.PROFILES:
                p=rec['generation']['parameters']; r=g.generate(level,7,template=template,parameters=p,profile=profile); r2=g.generate(level,19,template=template,parameters=p,profile=profile)
                assert r['question'][':question/id']==r2['question'][':question/id']
            alias=g.generate(level,parameters={**rec['generation']['parameters'],'variable':'y'},template=template)
            assert alias['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
# Exercise every supported variable and reduced rational alias explicitly.
for level in ('easy','moderate','hard'):
    for template in g.TEMPLATES:
        for variable in ('x','y','t','z'):
            a,b=g.catalog(level)[len(g.catalog(level))//2]
            inspect(g.generate(level,template=template,parameters={'a':a,'b':b,'variable':variable}))
alias_a=g.generate('hard',template='interval_to_inequality',parameters={'a':'2/4','b':'4/3'})
alias_b=g.generate('hard',template='interval_to_inequality',parameters={'a':'1/2','b':'8/6'})
assert alias_a['question'][':question/id']==alias_b['question'][':question/id']
# Source order must not hard-code the correct answer first.
positions={next(i for i,a in enumerate(g.generate_easy(seed)['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==g.generate_easy(seed)['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for seed in range(20)}
assert len(positions)>1
# Explicit invalid level domains and input shapes may never silently resample.
for level,p in [('easy',{'a':0,'b':4}),('moderate',{'a':1,'b':5}),('hard',{'a':'1/2','b':2}),('hard',{'a':'1/5','b':'2/3'}),('easy',{'a':4,'b':3})]:
    try: g.generate(level,parameters=p)
    except ValueError: pass
    else: raise AssertionError((level,p))
engine=[]
for i,record in enumerate(inputs):
    f=record['question'][':question/answer-fields'][0]
    engine.append({'label':f'original-or-family-{i}','record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'select independently parsed complete interval/inequality value'} for a in f[':answer-field/choices']]})
(ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
engine_path=ROOT.parents[1]/'runs/current/check-engine'
subprocess.run([str(engine_path),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
review=json.loads((ROOT/'review.json').read_text()); assert len(review)==12
for rec in review: inspect(rec)
report={'status':'pass','source':g.SOURCE,'source_practice_questions':2,'source_prompts_exact':{'matched':2,'total':2},'source_banks_exact':{'matched':2,'total':2},'source_displayed_options_exact':{'matched':10,'total':10},'source_correct_designations':{'matched':0,'available':0,'missing':2},'practice_worked_solutions':{'matched':0,'available':0,'missing':2},'canonical_worked_solution_exact':{'matched':1,'total':1},'derived_keys_unique':2,'authored_practice_solutions':2,'raw_replays':2,'exhaustive_generated_questions_checked':tested,'finite_mathematical_task_counts':counts,'structural_conversion_patterns':2,'native_engine_provenance':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (engine_path,engine_path.with_suffix('.rs'),engine_path.parent/'engine-build.log')},'radio_grading':json.loads((ROOT/'engine-report.json').read_text()),'equivalent_free_entries':'not applicable: both observed fields are radio; native grader checks every owned selection and independent set parser checks mathematical equivalence','unresolved_findings':[],'frozen_hashes':{str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),*sorted(ROOT.glob('*'))] if p.is_file() and p.name!='validation.json'}}
(ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(f'PASS: {tested} exhaustive records, 2/2 raw banks, 10/10 choices; authored counts {counts}')
