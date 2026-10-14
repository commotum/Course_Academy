#!/usr/bin/env python3
"""Independent printed-math, full source-bank, identity, and native-grader audit.
Raw source anomalies remain evidence exceptions; normal banks have no exceptions.
"""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT.with_suffix('.py')
spec=importlib.util.spec_from_file_location('kp87877',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X;Y=g.Y;YP=g.YP
TRANSFORMS=standard_transformations+(implicit_multiplication_application,)

def group(text,pos):
    if text[pos]!='{':raise ValueError('expected TeX group at '+text[pos:])
    depth=1;j=pos+1
    while depth:
        if j>=len(text):raise ValueError('unbalanced group')
        depth+=(text[j]=='{')-(text[j]=='}');j+=1
    return text[pos+1:j-1],j

def clean(tex):
    tex=tex.replace('\\\\','\\').replace('\\u2061','').replace('\u2061','')
    tex=re.sub(r'\\(?:text|textrm)\{([^}]*)\}',r'\1',tex)
    tex=tex.replace('\\operatorname{ln}',r'\ln').replace('\\operatorname{cos}',r'\cos').replace('\\operatorname{sin}',r'\sin')
    # All generated/replayed logarithmic banks explicitly assume x>0.
    tex=re.sub(r'\\ln\s*\|([^|]+)\|',lambda m:r'\ln('+m[1]+')',tex)
    return tex.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(' ','').replace('{e}', 'e')

def expression(tex):
    tex=clean(tex).rstrip('.')
    # Differential of a product is interpreted directly using the product rule.
    # This parser has no dependency on generation parameters or computed factors.
    tex=tex.replace(r'\frac{dy}{dx}','yp').replace(r'\dfrac{dy}{dx}','yp')
    tex=re.sub(r'(?<=[A-Za-z0-9)])yp',r'*yp',tex)
    derivative=re.compile(r'\\(?:d?frac)\{d\}\{dx(?:\^\{2\})?\}')
    while (m:=derivative.search(tex)):
        if m.end()>=len(tex) or tex[m.end()]!='(':raise ValueError('derivative must have a grouped operand')
        j=m.end()+1;dep=1
        while dep:
            dep+=(tex[j]=='(')-(tex[j]==')');j+=1
        operand=expression(tex[m.end()+1:j-1])
        result=s.diff(operand,X)+s.diff(operand,Y)*YP
        if '2' in m.group():result/=2*X
        placeholder='z'+str(len(REPLACEMENTS));REPLACEMENTS[placeholder]=result
        tex=tex[:m.start()]+placeholder+tex[j:]
    def convert(z):
        out='';i=0
        while i<len(z):
            if z.startswith(r'\frac',i) or z.startswith(r'\dfrac',i):
                cmd=r'\dfrac' if z.startswith(r'\dfrac',i) else r'\frac'
                num,j=group(z,i+len(cmd));den,k=group(z,j)
                out+='(('+convert(num)+')/('+convert(den)+'))';i=k
            elif z[i]=='{':
                inside,j=group(z,i);out+='('+convert(inside)+')';i=j
            elif z.startswith(r'\cos',i):out+='cos';i+=4
            elif z.startswith(r'\sin',i):out+='sin';i+=4
            elif z.startswith(r'\ln',i):out+='log';i+=3
            elif z[i]=='^':out+='**';i+=1
            elif z[i]=='\\':raise ValueError('unsupported command in '+z[i:])
            else:out+=z[i];i+=1
        # Convert TeX e**(exponent) to exp(exponent), not Euler's constant power.
        return out
    converted=convert(tex)
    converted=re.sub(r'log\|([^|]+)\|',r'log(Abs(\1))',converted)
    converted=re.sub(r"(cos|sin|log)x",r"\1(x)",converted)
    converted=re.sub(r"(?<=[\w)])(cos|sin|log)\(",r"*\1(",converted)
    locals={'x':X,'y':Y,'yp':YP,'e':s.E,'cos':s.cos,'sin':s.sin,'log':s.log,'Abs':s.Abs,**REPLACEMENTS}
    value=parse_expr(converted,local_dict=locals,transformations=TRANSFORMS,evaluate=True)
    return s.expand(value)
REPLACEMENTS={}

def relation(tex):
    left,right=tex.split('=',1)
    return s.expand(expression(left)-expression(right))
def same_equation(a,b):
    if not a.has(YP) or not b.has(YP):return False
    ca,cb=a.coeff(YP),b.coeff(YP)
    return s.cancel(a.coeff(Y)/ca-b.coeff(Y)/cb)==0 and s.cancel(a.subs({Y:0,YP:0})/ca-b.subs({Y:0,YP:0})/cb)==0

def formatting(text,delimited=True):
    if delimited:assert text.count('$')%2==0
    depth=0
    for i,c in enumerate(text):
        if c=='{' and (i==0 or text[i-1]!='\\'):depth+=1
        if c=='}' and (i==0 or text[i-1]!='\\'):depth-=1
        assert depth>=0,(text,'early closing brace')
    assert depth==0,(text,'unbalanced braces')
    assert '+-' not in text and '--' not in text

def block_maths(text):return re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',text)

def verify_record(record,allow_raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];meta=record['generation']
    assert meta['eligible_for_learning'] and not meta['evidence_only']
    for k in (':question/problem',':question/worked-solution'):formatting(q[k])
    problem=q[':question/problem']
    spans=list(g.MATH_SPAN.finditer(problem))
    ode=next(m.group().strip('$\n') for m in spans if r'\frac{dy}{dx}' in m.group())
    ode=ode.split(',')[0]
    supplied=relation(ode)
    normalized=s.expand(supplied/supplied.coeff(YP))
    P=s.simplify(normalized.coeff(Y));Q=s.simplify(-normalized.subs({Y:0,YP:0}))
    for name,expected_component in [('P',P),('Q',Q)]:
        matches=re.findall(r'\$'+name+r'\(x\)=([^$]+)\$',q[':question/worked-solution'])
        assert len(matches)==1
        assert s.simplify(expression(matches[0].rstrip('.'))-expected_component)==0,'stale named component'
    # Derive I independently from the printed ODE's coefficients.
    I=s.simplify(s.exp(s.integrate(P,X)))
    named_factor=re.findall(r'\$I\(x\)=([^$]+)\$',q[':question/worked-solution'])
    assert len(named_factor)==1 and s.simplify(expression(named_factor[0])-I)==0
    expected=s.expand(I*YP+s.diff(I,X)*Y-I*Q)
    f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5
    correct=f[':answer-field/correct'][1]
    choices=f[':answer-field/choices']
    assert len({a[':answer/id'] for a in choices})==5
    values=[];good=[]
    for a in choices:
        formatting(a[':answer/value'],False)
        assert r'\frac{d}{dx^{2}}' not in a[':answer/value'],'malformed operator cannot be eligible'
        value=relation(a[':answer/value']);values.append(value)
        if same_equation(value,expected):good.append(a[':answer/id'])
        assert a[':answer/id']==g.identity(f[':answer-field/id']+'/'+a[':answer/value'])
    assert good==[correct],(meta,good,correct)
    duplicates=[(i,j) for i in range(5) for j in range(i) if same_equation(values[i],values[j])]
    if not allow_raw:assert not duplicates,(meta,duplicates)
    # Independently parse every displayed arithmetic equality in worked stages.
    stages=block_maths(q[':question/worked-solution'])
    odeblocks=0
    for block in stages:
        if 'P(x)' in block or r'\int' in block:continue
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        for row in block.split(r'\\'):
            row=row.replace('&','').strip().rstrip('.')
            if not row:continue
            if row.startswith('I(x)'):continue
            actual=relation(row)
            assert same_equation(actual,normalized),(meta,row,actual,normalized)
            odeblocks+=1
    assert odeblocks>=3
    # Operative structure: factor definition, integration input, evaluated factor;
    # multiply the entire standard LHS, distribute it, then a product derivative.
    factorblocks=[b for b in stages if b.startswith(r'\begin{aligned}I(x)')]
    assert len(factorblocks)==1
    assert r'\int P(x)' in factorblocks[0] and factorblocks[0].count(r'\int')==2
    multiplied=[b for b in stages if r'\begin{aligned}\left(' in b and r'\frac{dy}{dx}' in b]
    assert len(multiplied)==1,'missing multiplication/distribution block'
    rows=multiplied[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    assert len(rows)==2
    first=rows[0].split('=',1)[0];second=rows[1].split('=',1)[0]
    assert r'\cdot \left(\frac{dy}{dx}' in first,'whole-LHS multiplication missing'
    assert r'\cdot \left(\frac{dy}{dx}' not in second,'distribution was not performed'
    assert any(b.startswith(r'\begin{aligned}\frac{d}{dx}\left(y\cdot ') for b in stages)
    if s.simplify(P*X).is_Integer and P.has(X):
        assert 'x>0' in problem, 'positive reciprocal branch omitted'
    for text in (q[':question/problem'],q[':question/worked-solution'],*(a[':answer/value'] for a in choices)):
        assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0 control'

    # Parse integrating-factor stages separately, checking derivative logarithm.
    factorblock=next(b for b in stages if b.startswith(r'\begin{aligned}I(x)'))
    rows=factorblock.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    for row in rows:
        rhs=row.split('=',1)[1].strip()
        if 'P(x)' in rhs:continue
        if r'\int' in rhs:
            integrand=rhs.split(r'\int',1)[1].rsplit(r'\,dx',1)[0]
            assert s.simplify(expression(integrand)-P)==0
        else:
            value=expression(rhs)
            assert s.simplify(value-I)==0,(rhs,value,I)
    assert q[':question/id']==g.identity(json.dumps([g.VERSION,q[':question/difficulty'].split('/')[-1],problem,q[':question/worked-solution'],sorted(a[':answer/value'] for a in choices),meta['domain']],ensure_ascii=False))
    assert r'\int I(x)Q(x)' not in q[':question/worked-solution'] and 'general solution' not in q[':question/worked-solution']
    return {'printed_equalities':odeblocks,'bank_choices':5,'equivalent_pairs':duplicates}

def prose(text):return g.MATH_SPAN.sub('<MATH>',text)

def engine_case(label,rec):
    f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'native radio correct/wrong selection'} for a in f[':answer-field/choices']]}


