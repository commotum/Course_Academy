#!/usr/bin/env python3
"""Read actual displayed endpoint tokens; independently construct SymPy sets.
Native radio grading is separate from full-bank and solution mathematics.
"""
import hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('kp',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x): (HERE/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def endpoint(s):
    s=s.strip().replace(' ','')
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
    s=re.sub(r'\\sqrt\{(\d+)\}',r'*sqrt(\1)',s)
    if s.startswith('*'):s=s[1:]
    if s.startswith('-*'):s='-'+s[2:]
    assert re.fullmatch(r'[-0-9()+*/sqrt]+',s),s
    return sp.sympify(s)
def parse(s):
    s=s.strip();s=s.replace(r'\leq','≤').replace(r'\le','≤')
    if '∈' in s:
        v,rest=s.split('∈');v=v.strip();rest=rest.strip();a,b=rest[1:-1].split(',');lc=rest[0]=='[';rc=rest[-1]==']';a,b=endpoint(a),endpoint(b)
    else:
        parts=re.split(r'\s*(≤|<)\s*',s);assert len(parts)==5,s
        a,op,v,op2,b=parts;a,b=endpoint(a),endpoint(b);lc=op=='≤';rc=op2=='≤'
    assert v in ('x','y','t','u'),v
    val=sp.EmptySet if a>b else sp.Interval(a,b,left_open=not lc,right_open=not rc)
    return val,(a,b,v,lc,rc)
def format_check(s):
    assert s.replace('$$','').count('$')%2==0,s
    n=0
    for c in s:
        n+=(c=='{')-(c=='}');assert n>=0,s
    assert n==0,s
    assert not re.search(r'\\\\[A-Za-z]',s),s

def inspect(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];uuid.UUID(q[':question/id']);fs=q[':question/answer-fields'];assert len(fs)==1
    f=fs[0];uuid.UUID(f[':answer-field/id']);assert f[':answer-field/key']=='selection';assert f[':answer-field/type']==':answer-field.type/radio'
    raw=r['generation']['raw_missing_fields_preserved'];vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==5
    prompt=re.search(r'\$(.*?)\$',q[':question/problem']).group(1);ps,info=parse(prompt)
    answers=[parse(s)[0] for s in vals];assert len(set(answers))==5,vals
    assert answers.count(ps)==1,vals
    for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math';format_check(a[':answer/value'])
    format_check(q[':question/problem'])
    if raw:
        assert ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q
    else:
        assert q[':question/difficulty']==':question.difficulty/'+r['generation']['difficulty']
        assert q[':question/difficulty'] in (':question.difficulty/easy',':question.difficulty/moderate',':question.difficulty/hard')
        ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
        found=[a for a in f[':answer-field/choices'] if a[':answer/id']==ref[1]];assert len(found)==1 and parse(found[0][':answer/value'])[0]==ps
        solution=q[':question/worked-solution'];format_check(solution);assert solution.startswith(g.OPENING)
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(blocks)==2
        assert all(parse(b)[0]==ps for b in blocks)
        assert parse(blocks[0])[1]==info
        for side,index,closed in [('left',0,info[3]),('right',1,info[4])]:
            m=re.search(r'The '+side+r' endpoint \$(.*?)\$ (.*?) included in the interval. Therefore, we use \$(.*?)\$',solution)
            assert m and endpoint(m[1])==info[index]
            assert ('is not' in m[2])==(not closed)
            expected=('[' if closed else '(') if side=='left' else (']' if closed else ')')
            if '∈' in prompt:expected=r'\le' if closed else '<'
            assert m[3].strip()==expected,(m[3],expected)
    return True

def main():
    capture=json.loads((HERE/'source.json').read_text());sources=capture['record'][':knowledge-point/questions'];cases=json.loads((HERE/'source-cases.json').read_text())
    originals=[];normal_sources=[]
    matched_options=matched_banks=0
    for q,c in zip(sources,cases):
        r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);inspect(r);originals.append(r)
        out=r['question'];assert out[':question/problem']==q[':question/problem']
        assert ':question/worked-solution' not in out and ':question/worked-solution' not in q
        f=out[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
        assert f[':answer-field/key']==sf[':answer-field/key'];assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        assert ':answer-field/correct' not in f and ':answer-field/correct' not in sf
        matched_options+=5;matched_banks+=1
        n=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'].removesuffix('_raw'));inspect(n);normal_sources.append(n)
    records=[]
    for level in g.LEVELS:
        for t in g.TEMPLATES:
            for seed in range(60):
                r=g.generate(level,seed,template=t);inspect(r);records.append(r)
    # Every raw/repaired observed profile is also parameterized away from source.
    profiles=[]
    for c in cases:
        p=dict(c['parameters']);p['a']='-6' if '25754' in c['source_id'] else '3';p['b']='3*sqrt(2)' if '25754' in c['source_id'] else '11';p['variable']='t'
        for suffix in ('_raw',''):
            prof=c['bank_profile'].removesuffix('_raw')+suffix
            r=g.generate(c['level'],seed=31,template=c['template'],parameters=p,profile=prof);inspect(r);profiles.append(r)
    # IDs do not depend on order or seed; equivalent endpoint spelling deduplicates.
    for r in records[:40]+normal_sources:
        d=r['generation'];n=g.generate(d['difficulty'],999,template=d['template'],parameters=d['parameters'],profile=d['profile']);assert n['question'][':question/id']==r['question'][':question/id'];assert n['generation']['mathematical_fingerprint']==d['mathematical_fingerprint']
    p={'a':'-1/2','b':'3/2','variable':'x','left_closed':True}
    a=g.generate('moderate',parameters=p);p['a']='-2/4';b=g.generate('moderate',parameters=p);assert a['question'][':question/id']==b['question'][':question/id']
    # Variable aliases excluded from semantic catalog, retained in display identity.
    p['variable']='y';b=g.generate('moderate',template=a['generation']['template'],parameters=p);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
    invalid=[('easy',{'a':'-1','b':'3','variable':'x','left_closed':True}),('moderate',{'a':'-1','b':'3','variable':'x','left_closed':True}),('hard',{'a':'-1','b':'3','variable':'x','left_closed':True}),('hard',{'a':'-sqrt(2)/2','b':'3','variable':'x','left_closed':True}),('hard',{'a':'sqrt(2)','b':'3','variable':'x','left_closed':True})]
    for l,p in invalid:
        try:g.generate(l,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('unguarded level',l,p))
    # Completed observed profiles obey authored bounds; only unrated raw evidence bypasses them.
    profile_invalid=[('easy','interval_to_inequality','observed_25754',{'a':'-5','b':'2*sqrt(2)','variable':'y','left_closed':True}),('hard','inequality_to_interval','observed_1253',{'a':'9','b':'13','variable':'x','left_closed':False}),('moderate','inequality_to_interval','observed_1253',{'a':'3','b':'11','variable':'x','left_closed':False})]
    for level,template,profile,parameters in profile_invalid:
        try:g.generate(level,template=template,profile=profile,parameters=parameters)
        except ValueError:pass
        else:raise AssertionError(('completed observed profile bypasses authored workload',level,profile))
    review=normal_sources+profiles
    for level in g.LEVELS:
        for t in g.TEMPLATES:review.append(g.generate(level,17,template=t))
    # Native grader: every correct and every wrong option, 10 reviewed normal records.
    normal=[r for r in review if not r['generation']['raw_missing_fields_preserved']]
    fixtures=[]
    for i,r in enumerate(normal):
        f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
        fixtures.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'complete radio bank ID selection'} for a in f[':answer-field/choices']]})
    save('engine-input.json',fixtures)
    subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    save('review.json',{'original_raw':originals,'generated':review})
    lines=['# Half-open intervals review','Original practice payloads: two unrated, no observed answer keys/solutions. Raw API replay retains all omissions.','']
    for i,r in enumerate(originals+review):
        lines+=['## '+('Raw original replay' if i<2 else 'Generated / minimally completed')+' — '+r['generation']['profile']+' / '+r['generation']['difficulty'],g.markdown(r),'']
    (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
    # Actual decoded string bytes, not escaped tool output.
    strings=[q[':question/problem'] for q in sources]+[a[':answer/value'] for q in sources for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    slash={'adjacent_raw_backslash_pairs':sum(s.count(chr(92)*2) for s in strings),'source_strings':len(strings),'teaching_repairs':0};assert slash['adjacent_raw_backslash_pairs']==0
    hashes={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('source.json','source-cases.json','authoritative-widget.json','classification.md','template-extraction.md','README.md','review.json','review.md','engine-input.json','engine-report.json','validate.py')};hashes['../17592186059827.py']=hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
    save('validation.json',{'pass':True,'source':capture|{'record':'preserved in source.json'},'fidelity':{'exact_prompts':{'matched':2,'total':2},'exact_complete_banks':{'matched':matched_banks,'total':2},'exact_displayed_choices':{'matched':matched_options,'total':10},'raw_missing_key_rating_solution_preserved':{'matched':2,'total':2},'observed_keys':{'matched':0,'total':0},'observed_solutions':{'matched':0,'total':0},'authored_derived_keys':{'correct':2,'total':2},'authored_solutions':{'checked':2,'total':2},'raw_native_grading_ineligible_missing_correct_refs':2},'displayed_math_checks':len(records)+len(profiles)+4,'sampled_per_level_template':60,'normal_observed_profile_guard_rejections':len(profile_invalid),'raw_source_byte_checks':slash,'semantic_catalog_counts':{l:len(g._CATALOG[l])*2 for l in g.LEVELS},'engine':json.loads((HERE/'engine-report.json').read_text())|{'records':'see engine-report.json'},'frozen_hashes':hashes,'unresolved':['Original practice difficulty, correct refs and worked solutions were not captured; no observed matches claimed.'],'database_writes':0})
    print('PASS: 2/2 raw prompts, 10/10 exact choices, 2/2 complete banks; 360 authored + 4 changed observed-profile cases; native bank grading passed.')
if __name__=='__main__':main()
