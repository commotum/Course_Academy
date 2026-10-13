"""Read displayed polynomial trig math independently; fail closed; no transactions."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('kp',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
S,C=sp.symbols('S C'); IDEAL=sp.groebner([S*S+C*C-1],S,C)
T=standard_transformations+(implicit_multiplication_application,)

def write(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def expr(text):
    """Independent parser consumes actual displayed complete function atoms.

    A missing argument never receives a guessed variable; source q-65229 must
    fail this check in its raw profile. Only sin/cos polynomial grammar allowed.
    """
    text=text.strip().rstrip('.')
    text=re.sub(r'\\operatorname\{(sin|cos)\}|\{(sin|cos)\}',lambda m:'\\'+(m[1] or m[2]),text)
    pattern=r'\\(sin|cos)(?:\^\{?(\d+)\}?)?[\s⁡]*\{?(\\theta|\\alpha|θ|x|t)\}?'
    text=re.sub(pattern,lambda m:('S' if m[1]=='sin' else 'C')+'**'+(m[2] or '1')+' ',text)
    text=text.replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
    assert not re.search(r'[^SC0-9\s*()+\-.]',text),('Invalid displayed expression',text)
    return sp.expand(parse_expr(text,local_dict={'S':S,'C':C},transformations=T))

def equal(a,b): return IDEAL.reduce(sp.expand(a-b))[1]==0

def formatting(text):
    assert text.count('$')%2==0
    # Braces in these sources are group braces, never literal system glyphs.
    depth=0
    for c in text:
        if c=='{':depth+=1
        elif c=='}':depth-=1;assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text

def rows(solution):
    blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
    blocks+=re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',solution,re.S)
    out=[]
    for block in blocks:
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        previous=None
        for row in block.split(r'\\'):
            row=row.replace('&','').strip()
            if '=' not in row:continue
            sides=row.split('=')
            if not sides[0].strip():
                assert previous is not None; sides[0]=previous
            previous=sides[-1]
            out.append(sides)
    return out

def check(record,check_solution=True):
    q=record['question'];f=q[':question/answer-fields'][0]
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    problem=q[':question/problem']; polynomial=expr(problem.split('$')[1])
    angle_pattern=r'\\theta|\\alpha|(?<![A-Za-z\\])(?:θ|x|t)(?![A-Za-z])'
    angles=lambda text:{r'\theta' if x=='θ' else x for x in re.findall(angle_pattern,text)}
    requested_angles=angles(problem)
    assert len(requested_angles)==1
    for text in [problem,q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:formatting(text)
    for text in [q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:
        assert angles(text)<=requested_angles,('Mismatched displayed angle',text)
    values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
    assert all(not equal(x,y) for i,x in enumerate(values) for y in values[:i])
    winners=[i for i,v in enumerate(values) if equal(polynomial,v)]
    assert len(winners)==1
    if ':answer-field/correct' in f:
        assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][winners[0]][':answer/id']]
    if f[':answer-field/type'].endswith('/blank'):assert '{{selection}}' in problem and len(values)==1
    else:assert len(values)==5
    if check_solution and ':question/worked-solution' in q:
        solution_rows=rows(q[':question/worked-solution'])
        assert len(solution_rows)>=5
        for sides in solution_rows:
            evaluated=[expr(side) for side in sides]
            assert all(equal(evaluated[0],v) for v in evaluated[1:]),('Wrong displayed stage',sides)
        if record['generation'].get('authored'):
            level=q[':question/difficulty'].split('/')[-1]
            assert len(solution_rows)==(6 if level=='moderate' else 5)
            display=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
            factored_side=display[0].split('=')[1]
            expected_groups=2 if level=='hard' else 1
            assert factored_side.count(r'\cdot(')==expected_groups
            substitution=display[1].split('&')[1].split(r'\\')[0]
            assert substitution.count(r'\cdot 1')==expected_groups
    return polynomial

def domain(level):
    if level=='easy':
        for a,(p,q) in itertools.product(tuple(range(-5,0))+tuple(range(1,6)),g.MONOMIALS):
            yield {'angle':'x','a':a,'p':p,'q':q}
    elif level=='moderate':
        for family in ('opposite','same'):
            for a,b,(p,q) in itertools.product(g.COEFFICIENTS,g.COEFFICIENTS,((1,0),(0,1))):
                yield {'angle':'x','a':a,'b':b,'p':p,'q':q,'family':family}
        for a,(p,q) in itertools.product(g.COEFFICIENTS,((2,0),(0,2))):
            yield {'angle':'x','a':a,'b':a,'p':p,'q':q,'family':'complement'}
    else:
        for a,b,p,n in itertools.product(g.COEFFICIENTS,g.COEFFICIENTS,(1,3),(1,3)):
            yield {'angle':'x','a':a,'b':b,'p':p,'q':0,'n':n}

def native_item(label,r):
    f=r['question'][':question/answer-fields'][0];checks=[]
    for a in f[':answer-field/choices']:
        checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio ID; displayed mathematics checked independently'})
    return {'label':label,'record':r,'checks':checks}

def main():
    raw=[];repaired=[];review=[];cases=[];native=[];source_results=[];known_failures=[]
    for sid,src in g.SOURCES.items():
        level=g.SOURCE_LEVELS[sid];p={'angle':r'\theta' if r'\theta' in src[':question/problem'] else ('θ' if 'θ' in src[':question/problem'] else 'x'),'swap':False}
        case={'source_id':sid,'source_uuid':src[':question/id'],'template':'source_'+sid,'parameters':p,'bank_profile':'raw:'+sid,'level':level,'authored_level_assignment':':question/difficulty' not in src};cases.append(case)
        r=g.generate(level,parameters=p,profile='raw:'+sid);raw.append(r);q=r['question'];sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert q[':question/problem']==src[':question/problem']
        assert set(q)==set(src)-{':db/id'}
        for key in (':question/difficulty',':question/worked-solution'):
            assert (key in q)==(key in src)
        if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        check(r,False)
        if sid in g.ERRORS:
            try:check(r)
            except AssertionError as e:known_failures.append({'source_id':sid,'reason':str(e)})
            else:raise AssertionError('Raw source error not detected')
        else:check(r)
        if ':answer-field/correct' in sf:
            original=next(a for a in sf[':answer-field/choices'] if a[':answer/id']==sf[':answer-field/correct'][':answer/id'])
            actual=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert actual[':answer/value']==original[':answer/value'];native.append(native_item('raw:'+sid,r))
        rr=g.generate(level,parameters=p,profile='repaired:'+sid);check(rr);repaired.append(rr);native.append(native_item('repaired:'+sid,rr))
        source_results.append({'source_id':sid,'full_prompt_exact':True,'bank_values_exact':5,'raw_key_presence_parity':True,'raw_solution_exact':':question/worked-solution' in src,'correct_designation_matched':':answer-field/correct' in sf,'raw_mathematical_solution_pass':sid not in g.ERRORS and ':question/worked-solution' in src,
                               'literal_backslash_u2061_count':sum(a[':answer/value'].count(chr(92)+'u2061') for a in sf[':answer-field/choices']),
                               'unicode_function_application_count':sum(a[':answer/value'].count(chr(8289)) for a in sf[':answer-field/choices'])})
        for swap in (False,True):
            v=g.generate(level,seed=int(swap)+17,parameters={'angle':r'\alpha','swap':swap},profile='repaired:'+sid);check(v);review.append(v)
            # Raw public symmetry profile keeps full source sequence, including faults.
            vraw=g.generate(level,parameters={'angle':'t','swap':swap},profile='raw:'+sid);check(vraw,False)
    domain_counts={};fingerprints={};rejected={};examined=0
    for level in ('easy','moderate','hard'):
        good=[];bad=0
        for p in domain(level):
            try:r=g.generate(level,parameters=p)
            except ValueError:bad+=1;continue
            poly=check(r);good.append(r);examined+=1
            # Same exact instance and changed seed must preserve complete content identity.
            changed=g.generate(level,seed=523,parameters=p)
            assert changed['question'][':question/id']==r['question'][':question/id']
            assert changed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
            assert r['generation']['mathematical_fingerprint']==g.digest(str(poly))
        assert len({r['generation']['mathematical_fingerprint'] for r in good})==len(good)
        domain_counts[level]=len(good);fingerprints[level]=[r['generation']['mathematical_fingerprint'] for r in good];rejected[level]=bad
        for seed in range(40):
            r=g.generate(level,seed);check(r)
            assert r['generation']['parameters'] in [dict(p,angle=r['generation']['parameters']['angle']) for p in (x['generation']['parameters'] for x in good)]
            if seed<2:review.append(r)
            if seed<10:native.append(native_item(level+':'+str(seed),r))
        for seed in (2,11):
            r=g.generate(level,seed,field_type='blank');check(r);review.append(r)
            value=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
            submitted=r['question'][':question/problem'].split('$')[1].rstrip('.')
            native.append({'label':level+':blank:'+str(seed),'record':r,'checks':[{'submitted':value,'expected':'accepted','purpose':'Canonical complete simplified expression'},
                          {'submitted':submitted,'expected':'accepted','purpose':'Meaningfully equivalent unreduced expression using the identity'},
                          {'submitted':'123','expected':'rejected','purpose':'Unequal constant'}]})
    # Enforce explicit guards beyond mere random reachability.
    invalid=[('easy',{'angle':'x','a':0,'p':1,'q':0}),('easy',{'angle':'x','a':6,'p':1,'q':0}),('easy',{'angle':'x','a':1,'p':4,'q':0}),
             ('moderate',{'angle':'x','a':5,'b':1,'p':1,'q':0,'family':'opposite'}),('moderate',{'angle':'x','a':1,'b':1,'p':2,'q':0,'family':'opposite'}),
             ('hard',{'angle':'x','a':1,'b':0,'p':1,'q':0,'n':1}),('hard',{'angle':'x','a':1,'b':1,'p':2,'q':0,'n':1}),('hard',{'angle':'x','a':-5,'b':1,'p':1,'q':0,'n':1})]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('Unenforced explicit guard',level,p))
    # Raw, repaired, authored and blank layouts unify by actual polynomial.
    matched_parameters={
        'q-65163':('easy',{'a':1,'p':0,'q':1}),
        'q-65193':('easy',{'a':1,'p':2,'q':1}),
        'q-119362':('easy',{'a':1,'p':0,'q':3}),
        'q-65229':('easy',{'a':1,'p':1,'q':0}),
        'q-65241':('easy',{'a':1,'p':1,'q':1}),
        'q-65242':('easy',{'a':1,'p':3,'q':0}),
        'q-119367':('moderate',{'a':-1,'b':2,'p':0,'q':1,'family':'opposite'}),
        'q-119371':('moderate',{'a':1,'b':1,'p':1,'q':0,'family':'same'}),
        'q-65243':('moderate',{'a':1,'b':1,'p':0,'q':2,'family':'complement'}),
        'q-72711':('moderate',{'a':2,'b':1,'p':0,'q':1,'family':'opposite'})}
    for sid,(level,p) in matched_parameters.items():
        hashes=[]
        for angle in g.ANGLES:
            for kind in ('radio','blank'):
                r=g.generate(level,parameters=dict(p,angle=angle),field_type=kind);check(r)
                hashes.append(r['generation']['mathematical_fingerprint'])
            for mode in ('raw','repaired'):
                r=g.generate(level,parameters={'angle':angle,'swap':False},profile=mode+':'+sid);check(r,mode!='raw' or sid not in g.ERRORS)
                hashes.append(r['generation']['mathematical_fingerprint'])
        assert len(set(hashes))==1
    symmetric=[g.generate('easy',parameters={'angle':'t','swap':swap},profile='raw:q-65241') for swap in (False,True)]
    assert symmetric[0]['generation']['mathematical_fingerprint']==symmetric[1]['generation']['mathematical_fingerprint']
    write('source-cases.json',cases);write('source-replays.json',raw);write('repaired-source-replays.json',repaired);write('review.json',review);write('engine-input.json',native)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    engine=json.loads((ROOT/'engine-report.json').read_text())
    validation={'passed':True,'source_questions':10,'full_source_prompts':10,'full_raw_banks':10,'matched_source_values':50,'matched_source_correct_designations':8,'missing_source_designations':2,
                'exact_raw_solutions':8,'raw_correct_solutions':6,'source_mathematical_errors':known_failures,'repaired_source_solutions':10,'source_results':source_results,
                'full_domain_valid_instances':examined,'finite_mathematical_tasks':domain_counts,'whole_instance_rejections':rejected,'sample_checks':120,'invalid_explicit_guards':len(invalid),
                'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':engine['documented_unresolved_checks'],
                'plots':'none','database_writes':0,'limitations':['Hard has no observed practice labels; its two-GCF workload is authored.','Raw profiles are evidence-only, including missing refs and two incorrect solution blocks.','Source bank intentions are unresolved; symmetry recipes recover the complete expression patterns only.','Angle aliases and layouts do not increase mathematical task counts.']}
    write('validation.json',validation);write('finite-task-fingerprints.json',fingerprints)
    sections=['# Source originals and generated variants\n','Raw originals are evidence only. Generated source variants below use explicitly repaired profiles; defaults and blanks are authored.\n']
    for r in raw:
        sid=r['generation']['source_ids'][0];sections+=['## Original '+sid+'\n',g.markdown(r)+'\n']
        for v in review:
            if v['generation']['template']=='source_'+sid:sections+=['### Generated repaired variant '+str(v['generation']['parameters'])+'\n',g.markdown(v)+'\n']
    for v in review:
        if not v['generation']['template'].startswith('source_'):sections+=['## Generated authored '+v['question'][':question/difficulty']+' '+v['question'][':question/answer-fields'][0][':answer-field/type']+'\n',g.markdown(v)+'\n']
    (ROOT/'review.md').write_text('\n'.join(sections))
    hashes={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),*sorted(ROOT.glob('*'))] if p.is_file() and p.name!='hashes.json'}
    hashes[str((REPO/'generate/runs/current/check-engine').relative_to(REPO))]=hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()
    write('hashes.json',hashes)
    print(json.dumps({k:validation[k] for k in ('passed','full_domain_valid_instances','finite_mathematical_tasks','native_accepted','native_rejected','native_unresolved')}))
if __name__=='__main__':main()
