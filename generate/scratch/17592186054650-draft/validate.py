"""Independent readback of displayed operands, stages and complete owned banks.
No EDB reads/writes; check-engine uses actual application grading in memory.
"""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('matrix_add_draft',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
MX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def save(name,x): (HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def read_cells(body): return [[s.strip() for s in row.split('&')] for row in body.split(r'\\')]
def read_matrix(body): return sp.Matrix([[sp.sympify(s) for s in row] for row in read_cells(body)])
def read_matrices(text): return [read_matrix(s) for s in MX.findall(text)]
def flatten(matrix): return tuple(matrix)
def mask(text): return MX.sub('<MATRIX>',text)
def check_text(text,prose=True):
    assert all(ord(c)>=32 or c in '\n\t\r' for c in text),'C0 control character'
    (g.validate_prose if prose else g.validate_tex)(text)
    assert (g.normalize_prose(text) if prose else g.normalize_tex(text))==text,'Noncanonical math'

def check(r):
    q=r['question'];meta=r['generation'];t=meta['template'];raw=meta['raw_replay']
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==17592186054650
    uuid.UUID(q[':question/id']);check_text(q[':question/problem'])
    a,b=read_matrices(q[':question/problem']);assert a.shape==b.shape and a.shape in ((2,3),(3,2));assert a.rows!=a.cols
    c=a+b
    assert list(a)==meta['parameters']['a'] and list(b)==meta['parameters']['b']
    source=g.SOURCES[t];fs=q[':question/answer-fields']
    if raw:
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in q)==(key in source),'Raw key-presence mismatch'
    else:
        assert ':question/worked-solution' in q and ':question/difficulty' in q
    assert mask(q[':question/problem'])==mask(source[':question/problem'])
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];check_text(sol)
        vals=read_matrices(sol);assert len(vals)==4,'Four matrices encode operand, expanded, evaluated stages'
        assert vals[0]==a and vals[1]==b and vals[2]==c and vals[3]==c,'Displayed stage arithmetic'
        expanded=read_cells(MX.findall(sol)[2])
        for idx,entry in enumerate(x for row in expanded for x in row):
            x,y=int(a[idx]),int(b[idx])
            left='('+str(x)+')' if t=='q-125722' and x<0 else str(x)
            right='('+str(y)+')' if y<0 else str(y)
            assert entry==left+'+'+right,'Required unevaluated entrywise addition stage missing/changed'
        if ':question/worked-solution' in source:
            assert mask(sol)==mask(source[':question/worked-solution']),'Shared source prose/stage sequence'
        elif t=='q-103':
            assert mask(sol)=='We add the corresponding entries:\n\n$$\n'+r'\begin{aligned}<MATRIX>+<MATRIX> & =<MATRIX> \\  & =<MATRIX>\end{aligned}'+'\n$$'
    all_ids=[];field_keys=[]
    for f in fs:
        uuid.UUID(f[':answer-field/id']);all_ids.append(f[':answer-field/id']);field_keys.append(f[':answer-field/key'])
        sf=next(s for s in source[':question/answer-fields'] if s[':answer-field/key']==f[':answer-field/key'])
        assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        if raw: assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        for ans in f[':answer-field/choices']:
            uuid.UUID(ans[':answer/id']);all_ids.append(ans[':answer/id']);check_text(ans[':answer/value'],False)
            assert set(ans)=={':answer/id',':answer/type',':answer/value'},'Absent source feedback must remain absent'
        if f[':answer-field/type'].endswith('/radio'):
            assert len(fs)==1 and len(f[':answer-field/choices'])==5
            vals=[read_matrices(ans[':answer/value'])[0] for ans in f[':answer-field/choices']]
            assert all(v.shape==c.shape for v in vals)
            assert len({flatten(v) for v in vals})==5,'Entire bank ambiguous'
            matches=[ans[':answer/id'] for ans,v in zip(f[':answer-field/choices'],vals) if v==c]
            assert len(matches)==1,'Independent complete-bank correct count'
            if ':answer-field/correct' in f: assert f[':answer-field/correct']==[':answer/id',matches[0]]
            if meta['profile']=='method-omission':
                expected=[c,a,b,a-b,b-a]
                assert {flatten(v) for v in vals}=={flatten(v) for v in expected}
            if meta['profile']=='method-sign':
                abs_sum=sp.Matrix(a.rows,a.cols,[abs(x)+abs(y) for x,y in zip(a,b)])
                assert {flatten(v) for v in vals}=={flatten(v) for v in [c,-c,a-b,b-a,abs_sum]}
        else:
            assert len(fs)==6 and len(f[':answer-field/choices'])==1
            idx=int(f[':answer-field/key'].split('-')[1])-1;assert sp.sympify(f[':answer-field/choices'][0][':answer/value'])==c[idx]
            assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][0][':answer/id']]
    assert len(all_ids)==len(set(all_ids));assert len(field_keys)==len(set(field_keys))
    if len(fs)==6: assert re.findall(r'\{\{(field-\d+)\}\}',q[':question/problem'])==['field-'+str(i) for i in range(1,7)]
    assert meta['eligible_for_learning']==(not meta['evidence_only'])
    return r

