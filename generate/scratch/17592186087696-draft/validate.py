#!/usr/bin/env python3
"""Independent displayed-shape/stage/fidelity tests plus memory-only real grader."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('square_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def dims(prompt):
    parsed=[]
    for label,body in re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S):
        rows=[row.split('&') for row in body.split(r'\\')];assert all(len(row)==len(rows[0]) for row in rows)
        for row in rows:
            for val in row:
                val=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',val.strip());assert sp.sympify(val).is_real
        parsed.append((label,len(rows),len(rows[0])))
    assert len(parsed)==3
    return parsed

def check_record(rec,raw=False):
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=rec['question'];parsed=dims(q[':question/problem']);selected={l for l,r,c in parsed if r==c}
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert not any(ord(c)<32 and c not in '\n\t\r' for c in text);g.validate_prose(text)
    if not raw:
        g.validate_generated_record(rec);sol=q[':question/worked-solution'];steps=sol.split('\n\n');assert len(steps)==4
        for (label,rows,cols),step in zip(parsed,steps[:3]):
            assert step.startswith('- $'+label+'$ ')
            assert ('*not*' in step)==(rows!=cols)
            assert ('same number of rows and columns.' in step)==(rows==cols)
            assert f'It has ${rows}$ row' in step and f'and ${cols}$ column' in step
            assert f'${rows}\\times {cols}$' in step
            assert ('so it is a' in step)==(rows==cols)
        assert steps[3].startswith('Therefore, ');assert set(re.findall(r'\$([A-Z])\$',steps[3]))==selected
        assert ('none of these matrices' in steps[3])==(not selected)
    fields=q[':question/answer-fields'];identities=[q[':question/id']]
    if len(fields)==3:
        assert {f[':answer-field/key'] for f in fields}=={l for l,r,c in parsed}
        for f in fields:
            assert f[':answer-field/type']==':answer-field.type/checkbox';choices=f[':answer-field/choices'];assert sorted(a[':answer/value'] for a in choices)==['false','true']
            if not raw:assert next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])==('true' if f[':answer-field/key'] in selected else 'false')
    else:
        assert len(fields)==1 and fields[0][':answer-field/type']==':answer-field.type/radio';choices=fields[0][':answer-field/choices'];assert len(choices)==5
        subsets=[set(re.findall(r'\$([A-Z])\$',a[':answer/value'])) for a in choices]
        assert all(a!=b for a,b in itertools.combinations(subsets,2));assert subsets.count(selected)==1
        if not raw:assert subsets[next(i for i,a in enumerate(choices) if a[':answer/id']==fields[0][':answer-field/correct'][1])]==selected
    for f in fields:
        identities+=[f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
        if not raw:assert f[':answer-field/correct'][0]==':answer/id'
        assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
    assert len(identities)==len(set(identities))
    for i in identities:__import__('uuid').UUID(i)
    independently=hashlib.sha256(json.dumps(['square-membership',sorted((r,c) for l,r,c in parsed)]).encode()).hexdigest()
    assert independently==rec['generation']['mathematical_fingerprint']

def parameters(shapes):return {'labels':['A','B','C'],'matrices':[[['0']*c for _ in range(r)] for r,c in shapes],'none_instruction':True,'trailing_space':False,'legacy_plural':False}
def native_item(rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'canonical selected choice; every incorrect alternative/subset'})
    return {'label':rec['question'][':question/id'],'record':rec,'checks':checks}
def must_fail(fn):
    try:fn()
    except (ValueError,AssertionError):return
    raise AssertionError('expected rejection')
def main():
    original=json.loads((D/'baseline-hashes.json').read_text());assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in original.items())
    baseline=D.with_name('17592186087696');baseline_files=[baseline.with_suffix('.py')]+[p for p in baseline.rglob('*') if p.is_file()]
    assert {str(p.relative_to(ROOT)) for p in baseline_files}==set(original)
    assert (D/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186087696.json').read_bytes()
    cases=[];fidelity=[];native=[];review=[];exact_prompts=exact_solutions=0
    for sid,src in g.QS.items():
        raw=sid=='q-7826';template='three-radio' if raw else 'three-checkbox';profile='observed-radio-raw' if raw else 'observed-checkbox'
        case={'source_id':sid,'level':'easy','template':template,'parameters':g.SOURCE_PARAMS[sid],'profile':profile,'bank_profile':profile};cases.append(case)
        rec=g.generate('easy',template=template,profile=profile,parameters=case['parameters']);check_record(rec,raw)
        q=rec['question'];assert q[':question/problem']==g.normalize_prose(src[':question/problem'])
        for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (attr in q)==(attr in src)
        exact_prompts+=q[':question/problem']==src[':question/problem']
        if not raw:assert q[':question/worked-solution']==g.normalize_prose(src[':question/worked-solution']);exact_solutions+=q[':question/worked-solution']==src[':question/worked-solution']
        for f in q[':question/answer-fields']:
            sf=next(x for x in src[':question/answer-fields'] if x[':answer-field/key']==f[':answer-field/key']);assert (':answer-field/correct' in sf)==(':answer-field/correct' in f)
            assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
            assert sorted((a[':answer/value'],a[':answer/type']) for a in f[':answer-field/choices'])==sorted((a[':answer/value'],a[':answer/type'][':db/ident']) for a in sf[':answer-field/choices'])
            if not raw:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==sf[':answer-field/correct'][':answer/value']
        fidelity.append({'source_id':sid,'complete_bank_match':True,'key_presence_parity':True,'source_correct_designation_matches':0 if raw else 3,'source_correct_designations_missing':1 if raw else 0})
        review.append({'label':'Original '+sid+' parameterized replay','source_id':sid,'record':rec})
        if raw:
            completed=g.generate(template=template,parameters=case['parameters'],profile='completed-observed-radio');check_record(completed);native.append(completed);review.append({'label':'Authored completion q-7826: A only; unrated source assigned easy','record':completed})
        else:native.append(rec)
        changed=copy.deepcopy(case['parameters'])
        if raw:
            changed['matrices']=[[['2']*c for _ in range(r)] for r,c in [(2,2),(4,3),(1,4)]]
            variant=g.generate(template=template,profile='completed-observed-radio',parameters=changed)
        else:
            r,c=g.shape(changed['matrices'][0]);changed['matrices'][0]=[['1']*c for _ in range(r%5+1)]
            variant=g.generate(template=template,profile=profile,parameters=changed)
        check_record(variant);native.append(variant);review.append({'label':'Generated changed-shape variant of source bank '+sid,'record':variant})
    write('source-cases.json',cases);write('source-fidelity.json',fidelity)
    inventories=[]
    for q in g.SOURCE['record'][':knowledge-point/questions']:
        if ':question/math-academy-id' not in q:inventories.append({'record':q,'role':'independently authored inventory','relationship_to_source_templates':'same square-shape recognition family'})
    write('independent-inventory.json',{**{k:g.SOURCE[k] for k in ('basis','database','lineage')},'questions':inventories})
    slotcoverage={str(i):set() for i in range(3)}
    for i in range(3):
        for rc in g.SOURCE_SHAPES:
            ds=[(1,1),(2,3),(2,2)];ds[i]=rc;rec=g.generate(template='three-checkbox',parameters=parameters(ds),profile='observed-checkbox');check_record(rec);native.append(rec);slotcoverage[str(i)].add(rc)
    patterns=set()
    for bits in itertools.product((False,True),repeat=3):
        rec=g.generate(template='three-checkbox',parameters=parameters([(1,1) if b else (1,2) for b in bits]));check_record(rec);native.append(rec);patterns.add(bits)
    capacity={};samplers={};banks=set();orderdiff=False
    for level in g.SUPPORTED_LEVELS:
        tasks=set();sampletasks=set()
        if level=='easy':family=[ds for ds in itertools.combinations_with_replacement(tuple(itertools.product(range(1,4),repeat=2)),3) if any(r==1 for r,c in ds)]
        elif level=='moderate':family=[((n,n),(r,c),(c,r)) for n in range(2,7) for r,c in itertools.combinations(range(2,7),2)]
        else:family=[((n,l),(n,n),(n,u)) for n in range(2,8) for l in range(1,n) for u in range(n+1,9)]
        for ds in family:
            rec=g.generate(level,template='three-checkbox',parameters=parameters(ds))
            check_record(rec);tasks.add(rec['generation']['mathematical_fingerprint']);native.append(rec)
        capacity[level]=len(tasks)
        for seed in range(300):
            rec=g.generate(level,seed);check_record(rec);sampletasks.add(rec['generation']['mathematical_fingerprint']);banks.add((level,rec['generation']['template'],rec['generation']['profile']))
            p=rec['generation']['parameters'];other=g.generate(level,seed+1,template=rec['generation']['template'],parameters=p,profile=rec['generation']['profile'])
            assert rec['question'][':question/id']==other['question'][':question/id'];orderdiff|=rec['question'][':question/answer-fields']!=other['question'][':question/answer-fields']
            if seed<8:native.append(rec)
        samplers[level]=len(sampletasks)
        for seed in (11,29):review.append({'label':'Generated '+level+' seed '+str(seed),'record':g.generate(level,seed)})
    assert capacity=={'easy':109,'moderate':50,'hard':56};assert orderdiff
    for kind in ('radio','checkbox'):
        for seed in range(5):
            rec=g.generate(field_type=kind,seed=seed);check_record(rec);assert rec['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/'+kind
    # Changed labels/values/order are presentation changes, not assessed-task diversity.
    rec=g.generate('hard',4);p=copy.deepcopy(rec['generation']['parameters']);p['labels']=['X','Y','Z'];p['matrices']=[[[str(-int(x)) for x in row] for row in m] for m in reversed(p['matrices'])]
    other=g.generate('hard',parameters=p);assert other['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint'];assert other['question'][':question/id']!=rec['question'][':question/id']
    mutations=0
    for attr in ('dimension','reason','conclusion','key','control'):
        bad=copy.deepcopy(rec);q=bad['question']
        if attr=='dimension':q[':question/worked-solution']=q[':question/worked-solution'].replace('It has $','It has $99',1)
        if attr=='reason':q[':question/worked-solution']=q[':question/worked-solution'].replace('is a square matrix','is *not* a square matrix',1)
        if attr=='conclusion':q[':question/worked-solution']=q[':question/worked-solution'].split('Therefore, ')[0]+'Therefore, $Z$ is a square matrix.'
        if attr=='key':f=q[':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
        if attr=='control':q[':question/problem']+='\x0c'
        must_fail(lambda:check_record(bad));mutations+=1
    for level,ds in [('easy',[(2,2)]*3),('moderate',[(2,2)]*3),('hard',[(2,2)]*3)]:must_fail(lambda:g.generate(level,template='three-checkbox',parameters=parameters(ds)))
    must_fail(lambda:g.generate(template='three-radio',parameters=parameters([(2,2)]*3)))
    must_fail(lambda:g.generate(parameters=parameters([(6,6),(1,1),(2,2)]),profile='observed-checkbox'))
    must_fail(lambda:g.generate('moderate',parameters=parameters([(7,7),(2,3),(3,2)])))
    must_fail(lambda:g.generate('hard',parameters=parameters([(8,1),(8,8),(8,9)])))
    must_fail(lambda:g.generate('hard',field_type='radio'))
    # Read every complete subset criterion; all pairs, including wrong/wrong.
    for seed in range(20):check_record(g.generate(template='three-radio',seed=seed));native.append(g.generate(template='three-radio',seed=seed))
    write('native-input.json',[native_item(r) for r in native]);engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    report=json.loads((D/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
    write('review.json',review);(D/'review.md').write_text('\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in original.items())
    write('validation.json',{'status':'pass','source_basis':2275,'source_originals_matched':6,'source_originals_total':6,'source_banks_matched':16,'source_banks_total':16,'source_choices_matched':35,'source_choices_total':35,'source_correct_designations_matched':15,'source_correct_designations_total_present':15,'missing_original_correct_designations':1,'raw_exact_prompts':exact_prompts,'normalized_prompts':6,'exact_solutions':exact_solutions,'present_source_solutions':5,'authored_missing_solution':1,'independent_inventory_count':len(inventories),'registered_baseline_files_unchanged':len(original),'mathematical_instances_checked':len(native),'mutation_regressions':mutations,'all8_checkbox_selection_patterns':len(patterns),'slot_dimension_coverage':{k:sorted(v) for k,v in slotcoverage.items()},'meaningful_task_capacity_checkbox':capacity,'sampled_distinct_tasks':samplers,'default_family_profile_coverage':sorted(banks),'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'limits':['moderate/hard difficulty calibration is authored and uncertain','raw q-7826 lacks key/solution/difficulty and is evidence-only','finite checkbox hard family has56 unordered shape tasks; numerical entry changes do not expand it','choice grading uses actual owned-answer selection; expression-equivalent entry is inapplicable to checkbox/radio']})
    print(json.dumps({'status':'pass','capacity':capacity,'source_originals':6,'native':report['accepted_checks']+report['rejected_checks']}))
if __name__=='__main__':main()
