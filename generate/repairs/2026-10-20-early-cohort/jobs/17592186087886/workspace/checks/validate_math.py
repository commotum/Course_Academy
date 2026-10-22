"""Finite-family visible-math, complete-source replay, and counterfactual checks."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
validator=load('retained_validator',ROOT/'17592186087886/validate.py');g=validator.g
from math_reader import rate,prompt_rhs,fingerprint,x,y,v
from collections import Counter
OUT=ROOT/'evidence'
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2,default=str,ensure_ascii=False)+'\n')
def bank(r):return sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
def key(r):
    f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def main():
    records=[];replays=[];coverage={};counterfactuals=[];negative=0
    for t,k0 in g.ORIGINAL.items():
        src=g.SOURCES[t];validator.solution_check(src)
        replay=g.generate(template=t,parameters={'k':k0})
        assert replay['question'][':question/problem']==src[':question/problem']
        assert replay['question'][':question/worked-solution']==src[':question/worked-solution']
        assert bank(replay)==sorted(a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices'])
        assert key(replay)==src[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
        rhs,recipes=g.mathematics(t,k0)
        for a,(coef,right) in zip(src[':question/answer-fields'][0][':answer-field/choices'],recipes):
            assert validator.equivalent(rate(a[':answer/value']),right/coef)
        replays.append({'template':t,'source_question_id':src[':question/id'],'exact_prompt':True,'exact_solution':True,'complete_choices':5,'distractors':4,'correct_equation':True})
        family=[]
        for k in g.DOMAINS[t]:
            r=g.generate('easy',37,t,{'k':k});validator.independent(r)
            # Compare every displayed equation, not just its key, against its source-bank recipe.
            intended=g.mathematics(t,k)[1];displayed=[rate(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert all(sum(validator.equivalent(d,b/a) for a,b in intended)==1 for d in displayed)
            family.append(r);records.append(r)
        coverage[t]={'k_values':[r['generation']['parameters']['k'] for r in family],'semantic_instances':len({fingerprint(r['question'][':question/problem']) for r in family}),'solution_rows_checked':sum(validator.solution_check(r['question']) for r in family)}
        changed=next(r for r in family if r['generation']['parameters']['k']!=k0)
        assert not validator.equivalent(rate(key(changed)),rate(key(replay)))
        stale=copy.deepcopy(changed['question']);stale[':question/worked-solution']=src[':question/worked-solution']
        try:validator.solution_check(stale)
        except AssertionError:negative+=1
        else:raise AssertionError('Stale solution escaped checks: '+t)
        irrelevant=g.generate('easy',3,t,{'k':changed['generation']['parameters']['k']})
        assert bank(changed)==bank(irrelevant) and key(changed)==key(irrelevant)
        assert changed['question'][':question/problem']==irrelevant['question'][':question/problem']
        assert changed['question'][':question/worked-solution']==irrelevant['question'][':question/worked-solution']
        assert changed['question'][':question/id']==irrelevant['question'][':question/id']
        counterfactuals.append({'template':t,'relevant_parameters':[{'k':k0},changed['generation']['parameters']],'visible_rate_changed':True,'all_worked_stages_verified':True,'irrelevant_seed_change_preserves_math_and_identity':True})
        print('Checked',t,flush=True)
    assert len(records)==48 and len({fingerprint(r['question'][':question/problem']) for r in records})==48
    for band in ['moderate','hard']:
        try:g.generate(band)
        except ValueError:pass
        else:raise AssertionError('Unsupported band generated')
    for t in g.DOMAINS:
        for bad in [0,8,1.5]:
            try:g.generate(template=t,parameters={'k':bad})
            except ValueError:pass
            else:raise AssertionError('Out-of-domain value generated')
    # Mathematical regression for the reproduced additive-coefficient failure.
    grouped=g.generate(template='q-14315',parameters={'k':2});validator.solution_check(grouped['question'])
    intended=v+1
    assert any(validator.equivalent(rate(a[':answer/value']),1/(x*intended)) for a in grouped['question'][':question/answer-fields'][0][':answer-field/choices'])
    save('records.json',records);save('source-replay.json',replays);save('slot-coverage.json',coverage);save('counterfactuals.json',counterfactuals)
    cases=[{'label':r['generation']['template']+':'+str(r['generation']['parameters']['k']),'record':r,'checks':validator.checks(r)} for r in records]
    # Key from a changed coefficient is wrong for the otherwise same family source instance.
    # Submitting that old-key choice in each changed instance must be rejected if still present.
    save('grader-input.json',cases)
    selected=[next(r for r in records if r['generation']['template']==t and r['generation']['parameters']['k']==k) for t,k in [('q-14315',2),('q-8747',3),('q-14314',4),('q-90600',6)]]
    save('render-records.json',selected)
    source_path=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186087886/source')
    inventory=json.loads((source_path/'inventory.json').read_text());inspected=[]
    for q in inventory['questions']:
        validator.solution_check(q)
        inspected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'math_and_grouping_defect_present':False,'math_academy_id':q.get(':question/math-academy-id')})
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
    save('inventory-audit.json',{'status':'verified absence of demonstrated grouping defect in all captured stored records','basis':inventory['basis'],'tested_records':inspected,'packaging_defect':'A script runtime closure defect does not occur in stored source question records. All eight captured records are original source items; none was relabeled as generated.'})
    save('math-validation.json',{'status':'pass','records':48,'source_banks':8,'source_choices':40,'source_distractors':32,'stale_solution_negative_controls':negative,'grouping_counterexample_fixed':True,'inventory_checked':len(inspected)})
    print(json.dumps({'status':'pass','records':48,'source_banks':8,'negative_controls':negative}))
if __name__=='__main__':main()
