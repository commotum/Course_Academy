#!/usr/bin/env python3
"""Independent source coverage, actual printed stages and native grader audit."""
import importlib.util,json,re,subprocess,hashlib,itertools,sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)
PARAMS=[{'c':1,'n':2},{'c':1,'n':2},{'b':3},{'k':2},{'c':1},{'c':1},{'c':1},{'c':1,'k':2},{'c':2,'n':2},{'c':1}]
CASES=[{'source_id':t,'template':t,'level':'easy','parameters':p,'bank_profile':'observed_raw'} for t,p in zip(g.SOURCES,PARAMS)]

def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def equal(a,b):assert g.equivalent(a,b),(a,b)
def format_check(text):
    assert text.count('$')%2==0
    braces=0
    for c in re.sub(r'\\[{}]','',text):
        if c=='{':braces+=1
        if c=='}':braces-=1
        assert braces>=0
    assert braces==0
    assert '--' not in text and '+-' not in text

def readback(record):
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
    field=q[':question/answer-fields'][0]
    correct_ref=field[':answer-field/correct'][1]
    ids=[a[':answer/id'] for a in field[':answer-field/choices']]
    assert len(ids)==len(set(ids)) and correct_ref in ids
    identity=hashlib.sha256(json.dumps([g.VERSION,q[':question/difficulty'].split('/')[-1],prompt,sol,field[':answer-field/type'].split('/')[-1],sorted(a[':answer/value'] for a in field[':answer-field/choices'])],sort_keys=True).encode()).hexdigest()
    assert identity==meta['content_hash']
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

