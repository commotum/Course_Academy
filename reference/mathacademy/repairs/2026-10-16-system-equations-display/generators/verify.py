"""Presentation repair regression: original code is retained under before/. No DB writes."""
import copy, hashlib, importlib.util, json, re, subprocess, sys, types
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy')
HERE=Path(__file__).resolve().parent
IDS=[17592186073752,17592186073753,17592186073776,17592186073778,17592186192654,17592186192655,17592186192656,17592186192657]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
import math_format

def load(path,name,source=None):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(path.read_text() if source is None else source,str(path),'exec'),m.__dict__)
    return m
qa=load(ROOT/'generate/runs/current/qa.py','structural_qa')

def save(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def field_signature(q):
    out=[]
    for f in q[':question/answer-fields']:
        c=f.get(':answer-field/correct',[None,None])[1]
        out.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'],
            'choices':[(a[':answer/type'],a[':answer/value'],a.get(':answer/id')==c) for a in f.get(':answer-field/choices',[])]})
    return out

def mathnorm(text):
    # Remove presentation wrappers only; arithmetic symbols/numbers and their order remain.
    text=re.sub(r'(?:&&\s*)?\([12]\)(?=\s*(?:\\\\|\\end|;|$))','',text)
    for x in (r'\left\{',r'\right.',r'\{',r'\begin{aligned}',r'\end{aligned}',r'\left',r'\right'):
        text=text.replace(x,'')
    text=text.replace(r'\\',';').replace('&','')
    text=re.sub(r'\s+','',text)
    text=text.replace(r'\mid\mid',r'\mid')
    return text

