#!/usr/bin/env python3
"""Independent display readback, provenance/fidelity, whole-bank and native QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('domain_kp',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,u,v=g.x,g.y,g.u,g.v

def write(name,value):(D/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def eq(a,b):
    diff=s.simplify(a-b)
    assert diff==0 or diff.equals(0),(a,b,diff)

def balanced(t):
    assert not any(ord(c)<32 and c not in '\n\t' for c in t),'C0 control byte'
    assert t.count('$')%2==0,'math delimiters'
    depth=0
    for i,c in enumerate(t):
        if c in '{}':
            n=0;j=i-1
            while j>=0 and t[j]=='\\':n+=1;j-=1
            if n%2:continue
            depth+=(1 if c=='{' else -1);assert depth>=0,'brace close'
    assert depth==0,'brace depth'

def group(t,i):
    assert t[i]=='{',(t,i);d=1;j=i+1
    while d:
        assert j<len(t),(t,'unterminated group');d+=(1 if t[j]=='{' else -1 if t[j]=='}' else 0);j+=1
    return t[i+1:j-1],j

def math(t):
    t=t.strip().replace('\u2061','').replace('\xa0','')
    for st in (r'\left',r'\right',r'\,',r'\:',r'\quad',r'\text{ }'):t=t.replace(st,'')
    t=t.replace(r'\operatorname{atan}',r'\arctan').replace(r'\operatorname{arctan}',r'\arctan').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{ln}',r'\ln')
    def expand(t):
        out='';i=0
        while i<len(t):
            m=re.match(r'\\(d?frac|sqrt)',t[i:])
            if not m:out+=t[i];i+=1;continue
            j=i+len(m[0]);a,j=group(t,j)
            if m[1]=='sqrt':out+='sqrt('+expand(a)+')'
            else:b,j=group(t,j);out+='(('+expand(a)+')/('+expand(b)+'))'
            i=j
        return out
    t=t.rstrip('.,')
    t=expand(t).replace(r'\cdot','*').replace(r'\pi','pi')
    t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
    for st,to in ((r'\arctan','atan'),(r'\sin','sin'),(r'\cos','cos'),(r'\ln','log')):t=t.replace(st,to)
    t=t.replace('{','(').replace('}',')').replace('[','(').replace(']',')').replace('^','**')
    t=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',t)
    # Source trig at ungrouped v and plain numeric log arguments.
    t=re.sub(r'(sin|cos|atan|log)\s*([uv]|[0-9]+)(?![a-zA-Z])',r'\1(\2)',t)
    assert '\\' not in t,('unsupported TeX',t)
    return parse_expr(t,local_dict=dict(x=x,y=y,u=u,v=v,pi=s.pi,E=s.E,sqrt=s.sqrt,Abs=s.Abs,sin=s.sin,cos=s.cos,atan=s.atan,log=s.log),transformations=standard_transformations+(implicit_multiplication_application,))

def calculus(t,ctx):
    t=t.replace(r'\left', '').replace(r'\right','')
    jabs=ctx['absj']
    t=t.replace(r'\left|\frac{\partial(x,y)}{\partial(u,v)}\right|',g.tex(jabs))
    t=t.replace(r'|\frac{\partial(x,y)}{\partial(u,v)}|',g.tex(jabs))
    if t.startswith(r'\iint_D '):
        f=math(t[len(r'\iint_D '):].split(r'\mathrm{d}x')[0].rstrip('\\,'))
        expr=s.simplify(f.subs({x:ctx['X'],y:ctx['Y']},simultaneous=True)*jabs)
        return s.integrate(expr,(u,ctx['a'],ctx['b']),(v,ctx['c'],ctx['d']))
    if t.startswith(r'\iint_\Delta '):
        f=math(t[len(r'\iint_\Delta '):].split(r'\mathrm{d}u')[0].rstrip('\\,'))
        return s.integrate(f,(u,ctx['a'],ctx['b']),(v,ctx['c'],ctx['d']))
    for _ in range(30):
        # Rightmost integral is innermost; its first differential closes it.
        pos=t.rfind(r'\int_')
        if pos>=0:
            lo,i=group(t,pos+len(r'\int_'));assert t[i]=='^';hi,j=group(t,i+1)
            close=re.search(r'\\mathrm\{d\}([uv])',t[j:]);assert close,(t,'integral differential')
            end=j+close.end();body=t[j:j+close.start()];var={'u':u,'v':v}[close[1]]
            value=s.integrate(calculus(body,ctx),(var,math(lo),math(hi)))
            t=t[:pos]+'('+g.tex(value)+')'+t[end:];continue
        # Last primitive bracket, followed by its own endpoint groups.
        candidates=list(re.finditer(r'\[([^\[\]]*)\]_\{',t))
        if candidates:
            m=candidates[-1];lo,i=group(t,m.end()-1);assert t[i]=='^';hi,j=group(t,i+1)
            expr=math(m[1]);vars=expr.free_symbols & {u,v};assert len(vars)==1,(expr,'primitive variable');var=vars.pop()
            value=expr.subs(var,math(hi))-expr.subs(var,math(lo));t=t[:m.start()]+'('+g.tex(value)+')'+t[j:];continue
        return math(t)
    raise AssertionError('calculus recursion ceiling')

def read_context(r):
    """Derive domain, inverse and integrand from actual learner strings."""
    prompt=r['question'][':question/problem'];sol=r['question'][':question/worked-solution']
    F=math(re.search(r'\\iint_D (.*?)\\,\\mathrm\{d\}x',prompt,re.S)[1])
    cond=prompt.split('where $D=\\{(x,y):')[1].split(r'\}.$')[0]
    parts=cond.split(r',\quad ');bounds=[];uv=[]
    for part in parts:
        aa,ex,bb=part.split(r'\le ');bounds.extend([math(aa),math(bb)]);uv.append(math(ex))
    a,b,c,d=bounds;U,V=uv
    match=re.search(r'\$x=(.*?),\\ y=(.*?)\$',sol);assert match
    X,Y=math(match[1]),math(match[2])
    eq(U.subs({x:X,y:Y},simultaneous=True),u);eq(V.subs({x:X,y:Y},simultaneous=True),v)
    J=s.det(s.Matrix([U,V]).jacobian([x,y]));j=s.det(s.Matrix([X,Y]).jacobian([u,v]))
    assert j!=0
    if r['generation']['template']=='radical':
        assert c*c < r['generation']['parameters']['R'] and d*d < r['generation']['parameters']['R']
        absj=s.sqrt(s.simplify(j*j))
        # Valid rectangle implies positive sqrt, derive it from printed inverse.
        absj=s.simplify(X/u)
    else:absj=abs(j)
    expr=s.simplify(F.subs({x:X,y:Y},simultaneous=True)*absj)
    I=s.expand(s.integrate(expr,(u,a,b),(v,c,d)))
    return dict(F=F,U=U,V=V,X=X,Y=Y,J=J,j=j,absj=absj,a=a,b=b,c=c,d=d,expr=expr,I=I)

def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];meta=r['generation'];f=meta['template']
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]:balanced(text)
    assert meta['eligible_for_learning'] and not meta['evidence_only']
    ctx=read_context(r);I=ctx['I'];field=q[':question/answer-fields'][0];answers=field[':answer-field/choices']
    assert len(answers)==5 and len({a[':answer/id'] for a in answers})==5
    ref=field[':answer-field/correct'];assert ref[0]==':answer/id'
    values=[math(a[':answer/value']) for a in answers]
    ix=next(i for i,a in enumerate(answers) if a[':answer/id']==ref[1]);eq(values[ix],I)
    for i in range(5):
        for j in range(i):assert s.simplify(values[i]-values[j])!=0,('whole bank ambiguity',f)
    # Read each displayed coordinate/domain stage before the integration chain.
    sol=q[':question/worked-solution'];step1=sol.split('**Step 1**')[1].split('**Step 2**')[0]
    transform=re.search(r'u=(.*?)\\,\\text\{and\}\\,v=(.*?)\.\n',step1,re.S);assert transform
    eq(math(transform[1]),ctx['U']);eq(math(transform[2]),ctx['V'])
    step2=sol.split('**Step 2**')[1].split('**Step 3**')[0]
    region=step2.split(r'\Delta=\{(u,v):')[1].split(r'\}.')[0]
    for part,var,lo,hi in zip(region.split(r',\,'),(u,v),(ctx['a'],ctx['c']),(ctx['b'],ctx['d'])):
        low,mid,high=part.split(r'\le ');eq(math(low),lo);eq(math(mid),var);eq(math(high),hi)
    step4=sol.split('**Step 4**')[1].split('Note that')[0]
    reciprocal=step4.split(r')^{-1}=')[1].split('\n$$')[0].rstrip('.')
    for expr in reciprocal.split('='):eq(math(expr).subs({x:ctx['X'],y:ctx['Y']},simultaneous=True),ctx['j'])
    # Jacobian matrix and determinant readback: formal matrix structure required.
    block=sol.split('**Step 3**')[1].split('**Step 4**')[0]
    matrix=re.search(r'\\left\|\\left\[\\begin\{matrix\}(.*?)\\end\{matrix\}\\right\]\\right\|',block,re.S)
    assert matrix,('Jacobian matrix missing',block)
    entries=[math(e) for row in matrix[1].split(r'\\') for e in row.split('&')]
    actual=s.Matrix(2,2,entries);expected=s.Matrix([ctx['U'],ctx['V']]).jacobian([x,y]);assert actual==expected
    printedJ=block.split(r'\\&=')[-1].split(r'.\end{aligned}')[0];eq(math(printedJ),ctx['J'])
    # Preserve operative stages independent of equalities.
    last=sol[sol.rfind(r'\begin{aligned}'):].split(r'\end{aligned}')[0]
    chain=last[len(r'\begin{aligned}'):].replace('&','').split(r'\\')
    pieces=[part for row in chain for part in row.split('=') if part.strip()]
    assert len(pieces)>=11,('required chain stages missing',f,len(pieces))
    if f=='radical':assert r'v^2(' in last and r'-v^2)' in last,'operative radical cancellation missing'
    if f=='quadratic_exp':assert r'\iint_D e^{x+(' in last,'exponent grouping absent'
    assert last.count(r'\int_')>=5 and last.count(r'\left[')>=2,'factor/separation/primitive structure'
    for part in pieces:
        try:eq(calculus(part.strip(),ctx),I)
        except AssertionError as e:raise AssertionError((f,meta['parameters'],part,e))
    # Every displayed primitive's derivative independently matches the factor
    # derived from the actual transformed integrand. Every evaluated component
    # at each endpoint is checked separately, preventing correlated errors.
    prims=re.findall(r'\\left\[(.*?)\\right\]_\{',last)
    assert len(prims)==2
    for prim in prims:
        expr=math(prim);vars=expr.free_symbols & {u,v};assert len(vars)==1;var=vars.pop()
        derivative=s.diff(expr,var)
        # Separability check includes the other factor, without relying on metadata.
        separated=s.separatevars(ctx['expr'],symbols=(u,v),dict=True);assert separated is not None
        eq(derivative,separated[var])
        lo,hi=(ctx['a'],ctx['b']) if var==u else (ctx['c'],ctx['d'])
        expected_components=[]
        for val in (hi,lo):expected_components.append([term.subs(var,val) for term in s.Add.make_args(s.expand(expr))])
        # Source-inspired added endpoint rows have explicit component parentheses.
        strings=[g.endpoint(expr,var,val) for val in (hi,lo)]
        # Readback is compared component by component, and presence is demanded.
        for text,components in zip(strings,expected_components):
            assert text in last,('individual endpoint components absent',f,text)
            terms=text.split('+');assert len(terms)==len(components)
            for displayed,expected_value in zip(terms,components):eq(math(displayed),expected_value)
    return len(pieces)

def source_math(record):
    """Read captured integrands/inequalities, solve inverse, integrate independently."""
    prompt=record['question'][':question/problem']
    if '$∬_(D)' in prompt:
        F=math(prompt.split('$∬_(D)')[1].split('dxdy')[0])
        conditions=prompt.split('where $D = {(x, y): ')[1].split('}')[0]
        parts=conditions.split(', ')
    else:
        F=math(prompt.split('{∬}_{D}')[1].split(r'\,dxdy')[0])
        conditions=prompt.split(r'where $D={(x,y)\,:\,')[1].rsplit('}.$',1)[0]
        parts=conditions.split(r'\,')
    parts=[part.rstrip('.') for part in parts if part]
    aa,UU,bb=parts[0].split(r'\le ');a,b,U=math(aa),math(bb),math(UU)
    if parts[1].startswith('|'):
        VV,dd=parts[1].split(r'\le ');V=math(VV.strip('|'));d=math(dd);c=-d
    else:
        cc,VV,dd=parts[1].split(r'\le ');c,d,V=math(cc),math(dd),math(VV)
    inv=s.solve([U-u,V-v],[x,y],dict=True);assert len(inv)==1,'global inverse ambiguity'
    X,Y=inv[0][x],inv[0][y];eq(U.subs({x:X,y:Y},simultaneous=True),u);eq(V.subs({x:X,y:Y},simultaneous=True),v)
    j=s.simplify(s.det(s.Matrix([X,Y]).jacobian([u,v])))
    if record['generation']['template']=='radical':
        rad=s.simplify((X/u)**2);assert rad.subs(v,c)>0 and rad.subs(v,d)>0
        absj=X/u
    else:absj=abs(j)
    weighted=s.simplify(F.subs({x:X,y:Y},simultaneous=True)*absj)
    return s.expand(s.integrate(weighted,(u,a,b),(v,c,d)))

def main():
    cases=[dict(source_id=g.SOURCE_NAMES[f],template=f,parameters={'k':1},bank_profile='source:'+g.SOURCE_NAMES[f]) for f in g.FAMILIES];write('source-cases.json',cases)
    raw=[];scaled_reviews=[];fidelity_banks=0;choices=0;designations=0;solutions=0;source_math_checks=0
    for case in cases:
        r=g.generate('moderate',seed=19,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];source=g.SOURCE_BY_NAME[case['source_id']]
        assert q[':question/problem']==source[':question/problem']
        for key in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (key in q)==(key in source),(case,key,'presence parity')
        if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution'];solutions+=1
        for field,orig in zip(q[':question/answer-fields'],source[':question/answer-fields']):
            assert field[':answer-field/key']==orig[':answer-field/key'];assert field[':answer-field/type']==orig[':answer-field/type'][':db/ident']
            assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in orig[':answer-field/choices'])
            assert (':answer-field/correct' in field)==(':answer-field/correct' in orig)
            if ':answer-field/correct' in orig:
                found=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert found[':answer/value']==orig[':answer-field/correct'][':answer/value'];designations+=1
            choices+=len(field[':answer-field/choices']);fidelity_banks+=1
        derived=source_math(r);source_math_checks+=1
        for field in q[':question/answer-fields']:
            vals=[math(a[':answer/value']) for a in field[':answer-field/choices']]
            assert sum(s.simplify(value-derived)==0 for value in vals)==1
            if ':answer-field/correct' in field:
                eq(math(next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])),derived)
        assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning'];raw.append(r)
        changed=g.generate('moderate',template=case['template'],profile=case['bank_profile'],parameters={'k':2});assert changed['question'][':question/problem']!=q[':question/problem'];assert changed['question'][':question/id']!=q[':question/id']
        scaled_reviews.append(changed)
        eq(source_math(changed),2*derived)
        for fi,field in enumerate(changed['question'][':question/answer-fields']):
            scaledvals=[math(a[':answer/value']) for a in field[':answer-field/choices']]
            origvals=[math(a[':answer/value']) for a in q[':question/answer-fields'][fi][':answer-field/choices']]
            assert all(sum(s.simplify(value-2*old)==0 for old in origvals)==1 for value in scaledvals)
    write('source-replay.json',raw)
    reviews=[];records=[];counts={};sample_task_counts={};family_coverage={};checks=0
    for level,families in g.LEVEL_FAMILIES.items():
        family_coverage[level]=[];sample_task_counts[level]={}
        for f in families:
            family_coverage[level].append(f);seen=set()
            for seed in range(12):
                r=g.generate(level,seed,template=f);checks+=check(r);records.append(r);seen.add(r['generation']['mathematical_fingerprint'])
                if seed<2:reviews.append(r)
                again=g.generate(level,seed+1,template=f,parameters=r['generation']['parameters'],profile='authored-method')
                assert again['question'][':question/id']==r['question'][':question/id'],'alias/order identity'
            sample_task_counts[level][f]=len(seen)
        counts[level]=len(families)*12
    easy_tasks=set()
    for b in range(1,9):
        for d in range(1,7):
            p=dict(a=0,b=b,c=0,d=d,m=1,k=1,h=0,q=1,R=9)
            try:r=g.generate_easy(parameters=p)
            except ValueError:continue
            easy_tasks.add(r['generation']['mathematical_fingerprint'])
    assert len(easy_tasks)==30
    hard_radical_tasks=set()
    for a in (1,2):
        for b in range(a+1,6):
            for c,d in ((1,2),(1,3),(2,3)):
                for R in (9,16,25):
                    if R<=d*d:continue
                    p=dict(a=a,b=b,c=c,d=d,m=1,k=1,h=0,q=1,R=R)
                    try:r=g.generate_hard(template='radical',parameters=p)
                    except ValueError:continue
                    hard_radical_tasks.add(r['generation']['mathematical_fingerprint'])
    assert len(hard_radical_tasks)==49
    moderate_enumeration={}
    for family,bounds in (('arctan',(range(2,9),range(2,7))),('quadratic_exp',(range(1,6),range(1,6)))):
        seen=set()
        for b in bounds[0]:
            for d in bounds[1]:
                p=dict(a=0,b=b,c=0,d=d,m=1,k=1,h=0,q=1,R=9)
                r=g.generate_moderate(template=family,parameters=p);seen.add(r['generation']['mathematical_fingerprint'])
        moderate_enumeration[family]=len(seen)
    assert moderate_enumeration=={'arctan':35,'quadratic_exp':25}
    # Normal selector default serves all families, rather than explicit-only support.
    for level in ('moderate','hard'):
        seen={g.generate(level,seed)['generation']['template'] for seed in range(50)};assert seen==set(g.LEVEL_FAMILIES[level])
    # Invalid explicit levels/inputs cannot bypass workload guards.
    invalid=[]
    for level in g.LEVEL_FAMILIES:
        r=g.generate(level,7);p=copy.deepcopy(r['generation']['parameters']);p['m']=10
        try:g.generate(level,template=r['generation']['template'],parameters=p)
        except ValueError:invalid.append(level)
        else:raise AssertionError('explicit workload escape')
    selectors_rejected=0
    for kw in (dict(profile='nonsense'),dict(field_type='blank'),dict(template='linear'),dict(template='arctan',profile='source:q-83651')):
        try:g.generate_moderate(**kw)
        except ValueError:selectors_rejected+=1
        else:raise AssertionError('selector accepted invalid alias')
    spelling=g.generate_hard(3,template='sine');pp=copy.deepcopy(spelling['generation']['parameters']);pp['c']='pi / 6'
    spelled=g.generate_hard(4,template='sine',parameters=pp)
    assert spelled['question'][':question/id']==spelling['question'][':question/id']
    assert spelled['generation']['mathematical_fingerprint']==spelling['generation']['mathematical_fingerprint']
    badrad=dict(a=1,b=3,c=1,d=4,m=1,k=1,h=0,q=1,R=25)
    try:g.generate_hard(template='radical',parameters=badrad)
    except ValueError:pass
    else:raise AssertionError('hard radical arithmetic ceiling escaped')
    # C0, endpoint and required-operation mutation regressions.
    base=g.generate('hard',2,template='radical')
    for kind in ('C0','endpoint','correlated_endpoints','operative'):
        bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution']
        if kind=='C0':text+='\f'
        elif kind in ('endpoint','correlated_endpoints'):
            ctx=read_context(base);expr=s.integrate(s.separatevars(ctx['expr'],symbols=(u,v),dict=True)[u],u)
            upper=g.endpoint(expr,u,ctx['b']);lower=g.endpoint(expr,u,ctx['a'])
            text=text.replace(upper,upper.replace(r'\left(',r'\left(1+',1),1)
            if kind=='correlated_endpoints':text=text.replace(lower,lower.replace(r'\left(',r'\left(1+',1),1)
        else:
            start=text.rfind(r'\begin{aligned}');prefix=text[:start];chain=text[start:]
            rows=chain.split(r' \\ & =');rows=[row for row in rows if r' u v^2(' not in row]
            text=prefix+r' \\ & ='.join(rows)
        bad['question'][':question/worked-solution']=text
        try:check(bad)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('mutation escaped '+kind)
    write('review.json',reviews+scaled_reviews)
    bankmap=[]
    for q in g.RAW:
        for fi,field in enumerate(q[':question/answer-fields']):
            bankmap.append(dict(source_id=q[':question/math-academy-id'],field_index=fi,correct_present=':answer-field/correct' in field,choices=[dict(source_answer_id=a[':answer/id'],value=a[':answer/value'],recipe='homogeneous k × immutable observed scalar atom; historical operation unresolved',match='exact') for a in field[':answer-field/choices']]))
    write('bank-map.json',bankmap)
    native=[]
    for i,r in enumerate(records):
        field=r['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
        native.append(dict(label=f'normal-{i}',record=r,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==correct else 'rejected',purpose='owned radio choice with independently verified displayed value') for a in field[':answer-field/choices']]))
    # Original designated banks can grade, but missing-correct raw fields cannot
    # enter the native fixture; record this denominator, never silently complete.
    for i,r in enumerate(raw):
        q=copy.deepcopy(r);fields=[f for f in q['question'][':question/answer-fields'] if ':answer-field/correct' in f]
        if fields:
            q['question'][':question/answer-fields']=fields
            native.append(dict(label='raw-designated-bank-'+str(i),record=q,checks=[dict(field_index=fi,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='faithful existing designation; not proof of math') for fi,f in enumerate(fields) for a in f[':answer-field/choices']]))
    write('native-input.json',native)
    root=D.parents[2];engine=root/'generate/runs/current/check-engine';report=D/'native-report.json'
    proc=subprocess.run([str(engine),str(D/'native-input.json'),str(report)],capture_output=True,text=True);assert proc.returncode==0,proc.stdout+proc.stderr
    n=json.loads(report.read_text())
    validation=dict(status='pass_with_documented_source_anomalies',source=dict(questions=6,prompts_exact=6,complete_banks_exact=fidelity_banks,choices_exact=choices,correct_designations_matched=designations,correct_designations_total=5,missing_designations=2,worked_solutions_exact=solutions,worked_solutions_present=5,raw_presence_parity=6,raw_evidence_only=True,original_integrals_independently_derived=source_math_checks,homogeneous_changed_integrals_checked=6),normal=dict(records=len(records),solution_equalities_verified=checks,per_level=counts,sampled_distinct_tasks=sample_task_counts,family_coverage=family_coverage,mutations_rejected=4,invalid_explicit_parameters_rejected=invalid,easy_eligible_tasks_enumerated=len(easy_tasks),hard_radical_eligible_tasks_enumerated=len(hard_radical_tasks),invalid_selectors_rejected=selectors_rejected,moderate_eligible_tasks_enumerated=moderate_enumeration),native=dict(accepted=n['accepted_checks'],rejected=n['rejected_checks'],unresolved=n['documented_unresolved_checks'],raw_missing_correct_fields_ineligible=2,engine_sha256=hashlib.sha256(engine.read_bytes()).hexdigest()),dependencies=dict(python=sys.version.split()[0],sympy=s.__version__),source_anomalies=['q38377 legacy duplicate field lacks correct designation; normal uses one supported radio','q82916 difficulty, correct and worked solution absent; raw omits them, normal independently completes','q160911 two outer dv differentials should be du; raw evidence exact, normal corrected','opaque source banks: only homogeneous scaling is claimed; no historical error intent recovered'],plots='none: inspected notation-only canonical rasters at full resolution')
    write('validation.json',validation)
    sections=['# Originals and generated variants','Database math, basis 1356. Raw originals are ineligible evidence. Generated variants use authored method banks.']
    for r in raw:sections.extend(['## Original '+r['generation']['source_ids'][0],g.markdown(r)])
    for r in scaled_reviews:sections.extend(['## Generated homogeneous source evidence k=2 / '+r['generation']['source_ids'][0],g.markdown(r)])
    for r in reviews:sections.extend(['## Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+r['generation']['template'],g.markdown(r)])
    (D/'review.md').write_text('\n\n'.join(sections)+'\n');print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
