"""Independently read rendered matrices, equations, targets and complete answer banks."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('scalar',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def independent(rec):
    q=rec['question'];m=rec['generation'];assert rec==g.generate('easy',m['seed'],m['template'],m['parameters'])
    b,a=g.matrices(q[':question/problem']);ratios={y/x for x,y in zip(a,b) if x};assert len(ratios)==1 and all(y==0 for x,y in zip(a,b) if x==0)
    ratio=ratios.pop();assert ratio==sp.Rational(m['parameters']['scalar'])
    f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];radio=f[':answer-field/type'].endswith('/radio')
    vals=[g.parse(x[':answer/value'].split('=')[-1]) for x in bank];assert len(set(vals))==len(vals)==(5 if radio else 1)
    assert [x[':answer/id'] for x,v in zip(bank,vals) if v==ratio]==[f[':answer-field/correct'][1]]
    sol=q[':question/worked-solution'];ms=g.matrices(sol);assert ms==[a,a*g.k,a*g.k,b]
    tail=sol.split('Equating these elements, we get')[1];equation=tail.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    left,right=equation.split(r'\\');lhs,rhs=left.replace('&','').split('=');lhs2,rhs2=right.rstrip('.').replace('&','').split('=')
    assert g.parse(lhs).subs(g.k,ratio)==g.parse(rhs) and g.parse(lhs2)==g.k and g.parse(rhs2)==ratio
    i,j=m['parameters']['target'];assert g.parse(lhs)==a[i,j]*g.k and g.parse(rhs)==b[i,j]
    described=re.search(r'row \$(\d+)\$ and column \$(\d+)\$',sol)
    if described:assert [int(described[1])-1,int(described[2])-1]==[i,j]
    else:assert [i,j]==g.DEFAULTS[m['template']]['target']
    assert fingerprint(q)==m['mathematical_fingerprint']
    return rec
check=independent
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    if f[':answer-field/type'].endswith('/radio'):return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank'} for a in f[':answer-field/choices']]
    k=sp.Rational(rec['generation']['parameters']['scalar']);return [{'submitted':s,'expected':e,'purpose':'blank equivalent/incorrect through actual learner grader'} for s,e in [(str(k),'accepted'),(str(k*2)+'/2','accepted'),(str(k+1),'rejected'),('0','rejected')]]
def native(rec,label):return {'label':label,'record':rec,'checks':checks(rec)}
def main():
    inputs=[];replay=[];coverage={};review=[];recipes=[]
    for sid,src in g.CASES.items():
        r=independent(g.generate('easy',0,sid,g.DEFAULTS[sid]));f=r['question'][':question/answer-fields'][0];old=src[':question/answer-fields'][0]
        compact=lambda s:re.sub(r'\s+','',s)
        assert sorted(compact(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(compact(a[':answer/value']) for a in old[':answer-field/choices'])
        assert compact(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==compact(old[':answer-field/correct'][':answer/value'])
        assert g.matrices(src[':question/problem'])==g.matrices(r['question'][':question/problem'])
        oldsol=src[':question/worked-solution']
        if sid=='q-320536':oldsol=oldsol.replace('11 & 12 \\\\ 4 & -8','11 & 12 \\\\ -4 & -8').replace('11k & 12k \\\\ 4k & -8k','11k & 12k \\\\ -4k & -8k')
        assert g.matrices(oldsol)==g.matrices(r['question'][':question/worked-solution'])
        # Strip only TeX whitespace; all source instructional prose and ordered equations remain.
        assert compact(g.normalize_prose(oldsol))==compact(r['question'][':question/worked-solution'])
        assert compact(src[':question/problem'])==compact(r['question'][':question/problem'])
        replay.append({'source':sid,'complete_bank':True,'choices_matched':len(f[':answer-field/choices']),'distractors_matched':len(f[':answer-field/choices'])-1,'missing':[],'extra':[],'prompt_match':'TeX whitespace normalized','solution_match':'TeX whitespace normalized; documented sign correction' if sid=='q-320536' else 'TeX whitespace normalized'})
        for a in old[':answer-field/choices']:
            value=g.parse(a[':answer/value'].split('=')[-1]);correct=sp.Rational(g.DEFAULTS[sid]['scalar']);recipe=('0' if value==0 and sid=='q-69670' else 'k'+('+' if value-correct>=0 else '')+str(value-correct)) if len(old[':answer-field/choices'])>1 else 'k'
            recipes.append({'source':sid,'field':old[':answer-field/key'],'answer_id':a[':answer/id'],'value':a[':answer/value'],'profile':sid if len(old[':answer-field/choices'])>1 else None,'recipe':recipe,'interpretation':'observed offset pattern, psychological interpretation unresolved','reproduced':True})
        inputs.append(native(r,sid+' source replay'));targets=set();scalars=set();signs=set();unique=set()
        for seed in range(80):
            rec=independent(g.generate('easy',seed,sid));inputs.append(native(rec,sid+' '+str(seed)));p=rec['generation']['parameters'];targets.add(tuple(p['target']));scalars.add(p['scalar']);signs.add(tuple(sp.sign(x) for x in sp.Matrix(p['matrix'])));unique.add(fingerprint(rec['question']))
        original=sp.Matrix(g.DEFAULTS[sid]['matrix']);eligible={(i,j) for i in range(original.rows) for j in range(original.cols) if original[i,j]};assert targets==eligible
        for target in sorted(eligible):
            p=dict(g.DEFAULTS[sid],target=list(target));rec=independent(g.generate('easy',0,sid,p));inputs.append(native(rec,sid+' same data, target '+str(target)))
        boundary=[]
        for magnitude,scalar in ((1,5 if sid=='q-981' else -6 if sid=='q-69670' else '1/2' if sid=='q-320563' else 2),(12,9 if sid=='q-981' else -9 if sid=='q-69670' else '1/6' if sid=='q-320563' else 9)):
            d=sp.Rational(scalar).q;am=original.applyfunc(lambda x:sp.sign(x)*magnitude*d if x else 0)
            p={'matrix':[[str(am[i,j]) for j in range(am.cols)] for i in range(am.rows)],'scalar':str(scalar),'target':list(sorted(eligible)[-1])}
            rec=independent(g.generate('easy',0,sid,p));inputs.append(native(rec,sid+' boundary '+str(magnitude)));boundary.append(p)
        coverage[sid]={'sampled_targets':sorted(targets),'eligible_targets':sorted(eligible),'missing_targets':[],'scalars':sorted(scalars),'distinct_tasks':len(unique),'same_data_changed_target_checks':len(eligible),'boundary_cases':boundary}
        variant=independent(g.generate('easy',59741,sid));review += ['## '+sid+'\n\nSource replay (corrected where documented)\n\n'+g.markdown(r)+'\n\nSampled variant\n\n'+g.markdown(variant)]
        assert g.generate('easy',999,sid,g.DEFAULTS[sid])['question']==r['question']
    for level in ('moderate','hard','unclassified'):
        try:g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level admitted')
    save('source-replay.json',{'passed':True,'banks_matched':5,'banks_total':5,'source_distractors_matched':8,'source_distractors_total':8,'profiles':replay,'excluded':['q-11442','q-139431']});save('choice-recipes.json',recipes);save('slot-coverage.json',coverage);save('native-input.json',inputs)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'status':'pass','passed':True,'sampled_instances':400,'supported_levels':['easy'],'source_fidelity':'5/5 complete banks; 8/8 distractors; prompt and solution replay modulo TeX whitespace and documented source sign correction','correctness':'independent rendered matrix ratios; all bank values; all four solution matrices; final equation; target prose; deterministic replay','grading':'native grade_field complete radio banks and blank equivalent/incorrect checks','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'capabilities.json',ROOT/'generate/runs/current/check-engine']}})
if __name__=='__main__':main()
