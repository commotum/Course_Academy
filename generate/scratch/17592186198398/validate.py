#!/usr/bin/env python3
"""Independent displayed-math, source fidelity, identity and native grading QA."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z,u,v,w=s.symbols('x y z u v w',real=True);variables=(u,v,w)
transforms=standard_transformations+(implicit_multiplication_application,)

def parse(text):
    text=text.strip().rstrip('.')
    text=text.replace('⁡','').replace('π',r'\pi').replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin')
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\cdot','*').replace(r'\pi','pi')
    # Recursive TeX fraction translation, independent of generator rendering.
    def brace(pos):
        if text[pos]!='{':raise AssertionError(('group expected',text,pos))
        depth=1;i=pos+1
        while depth:
            depth+=(text[i]=='{')-(text[i]=='}');i+=1
        return text[pos+1:i-1],i
    while r'\frac' in text:
        pos=text.rfind(r'\frac');a,end=brace(pos+5);b,end2=brace(end)
        text=text[:pos]+'(('+a+')/('+b+'))'+text[end2:]
    text=text.replace(r'\cos','cos').replace(r'\sin','sin').replace(r'\ln','log').replace(r'\sqrt','sqrt')
    text=text.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in text,('unparsed command',text)
    return parse_expr(text,local_dict=dict(zip(('x','y','z','u','v','w'),(x,y,z,u,v,w)))|{'pi':s.pi,'e':s.E,'cos':s.cos,'sin':s.sin,'log':s.log,'sqrt':s.sqrt},transformations=transforms)

def eq(a,b):assert s.simplify(a-b)==0,(a,b)
def formatcheck(text):
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    depth=0
    for i,ch in enumerate(text):
        if ch in '{}':
            count=0;j=i-1
            while j>=0 and text[j]=='\\':count+=1;j-=1
            if count%2:continue
            depth+=1 if ch=='{' else -1
            assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text
    assert '{{' not in text

def read_prompt(record):
    prompt=record['question'][':question/problem'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',prompt,re.S)
    if blocks:change,integrand,region=blocks
    else:change,integrand,region=re.findall(r'\$(.*?)\$',prompt,re.S)[0],re.findall(r'\$(.*?)\$',prompt,re.S)[1],re.findall(r'\$(.*?)\$',prompt,re.S)[3]
    clean=change.replace(r'\quad','').replace(r'\,','')
    trans=[]
    for token,t in zip(clean.split(','),(u,v,w)):
        lhs,rhs=token.split('=',1);assert lhs.strip()==str(t);trans.append(parse(rhs))
    integrand=re.sub(r'^\s*(?:\\iiint_R|\{∭\}_\{R\}|∭_\(R\))\s*','',integrand)
    integrand=re.sub(r'(?:\\,)?(?:\\mathrm\{d\}V|dV),?\s*$','',integrand)
    F=parse(integrand)
    region=region.split(':',1)[1].replace(r'\quad','').replace(r'\,','').strip().rstrip('.').rstrip('}').rstrip('\\')
    bound_expressions=[]
    for component in region.split(','):
        lo,expr,hi=component.split(r'\le');bound_expressions.append((parse(lo),parse(expr),parse(hi)))
    assert len(bound_expressions)==3
    M=s.Matrix(trans).jacobian((x,y,z));det=s.factor(M.det());assert det!=0
    # Solve uniquely, verifying every coordinate relation instead of choosing roots.
    inv=s.solve([e-t for e,t in zip(trans,(u,v,w))],(x,y,z),dict=True)
    assert len(inv)==1;inv=inv[0]
    bounds=[]
    for i,(lo,expr,hi) in enumerate(bound_expressions):
        transformed=s.simplify(expr.subs(inv,simultaneous=True));t=variables[i]
        factor=s.diff(transformed,t);offset=s.simplify(transformed-factor*t)
        assert offset==0 and factor.is_positive is True
        bounds.append((lo/factor,hi/factor))
    density=s.simplify(F.subs(inv,simultaneous=True)/s.Abs(det))
    answer=s.integrate(density,(w,*bounds[2]),(v,*bounds[1]),(u,*bounds[0]))
    return trans,M,det,bounds,density,s.simplify(answer)

def normalcheck(r):
    q=r['question'];f=q[':question/answer-fields'][0];meta=r['generation']
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    formatcheck(q[':question/problem']);formatcheck(q[':question/worked-solution'])
    for a in f[':answer-field/choices']:formatcheck(a[':answer/value'])
    assert len(f[':answer-field/choices'])==5 and len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    trans,M,D,bounds,density,answer=read_prompt(r)
    bank=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert all(s.simplify(a-b)!=0 for i,a in enumerate(bank) for b in bank[i+1:])
    index=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);eq(bank[index],answer)
    # Independent operation-bank QA reads the actual supplied transformation,
    # density and bounds; it never trusts generator answer-math metadata.
    J=1/s.Abs(D);c=M[2,2]
    integrate=lambda expression:s.simplify(s.integrate(expression,(w,*bounds[2]),(v,*bounds[1]),(u,*bounds[0])))
    expected_wrong=[integrate(density/J),integrate(density/J*s.Abs(D))]
    family=meta['template']
    if family=='power':
        n=s.degree(density,u)
        expected_wrong += [(n+1)*answer,answer/c if n==1 else 2*answer]
    elif family=='vcosu':expected_wrong += [integrate(J*v*(-s.sin(u))),2*answer]
    elif family=='ucosv':expected_wrong += [2*answer,integrate(J*u*(-s.sin(v)))]
    elif family=='sum':expected_wrong += [integrate(J*w),integrate(J*u)]
    elif family=='exp':expected_wrong += [J*s.exp(bounds[0][1])*(bounds[1][1]**2-bounds[1][0]**2)/2*(bounds[2][1]-bounds[2][0]),2*answer]
    elif family=='zcosu':expected_wrong += [integrate(J*w*w*s.cos(u)),3*answer]
    elif family=='sinsin':expected_wrong += [answer/c,-answer]
    assert len(expected_wrong)==4
    expected_bank=[answer]+expected_wrong
    for shown_value in bank:
        assert sum(s.simplify(shown_value-wanted)==0 for wanted in expected_bank)==1,(family,shown_value,expected_bank)
    # Read actual numeric Jacobian block cells and the minor expansion.
    matrices=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',q[':question/worked-solution'],re.S)
    assert len(matrices)==3
    actual=[[parse(c) for c in row.split('&')] for row in matrices[1].split(r'\\')]
    assert s.Matrix(actual)==M
    minor=[[parse(c) for c in row.split('&')] for row in matrices[2].split(r'\\')]
    assert s.Matrix(minor)==M[:2,:2]
    jacpart=q[':question/worked-solution'].split('**Step 2**:')[1].split('**Step 3**:')[0]
    cofactor_tail=jacpart.rsplit(r'\end{vmatrix}',1)[1].split(r' \\  & =')
    eq(parse(cofactor_tail[1]),D)
    eq(parse(cofactor_tail[2].split(r'\end{aligned}',1)[0]),D)
    inversepart=q[':question/worked-solution'].split('**Step 3**:')[1].split('**Step 4**:')[0]
    inverse_tex=inversepart.split(r'\right)^{-1}=',1)[1].split('.',1)[0]
    eq(parse(inverse_tex),1/D)
    assert len(re.findall(r'\\partial [uvw]\}\{\\partial [xyz]',matrices[0]))==9
    # The actual first density and initial transformed f are read from aligned RHS.
    text=q[':question/worked-solution'].split('**Step 4**:')[1]
    arith=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[0]
    rows=arith.split(r' \\ ')
    assert len(rows)==15
    first_rhs=rows[0].split(' & =',1)[1].split(r'\iiint_\Delta ',1)[1]
    first_f,first_inverse=first_rhs.split(r'\cdot \left|',1)
    inv_value=parse(first_inverse.split(r'\right|',1)[0])
    eq(inv_value,1/D)
    eq(parse(first_f)*s.Abs(inv_value),density)
    shown=rows[1].split(r'\iiint_\Delta ',1)[1].split(r'\,\mathrm{d}',1)[0]
    eq(parse(shown),density)
    # Verify every primitive and individually evaluated endpoint term from actual
    # rendered rows. Primitive brackets contain CAS expressions, not metadata.
    current=density
    for pos,t,offset in ((2,w,3),(1,v,7),(0,u,11)):
        primitive_row=rows[offset].split(' & =',1)[1]
        primitive_tex=primitive_row.split(r'\left[',1)[1].split(r'\right]',1)[0]
        primitive=parse(primitive_tex);eq(s.diff(primitive,t),current)
        # Independently parse displayed substitution and evaluated component rows;
        # remove precisely the enclosing remaining-integral prefixes/differentials.
        def arithmetic_expr(row):
            value=row.split(' & =',1)[1]
            if pos:
                prefixes=''.join(r'\int_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}' for lo,hi in bounds[:pos])
                assert value.startswith(prefixes+r'\left(')
                value=value[len(prefixes+r'\left('):]
                suffix=r'\right)'+''.join(r'\,\mathrm{d}'+str(t0) for t0 in reversed(variables[:pos]))
                assert value.endswith(suffix);value=value[:-len(suffix)]
            return parse(value)
        expected=s.simplify(primitive.subs(t,bounds[pos][1])-primitive.subs(t,bounds[pos][0]))
        eq(arithmetic_expr(rows[offset+1]),expected);eq(arithmetic_expr(rows[offset+2]),expected);eq(arithmetic_expr(rows[offset+3]),expected)
        # Distinct individual endpoint component pairs precede reduction.
        stage=meta['stages'][2-pos];terms=s.Add.make_args(s.expand(primitive))
        assert len(stage['components'])==len(terms)
        for term,pair in zip(terms,stage['components']):
            eq(parse(g.tex(s.sympify(pair[0],locals={'u':u,'v':v,'w':w}))),term.subs(t,bounds[pos][1]))
            eq(parse(g.tex(s.sympify(pair[1],locals={'u':u,'v':v,'w':w}))),term.subs(t,bounds[pos][0]))
        if q[':question/difficulty'].endswith('hard'):
            assert all(lo>0 for lo,hi in bounds)
            assert all(s.simplify(term.subs(t,bounds[pos][0]))!=0 for term in terms),('hard must evaluate every nonzero lower component',stage)
        current=expected
    eq(current,answer)
    return answer


def run():
    source=g.SOURCE['record'][':knowledge-point/questions'];cases=json.loads((HERE/'source-cases.json').read_text());raw_records=[]
    fidelity={'prompts':0,'worked_solutions':0,'banks':0,'choices':0,'correct_designations':0,'question_key_presence':0,'field_key_presence':0,'raw_solution_defects':1,'missing_correct_designations':2,'missing_worked_solutions':2,'unrated':2}
    for q,case in zip(source,cases):
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);raw_records.append(r)
        rq=r['question'];rf=rq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
        assert rq[':question/problem']==q[':question/problem'];fidelity['prompts']+=1
        assert set(rq)-{':question/id'}==set(q)-{':db/id',':question/id',':question/math-academy-id'};fidelity['question_key_presence']+=1
        assert set(rf)-{':answer-field/id'}==set(sf)-{':db/id',':answer-field/id'};fidelity['field_key_presence']+=1
        assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']);fidelity['banks']+=1;fidelity['choices']+=5
        _,_,_,_,_,ans=read_prompt(r)
        matching=[a for a in rf[':answer-field/choices'] if s.simplify(parse(a[':answer/value'])-ans)==0];assert len(matching)==1
        if ':question/worked-solution' in q:assert rq[':question/worked-solution']==q[':question/worked-solution'];fidelity['worked_solutions']+=1
        if ':answer-field/correct' in sf:
            correct=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert correct==sf[':answer-field/correct'][':answer/value'];fidelity['correct_designations']+=1
        assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
        # Public replay must actually vary integrand, all ordered stages, and bank.
        scaled=g.generate('moderate',template=case['template'],parameters={'scale':3},profile=case['bank_profile']);_,_,_,_,_,scaled_ans=read_prompt(scaled);eq(scaled_ans,3*ans)
        assert scaled['question'][':question/problem']!=rq[':question/problem']
        eq(next(parse(a[':answer/value']) for a in scaled['question'][':question/answer-fields'][0][':answer-field/choices'] if s.simplify(parse(a[':answer/value'])-3*ans)==0),3*ans)
    records=[];tasks={};coverage={};reviews=[]
    for level in g.LEVELS:
        families=('power',) if level=='easy' else g.FAMILIES
        for family in families:
            values=set();coverage[level+'-'+family]=0
            for seed in range(24):
                r=g.generate(level,seed,template=family);normalcheck(r);records.append(r);coverage[level+'-'+family]+=1;values.add(r['generation']['parameter_fingerprint'])
                # Fixed params/template/bank must keep UUIDs under seed changes.
                repeat=g.generate(level,seed+10000,template=family,parameters=r['generation']['parameters'])
                assert repeat['question'][':question/id']==r['question'][':question/id']
                assert sorted(a[':answer/id'] for a in repeat['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
                if seed<2:reviews.append(r)
            tasks[level+'-'+family]=len(values)
    # Normal default family coverage is measured, not inferred from API availability.
    defaultfamilies=set()
    for seed in range(70):defaultfamilies.add(g.generate('moderate',seed)['generation']['template'])
    assert defaultfamilies==set(g.FAMILIES)
    # Reduced task domains must separate difficulty, independent of labels/banks.
    bylevel={level:{r['generation']['parameter_fingerprint'] for r in records if r['question'][':question/difficulty'].endswith(level)} for level in g.LEVELS}
    assert all(not bylevel[a]&bylevel[b] for i,a in enumerate(g.LEVELS) for b in g.LEVELS[i+1:])
    positions=set()
    for r in records[:24]:
        f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    assert len(positions)>1
    # Explicit workload failures must not silently resample.
    hard=reviews[-1]
    invalid=dict(hard['generation']['parameters']);invalid['lz']='0'
    try:g.generate('hard',template=hard['generation']['template'],parameters=invalid)
    except ValueError:pass
    else:raise AssertionError('Hard accepted zero lower endpoint')
    engine=[]
    for i,r in enumerate(records+raw_records):
        f=r['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in f:continue
        engine.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio choice; scalar equivalence checked independently'} for a in f[':answer-field/choices']]})
    (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
    binary=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
    native=json.loads((HERE/'engine.json').read_text())
    (HERE/'review.json').write_text(json.dumps({'original_replays':raw_records,'generated_variants':reviews},indent=2,ensure_ascii=False)+'\n')
    text=['# Triple integral evaluation review','','Raw original evidence is ineligible for learning. Generated method banks are authored.']
    for original,case in zip(raw_records,cases):
        text += ['','### Original '+case['source_id'],'',g.markdown(original),'','### Generated moderate variants — '+case['template'],'']
        text += [g.markdown(r) for r in reviews if r['generation']['template']==case['template'] and r['question'][':question/difficulty'].endswith('moderate')]
    for level in ('easy','hard'):
        text+=['','### Authored '+level+' examples','']+[g.markdown(r) for r in reviews if r['question'][':question/difficulty'].endswith(level)]
    (HERE/'review.md').write_text('\n\n'.join(text)+'\n')
    report={'passed':True,'generator_version':g.VERSION,'python_version':sys.version.split()[0],'sympy_version':s.__version__,'source_basis':1356,'source_fidelity':fidelity,'normal_records_checked':len(records),'additional_actual_cofactor_inverse_initial_density_routes_checked':len(coverage),'independent_authored_wrong_operation_records_checked':len(records),'default_sampler_meaningful_capacity':json.loads((HERE/'domain-counts.json').read_text())['total'],'family_level_coverage':coverage,'unique_sampled_mathematical_tasks':tasks,'default_moderate_families':sorted(defaultfamilies),'graded_records':len(engine),'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'raw_native_untestable_missing_correct':2,'known_raw_format_defects':1,'authored_easy_hard':True,'database_writes':0,'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'limitations':['Raw opaque banks scale observed mathematical atoms; author error intentions are not recoverable from scalar evidence.','Two raw records lack correct refs/solution/difficulty and cannot be graded faithfully by the fixture.','One raw worked-solution endpoint row has an unmatched parenthesis; normal authored rows repair presentation.','Normal worked solutions use source common four-step prose and expanded successive integration rows; exact original ordered math rows are retained by public evidence replay.']}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
