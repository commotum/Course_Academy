#!/usr/bin/env python3
"""Independent displayed-math readback, exact source presence/banks, native grading."""
import copy,hashlib,importlib.util,importlib.metadata,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def scalar(text):
    text=text.strip().replace('−','-').replace(r'\cdot','*')
    frac=re.compile(r'\\frac\{(-?\d+)\}\{(-?\d+)\}')
    text=frac.sub(lambda m:'('+m[1]+'/'+m[2]+')',text)
    text=text.replace(' ','')
    assert re.fullmatch(r'[\d+*/().-]+',text),text
    return sp.sympify(text,rational=True)
def vector(text):
    match=re.fullmatch(r'⟨(.*),(.*)⟩',text.strip());assert match,text
    return sp.ImmutableMatrix([scalar(match[1]),scalar(match[2])])
def expression(text,env=None):
    matrices={}
    def slot(m):
        name='V'+str(len(matrices));matrices[name]=vector(m[0]);return name
    text=re.sub(r'⟨[^⟩]+⟩',slot,text.strip())
    text=text.replace(r'\cdot','*')
    text=text.replace(r'\overset{\to }{A}','a').replace(r'\overset{\to }{B}','b')
    text=re.sub(r'(\d)([abuv])',r'\1*\2',text)
    text=re.sub(r'(\))(V\d+)',r'\1*\2',text)
    assert re.fullmatch(r'[\w+*/().\s-]+',text),text
    return sp.sympify(text,locals=matrices|dict(env or {}),rational=True)
def displayed_correct(record):
    q=record['question'];prompt=q[':question/problem'];vs=[vector(x) for x in re.findall(r'⟨[^⟩]+⟩',prompt)]
    env={'a':vs[0],'u':vs[0]}
    if len(vs)==2:env|={'b':vs[1],'v':vs[1]}
    if prompt.startswith('What is the sum'):return vs[0]+vs[1]
    maths=re.findall(r'\$([^$]+)\$',prompt)
    target=maths[-1].rstrip('= ')
    return expression(target,env)
