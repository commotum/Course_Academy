"""Private independent full rendered-math validation and frozen native grading."""
import copy, hashlib, importlib.util, json, subprocess, sys, uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.dont_write_bytecode=True

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

g=module('kp04091',HERE.with_suffix('.py'));p=module('private_parser',HERE/'parser.py')

def save(name,data): (HERE/name).write_text(json.dumps(data,indent=2,default=str)+'\n')

def independent(rec):
    slots,root=p.rendered_math(rec)
    assert slots==rec['generation']['parameters']
    assert rec['knowledge_point']['db_id']==g.KP_ID
    q=rec['question'];f=q[':question/answer-fields'][0];ids=[q[':question/id'],f[':answer-field/id'],f[':answer-field/choices'][0][':answer/id']]
    assert len(set(ids))==3
    for value in ids: uuid.UUID(value)
    g.math_format.validate_generated_record(rec)
    return root

def checks(rec):
    value=int(rec['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
    return [dict(field_index=0,submitted=text,expected=('accepted' if text=='1' and value==1 else outcome),purpose='Actual bounded public scalar blank grading') for outcome,entries in [('accepted',[str(value),str(value)+'.0',str(value)+'+0',r'\frac{'+str(2*value)+'}{2}']),('rejected',['0','1',str(value+1)])] for text in entries]

def main():
    source=g.SOURCE;cases=[];replays=[];excluded=[];fidelity=[]
    for mid,q in g.ORIGINALS.items():
        slots=p.parameters(q[':question/problem']);complete=':question/worked-solution'in q and ':answer-field/correct'in q[':question/answer-fields'][0]
        level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
        case=dict(source_id=mid,source_question_id=q[':question/id'],parameters=slots,difficulty=level,template='direct' if slots['scale']==1 else 'scaled',bank_profile='blank-integer' if complete else 'incomplete-unrated',record=q,evidence_role='Math Academy practice source',complete=complete)
        cases.append(case)
        assert g.replay_source(mid)==q
        if not complete:
            excluded.append(dict(source_id=mid,reason='Raw evidence preserved; source missing rating, solution, bank, and correct reference. No fabricated original answer.'))
            continue
        rec=g.generate(level,parameters=slots);independent(rec);new=rec['question'];oldfield=q[':question/answer-fields'][0];newfield=new[':question/answer-fields'][0]
        assert new[':question/problem']==g.math_format.normalize_prose(q[':question/problem'])
        assert new[':question/worked-solution']==g.math_format.normalize_prose(q[':question/worked-solution'])
        assert oldfield[':answer-field/type'][':db/ident']==newfield[':answer-field/type'] and oldfield[':answer-field/key']==newfield[':answer-field/key']
        assert [a[':answer/value'] for a in oldfield[':answer-field/choices']]==[a[':answer/value'] for a in newfield[':answer-field/choices']]
        assert oldfield[':answer-field/correct'][':answer/value']==newfield[':answer-field/choices'][0][':answer/value']
        assert all(':answer/feedback' not in a for a in oldfield[':answer-field/choices'])
        fidelity.append(dict(source_id=mid,exact_prompt=True,exact_full_solution=True,full_fields_bank_correct_feedback=True,matched_options=1,total_options=1,missing_options=[],extra_options=[]));replays.append(rec)
    save('source-cases.json',cases);save('excluded-source.json',excluded)
    for case in cases: assert g.replay_source(case['source_id'],case['parameters'])==case['record']
    variants=[];coverage={};batches={}
    for level in g.SUPPORTED_LEVELS:
        records=[g.generate(level,seed) for seed in range(100)]
        for rec in records: independent(rec)
        batch=g.batch(level,g.CAPACITY[level],811)
        for rec in batch: independent(rec)
        assert len({r['generation']['parameter_fingerprint'] for r in batch})==g.CAPACITY[level]
        assert batch==g.batch(level,g.CAPACITY[level],811)
        variants+=records+batch;batches[level]=batch
        coverage[level]={k:sorted({r['generation']['parameters'][k] for r in records+batch}) for k in ('variable','parameter','scale','shift','left','right')}
    # Exhaust every public mathematical tuple; label aliases do not add tasks.
    boundaries=[]
    for level in g.SUPPORTED_LEVELS:
        for numeric in g.CATALOG[level]:
            slots=dict(zip(('scale','shift','left','right'),numeric));slots.update(variable='x',parameter='p')
            rec=g.generate(level,parameters=slots);independent(rec);boundaries.append(rec)
    # Controlled changed numeric slot with other givens fixed; rerender and re-read everything.
    controlled=[];base=dict(variable='x',parameter='p',scale=-7,shift=3,left=8,right=1)
    for slot,value in [('shift',-3),('left',-8),('right',-10),('scale',3),('variable','w'),('parameter','r')]:
        rec=g.generate('moderate',parameters=dict(base,**{slot:value}));independent(rec);controlled.append(dict(changed_slot=slot,record=rec))
    neg=[]
    def rejects(label,fn):
        try: fn()
        except (ValueError,TypeError,AssertionError): neg.append(label)
        else: raise AssertionError('Accepted invalid case: '+label)
    for kwargs in [dict(level='unknown'),dict(level='moderate',seed=True),dict(level='moderate',seed='1'),dict(level='easy',template=''),dict(level='easy',profile=''),dict(level='easy',template=[]),dict(level='easy',profile={})]: rejects(str(kwargs),lambda kwargs=kwargs:g.generate(**kwargs))
    for slot,value in [('scale',0),('scale',-1),('scale',10),('shift',0),('shift',10),('shift',True),('left',0),('left',10),('right',11),('right',8),('variable',[]),('parameter',None)]: rejects('invalid '+slot+str(value),lambda slot=slot,value=value:g.generate('moderate',parameters=dict(base,**{slot:value})))
    for parameters in [[],True,dict(base,extra=1),{k:v for k,v in base.items()if k!='scale'}]: rejects('invalid parameter contract',lambda parameters=parameters:g.generate('moderate',parameters=parameters))
    for level in g.SUPPORTED_LEVELS:
        for count in [-1,g.CAPACITY[level]+1,True,1.0]: rejects('invalid count',lambda level=level,count=count:g.batch(level,count))
        assert g.batch(level,0)==[]
        for fmt in ('json','markdown'):
            args=[str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty',level,'--seed','811','--count','2','--format',fmt]
            a=subprocess.run(args,capture_output=True,text=True,check=True).stdout;b=subprocess.run(args,capture_output=True,text=True,check=True).stdout;assert a==b
            if fmt=='json': assert json.loads(a)==batches[level][:2]
            else: assert a.count('{{field-1}}')==2
    for target in ('question',):
        ref=g.generate('moderate',parameters=base)
        mutations=[('key',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].update({':answer/value':'0'})),('given',lambda q:q.update({':question/problem':q[':question/problem'].replace('=1','=8',1)})),('solution target',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('k & =-3.','k & =2.').replace('p & =-3.','p & =2.')})),('condition',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('-7(p+3)=0.','-7(p+3)=1.')})),('reduction',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('{{-7}_{⏟}}_{b}','{{7}_{⏟}}_{b}')}))]
        for label,fn in mutations:
            bad=copy.deepcopy(ref);fn(bad['question']);rejects('semantic mutation '+label,lambda bad=bad:independent(bad))
    records=replays+variants+boundaries+[r['record']for r in controlled]
    save('engine-input.json',[dict(label=str(i),record=rec,checks=checks(rec)) for i,rec in enumerate(records)])
    binary=ROOT/'generate/runs/current/check-engine';sha=hashlib.sha256(binary.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
    result=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(result.stdout+result.stderr);assert result.returncode==0,result.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    baseline=json.loads((HERE/'baseline.json').read_text());paths=[ROOT/'generate/scratch/17592186204091.py']+sorted((ROOT/'generate/scratch/17592186204091').rglob('*'));paths=[p for p in paths if p.is_file()];assert [str(p.relative_to(ROOT)) for p in paths]==baseline['pathset'];assert all(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==hash for path,hash in baseline['sha256'].items())
    save('fidelity.json',dict(complete_banks=len(fidelity),complete_values=len(fidelity),total_values=len(fidelity),cases=fidelity,raw_pull_full_record_replays=len(cases),incomplete=excluded,source_repairs=[]))
    save('capacity.json',dict(per_level=g.CAPACITY,definition='Full normalized supplied equation: direct/scaled backbone, shift, left/scale, right/scale. Ignore variable/parameter labels, seeds, IDs, rating, uniform entire-equation scaling.',global_distinct_tasks=len({r['generation']['parameter_fingerprint']for r in boundaries}),hard_overlap='Negative-scale hard catalog overlaps moderate; difficulty rating is not distinctness.'))
    save('validation.json',dict(status='pass',basis=2275,lineage=source['lineage'],fidelity=fidelity,source_repairs=[],incomplete=excluded,independent_rendered_records=len(records),boundary_records=len(boundaries),negative_controls=neg,slot_coverage=coverage,native={k:engine[k]for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},native_binary_sha256=sha,baseline_pathset_unchanged=True,baseline_hashes_unchanged=True,database_writes=0))
    save('review.json',dict(replays=replays,variants=[g.generate(level,811)for level in g.SUPPORTED_LEVELS],controlled_changed_slots=controlled))
    review=[]
    for case,rec in zip([c for c in cases if c['complete']],replays):review.append('## Source '+case['source_id']+'\n\n'+case['record'][':question/problem']+'\n\n'+case['record'][':question/worked-solution']+'\n\n### Served replay\n\n'+g.markdown(rec))
    for level in g.SUPPORTED_LEVELS:review.append('## '+level+' variant\n\n'+g.markdown(g.generate(level,811)))
    for row in controlled:review.append('## Controlled slot '+row['changed_slot']+'\n\n'+g.markdown(row['record']))
    (HERE/'review.md').write_text('\n\n---\n\n'.join(review)+'\n')
    print(json.dumps(dict(records=len(records),fidelity=len(fidelity),native=engine['accepted_checks']+engine['rejected_checks'],negative_controls=len(neg))))

if __name__=='__main__':main()
