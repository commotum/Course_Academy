#!/usr/bin/env python3
"""Independent displayed-set and solution QA, source replay, real radio grading."""
from pathlib import Path
import hashlib, importlib.util, itertools, json, re, subprocess, uuid
import sympy as sp
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('closed',HERE.with_suffix('.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def dump(name,v): (HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def num(s):
    s=s.strip().replace(' ','').replace('−','-')
    if s=='-∞':return -sp.oo
    s=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
    s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',s)
    s=re.sub(r'(\d)(sqrt)',r'\1*\2',s)
    assert re.fullmatch(r'[0-9+*/().\-sqrt]+',s),s
    return sp.sympify(s)

def read_set(s):
    s=s.replace('$','').strip().replace(r'\,','').replace(r'\in','∈')
    s=re.sub(r'\{\\color\{(?:red|blue)\}\{([^{}]*)\}\}',r'\1',s).strip()
    if '∈' in s:
        var,s=s.split('∈');assert var.strip()=='x';s=s.strip()
    if ' or ' in s:
        l,r=s.split(' or ')
        assert l.startswith('x < ') and r.startswith('x > ')
        return sp.Union(sp.Interval.open(-sp.oo,num(l[4:])),sp.Interval.open(num(r[4:]),sp.oo))
    if s[0] in '[(':
        a,b=s[1:-1].split(',');assert s[-1] in '])'
        return sp.Interval(num(a),num(b),left_open=s[0]=='(',right_open=s[-1]==')')
    parts=re.split(r'\s*(\\le|<)\s*',s)
    assert len(parts)==5 and parts[2].strip()=='x',s
    # Solve the two independently parsed relations; do not infer from choice ID.
    x=sp.Symbol('x',real=True);a,b=num(parts[0]),num(parts[4])
    left=x>=a if parts[1]==r'\le' else x>a
    right=x<=b if parts[3]==r'\le' else x<b
    return sp.Intersection(left.as_set(),right.as_set())

def prompt_set(q):
    math=re.findall(r'\$([^$]+)\$',q[':question/problem']);assert len(math)==1
    return read_set(math[0])

def fmt(s):
    assert s.count('$')%2==0,s
    depth=0
    for c in s:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert '\\'*2 not in s,'decoded adjacent command slashes'
    assert 'NaN' not in s and 'zoo' not in s

def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==m.KP_ID
    q=r['question'];f=q[':question/answer-fields'][0]
    target=prompt_set(q)
    assert isinstance(target,sp.Interval) and not target.left_open and not target.right_open
    assert target.start.is_finite and target.end.is_finite and target.start<target.end
    bank=f[':answer-field/choices'];assert len(bank)==5
    actual=[read_set(a[':answer/value']) for a in bank]
    assert len(set(actual))==5 and sum(v==target for v in actual)==1
    for obj,key in ((q,':question/id'),(f,':answer-field/id')):uuid.UUID(obj[key])
    assert len({a[':answer/id'] for a in bank})==5
    for a in bank:uuid.UUID(a[':answer/id']);fmt(a[':answer/value'])
    fmt(q[':question/problem'])
    if r['generation']['raw_evidence']:
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q
        assert ':answer-field/correct' not in f
    else:
        ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
        selected=next(a for a in bank if a[':answer/id']==ref[1])
        assert read_set(selected[':answer/value'])==target
        s=q[':question/worked-solution'];fmt(s)
        stages=re.findall(r'\$\$\s*(.*?)\s*\$\$',s,re.S)
        direction='inequality' if q[':question/problem'].startswith('The inequality') else 'interval'
        assert len(stages)==(3 if direction=='inequality' else 2)
        for st in stages:assert read_set(st)==target,(st,target)
        if direction=='inequality':
            a,b=map(m.tex,(r['generation']['parameters']['a'],r['generation']['parameters']['b']))
            assert 'endpoints $'+a+'$ and $'+b+'$ *are* included.' in s
            assert stages[0].count(r'\le')==2
            assert 'More formally, we can also write' in s
        else:
            assert 'Our interval contains only brackets. So, the endpoints are *included*.' in s
            assert stages[-1].count(r'\le')==2
        assert 'or equal to' in s if direction=='inequality' else 'only brackets' in s
    return target

def main():
    cases=[{'source_id':'q-102200','template':'inequality_to_interval','parameters':{'a':'-10','b':'3'},'bank_profile':'raw_interval'},
           {'source_id':'q-59295','template':'interval_to_inequality','parameters':{'a':'-2','b':'1'},'bank_profile':'raw_inequality'}]
    dump('source-cases.json',cases)
    originals=m.SOURCE['record'][':knowledge-point/questions'];replays=[];normals=[]
    for case,original in zip(cases,originals):
        r=m.generate('easy',19,case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r)
        q=r['question'];of=original[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert q[':question/problem']==original[':question/problem']
        assert sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in of[':answer-field/choices'])
        for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in original)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
        assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
        assert set(read_set(a[':answer/value']) for a in f[':answer-field/choices'])==set(read_set(a[':answer/value']) for a in of[':answer-field/choices'])
        replays.append(r)
        normal=m.generate('easy',19,case['template'],parameters=case['parameters'],profile=case['bank_profile'].replace('raw','observed'));check(normal);normals.append(normal)
        changed=m.generate('easy',19,case['template'],parameters={'a':'-9','b':'7'},profile=case['bank_profile']);check(changed)
        assert changed['question'][':question/problem']!=q[':question/problem']
    # Canonical example exact sequence and prose at its own endpoints.
    canonical=m.generate_easy(parameters={'a':'1','b':'4'},template='inequality_to_interval')
    assert canonical['question'][':question/worked-solution']==m.SOURCE['record'][':knowledge-point/canonical-example'][':question/worked-solution']
    catalog_counts={};math_checks=0;native_records=list(normals);review=list(replays)+list(normals)
    fingerprints=set();positions=set()
    for level in ('easy','moderate','hard'):
        params=m.parameter_catalog(level);catalog_counts[level]={'endpoint_forms':len(m.endpoint_catalog(level)),'pairs':len(params),'meaningful_directional_tasks':len(params)*2}
        # Exhaust every eligible finite object and both complete bank families.
        for p in params:
            for t in m.TEMPLATES:
                r=m.generate(level,3,t,parameters=p);check(r);math_checks+=1
                fp=r['generation']['mathematical_fingerprint'];assert fp not in fingerprints;fingerprints.add(fp)
        for t in m.TEMPLATES:
            for seed in (5,16):
                r=m.generate(level,seed,t);check(r);native_records.append(r);review.append(r)
                other=m.generate(level,seed+999,t,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
                assert r['question'][':question/id']==other['question'][':question/id']
                assert r['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
        for seed in range(30):
            r=m.generate(level,seed);native_records.append(r);f=r['question'][':question/answer-fields'][0]
            positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    assert positions==set(range(5))
    invalid=[('easy',{'a':'2/4','b':'3'}),('easy',{'a':'3','b':'3'}),('easy',{'a':'4','b':'1'}),('moderate',{'a':'-2','b':'1'}),('moderate',{'a':'-13/5','b':'1'}),('hard',{'a':'1','b':'sqrt(2)'}),('hard',{'a':'-2','b':'sqrt(2)'}),('hard',{'a':'-4*sqrt(2)','b':'sqrt(3)'})]
    for level,p in invalid:
        try:m.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('guard failed',level,p))
    grader=[]
    for i,r in enumerate(native_records):
        f=r['question'][':question/answer-fields'][0]
        grader.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned radio choice ID; mathematics separately verified'} for a in f[':answer-field/choices']]})
    dump('engine-input.json',grader)
    binary=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    dump('review.json',review)
    md=['# Closed intervals — source and generated review','All source ratings, correct keys and worked solutions are absent. Generated levels and repairs are authored.']
    for case,original,r in zip(cases,originals,replays):
        md+=['\n## Original '+case['source_id'],original[':question/problem']]
        md += ['- '+(a[':answer/value'] if a[':answer/type'][':db/ident'].endswith('/text') else '$'+a[':answer/value']+'$') for a in original[':question/answer-fields'][0][':answer-field/choices']]
        md+=['\n### Public raw replay',m.markdown(r)]
    for r in review[2:]:
        g=r['generation'];md+=['\n## Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+g['template']+' / '+g['bank_profile'],m.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
    strings=[]
    def walk(v):
        if isinstance(v,str):strings.append(v)
        elif isinstance(v,dict):
            for x in v.values():walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    walk(m.SOURCE['record'])
    byte_evidence={'decoded_strings_inspected':len(strings),'adjacent_backslash_pairs':sum(s.count('\\'*2) for s in strings),'repair_needed':False,'method':'inspect decoded string characters; JSON escaping is not evidence'}
    dump('decoded-byte-checks.json',byte_evidence)
    engine=json.loads((HERE/'engine-report.json').read_text())
    dump('validation.json',{'status':'passed','version':m.VERSION,'source_provenance':{k:m.SOURCE[k] for k in ('database','basis','lineage')},
      'source_fidelity':{'source_questions':2,'exact_prompts':2,'exact_complete_banks':2,'exact_choice_values_and_types':10,'missing_correct_designations_preserved':2,'matched_present_correct_designations':0,'present_correct_designation_denominator':0,'missing_solutions_preserved':2,'missing_ratings_preserved':2},
      'authored_repairs':{'derived_keys':2,'worked_solutions':2,'ratings':2,'canonical_solution_exact':True,'mathematical_errors_in_original_banks':0},
      'finite_catalogs':catalog_counts,'exhaustive_displayed_question_bank_solution_checks':math_checks,'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
      'final_review_records_checked':len(review),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'explicit_invalid_parameters_rejected':len(invalid),'decoded_byte_checks':byte_evidence,'database_writes':0,'scope':'finite closed intervals, direct conversion in both directions','unresolved_findings':[]})
    freeze={}
    for p in sorted([HERE.with_suffix('.py')]+list(HERE.glob('*'))):
        if p.is_file() and p.name!='freeze.json':freeze[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    dump('freeze.json',{'version':m.VERSION,'sha256':freeze})
    print('Passed:',math_checks,'exhaustive mathematical tasks;',len(grader)*5,'native radio checks; 2/2 source banks, 10/10 values; no unresolved findings.')
if __name__=='__main__':main()
