#!/usr/bin/env python3
"""Independent source coverage, actual printed stages and native grader audit."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,re,subprocess,hashlib,itertools,copy,collections
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)
PARAMS=[{'c':1,'n':2},{'c':1,'n':2},{'b':3},{'k':2},{'c':1},{'c':1},{'c':1},{'c':1,'k':2},{'c':2,'n':2},{'c':1}]
CASES=[{'source_id':t,'template':t,'level':'easy','parameters':p,'bank_profile':'observed_raw'} for t,p in zip(g.SOURCES,PARAMS)]

def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def equal(a,b):assert g.equivalent(a,b),(a,b)
def format_check(text):
    assert not any(ord(c)<32 and c not in '\n\t' for c in text), 'Unintended C0'
    assert text.count('$')%2==0
    braces=0
    for c in re.sub(r'\\[{}]','',text):
        if c=='{':braces+=1
        if c=='}':braces-=1
        assert braces>=0
    assert braces==0
    assert '--' not in text and '+-' not in text

def readback(record,check_identity=True):
    q=record['question'];meta=record['generation']; t=meta['template']
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    prompt=q[':question/problem'];sol=q[':question/worked-solution']
    format_check(prompt);format_check(sol)
    # Product comes from actual first prompt math, not hidden parameters.
    printed=re.search(r'\$(.*?)\$',prompt,re.S).group(1).rstrip('.')
    product=g.parse(printed);expected=s.diff(product,g.X)
    uv=re.search(r'\$u\(x\)=(.*?)\$ and \$v\(x\)=(.*?)\$',sol,re.S)
    assert uv,(t,sol)
    u,v=(g.parse(z.rstrip('.')) for z in uv.groups());equal(u*v,product)
    env={'u':u,'v':v}
    aligned=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
    rows=re.split(r'\\\\',aligned)
    assert len(rows)==4,(t,len(rows))
    lhs=rows[0].split('&')[0].strip()
    bad_raw=t=='q-319350' and meta['profile']=='observed_raw'
    if not bad_raw:equal(g.parse(lhs,env),expected)
    else:assert not g.equivalent(g.parse(lhs,env),expected)
    # All four printed stages independently parse, including rule references,
    # differentiated component expansion, evaluated factors, and distribution.
    for row in rows:
        rhs=row.split('&')[1].strip().lstrip('=').strip(); equal(g.parse(rhs,env),expected)

    # Preserve actual ordered product-rule operations, not just equal row totals.
    first_three=[row.split('&')[1].strip().lstrip('=').strip() for row in rows[:3]]
    for index,rhs in enumerate(first_three):
        terms=split_sum(rhs)
        assert len(terms)==2,(t,index,terms)
        equal(g.parse(terms[0],env),s.diff(u,g.X)*v)
        equal(g.parse(terms[1],env),u*s.diff(v,g.X))
        if index<2:
            assert g.norm(rhs).count("'")==2,(t,index,rhs)
            assert rhs.count(r'\cdot')==2,(t,index,rhs)
        else:
            assert "'" not in g.norm(rhs)
    if t not in g.SOURCES:
        expanded=g.parse(rows[-1].split('&')[1].strip().lstrip('=').strip(),env)
        assert len(s.Add.make_args(expanded))==(3 if t=='binomial' else 6),(t,expanded)
    assert 'Therefore' not in sol # no unvalidated separate source conclusion exists.

    field=q[':question/answer-fields'][0]
    correct_ref=field[':answer-field/correct'][1]
    ids=[a[':answer/id'] for a in field[':answer-field/choices']]
    assert len(ids)==len(set(ids)) and correct_ref in ids
    raw=g.QUESTIONS.get(t,{})
    profile=meta['profile']
    presence=[profile!='observed_raw' or key in raw for key in (':question/difficulty',':question/worked-solution',':question/answer-fields')]
    originals=raw.get(':question/answer-fields',[])
    correct_present=profile!='observed_raw' or bool(originals and ':answer-field/correct' in originals[0])
    identity=hashlib.sha256(json.dumps([g.VERSION,q[':question/difficulty'].split('/')[-1],prompt,sol,field[':answer-field/type'].split('/')[-1],sorted(a[':answer/value'] for a in field[':answer-field/choices']),presence,correct_present],sort_keys=True).encode()).hexdigest()
    if check_identity:assert identity==meta['content_hash']
    values=[g.parse(a[':answer/value']) for a in field[':answer-field/choices']]
    if field[':answer-field/type'].endswith('blank'):
        assert '{{'+field[':answer-field/key']+'}}' in prompt
        partial=re.search(r'\$([^$]*?)=([^$]*)\$\s*\{\{field-1\}\}(?:\s*\$([^$]*)\$)?',prompt,re.S)
        assert partial,(t,prompt)
        lhs,rhs,after=partial.groups(); lhs=lhs.strip()
        # f'(x) is just an authored requested full derivative.
        lhs_value=expected if lhs=="f'(x)" else g.parse(lhs)
        equal(lhs_value,expected)
        before=rhs.strip().rstrip('+').strip()
        tail=(after or '').strip().replace(r'\,','')
        if tail.startswith('+'):before=before+'+'+str(0) if before else ''
        full=g.parse(before) if before else s.Integer(0)
        if tail:full+=g.parse('('+field[':answer-field/choices'][0][':answer/value']+')'+tail)
        else:full+=values[0]
        equal(full,expected)
        assert len(values)==1
    else:
        assert len(values)==5
        for i,a in enumerate(values):
            correct=field[':answer-field/choices'][i][':answer/id']==correct_ref
            assert g.equivalent(a,expected)==correct
            for b in values[i+1:]:assert not g.equivalent(a,b)
    return values

def engine_entry(record,label):
    field=record['question'][':question/answer-fields'][0];checks=[]
    for a in field[':answer-field/choices']:
        if field[':answer-field/type'].endswith('radio'):
            checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Every displayed radio option'})
        else:
            answer=g.parse(a[':answer/value']);expanded=s.expand(answer);factored=s.factor(answer)
            if expanded!=answer:equivalent=g.tex(expanded)
            elif factored!=answer:equivalent=g.tex(factored)
            elif answer.has(s.sec(g.X)):
                equivalent=g.tex(answer.xreplace({s.sec(g.X)**2:1+s.tan(g.X)**2}))
            else:equivalent='('+g.tex(answer)+')*('+r'\sin^2(x)+\cos^2(x)'+')'
            checks.extend([{'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical exact fragment'}, {'submitted':equivalent,'expected':'accepted','purpose':'Uncollected/factored or trig-identity equivalent entry'}, {'submitted':g.tex(answer+1),'expected':'rejected','purpose':'Incorrect shifted fragment'}])
    return {'label':label,'record':record,'checks':checks}


def split_sum(text):
    depth=0;parts=[];start=0
    for i,c in enumerate(text):
        if c in '({':depth+=1
        elif c in ')}':depth-=1
        elif c=='+' and depth==0:parts.append(text[start:i]);start=i+1
    parts.append(text[start:]);return parts

def baseline():
    base=HERE.with_name(str(g.KP_ID));files=[base.with_suffix('.py')]+sorted(p for p in base.rglob('*') if p.is_file())+sorted((base.parent/'__pycache__').glob(str(g.KP_ID)+'.*.pyc'))
    return {str(p.relative_to(Path.cwd())):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def verify_native():
    b=Path('generate/scratch/17592186059716-draft/reference/grader-build.json');d=json.loads(b.read_text());mapping={d['source']:d['source_sha256'],d['library']:d['library_sha256'],d['binary']:d['binary_sha256'],**d['engine_sources'],**d['dependencies']}
    for path,sha in mapping.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha,path
    assert len(mapping)==42
    save('native-build-verification.json',{'build_record':str(b),'build_record_sha256':hashlib.sha256(b.read_bytes()).hexdigest(),'verified_hashes':len(mapping),'binary':d['binary'],'binary_sha256':d['binary_sha256']})
    return d['binary']

def raw_check(record,raw,case):
    q=record['question'];assert record['generation']['evidence_only'] and not record['generation']['eligible_for_learning']
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
        assert (key in q)==(key in raw),(case['source_id'],key)
    for f,o in zip(q.get(':question/answer-fields',[]),raw.get(':question/answer-fields',[])):
        assert (':answer-field/correct' in f)==(':answer-field/correct' in o)
        assert f[':answer-field/key']==o[':answer-field/key'] and f[':answer-field/type']==o[':answer-field/type'][':db/ident']
        vals=[g.parse(a[':answer/value']) for a in f[':answer-field/choices']];orig=[g.parse(a[':answer/value']) for a in o[':answer-field/choices']]
        assert len(vals)==len(orig)
        for value in orig:assert sum(g.equivalent(value,v) for v in vals)==1
        if ':answer-field/correct' in o:
            actual=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            equal(g.parse(actual[':answer/value']),g.parse(o[':answer-field/correct'][':answer/value']))
    assert q[':question/problem']==g.normalize_prose(g.masked(raw[':question/problem'],g.source_data(case['template'],case['parameters'])[2]))
    if ':question/worked-solution' in raw:
        expected=g.normalize_prose(g.masked(raw[':question/worked-solution'],g.source_data(case['template'],case['parameters'])[2]))
        assert q[':question/worked-solution']==expected


def raw_bank_readback(record):
    """Read product from public prompt; audit every raw complete bank at changed inputs."""
    q=record['question'];name=record['generation']['template'];prompt=q[':question/problem']
    product=g.parse(re.search(r'\$(.*?)\$',prompt,re.S).group(1).rstrip('.'));derivative=s.diff(product,g.X)
    for f in q.get(':question/answer-fields',[]):
        vals=[g.parse(a[':answer/value']) for a in f[':answer-field/choices']]
        for i,a in enumerate(vals):
            for b in vals[i+1:]:assert not g.equivalent(a,b)
        if f[':answer-field/type'].endswith('radio'):
            assert sum(g.equivalent(a,derivative) for a in vals)==1
            if ':answer-field/correct' in f:
                chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);equal(g.parse(chosen[':answer/value']),derivative)
            if name=='q-47965':
                # Recover polynomial degree/coefficient from the printed prompt,
                # independently of metadata and generator recipes.
                polynomial=s.simplify(product/s.tan(g.X));n=s.degree(polynomial,g.X);c=s.Poly(polynomial,g.X).LC();du=s.diff(polynomial,g.X);x=g.X
                expected=[du+polynomial*s.sec(x)*s.tan(x),c*x**(n-1)*s.tan(x)*(n*x+s.sec(x)),du*s.sec(x)*s.tan(x),du*s.tan(x)+polynomial*s.sec(x)**2,s.sec(x)*(n*c+polynomial*s.tan(x))]
                assert all(sum(g.equivalent(a,b) for b in vals)==1 for a in expected)
        else:
            partial=re.search(r'\$([^$]*?)=([^$]*)\$\s*\{\{field-1\}\}(?:\s*\$([^$]*)\$)?',prompt,re.S);assert partial
            lhs,before,tail=partial.groups();equal(g.parse(lhs),derivative)
            before=before.strip().rstrip('+').strip();tail=(tail or '').strip().replace(r'\,','')
            full=g.parse(before) if before else s.Integer(0)
            full+=g.parse('('+f[':answer-field/choices'][0][':answer/value']+')'+tail) if tail else vals[0]
            equal(full,derivative)
    return sum(len(f[':answer-field/choices']) for f in q.get(':question/answer-fields',[]))

def run():
    assert baseline()==json.loads((HERE/'registered-baseline.json').read_text())['files']
    native=verify_native();save('source-cases.json',CASES)
    provenance={k:g.CAPTURE[k] for k in ('database','basis','lineage')}
    assert (HERE/'source.json').read_bytes()==Path('generate/runs/current/sources/'+str(g.KP_ID)+'.json').read_bytes()
    canonical=g.CAPTURE['record'][':knowledge-point/canonical-example'];save('canonical-example.json',{'source':provenance,'role':'canonical example, not practice','record':canonical})
    save('independent-inventory.json',{**provenance,'questions':[]})
    review=[];engine=[];variants=[];readbacks=0;raw_bank_values=0;fingerprints={l:set() for l in ('easy','moderate','hard')};slots={};default_families={};source_values=0;refs=0;exact_prompts=0;exact_solutions=0;normal_prose=0
    for case in CASES:
        t=case['template'];print('source',t,flush=True);raw=g.QUESTIONS[t]
        replay=g.generate('easy',seed=3,template=t,parameters=case['parameters'],profile='observed_raw');raw_check(replay,raw,case);raw_bank_values+=raw_bank_readback(replay)
        normal=g.generate('easy',seed=3,template=t,parameters=case['parameters']);readback(normal);readbacks+=1
        if ':question/worked-solution' in raw:
            expected=g.normalize_prose(g.masked(raw[':question/worked-solution'],g.source_data(t,case['parameters'])[2]))
            if t=='q-319350':expected=expected.replace('({e}^{x}sec⁡(x))','({e}^{x}(2+sin⁡(x)))',1)
            assert normal['question'][':question/worked-solution']==expected
            normal_prose+=1
        source_values+=sum(len(f[':answer-field/choices']) for f in raw.get(':question/answer-fields',[]));refs+=sum(':answer-field/correct' in f for f in raw.get(':question/answer-fields',[]))
        exact_prompts+=replay['question'][':question/problem']==raw[':question/problem']
        exact_solutions+=bool(raw.get(':question/worked-solution')) and replay['question'].get(':question/worked-solution')==raw.get(':question/worked-solution')
        review.append({'source_id':t,'original':raw,'raw_replay':replay,'normal_repair':normal})
        variants.append(normal);engine.append(engine_entry(normal,t+' original parameters normal'))
    for level,templates in [('easy',g.SOURCES),('moderate',('binomial',)),('hard',('affine_trig',))]:
        familycounts=collections.Counter()
        for seed in range(120):
            record=g.generate(level,seed=seed);familycounts[record['generation']['template']]+=1
        assert set(familycounts)==set(templates);default_families[level]=dict(familycounts)
        for t in templates:
            print('variants',level,t,flush=True);seen=collections.defaultdict(set)
            for seed in range(12):
                record=g.generate(level,seed=seed,template=t);readback(record);readbacks+=1
                fingerprints[level].add(record['generation']['mathematical_fingerprint'])
                p=record['generation']['parameters'];again=g.generate(level,seed=999,template=t,parameters=p)
                assert again['question'][':question/id']==record['question'][':question/id']
                assert again['generation']['mathematical_fingerprint']==record['generation']['mathematical_fingerprint']
                for key,value in p.items():seen[key].add(value)
                if seed<2:variants.append(record);engine.append(engine_entry(record,level+' '+t+' '+str(seed)))
                if level=='easy':
                    # Changed raw profiles preserve key omissions, prose and source
                    # operative masks; normal readback validates every displayed row.
                    raw=g.QUESTIONS[t];rp=g.generate(level,seed=seed,template=t,parameters=p,profile='observed_raw');raw_bank_values+=raw_bank_readback(rp)
                    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in rp['question'])==(key in raw)
                    if ':question/worked-solution' in raw:assert rp['question'][':question/worked-solution']==g.normalize_prose(g.masked(raw[':question/worked-solution'],g.source_data(t,p)[2]))
            slots[level+' '+t]={k:sorted(v) for k,v in seen.items()}
            assert all(len(v)>1 for v in seen.values())
        if level!='easy':
            for trig in g.TRIG:
                for kind,p in [('radio',{'a':2,'b':-3,'n':3,'trig':trig}),('blank',{'a':-4,'b':2,'n':4,'trig':trig})]:
                    if level=='hard':p['d']=-2 if kind=='radio' else 3
                    record=g.generate(level,seed=44,parameters=p,field_type=kind);readback(record);readbacks+=1;variants.append(record);engine.append(engine_entry(record,level+' '+trig+' '+kind))
    # Held-other-slots-fixed coverage through independently read actual displays.
    held=[]
    for level,t,p in [('easy',c['template'],c['parameters']) for c in CASES]+[('moderate','binomial',{'a':2,'b':-3,'n':3,'trig':'sin'}),('hard','affine_trig',{'a':2,'b':-3,'n':3,'trig':'sin','d':2})]:
        for key in p:
            other=dict(p);other[key]=('cos' if p[key]=='sin' else 'sin') if key=='trig' else (p[key]+1 if p[key]<4 else p[key]-1)
            a=g.generate(level,template=t,parameters=p);b=g.generate(level,template=t,parameters=other);readback(b);readbacks+=1
            assert a['question'][':question/problem']!=b['question'][':question/problem'];assert a['generation']['mathematical_fingerprint']!=b['generation']['mathematical_fingerprint']
            held.append({'level':level,'template':t,'slot':key,'from':p[key],'to':other[key]})
    badcases=[('easy','q-1907',{'c':0,'n':2}),('moderate','binomial',{'a':1,'b':0,'n':2,'trig':'sin'}),('hard','affine_trig',{'a':-5,'b':1,'d':2,'n':2,'trig':'sin'})]
    for level,t,p in badcases:
        try:g.generate(level,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Out-of-scope input admitted')
    mutations=[]
    base=g.generate('hard',parameters={'a':2,'b':-3,'n':3,'trig':'cos','d':2})
    for label,change in [('C0',lambda text:text+'\x0c'),('wrong-sign-distribution',lambda text:text.replace('12 x^{2}', '13 x^{2}')),('drop-operative-derivative',lambda text:text.replace("u'(x)\\cdot v(x)+u(x)\\cdot v'(x)",g.tex(s.diff(g.parse(re.search(r'\$(.*?)\$',base['question'][':question/problem']).group(1).rstrip('.')),g.X))))]:
        record=copy.deepcopy(base);before=record['question'][':question/worked-solution'];after=change(before)
        assert before!=after,label;record['question'][':question/worked-solution']=after
        try:readback(record,check_identity=False)
        except (AssertionError,ValueError):mutations.append(label)
        else:raise AssertionError('Mutation passed '+label)

    record=copy.deepcopy(base);sol=record['question'][':question/worked-solution'];aligned=re.search(r'\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1);parts=re.split(r'\\\\',aligned);parts[-1]=parts[-2]
    record['question'][':question/worked-solution']=sol.replace(aligned,r' \\ '.join(parts))
    try:readback(record,check_identity=False)
    except (AssertionError,ValueError):mutations.append('equal-but-undistributed-final-row')
    else:raise AssertionError('Operative distribution mutation passed')
    original_solution=g.solution
    try:
        g.solution=lambda u,v:original_solution(u,v)+'\x0c'
        try:g.generate('moderate',seed=1)
        except ValueError:mutations.append('generator-C0-guard')
        else:raise AssertionError('Public generator admitted C0')
    finally:g.solution=original_solution

    save('review.json',{'sources':review,'generated_variants':variants});save('engine-input.json',engine)
    subprocess.run([native,str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    native_report=json.loads((HERE/'engine-validation.json').read_text())
    assert baseline()==json.loads((HERE/'registered-baseline.json').read_text())['files']
    result={'pass':True,'approval':'pending root independent QA','generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'source_provenance':provenance,'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'original_MA_practice':10,'independent_inventory':0,'canonical_examples':1,'source_choice_values_matched':source_values,'complete_banks_matched':9,'correct_designations_matched':refs,'missing_designations_preserved_raw':2,'fieldless_preserved_raw':1,'source_key_presence_cases':10,'raw_exact_prompts':exact_prompts,'raw_exact_existing_solutions':exact_solutions,'normal_ordered_existing_solution_prose':normal_prose,'normal_corrected_LHS':1,'opaque_observed_bank_evidence_only':'q-47965','normal_opaque_bank_replacement':'complete authored method-derived bank','changed_and_original_raw_bank_values_read_back':raw_bank_values,'independent_display_readbacks':readbacks,'held_slots':held,'default_family_coverage':default_families,'slot_coverage':slots,'sample_mathematical_fingerprints':{k:len(v) for k,v in fingerprints.items()},'mutation_rejections':mutations,'native':native_report,'registered_baseline_unchanged_files':len(baseline()),'python':sys.version.split()[0],'sympy':s.__version__,'plots':0,'limitations':['Moderate/hard are authored same-KP scope judgments, not observed labels.','Only sampled bounded combinations are mathematically read back; explicit guards apply to all inputs.','q-47965 peculiar historical choices retain unresolved intended-error interpretation and remain raw evidence.'],'database_writes':0}
    save('validation.json',result)
    lines=['# Product-rule trig review','Original Math Academy practice; exact basis1356 wrapper retained. Raw evidence may lack fields, labels, keys or solutions. Normal repairs are separate.']
    for item in review:
        lines+=['## Original '+item['source_id'],item['original'][':question/problem'],item['original'].get(':question/worked-solution','No source solution.'),'Original complete bank:']+[a[':answer/value'] for f in item['original'].get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
        lines+=['### Normal completed/repaired instance',item['normal_repair']['question'][':question/problem'],item['normal_repair']['question'][':question/worked-solution']]
    for record in variants:
        q=record['question'];lines+=['## Generated '+record['generation']['template']+' '+q[':question/difficulty'],q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    (HERE/'review.md').write_text('\n\n'.join(lines)+'\n');print(json.dumps({k:result[k] for k in ['pass','source_choice_values_matched','complete_banks_matched','independent_display_readbacks','sample_mathematical_fingerprints']},indent=2))
if __name__=='__main__':run()
