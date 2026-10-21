"""Independent visible-record checks retained from review-0; no runtime imports."""
import collections,re
import sympy as S
y=S.Symbol('y');x=S.Symbol('x')
def expr(v):
    v=v.strip().replace(' ','').replace(r'\,','').replace('−','-')
    v=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',v)
    v=re.sub(r'(?<=[0-9)])(?=[xy])','*',v)
    return S.sympify(v,locals={'x':x,'y':y})
def mats(v):
    return [S.Matrix([[expr(c) for c in row.strip().split('&')] for row in body.split(r'\\')]) for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',v,re.S)]
def family(v):
    mm=mats(v)
    if mm:
        m=mm[-1]
        return list(m) if m.shape==(2,1) else None
    m=re.search('⟨(.*?)⟩',v)
    if m:
        return [expr(c) for c in m.group(1).replace(r'\,','').split(',')]
    return None
def keypos(r):
    f=r['question'][':question/answer-fields'][0]
    return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def signature(r):
    q=r['question'];a=mats(q[':question/problem'])[0]
    return ('ref' if 'then find' not in q[':question/problem'] and 'reduce' in q[':question/problem'] else 'solution', tuple(str(v) for v in a[:,:2]))
def shortcut(r):
    """No prompt, generation metadata, labels, IDs or correct key are read."""
    bank=r['question'][':question/answer-fields'][0][':answer-field/choices']
    ms=[mats(a[':answer/value']) for a in bank]
    if all(m and m[-1].shape==(2,3) for m in ms):
        rows=[tuple(m[-1][0,:]) for m in ms];modal=collections.Counter(rows).most_common(1)[0][0]
        picks=[i for i,m in enumerate(ms) if rows[i]==modal and list(m[-1][1,:])==[0,0,0]]
        return picks, 'modal top row plus all-zero bottom row'
    fs=[family(a[':answer/value']) for a in bank]
    af=[(i,f[0]) for i,f in enumerate(fs) if f and f[1]==y and S.diff(f[0],y)!=0]
    constants=[S.sign(e.subs(y,0)) for i,e in af];slopes=[S.sign(S.diff(e,y)) for i,e in af]
    if not af:return [],'majority intercept and slope signs'
    cs=collections.Counter(constants).most_common();ss=collections.Counter(slopes).most_common()
    if (len(cs)>1 and cs[0][1]==cs[1][1]) or (len(ss)>1 and ss[0][1]==ss[1][1]):return [],'majority intercept and slope signs'
    cm=collections.Counter(abs(e.subs(y,0)) for i,e in af).most_common(1)[0][0]
    sm=collections.Counter(abs(S.diff(e,y)) for i,e in af).most_common(1)[0][0]
    return [i for i,e in af if S.sign(e.subs(y,0))==cs[0][0] and S.sign(S.diff(e,y))==ss[0][0] and abs(e.subs(y,0))==cm and abs(S.diff(e,y))==sm], 'majority signs with modal coefficient magnitudes among affine options'
def math_record(r):
    q=r['question'];a=mats(q[':question/problem'])[0];ref=a.rref()[0]
    f=q[':question/answer-fields'][0];isref=signature(r)[0]=='ref';valid=[];checks=[]
    for c in f[':answer-field/choices']:
        v=c[':answer/value']
        if isref:
            b=mats(v)[-1];ok=b==ref
        else:
            b=family(v);ok=b is not None and b[1].has(y) and all(S.simplify(a[i,0]*b[0]+a[i,1]*b[1]-a[i,2])==0 for i in range(2))
        valid.append(bool(ok))
    solution=q[':question/worked-solution'];badmat=[]
    for n,b in enumerate(mats(solution)):
        if b.shape==(2,3) and b.rref()[0]!=ref:badmat.append(n)
        if b.shape==(2,1) and b[0]!=x and b[1]==y and any(S.simplify(a[i,0]*b[0]+a[i,1]*y-a[i,2])!=0 for i in range(2)):badmat.append(n)
    # Independently check scalar equations in the solution, including repeated explanatory prose.
    badeq=[]
    expected=S.simplify((a[0,2]-a[0,1]*y)/a[0,0])
    for m in re.finditer(r'(?<![0-9A-Za-z])(x(?:\s*[+\-]\s*\d*y)?)\s*&?=\s*([+\-\d y]+)',solution):
        left=expr(m[1]);right=expr(m[2]);res=S.simplify((left-right).subs(x,expected))
        if res!=0:badeq.append({'equation':m[0],'residual':str(res)})
    return {'question_id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'valid_choices':valid,'key_position':keypos(r)+1,'unique_correct':valid.count(True)==1 and valid[keypos(r)],'invalid_solution_matrix_indices':badmat,'invalid_scalar_equations':badeq,'pass':valid.count(True)==1 and valid[keypos(r)] and not badmat and not badeq}
