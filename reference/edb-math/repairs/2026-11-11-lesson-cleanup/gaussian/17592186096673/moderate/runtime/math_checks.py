"""Independent visible-content witnesses; SymPy verifies authored Fraction arithmetic."""
import re
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from fingerprint import answer_id, enum
X=S.symbols('x y z')

def scalar(value):
    value=value.strip().rstrip('.,')
    value=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',value)
    return S.Rational(value) if re.fullmatch(r'-?\d+(?:/\d+)?',value) else S.sympify(value)

def matrices(value):
    return [S.Matrix([[scalar(c) for c in row.split('&')] for row in body.split('\\\\')])
            for body in re.findall(r'\\begin\{array\}\{[^}]+\}(.*?)\\end\{array\}',value,re.S)]

def initial(question):
    prompt=question[':question/problem']; ms=matrices(prompt)
    if ms: return ms[0]
    body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',prompt,re.S).group(1)
    equations=[]
    for row in body.split('\\\\'):
        lhs,rhs=row.replace('&','').split('=')
        equations.append(parse_expr(lhs,local_dict=dict(zip('xyz',X)),transformations=standard_transformations+(implicit_multiplication_application,))-scalar(rhs))
    A,b=S.linear_eq_to_matrix(equations,X)
    return A.row_join(b)

def endpoint(answer):
    value=answer[':answer/value']; ms=matrices(value)
    if ms:return ms[0]
    if 'x=' in value:
        vals=re.findall(r'[xyz]=([^$]+)',value)
    else:
        value=value.replace(r'\left(', '').replace(r'\right)', '').strip('⟨⟩')
        vals=value.split(',')
    return S.Matrix([scalar(v) for v in vals])

def audit(record):
    q=record['question']; M=initial(q); A=M[:,:3]; b=M[:,3]
    assert M.shape==(3,4) and A.det()!=0
    # Independent forward elimination checks the structural target, not metadata.
    R=M.copy(); assert R[0,0]!=0
    R[0,:]=R[0,:]/R[0,0]
    for j in (1,2):R[j,:]=R[j,:]-R[j,0]*R[0,:]
    assert R[1,1]==0 and R[2,1]!=0 and R[1,2]!=0,'Missing required pivot repair'
    before_swap=R.copy();R.row_swap(1,2)
    for j in (1,2):R[j,:]=R[j,:]/R[j,j]
    solution=A.inv()*b
    f,=q[':question/answer-fields']; assert enum(f[':answer-field/type'])==':answer-field.type/radio'
    choices=f[':answer-field/choices'];assert len(choices)==5
    cid=answer_id(f[':answer-field/correct']); seen=set(); checks=[]
    for a in choices:
        e=endpoint(a); signature=str(e);assert signature not in seen;seen.add(signature)
        if e.shape==(3,4):
            valid=(e.rref()[0]==M.rref()[0]); good=(e==R)
        else:
            assert e.shape==(3,1);valid=(A*e==b);good=valid
        keyed=a[':answer/id']==cid
        assert valid==keyed and good==keyed,'Invalid or ambiguous visible choice'
        checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if valid else 'rejected','control':'correct' if valid else 'wrong','purpose':'Exact independent '+('row-equivalence and unit-pivot elimination' if e.shape==(3,4) else 'substitution into all three original equations')+' verifies this complete option.'})
    sol=q[':question/worked-solution']
    sms=matrices(sol); assert sms
    for m in sms:assert m.rref()[0]==M.rref()[0],'Worked matrix changes the system'
    assert sms[-1]==R
    solve='then solve' in q[':question/problem']
    key=next(a for a in choices if a[':answer/id']==cid)
    assert endpoint(key)==(solution if solve else R)
    if solve and key[':answer/value'].startswith(r'\left('):
        assert key[':answer/value'] in sol,'Final displayed tuple differs from key'
    if solve and 'Back substitute, starting with the last row:' in sol:
        body=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1]
        body=body.replace('\\\\','').replace('&','').replace(r'\quad','')
        body=re.sub(r'\\left|\\right','',body)
        for name,expression in re.findall(r'([xyz])\s*=(.*?)(?=[xyz]\s*=|$)',body,re.S):
            for side in expression.split('='):
                side=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',side.strip())
                value=parse_expr(side,transformations=standard_transformations+(implicit_multiplication_application,))
                assert S.simplify(value-solution['xyz'.index(name)])==0,'Incorrect displayed back substitution'
    assert not re.search(r'(zero pivot|second pivot|exchange|swap|R_[123])',q[':question/problem'],re.I)
    return {'initial':str(M),'solution':str(solution),'before_swap':str(before_swap),'echelon':str(R),'solution_matrices':len(sms),'endpoint':'solve' if solve else 'echelon','checks':checks}

def check_bank(record):
    from collections import Counter
    q=record['question'];solve='then solve' in q[':question/problem']
    f,=q[':question/answer-fields'];es=[endpoint(a) for a in f[':answer-field/choices']]
    zs=[e[2,0] if solve else e[2,3] for e in es]
    counts=Counter(zs)
    assert len(counts)>=2 and min(counts.values())>=2,'A last-coordinate calculation uniquely selects a full endpoint'
    return {str(k):v for k,v in counts.items()}
