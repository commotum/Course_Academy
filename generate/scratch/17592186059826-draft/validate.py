#!/usr/bin/env python3
"""Printed-value/set parsing, exact original fidelity, slot/structure guards and native grading."""
from __future__ import annotations
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys, uuid
from collections import Counter
from functools import lru_cache
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT.with_suffix('.py')
SPEC=importlib.util.spec_from_file_location('open_interval_draft',SCRIPT)
g=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(g)
SOURCE=json.loads((ROOT/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
CANONICAL=SOURCE['record'][':knowledge-point/canonical-example']

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def identifier(*parts): return str(uuid.uuid5(uuid.UUID('74f45f69-d8e7-5e79-a1ec-38d8912cbc19'),'|'.join(parts)))

def clean(text):
    text=re.sub(r'\{\\color\{(?:red|blue)\}\{([^{}]*)\}\}',r'\1',text)
    return text.replace(r'\,','').strip().replace('$','').rstrip('.?').strip()

@lru_cache(maxsize=2048)
def number(text):
    text=text.strip().replace('−','-').replace(' ','')
    if text in ('-∞',r'-\infty'): return -sp.oo
    match=re.fullmatch(r'(-?)\\sqrt\{(\d+)\}',text)
    if match: return (-1 if match[1] else 1)*sp.sqrt(int(match[2]))
    match=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',text)
    if match: return (-1 if match[1] else 1)*sp.Rational(int(match[2]),int(match[3]))
    assert re.fullmatch(r'-?\d+',text),text
    return sp.Integer(text)

@lru_cache(maxsize=8192)
def set_object(text):
    text=clean(text)
    if '∈' in text or re.search(r'\\in(?![a-z])',text):
        match=re.fullmatch(r'([xyzt])\s*(?:∈|\\in)\s*(.*)',text); assert match,text
        obj,_=set_object(match[2]); return obj,'membership'
    if text.startswith(('(','[')):
        assert text[-1] in ')]',text
        a,b=map(number,text[1:-1].split(',')); assert a<b
        return sp.Interval(a,b,left_open=text[0]=='(',right_open=text[-1]==')'),'interval'
    if ' or ' in text:
        match=re.fullmatch(r'([xyzt])\s*<\s*(.*?)\s+or\s+\1\s*>\s*(.*)',text); assert match,text
        a,b=number(match[2]),number(match[3]); assert a<b
        return sp.Union(sp.Interval.open(-sp.oo,a),sp.Interval.open(b,sp.oo)),'outside'
    match=re.fullmatch(r'(.*?)\s*(\\le|<)\s*([xyzt])\s*(\\le|<)\s*(.*)',text); assert match,text
    a,b=number(match[1]),number(match[5]); assert a<b
    return sp.Interval(a,b,left_open=match[2]=='<',right_open=match[4]=='<'),'inequality'

def formatting(text):
    assert isinstance(text,str)
    assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0 control character'
    assert '\\\\' not in text,'doubled raw backslash'
    # Inline/display delimiters pair by kind; a dangling dollar cannot be hidden.
    tokens=re.findall(r'\$\$|\$',text); pending=None
    for token in tokens:
        if pending is None: pending=token
        else: assert pending==token,'mixed math delimiter pair'; pending=None
    assert pending is None,'unclosed math delimiter'
    balance=0
    for c in text:
        if c=='{': balance+=1
        elif c=='}': balance-=1; assert balance>=0,'unbalanced brace'
    assert balance==0

def prompt_components(prompt):
    values=re.findall(r'\$(.*?)\$',prompt)
    assert len(values)==1
    text=clean(values[0])
    if '∈' in text:
        match=re.fullmatch(r'([xyzt]) ∈ \((.*?), (.*?)\)',text); assert match,text
        a,b,v=match[2],match[3],match[1]; direction='interval_to_inequality'
    else:
        match=re.fullmatch(r'(.*?)\s*<\s*([xyzt])\s*<\s*(.*)',text); assert match,text
        a,b,v=match[1].strip(),match[3].strip(),match[2]; direction='inequality_to_interval'
    expected=sp.Interval.open(number(a),number(b))
    assert expected.start<expected.end
    return a,b,v,direction,expected

# Independent source-driven full prose/mask reconstruction; no generator solution call.
def expected_solution(a,b,v,direction):
    base=CANONICAL[':question/worked-solution'] if direction=='interval_to_inequality' else ORIGINALS['q-1256'][':question/worked-solution']
    if direction=='interval_to_inequality':
        rows=[v+r'\in {\color{red}{(}}'+a+', '+b+r'{\color{red}{)}}',a+r' \,\,{\color{red}{<      }}\,\,      '+v+r'  \,\,{\color{red}{<      }}\,\,      '+b]
    else:
        base=base.replace('endpoints $-3$ and $-1$','endpoints $'+a+'$ and $'+b+'$')
        rows=[a+r'\,\,<\,\,'+v+r'\,\,<\,\,'+b,'('+a+','+b+')',v+r'\in ('+a+','+b+').']
    index=iter(rows)
    return re.sub(r'\$\$\n.*?\n\$\$',lambda _: '$$\n'+next(index)+'\n$$',base,flags=re.S)

def assert_level(a,b,level,profile):
    # Independent level constraints on REDUCED displayed values, not metadata guard.
    if level=='easy':
        if profile=='compact_ray':
            assert sp.simplify(a+b)==0 and a<0 and b>0
            assert b**2 in (2,3,5,6,7,10,11,13)
        else:
            assert a.is_Integer and b.is_Integer and -12<=a<b<=12
            if profile=='compact_reflection': assert a+b!=0
    elif level=='moderate':
        assert a.is_Rational and b.is_Rational and -6<=a<b<=6
        assert bool(a.is_Integer)!=bool(b.is_Integer)
        assert all(q.q in (1,2,3,4) for q in (a,b))
    elif level=='hard':
        assert a.is_Rational and b.is_Rational and -6<=a<b<=6
        assert a.q in (2,3,4) and b.q in (2,3,4) and a.q!=b.q
    else: raise AssertionError(level)

def inspect(record):
    assert record['knowledge_point']=={'db_id':17592186059826,'id':'74f45f69-d8e7-5e79-a1ec-38d8912cbc19','title':'Converting Between Intervals and Inequalities: Open Intervals'}
    meta=record['generation']; q=record['question']; f=q[':question/answer-fields'][0]; answers=f[':answer-field/choices']
    assert len(q[':question/answer-fields'])==1 and len(answers)==5
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    assert len({a[':answer/id'] for a in answers})==5
    uuid.UUID(q[':question/id']); uuid.UUID(f[':answer-field/id'])
    formatting(q[':question/problem'])
    at,bt,v,direction,expected=prompt_components(q[':question/problem'])
    profile=meta['profile'].removeprefix('raw_'); level=meta['difficulty']
    assert_level(expected.start,expected.end,level,profile)
    assert meta['parameters']=={'a':str(expected.start),'b':str(expected.end),'variable':v}
    template=meta['template']
    if template=='inequality_spaced': assert q[':question/problem']==f'The inequality ${at} < {v} < {bt}$ can be expressed in interval notation as'
    elif template=='inequality_compact': assert q[':question/problem']==f'The inequality ${at}<{v}<{bt}$ can be expressed in interval notation as'
    else: assert template=='interval_to_inequality' and direction=='interval_to_inequality' and q[':question/problem']==f'Which inequality corresponds to the interval ${v} ∈ ({at}, {bt})$?'
    assert (template,profile) in (('inequality_spaced','spaced_ray'),('inequality_compact','compact_reflection'),('inequality_compact','compact_ray'),('interval_to_inequality','membership'))
    sets=[]
    for a in answers:
        uuid.UUID(a[':answer/id']); formatting(a[':answer/value'])
        assert ':answer/feedback' not in a,'original feedback absent'
        obj,role=set_object(a[':answer/value']); sets.append(obj)
        if profile=='membership': assert a[':answer/type']==(':answer.type/text' if role=='outside' else ':answer.type/math')
        else: assert a[':answer/type']==':answer.type/math' and role=='interval'
        assert a[':answer/id']==identifier(f[':answer-field/id'],a[':answer/type'].split('/')[-1],a[':answer/value'])
    assert all(a!=b for a,b in itertools.combinations(sets,2)),'equivalent options (including wrong-wrong pairs)'
    assert sum(obj==expected for obj in sets)==1
    # Independently derive all expected bank sets from the printed ordered endpoints.
    base_sets={expected,sp.Interval(expected.start,expected.end),sp.Interval(expected.start,expected.end,left_open=True),sp.Interval(expected.start,expected.end,right_open=True)}
    extra=sp.Union(sp.Interval.open(-sp.oo,expected.start),sp.Interval.open(expected.end,sp.oo)) if profile=='membership' else sp.Interval.open(-expected.end,-expected.start) if profile=='compact_reflection' else sp.Interval.open(-sp.oo,expected.end)
    assert set(sets)==base_sets|{extra}
    raw=meta['profile'].startswith('raw_'); omitted=raw and profile in ('spaced_ray','membership')
    assert meta['evidence_only']==raw and meta['eligible_for_learning']==(not raw)
    if omitted:
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q and ':answer-field/correct' not in f
    else:
        assert q[':question/difficulty']==':question.difficulty/'+level
        correct=f[':answer-field/correct']; assert correct[0]==':answer/id'
        assert sets[next(i for i,a in enumerate(answers) if a[':answer/id']==correct[1])]==expected
        sol=q[':question/worked-solution']; formatting(sol)
        assert sol==expected_solution(at,bt,v,direction),'full source-derived solution prose/mask mismatch'
        rows=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
        roles=('membership','inequality') if direction=='interval_to_inequality' else ('inequality','interval','membership')
        assert len(rows)==len(roles)
        for row,role in zip(rows,roles):
            obj,actual_role=set_object(row); assert obj==expected and actual_role==role
            # Check variable use from actual printed rows before any alias normalization.
            if role in ('membership','inequality'): assert re.findall(r'(?<![a-z])[xyzt](?![a-z])',row)==[v]
    identity={'version':meta['version'],'difficulty':None if omitted else level,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted((a[':answer/value'],a[':answer/type'].split('/')[-1]) for a in answers),'correct':None if omitted else next(a[':answer/value'] for a in answers if a[':answer/id']==f[':answer-field/correct'][1])}
    identity_hash=digest(identity)
    assert meta['content_fingerprint']==identity_hash and q[':question/id']==identifier('question',identity_hash)
    assert f[':answer-field/id']==identifier(q[':question/id'],'selection')
    assert meta['mathematical_fingerprint']==digest({'direction':direction,'a':str(expected.start),'b':str(expected.end),'endpoint_reading_policy':level})
    assert meta['python_version']==sys.version.split()[0] and meta['sympy_version']==sp.__version__
    return direction,expected

def bank(q):
    return sorted((a[':answer/value'],a[':answer/type'] if isinstance(a[':answer/type'],str) else a[':answer/type'][':db/ident']) for a in q[':question/answer-fields'][0][':answer-field/choices'])

assert SOURCE['basis']==2275 and len(SOURCE['record'][':knowledge-point/questions'])==7 and len(ORIGINALS)==4
refresh=ROOT.parents[1]/'runs/current/refresh-2026-10-14/sources/17592186059826.json'
assert (ROOT/'source.json').read_bytes()==refresh.read_bytes(),'immutable wrapper copy'
cases=json.loads((ROOT/'source-cases.json').read_text()); assert {c['source_id'] for c in cases}==set(ORIGINALS) and len(cases)==4
inventory=json.loads((ROOT/'independent-inventory.json').read_text())
assert {k:inventory[k] for k in ('database','basis','lineage')}=={k:SOURCE[k] for k in ('database','basis','lineage')}
independent=[q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
assert len(inventory['questions'])==len(independent)==3
for row,original in zip(inventory['questions'],independent):
    assert row['record']==original and row['role']=='independently authored inventory' and row['relationship_to_source_templates']
    # Inventory correctness is distinct from original template-fidelity/difficulty evidence.
    _,_,_,_,expected=prompt_components(original[':question/problem'])
    for answer in original[':question/answer-fields'][0][':answer-field/choices']: set_object(answer[':answer/value'])
    assert set_object(original[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])[0]==expected

fidelity=[]; native_records=[]; original_review=[]; raw_review=[]
for case in cases:
    original=ORIGINALS[case['source_id']]
    raw=g.generate(case['difficulty'],17,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']); inspect(raw)
    normal=g.generate(case['difficulty'],17,template=case['template'],parameters=case['parameters'],profile=case['normal_profile']); inspect(normal)
    q=raw['question']; f=q[':question/answer-fields'][0]; original_field=original[':question/answer-fields'][0]
    assert q[':question/problem']==original[':question/problem'] and bank(q)==bank(original)
    assert original_field[':answer-field/key']==f[':answer-field/key'] and original_field[':answer-field/type'][':db/ident']==f[':answer-field/type']
    for key in (':question/difficulty',':question/worked-solution'):
        assert (key in q)==(key in original),'per-original presence parity'
        if key in original: assert q[key]==(original[key][':db/ident'] if isinstance(original[key],dict) else original[key])
    assert (':answer-field/correct' in f)==(':answer-field/correct' in original_field)
    if ':answer-field/correct' in original_field:
        value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert value==original_field[':answer-field/correct'][':answer/value']
        # Normal operative source solution must be exact too, not only raw replay.
        assert normal['question'][':question/worked-solution']==original[':question/worked-solution']
    fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'displayed_bank_values_types_exact':5,'attribute_presence_exact':True,'captured_correct_ref_available':':answer-field/correct' in original_field,'captured_solution_available':':question/worked-solution' in original,'captured_difficulty_available':':question/difficulty' in original})
    native_records.append((case['source_id']+' normal enrichment',normal)); original_review.append(normal); raw_review.append(raw)
assert g.membership_solution('1','5','x')==CANONICAL[':question/worked-solution']
# Inspect decoded strings; JSON escaping is not a raw adjacent-backslash anomaly.
byte_evidence=[]
for q in [CANONICAL,*ORIGINALS.values()]:
    strings=[q[':question/problem']]+([q[':question/worked-solution']] if ':question/worked-solution' in q else [])+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
    assert all('\\\\' not in text for text in strings)
    byte_evidence.append({'source_id':q[':question/math-academy-id'],'adjacent_backslash_pairs':sum(text.count('\\\\') for text in strings),'C0_anomalies':sum(any(ord(c)<32 and c not in '\n\t' for c in text) for text in strings)})

# Enumerate each complete-profile domain and deduplicate mathematical tasks across layouts/banks.
counts={}; profile_counts={}; slot_coverage={}; exhaustive=0
for level in ('easy','moderate','hard'):
    fingerprints=set(); profile_counts[level]={}; slot_coverage[level]={}
    for profile in g.BANKS:
        pool=g.catalog(level,profile); profile_counts[level][profile]=len(pool)
        lower=set(); upper=set(); forms=Counter()
        for a,b in pool:
            rec=g.generate(level,template=g.BANKS[profile][0],parameters={'a':a,'b':b},profile=profile)
            inspect(rec); fingerprints.add(rec['generation']['mathematical_fingerprint']); exhaustive+=1;lower.add(a);upper.add(b)
            forms['radical' if 'sqrt' in a+b else 'rational' if '/' in a+b else 'integer']+=1
        slot_coverage[level][profile]={'lower_values':sorted(lower),'upper_values':sorted(upper),'endpoint_forms':dict(forms),'all_catalog_pairs_checked':len(pool)}
    counts[level]=len(fingerprints)
    print('Exhaustive',level,profile_counts[level],flush=True)

# Default family/bank coverage: all four eligible profiles must be selected before parameters.
default_coverage={}
for level in ('easy','moderate','hard'):
    profiles=Counter(); templates=Counter()
    for seed in range(160):
        rec=g.generate(level,seed); inspect(rec); profiles[rec['generation']['profile']]+=1; templates[rec['generation']['template']]+=1
    assert set(profiles)==set(g.BANKS) and set(templates)==set(g.TEMPLATES)
    default_coverage[level]={'profiles':dict(profiles),'templates':dict(templates)}

# Changed endpoint with other data held fixed, variable aliases, deterministic shuffling and identity.
changed_cases=[('easy','spaced_ray',{'a':3,'b':7},{'a':3,'b':8}),('easy','compact_reflection',{'a':-3,'b':-1},{'a':-4,'b':-1}),('easy','compact_ray',{'a':'-sqrt(2)','b':'sqrt(2)'},{'a':'-sqrt(3)','b':'sqrt(3)'}),('easy','membership',{'a':3,'b':4},{'a':3,'b':5})]
for level,profile,p1,p2 in changed_cases:
    r1=g.generate(level,profile=profile,parameters=p1);r2=g.generate(level,profile=profile,parameters=p2);inspect(r1);inspect(r2)
    assert r1['generation']['mathematical_fingerprint']!=r2['generation']['mathematical_fingerprint']
    assert r1['question'][':question/worked-solution']!=r2['question'][':question/worked-solution']
for level in ('easy','moderate','hard'):
    for profile in g.BANKS:
        pool=g.catalog(level,profile)
        for a,b in (pool[0],pool[-1],pool[len(pool)//2]):
            ref=g.generate(level,3,profile=profile,parameters={'a':a,'b':b}); other=g.generate(level,11,profile=profile,parameters={'a':a,'b':b});inspect(ref);inspect(other)
            assert ref['question'][':question/id']==other['question'][':question/id']
            for variable in ('y','t','z'):
                alias=g.generate(level,11,profile=profile,parameters={'a':a,'b':b,'variable':variable}); inspect(alias)
                assert alias['generation']['mathematical_fingerprint']==ref['generation']['mathematical_fingerprint']
for profile in g.BANKS:
    positions=set()
    for seed in range(20):
        a,b=g.catalog('easy',profile)[0]; rec=g.generate_easy(seed,profile=profile,parameters={'a':a,'b':b});f=rec['question'][':question/answer-fields'][0]
        positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    assert len(positions)>1
alias1=g.generate_hard(profile='compact_ray',parameters={'a':'2/4','b':'4/3'});alias2=g.generate_hard(profile='compact_ray',parameters={'a':'1/2','b':'8/6'})
assert alias1['question'][':question/id']==alias2['question'][':question/id']
# Explicit valid endpoints without a bank choose only whole eligible profiles.
for seed in range(20):
    inspect(g.generate_easy(seed,parameters={'a':'-sqrt(2)','b':'sqrt(2)'}))
    inspect(g.generate_easy(seed,parameters={'a':-3,'b':3}))
layout1=g.generate_moderate(profile='spaced_ray',parameters={'a':1,'b':'3/2'});layout2=g.generate_moderate(profile='compact_ray',parameters={'a':1,'b':'3/2'})
assert layout1['generation']['mathematical_fingerprint']==layout2['generation']['mathematical_fingerprint']
assert layout1['question'][':question/id']!=layout2['question'][':question/id']

bad_calls=[('easy','compact_reflection',{'a':-3,'b':3}),('easy','compact_ray',{'a':'-sqrt(2)','b':'sqrt(3)'}),('easy','spaced_ray',{'a':1,'b':'3/2'}),('moderate','membership',{'a':1,'b':2}),('moderate','spaced_ray',{'a':'1/2','b':'2/3'}),('hard','compact_ray',{'a':'1/2','b':2}),('hard','membership',{'a':'1/2','b':'3/2'}),('hard','membership',{'a':'1/5','b':'2/3'}),('moderate','spaced_ray',{'a':-7,'b':'-13/2'}),('hard','compact_ray',{'a':'-25/4','b':'1/3'}),('easy','spaced_ray',{'a':3,'b':2}),('easy','spaced_ray',{'a':'sqrt(x)','b':5})]
for level,profile,parameters in bad_calls:
    try: g.generate(level,profile=profile,parameters=parameters)
    except ValueError: pass
    else: raise AssertionError(('invalid public parameters accepted',level,profile,parameters))
try: g.generate_moderate(profile='raw_membership')
except ValueError: pass
else: raise AssertionError('raw missing difficulty promoted to authored difficulty')
try: g.generate_easy(template='inequality_compact',profile='membership')
except ValueError: pass
else: raise AssertionError('mismatched family/profile accepted')

# Mutation regressions: not just row counts/algebraic equality; reject stale prose and wrong pair semantics.
mutations=[]
base=original_review[2]
for name,mutator in [
 ('control character',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\f')),
 ('same-value wrong stage structure',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('$$\n(-3,-1)\n$$','$$\nx\\in (-3,-1)\n$$'))),
 ('stale prose endpoint',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('endpoints $-3$','endpoints $-4$'))),
 ('wrong-wrong equivalent options',lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][1].__setitem__(':answer/value',r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])),
 ('changed prompt stale solution',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('-3<x','-4<x')))
]:
    mutated=copy.deepcopy(base);mutator(mutated)
    try: inspect(mutated)
    except (AssertionError,ValueError,KeyError): mutations.append({'mutation':name,'rejected':True})
    else: raise AssertionError(('mutation undetected',name))

