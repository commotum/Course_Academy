"""Independent exact elimination, rendered-content, source-bank and learner checks."""
import hashlib, importlib.util, itertools, json, re, subprocess
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('pivot_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def exact_rank(m):
    a=[[Fraction(str(x)) for x in row] for row in m.tolist()];i=0
    for j in range(len(a[0])):
        k=next((k for k in range(i,len(a)) if a[k][j]),None)
        if k is None:continue
        a[i],a[k]=a[k],a[i];pivot=a[i][j]
        a[i]=[x/pivot for x in a[i]]
        for k in range(i+1,len(a)):
            c=a[k][j];a[k]=[x-c*y for x,y in zip(a[k],a[i])]
        i+=1
        if i==len(a):break
    return i

def check_record(r):
    assert r['knowledge_point']['db_id']==g.ID and r['generation']['eligible_for_learning']
    q=r['question'];assert q[':question/difficulty']==':question.difficulty/moderate'
    a=g.matrices(q[':question/problem']);states=g.matrices(q[':question/worked-solution']);assert len(a)==1 and a[0]==states[0]
    t=g.TEMPLATES[r['generation']['template']];assert len(states)==len(t['states'])
    assert all(g.mask(a)==g.mask(b) for a,b in zip(states,t['states']))
    ops=r['generation']['operations'];assert len(ops)==len(states)-1
    rendered_ops=re.findall(r'\{R\}_\{(\d+)\} & :=\{R\}_\{(\d+)\}\+\((.*?)\)\{R\}_\{(\d+)\}',q[':question/worked-solution'])
    assert len(rendered_ops)==len(ops)
    for (i,j,c),(ri,ri2,rc,rj),before,after in zip(ops,rendered_ops,states,states[1:]):
        assert int(ri)==int(ri2)==i+1 and int(rj)==j+1 and rc==g.s.latex(g.s.Rational(c))
        expected=before.copy();expected[i,:]=before.row(i)+g.s.Rational(c)*before.row(j);assert expected==after
    assert states[-1].is_echelon
    correct=exact_rank(states[0]);assert all(exact_rank(m)==correct for m in states)
    assert correct==sum(any(x for x in row) for row in states[-1].tolist())
    f=q[':question/answer-fields'];assert len(f)==1;f=f[0]
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    choices=f[':answer-field/choices'];assert len({a[':answer/id'] for a in choices})==5
    values=[int(a[':answer/value']) for a in choices];assert sorted(values)==t['bank'] and len(set(values))==5
    assert all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in choices)
    right=[a for a in choices if int(a[':answer/value'])==correct];assert len(right)==1 and f[':answer-field/correct']==[':answer/id',right[0][':answer/id']]
    assert f'${t["name"]}$ has ${correct}$ pivots' in q[':question/worked-solution']
    assert f'number of pivot columns is ${correct}.$' in q[':question/worked-solution']
    assert g.fingerprint(states[0])==r['generation']['mathematical_fingerprint']
    # Content-addressed field ownership, independent of seed.
    assert q[':question/id']==g.uid([g.VERSION,g.fingerprint(states[0]),t['bank']])
    assert f[':answer-field/id']==g.uid([q[':question/id'],'selection'])
    assert all(a[':answer/id']==g.uid([f[':answer-field/id'],a[':answer/value']]) for a in choices)
    assert ':question/math-academy-id' not in q
    return correct

def native_checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned radio bank'} for a in f[':answer-field/choices']]

