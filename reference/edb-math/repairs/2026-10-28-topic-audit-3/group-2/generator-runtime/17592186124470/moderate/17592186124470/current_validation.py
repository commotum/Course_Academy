"""Read current source/instance displays independently; preserve stored identities."""
import importlib.util, re
from pathlib import Path
import sympy as s
_spec=importlib.util.spec_from_file_location('vector_chain_validation',Path(__file__).with_name('validate.py'))
v=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(v)
g=v.g

def objects(q):
    q=dict(q)
    q[':question/problem']=re.sub(r'\\mathbf\s*\{?([rijk])\}?',r'\1',q[':question/problem'])
    q[':question/problem']=re.sub(r'\br\s+\(t\)', 'r(t)',q[':question/problem'])
    fr,rr=g.prompt_parts(q)
    return g.read_scalar(fr),v.vec(rr)

def check_question(q):
    f,r=objects(q)
    grad=tuple(s.diff(f,z) for z in g.VARS)
    gr=tuple(s.expand_mul(z.subs(dict(zip(g.VARS,r)),simultaneous=True)) for z in grad)
    rd=tuple(s.diff(z,g.T) for z in r)
    ans=s.factor_terms(s.expand(sum(a*b for a,b in zip(gr,rd))))
    p=q[':question/problem'];solution=q[':question/worked-solution']
    for text in (p,solution):v.balanced(text)
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
    assert len(blocks)==5
    assert blocks[0]==r'\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).'
    allrows=[]
    for block in blocks[1:]:
        assert block.startswith(r'\begin{aligned}') and block.endswith(r'\end{aligned}')
        lhs,rhs=block[len(r'\begin{aligned}'):-len(r'\end{aligned}')].split(' & =',1)
        allrows.append((lhs,rhs.split(r' \\  & =')))
    assert [l for l,rs in allrows]==['∇f(x,y,z)','∇f(r(t))',r'{r}^{′}(t)',r'\frac{\text{d}}{\text{d}t}[f(r(t))]']
    for raw,z in zip(g.vector_parts(allrows[0][1][0]),g.VARS):
        prefix=r'\frac{∂}{∂'+str(z)+'}'
        raw=raw.lstrip('+')
        assert raw.startswith(prefix)
        assert g.equal(g.read_scalar(raw[len(prefix):]),f)
    for row in allrows[0][1][1:]:v.same_vec(v.vec(row),grad)
    for row in allrows[1][1]:v.same_vec(v.vec(row),gr)
    for raw,z in zip(g.vector_parts(allrows[2][1][0]),r):
        prefix=r'\frac{\text{d}}{\text{d}t}'
        raw=raw.lstrip('+')
        assert raw.startswith(prefix)
        assert g.equal(g.read_scalar(raw[len(prefix):]),z)
    for row in allrows[2][1][1:]:v.same_vec(v.vec(row),rd)
    rows=allrows[3][1];assert len(rows)>=3 and rows[0]==r'∇f(r(t))\cdot {r}^{′}(t)'
    left,end=v.group(rows[1],0);assert rows[1][end:].startswith(r'\cdot (')
    right,pos=v.group(rows[1],end+len(r'\cdot '));assert pos==len(rows[1])
    v.same_vec(v.vec(left),gr);v.same_vec(v.vec(right),rd)
    for row in rows[2:]:assert g.equal(g.read_scalar(row),ans),('scalar solution',row,ans)
    prose=next(p for p in solution.split('\n\n') if p.startswith('Next, we substitute'))
    inline=''.join(re.findall(r'\$(.*?)\$',prose.split(' into the above',1)[0])).replace(' and ','').replace(' ','')
    coords=re.findall(r'([xyz])=(.*?)(?=,[xyz]=|[xyz]=|$)',inline)
    assert len(coords)==3
    for (name,raw),expected in zip(coords,r):assert g.equal(g.read_scalar(raw.rstrip(',')),expected)
    assert q[':question/difficulty'] in [':question.difficulty/'+l for l in ('easy','moderate','hard')]
    assert len(q[':question/answer-fields'])==1
    field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio'
    choices=field[':answer-field/choices'];assert len(choices)==5
    expressions=[]
    for a in choices:
        assert a[':answer/type']==':answer.type/math';v.balanced(a[':answer/value'])
        assert '$' not in a[':answer/value'];expressions.append(g.read_scalar(a[':answer/value']))
    for i,a in enumerate(expressions):assert all(not g.equal(a,b) for b in expressions[i+1:])
    correct=[a[':answer/id'] for a,e in zip(choices,expressions) if g.equal(e,ans)]
    assert len(correct)==1 and field[':answer-field/correct']==[':answer/id',correct[0]]
    return ans
