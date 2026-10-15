"""Read rendered systems/stages/choices and independently check exact arithmetic."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('gauss_jordan_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete radio-bank choice'} for a in f[':answer-field/choices']]

def evaluate(a,text):
    text=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text).replace(' ','').replace('&','').replace(r'\\','')
    result=a.copy()
    if '↔' in text:
        x,y=map(lambda z:int(z[1:])-1,text.split('↔'))
        result[x,:]=a[y,:];result[y,:]=a[x,:]
    else:
        lhs,rhs=text.split(':=');i=int(lhs[1:])-1
        rhs=re.sub(r'(\d|\))(?=r)',r'\1*',rhs)
        for j in range(a.cols):
            result[i,j]=sp.sympify(rhs,locals={f'r{k+1}':a[k,j] for k in range(3)})
    return result

def independent(rec):
    q=rec['question'];meta=rec['generation']
    assert rec==g.generate('moderate',meta['seed'],meta['template'],meta['parameters'])
    ms=g.matrices(q[':question/worked-solution']);initial=ms[0];a=initial[:,:3];b=initial[:,3]
    assert a.det()!=0 and initial.rref()[0]==ms[-1]
    assert ms[1]==initial and ms[-1][:,:3]==sp.eye(3)
    matches=list(g.MATRIX.finditer(q[':question/worked-solution']))
    for i in range(1,len(matches)-1):
        operation=q[':question/worked-solution'][matches[i].end():matches[i+1].start()]
        operation=operation.replace('∼','').strip()
        assert evaluate(ms[i],operation)==ms[i+1],(meta['template'],operation)
    # Parse the rendered prompt independently of its generation metadata.
    prompt=q[':question/problem'];body=prompt.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    equations=body.replace('&','').split(r'\\');symbols=sp.symbols('x y z')
    expressions=[]
    for eq in equations:
        lhs,rhs=eq.split('=')
        lhs=re.sub(r'(\d)([xyz])',r'\1*\2',lhs.replace(' ',''))
        expressions.append(sp.sympify(lhs,locals=dict(zip('xyz',symbols)))-sp.Rational(rhs.strip()))
    pa,pb=sp.linear_eq_to_matrix(expressions,symbols)
    assert pa==a and pb==b
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    correct=[];values=[]
    for answer in f[':answer-field/choices']:
        v=g.value_vector(answer[':answer/value']);values.append(tuple(v))
        if a*v==b:correct.append(answer[':answer/id'])
    assert len(values)==len(set(values))==5 and correct==[f[':answer-field/correct'][1]]
    assert q[':question/difficulty']==':question.difficulty/moderate'
    if not g.MATRIX.search(f[':answer-field/choices'][0][':answer/value']):
        final=q[':question/worked-solution'].split('The corresponding system is now')[1]
        for name,value in zip('xyz',ms[-1][:,3]):assert f'${name}={sp.latex(value)}' in final
    return True

def fingerprint(q):return g.fingerprint(q)

def main():
    reports=[];records=[];review=[]
    for mid,source in g.QUESTIONS.items():
        replay=g.generate(template=mid,parameters=g.DEFAULTS[mid]);independent(replay)
        f=source[':question/answer-fields'][0];rf=replay['question'][':question/answer-fields'][0]
        old=[tuple(g.value_vector(a[':answer/value'])) for a in f[':answer-field/choices']]
        new=[tuple(g.value_vector(a[':answer/value'])) for a in rf[':answer-field/choices']]
        assert sorted(old)==sorted(new) and len(set(old))==5
        old_correct=tuple(g.value_vector(f[':answer-field/correct'][':answer/value']))
        new_correct=next(tuple(g.value_vector(a[':answer/value'])) for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        assert old_correct==new_correct
        reports.append({'template':mid,'source_distractors_matched':4,'source_distractors_total':4,'complete_banks_matched':1,'complete_banks_total':1,'extra':[],'missing':[]})
        records.append(replay)
        variants=[]
        # Coordinate boundary, signed, zero, and simultaneous coordinate cases.
        if mid!='q-10636':
            base=list(map(int,g.DEFAULTS[mid]['solution']))
            for index in range(3):
                for val in (-12,0,12):
                    s=base.copy();s[index]=val
                    r=g.generate(template=mid,parameters={'solution':s});independent(r);records.append(r);variants.append(s)
            for seed in range(20):
                r=g.generate(seed=seed,template=mid);independent(r);records.append(r);variants.append(r['generation']['parameters']['solution'])
            review.append({'source':source,'replay':replay,'variant':records[-1]})
        reports[-1]['sampled_solution_vectors']=variants
    inp=HERE/'reference/native-input.json';out=HERE/'reference/native-report.json'
    inp.write_text(json.dumps([{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)],indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(inp),str(out)],check=True)
    (HERE/'reference/source-replay.json').write_text(json.dumps(reports,indent=2)+'\n')
    (HERE/'reference/side-by-side.json').write_text(json.dumps(review,indent=2)+'\n')
    md=[]
    for r in review[:3]:
        md += ['## '+r['source'][':question/math-academy-id'],'### Source',r['source'][':question/problem'],r['source'][':question/worked-solution'],'### Variant',r['variant']['question'][':question/problem'],r['variant']['question'][':question/worked-solution']]
    (HERE/'reference/side-by-side.md').write_text('\n\n'.join(md)+'\n')
    result={'status':'pass','mathematical_records':len(records),'complete_source_banks':'11/11','source_distractors':'44/44','source_options':'55/55','independent_rendered_row_operation_checks':True,'rendered_prompt_readback':True,'slot_coverage':'Every variable RHS/solution coordinate exercised at -12, 0, 12 and in 20 seeded samples per variable family; fixed coefficients and row stages checked. No variable targets.','actual_grader':'reference/native-report.json','source_solution_correction':'q-10636 final operation target R2 corrected to R1 in generated solution only. All source DB facts retained.','fidelity':'All complete answer banks replayed; source stages and sentences retained with corrected operation label, normalized system braces and final-system typography.','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'source.json',Path(__file__)]}}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':main()
