"""Read printed matrix data and independently execute every displayed operation."""
import hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('row_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)

def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)

def evaluate(a,text):
    """Independent columnwise evaluation; do not use generator operation/apply."""
    text=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text).replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(' ','')
    result=a.copy()
    if '↔' in text:
        x,y=map(lambda z:int(z[1:])-1,text.split('↔'))
        result[x,:]=a[y,:];result[y,:]=a[x,:]
    else:
        lhs,rhs=text.split(':=');i=int(lhs[1:])-1
        rhs=re.sub(r'(\d|\))(?=r)',r'\1*',rhs)
        for j in range(3):result[i,j]=sp.sympify(rhs,locals={f'r{k+1}':a[k,j] for k in range(3)})
    return result

def independent(rec):
    q=rec['question'];meta=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID
    assert q[':question/difficulty']==':question.difficulty/moderate'
    assert rec==g.generate('moderate',meta['seed'],meta['template'],meta['parameters'])
    a,b=g.matrices(q[':question/problem']);assert a.shape==b.shape==(3,3) and a!=b
    assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5 and len({x[':answer/value'] for x in f[':answer-field/choices']})==5
    outcomes=[evaluate(a,x[':answer/value']) for x in f[':answer-field/choices']]
    matches=[x[':answer/id'] for x,out in zip(f[':answer-field/choices'],outcomes) if out==b]
    assert matches==[f[':answer-field/correct'][1]],'Ambiguous or incorrect complete bank'
    # All source distractors remain distinct mathematical transformations.
    assert len({tuple(out) for out in outcomes})==5,'Equivalent choices'
    sol=q[':question/worked-solution'];assert g.matrices(sol)==[a,b]
    changed=[i for i in range(3) if a[i,:]!=b[i,:]]
    pre=sol.split('By considering')[0]
    ordinal=('st','nd','rd')
    for i in range(3):assert ('$'+str(i+1)+'$'+ordinal[i]) in pre
    # Check which row(s) the introductory prose says have changed.
    changed_text=pre.split('The only row')[1]
    described={int(i)-1 for i in re.findall(r'\$([123])\$(?:st|nd|rd)',changed_text)}
    assert described==set(changed),'Stale prose targets'
    final=sol.split('Therefore, the required row operation is')[1].split('$$')[1].strip().rstrip('.')
    assert evaluate(a,final)==b,'Stale solution operation'
    assert meta['mathematical_fingerprint']==fingerprint(q)
    return rec

check=independent
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each choice through actual application radio grader'} for a in f[':answer-field/choices']]
def native(label,rec):return {'label':label,'record':rec,'checks':checks(rec)}

def main():
    # Current focused suite retains independent/evaluate above and writes only
    # workspace evidence. Legacy repository-relative publication paths are gone.
    import runpy
    runpy.run_path(str(HERE.parent / 'checks/validate.py'), run_name='__main__')

if __name__ == '__main__':
    main()