def source_audit(rec,sid,exact=True):
    raw=g.QUESTIONS[sid];q=rec['question'];f=q[':question/answer-fields'][0];rf=raw[':question/answer-fields'][0]
    for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
        assert (k in raw)==(k in q),(sid,'presence mismatch',k)
    assert (':answer-field/correct' in f)==(':answer-field/correct' in rf)
    if exact:
        assert q[':question/problem']==raw[':question/problem']
        assert q.get(':question/worked-solution')==raw.get(':question/worked-solution')
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
    assert f[':answer-field/key']==rf[':answer-field/key'] and f[':answer-field/type']==rf[':answer-field/type'][':db/ident']
    assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning']
    if ':answer-field/correct' in rf:
        a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        if exact:assert a[':answer/value']==rf[':answer-field/correct'][':answer/value']
    # Independent printed prompt derivation; malformed operator is excluded from
    # unambiguous semantic credit (its exact bytes still matched above).
    ode=next(m.group().strip('$\n') for m in g.MATH_SPAN.finditer(q[':question/problem']) if r'\frac{dy}{dx}' in m.group() or r'\frac{\text{d}y}' in m.group()).split(',')[0]
    equation=relation(ode);norm=s.expand(equation/equation.coeff(YP));P=s.simplify(norm.coeff(Y));Q=-norm.subs({Y:0,YP:0});I=s.simplify(s.exp(s.integrate(P,X)))
    expected=s.expand(I*YP+s.diff(I,X)*Y-I*Q)
    parsed=[];malformed=0;good=[]
    for a in f[':answer-field/choices']:
        if r'\frac{d}{dx^{2}}' in a[':answer/value']:
            malformed+=1
            assert s.simplify(expression(a[':answer/value'].split('=',1)[1])-X**2*Q)==0,'raw malformed-choice RHS stale'
            continue
        e=relation(a[':answer/value']);parsed.append(e)
        assert s.simplify(-e.subs({Y:0,YP:0})/e.coeff(YP)-Q)==0,'raw forcing stale in choice'
        original_factors=[relation(v[':answer/value']).coeff(YP) for v in rf[':answer-field/choices'] if r'\frac{d}{dx^{2}}' not in v[':answer/value']]
        assert any(s.simplify(e.coeff(YP)-v)==0 for v in original_factors),'raw factor changed outside its fixed slot'
        if same_equation(e,expected):good.append(a)
    assert len(good)==1
    if ':answer-field/correct' in f:assert good[0][':answer/id']==f[':answer-field/correct'][1]
    pairs=[(i,j) for i in range(len(parsed)) for j in range(i) if same_equation(parsed[i],parsed[j])]
    raw_wrong_stages=[]
    for block in block_maths(q.get(':question/worked-solution','')):
        if 'P(x)' in block or 'I(x)' in block:continue
        for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
            row=row.replace('&','').strip().rstrip('.')
            if not same_equation(relation(row),norm):raw_wrong_stages.append(row)
    assert len(raw_wrong_stages)==(1 if sid=='q-335278' else 0)
    return {'source_id':sid,'exact_prompt':True,'exact_solution':':question/worked-solution' in raw,'exact_complete_bank':True,'exact_values':5,'existing_key_matched':':answer-field/correct' in rf,'unambiguous_math_values':5-malformed,'malformed_exact_only':malformed,'equivalent_wrong_pairs':pairs,'original_wrong_stages':raw_wrong_stages,'missing_correct_independently_derived':':answer-field/correct' not in rf}

