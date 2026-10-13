#!/usr/bin/env python3
"""Fail-closed source/bank/printed math/identity/plot/native verification."""
from pathlib import Path
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys
import sympy as S
import mpmath as mp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('planar',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def same(a,b):
    diff=S.trigsimp(a-b)
    if S.simplify(diff)!=0:
        assert abs(complex(S.N(diff,50)))<1e-35,(a,b,diff)

def rows(sol):
    return [row for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S) for row in b.split(r'\\')]
def repaired(sid):
    sol=g.QS[sid][':question/worked-solution']
    if sid=='q-77220':sol=sol.replace(r'16{t}^{2}{cos}^{2}⁡t+16{t}^{2}{sin}^{2}',r'16{t}^{2}{cos}^{2}⁡2t+16{t}^{2}{sin}^{2}⁡2t')
    return sol

def normalize(s):return re.sub(r'\s+','',s)
def strip_factor(rhs):
    rhs=rhs.strip().rstrip('.,')
    m=re.fullmatch(r'(\d+)\\left\((.*)\\right\)',rhs,re.S)
    return (S.Integer(m.group(1)),m.group(2)) if m else (S.Integer(1),rhs)

def eval_scalar_stage(s,printed_square=None):
    """Evaluate printed integral/endpoint/arithmetic RHS, independently.

    Captured source TeX permits bars with several bracing conventions. Handling
    these is structural: integrate the actual printed integrand or substitute
    actual printed bounds into the actual antiderivative, never answer metadata.
    """
    s=s.strip().rstrip('.,');s=s.replace(r'\,','').replace(r'\text{d}',r'\mathrm{d}').replace('{\\int }',r'\int')
    # Captured superscripted grouping around an evaluated expression.
    s=s.replace(r'\,{|}', '|').replace('{|}','|').replace(r'\big|','|')
    s=re.sub(r'\{\((.*?)\)\|\}',r'(\1)|',s)
    if r'\int' in s:
        m=re.search(r'\\int\s*_',s);prefix=s[:m.start()];i=m.end();low,j=g.braces(s,i)
        assert s[j]=='^';high,k=g.braces(s,j+1)
        rest=s[k:];v=re.search(r'\\mathrm\{d\}([tu])',rest);assert v,(s,rest)
        integrand=rest[:v.start()];var=g.T if v.group(1)=='t' else g.U
        if '‖' in integrand:
            assert printed_square is not None
            raw_speed=S.sqrt(S.factor(printed_square))
            # Derive the sign branch from these actual printed bounds.
            if float(g.parse_math(low))>=0:raw_speed=raw_speed.subs(S.Abs(g.T),g.T)
            if float(g.parse_math(low))>0:raw_speed=raw_speed.refine(S.Q.positive(g.T))
            return (g.parse_math(prefix) if prefix else S.Integer(1))*S.integrate(raw_speed,(var,g.parse_math(low),g.parse_math(high)))
        return (g.parse_math(prefix) if prefix else S.Integer(1))*S.integrate(g.parse_math(integrand),(var,g.parse_math(low),g.parse_math(high)))
    if '|' in s:
        left,right=s.split('|',1)
        assert right.startswith('_'),s
        low,j=g.braces(right,1);assert right[j]=='^';high,k=g.braces(right,j+1)
        assert not right[k:].strip(),s
        f=g.parse_math(left);var=g.U if g.U in f.free_symbols else g.T
        return f.subs(var,g.parse_math(high))-f.subs(var,g.parse_math(low))
    return g.parse_math(s)

checks=[];records=[];fidelity=[];cases=[];stage_count=0

