"""Fail-closed local readback, fidelity, structure, identity and native checks."""
from pathlib import Path
import importlib.util,json,re,subprocess,sys,hashlib,itertools
import sympy as s
D=Path(__file__).resolve().parent
R=D.parents[2]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('slope_generator',D.with_suffix('.py'));p=module('slope_readback',D/'readback.py')
C={'source_prompts_exact':0,'source_solutions_exact':0,'source_solution_absence_exact':0,'source_banks_exact':0,'source_values_exact':0,'source_designations_exact':0,'source_designation_absence_exact':0,'source_key_presence':0,'records_checked':0,'displayed_choices':0,'displayed_solution_stages':0,'scope_invalid_rejections':0,'mutation_rejections':0}
def equal(a,b):
    d=s.expand(a-b)
    return d==0 or s.cancel(d)==0 or s.simplify(d)==0
def mathspans(text):return re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',text,re.S)
def pair(text):
    xs=text.split(',');assert len(xs)==2;return tuple(p.scalar(v.strip()) for v in xs)
def displayed(record):
    q=record['question'];prompt=q[':question/problem'];spans=mathspans(prompt);planes=[];points=[];derivatives=[]
    for span in spans:
        span=span.rstrip('.')
        if re.match(r'^[xy]\s*=',span):planes.append((span.strip()[0],p.scalar(span.split('=',1)[1])))
        if re.match(r'^P\(',span):points.append(tuple(p.scalar(v) for v in span[2:-1].split(',')))
        if re.match(r'^(?:\{f\}|f)_',span):
            lhs,rhs=span.split('=',1);var=re.search(r'_\{?([xy])',lhs)[1];derivatives.append((var,p.scalar(rhs)))
    assert len(planes)==len(derivatives)==1,(planes,derivatives,prompt)
    hold,H=planes[0];var,F=derivatives[0];assert var!=hold
    if points:
        assert len(points)==1 and len(points[0])==3;X,Y,Z=points[0]
    else:
        m=re.search(r'with \$([xy])\$-coordinate \$(.*?)\$',prompt);assert m;mvar,V=m[1],p.scalar(m[2]);assert mvar==var
        X,Y=(V,H) if var=='x' else (H,V)
    assert equal(H,Y if hold=='y' else X)
    answer=s.expand(F.subs({p.x:X,p.y:Y},simultaneous=True));assert answer.is_real and not answer.has(s.nan,s.zoo,s.oo)
    return F,var,hold,X,Y,answer

def independent_bank(t,F,X,Y,prompt):
    xx,yy=p.x,p.y;A=s.expand(F).coeff(xx,2).coeff(yy) if t in ('polynomial','monomial') else s.expand(F).coeff(xx) if t=='linear' else s.expand(F).coeff(xx)*yy if t.startswith('canonical_') else None
    B=-s.expand(F).coeff(xx).coeff(yy,2) if t=='polynomial' else s.expand(F).coeff(s.cos(s.pi*yy)) if t=='canonical_trig' else None
    if t=='linear':wrong=[A*X+Y,A*X,-Y,A*Y-X]
    elif t=='cos_sum':wrong=[Y*s.sin(X)+s.cos(Y),-s.cos(Y),Y,Y*s.sin(X)-s.cos(Y)]
    elif t=='sin_product':wrong=[-s.sin(X)+X*Y,s.sin(X),X*Y,s.sin(X)+X]
    elif t=='rational_radical':
        u=(X*X+1)/(X*X*Y*Y);v=Y*s.sqrt(X);wrong=[(X*X+1)/(X*X*Y)+v,u,v,u-v]
    elif t=='cos_shift':wrong=[s.sqrt(2)*X*s.cos(X*Y),X*s.cos(X*Y+s.pi/4),s.sqrt(2)*X,-s.sqrt(2)*X*s.cos(X*Y+s.pi/4)]
    elif t=='polynomial':wrong=[A*X*X*Y+B*X*Y*Y,A*X*X*Y,-B*X*Y*Y,A*Y*Y*X-B*Y*X*X]
    elif t=='monomial':wrong=[A*X*Y,A*Y*Y*X,A*X*X,A*(X*X+Y)]
    elif t=='log_exp':wrong=[Y*s.log(X)-s.exp(Y),2*Y*s.log(X),-s.exp(Y)/X,2*Y*s.log(X)+s.exp(Y)/X]
    elif t=='exp_cos':wrong=[Y,(X+Y)*s.exp(-s.cos(X*Y)),X+s.exp(s.cos(X*Y))*Y,(X+Y)*s.cos(X*Y)]
    elif t=='radical_ratio':u=s.sqrt(X*X-2*Y*Y);wrong=[u/(X-Y),u/Y,-u/Y,s.sqrt(X*X-Y*Y)/(Y-X)]
    elif t=='base_exp':
        A=s.Integer(re.search(r'\{(\d+)\}\^\{x\+y\}',prompt)[1]);u=A**(X+Y)*Y*(X*s.log(A)+1);wrong=[A**X*Y*(X*s.log(A)+1),-u,A**(X+Y)*Y*X*s.log(A),A**(X+Y)*(X*s.log(A)+Y+1)]
    else:
        u=A*X/Y;v=-A*X*X*Y;w=B*s.cos(s.pi*Y) if t=='canonical_trig' else 0;wrong=[u-v+w,v+w,u+w,A*X+v+w]
    return wrong,A,B