def run():
    save('source-cases.json',CASES); source_review=[];bank_values=0;designation=0;exact_prompt=0;exact_solution=0;normalized_solution=0
    engine=[];generated=[];fingerprints={l:set() for l in ('easy','moderate','hard')}
    for case in CASES:
        print('Source',case['source_id'],flush=True)
        t=case['source_id'];raw=g.QUESTIONS[t]
        record=g.generate('easy',seed=3,template=t,parameters=case['parameters'],profile=case['bank_profile'])
        values=readback(record)
        sourcefields=raw.get(':question/answer-fields',[])
        if sourcefields:
            originals=[g.parse(a[':answer/value']) for a in sourcefields[0][':answer-field/choices']]
            assert len(originals)==len(values)
            for a in originals:assert sum(g.equivalent(a,b) for b in values)==1
            bank_values+=len(originals)
            if sourcefields[0].get(':answer-field/correct'):
                original=g.parse(sourcefields[0][':answer-field/correct'][':answer/value'])
                field=record['question'][':question/answer-fields'][0];a=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);equal(original,g.parse(a[':answer/value']));designation+=1
        if record['question'][':question/problem']==raw[':question/problem']:exact_prompt+=1
        if raw.get(':question/worked-solution'):
            if record['question'][':question/worked-solution']==raw[':question/worked-solution']:exact_solution+=1
            # Whole prose and ordered sequence fidelity under separately
            # documented component notation normalization.
            expected=g.masked(raw[':question/worked-solution'],g.source_data(t,case['parameters'])[2])
            assert record['question'][':question/worked-solution']==expected
            normalized_solution+=1
        source_review.append({'source_id':t,'original':raw,'generated_replay':record})
        # Raw known source LHS error is not used as a teaching default.
        repaired=g.generate('easy',template=t,parameters=case['parameters']);readback(repaired)
        engine.append(engine_entry(repaired,t+' source parameters repaired'))
    for level,templates in [('easy',g.SOURCES),('moderate',('binomial',)),('hard',('affine_trig',))]:
        for t in templates:
            print('Variants',level,t,flush=True)
            for seed in range(12):
                record=g.generate(level,seed=seed,template=t);readback(record);fingerprints[level].add(record['generation']['mathematical_fingerprint'])
                p=record['generation']['parameters'];copy=g.generate(level,seed=999,template=t,parameters=p)
                assert copy['question'][':question/id']==record['question'][':question/id']
                assert copy['generation']['mathematical_fingerprint']==record['generation']['mathematical_fingerprint']
                if seed<2:
                    generated.append(record);engine.append(engine_entry(record,level+' '+t+' '+str(seed)))
                # Explicit raw bank generalization on observed profiles.
                if level=='easy':readback(g.generate(level,template=t,parameters=p,profile='observed_raw'))
        if level!='easy':
            for seed in (2,3):
                record=g.generate(level,seed=seed,field_type='blank');readback(record);generated.append(record);engine.append(engine_entry(record,level+' blank '+str(seed)))
    # Explicit family coverage: two different signed instances of each primitive
    # trig function in each authored level, covering radio and full blank layouts.
    for level,t in [('moderate','binomial'),('hard','affine_trig')]:
        for trig in ('sin','cos','tan'):
            for kind,p in [('radio',{'a':2,'b':-3,'n':3,'trig':trig}),('blank',{'a':-4,'b':2,'n':4,'trig':trig})]:
                if level=='hard':p['d']=-2 if kind=='radio' else 3
                record=g.generate(level,seed=44,template=t,parameters=p,field_type=kind)
                readback(record);generated.append(record);fingerprints[level].add(record['generation']['mathematical_fingerprint'])
                engine.append(engine_entry(record,level+' explicit '+trig+' '+kind))
    # Bounds and malformed-input rejection share normal generator paths.
    for level,t,p in [('easy','q-1907',{'c':0,'n':2}),('moderate','binomial',{'a':1,'b':0,'n':2,'trig':'sin'}),('hard','affine_trig',{'a':-5,'b':1,'d':2,'n':2,'trig':'sin'})]:
        try:g.generate(level,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit scope input admitted')
    try:g.generate('hard',field_type='checkbox')
    except ValueError:pass
    else:raise AssertionError('Unsupported field layout admitted')
    save('review.json',{'sources':source_review,'generated_variants':generated})
    save('engine-input.json',engine)
    tool=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(tool),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    engine_report=json.loads((HERE/'engine-validation.json').read_text())
    result={'pass':True,'source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'practice_sources':10,'complete_source_banks_matched':9,'complete_radio_source_banks_matched':4,'source_blank_values_matched':5,'source_choice_values_matched':bank_values,'observed_correct_designations_matched':designation,'correct_designations_missing_repaired':2,'fieldless_sources_repaired':1,'raw_exact_prompts':exact_prompt,'raw_exact_existing_solutions':exact_solution,'component_notation_normalized_existing_solutions':normalized_solution,'source_solution_count':8,'source_mathematical_solution_error_preserved_raw':1,'normal_solutions_repaired':1,'generated_variants_reviewed':len(generated),'sample_cases_per_observed_template':12,'independent_displayed_record_readbacks':300,'seed_identity_checks':144,'meaningful_sample_fingerprints':{k:len(v) for k,v in fingerprints.items()},'bounded_parameter_domains':{'easy_presentations':126,'moderate_parameter_sets':576,'hard_parameter_sets':4608},'limitations':['No chain rule, composed trig, tangent slope, or plot families.','Moderate/hard difficulty levels are authored scope judgments, not observed labels.','The finite parameter-domain size is a design bound; only reported sampled fingerprints were independently validated.','q-47965 odd wrong expressions are generalized observed shapes; original author intent is not recoverable.'],'native_grader':engine_report,'engine_sha256':hashlib.sha256(tool.read_bytes()).hexdigest()}
    save('validation.json',result)
    review=['# Product-rule trig review','All originals below come from math basis 1356. Generated variants are labeled separately.']
    for item in source_review:
        raw=item['original'];q=item['generated_replay']['question'];review+=['## Original '+item['source_id'],raw[':question/problem'],raw.get(':question/worked-solution','No captured solution.'),'Original complete bank:']+[a[':answer/value'] for f in raw.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]+['### Parameterized observed replay',q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
    for r in generated:
        q=r['question'];review+=['## Generated '+r['generation']['template']+' '+q[':question/difficulty'],q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    # Freeze hashes last; validation itself and review are included.
    save('frozen-manifest.json',{'version':g.VERSION,'artifacts':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py')]+sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='frozen-manifest.json')}})
    print(json.dumps({k:result[k] for k in ('pass','source_choice_values_matched','observed_correct_designations_matched','raw_exact_prompts','raw_exact_existing_solutions','generated_variants_reviewed','meaningful_sample_fingerprints')},indent=2))
if __name__=='__main__':run()
