"""Focused independent regression of the exponential tangent bank repair."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random
import sys
import sympy as s
import probe

HERE=Path(__file__).resolve().parent
OUT=HERE/'evidence';OUT.mkdir(exist_ok=True)
def save(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def module(name,path):
    sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result
g=module('candidate',HERE/'package/generator.py')
old=module('original',HERE/'original/generator.py')


def math_check(record):
    expected=probe.expected(record)
    choices=probe.choices(record)
    values=[probe.parse(c[':answer/value']) for c in choices]
    assert len(values)==5 and len(set(map(s.srepr,values)))==5
    correct=[c[':answer/id'] for c,v in zip(choices,values) if s.simplify(v-expected)==0]
    assert correct==[probe.correct(record)]
    problem=record['question'][':question/problem']
    point=probe.parse(__import__('re').search(r'point where \$x=([^$]+)',problem)[1].rstrip('.'))
    slopes=[s.simplify(s.diff(v,probe.x)) for v in values]
    assert len(set(slopes))==5, 'A repeated coefficient must not encode the key'
    assert len(set(s.simplify(v.subs(probe.x,point)) for v in values))==1
    return values,slopes


def main():
    old_batch=[old.generate_hard(1072510293+i) for i in range(4)]
    old_fresh=[old.generate_hard(seed) for seed in range(800,824)]
    negative={'requested':probe.probes(old_batch),'fresh':probe.probes(old_fresh)}
    assert negative['requested']['correct']==4 and negative['fresh']['correct']==24
    save('negative-controls.json',negative)
    batch=[g.generate_hard(1072510293+i) for i in range(4)]
    fresh=[g.generate_hard(seed) for seed in range(800,824)]
    save('requested.json',batch);save('fresh.json',fresh)
    cases=[];graders=[];ranks=Counter();positions=Counter();signs=Counter()
    for name,records in [('requested',batch),('fresh',fresh)]:
        assert probe.probes(records)['correct']==0
        for index,record in enumerate(records):
            _,slopes=math_check(record)
            cs=probe.choices(record);key=probe.correct(record)
            correct_index=next(i for i,c in enumerate(cs) if c[':answer/id']==key)
            rank=sorted(range(5),key=lambda i:float(slopes[i])).index(correct_index)
            ranks[rank]+=1;positions[correct_index]+=1;signs[int(s.sign(slopes[correct_index]))]+=1
            cases.append({'set':name,'index':index,'rank':rank,'position':correct_index,'point':record['generation']['parameters']['point']})
            graders.append({'label':name+'/'+str(index),'record':record,'checks':[
                {'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected'} for c in cs]})
    assert len(ranks)==5 and len(positions)==5 and len(signs)==2
    # Hold every complete requested bank fixed and change the curve to make each
    # of its five equations correct. Search only the incidental bank seed for
    # these explicit controls; ordinary generation above uses unchanged seeds.
    controls=[]
    for index,record in enumerate(batch):
        params=record['generation']['parameters'];p=g.complete('q-107463',params)
        t=s.Rational(params['point']);e=g.inner(p).subs(g.X,t)
        ordinate=p['b']**e; factor=ordinate*s.log(p['b'])
        bank_values=[probe.parse(c[':answer/value']) for c in probe.choices(record)]
        wanted=sorted(int(s.simplify(s.diff(v,probe.x)/factor)) for v in bank_values)
        eligible=g.tangent_coefficients(p)
        for coefficient in wanted:
            alternate={**params,'a':coefficient,'d':int(e-coefficient*t)}
            other=g.complete('q-107463',alternate);g.guard('q-107463',other)
            pool=[a for a in eligible if a!=coefficient]
            bank_seed=next(seed for seed in range(50000)
                           if sorted([coefficient,*random.Random(seed).sample(pool,4)])==wanted)
            other['_bank_seed']=bank_seed
            changed=g.build('q-107463',other,record['generation']['seed'],'method:q-107463')
            math_check(changed)
            actual=[probe.parse(c[':answer/value']) for c in probe.choices(changed)]
            assert sorted(map(str,actual))==sorted(map(str,bank_values))
            controls.append({'original':record,'changed_target_same_bank':changed,
                             'original_coefficient':params['a'],'changed_coefficient':coefficient})
    save('same-bank-controls.json',controls)
    changed=[r['changed_target_same_bank'] for r in controls]
    save('controls.json',changed)
    assert probe.probes(changed)['correct']==0
    for index,record in enumerate(changed[:5]):
        graders.append({'label':'same-bank/'+str(index),'record':record,'checks':[
            {'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==probe.correct(record) else 'rejected'}
            for c in probe.choices(record)]})
    # Every supported hard parameter bucket has enough alternate curves; no
    # parameter domain was tightened to hide a failed or inconvenient bank.
    domains=[]
    for b in range(2,7):
        for point in [-1,0,1]:
            for exponent in range(-2,3):
                for a in range(-9,10):
                    if a==0:continue
                    p=g.complete('q-107463',dict(b=b,c=1,a=a,n=1,k=0,l=0,d=exponent-a*point,point=str(point)))
                    try:g.guard('q-107463',p)
                    except ValueError:continue
                    eligible=g.tangent_coefficients(p)
                    assert a in eligible and len(eligible)>=5
                    domains.append({'b':b,'point':point,'exponent':exponent,'a':a,'eligible_coefficients':eligible})
    save('bounded-domains.json',domains)
    # Unrelated supported bands keep the same visible tasks and answer values.
    other_bands=[]
    for level in ['easy','moderate']:
        for seed in [12,73,901]:
            before=old.generate(level,seed);after=g.generate(level,seed)
            for name in [':question/problem',':question/worked-solution',':question/difficulty']:
                assert before['question'][name]==after['question'][name]
            assert sorted(c[':answer/value'] for c in probe.choices(before))==sorted(c[':answer/value'] for c in probe.choices(after))
            other_bands.append({'level':level,'seed':seed,'unchanged_visible_task_and_bank':True})
    save('grader-input.json',graders)
    result={'passed':True,'negative_counts':{k:len(v['cases']) for k,v in negative.items()},
            'current_requested':4,'fresh':24,'same_bank_targets':len(controls),
            'source_supported_parameter_cases':len(domains),'rank_counts':dict(ranks),
            'position_counts':dict(positions),'slope_sign_counts':dict(signs),'cases':cases,
            'other_bands':other_bands,
            'limitation':'All lines pass through the target point; point membership alone does not identify an option. The learner must distinguish the correct tangent slope. Original source-bank repair is a separate guarded database action.'}
    save('verification.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','other_bands']}))


if __name__=='__main__':main()