def formatting(text):
    assert '@@SLOT' not in text and '--' not in text and '+-' not in text
    # Inline/display math counts and every nonliteral TeX group must balance.
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    dep=0
    for c in text:
        dep+=(c=='{')-(c=='}');assert dep>=0
    assert dep==0

def check(record,raw=False):
    assert set(record)=={'knowledge_point','question','generation'}
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];F,var,hold,X,Y,answer=displayed(record);formatting(q[':question/problem'])
    for f in q[':question/answer-fields']:
        values=[p.scalar(c[':answer/value']) for c in f[':answer-field/choices']];C['displayed_choices']+=len(values)
        assert len(values)==(1 if f[':answer-field/type'].endswith('/blank') else 5)
        assert not any(equal(v,w) for i,v in enumerate(values) for w in values[:i])
        assert sum(equal(v,answer) for v in values)==1
        t=record['generation']['template'];wrong,A,B=independent_bank(t,F,X,Y,q[':question/problem'])
        if len(values)>1:
            if record['generation']['profile']=='authored_method':expected=[answer]+wrong
            else:
                extraction=json.loads((D/'extraction.json').read_text());entry=next(v for v in extraction if v['template']==t)
                expected=[s.sympify(v['parameterized_pattern'],locals={'X':X,'Y':Y,'A':A,'B':B}) for v in entry['bank']]
            assert all(sum(equal(v,w) for w in values)==1 for v in expected),('incomplete operation bank',t,values,expected)
        if ':answer-field/correct' in f:
            assert f[':answer-field/correct'][0]==':answer/id'
            good=next(c for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]);assert equal(p.scalar(good[':answer/value']),answer)
        else:assert raw
        assert len({c[':answer/id'] for c in f[':answer-field/choices']})==len(values)
        if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        for c in f[':answer-field/choices']:formatting(c[':answer/value'])
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];formatting(sol)
        # Read every prose evaluation, point and fixed plane independently.
        for span in mathspans(sol):
            for vname,xy in re.findall(r'(?:\{f\}|f)_\{?([xy])\}?\((.*?)\)',span):
                assert vname==var
                if 'x' in xy or 'y' in xy:continue
                a,b=pair(xy);assert equal(a,X) and equal(b,Y)
            if re.match(r'[xy]\s*=',span):assert equal(p.scalar(span.split('=',1)[1]),Y if span[0]=='y' else X)
            if span.startswith('P('):a,b,_=map(p.scalar,span[2:-1].split(','));assert equal(a,X) and equal(b,Y)
        block=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(block)==1
        body=block[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
        rows=body.split(r'\\');first=True;stages=[]
        for row_index,row in enumerate(rows):
            sides=row.split('=');assert len(sides)>=2
            if row_index==0:
                lhs=re.fullmatch(r'\{f\}_\{([xy])\}\((.*)\)',sides[0].strip());assert lhs and lhs[1]==var
                a,b=pair(lhs[2]);assert equal(a,X) and equal(b,Y)
            else:assert not sides[0].strip()
            for side in sides[1:]:
                v=p.scalar(side.strip());assert equal(v,answer),(record['generation']['template'],row,v,answer);stages.append(side.strip());C['displayed_solution_stages']+=1
        # Require each family operation, beyond equality/row count. These check
        # unevaluated substitution structure read from the actual first row.
        t=record['generation']['template'];first=stages[0]
        assert 'x' not in re.sub(r'\\(?:operatorname|exp)', '',first) and not re.search(r'(?<![A-Za-z])y(?![A-Za-z])',first)
        if t in ('rational_radical','canonical_rational','canonical_trig'):assert r'\frac' in first and '^' in first and '(' in first
        if t=='rational_radical':assert r'\sqrt' in first and r'\frac' in stages[1] and '(' in stages[1] and len(rows)==3
        if t=='cos_shift':assert r'\operatorname{cos}' in first and r'\cdot' in first and r'\operatorname{cos}' in stages[1] and r'\cdot' in stages[2] and len(rows)==4
        if t=='polynomial':assert first.count('^{2}')==2 and len(rows)==3
        if t=='exp_cos':assert r'\operatorname{cos}' in first and r'\operatorname{cos}' not in stages[1] and '{e}^' in stages[1] and len(rows)==3
        if t=='radical_ratio':assert first.count('^{2}')==2 and r'\sqrt' in stages[1] and len(rows)==3
        if t.startswith('canonical_'):assert len(rows)==3 and stages[1].count('(')==(3 if t=='canonical_trig' else 2)
    else:assert raw
    C['records_checked']+=1
    return answer

cases=[];review=[];native=[]
for t,(i,var,layout,pa) in g.CONFIG.items():
    if i is None:continue
    src=g.SOURCES[i];record=g.generate('easy',template=t,parameters=pa,profile='observed_raw');q=record['question'];check(record,True)
    assert q[':question/problem']==src[':question/problem'];C['source_prompts_exact']+=1
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in src)
    if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution'];C['source_solutions_exact']+=1
    else:C['source_solution_absence_exact']+=1
    sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0];assert set(sf)-{':db/id'}==set(f)
    assert sorted(c[':answer/value'] for c in f[':answer-field/choices'])==sorted(c[':answer/value'] for c in sf[':answer-field/choices']);C['source_banks_exact']+=1;C['source_values_exact']+=5
    if ':answer-field/correct' in sf:
        good=next(c for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1]);assert good[':answer/value']==sf[':answer-field/correct'][':answer/value'];C['source_designations_exact']+=1
    else:assert ':answer-field/correct' not in f;C['source_designation_absence_exact']+=1
    C['source_key_presence']+=1
    cases.append({'source_id':src[':db/id'],'math_academy_id':src[':question/math-academy-id'],'difficulty':'easy','difficulty_origin':'observed' if ':question/difficulty' in src else 'authored-supported-assignment','template':t,'parameters':pa,'bank_profile':'observed_raw'})
    review.append(record)
    supported=g.generate('easy',template=t,parameters=pa,profile='observed_supported');check(supported);review.append(supported)
    for j in (431,829):
        changed=g.generate('easy',j,template=t,profile='observed_raw');check(changed,True);review.append(changed)
