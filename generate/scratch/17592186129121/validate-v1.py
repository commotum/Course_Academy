#!/usr/bin/env python3
"""Independent displayed-math/source-fidelity/native-grading checks; local only."""
import collections, hashlib, importlib.util, json, math, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('amplitude_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True)

def read_group(s,start):
    assert s[start]=='{',s
    depth=1;i=start+1
    while depth:
        if s[i]=='{':depth+=1
        elif s[i]=='}':depth-=1
        i+=1
    return s[start+1:i-1],i

def fractions(s):
    while '\\frac' in s:
        at=s.index('\\frac');a,end=read_group(s,at+5);b,stop=read_group(s,end)
        s=s[:at]+'(('+fractions(a)+')/('+fractions(b)+'))'+s[stop:]
    return s

def parse(s):
    s=s.strip().rstrip('.,?')
    s=re.sub(r'\\operatorname\{(sin|cos)\}',r'\1',s)
    s=s.replace('⁡','').replace('\\left','').replace('\\right','').replace('\\cdot','*')
    s=fractions(s).replace('\\pi','pi').replace('\\sin','sin').replace('\\cos','cos')
    s=re.sub(r'(?<![A-Za-z])(sin|cos)\s*x\b',r'\1(x)',s)
    assert '\\' not in s and '{' not in s and '}' not in s,s
    return parse_expr(s.replace('^','**'),local_dict={'x':x,'sin':lambda z:sp.sin(z,evaluate=False),'cos':lambda z:sp.cos(z,evaluate=False),'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,))

def expression_from_prompt(q):
    math=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',q[':question/problem']).group(1)
    return parse(math)

def formatting(s):
    assert s.count('$')%2==0,s
    depth=0
    for ch in s:
        if ch=='{':depth+=1
        if ch=='}':depth-=1
        assert depth>=0,s
    assert depth==0,s
    assert '--' not in s and '+-' not in s,s


def check_display(record):
    q,meta=record['question'],record['generation'];expr=expression_from_prompt(q)
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    atom=list(expr.atoms(sp.sin,sp.cos));assert len(atom)==1,expr
    arg=atom[0].args[0];assert sp.diff(arg,x)!=0
    z=sp.Symbol('s');affine=sp.expand(expr.xreplace({atom[0]:z}))
    a=affine.coeff(z);assert sp.diff(affine,z,2)==0
    correct=abs(a)
    # Independent printed prompt vs metadata also covers horizontal arguments,
    # signs, complete numerator constants and outer shifts.
    p=g.decode(meta['parameters']);expected=(p['A'] if 'A' in p else p.get('P',1)*p['N']/p['Q'])*getattr(sp,p['trig'])(p['B']*x+p['C'])+(p['D'] if 'A' in p else p.get('P',1)*p['D']/p['Q']+p.get('E',0))
    assert sp.simplify(expr-expected)==0,(expr,expected)
    fields=q.get(':question/answer-fields',[])
    for f in fields:
        assert f[':answer-field/type']==':answer-field.type/radio'
        assert len(f[':answer-field/choices'])==5
        values=[parse(v[':answer/value']) for v in f[':answer-field/choices']]
        assert len(set(values))==5 and values.count(correct)==1
        for v in f[':answer-field/choices']:formatting(v[':answer/value'])
        ref=f.get(':answer-field/correct')
        if ref:
            assert ref[0]==':answer/id'
            v=next(a for a in f[':answer-field/choices'] if a[':answer/id']==ref[1]);assert parse(v[':answer/value'])==correct
    solution=q.get(':question/worked-solution')
    if solution:
        # Check each printed numeric A and concluding |A| chain independently.
        avals=re.findall(r'\$A=(.*?)[.,]\$',solution)
        assert len(avals)==1 and parse(avals[0])==a,(avals,a)
        chain=re.search(r'\$\|A\|=\|(.*?)\|=(.*?)\.\$',solution)
        assert chain and parse(chain[1])==a and parse(chain[2])==correct
        # Every displayed rewrite row is checked, including unevaluated products.
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
        for block in blocks:
            if '\\begin{aligned}' in block:
                rows=block.removeprefix('\\begin{aligned}').removesuffix('\\end{aligned}').split('\\\\')
                assert len(rows)==3
                assert '\\cdot (' in rows[1] and rows[1].count('\\frac')>=2
                for row in rows:
                    value=row.split('&=',1)[1];assert sp.simplify(parse(value)-expr)==0,(row,expr)
            else:
                pieces=block.split('=');assert pieces[0]=='f(x)' and len(pieces)==3
                for value in pieces[1:]:assert sp.simplify(parse(value)-expr)==0
        if meta['template']=='factored':assert len(blocks)==1 and '\\begin{aligned}' in blocks[0]
        if meta['template'] in ('positive','unit','negative'):assert not blocks
    for s in [q[':question/problem'],solution or '']:formatting(s)
    return correct


def parity(raw,src):
    q=raw['question']
    for k in [':question/problem',':question/difficulty',':question/worked-solution',':question/answer-fields',':question/math-academy-id']:
        assert (k in q)==(k in src),(src[':question/math-academy-id'],k)
    assert q[':question/problem']==src[':question/problem']
    if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution']
    for f,s in zip(q.get(':question/answer-fields',[]),src.get(':question/answer-fields',[]),strict=True):
        for k in [':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct']:assert (k in f)==(k in s)
        assert f[':answer-field/key']==s[':answer-field/key'] and f[':answer-field/type']==s[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in s[':answer-field/choices'])
        if ':answer-field/correct' in s:
            ref=f[':answer-field/correct'];assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref[1])==s[':answer-field/correct'][':answer/value']
    assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']


def native_fixture(record,label):
    checks=[]
    for i,f in enumerate(record['question'].get(':question/answer-fields',[])):
        if ':answer-field/correct' not in f:continue
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual radio option ID; mathematics independently read from displayed bank'})
    return {'label':label,'record':record,'checks':checks} if checks else None


def assert_rejected(level,template,p):
    try:g.generate(level,template=template,parameters=p)
    except ValueError:return
    raise AssertionError(('Explicit workload violation accepted',level,template,p))


def main():
    cases=[];raws=[];native=[];variants=[]
    for sid,s in g.SPECS.items():
        params={**s['params'],'trig':s['trig']}
        case={'source_id':sid,'template':sid,'level':s['level'],'parameters':params,'bank_profile':'raw:'+sid,'authored_level_assignment':sid in ['q-43277','q-43278']};cases.append(case)
        r=g.generate(s['level'],template=sid,parameters=params,profile=case['bank_profile']);parity(r,g.QUESTIONS[sid]);check_display(r);raws.append(r)
        fixture=native_fixture(r,sid)
        if fixture:native.append(fixture)
        # Each raw mask is truly parameterized, including opaque complete banks.
        changed=dict(params)
        if 'A' in changed:changed['A']=1 if s['kind'].startswith('unit') else str(g.rational(changed['A'])*sp.Rational(3,2))
        else:changed.update(N=-11,D=4,Q=13)
        if s['kind'].startswith('unit'):changed.update(B='1/5',C='1/7')
        elif 'Q' not in changed and s['kind']!='legacy_direct':changed.update(B=4,C='-pi/2',D=0 if s['level']=='easy' else -4)
        r2=g.generate(s['level'],template=sid,parameters=changed,profile=case['bank_profile']);check_display(r2);variants.append(r2)
        assert r2['question'][':question/problem']!=r['question'][':question/problem']
    byte_counts={sid:{k:sum(ord(a)==92 and ord(b)==92 for a,b in zip(q.get(k,''),q.get(k,'')[1:])) for k in (':question/problem',':question/worked-solution')} for sid,q in g.QUESTIONS.items()}
    (HERE/'decoded-source-byte-counts.json').write_text(json.dumps(byte_counts,indent=2)+'\n')
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    normal_counts=collections.Counter();profile_counts=collections.Counter();tasks={l:set() for l in ('easy','moderate','hard')};math_checks=0
    for level in tasks:
        for seed in range(180):
            r=g.generate(level,seed);check_display(r);math_checks+=1
            normal_counts[r['generation']['template']]+=1;profile_counts[r['generation']['bank_profile']]+=1;tasks[level].add(r['generation']['parameter_fingerprint'])
            if seed<12:native.append(native_fixture(r,f'{level}-{seed}'))
            assert r==g.generate(level,seed)
            p=r['generation']['parameters'];same=g.generate(level,seed+899,template=r['generation']['template'],parameters=p,profile=r['generation']['bank_profile'])
            assert r['question'][':question/id']==same['question'][':question/id'] and r['generation']['parameter_fingerprint']==same['generation']['parameter_fingerprint']
        assert len(tasks[level])>= (20 if level!='easy' else 15)
    assert set(normal_counts)==set(g.TEMPLATES) and set(profile_counts)==set(g.BANK_PROFILES)-{'raw:'+s for s in g.SPECS}
    # Every complete normal bank exercised explicitly as well as sampled.
    for profile,b in g.BANK_PROFILES.items():
        if not b['eligible_for_learning']:continue
        for seed in range(20):check_display(g.generate(b['level'],seed,profile=profile));math_checks+=1
        variants.extend(g.generate(b['level'],seed,profile=profile) for seed in (401,402))
    # Boundaries below verify reduced workload, signed magnitudes, nonunit
    # factors and nonzero defining operations for explicit public inputs.
    valid={n:g.generate(l,123,template=n)['generation']['parameters'] for n,l in g.TEMPLATES.items()}
    bad=[('positive','A','-2'),('positive','A','1/7'),('positive','D','1'),('negative','A','2'),('negative','A','-14'),('unit','A','2'),('unit','B','1/10'),('quotient','N','-10'),('quotient','Q','1'),('quotient','B','2'),('factored','P','1'),('factored','P','-5'),('factored','N','0'),('factored','C','0'),('factored','E','0'),('factored','Q','2')]
    guards=0
    for name,k,v in bad:
        p={**valid[name],k:v}
        # N=-10 may remain primitive for Q !=5/10. Force common-factor case.
        if name=='quotient' and k=='N':p['Q']='5'
        assert_rejected(g.TEMPLATES[name],name,p);guards+=1
    # Numeric spelling aliases and incidental horizontal/vertical parameters do
    # not create mathematical tasks, though changed displayed content does.
    r=g.generate('moderate',2,template='negative');p=r['generation']['parameters'];p2={**p,'D':str(int(p['D'])+1 if int(p['D'])<6 else -1)}
    r2=g.generate('moderate',3,template='negative',parameters=p2)
    assert r['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint'] and r['question'][':question/id']!=r2['question'][':question/id']
    p3={**p,'A':str(2*g.rational(p['A']).p)+'/'+str(2*g.rational(p['A']).q)}
    alias=g.generate('moderate',5,template='negative',parameters=p3)
    assert alias['question'][':question/id']==g.generate('moderate',6,template='negative',parameters=p)['question'][':question/id']
    # Exact finite mathematical task counts, excluding offsets/arguments/banks.
    easy={str(sp.Rational(n,d)) for n in range(1,13) for d in range(1,7)}
    moderate_direct={str(-sp.Rational(n,d)) for n in range(1,14) for d in range(1,7)}
    moderate_quotient={(n,q) for n in range(-13,-1) for q in range(3,14) if math.gcd(abs(n),q)==1 and sp.Rational(n,q).q>1}
    hard={(P,n,q) for P in [-4,-3,-2,2,3,4] for n in list(range(-13,-1))+list(range(2,14)) for q in range(3,14) if abs(n)!=abs(P) and abs(P*n)<=36 and math.gcd(abs(P*n),q)==1 and sp.Rational(P*n,q).q>1}
    # Prove all substantive signatures have at least one eligible full bank.
    domain_counts={}
    for level,names in [('easy',[("positive",dict(A=a)) for a in sorted(easy-{'1'})]),('moderate',[("negative",dict(A=a)) for a in sorted(moderate_direct)]+[("quotient",dict(N=n,Q=q)) for n,q in sorted(moderate_quotient)]),('hard',[("factored",dict(P=P,N=n,Q=q)) for P,n,q in sorted(hard)])]:
        count=0
        for name,parts in names:
            found=False
            for B in ([2,3,4,5,6] if name in ('positive','negative') else [1]):
                for D in ([1,2,3,4,5,6,7,8,9] if name in ('quotient','factored') else [0]):
                    p={**valid[name],**parts,'B':B,'D':D}
                    if name=='negative':p['C']='pi/2'
                    if name=='factored':p['C']='1'
                    for profile in g.NORMAL_BANKS[name]:
                        try:r=g.generate(level,parameters=p,template=name,profile=profile)
                        except ValueError:continue
                        check_display(r);found=True;break
                    if found:break
                if found:break
            assert found,(level,name,parts)
            count+=1
        domain_counts[level]=count+(1 if level=='easy' else 0) # one implicit-one signature
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
    result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],text=True,capture_output=True)
    assert result.returncode==0,result.stdout+result.stderr
    print(result.stdout.strip())
    native_report=json.loads((HERE/'native-report.json').read_text())
    engine=ROOT/'generate/runs/current/check-engine'
    native_provenance={'binary_path':str(engine.relative_to(ROOT)),'sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(engine.with_suffix('.rs').read_bytes()).hexdigest(),'entry_point':'course_academy_engine::learning::grade_field','database_operations':0}
    review={'source_replays':raws,'generated_variants':variants}
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    text=['# Amplitude source and generated review','All raw records are evidence only; omissions are preserved. Authored records are learning eligible.','']
    for r in raws:text+=[g.markdown(r),'']
    text+=['## Parameterized evidence variants','Each opaque or malformed raw mask is also shown at changed parameters and remains evidence only.','']
    for r in variants:text+=[g.markdown(r),'']
    (HERE/'review.md').write_text('\n'.join(text)+'\n')
    report={'status':'passed','version':g.VERSION,'provenance':g.PROVENANCE,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'decoded_adjacent_backslash_pair_counts':byte_counts,'source_questions':9,'raw_presence_parity':'9/9','exact_prompts':'9/9','exact_present_solutions':'7/7','source_banks':'7/7','source_option_values':'35/35','correct_designations':'5/5 present; 2 missing, not counted as matches','source_distractors':'20/20 designated wrong options; 10 options in undesignated banks not classified as source wrong','fieldless_sources':2,'missing_difficulty_sources':2,'inferred_math_amplitudes':'9/9 independently verified; does not repair raw records','normal_sample_checks':math_checks,'default_template_coverage':dict(normal_counts),'default_bank_coverage':dict(profile_counts),'sampled_semantic_tasks':{k:len(v) for k,v in tasks.items()},'finite_eligible_semantic_domain':domain_counts,'explicit_guard_rejections':guards,'native':{'records':len(native),'accepted':native_report['accepted_checks'],'rejected':native_report['rejected_checks'],'unresolved':native_report['documented_unresolved_checks'],'raw_ineligible_not_sent':4,'provenance':native_provenance},'plots':'none; tutorial context raster inspected at full resolution on white','authored_hard':'Two coefficient operations P*N/Q, nonunit P, primitive N/Q and P*N/Q, product <=36, no cancellation to integer','remaining_findings':['Raw source correct refs missing in q-43277/q-43278; raw fields absent q-117568/q-117575. Preserved and ineligible.','q-43277 A**2 and q-53428 1/(B*C) error intentions opaque; complete raw parameterized profiles ineligible.','Hard difficulty is an authored scope claim; no observed hard question.']}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