# Review every observed bank plus two changed instances per bank and EACH level.
review=[]
for level in ('easy','moderate','hard'):
    for profile in g.BANKS:
        for seed in (7,19):
            rec=g.generate(level,seed,profile=profile);inspect(rec);review.append(rec);native_records.append((level+'/'+profile+'/seed'+str(seed),rec))
(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
lines=['# Basis 2275 original evidence and generated draft review','','Only four MA-identified originals establish source fidelity. The three independent inventory records are copied exactly in independent-inventory.json and remain separate from recovered-original difficulty/template evidence. All generated moderate/hard labels are authored.']
for case,raw,normal in zip(cases,raw_review,original_review):
    lines+=['','## Original '+case['source_id']+' / '+case['bank_profile'],'','**Public exact raw replay:**','',g.markdown(raw),'','**Normal source-shaped record (missing attributes enriched only where absent):**','',g.markdown(normal)]
for rec in review:
    m=rec['generation'];lines+=['','## Generated '+m['difficulty']+' / '+m['profile']+' / seed '+str(m['seed']),'','Authored endpoint sampling; '+('missing-level label authored.' if m['difficulty']!='easy' else 'easy is observed for the compact source families; other easy assignments are authored.'),'',g.markdown(rec)]
(ROOT/'review.md').write_text('\n'.join(lines)+'\n')
engine_input=[]
for label,rec in native_records:
    f=rec['question'][':question/answer-fields'][0]
    engine_input.append({'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio selection; complete displayed set independently parsed, all wrong-wrong equivalences checked'} for a in f[':answer-field/choices']]})
