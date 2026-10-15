"""Frozen private exact parser for this restricted linear-equation grammar."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

def parameters(problem):
    compact = re.sub(r'\s+', '', problem)
    match = re.search(r'(-?\d*)\(([pkmqr])([+-]\d+)\)([xuvzw])([+-]\d+)=(-?\d+)', compact)
    assert match, problem
    scale, parameter, shift, variable, left, right = match.groups()
    return dict(variable=variable, parameter=parameter, scale=int(scale or 1), shift=int(shift), left=int(left), right=int(right))

def expr(text):
    text = re.sub(r'\{\{(.*?)\}_\{⏟\}\}_\{[ab]\}', r'\1', text)
    text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', text.strip().rstrip('.'))
    assert re.fullmatch(r'[A-Za-z0-9+*/().\s-]+', text), text
    return parse_expr(text, transformations=standard_transformations+(implicit_multiplication_application,), local_dict={c:sp.Symbol(c) for c in 'xuvzwpkmqrab'})

def rendered_math(record):
    q=record['question']; p=parameters(q[':question/problem'])
    displays=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S)
    assert len(displays)==1
    lhs,rhs=map(expr,displays[0].split('='));x,k=sp.Symbol(p['variable']),sp.Symbol(p['parameter'])
    delta=sp.expand(lhs-rhs);coefficient=delta.coeff(x);constant=delta.subs(x,0)
    assert sp.Poly(delta,x).degree()==1 and constant!=0 and coefficient==p['scale']*(k+p['shift'])
    roots=sp.solve(coefficient,k);assert len(roots)==1;root=roots[0]
    assert sp.solveset(sp.Eq(lhs.subs(k,root),rhs),x,domain=sp.S.Reals)==sp.S.EmptySet
    assert sp.solveset(sp.Eq(lhs.subs(k,root+1),rhs),x,domain=sp.S.Reals)!=sp.S.EmptySet
    assert re.search(r'\$'+p['parameter']+r'=\$\s*\{\{field-1\}\}',q[':question/problem'])
    assert 'where $'+p['parameter']+'$ is a constant.' in q[':question/problem']
    assert 'equation in the variable $'+p['variable']+',$' in q[':question/problem']
    sol=q[':question/worked-solution'];stages=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
    assert len(stages)==4 and stages[0]=='ax=b'
    assert 'where $a$ and $b$ are constants, and $b\\ne 0.$ If $a=0,$ then the equation has no solution.' in sol
    assert f'form $a{p["variable"]}=b:$' in sol
    def lines(stage):
        assert stage.startswith(r'\begin{aligned}') and stage.endswith(r'\end{aligned}')
        return stage[len(r'\begin{aligned}'):-len(r'\end{aligned}')].split(r'\\')
    reduction=lines(stages[1]);assert len(reduction)==3
    for line in reduction:
        a,b=map(expr,line.replace('&','').split('='));assert sp.expand(a-b-delta)==0,line
    a,b=map(expr,stages[2].split('='));assert b==0 and sp.solve(a-b,k)==roots
    solving=lines(stages[3]);assert len(solving)==(2 if p['scale']==1 else 4)
    for line in solving:
        a,b=map(expr,line.replace('&','').split('='));assert sp.solve(a-b,k)==roots,line
    if p['scale']!=1:
        assert r'\frac{0}{'+str(p['scale'])+'}' in solving[1]
    # Last line must identify the requested parameter and its actual numeric root.
    a,b=map(expr,solving[-1].replace('&','').split('='));assert a==k and b==root
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];answers=f[':answer-field/choices'];assert len(answers)==1
    assert f[':answer-field/type']==':answer-field.type/blank' and f[':answer-field/key']=='field-1'
    assert answers[0][':answer/type']==':answer.type/math' and expr(answers[0][':answer/value'])==root
    assert f[':answer-field/correct']==[':answer/id',answers[0][':answer/id']]
    assert q[':question/problem'].count('{{field-1}}')==1
    return p,int(root)