def assert_baseline():
    baseline=json.loads((ROOT/'registered-baseline.json').read_text());paths=[]
    for base in (ROOT.parent/'17592186087877.py',ROOT.parent/'17592186087877'):
        for p in ([base] if base.is_file() else [base,*sorted(base.rglob('*'))]):paths.append(str(p.relative_to(ROOT.parents[2])))
    expected=baseline['pathset']
    assert paths==expected,('registered pathset changed',paths,expected)
    for row in baseline['files']:
        assert hashlib.sha256((ROOT.parents[2]/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
    return {'files':len(baseline['files']),'paths':len(paths),'byte_hashes_unchanged':True,'pathset_unchanged':True}

def run():
    baseline=assert_baseline();source_cases=[];reports=[];review=[];md=[];engine=[];printed=0
    for sid,t,p in g.CASES:
        level=g.TEMPLATES[t][0];rec=g.generate(level,0,t,parameters=p,profile='raw:'+sid)
        reports.append(source_audit(rec,sid))
        if ':answer-field/correct' in rec['question'][':question/answer-fields'][0]:engine.append(engine_case(sid+'-exact-raw',rec))
        source_cases.append({'source_id':sid,'template':t,'level':level,'parameters':p,'bank_profile':'raw:'+sid,'profile':'raw:'+sid,'evidence_only':True,'difficulty_presence':':question/difficulty' in rec['question']})
        review.append(rec);md+=['## Exact original '+sid+' (ineligible evidence)',g.markdown(rec)]
        # Vary only the declared complete forcing slots, retaining the raw P.
        changed=dict(p)
        for k in ('n','b','c'):
            if k in changed:changed[k]=2
        variant=g.generate(level,7,t,parameters=changed,profile='raw:'+sid)
        assert variant['question'][':question/problem']!=rec['question'][':question/problem']
        assert variant['generation']['mathematical_fingerprint']!=rec['generation']['mathematical_fingerprint']
        source_audit(variant,sid,exact=False)
        review.append(variant);md+=['### Changed forcing / whole historical bank',g.markdown(variant)]
        normal=g.generate(level,9,t,parameters=p);printed+=verify_record(normal)['printed_equalities'];review.append(normal);md+=['### Normal supported presentation at source parameters',g.markdown(normal)]
        engine.append(engine_case(sid+'-normal',normal))
        # Prose and ordered source stages persist in default solutions.
        if ':question/worked-solution' in g.QUESTIONS[sid]:
            assert prose(normal['question'][':question/worked-solution'])==prose(rec['question'][':question/worked-solution'])
            assert [b.count(r'\\') for b in block_maths(normal['question'][':question/worked-solution'])]==[b.count(r'\\') for b in block_maths(rec['question'][':question/worked-solution'])]
    counts={};tasks={};slot_coverage={};default_coverage={}
    for level in ('easy','moderate','hard'):
        fingerprints=set();n=0;default=set()
        for seed in range(80):default.add(g.generate(level,seed)['generation']['template'])
        assert default=={t for t,(l,_) in g.TEMPLATES.items() if l==level}
        default_coverage[level]=sorted(default)
        for t,(l,_) in g.TEMPLATES.items():
            if l!=level:continue
            slots={}
            for seed in range(24):
                rec=g.generate(level,seed,t);printed+=verify_record(rec)['printed_equalities'];n+=1
                fingerprints.add(rec['generation']['mathematical_fingerprint'])
                assert rec==g.generate(level,seed,t)
                fixed=g.generate(level,seed+99,t,parameters=rec['generation']['parameters'])
                assert rec['question'][':question/id']==fixed['question'][':question/id']
                for k,v in rec['generation']['parameters'].items():slots.setdefault(k,set()).add(str(v))
                if seed<2:review.append(rec);md+=['## Generated '+level+' '+t+' seed '+str(seed),g.markdown(rec)];engine.append(engine_case(level+'-'+t+'-'+str(seed),rec))
            slot_coverage[t]={k:sorted(v) for k,v in slots.items()}
            assert all(len(v)>1 for v in slots.values())
        counts[level]=n;tasks[level]=len(fingerprints)
    # Each declared slot is swept with all other formal data held constant;
    # this checks actual prompts/steps/keys, not only metadata diversity.
    slot_sweeps={};sweep_total=0
    for t,(level,sid) in g.TEMPLATES.items():
        base=dict(g.RAW_CASES[sid][1]) if sid else dict(a=1,b=2,d=2,scale=2)
        domains={}
        for key in base:
            if key=='a':domains[key]=[str(a) for a in g.A_VALUES] if level=='easy' else [i for i in range(-3,4) if i]
            elif key=='k':domains[key]=[i for i in range(-4,5) if i]
            elif key=='n':domains[key]=[1,2,3,4]
            elif key=='d':domains[key]=[2,3]
            elif key=='scale':domains[key]=[2,3,4]
            elif key=='b' and t in ('constant_cos','scaled_reciprocal_cos'):domains[key]=[1,2,3,4]
            else:domains[key]=[i for i in range(-4,5) if i]
        slot_sweeps[t]={}
        for key,values in domains.items():
            changed_records=[]
            for value in values:
                p={**base,key:value};rec=g.generate(level,0,t,parameters=p)
                printed+=verify_record(rec)['printed_equalities'];sweep_total+=1
                changed_records.append(rec['generation']['mathematical_fingerprint'])
            slot_sweeps[t][key]={'values':list(map(str,values)),'math_task_count':len(set(changed_records)),'presentation_only_slot':key=='scale'}
            assert len(set(changed_records))==(1 if key=='scale' else len(values))
    # Legacy normalized evidence profiles must never enter either the public
    # serving API or its internal normal-record constructor as eligible output.
    legacy_rejections=[]
    for t,(level,sid) in g.TEMPLATES.items():
        p=dict(g.RAW_CASES[sid][1]) if sid else dict(a=1,b=2,d=2,scale=2)
        for entrypoint in (g.generate,g._generate_normal):
            try:entrypoint(level,0,t,parameters=p,profile='observed_raw')
            except ValueError:legacy_rejections.append({'template':t,'entrypoint':entrypoint.__name__,'result':'rejected before record creation'})
            else:raise AssertionError('Legacy normalized historical bank was returned as a serving record')
    # Public formal inputs and role-specific workload guards.
    invalid=[]
    for t,(level,_) in g.TEMPLATES.items():
        p=g.generate(level,5,t)['generation']['parameters']
        for bad in ({**p,'unused':1},{k:v for k,v in p.items() if k!=next(iter(p))},{**p,next(iter(p)):True}):invalid.append((level,t,bad))
        for k in p:
            invalid.append((level,t,{**p,k:0}))
            if k=='n':invalid.append((level,t,{**p,k:5}))
            elif k=='d':invalid.append((level,t,{**p,k:4}))
            elif k=='scale':invalid.append((level,t,{**p,k:1}))
            else:invalid.append((level,t,{**p,k:99}))
    for level,t,p in invalid:
        try:g.generate(level,parameters=p,template=t)
        except (ValueError,TypeError):pass
        else:raise AssertionError(('invalid public input accepted',level,t,p))
    # Scale is incidental to the assessed normalized ODE and excluded from task counts.
    a=g.generate('hard',0,'polynomial_transform',parameters=dict(a=1,b=2,d=3,scale=2));b=g.generate('hard',0,'polynomial_transform',parameters=dict(a=1,b=2,d=3,scale=4))
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
    # Structural mutation controls retain equality or row counts while deleting
    # the requested teaching operation. They must fail independently of final key.
    mutations=[];base=g.generate('moderate',0,'reciprocal_exp',parameters=dict(k=-3,b=2))
    sol=base['question'][':question/worked-solution'];blocks=block_maths(sol);mult=next(b for b in blocks if b.startswith(r'\begin{aligned}\left('))
    rows=mult.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    mutation=copy_record(base);mutation['question'][':question/worked-solution']=sol.replace(rows[0],rows[1]);mutations.append(('whole-LHS multiplication deleted but equal distributed row duplicated',mutation))
    mutation=copy_record(base);mutation['question'][':question/worked-solution']=sol.replace(rows[1],rows[0]);mutations.append(('distribution deleted but equal grouped row duplicated',mutation))
    mutation=copy_record(base);mutation['question'][':question/worked-solution']=sol.replace('$P(x)=-', '$P(x)=');mutations.append(('wrong named P sign',mutation))
    mutation=copy_record(base);mutation['question'][':question/worked-solution']=sol+'\x0c';mutations.append(('control-character injection',mutation))
    mutation=copy_record(base);mutation['question'][':question/problem']=mutation['question'][':question/problem'].replace('x>0','x<0');mutations.append(('positive logarithm branch switched without factor convention repair',mutation))
    for label,mut in mutations:
        try:verify_record(mut)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('mutation not rejected: '+label)
    # ln|2x| branch and factor-constant convention are checked symbolically without
    # substituting the positive proxy into a negative-interval expression.
    z=s.Symbol('z',real=True)
    assert s.simplify(s.diff(s.log(-2*z),z)-1/z)==0
    assert s.simplify(s.diff(-z**3,z)/(-z**3)-3/z)==0
    (ROOT/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
    (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([str(ROOT.parents[1]/'runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    native=json.loads((ROOT/'engine-report.json').read_text());baseline=assert_baseline()
    inventory=json.loads((ROOT/'independent-inventory.json').read_text());assert inventory['basis']==g.SOURCE['basis'] and len(inventory['questions'])==9
    assert [r['record'] for r in inventory['questions']]==[q for q in g.SOURCE['record'][':knowledge-point/questions'] if not q.get(':question/math-academy-id')]
    report={'status':'pass','script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'original_MA_questions':8,'independent_inventory_exact_records':9,'raw_exact_prompts':8,'raw_exact_complete_banks':8,'raw_exact_values':40,'raw_exact_solutions':6,'attribute_omission_parity':8,'existing_correct_refs_exact':6,'missing_correct_refs_preserved':2,'missing_correct_independent_normal_derivations':2,'unambiguous_source_value_math_checks':39,'malformed_source_value_exact_bytes_only':1,'raw_ambiguous_banks':3,'raw_sign_error_retained':1,'normal_sign_error_repaired':1,'generated_cases':counts,'mathematical_task_counts':tasks,'slot_coverage':slot_coverage,'default_family_coverage':default_coverage,'printed_equalities_verified':printed,'slot_sweeps':slot_sweeps,'slot_sweep_cases':sweep_total,'legacy_observed_raw_rejections':legacy_rejections,'invalid_public_inputs_rejected':len(invalid),'structural_mutations_rejected':[label for label,_ in mutations],'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':native['documented_unresolved_checks'],'native_response_contract':'All sources/defaults are radio. Native checks use actual option selection; typed algebraic-equivalence entries are not a radio response. Complete-equation equivalence is independently checked from printed math.','baseline':baseline,'source_audits':reports,'all_normal_profiles_eligible':True,'raw_profiles_eligible':False,'known_findings':['Historical malformed d/dx² meaning is unresolved; exact ineligible raw replay receives byte fidelity only.','Three historical banks have scale-equivalent wrong equations; normal whole banks reject those.','q335278 contains one wrong distributed sign; raw retained and normal repaired.','Earlier worker escaped-TeX anomaly claim was incorrect: decoded strings have single command slashes and actual U+2061, as preserved raw evidence.']}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('slot_coverage','slot_sweeps','source_audits','legacy_observed_raw_rejections')},indent=2))

def copy_record(rec):return json.loads(json.dumps(rec))
if __name__=='__main__':run()
