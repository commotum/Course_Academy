#!/usr/bin/env python3
"""Actual printed ODE/initial pair, ordered operators, components, grading and baseline."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,re,hashlib,subprocess,copy,collections
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
Q=s.Symbol('Q',real=True)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def clean(t):return t.strip().rstrip('.').replace(r'\,','').strip()
def equality(a,b,domain='real x'):
    difference=s.sympify(a)-s.sympify(b)
    if domain=='x>-1/2':
        positive=s.Symbol('positive',positive=True);difference=difference.subs(g.X,(positive-1)/2)
    assert s.simplify(difference)==0,(a,b,domain,s.simplify(difference))
def derivative_token(t):
    t=t.replace(r'\frac{\text{d}y}{\text{d}x}','Q')
    t=re.sub(r'\{?[fgy]\}?\^\{′\}(?:\(x\))?','Q',t)
    return re.sub(r"[fgy]'(?:\(x\))?",'Q',t)
def actual(q):
    text=q[':question/problem'];ic=re.search(r'([fgy])\(([-\d]+)\)\s*=\s*(-?\d+)',text);assert ic,text
    name,input_,target=ic.groups();input_=s.Integer(input_);target=s.Integer(target)
    for match in g.fmt.MATH.finditer(text):
        width=2 if match[0].startswith('$$') else 1;math=clean(match[0][width:-width])
        if not ('′' in math or "'" in math or r'\text{d}y' in math):continue
        left,right=derivative_token(math).split('=');residual=g.parse(left)-g.parse(right);assert residual.has(Q)
        coefficient=s.diff(residual,Q);assert not coefficient.has(Q)
        der=s.solve(residual,Q)[0]
        return residual,der,input_,target,name
    raise AssertionError('No actual ODE')
def formatting(record):
    temporary=copy.deepcopy(record);temporary['question'].setdefault(':question/worked-solution','');g.fmt.validate_generated_record(temporary)
    texts=[record['question'][':question/problem'],record['question'].get(':question/worked-solution','')]+[a[':answer/value'] for f in record['question'].get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
    for text in texts:
        assert not any(ord(c)<32 and c not in '\n\t' for c in text),'control character'
        assert '--' not in text and '+-' not in text and '+ -' not in text

def integral_value(rhs,solution):
    while r'\int' in rhs:
        match=re.search(r'\\int\s*(.*?)\\text\{d\}([xu])',rhs,re.S);assert match,('unparsed integral',rhs)
        inside=clean(match[1]);var=g.X if match[2]=='x' else s.Symbol('u',real=True)
        primitive=s.integrate(g.parse(inside) if inside else s.Integer(1),var)
        rhs=rhs[:match.start()]+'('+g.tex(primitive)+')'+rhs[match.end():]
    value=g.parse(rhs)
    if value.has(s.Symbol('u',real=True)):
        assigned=re.search(r'Let \$u=(.*?)\.\$',solution);assert assigned
        value=value.subs(s.Symbol('u',real=True),g.parse(assigned[1]))
    return value

def solution_rows(sol):return [body.split(chr(92)*2) for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)]
def scaled_core(rhs):
    rhs=rhs.strip().lstrip('=').strip();before=rhs
    if rhs.endswith('.'):rhs=rhs[:-1]
    rhs=rhs.removesuffix(r'\,').rstrip()
    match=re.match(r'^\((-?\d+)\)\\cdot\((.*)\)(\+C)?$',rhs,re.S)
    if match:return match[2]+(match[3] or '')
    return rhs

def structure_check(r,sol):
    t=r['generation']['template']
    if t in g.QUESTIONS:
        original=g.QUESTIONS[t].get(':question/worked-solution')
        if original is None:return
        if t=='q-119045':original=original.replace('general solution is $y=', 'general solution is $f(x)=')
        if t=='q-50044':original=original.replace(r'6(\frac{{x}^{3}}{3})\,\text{d}x',r'6(\frac{{x}^{3}}{3})+C').replace('f(x)=','y=')
        source=solution_rows(original);rendered=solution_rows(sol);assert list(map(len,source))==list(map(len,rendered)),('operative row count',t)
        for block_index,(src,got) in enumerate(zip(source,rendered)):
            for a,b in zip(src,got):
                src_l,src_r=a.split('&',1);got_l,got_r=b.split('&',1)
                if block_index<len(source)-1:assert re.sub(r'\s+','',src_l)==re.sub(r'\s+','',got_l),'formal left input/variable changed'
                if src_l.strip()=='C' or (t=='q-8311' and src_l.strip()=='0' and 'C' in src_r):continue
                src_core=scaled_core(src_r);got_core=scaled_core(got_r)
                # Complete source component order/operator masks must survive,
                # including primitive multiplication and individually evaluated sums.
                canon=lambda z:re.sub(r'\s+','',z).rstrip('.')
                assert canon(src_core)==canon(got_core),('operative mask',t,block_index,src_core,got_core)
        assert sol.count('Then, we integrate both sides')==original.count('Then, we integrate both sides')
    else:
        rows=solution_rows(sol);assert list(map(len,rows))==[4,3]
        assert rows[0][2].count(')(')==3, 'three primitive coefficient products'
        assert rows[1][0].count('(')>=3 and rows[1][1].count('(')>=3,'three separate substitutions/evaluations'
        assert rows[0][1].count(r'\int')==3

def readback(r,raw=False):
    q=r['question'];m=r['generation'];assert set(r['knowledge_point'])=={'db_id','id','title'}
    formatting(r);residual,der,t,v,name=actual(q);domain=m['domain'];field=q[':question/answer-fields'][0]
    if m['template'] in ('q-119078','q-352066'):
        shift='1' if m['template']=='q-119078' else '3'
        assert re.search(r'\(\s*x\s*-\s*'+shift+r'\s*\)\^\{2\}',q[':question/problem']),'factored square coefficient required'
    assert m['mathematical_fingerprint']==m['math_fingerprint']
    assert m['mathematical_fingerprint']==g.fingerprint([s.srepr(s.factor(s.cancel(der))),str(t),str(v)])
    assert m['evidence_only']==m['profile'].startswith('observed_');assert m['eligible_for_learning']==(not m['evidence_only'])
    expected_domain='real x'
    coefficients=s.factor(s.diff(residual,Q));denom=s.denom(s.cancel(der))
    if der.has(s.log):raise AssertionError('logarithmic derivative unexpected')
    if der.has((g.X+1)**s.Rational(-1,2)):expected_domain='x>-1'
    elif s.simplify(denom.subs(g.X,s.Rational(-1,2)))==0:expected_domain='x>-1/2'
    elif s.simplify(denom.subs(g.X,1))==0:expected_domain='x>1'
    elif s.simplify(denom.subs(g.X,3))==0:expected_domain='x>3'
    elif s.simplify(coefficients.subs(g.X,0))==0:expected_domain='x<0'
    assert domain==expected_domain,(domain,expected_domain)
    if domain=='x>-1/2':assert t>s.Rational(-1,2)
    elif domain=='x>-1':assert t>-1
    elif domain=='x>1':assert t>1
    elif domain=='x>3':assert t>3
    elif domain=='x<0':assert t<0
    values=[];full=[]
    for a in field[':answer-field/choices']:
        answer=a[':answer/value']
        if field[':answer-field/type'].endswith('radio'):
            left,right=answer.split('=',1);assert left.strip()==('y' if name=='y' else name+'(x)');z=g.parse(right)
        else:
            assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem'];z=g.parse(answer)
        assert z.free_symbols<={g.X};values.append(z)
        if field[':answer-field/type'].endswith('blank'):
            partial=re.search(r'\$[^$]*?=([^$]*)\$\{\{field-1\}\}',q[':question/problem']);assert partial
            prefix=clean(partial[1]).rstrip('+');full.append(z+(g.parse(prefix) if prefix else 0))
        else:full.append(z)
    valid=[]
    for z in full:
        try:
            equality(residual.subs(Q,s.diff(z,g.X)),0,domain);equality(z.subs(g.X,t),v,domain);valid.append(True)
        except AssertionError:valid.append(False)
    assert sum(valid)==1,(m,valid)
    for i,z in enumerate(values):
        for other in values[i+1:]:assert s.simplify(z-other)!=0,'complete functions equivalent'
    ids=[a[':answer/id'] for a in field[':answer-field/choices']];assert len(set(ids))==len(ids)
    owned=field.get(':answer-field/correct',[None,None])[1]
    if owned is not None:assert owned in ids and valid[ids.index(owned)]
    correct_value=next((a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==owned),None)
    presence={'difficulty':q.get(':question/difficulty','').split('/')[-1] or None,'solution':':question/worked-solution' in q,'correct_value':correct_value}
    expected_hash=g.fingerprint([g.VERSION,q[':question/problem'],q.get(':question/worked-solution'),field[':answer-field/type'].split('/')[-1],field[':answer-field/key'],sorted(a[':answer/value'] for a in field[':answer-field/choices']),presence]);assert expected_hash==m['content_hash']
    sol=q.get(':question/worked-solution')
    if not sol:return values,valid
    if raw and m['template']=='q-119045':raise AssertionError('captured general solution dependent variable is y rather than f')
    if raw and m['template']=='q-50044':raise AssertionError('captured primitive retains dx and final dependent variable is f rather than y')
    structure_check(r,sol)
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)>=3
    first=clean(blocks[0]);left,right=derivative_token(first).split('=',1);equality((g.parse(left)-g.parse(right)).subs(Q,der),0,domain)
    last=clean(blocks[-1]);left,right=last.split('=',1);assert left==('y' if name=='y' else name+'(x)');final=g.parse(right);equality(final,full[valid.index(True)],domain)
    general=re.search(r'So our general solution is \$([^$]+)\$',sol);assert general
    left,right=clean(general[1]).split('=',1);assert left==('y' if name=='y' else name+'(x)');general_expr=g.parse(right)
    equality(s.diff(general_expr,g.X),der,domain);assert s.diff(general_expr,g.C)==1,'same additive C convention'
    actual_c=s.simplify(v-general_expr.subs({g.X:t,g.C:0}));assert not actual_c.has(g.X)
    # Verify original u substitution/differential using the actual printed u.
    if 'Let $u=' in sol:
        u=re.search(r'Let \$u=(.*?)\.\$',sol);du=re.search(r'Then \$\\text\{d\}u=(.*?)\\,\\text\{d\}x\.\$',sol);assert u and du
        equality(s.diff(g.parse(u[1]),g.X),g.parse(du[1]),domain)
    rows=solution_rows(sol)
    for group in rows[:-1]:
        for row in group:
            l,rhs=row.split('&',1);rhs=clean(rhs.strip().lstrip('='))
            if r'\int' in rhs:primitive=integral_value(rhs,sol)
            else:
                assert r'\text{d}x' not in rhs,'dx must end an integral, not an evaluated primitive'
                primitive=g.parse(rhs)
                if primitive.has(s.Symbol('u',real=True)):
                    primitive=primitive.subs(s.Symbol('u',real=True),g.parse(re.search(r'Let \$u=(.*?)\.\$',sol)[1]))
            equality(s.diff(primitive,g.X),der,domain)
    for row in rows[-1]:
        lhs,rhs=row.split('&',1);lhs=clean(lhs);rhs=clean(rhs.strip().lstrip('='))
        if lhs in ('y','f(x)','g(x)'):
            equality(s.diff(g.parse(rhs),g.X),der,domain);continue
        equality(g.parse(lhs).subs(g.C,actual_c),g.parse(rhs).subs(g.C,actual_c),domain)
    for match in re.finditer(r'(?:f|g|y)\(([-\d]+)\)\s*=\s*(-?\d+)',sol):
        assert s.Integer(match[1])==t and s.Integer(match[2])==v,'stale condition in prose'
    return values,valid

def engine_case(r,label):
    f=r['question'][':question/answer-fields'][0];checks=[]
    if f[':answer-field/type'].endswith('radio'):
        for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned complete-equation radio option'})
    else:
        a=f[':answer-field/choices'][0][':answer/value'];z=g.parse(a);alt=g.tex(s.expand(z))
        if alt==a:alt='('+a+')+'+r'\sin^2(x)+\cos^2(x)-1'
        checks=[{'submitted':a,'expected':'accepted','purpose':'Canonical exact required fragment'}, {'submitted':alt,'expected':'accepted','purpose':'Independently expanded or trig-identity equivalent'}, {'submitted':g.tex(z+1),'expected':'rejected','purpose':'Incorrect constant'}, {'submitted':g.tex(s.diff(z,g.X)),'expected':'rejected','purpose':'Derivative instead of primitive fragment'}]
    return {'label':label,'record':r,'checks':checks}

def baseline():
    expected=json.loads((HERE/'registered-baseline.json').read_text());paths=[Path('generate/scratch/17592186096699.py')]+sorted(p for p in Path('generate/scratch/17592186096699').rglob('*') if p.is_file())
    assert [str(p) for p in paths]==expected['pathset'],'registered pathset changed'
    for p in paths:assert hashlib.sha256(p.read_bytes()).hexdigest()==expected['files'][str(p)],str(p)
    return {'status':'unchanged','files':len(paths)}

def mutation_controls(records):
    sample=next(r for r in records if r['generation']['template']=='q-119046')
    source=sample['question'][':question/worked-solution'];cases=[]
    def reject(label,fn):
        r=copy.deepcopy(sample);fn(r)
        q=r['question'];field=q[':question/answer-fields'][0];ref=field.get(':answer-field/correct',[None,None])[1]
        correct_value=next((a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==ref),None)
        presence={'difficulty':q.get(':question/difficulty','').split('/')[-1] or None,'solution':':question/worked-solution' in q,'correct_value':correct_value}
        r['generation']['content_hash']=g.fingerprint([g.VERSION,q[':question/problem'],q.get(':question/worked-solution'),field[':answer-field/type'].split('/')[-1],field[':answer-field/key'],sorted(a[':answer/value'] for a in field[':answer-field/choices']),presence])
        try:
            _,d,t,v,_=actual(q);r['generation']['mathematical_fingerprint']=g.fingerprint([s.srepr(s.factor(s.cancel(d))),str(t),str(v)]);r['generation']['math_fingerprint']=r['generation']['mathematical_fingerprint']
            readback(r)
        except (AssertionError,ValueError,TypeError,IndexError):cases.append({'mutation':label,'rejected':True})
        else:raise AssertionError('undetected mutation '+label)
    reject('supplied initial value changes',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('f(1)=','f(2)=')))
    reject('operative primitive factor becomes algebraically collapsed',lambda r:r['question'].__setitem__(':question/worked-solution',source.replace(r'4(\frac{1}{2}{x}^{2})+x',r'2{x}^{2}+x')))
    reject('formal integral input changes',lambda r:r['question'].__setitem__(':question/worked-solution',source.replace('(4x+1)','(4x+2)',1)))
    reject('constant-substitution evaluated component changes',lambda r:r['question'].__setitem__(':question/worked-solution',source.replace('2+1+C','2+2+C')))
    reject('general-solution prose uses wrong dependent variable',lambda r:r['question'].__setitem__(':question/worked-solution',source.replace('general solution is $f(x)=','general solution is $y=')))
    reject('control character in learner content',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'))
    # Separate structural control bypasses content identity so collapsed equality
    # itself is rejected, not merely its intentionally stale hash.
    collapsed=source.replace(r'4(\frac{1}{2}{x}^{2})+x',r'2{x}^{2}+x')
    assert collapsed!=source
    try:structure_check(sample,collapsed)
    except AssertionError:cases.append({'mutation':'algebraically equivalent collapse without identity check','rejected':True})
    else:raise AssertionError('structure-only mutation undetected')
    return cases

def run():
    counts={'ma_questions':len(g.QUESTIONS),'prompts_exact':0,'solutions_present':0,'solutions_exact':0,'banks':0,'values':0,'captured_correct_designations':0,'presence_parity':0,'exact_answer_strings':0};cases=[];originals=[];engine=[];raw_errors=[];normal=[];notation=[];coverage=collections.defaultdict(set);slots=collections.defaultdict(lambda:collections.defaultdict(set))
    independent={'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':[]}
    for q in g.INDEPENDENT:
        hard=q[':question/difficulty'][':db/ident'].endswith('hard')
        independent['questions'].append({'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Authored three-component polynomial/exponential/trigonometric direct integration followed by one initial-condition constant equation; extends the two-component q-119075/q-119083 method without being observed MA hard evidence.' if hard else 'Authored already-isolated polynomial-plus-exponential direct integration followed by one initial condition, matching the mathematical workload of original q-119075/q-119083 with an authored opening/layout.'})
    save('independent-inventory.json',independent)
    for t,q in g.QUESTIONS.items():
        print('Original',t,flush=True);level=g.level_of(t);case={'source_id':t,'template':t,'level':level,'parameters':{'scale':1},'bank_profile':'observed_raw','unrated_level_is_authored':':question/difficulty' not in q};cases.append(case)
        raw=g.generate(level,template=t,profile='observed_raw',parameters={'scale':1});out=raw['question'];assert out[':question/problem']==q[':question/problem'];counts['prompts_exact']+=1
        assert out.get(':question/worked-solution')==q.get(':question/worked-solution')
        if ':question/worked-solution' in q:counts['solutions_present']+=1;counts['solutions_exact']+=1
        assert set(q)-{':db/id',':question/id',':question/math-academy-id'}==set(out)-{':question/id'}
        a=q[':question/answer-fields'][0];b=out[':question/answer-fields'][0]
        assert set(a)-{':db/id',':answer-field/id'}==set(b)-{':answer-field/id'};counts['presence_parity']+=1
        old=[g.parse(z[':answer/value'].split('=')[-1]) for z in a[':answer-field/choices']];new=[g.parse(z[':answer/value'].split('=')[-1]) for z in b[':answer-field/choices']];assert len(old)==len(new)
        for z in old:assert sum(s.simplify(z-w)==0 for w in new)==1
        for item in a[':answer-field/choices']:
            z=g.parse(item[':answer/value'].split('=')[-1]);got=next(w[':answer/value'] for w in b[':answer-field/choices'] if s.simplify(g.parse(w[':answer/value'].split('=')[-1])-z)==0);counts['exact_answer_strings']+=item[':answer/value']==got;notation.append({'source_id':t,'source':item[':answer/value'],'generated':got,'whole_value_matches':True})
        counts['banks']+=1;counts['values']+=len(old)
        if ':answer-field/correct' in a:counts['captured_correct_designations']+=1
        try:readback(raw,True)
        except AssertionError as error:
            assert t in ('q-119045','q-50044'),(t,error);raw_errors.append({'source_id':t,'error':str(error),'eligible_for_learning':False})
        repaired=g.generate(level,template=t,profile='observed_repaired',parameters={'scale':1});readback(repaired);engine.append(engine_case(repaired,t+'-repaired'))
        original={'source_id':t,'level':level,'raw':raw,'repaired':repaired,'variants':[]}
        for scale in (-2,2,4):
            replay=g.generate(level,template=t,profile='observed_repaired',parameters={'scale':scale});readback(replay);original['variants'].append(replay)
        originals.append(original)
    # Each easy/moderate source family is sampled through the supported normal
    # method bank, preserving its exact response layout and operative mask chain.
    for t in g.QUESTIONS:
        level=g.level_of(t)
        for scale,target in [(1,-1),(-2,7),(3,-8),(4,11)]:
            r=g.generate(level,template=t,parameters={'scale':scale,'target':target});readback(r);normal.append(r)
            slots[t]['scale'].add(scale);slots[t]['target'].add(target)
            if scale in (1,-2):engine.append(engine_case(r,'normal-'+t+'-'+str(scale)))
            other=g.generate(level,seed=123,template=t,parameters=r['generation']['parameters']);assert other['question'][':question/id']==r['question'][':question/id']
    fingerprints={l:set() for l in ('easy','moderate','hard')}
    for level in fingerprints:
        for seed in range(60):
            r=g.generate(level,seed=seed);readback(r);normal.append(r);coverage[level].add(r['generation']['template']);fingerprints[level].add(r['generation']['mathematical_fingerprint'])
            if level=='hard' and seed<4:engine.append(engine_case(r,'normal-hard-'+str(seed)))
    assert coverage['easy']=={t for t in g.QUESTIONS if g.level_of(t)=='easy'}
    assert coverage['moderate']=={t for t in g.QUESTIONS if g.level_of(t)=='moderate'}
    for kind in ('blank','radio'):
        r=g.generate('hard',seed=7,field_type=kind);readback(r);normal.append(r);engine.append(engine_case(r,'hard-'+kind))
        p=dict(r['generation']['parameters']);p['name']='g' if p['name']!='g' else 'f';renamed=g.generate('hard',parameters=p,field_type=kind);readback(renamed);assert r['generation']['mathematical_fingerprint']==renamed['generation']['mathematical_fingerprint']
    for level in ('easy','moderate'):
        t=next(t for t in g.QUESTIONS if g.level_of(t)==level)
        for bad in ({'scale':'3/2','target':1},{'scale':100,'target':1},{'scale':1,'target':'1/2'},{'scale':1,'target':0},{'scale':1,'target':13}):
            try:g.generate(level,template=t,parameters=bad)
            except AssertionError:pass
            else:raise AssertionError('invalid parameter accepted')
    alias1=g.generate('easy',template='q-352066',parameters={'scale':2,'target':7})
    alias2=g.generate('easy',seed=123,template='q-352066',parameters={'scale':'2/1','target':'7/1'})
    assert alias1['question'][':question/id']==alias2['question'][':question/id']
    base=g.generate('hard',field_type='blank')['generation']['parameters']
    for key,value in [('a','3/2'),('a',100),('b','3/2'),('b',4),('b',0),('d','3/2'),('d',5),('d',0),('v','1/2'),('v',13),('t','1/2'),('k','1/2')]:
        p=dict(base);p[key]=value
        try:g.generate('hard',parameters=p)
        except AssertionError:pass
        else:raise AssertionError('hard bound accepted')
    # Unassessed incidental parameters cannot create new hard task/content IDs.
    # All hard numeric parameters are assessed except function spelling, whose
    # task identity was independently checked above.
    mutations=mutation_controls(normal)
    save('source-cases.json',cases);save('notation-audit.json',notation);save('review.json',{'originals':originals,'generated':normal});save('engine-input.json',engine)
    subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    native=json.loads((HERE/'engine-validation.json').read_text());base_status=baseline()
    report={'status':'pass','database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'fidelity':counts,'independently_authored_inventory':len(independent['questions']),'raw_source_errors':raw_errors,'normal_math_instances':len(normal),'task_counts_in_default_sample':{l:len(v) for l,v in fingerprints.items()},'default_family_coverage':{l:sorted(v) for l,v in coverage.items()},'slots':{t:{k:sorted(v) for k,v in data.items()} for t,data in slots.items()},'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'mutation_controls':mutations,'registered_baseline':base_status,'database_writes':0}
    save('validation.json',report)
    md='# Basis-2275 particular-solution draft review\n\nOriginal replay preserves missing attributes and documented source errors. Banks use standard-TeX notation from scaling recipes. All observed banks are evidence-only. Independent inventory is separately identified.\n\n'
    for item in originals:
        md+='## '+item['source_id']+' — '+('unrated' if item['source_id'] in ('q-119078','q-49942') else item['level'])+' original raw replay\n\n'+g.markdown(item['raw'])+'\n\n'
        md+='### '+item['level']+' generated observed-pattern variant (scale 2; repaired and ineligible)\n\n'+g.markdown(item['variants'][1])+'\n\n'
        normal_variant=next(r for r in normal if r['generation']['template']==item['source_id'] and r['generation']['parameters']=={'scale':-2,'target':7})
        md+='### '+item['level']+' generated normal family variant (authored method bank)\n\n'+g.markdown(normal_variant)+'\n\n'
    for level in ('easy','moderate','hard'):
        examples=[r for r in normal if r['question'][':question/difficulty'].endswith('/'+level)][-2:]
        for i,r in enumerate(examples):md+='## '+level+' generated default variant '+str(i+1)+'\n\n'+g.markdown(r)+'\n\n'
    (HERE/'review.md').write_text(md);print(json.dumps(report,indent=2))
if __name__=='__main__':run()
