#!/usr/bin/env python3
"""Independent displayed-math, full source fidelity and native engine checks."""
import collections,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;BASE=D.parent.parent.parent
spec=importlib.util.spec_from_file_location('scalar_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
checks=collections.Counter();engine=[];reviews=[]

def independent_prompt(q):
    p=q[':question/problem'];mm=re.search(r'\|=(.*?)\$ and',p).group(1).strip();M=g.parse_scalar(mm)
    at=re.search(r'(?:\\theta|θ)\s*=\s*(.*?)\$',p).group(1).rstrip('.')
    angle=g.parse_scalar(at.replace('\\pi','pi')) if 'pi' in at else sp.Rational(int(re.search(r'\d+',at).group()),180)*sp.pi
    a,b=re.search(r'vectors \$(\w)\$ and \$(\w)\$',p).groups()
    return M,angle,a,b

def formatting(s):
    assert s.count('$')%2==0
    depth=0
    for i,c in enumerate(s):
        if c=='{' and (i==0 or s[i-1]!='\\'):depth+=1
        if c=='}' and (i==0 or s[i-1]!='\\'):depth-=1;assert depth>=0
    assert depth==0

def verify(r,native=True):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];uuid.UUID(q[':question/id']);M,angle,a,b=independent_prompt(q);correct=sp.simplify(M*sp.cos(angle));kind=q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
    for s in (q[':question/problem'],q.get(':question/worked-solution','')):formatting(s)
    f=q[':question/answer-fields'][0];uuid.UUID(f[':answer-field/id'])
    for ans in f[':answer-field/choices']:
        uuid.UUID(ans[':answer/id']);assert ans[':answer/type']==':answer.type/math'
    assert len({ans[':answer/id'] for ans in f[':answer-field/choices']})==len(f[':answer-field/choices'])
    values=[g.parse_scalar(x[':answer/value']) for x in f[':answer-field/choices']]
    assert len(values)==(1 if kind=='blank' else 5)
    assert all(v.is_real and v.is_finite for v in values)
    assert len(set(values))==len(values)
    assert sum(sp.simplify(v-correct)==0 for v in values)==1
    if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    if ':answer-field/correct' in f:
        ca=next(x for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]);assert sp.simplify(g.parse_scalar(ca[':answer/value'])-correct)==0
    if ':question/worked-solution' in q:
        s=q[':question/worked-solution'];parts=s.split(' & =')[1:];assert len(parts)==4
        assert parts[0].split('  \\\\')[0]==r'|\,'+a+r'\,|\operatorname{cos}⁡\theta'
        substitute=parts[1].split(r' \\')[0];substitute=substitute.replace(r'\operatorname{cos}⁡','cos').replace(r'cos\,','cos')
        mtext,at=substitute.split('cos(',1);at=at[:-1]
        assert sp.simplify(g.parse_scalar(mtext)-M)==0
        row_angle=g.parse_scalar(at.replace('\\pi','pi')) if 'pi' in at else sp.Rational(int(re.search(r'\d+',at).group()),180)*sp.pi
        assert row_angle==angle
        product=parts[2].split(r' \\')[0];mt,ct=product.split(r'\cdot ')
        assert sp.simplify(g.parse_scalar(mt)-M)==0
        assert sp.simplify(g.parse_scalar(ct)-sp.cos(angle))==0
        final=parts[3].split(r'.\end{aligned}')[0];assert sp.simplify(g.parse_scalar(final)-correct)==0
        assert r'{\text{comp}}_{'+b+r'}\,'+a in s
        checks['displayed_four_stages']+=1
    checks['math_records']+=1
    if native and ':answer-field/correct' in f:
        cases=[]
        if kind=='radio':
            for ans in f[':answer-field/choices']:cases.append({'submitted_answer_id':ans[':answer/id'],'expected':'accepted' if ans[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each full-bank choice'})
        else:
            cases=[{'submitted':ca[':answer/value'],'expected':'accepted','purpose':'canonical scalar'},
                {'submitted':'('+str(M)+')*cos('+str(angle)+')','expected':'accepted','purpose':'unreduced magnitude-cosine product'},
                {'submitted':str(correct+1),'expected':'rejected','purpose':'wrong scalar'}]
        engine.append({'label':'instance-'+str(len(engine)),'record':r,'checks':cases})

source_cases=[]
assert (D/'source.json').read_bytes()==(BASE/'generate/runs/current/sources/17592186105916.json').read_bytes()
for profile,o in g.OBSERVED.items():
    q=o['raw_q'];r=g.generate('easy',profile=profile,parameters=o['parameters']);verify(r)
    x=r['question'];assert set(x)==set(q)-{':db/id'}
    for k in (':question/problem',':question/worked-solution'):
        assert x.get(k)==q.get(k);assert (k in x)==(k in q)
    assert x[':question/math-academy-id']==q[':question/math-academy-id']
    assert (':question/difficulty' in x)==(':question/difficulty' in q)
    assert ':question/answer-fields' in x and ':question/answer-fields' in q
    f=q[':question/answer-fields'][0];gf=x[':question/answer-fields'][0]
    assert set(gf)==set(f)-{':db/id'}
    assert all(set(ga)==set(sa)-{':db/id'} for ga,sa in zip(gf[':answer-field/choices'],f[':answer-field/choices']))
    assert gf[':answer-field/key']==f[':answer-field/key']
    assert gf[':answer-field/type']==f[':answer-field/type'][':db/ident']
    assert (':answer-field/correct' in gf)==(':answer-field/correct' in f)
    assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
    checks['source_banks']+=1;checks['source_options']+=len(f[':answer-field/choices'])
    if o['has_correct']:checks['source_correct_designations']+=1
    if o['has_solution']:checks['source_exact_solutions']+=1
    source_cases.append({'source_id':o['source_id'],'template':o['template'],'level':'easy','authored_level_assignment':not o['has_difficulty'],'parameters':o['parameters'],'bank_profile':profile})
    reviews.append({'label':'original replay '+o['source_id'],'record':r})
    # Changed magnitude through public API proves each historical bank is parameterized.
    p=dict(o['parameters']);p['coefficient']=str(1 if sp.Rational(p['coefficient'])!=1 else 2)
    changed=g.generate('easy',template=o['template'],profile=profile,parameters=p);verify(changed);reviews.append({'label':'generated evidence variant '+o['source_id'],'record':changed})

# Exercise all normal shapes and both authored absent levels.
coverage=collections.Counter();mathids={l:set() for l in ('easy','moderate','hard')}
for level in mathids:
    for seed in range(240):
        r=g.generate(level,seed);verify(r);coverage[level+':'+r['generation']['template']]+=1;coverage[level+':'+r['generation']['profile']]+=1;mathids[level].add(r['generation']['mathematical_fingerprint'])
        if seed<2:reviews.append({'label':'authored normal '+level+' '+str(seed),'record':r})
    assert all(coverage[level+':'+t] for t in g.NORMAL_TEMPLATES)
    assert len(mathids[level])>=80

# Review every complete normal radio profile and every prose mask at each level.
for level in mathids:
    for template in g.NORMAL_TEMPLATES:
        profiles=('trig_signed','trig_denominator','right_angle') if template=='radio_operator' and level=='easy' else ('trig_signed','trig_denominator') if template=='radio_operator' else ('blank',)
        for profile in profiles:
            r=g.generate(level,19,template=template,profile=profile);verify(r);reviews.append({'label':'authored normal '+level+' / '+template+' / '+profile,'record':r})

# Identity excludes seed, notation and unit aliases from mathematical-task counts.
for level in mathids:
    r=g.generate(level,44);kw={'template':r['generation']['template'],'profile':r['generation']['profile'],'parameters':r['generation']['parameters']}
    assert g.generate(level,999,**kw)['question'][':question/id']==r['question'][':question/id']
    p=dict(kw['parameters']);p.update(a='c',b='d',unit='radians' if p['unit']=='degrees' else 'degrees');r2=g.generate(level,parameters=p,template=kw['template'],profile=kw['profile']);assert r2['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'];checks['identity_checks']+=1
# Same exact guards for explicit requests and sampling. No floating coefficient or new angle.
for level,p in [('easy',{'coefficient':'3/2','radicand':1,'angle':30}),('moderate',{'coefficient':'2','radicand':1,'angle':30}),('hard',{'coefficient':'3/2','radicand':2,'angle':45}),('easy',{'coefficient':'1.5','radicand':1,'angle':60}),('easy',{'coefficient':'4','radicand':1,'angle':15}),('hard',{'coefficient':'25/2','radicand':2,'angle':30}),('moderate',{'coefficient':'2/3','radicand':1,'angle':30}),('hard',{'coefficient':'1/2','radicand':2,'angle':30}),('easy',{'coefficient':'4','radicand':2.0,'angle':30})]:
    p.update(unit='degrees',a='a',b='b')
    try:g.generate(level,parameters=p,template='blank_operator')
    except ValueError:checks['invalid_rejected']+=1
    else:raise AssertionError('explicit invalid accepted')
p={'coefficient':'4','radicand':1,'angle':45,'unit':'degrees','a':'a','b':'b'}
try:g.generate('easy',template='radio_operator',profile='trig_signed',parameters=p)
except ValueError:checks['ambiguous_complete_bank_rejected']+=1
else:raise AssertionError('ambiguous whole bank accepted')

(D/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
(D/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2)+'\n')
subprocess.run([str(BASE/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
er=json.loads((D/'engine-report.json').read_text())
(D/'review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
(D/'review.md').write_text('# Scalar projection review\n\nAll original banks and changed-magnitude evidence variants are labeled ineligible historical evidence. Normal variants are separately labeled authored.\n\n'+'\n\n---\n\n'.join('## '+x['label']+'\n\n'+g.markdown(x['record']) for x in reviews)+'\n')
counts={}
for level in mathids:
    tasks=set()
    for den in ((1,) if level=='easy' else (2,3,4)):
        for num in range(1 if level=='easy' else 3,25):
            c=sp.Rational(num,den)
            if c.q!=den:continue
            for d in (1,2,3):
                for a in g.ANGLES:
                    p={'coefficient':str(c),'radicand':d,'angle':a,'unit':'degrees','a':'a','b':'b'}
                    try:g.guard(level,p)
                    except ValueError:continue
                    tasks.add((str(c*sp.sqrt(d)) if a!=90 else 'incidental_at_right_angle',a))
    counts[level]=len(tasks)
result={'status':'pass','generator_version':g.VERSION,'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'checks':dict(checks),'source_fidelity':{'questions':17,'complete_banks':17,'options':57,'correct_designations':'16/16 present; one absent, never claimed matched','worked_solutions':'16/16 exact; one absent','question_optional_presence':'17/17'},'default_coverage':dict(coverage),'sampled_mathematical_tasks':{k:len(v) for k,v in mathids.items()},'enumerated_mathematical_tasks':counts,'native':{'accepted':er['accepted_checks'],'rejected':er['rejected_checks'],'unresolved':er['documented_unresolved_checks'],'source_missing_correct_omitted':1,'engine_sha256':hashlib.sha256((BASE/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'limits':['All 10 historical radio profiles are evidence-only; homogeneous scalar patterns do not establish original error intent.','One original has no correct ref, worked solution or difficulty; mathematically inferred correct scalar is kept in metadata only.','Moderate and hard are authored absent-level bookkeeping extensions; their difficulty labels are design claims.'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}
(D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