def display_signature(text):
    pat=re.compile(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',re.S)
    maths=[mathnorm(m.group(1) if m.group(1) is not None else m.group(2)) for m in pat.finditer(text)]
    prose=pat.sub(' MATH ',text)
    return re.sub(r'[\s.]','',prose), maths

def layout_checks(record):
    for attribute in (':question/problem',':question/worked-solution'):
        text=record['question'][attribute]
        assert not re.search(r'\\mid\s*\\mid',text),(attribute,'double operation bars')
        for m in re.finditer(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',text,re.S):
            tex=m.group(1) if m.group(1) is not None else m.group(2)
            if r'\{' in tex:
                assert r'\left\{\begin{aligned}' in tex and r'\\' in tex,(attribute,tex)
                assert ';' not in tex,(attribute,tex)
                assert m.group(1) is not None,(attribute,'system must be display math')
                assert r'\end{aligned}\right.' in tex

def possible_calls(g):
    calls=[];unsupported=[]
    for level in ('easy','moderate','hard'):
        templates=[None,*g.TEMPLATES] if hasattr(g,'TEMPLATES') else [None,'one_transformation']
        for template in templates:
            kwargs={} if template is None else {'template':template}
            try: g.generate(level,seed=0,**kwargs)
            except ValueError as ex:
                unsupported.append({'difficulty':level,'template':template,'reason':str(ex)});continue
            for seed in range(12):calls.append((level,seed,kwargs))
        # Exercise every normal complete bank profile at every supported difficulty.
        profiles=getattr(g,'PROFILES',getattr(g,'PROFILE_TEMPLATE',{}))
        if g.KP_ID==17592186192654: profiles=['authored-coefficient-confusion']
        if g.KP_ID==17592186192655: profiles=['difference','coefficient']
        if g.KP_ID==17592186192656: profiles=['authored-method-errors','authored-blanks']
        for profile in profiles:
            if profile.startswith(('raw','source')):continue
            try: g.generate(level,seed=0,profile=profile)
            except ValueError:continue
            for seed in range(4):calls.append((level,seed,{'profile':profile}))
    return calls,unsupported

report={'database_mutations':0,'generators':[],'baseline_validator_limitations':[]}
engine=[];examples=[]
validator_functions=['check_record','verify','check_record','check','validate_record','check_record','validate_record','actual_math']
for kp,check_name in zip(IDS,validator_functions):
    path=ROOT/f'generate/scratch/{kp}.py';old=load(path,f'baseline_{kp}',(HERE/f'before/{kp}.py').read_text());new=load(path,f'new_{kp}')
    vpath=path.with_suffix('')/'validate.py'
    validator_source=vpath.read_text()
    if kp==17592186073753:validator_source=validator_source.split('\ncases=',1)[0]
    v=load(vpath,f'validator_{kp}',validator_source);v.g=old
    calls,unsupported=possible_calls(old);checked=set();passed=0;examples_by=set();raw_checks=0
    for level,seed,kwargs in calls:
        before=old.generate(level,seed=seed,**kwargs);after=new.generate(level,seed=seed,**kwargs)
        assert after==new.generate(level,seed=seed,**kwargs),'determinism'
        a,b=before['question'],after['question']
        assert field_signature(a)==field_signature(b),(kp,level,seed,kwargs,'fields')
        assert a.get(':question/difficulty')==b.get(':question/difficulty')
        for k in ('parameters','template','profile','bank_profile','recipes','mathematical_fingerprint','parameter_fingerprint'):
            assert before['generation'].get(k)==after['generation'].get(k),(kp,k)
        for k in (':question/problem',':question/worked-solution'):
            sa,sb=display_signature(a.get(k,'')),display_signature(b.get(k,''))
            assert sa==sb,(kp,level,seed,kwargs,k,sa,sb)
        layout_checks(after)
        checks=qa.record_checks(after)
        # Every choice and canonical blank goes through the real application grader.
        engine.append({'label':f'{kp}/{level}/{seed}/{kwargs}','record':after,'checks':checks})
        key=(level,before['generation']['template'])
        if key not in checked:
            getattr(v,check_name)(before);checked.add(key)
        if key not in examples_by:
            examples.append(after);examples_by.add(key)
        passed+=1
    # Retain exact original raw prompts and source banks, excluding derived UUIDs.
    casepath=path.with_suffix('')/'source-cases.json'
    cases=json.loads(casepath.read_text())
    if isinstance(cases,dict):cases=cases.get('questions',[])
    for case in cases:
        profile=case.get('bank_profile',case.get('profile'))
        if not profile or not profile.startswith(('raw','source')):continue
        level=case.get('level',case.get('authored_level','easy'));kwargs={'parameters':case['parameters'],'profile':profile}
        if case.get('template'):kwargs['template']=case['template']
        before=old.generate(level,seed=17,**kwargs);after=new.generate(level,seed=17,**kwargs)
        assert field_signature(before['question'])==field_signature(after['question'])
        is_raw=before['generation'].get('evidence_only',before['generation'].get('raw_evidence',False))
        if is_raw:assert before['question'][':question/problem']==after['question'][':question/problem']
        else:
            for k in (':question/problem',':question/worked-solution'):
                assert display_signature(before['question'].get(k,''))==display_signature(after['question'].get(k,'')),(kp,profile,k)
        raw_checks+=1
    report['generators'].append({'kp':kp,'before_sha256':sha(HERE/f'before/{kp}.py'),'after_sha256':sha(path),'version':new.VERSION,'sampled_records':passed,'templates_and_difficulties':sorted([list(x) for x in checked]),'source_replay_cases':raw_checks,'unsupported_combinations':unsupported,'baseline_mathematical_validation':'passed','answer_banks_correct_keys_difficulty_parameters_fingerprints':'unchanged','displayed_mathematics_and_prose':'equivalent except presentation','deterministic_replay':True,'multirow_layout_checks':'passed'})
    print(kp,passed,'passed',flush=True)
save('engine-input.json',engine);save('examples.json',examples)
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
report['native_grading']=json.loads((HERE/'engine-report.json').read_text())
report['shared_formatter_sha256']=sha(ROOT/'scripts/question_capture/math_format.py')
report['total_sampled_records']=sum(g['sampled_records'] for g in report['generators'])
report['passed']=True
save('verification.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ('generators','native_grading')},indent=2))