(ROOT/'engine-input.json').write_text(json.dumps(engine_input,indent=2,ensure_ascii=False)+'\n')
engine=ROOT.parents[1]/'runs/current/check-engine'
subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
# CLI must render omission profiles, never assume correct/difficulty/solution presence.
for profile in ('raw_spaced_ray','raw_membership','raw_compact_ray'):
    subprocess.run([sys.executable,'-B',str(SCRIPT),'--difficulty','easy','--profile',profile,'--seed','7','--format','markdown'],stdout=subprocess.DEVNULL,check=True)
baseline=json.loads((ROOT/'baseline-hashes.json').read_text())
for path,expected_hash in baseline.items(): assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected_hash,'registered baseline changed'
report={'status':'worker_validation_passed_pending_parent_QA','source':{k:SOURCE[k] for k in ('database','basis','lineage')},'current_pool':7,'MA_originals':4,'independent_inventory_exact':{'matched':3,'total':3},'source_fidelity':{'rows':fidelity,'prompts':{'matched':4,'total':4},'complete_banks':{'matched':4,'total':4},'displayed_options':{'matched':20,'total':20},'original_distractors':{'matched':16,'total':16},'captured_correct_refs':{'matched':2,'available':2,'missing':2},'captured_worked_solutions':{'matched':2,'available':2,'missing':2},'captured_difficulties':{'matched':2,'available':2,'missing':2},'canonical_solution':{'matched':1,'total':1},'raw_attribute_presence_parity':4,'normal_complete_original_solutions_exact':2},'source_byte_checks':byte_evidence,'mathematical_validation':{'exhaustive_profile_instances':exhaustive,'finite_tasks_deduplicated_across_banks_layouts':counts,'profile_catalog_counts':profile_counts,'structural_conversion_methods':2,'slot_coverage':slot_coverage,'default_coverage':default_coverage,'mutation_regressions':mutations},'native_grading':json.loads((ROOT/'engine-report.json').read_text()),'equivalent_free_entry_checks':'Not applicable to the observed radio contract; native owned selection checks are separate from full set-equivalence checks of every bank pair.','review_records':len(review),'baseline_unchanged':True,'authored_extensions':['Missing correct refs independently derived for q-102204/q-59294','Missing worked solutions supplied by operative source/canonical masks','Unrated originals assigned easy by explicit authored policy','Moderate: one integer and one noninteger rational endpoint','Hard: two noninteger rational endpoints with different reduced denominators'],'unresolved_findings':[],'native_engine_provenance':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (engine,engine.with_suffix('.rs'),engine.parent/'engine-build.log')},'frozen_hashes':{str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SCRIPT,*sorted(ROOT.glob('*'))] if p.is_file() and p.name!='validation.json'}}
(ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('PASS:',exhaustive,'exhaustive bank instances; source 4/4 banks,20/20 options; finite tasks',counts)