for t,data in g.TEMPLATES.items():
    print('Validating',t,flush=True)
    level=data['level'];seen=set()
    for seed in range(20):
        rec=g.generate(level,seed,template=t);ans=check(rec);seen.add(rec['generation']['mathematical_fingerprint'])
        # Identical arguments produce identical COMPLETE JSON-native records.
        assert rec==g.generate(level,seed,template=t)
        pp=rec['generation']['parameters'];other=g.generate(level,seed+1000,template=t,parameters=pp)
        assert rec['question'][':question/id']==other['question'][':question/id']
        if seed<2:review.append(rec)
        if seed<4:
            f=rec['question'][':question/answer-fields'][0]
            native.append({'label':t+'-'+str(seed),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio selection'} for a in f[':answer-field/choices']]})
            blank=g.generate(level,seed,template=t,field_type='blank',parameters=pp);ba=check(blank)
            canonical=next(a[':answer/value'] for a in blank['question'][':question/answer-fields'][0][':answer-field/choices'])
            # Actual derivative substituted into original expression, unreduced
            # parentheses remain in typed entry; not a CAS-simplified synonym.
            expr=displayed(blank)[0];X,Y=displayed(blank)[3:5]
            # Protect exp function name by replace token identifiers only.
            typed=re.sub(r'\bx\b','('+s.sstr(X)+')',s.sstr(expr));typed=re.sub(r'\by\b','('+s.sstr(Y)+')',typed)
            typed=typed.replace('log(','ln(').replace('E','e').replace('**','^')
            checks=[{'submitted':canonical,'expected':'accepted','purpose':'authored blank canonical slope'},{'submitted':typed,'expected':'accepted','purpose':'independently unreduced displayed derivative substitution'},{'submitted':g.tex(ba+1),'expected':'rejected','purpose':'incorrect typed slope'}]
            if t=='log_exp' and seed==0:
                checks[1]['expected']='unresolved'
                checks[1]['purpose']='documented native ln(exp(2)) identity restriction; independent math verifies equivalence'
                checks.append({'submitted':'2*2*2-e^2/e^2','expected':'accepted','purpose':'unreduced components after familiar logarithm evaluation'})
            native.append({'label':t+'-blank-'+str(seed),'record':blank,'checks':checks})
    assert len(seen)>=5, (t,len(seen))
# Every observed field with a real correct designation is checked in native
# replay; the supported missing-ref case adds an independently inferred answer.
for t,(i,*_) in g.CONFIG.items():
    if i is None:continue
    r=g.generate('easy',template=t,parameters=g.CONFIG[t][3],profile='observed_supported');f=r['question'][':question/answer-fields'][0]
    native.append({'label':t+'-observed-supported','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'source bank radio selection, inferred ref explicitly supported'} for a in f[':answer-field/choices']]})
# Scope and ambiguity regression guards.
for t,updates in [('canonical_rational',{'y':1}),('canonical_trig',{'b':0}),('canonical_rational',{'a':2,'x':2,'y':4}),('rational_radical',{'x':2}),('base_exp',{'a':8})]:
    pp=dict(g.CONFIG[t][3]);pp.update(updates)
    try:g.generate(g.TEMPLATES[t]['level'],template=t,parameters=pp)
    except ValueError:C['scope_invalid_rejections']+=1
    else:raise AssertionError(('invalid explicit parameters accepted',t,pp))
# Mutation must be caught even when final answer and row count remain correct.
r=g.generate('hard',template='canonical_trig');bad=json.loads(json.dumps(r));sol=bad['question'][':question/worked-solution'];first=sol.split('& =',1)[1].split(r'\\',1)[0];bad['question'][':question/worked-solution']=sol.replace(first,' '+g.tex(check(r))+' ',1)
try:check(bad)
except AssertionError:C['mutation_rejections']+=1
else:raise AssertionError('collapsed first operative stage passed')
(D/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n');(D/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(D/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
engine=R/'generate/runs/current/check-engine';subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
report=json.loads((D/'native-report.json').read_text());C.update(native_accepted=report['accepted_checks'],native_rejected=report['rejected_checks'],native_unresolved=report['documented_unresolved_checks'],engine_sha256=hashlib.sha256(engine.read_bytes()).hexdigest(),native_source_hashes={str(path.relative_to(R)):hashlib.sha256(path.read_bytes()).hexdigest() for path in (R/'engine/rust/learning.rs',R/'engine/rust/symbolic.rs',R/'generate/runs/current/check-engine.rs')},python=sys.version.split()[0],sympy=s.__version__,status='pass',database_writes=0,plots='none; no renderer/cache/concurrency applicable')
(D/'validation.json').write_text(json.dumps(C,indent=2)+'\n');print(json.dumps(C,indent=2))
