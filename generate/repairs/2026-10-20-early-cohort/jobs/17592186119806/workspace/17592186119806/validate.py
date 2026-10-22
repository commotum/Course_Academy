"""Independent displayed-math checks, exhaustive slots, replay, native grading."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sympy as sp

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('vector_combination',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q): return g.fingerprint(q)
def native(label,rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every bank option through actual application radio grader'} for a in f[':answer-field/choices']]}

def check(rec):
    q=rec['question'];meta=rec['generation'];sid=meta['bank_profile']
    # Read only displayed coefficients and vectors for the mathematical oracle.
    p,c,a,b,target=g.parse_problem(q[':question/problem'])
    solved=sp.ImmutableMatrix([sp.Rational(bi-p*ai,c) for ai,bi in zip(a,b)])
    assert all(v.is_Integer for v in solved) and p*a+c*solved==b
    expected=g.target_value(solved,target)
    f=q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    opts=[g.vector(z[':answer/value']) if target is None else sp.Integer(z[':answer/value']) for z in f[':answer-field/choices']]
    assert len(set(map(g.tex,opts)))==5
    correct=[v for z,v in zip(f[':answer-field/choices'],opts) if z[':answer/id']==f[':answer-field/correct'][1]]
    assert correct==[expected] and sum(v==expected for v in opts)==1
    # Inspect every concrete solution stage: supplied matrices, numerator, result.
    solution=q[':question/worked-solution'];matrices=[g.vector(z.group()) for z in g.MATRIX.finditer(solution)]
    assert len(matrices)==4
    reverse=' & ='+str(p)+'a-b' in solution
    assert matrices[:2]==([a,b] if reverse else [b,a])
    numerator=p*a-b if reverse else b-p*a
    divisor=-c if reverse else c
    assert matrices[2]==numerator and matrices[3]==solved and matrices[2]/divisor==solved
    coef=str(abs(c));signed='-' if c<0 and not reverse else ''
    assert 'x & ='+signed+r'\frac{1}{'+coef+'}' in solution
    if target is not None:
        end=solution.split('Therefore,')[1]
        assert g.target_tex(target) in end
        expression=end.split('=')[1]
        assert sp.sympify(expression)==expected and end.endswith('='+str(expected)+'.$')
    assert meta['correct_value']==g.tex(expected) and meta['mathematical_fingerprint']==fingerprint(q)
    assert meta['assets']==[] and rec['knowledge_point']['db_id']==g.KP_ID
    replay=g.generate('easy',meta['seed'],sid,meta['parameters'])
    assert replay==rec
    return rec

def fidelity(old,rec):
    check(rec);q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
    assert old[':question/problem']==q[':question/problem'] and old[':question/worked-solution']==q[':question/worked-solution']
    assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
    assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']

def main():
    replay=[];recipes=[];all_records=[];inputs=[];review=[];coverage={}
    for sid,old in sorted(g.CASES.items()):
        p,c,a,b,target=g.parse_problem(old[':question/problem']);solved=(b-p*a)/c;base=g.target_value(solved,target)
        src=check(g.generate('easy',0,sid,{'scale':1,'target':list(target) if target else None}));fidelity(old,src)
        replay.append({'source':sid,'template':g.template_id(sid),'profile':sid,'matched_choices':5,'matched_distractors':4,'complete_bank':True,'correct_designation':True,'prompt_exact':True,'solution_exact':True,'missing':[],'extra':[]})
        for a0 in old[':question/answer-fields'][0][':answer-field/choices']:
            val=g.vector(a0[':answer/value']) if target is None else sp.Integer(a0[':answer/value'])
            recipes.append({'source':sid,'field':'selection','source_answer_id':a0[':answer/id'],'source_value':a0[':answer/value'],'offset':g.tex(val-base),'recipe':'requested_value + scale * observed_offset','reproduces_complete_value':True,'interpretation':'whole observed affine-offset value pattern; underlying learner error unresolved'})
        cases=[]
        for k in (1,2,3):
            for t in g.eligible_targets(sid):
                r=check(g.generate('easy',0,sid,{'scale':k,'target':list(t) if t else None}));all_records.append(r);inputs.append(native(sid+' '+str(r['generation']['parameters']),r));cases.append(r)
                again=g.generate('easy',99,sid,r['generation']['parameters']);assert again['question'][':question/id']==r['question'][':question/id']
        coverage[sid]={'scales':[1,2,3],'eligible_targets':g.eligible_targets(sid),'sampled_targets':g.eligible_targets(sid),'unsampled_targets':[],'instances':len(cases)}
        variant=next(r for r in cases if r['generation']['parameters']['scale']==2 and (target is None or tuple(r['generation']['parameters']['target'])!=target))
        review.append('## '+sid+' ('+g.template_id(sid)+')\n\nSource replay\n\n'+g.markdown(src)+'\n\nChanged values'+(' and target' if target else '')+'\n\n'+g.markdown(variant))
        if target is not None:
            changed=next(t for t in g.eligible_targets(sid) if t!=target)
            r=check(g.generate('easy',0,sid,{'scale':1,'target':list(changed)}))
            assert g.parse_problem(r['question'][':question/problem'])[2:4]==(a,b)
            assert g.target_tex(changed) in r['question'][':question/problem'] and g.target_tex(changed) in r['question'][':question/worked-solution'].split('Therefore,')[1]
            # A stale final target or key must fail independent validation.
            import copy
            stale=copy.deepcopy(r);stale['question'][':question/worked-solution']=stale['question'][':question/worked-solution'].split('Therefore,')[0]+'Therefore,'+src['question'][':question/worked-solution'].split('Therefore,')[1]
            try:check(stale)
            except AssertionError:pass
            else:raise AssertionError('Stale target solution escaped validation')
    catalog=g.catalog();fps={fingerprint(r['question']) for r in catalog};assert len(fps)==len(catalog)
    for level in ('moderate','hard','unclassified'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported level generated')
    for params in ({'scale':0,'target':None},{'scale':4,'target':None},{'scale':2,'target':[0,0,'+']}):
        try:g.generate('easy',0,'q-34248',params)
        except ValueError:pass
        else:raise AssertionError('Invalid parameters allowed')
    try:g.batch('easy',len(catalog)+1)
    except ValueError:pass
    else:raise AssertionError('Finite bound ignored')
    source_fps={fingerprint(q) for q in g.CASES.values()}
    save('source-replay.json',{'passed':True,'matched_banks':13,'total_banks':13,'matched_distractors':52,'total_distractors':52,'profiles':replay,'excluded_sources':{'q-34574':'unrated; absent correct designation and worked solution; preserved and not admitted'}})
    save('choice-recipes.json',recipes);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save('previews.json',g.batch('easy',5,119806));(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('capabilities.json',{'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'finite_distinct_tasks':len(catalog),'finite_new_variants':{'easy':len(fps-source_fps)},'exceptions':[{'levels':['moderate','hard'],'scope':'bounded current source evidence and same-backbone generator','reason':'All 13 rated complete source questions are easy. Increasing dimensions, adding operations or introducing fractions to manufacture harder bands would exceed the extracted backbones. No evidence supports moderate/hard; reopen on new source evidence.','shortage_each':5,'filled':False}], 'policy':'Seed, choice order, profile identity and irrelevant scalar-query coordinates do not create mathematical novelty. Eligible sum pairs are unordered; subtraction pairs are ordered. Declared finite domain scale 1..3 is a conservative workload policy, not a mathematical impossibility claim.'})
    save('validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'exhaustive_profile_instances':len(all_records),'distinct_mathematical_tasks':len(catalog),'new_variants_excluding_sources':len(fps-source_fps),'complete_banks':'13/13','source_distractors':'52/52','source_fidelity':'prompt, solution and complete answer-bank exact at source parameters; source correct designation exact','correctness':'Independent displayed coefficient/vector solve; every solution matrix and division; target arithmetic; unique five-option bank; one correct designation','grading':'All five options of every exhaustive profile instance through course_academy_engine::learning::grade_field','slot_coverage':'all scales and all eligible same-operation component pairs; changed target with fixed vectors and stale-target negative control','plot_requirement':'none; source canonical SVG is standalone MathJax vector notation','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',ROOT/'generate/runs/current/check-engine')}})
    print(json.dumps({'passed':True,'exhaustive_instances':len(all_records),'distinct_tasks':len(catalog),'new_variants':len(fps-source_fps)}))

if __name__=='__main__':main()