def run():
    out=HERE/'reference';records=[];reports=[];reviews=[]
    for key,t in g.TEMPLATES.items():
        replay=g.source_replay(key);check_record(replay)
        q=t['source'];f=q[':question/answer-fields'][0]
        source_values=sorted(a[':answer/value'] for a in f[':answer-field/choices']);rf=replay['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==source_values
        assert next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])==f[':answer-field/correct'][':answer/value']
        assert g.matrices(replay['question'][':question/problem'])[0]==t['states'][0]
        assert g.matrices(replay['question'][':question/worked-solution'])==t['states']
        records.append(replay);variants=[]
        candidate_duplicates=0;fingerprints=set()
        for seed in range(1000):
            r=g.generate(seed=seed,template=key);check_record(r);assert r==g.generate(seed=seed,template=key)
            assert r==g.generate(seed=seed,template=key,parameters=r['generation']['parameters'])
            fp=r['generation']['mathematical_fingerprint']
            if fp in fingerprints:
                candidate_duplicates+=1;continue
            fingerprints.add(fp);variants.append(r);records.append(r)
            if len(variants)==12:break
        assert len(variants)==12,'Bounded distinct sampler exhausted'
        assert len({r['generation']['mathematical_fingerprint'] for r in variants})==len(variants)
        cells=[]
        for i,row in enumerate(t['states'][-1].tolist()):
            for j,x in enumerate(row):
                values={r['generation']['parameters']['echelon'][i][j] for r in variants}
                if x:assert len(values)>1
                else:assert values=={'0'}
                cells.append({'row':i,'column':j,'role':'nonzero entry' if x else 'structural zero','sampled_values':sorted(values)})
        coefficients=[]
        for i,op in enumerate(t['operations']):
            values={r['generation']['parameters']['multipliers'][i] for r in variants};assert len(values)>1
            coefficients.append({'target_row':op[0],'source_row':op[1],'values':sorted(values)})
        # Held-data change: edit one echelon entry, keeping all other data fixed.
        changed=None;base=variants[0];p=base['generation']['parameters']
        for i,row in enumerate(p['echelon']):
            for j,x in enumerate(row):
                if x=='0':continue
                for n in (-9,-5,-1,1,5,9):
                    pp=json.loads(json.dumps(p));pp['echelon'][i][j]=str(n)
                    try:r=g.generate(template=key,parameters=pp)
                    except ValueError:continue
                    if r['generation']['mathematical_fingerprint']!=base['generation']['mathematical_fingerprint']:
                        check_record(r);changed=r;break
                if changed:break
            if changed:break
        assert changed;records.append(changed)
        reports.append({'template':key,'source_eid':q[':db/id'],'profile':t['profile'],'shape':list(t['states'][0].shape),'operations':[[i,j,str(c)] for i,j,c in t['operations']],'rank':exact_rank(t['states'][0]),'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'complete_bank_matched':True,'echelon_slot_coverage':cells,'multiplier_slot_coverage':coefficients,'changed_value_with_other_data_fixed':True,'target_slot':'All pivot columns are counted; no selected target slot','sampled_distinct_tasks':len(variants),'candidate_duplicate_tasks_excluded':candidate_duplicates})
        reviews.append('## '+key+'\n\nOriginal:\n\n'+q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\nVariant:\n\n'+variants[0]['question'][':question/problem']+'\n\n'+variants[0]['question'][':question/worked-solution'])
    for level in ('easy','hard'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported band accepted')
    # Invalid explicit parameters are rejected, not silently changed.
    t=next(iter(g.TEMPLATES));p=g.source_replay(t)['generation']['parameters'];p=json.loads(json.dumps(p));p['multipliers'][0]='0'
    try:g.generate(template=t,parameters=p)
    except ValueError:pass
    else:raise AssertionError('Zero row-operation coefficient accepted')
    (out/'native-input.json').write_text(json.dumps([{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(records)],indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(out/'native-input.json'),str(out/'native-report.json')],check=True)
    (out/'side-by-side.md').write_text('# Original and generated pivot-column questions\n\n'+'\n\n'.join(reviews)+'\n')
    result={'status':'passed','basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'templates':reports,'supported_levels':['moderate'],'source_practice_questions':17,'supported_complete_source_banks':16,'source_choices_matched':80,'source_distractors_matched':64,'excluded_source_questions':g.EXCLUDED,'excluded_reason':'q-35459 is unrated and has no correct answer or worked solution; retained unchanged, not supported or counted','correctness':'Independent Fraction Gaussian elimination, exact rendered row operations and echelon pivot count','grading':'Actual course_academy_engine::learning::grade_field for every option of every checked instance','validated_records':len(records),'new_plots':0,'fixed_slots':'matrix letter, dimensions, zero masks, elimination row roles, number of stages, rank, count-all-columns target, field layout, complete bank','fidelity':'Exact source matrices, all intermediate states, operation coefficients, full bank and correct designation replayed. Three stale A references corrected in rendered conclusions; arithmetic unchanged. Generic row-operation notation is normalized to addition of a signed multiple.','capability_exceptions':[{'difficulty':l,'status':'unsupported-in-current-package','shortage_to_target':5,'evidence':'No rated source or calibrated template at this band. All 16 complete sources are moderate and use 1–2 short elimination operations. Changing the stage workload or assigning a new difficulty would require new classification evidence.'} for l in ('easy','hard')]}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'validate.py',out/'source.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'template-extraction.json',HERE/'replenish.py',HERE/'validation.json',out/'native-report.json']}
    (HERE/'validation-freeze.json').write_text(json.dumps({'status':'passed','hashes':hashes},indent=2)+'\n')
    print(json.dumps({'status':'passed','templates':len(reports),'validated_records':len(records),'source_banks':16}))
if __name__=='__main__':run()