def check(record):
    q=record['question'];meta=record['generation'];correct=displayed_correct(record)
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert all(k.startswith(':') for k in q)
    import uuid
    uuid.UUID(q[':question/id'])
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]:
        assert not any(ord(c)<32 and c not in '\n\t' for c in text)
        assert text.count('$')%2==0
        n=0
        for c in text:
            if c=='{':n+=1
            if c=='}':n-=1
            assert n>=0
        assert n==0
        assert not any(bad in text for bad in ('+-','--','-+'))
        assert '![[' not in text and '![](' not in text
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];body=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
        rows=body.split('\\\\')
        promptvs=[vector(x) for x in re.findall(r'⟨[^⟩]+⟩',q[':question/problem'])]
        env={'a':promptvs[0],'u':promptvs[0]}
        if len(promptvs)>1:env.update(b=promptvs[1],v=promptvs[1])
        assert expression(rows[0].split('&')[0],env)==correct
        initial_vectors=[vector(x) for x in re.findall(r'⟨[^⟩]+⟩',rows[0])]
        assert initial_vectors==promptvs,('printed operand mismatch',initial_vectors,promptvs)
        expected_rows={'sum':2,'subtract':3,'scalar':3,'linear':4,'double_scaled':4,'fractional_linear':4}[meta['template']]
        assert len(rows)==expected_rows,(rows,meta)
        for row in rows:
            rhs=row.split('=',1)[1].strip();assert expression(rhs)==correct,(rhs,correct)
        # These unevaluated operations are structurally mandatory, not simplified aliases.
        if meta['template']=='scalar':assert rows[1].count(r'\cdot')==2
        if meta['template'] in ('subtract','linear','double_scaled','fractional_linear'):
            component_parts=re.findall(r'⟨([^⟩]+)⟩',rows[-2])[0].split(',')
            assert len(component_parts)==2 and all(re.search(r'\s[+-]\s',part) for part in component_parts)
            assert rows[0].count(r'\cdot')=={'subtract':0,'linear':1,'double_scaled':2,'fractional_linear':1}[meta['template']]
            if meta['template']!='subtract':assert r'\cdot' not in rows[1]
        assert OPENING in sol
    # Independent whole-bank construction from actually printed operands/coefficient.
    pv=[vector(x) for x in re.findall(r'⟨[^⟩]+⟩',q[':question/problem'])]
    a=tuple(pv[0]); b=tuple(pv[1]) if len(pv)>1 else None; c=tuple(correct)
    family=meta['template']
    if family=='sum': expected=[c,(a[0]-b[0],c[1]),(c[0],a[1]-b[1]),(a[0]-b[0],a[1]-b[1]),(c[1],c[0])]
    elif family=='subtract':expected=[c,(a[0]-b[0],a[1]+b[1]),(b[0]-a[0],c[1]),(a[0]+b[0],c[1]),(a[0]+b[0],a[1]+b[1])]
    else:
        requested=re.findall(r'\$([^$]+)\$',q[':question/problem'])[-1].rstrip('= ')
        symbols={x:sp.Symbol(x) for x in ('a','b','u','v')}
        parsed=expression(requested,symbols)
        k=parsed.coeff(symbols['a']) if family=='scalar' else parsed.coeff(symbols['b'])
        if family=='scalar':expected=[c,(k*a[0],a[1]),(a[0],k*a[1]),(-k*a[0],-k*a[1]),(a[0]+k,a[1]+k)]
        elif family in ('linear','fractional_linear'):expected=[c,(-a[0]+k*b[0],c[1]),(-a[0]+k*b[0],-a[1]+k*b[1]),(c[0],-a[1]+k*b[1]),(c[0],-c[1])]
        else:
            r=parsed.coeff(symbols['a'])
            expected=[c,(a[0]+k*b[0],a[1]+k*b[1]),(r*a[0]+b[0],r*a[1]+b[1]),(r*a[0]-k*b[0],r*a[1]-k*b[1]),(r*a[0]+k*b[1],r*a[1]+k*b[0])]
    if ':question/worked-solution' in q:
        if family in ('linear','fractional_linear'):
            ev=[vector(x) for x in re.findall(r'⟨[^⟩]+⟩',rows[1])]
            assert ev==[pv[0],abs(k)*pv[1]],('scaled operands',ev)
        if family in ('subtract','linear','fractional_linear'):
            factor=-1 if family=='subtract' else k
            for index,part in enumerate(component_parts):
                bits=re.split(r'\s([+-])\s',part.strip(),maxsplit=1);assert len(bits)==3,bits
                assert scalar(bits[0])==a[index] and scalar(bits[2])==abs(factor)*b[index]
                assert bits[1]==('+' if factor>0 else '-')
        if family=='scalar':
            parts=re.findall(r'⟨([^⟩]+)⟩',rows[1])[0].split(',')
            for index,part in enumerate(parts):
                bits=part.split(r'\cdot');assert len(bits)==2
                assert scalar(bits[0])==k and scalar(bits[1])==a[index]
    for f in q.get(':question/answer-fields',[]):
        assert f[':answer-field/type']==':answer-field.type/radio'
        choices=f[':answer-field/choices'];assert len(choices)==5
        vals=[vector(a[':answer/value']) for a in choices]
        assert {tuple(v) for v in vals}==set(expected),(vals,expected)
        assert len(set(vals))==5
        matches=[a for a,v in zip(choices,vals) if v==correct];assert len(matches)==1
        assert len({a[':answer/id'] for a in choices})==5
        if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',matches[0][':answer/id']]
        else:assert meta['evidence_only']
    return correct
