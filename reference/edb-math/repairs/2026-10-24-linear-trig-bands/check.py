"""Inspect actual printed tasks/steps/banks and exercise sampler regressions."""
from collections import Counter,defaultdict
import copy
import importlib.util
import json
from pathlib import Path
import sys

import sympy as sp

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(H));sys.path.insert(0,str(ROOT))
from read_math import X,U,C,prompt,scalar,check,source_prompt,mathematical_key
from scripts.generator_publish import normalized_question


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def save(name,value):(H/name).write_text(json.dumps(value,default=str,indent=2)+'\n')


def main():
    inventory=json.loads((H/'source/inventory.json').read_text())
    excluded=[]
    for q in inventory['questions']+[inventory['canonical_example']]:
        body,_,lo,hi=source_prompt(q[':question/problem'])
        excluded.append(mathematical_key(body,lo,hi))
    path=H/'package/source-evidence.json';evidence=json.loads(path.read_text())
    evidence['excluded_practice_fingerprints']=sorted(set(excluded))
    path.write_text(json.dumps(evidence,indent=2)+'\n')
    g=module('linear_trig_candidate',H/'package/generator.py')
    coverage=defaultdict(Counter);equalities=0;all_rows=[];mathematical_keys=set()
    for band in g.CASES:
        for seed in (24681357,97531):
            rows=g.batch(band,12,seed);assert rows==g.batch(band,12,seed)
            keys=[r['generation']['mathematical_fingerprint'] for r in rows];assert len(set(keys))==len(keys)
            for row in rows:
                result=check(row);equalities+=result['equalities']
                meta=row['generation'];p=meta['parameters'];actual_fn=next(iter(result['integrand'].atoms(sp.sin,sp.cos))).func.__name__
                assert mathematical_key(result['integrand'],result['lower'],result['upper']) not in excluded
                assert actual_fn==p['function']
                assert sp.simplify(result['argument']-(sp.sympify(p['slope'])*X+sp.sympify(p['shift'])))==0
                coverage[band]['function:'+actual_fn]+=1;coverage[band]['case:'+meta['template']]+=1
                coverage[band]['response:'+meta['response']]+=1
                coverage[band]['slope:'+('negative' if sp.sympify(p['slope'])<0 else 'positive')]+=1
                if result['lower'] is None:coverage[band]['indefinite']+=1
                else:
                    coverage[band]['definite']+=1;coverage[band]['outcome:'+str(sp.sign(result['result']))]+=1
                all_rows.append(row);mathematical_keys.add(meta['mathematical_fingerprint'])
        assert coverage[band]['function:sin'] and coverage[band]['function:cos']
        assert coverage[band]['slope:negative'] and coverage[band]['slope:positive']
        assert coverage[band]['outcome:1'] and coverage[band]['outcome:-1']
        if band!='hard':assert coverage[band]['response:radio'] and coverage[band]['response:blank']
        if band=='easy':assert coverage[band]['indefinite'] and coverage[band]['outcome:0']
        if band=='hard':
            assert coverage[band]['response:radio']==0
            for row in [r for r in all_rows if r['question'][':question/difficulty'].endswith('/hard')]:
                result=check(row);values=[getattr(sp,'cos' if row['generation']['parameters']['function']=='sin' else 'sin')(
                    result['argument'].subs(X,bound)) for bound in (result['lower'],result['upper'])]
                assert {sp.simplify(abs(v)) for v in values}=={sp.sqrt(2)/2,sp.sqrt(3)/2}
    # Every response shape remains available within the easy definite subgroup.
    definite_blanks=[r for r in all_rows if r['generation']['template'].startswith('def_') and r['generation']['response']=='blank']
    assert {r['generation']['parameters']['function'] for r in definite_blanks}=={'sin','cos'}
    assert len({r['generation']['parameters']['amplitude'] for r in definite_blanks})>1
    # A controlled function change must update the primitive, sign and key.
    before=g.build('easy','indef_sin',('sin',sp.Integer(3),sp.Integer(-4),sp.Integer(5),None,None))
    after=g.build('easy','indef_cos',('cos',sp.Integer(3),sp.Integer(-4),sp.Integer(5),None,None))
    for row in (before,after):check(row)
    assert before['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']!=after['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
    negative_controls=[]
    # An altered substitution factor must fail the printed-derivation checker.
    broken=copy.deepcopy(before)
    broken['question'][':question/worked-solution']=broken['question'][':question/worked-solution'].replace(
        r'\mathrm{d}x=\left(- \frac{1}{4}\right)',r'\mathrm{d}x=\left(-4\right)')
    assert broken!=before
    try:check(broken)
    except AssertionError:negative_controls.append('wrong displayed substitution factor rejected')
    else:raise AssertionError('Checker accepted an incorrect printed substitution')
    # An easy case cannot be relabeled hard by choosing the hard case name.
    try:g.build('hard','compound_sin_positive',('sin',sp.Integer(2),sp.Integer(3),sp.Integer(0),sp.Integer(0),sp.pi/6))
    except ValueError:negative_controls.append('easy work relabeled hard rejected')
    else:raise AssertionError('Hard contract accepted easy work')
    try:g.batch('hard',201,0)
    except ValueError:negative_controls.append('unsupported requested capacity rejected')
    else:raise AssertionError('Capacity silently exceeded')
    # Reproduce the original frozen easy definite-blank family without changing
    # its archive or pretending its numerical correctness establishes variety.
    old=module('original_linear_trig',H/'original-generator.py')
    old.HERE=ROOT/'generate/scratch/17592186068915'
    old_blanks=[old.generate('easy',0,'q-350040',{'k':k}) for k in (2,5,12)]
    parsed=[source_prompt(r['question'][':question/problem']) for r in old_blanks]
    assert all(sp.simplify(f/next(iter(f.atoms(sp.sin))))==9 for f,_,_,_ in parsed)
    negative_controls.append('retained old family fails amplitude/function variety probe')
    # Explicit and independent hard example from the agreed proposal.
    explicit=g.build('hard','compound_sin_negative',('sin',sp.Rational(5,3),sp.Rational(-3,2),sp.pi,sp.pi/9,sp.pi/2))
    verified=check(explicit);assert sp.simplify(verified['result']-sp.Rational(5,9)*(sp.sqrt(2)+sp.sqrt(3)))==0
    all_rows.append(explicit)
    pool=[r for band in g.CASES for r in g.batch(band,5,24681357)]
    for row in pool:check(row)
    save('candidate-pool.json',pool);save('regression-samples.json',all_rows)
    save('render-input.json',[next(r for r in pool if r['generation']['template'].startswith('indef')),
        next(r for r in pool if r['generation']['template']=='def_cos'),
        next(r for r in pool if r['generation']['template'].startswith('shift')),
        next(r for r in pool if r['generation']['template'].startswith('fraction')),
        next(r for r in pool if r['generation']['template'].startswith('compound_sin_negative')),
        next(r for r in pool if r['generation']['template'].startswith('compound_cos_positive'))])
    grader=[]
    for index,row in enumerate(pool+[before,after,explicit]):
        checks=[];field=row['question'][':question/answer-fields'][0]
        if field[':answer-field/type']==':answer-field.type/radio':
            for answer in field[':answer-field/choices']:
                checks.append({'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if answer[':answer/id']==field[':answer-field/correct'][1] else 'rejected'})
        else:
            key=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
            value=scalar(key)
            wrong=-value if prompt(row['question'][':question/problem'])[2] is None else value+1
            checks=[{'submitted':key,'expected':'accepted'},{'submitted':sp.latex(sp.expand(value)),'expected':'accepted'},
                    {'submitted':sp.latex(wrong),'expected':'rejected'}]
        grader.append({'label':f'published band/shape {index}','record':row,'checks':checks})
    save('grader-input.json',grader)
    old_questions=[q for q in inventory['questions'] if not q.get(':question/math-academy-id')]
    save('retirement-candidates.json',old_questions)
    assert {q[':db/id'] for q in old_questions}=={17592186482716,17592186482718,17592186482722,17592186482724}
    report={'samples_checked':len(all_rows),'printed_equalities_checked':equalities,'unique_mathematical_samples':len(mathematical_keys),
        'coverage':{k:dict(v) for k,v in coverage.items()},'negative_controls':negative_controls,'old_variants_to_retire':len(old_questions),
        'candidate_pool_counts':dict(Counter(r['question'][':question/difficulty'] for r in pool)),
        'independent_checks':'Actual printed integrands, derivatives, transformed bounds, every evaluation row, final keys and all answer choices',
        'hard_calibration':'Authored compound of existing skills, explicitly approved design; zero imported hard anchors'}
    save('generator-verification.json',report);print(json.dumps(report))


if __name__=='__main__':main()