def native(label,r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if f[':answer-field/correct'][1]==a[':answer/id'] else 'rejected','purpose':'All five complete bank choices'} for a in f[':answer-field/choices']]
        else:
            n=int(f[':answer-field/choices'][0][':answer/value'])
            checks += [{'field_index':i,'submitted':v,'expected':result,'purpose':'Blank canonical/equivalent/wrong integer'} for v,result in [(str(n),'accepted'),('('+str(n+3)+'-3)','accepted'),(str(2*n)+'/2','accepted'),(str(n+1),'rejected')]]
    return {'label':label,'record':r,'checks':checks}

def must_reject(fn):
    try: fn()
    except (AssertionError,ValueError): return
    raise AssertionError('Mutation/invalid parameter was not rejected')

def main():
    assert (HERE/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186054650.json').read_bytes()
    baseline=json.loads((HERE/'registered-baseline-hashes.json').read_text())
    for path,sha in baseline.items(): assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,'Registered baseline changed: '+path
    cases=[];replays=[];inputs=[];review=[];reviewmd=[];mapping=[]
    matched_choices=0;known_correct=0;matched_solutions=0
    for t,source in g.SOURCES.items():
        case={'source_id':source[':db/id'],'math_academy_id':t,'template':t,'level':'easy','parameters':g.original(t),'bank_profile':'source:'+t}
        cases.append(case);r=check(g.generate('easy',template=t,parameters=case['parameters'],profile=case['bank_profile']))
        q=r['question'];assert q[':question/problem']==source[':question/problem'],'Exact prompt '+t
        if ':question/worked-solution' in source:
            assert q[':question/worked-solution']==source[':question/worked-solution'];matched_solutions+=1
        for sf in source[':question/answer-fields']:
            f=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']==sf[':answer-field/key'])
            original=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);generated=sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert original==generated
            matched_choices+=len(original)
            if ':answer-field/correct' in sf:
                expected=sf[':answer-field/correct'][':answer/value'];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==expected;known_correct+=1
            for a in sf[':answer-field/choices']:
                mapping.append({'source_id':source[':db/id'],'template':t,'field_key':sf[':answer-field/key'],'source_answer_id':a[':answer/id'],'value':a[':answer/value'],'exact_value_matched':True,'original_designation_present':':answer-field/correct' in sf})
        completed=check(g.generate('easy',template=t,parameters=case['parameters'],profile='source-completed:'+t));inputs.append(native('completed-original-'+t,completed))
        replays.append({'source_id':source[':db/id'],'template':t,'exact_prompt':True,'exact_solution':':question/worked-solution' in source,'complete_bank_match':True,'attribute_presence_match':True,'raw_record':r})
        reviewmd += ['## Original MA '+t+'\n\n'+g.markdown(r),'## Historical bank completion '+t+' (authored missing attributes, evidence only)\n\n'+g.markdown(completed)]
        # Changed-parameter evidence demonstrates recipes do not return anchor payload.
        changed={k:[-x for x in v] for k,v in case['parameters'].items()}
        changed_record=check(g.generate('easy',template=t,parameters=changed,profile='source:'+t))
        assert changed_record['question'][':question/problem']!=q[':question/problem'];review.append(changed_record)
        reviewmd.append('## Parameterized original profile '+t+' (evidence only)\n\n'+g.markdown(changed_record))
    samples=[];coverage={level:{'templates':set(),'profiles':set(),'orientations':set(),'opposite_pairs':set(),'a_slots':[set() for _ in range(6)],'b_slots':[set() for _ in range(6)]} for level in g.LEVELS}
    fingerprints={level:set() for level in g.LEVELS};normal_default={level:{'templates':set(),'profiles':set()} for level in g.LEVELS}
    for level in g.LEVELS:
        for seed in range(250):
            default=check(g.generate(level,seed));normal_default[level]['templates'].add(default['generation']['template']);normal_default[level]['profiles'].add(default['generation']['profile'])
        for t,profile in itertools.product(g.TEMPLATES,g.PROFILES):
            for seed in range(30):
                r=check(g.generate(level,seed+g.TEMPLATES.index(t)*1000+g.PROFILES.index(profile)*100,template=t,profile=profile));samples.append(r);inputs.append(native(level+'-'+t+'-'+profile+'-'+str(seed),r))
                p=r['generation']['parameters'];cov=coverage[level];cov['templates'].add(t);cov['profiles'].add(profile);cov['orientations'].add(str(read_matrices(r['question'][':question/problem'])[0].shape));cov['opposite_pairs'].add(sum(x*y<0 for x,y in zip(p['a'],p['b'])))
                for k in ('a','b'):
                    for i,v in enumerate(p[k]):cov[k+'_slots'][i].add(v)
                fingerprints[level].add(r['generation']['mathematical_fingerprint'])
                replay=check(g.generate(level,seed+998,template=t,profile=profile,parameters=p))
                assert replay['question'][':question/id']==r['question'][':question/id'],'Seed/order affects identity'
                if seed<2:
                    review.append(r);reviewmd.append('## Generated '+level+' '+t+' '+profile+' seed '+str(seed)+' (authored)\n\n'+g.markdown(r))
        assert normal_default[level]['templates']==set(g.TEMPLATES) and normal_default[level]['profiles']==set(g.PROFILES)
        assert len(fingerprints[level])>=350
    # Profile aliases and commutative task identity are separated from content.
    for level in g.LEVELS:
        r=g.generate(level,5,template='q-103',profile='method-omission');p=r['generation']['parameters']
        for alias in ('method','authored-method'):
            assert g.generate(level,50,template='q-103',profile=alias,parameters=p)['question'][':question/id']==r['question'][':question/id']
        s=g.generate(level,12,template='q-103',profile='method-sign',parameters=p)
        assert s['question'][':question/id']!=r['question'][':question/id']
        assert s['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        swapped={'a':p['b'],'b':p['a']};s=g.generate(level,12,template='q-103',profile='method-omission',parameters=swapped)
        assert s['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        assert s['question'][':question/id']!=r['question'][':question/id']
    # Explicit workload/field guards and whole bank collisions (no replacements).
    for level,p in [('easy',{'a':[10]*6,'b':[-1]*6}),('moderate',{'a':[1]*6,'b':[1]*6}),('hard',{'a':[10]*6,'b':[-10]*6}),('hard',{'a':[9]*6,'b':[-16]*6})]:
        must_reject(lambda level=level,p=p:g.generate(level,parameters=p,template='q-103'))
    must_reject(lambda:g.generate('easy',parameters={'a':[1]*6,'b':[1]*6},template='q-103',profile='method-omission'))
    must_reject(lambda:g.generate('easy',template='q-319601',field_type='radio'))
    # Six substantive slots, both orientations, including signed boundary entries.
    for level in g.LEVELS:
        for value in ([0,-9,9] if level=='easy' else [-16,-1,1,16] if level=='moderate' else [-16,-10,10,16]):
            for k in ('a','b'):
                for slot in range(6):
                    found=False
                    for seed in range(250):
                        base=g.generate(level,seed,template='q-319601')['generation']['parameters'];base[k][slot]=value
                        try:r=g.generate(level,parameters=base,template='q-319601')
                        except ValueError:continue
                        check(r);found=True;break
                    assert found,(level,k,slot,value)
    # Real validator mutation regressions (stage equality alone is insufficient).
    original=g.generate('moderate',2,template='q-125722',profile='method-omission')
    mutations=[]
    broken=copy.deepcopy(original);sol=broken['question'][':question/worked-solution'];stages=MX.findall(sol);broken['question'][':question/worked-solution']=sol.replace(stages[2],stages[3]);mutations.append(broken)
    broken=copy.deepcopy(original);broken['question'][':question/worked-solution']+='\x0c';mutations.append(broken)
    broken=copy.deepcopy(original);choices=broken['question'][':question/answer-fields'][0][':answer-field/choices'];choices[0][':answer/value']=choices[1][':answer/value'];mutations.append(broken)
    broken=copy.deepcopy(original);broken['question'][':question/problem']=broken['question'][':question/problem'].replace('Calculate $P+Q','Calculate $P-Q');mutations.append(broken)
    for broken in mutations: must_reject(lambda broken=broken:check(broken))
    raw=g.generate('easy',template='q-103',parameters=g.original('q-103'),profile='source');raw['question'][':question/difficulty']=':question.difficulty/easy';must_reject(lambda:check(raw))
    assert all(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha for path,sha in baseline.items())
    save('source-cases.json',cases);save('source-choice-mapping.json',mapping);save('source-replay.json',replays)
    save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    native_report=json.loads((HERE/'native-grading.json').read_text());assert native_report['documented_unresolved_checks']==0
    save('review.json',review);(HERE/'review.md').write_text('\n\n'.join(reviewmd)+'\n')
    encode=lambda x: sorted(x) if isinstance(x,set) else [sorted(y) for y in x]
    result={'passed':True,'source_basis':g.S['basis'],'source_lineage':g.S['lineage'],'original_MA_records':7,'independent_inventory_records':0,
            'fidelity':{'exact_prompts':'7/7','complete_banks':'7/7','answer_values':str(matched_choices)+'/36','present_solutions':str(matched_solutions)+'/5','present_correct_designations':str(known_correct)+'/10','missing_correct_designations':2,'missing_solutions':2,'raw_presence_parity':'7/7','source_repairs':0},
            'authored_levels':['moderate','hard'],'level_calibration':'Uncertain conservative same-method workload claims, not recovered MA labels; easy default bounds also authored',
            'normal_samples':len(samples),'normal_default_samples':750,'unique_mathematical_tasks':{k:len(v) for k,v in fingerprints.items()},
            'coverage':{level:{k:encode(v) for k,v in cov.items()} for level,cov in coverage.items()},
            'native':{k:v for k,v in native_report.items() if k!='records'},'baseline_files_unchanged':len(baseline),'mutation_regressions':5,
            'capacity_constructive_lower_bounds':{'easy_per_orientation':531440,'moderate_per_orientation':13824000,'hard_per_orientation':46656},
            'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},
            'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',ROOT/'generate/runs/current/check-engine']}}
    save('validation.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('coverage','hashes')},indent=2))
if __name__=='__main__':main()