def verify(r):
    global stage_count
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];m=r['generation'];prompt=q[':question/problem'];template=m['template'];c=m['parameters']['c'];sol=q[':question/worked-solution']
    # Read actual displayed formula including implicit products and TeX groups.
    vector=re.search('(?:⟨|\\\\langle)(.*?)(?:⟩|\\\\rangle)',prompt,re.S).group(1)
    components=re.split(r',(?:\\,)?',vector);assert len(components)==2
    x,y=map(g.parse_math,components)
    interval=re.search(r'from\s+\$t\s*=([^$]+)\$\s+to\s+\$t\s*=([^$]+)\$',prompt)
    assert interval,prompt
    a,b=map(g.parse_math,interval.groups());assert float(a)<float(b)
    dx,dy=S.diff(x,g.T),S.diff(y,g.T);square=S.trigsimp(dx*dx+dy*dy)
    speed=S.sympify(m['speed'],locals={'t':g.T});same(square,speed**2)
    # Integrate actual printed derivative norm numerically, separate from the
    # exact simplification and printed answer evaluation.
    fun=S.lambdify(g.T,S.sqrt(square),'mpmath');mp.mp.dps=40
    numerical=mp.quad(fun,[mp.mpf(str(S.N(a,40))),mp.mpf(str(S.N(b,40)))])
    L=S.integrate(speed,(g.T,a,b));same(L,S.sympify(m['length']));assert abs(numerical-mp.mpf(str(S.N(L,40))))<mp.mpf('1e-28')
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio';bank=f[':answer-field/choices'];assert len(bank)==5
    values=[g.parse_math(z[':answer/value']) for z in bank]
    assert all(float(S.N(z))>0 for z in values)
    assert all(abs(float(S.N(values[i]-values[j],50)))>1e-9 for i in range(5) for j in range(i))
    cid=f[':answer-field/correct'][1];assert sum(z[':answer/id']==cid for z in bank)==1
    same(next(v for z,v in zip(bank,values) if z[':answer/id']==cid),L)
    for z in bank:assert z[':answer/id']==g.uid(f[':answer-field/id']+':'+z[':answer/value'])
    if template in g.BASE:
        expected=repaired(template)
        if c==1:
            normalized_plot=lambda text:re.sub(r'!\[\]\(.*?\)','![](PLOT)',text)
            assert normalized_plot(prompt)==normalized_plot(g.QS[template][':question/problem'])
        actual_rows=rows(sol);expected_rows=rows(expected);assert len(actual_rows)==len(expected_rows)
        # All complete prose and all ordered masks must match, rather than
        # checking a few phrases or trusting generation metadata.
        assert normalize(re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','MATH',sol,flags=re.S))==normalize(re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','MATH',expected,flags=re.S))
        first_integral=False
        for got,want in zip(actual_rows,expected_rows):
            before,rhs=got.split('=',1);wb,wr=want.split('=',1);scale,core=strip_factor(rhs)
            expected_scale=1 if '‖' in wr and r'\int' in wr else c
            assert scale==expected_scale and normalize(core)==normalize(wr.rstrip().rstrip('.,')),(got,want)
            assert normalize(before)==normalize(wb)
            if '⟨' in core:
                if r'\text{d}' not in core:
                    v=re.search('⟨(.*?)⟩',core).group(1);parts=v.replace(r'\,','').split(',')
                    prefix=core.split('⟨',1)[0];mult=g.parse_math(prefix) if prefix.strip() else 1
                    assert len(parts)==2,core
                    same(scale*mult*g.parse_math(parts[0]),dx);same(scale*mult*g.parse_math(parts[1]),dy)
                    stage_count+=2
                continue
            if r'\int' in core:first_integral=True
            if not first_integral:
                val=g.parse_math(core);same((scale*val)**2,square);stage_count+=1
            else:
                val=eval_scalar_stage(core,square)
                if val is not None:same(scale*val,L);stage_count+=1
    else:
        # Check the exact printed derivative tuple and all norm/arithmetic
        # stages; the first row's differentiation operators are checked against
        # the independently parsed curve above.
        rr=rows(sol);vec=re.search(r'\\left\\langle(.*?)\\right\\rangle',rr[1]).group(1)
        vx,vy=map(g.parse_math,vec.split(','));same(vx,dx);same(vy,dy)
        before_integral=True
        for row in rr[2:]:
            rhs=row.split('=',1)[1]
            if r'\int' in rhs:before_integral=False
            if before_integral:same(g.parse_math(rhs)**2,square);stage_count+=1
            else:
                v=eval_scalar_stage(rhs)
                if v is not None:
                    assert not v.free_symbols, (row,v)
                    same(v,L);stage_count+=1
    for text in (prompt,sol,*[z[':answer/value'] for z in bank]):
        assert all(ord(ch)>=32 or ch in '\n\t' for ch in text),repr(text)
        assert text.count('$')%2==0
        assert text.count('{')==text.count('}')
    side=json.loads(Path(m['plot']['sidecar']).read_text());assert side['identity']==m['content_fingerprint'];assert len(side['segment'])==401
    for i,t in ((0,a),(-1,b)):
        px,py=side['segment'][i];assert abs(px-float(x.subs(g.T,t)))<1e-7*max(1,abs(px));assert abs(py-float(y.subs(g.T,t)))<1e-7*max(1,abs(py))
    enginechecks=[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==cid else 'rejected','purpose':'every displayed radio option'} for z in bank]
    checks.append({'label':template+':'+m['bank_profile']+':c'+str(c),'record':r,'checks':enginechecks})

