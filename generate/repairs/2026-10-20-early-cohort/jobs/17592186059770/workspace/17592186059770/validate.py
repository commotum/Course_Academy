#!/usr/bin/env python3
"""Read displayed equations/matrices independently, replay banks, and grade natively."""
import importlib.util,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def scalar(x):
    x=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',x.strip())
    assert re.fullmatch(r'[\d()*/+ .-]+',x),x
    return sp.Rational(sp.sympify(x,rational=True))
def matrix(text):
    text=text.strip()
    if text.startswith(r'\begin{bmatrix}'):
        assert text.endswith(r'\end{bmatrix}');body=text[len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')]
    else:
        m=re.search(r'\\begin\{array\}\{[c|]+\}(.*?)\\end\{array\}',text);assert m,text
        body=m[1]
    rows=[[scalar(cell) for cell in row.split('&')] for row in body.split(r'\\')]
    assert len({len(r) for r in rows})==1
    return sp.ImmutableMatrix(rows)
def expression(text):
    text=text.replace('&','').strip();text=re.sub(r'\{x\}_\{(\d)\}',r'x\1',text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',text)
    assert re.fullmatch(r'[a-z\d()*/+ .-]+',text),text
    local={x:sp.Symbol(x) for x in ('a','b','c','x1','x2','x3')}
    text=re.sub(r'(?<=[0-9)])(?=[a-z])','*',text)
    return sp.sympify(text,locals=local,rational=True)
def equations(text):
    m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S);assert m,text
    result=[]
    for row in m[1].split(r'\\'):
        lhs,rhs=row.split('=');result.append(sp.expand(expression(lhs)-expression(rhs)))
    return result

def task(q):
    exprs=equations(q[':question/problem'])
    names=['x1','x2','x3'] if '{x}_{1}' in q[':question/problem'] else ['a','b','c']
    syms=[sp.Symbol(s) for s in names];A=[];rhs=[]
    for expr in exprs:
        assert expr.free_symbols<=set(syms),'Different variable backbone'
        row=[expr.coeff(s) for s in syms];constant=expr.subs(dict.fromkeys(syms,0))
        assert sp.expand(expr-sum(v*s for v,s in zip(row,syms))-constant)==0
        A.append(row);rhs.append(-constant)
    template='coefficient' if 'coefficient matrix' in q[':question/problem'] else 'augmented'
    return template,A,rhs

def fingerprint(q):
    template,A,rhs=task(q)
    return g.mathematical_fingerprint(template,A,rhs)
def check(rec):
    q=rec['question'];template,A,rhs=task(q)
    assert len(A)==2 and len(A[0])==3
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
    parsed=[matrix(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(parsed))==5
    target=sp.ImmutableMatrix(A) if template=='coefficient' else sp.ImmutableMatrix([row+[v] for row,v in zip(A,rhs)])
    correct=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
    assert matrix(correct[0][':answer/value'])==target and sum(x==target for x in parsed)==1
    original=equations(q[':question/problem']);organized=equations(q[':question/worked-solution']);assert original==organized
    solution_matrices=re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}|\\left\[\\begin\{array\}.*?\\end\{array\}\\right\]',q[':question/worked-solution'],re.S)
    assert matrix(solution_matrices[0])==sp.ImmutableMatrix(A)
    assert matrix(solution_matrices[-1])==target
    assert rec['generation']['mathematical_fingerprint']==fingerprint(q)
    assert '$' not in correct[0][':answer/value']
    assert '![' not in q[':question/problem']
    return True

def engine_item(rec):
    f=rec['question'][':question/answer-fields'][0]
    return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned source-backed matrix radio choice'} for a in f[':answer-field/choices']]}
def grade(records,path):
    path.mkdir(parents=True,exist_ok=True);(path/'native-input.json').write_text(json.dumps([engine_item(r) for r in records],indent=2))
    subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
    x=json.loads((path/'native-report.json').read_text());assert x['documented_unresolved_checks']==0 and x['accepted_checks']==len(records) and x['rejected_checks']==4*len(records)
    return {'accepted_checks':x['accepted_checks'],'rejected_checks':x['rejected_checks'],'documented_unresolved_checks':0}
def main():
    source=json.loads((HERE/'source.json').read_text());qs={q.get(':question/math-academy-id'):q for q in source['record'][':knowledge-point/questions']}
    reports=[];records=[];review=[]
    for template,source_id in g.TEMPLATES.items():
        replay=g.generate('moderate',template=template,parameters=g.SOURCE_PARAMETERS[template]);check(replay)
        f=qs[source_id][':question/answer-fields'][0];rf=replay['question'][':question/answer-fields'][0]
        original=[matrix(a[':answer/value']) for a in f[':answer-field/choices']];generated=[matrix(a[':answer/value']) for a in rf[':answer-field/choices']]
        assert len(original)==len(generated)==5 and set(original)==set(generated)
        assert matrix(f[':answer-field/correct'][':answer/value'])==matrix(next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))
        assert equations(qs[source_id][':question/problem'])==equations(replay['question'][':question/problem'])
        assert equations(qs[source_id][':question/worked-solution'])==equations(replay['question'][':question/worked-solution'])
        reports.append({'template':template,'profile':source_id,'matched_distractors':4,'total_distractors':4,'complete_banks_matched':1,'complete_banks_total':1,'correct_designation_matched':True,'missing_options':[],'extra_options':[]})
        review += ['## '+template+' original',qs[source_id][':question/problem'],qs[source_id][':question/worked-solution'],'## Original-parameter replay',g.markdown(replay)]
        records.append(replay);params_seen={k:set() for k in g.SOURCE_PARAMETERS[template]}
        for seed in range(120):
            rec=g.generate('moderate',seed,template);check(rec);assert rec==g.generate('moderate',seed,template)
            for key,val in rec['generation']['parameters'].items():params_seen[key].add(val)
            records.append(rec)
        for key,observed in params_seen.items():assert len(observed)>5,(key,observed)
        reports[-1]['sampled_slot_values']={k:sorted(z) for k,z in params_seen.items()}
        # Change every numeric slot in isolation, independently reading prompt,
        # organization and matrices to catch stale references and keys.
        for key,val in g.SOURCE_PARAMETERS[template].items():
            p=dict(g.SOURCE_PARAMETERS[template]);p[key]=val+1 if val>0 else val-1
            changed=g.generate('moderate',template=template,parameters=p);check(changed)
            assert equations(changed['question'][':question/problem'])!=equations(replay['question'][':question/problem'])
            records.append(changed)
        for seed in (5,28):review+=['## Variant '+str(seed),g.markdown(g.generate('moderate',seed,template))]
    # Boundaries of every declared numeric slot, not only random variation.
    for template in g.TEMPLATES:
        for key in g.SOURCE_PARAMETERS[template]:
            bounds=(-15,-1) if key in ('d','r') else ((2,15) if template=='augmented' else (1,15))
            for bound in bounds:
                p=dict(g.SOURCE_PARAMETERS[template]);p[key]=bound
                if template=='coefficient' and p['a']==p['b']:continue
                rec=g.generate('moderate',template=template,parameters=p);check(rec);records.append(rec)
    native=grade(records,HERE/'reference/validation-grading')
    save('review.json',[g.generate('moderate',seed,t) for t in g.TEMPLATES for seed in (5,28)])
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'status':'passed','basis':source['basis'],'lineage':source['lineage'],'supported_levels':['moderate'],'records_checked':len(records),'fidelity':reports,'correctness':'Independent rendered-equation coefficient extraction, exact matrices, zero patterns and solution-stage equality','grading':native,'plots':'none; all generated visuals are standalone LaTeX mathematics','deterministic_replay':True,'single_slot_change_checks':9,'field_contract':'selection radio, five owned math choices, delimiter-free matrix values','distinctness':'Normalized coefficients for coefficient task; normalized supplied equations for augmented task. Irrelevant coefficient-task RHS, scaling aliases, seed, UUID and choice order excluded','unimplemented_observed_levels':['easy','hard'],'source_preserved':True})
    paths=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'check-engine.rs',HERE/'check-engine',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json',HERE/'replenish.py']
    save('freeze-hashes.json',{'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})
    print(json.dumps({'status':'passed','records_checked':len(records),'fidelity_banks':'2/2','distractors':'8/8','native':native}))
if __name__=='__main__':main()