OPENING='we just need to perform the required operations with each component separately:'
source=json.loads((HERE/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
cases=json.loads((HERE/'replay-parameters.json').read_text())
def main():
    raw=[];completed=[];fidelity=[]
    for case in cases:
        record=g.generate(case['level'],profile=case['bank_profile'],parameters=case['parameters']);raw.append(record);check(record)
        orig=sources[case['source_id']];q=record['question']
        for key in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (key in q)==(key in orig),(case,key)
        assert q[':question/problem']==orig[':question/problem'],(q[':question/problem'],orig[':question/problem'])
        if ':question/worked-solution' in orig:assert q[':question/worked-solution']==orig[':question/worked-solution']
        if ':question/answer-fields' in orig:
            old=orig[':question/answer-fields'][0];new=q[':question/answer-fields'][0]
            assert (':answer-field/correct' in old)==(':answer-field/correct' in new)
            assert sorted(a[':answer/value'] for a in old[':answer-field/choices'])==sorted(a[':answer/value'] for a in new[':answer-field/choices'])
            assert old[':answer-field/type'][':db/ident']==new[':answer-field/type']
        fidelity.append({'source_id':case['source_id'],'exact_prompt':True,'presence_parity':True,'complete_bank_matched':':question/answer-fields' in orig,'exact_solution_matched':':question/worked-solution' in orig,'original_correct_ref_present':False})
        completed.append(g.generate(case['level'],profile=case['normal_profile'],parameters=case['parameters']))
    save('source-replays.json',raw);save('source-completions.json',completed)
    inventory=json.loads((HERE/'independent-inventory.json').read_text())
    assert {k:inventory[k] for k in ('database','basis','lineage')}==g.SOURCE
    nonma=[q for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    assert [r['record'] for r in inventory['questions']]==nonma
    for captured in nonma:
        q=copy.deepcopy(captured);prompt=q[':question/problem']
        family='sum' if prompt.startswith('What') else 'subtract' if prompt.startswith('If $u') else 'scalar' if prompt.startswith('If') else 'linear'
        for f in q[':question/answer-fields']:
            f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
            for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
        check({'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':q,'generation':{'template':family}})
    assert all(r['role']=='independently authored inventory' and r['relationship_to_source_templates'] for r in inventory['questions'])
    originalwrappers=json.loads((HERE/'source-cases.json').read_text());assert originalwrappers==[{'source_id':q[':question/math-academy-id'],'record':q} for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
    # Canonical proof chain, apart from its bold/whitespace presentation, uses the same four stages.
    canonical=source['record'][':knowledge-point/canonical-example'];canonical_normal=g.generate_moderate(parameters={'a':[-7,15],'b':[14,-11],'k':-3});check(canonical_normal);save('canonical-normal.json',canonical_normal)
    body=canonical[':question/worked-solution'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    assert len(body.split('\\\\'))==4
    for row in body.split('\\\\'):assert expression(row.split('=')[1])==sp.ImmutableMatrix([-49,48])
    records=[];counts={};families={};positions=set();slotcoverage={};hard_positions=set()
    for level in g.SUPPORTED_LEVELS:
        fps=set();family=set()
        for seed in range(400):
            record=g.generate(level,seed);check(record);fps.add(record['generation']['mathematical_fingerprint']);family.add(record['generation']['template'])
            m=record['generation']
            if level=='hard':
                hard_positions.update((name,index) for name in ('a','b') for index,value in enumerate(m['parameters'][name]) if sp.Rational(value).q==2)
                assert abs(sp.Rational(m['parameters']['k'])) in (3,5)
            slots=slotcoverage.setdefault(m['template'],{})
            for slot,val in m['parameters'].items():
                for i,item in enumerate(val if isinstance(val,list) else [val]):slots.setdefault(slot+str(i),set()).add(item)
            q=record['question'];f=q[':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            if seed<75:records.append(record)
        assert len(fps)>370,(level,len(fps))
        assert family=={t for t,l in g.TEMPLATES.items() if l==level}
        counts[level]=len(fps);families[level]=sorted(family)
    assert positions==set(range(5));assert hard_positions=={('a',0),('a',1),('b',0),('b',1)}
    # Move the half to every eligible slot with all remaining mathematical data fixed.
    for name,index in sorted(hard_positions):
        params={'a':[4,7],'b':[-6,2],'k':3};params[name][index]='5/2'
        check(g.generate_hard(parameters=params))
    for record in completed+records:
        check(record)
        m=record['generation'];params=m['parameters']
        other=g.generate(m['difficulty_design'],seed=m['seed']+997,template=m['template'],profile=m['bank_profile'],parameters=params)
        assert other['question'][':question/id']==record['question'][':question/id']
        assert other['generation']['mathematical_fingerprint']==m['mathematical_fingerprint']
    # Explicit level guard and complete-bank collision probes; never silently alter input.
    bad=[('moderate','linear',{'a':[2,3],'b':[1,2],'k':1}),('hard','fractional_linear',{'a':[2,3],'b':[1,2],'k':2}),('moderate','linear',{'a':[2,'3/2'],'b':[1,2],'k':2}),('easy','sum',{'a':[2,3],'b':[2,1]})]
    for level,template,p in bad:
        try:g.generate(level,template=template,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('invalid input accepted',p))
    # Signed boundary inputs for each family, independently read from the output.
    for level,template,p in [('easy','scalar',{'a':[-15,'-29/2'],'k':5}),('easy','subtract',{'a':[-15,14],'b':[13,-12]}),('moderate','linear',{'a':[-15,14],'b':[13,-12],'k':-5})]:check(g.generate(level,template=template,parameters=p))
    # Inverse coefficient/vector scaling aliases cannot inflate task variety.
    alias_a=g.generate_moderate(parameters={'a':[-5,7],'b':[2,-4],'k':3})
    alias_b=g.generate_moderate(parameters={'a':[-5,7],'b':[3,-6],'k':2})
    assert alias_a['generation']['mathematical_fingerprint']==alias_b['generation']['mathematical_fingerprint']
    assert alias_a['question'][':question/id']!=alias_b['question'][':question/id']
    # Negative controls retain final keys and conclusory row.
    negative_controls=[]
    base=g.generate_moderate(parameters={'a':[-5,7],'b':[2,-4],'k':3})
    for name,old,new in [('operative_intermediate','⟨6,-12⟩','⟨7,-12⟩'),('initial_operand','⟨2,-4⟩','⟨3,-4⟩'),('removed_component_stage','⟨-5 + 6, 7 + (-12)⟩','⟨1,-5⟩'),('control_character',r'\begin{aligned}',r'\begin{aligned}'+chr(12))]:
        mutant=copy.deepcopy(base);sol=mutant['question'][':question/worked-solution'];assert old in sol,(name,sol);mutant['question'][':question/worked-solution']=sol.replace(old,new,1)
        assert mutant['question'][':question/answer-fields']==base['question'][':question/answer-fields']
        try:check(mutant)
        except (AssertionError,ValueError,TypeError):negative_controls.append(name)
        else:raise AssertionError(('negative control escaped',name))
    # Native grader tests only complete normal fields; raw sources lack a designation.
    native=[]
    for i,record in enumerate(completed+records):
        f=record['question'][':question/answer-fields'][0]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual choice selection; displayed math independently read back'} for a in f[':answer-field/choices']]
        native.append({'label':f'completed-or-generated-{i}','record':record,'checks':checks})
    save('engine-input.json',native)
    engine=HERE/'check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    review=[]
    for template,level in g.TEMPLATES.items():
        for seed in (32,77):review.append(g.generate(level,seed,template=template))
    save('review.json',review)
    lines=['# Angle bracket vector review','', 'Original evidence is fieldless or lacks original correct designations. Generated completions are explicitly inferred/authored; raw replay preserves those omissions.','']
    for case,record,normal in zip(cases,raw,completed,strict=True):
        orig=sources[case['source_id']];lines+=['## Original '+case['source_id'],'',orig[':question/problem'],'']
        for f in orig.get(':question/answer-fields',[]):lines += ['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
        lines+=['',orig.get(':question/worked-solution','Worked solution absent.'),'','### Parameterized raw public replay','',g.markdown(record),'','### Inferred completed original parameters','',g.markdown(normal),'']
    for record in review:lines+=['## Clearly labeled generated variant','',g.markdown(record),'']
    (HERE/'review.md').write_text('\n'.join(lines))
    result={'status':'checks passed; pending independent root QA','database_writes':0,'source':g.SOURCE,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':importlib.metadata.version('matplotlib'),'renderer_used':None},'fidelity':{'practice_sources':4,'exact_prompts':'4/4','attribute_presence_parity':'4/4','complete_banks':'2/2','displayed_choices':'10/10','observed_distractors_with_independently_inferred_correct':'8/8','original_correct_designations':'0/0 (all absent; none claimed matched)','worked_solutions':'2/2','mathematical_repairs':0,'source_format_completions':4,'sources':fidelity},'independent_displayed_math_checks':1200+len(raw)+len(completed)+len(records)+3+1+len(hard_positions)+len(nonma),'meaningful_unique_tasks_in_400_seeds':counts,'default_family_coverage':families,'native':json.loads((HERE/'engine-report.json').read_text()),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'independent_inventory_exact_records':len(nonma),'canonical_equalities':4,'slot_coverage':{f:{k:sorted(v) for k,v in slots.items()} for f,slots in slotcoverage.items()},'hard_half_position_coverage':[list(x) for x in sorted(hard_positions)],'target_roles':'All requested results are complete vectors; ordered supplied coordinate pairs are eligible numerical slots. There is no selectable cell/point/subtarget in this KP.','negative_controls':negative_controls,'limitations':['Unrated source levels are authored assignments, not recovered labels.','Missing original correct refs prevent original designation fidelity/native grading; completed fixtures are tested separately.','Original widget has no q1301/q1389; their frozen EDB prompts/solutions remain primary evidence.','Source distractor operations faithfully replay all values but their pedagogical intent is inferred.','Moderate is authored assignment of observed one-scaled-vector integer work. Hard is authored half-integer same-method workload, with no observed MA hard labels.']}
    manifest=json.loads((HERE/'reference/grader-build.json').read_text());artifacts={manifest['source']:manifest['source_sha256'],manifest['library']:manifest['library_sha256'],manifest['binary']:manifest['binary_sha256']}|manifest['engine_sources']|manifest['dependencies']
    assert len(artifacts)==42
    for path,sha in artifacts.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    assert hashlib.sha256((HERE/'check-engine').read_bytes()).hexdigest()==manifest['binary_sha256']
    result['current_native_artifact_hashes_verified']=42
    baseline=json.loads((HERE/'registered-baseline.json').read_text());base=HERE.parent;kp=str(g.KP_ID)
    paths=[base/(kp+'.py')]+list((base/kp).rglob('*'))+list((base/'__pycache__').glob(kp+'.*.pyc'))
    current={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths if x.is_file()}
    assert current==baseline,'Registered pathset or hashes changed'
    result['registered_baseline_unchanged']=True;result['registered_baseline_file_count']=len(baseline)
    cli=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--format','json'],check=True,capture_output=True,text=True)
    assert isinstance(json.loads(cli.stdout),list) and len(json.loads(cli.stdout))==3
    (HERE/'cli-all.json').write_text(cli.stdout);result['cli_all_count1_records']=3
    save('validation.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('native',)},indent=2))

if __name__=="__main__": main()