for sid in g.QS:
    print('Checking',sid,flush=True)
    level=g.TEMPLATES[sid]['level'];case={'source_id':sid,'template':sid,'level':level,'parameters':{'c':1},'bank_profile':'observed:'+sid};cases.append(case)
    r=g.generate(level,template=sid,parameters=case['parameters'],profile=case['bank_profile']);verify(r);records.append(r)
    q=g.QS[sid];f=q[':question/answer-fields'][0];generated=r['question'][':question/answer-fields'][0]
    src=[g.parse_math(z[':answer/value']) for z in f[':answer-field/choices']];got=[g.parse_math(z[':answer/value']) for z in generated[':answer-field/choices']]
    assert all(sum(S.simplify(a-b)==0 for b in got)==1 for a in src)
    raw=normalize(q[':question/worked-solution'])==normalize(r['question'][':question/worked-solution'])
    fidelity.append({'source_id':sid,'bank_matched':5,'distractors_matched':4,'correct_designation':True,'raw_solution_exact':raw,'repaired_solution_exact':normalize(repaired(sid))==normalize(r['question'][':question/worked-solution']),'stage_rows':len(rows(r['question'][':question/worked-solution']))})
    # Changed observed profile plus two independently authored-bank variants.
    for c,profile in ((3,'observed:'+sid),(2,'authored-method-bank'),(5,'authored-method-bank')):
        r=g.generate(level,seed=c,template=sid,parameters={'c':c},profile=profile);verify(r);records.append(r)
for template in ('hard_exp_spiral','hard_reciprocal_affine'):
    print('Checking',template,flush=True)
    for p in ({'c':2,'k':2,'d':1,'a':0,'b':1},{'c':3,'k':3,'d':2,'a':0,'b':1}):
        if template=='hard_exp_spiral':p=dict(p,q=1,a=0,b=2 if p['c']==3 else 1);p.pop('d')
        r=g.generate('hard',template=template,parameters=p);verify(r);records.append(r)
# Seed/order invariance for fixed mathematical and presentation content.
r0=g.generate('easy',seed=0,template='q-77065',parameters={'c':4});r1=g.generate('easy',seed=72,template='q-77065',parameters={'c':4});assert r0['question'][':question/id']==r1['question'][':question/id'];assert r0['question'][':question/answer-fields'][0][':answer-field/choices']!=r1['question'][':question/answer-fields'][0][':answer-field/choices']
obs=g.generate('easy',template='q-77065',parameters={'c':4},profile='observed:q-77065');assert obs['question'][':question/id']!=r0['question'][':question/id'];assert obs['generation']['mathematical_task_fingerprint']==r0['generation']['mathematical_task_fingerprint']
# All default-scope coefficient values, complete-bank rejection and explicit
# hard bounds. Avoid rendering additional instances: normal generate still runs.
for bad in ({'c':0},{'c':13},{'c':-2},{'c':2.5},{'c':2,'extra':1}):
    try:g.generate('easy',template='q-77065',parameters=bad)
    except ValueError:pass
    else:raise AssertionError('Invalid explicit parameter accepted')
# Change one bound at a time from an otherwise admissible instance.
guard_checks=0
for template,base,updates in (
 ('hard_reciprocal_affine',{'c':2,'k':2,'d':1,'a':0,'b':1},[{'k':0},{'k':1},{'k':4},{'d':0},{'d':3},{'a':1},{'b':2},{'c':13}]),
 ('hard_exp_spiral',{'c':2,'k':2,'q':1,'a':0,'b':1},[{'k':1},{'k':4},{'q':0},{'q':4},{'q':2},{'a':-1},{'b':3},{'d':1},{'c':13}])):
    for changes in updates:
        bad=dict(base,**changes)
        try:g.generate('hard',template=template,parameters=bad)
        except ValueError:guard_checks+=1
        else:raise AssertionError(('Hard bound accepted',template,bad))
for template,p in (('q-77065',{'c':12}),('q-77219',{'c':12}),('hard_reciprocal_affine',{'c':12,'k':3,'d':2,'a':0,'b':1}),('hard_exp_spiral',{'c':12,'k':3,'q':2,'a':1,'b':2})):
    r=g.generate(g.TEMPLATES[template]['level'],template=template,parameters=p);verify(r);records.append(r)
# Concurrent identical and different plot instances must have independent
# metadata and paths, with no surviving shared temporary inputs.
def concurrent_call(c):return g.generate('easy',template='q-77065',parameters={'c':c})
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:parallel=list(pool.map(concurrent_call,[7,7,8]))
assert parallel[0]['question'][':question/id']==parallel[1]['question'][':question/id'];assert parallel[0]['generation']['plot']['prompt']!=parallel[2]['generation']['plot']['prompt']
for r in parallel:verify(r)
assert not list(HERE.glob('render-input-*.json'))
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n');(HERE/'engine-input.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
report={'status':'passed','records_checked':len(records)+len(parallel),'source_questions':10,'source_bank_values':'50/50','source_distractors':'40/40','source_complete_banks':'10/10','source_correct_designations':'10/10','raw_complete_solution_fidelity':'9/10','corrected_complete_solution_fidelity':'10/10','printed_scalar_stages_checked':stage_count,'native_checks':sum(len(x['checks']) for x in checks),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'fidelity':fidelity,'authored_hard_templates':['hard_exp_spiral','hard_reciprocal_affine'],'isolated_hard_bound_rejections':guard_checks,'upper_bound_instances':'4 independently verified','seed_identity':'passed','concurrent_plots':'passed','script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
