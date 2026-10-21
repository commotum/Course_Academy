#!/usr/bin/env python3
"""Independent checks read printed systems, matrix stages and row operations.
The generator metadata is never used to infer mathematical answers."""
import importlib.util,json,pathlib,re,subprocess,hashlib,sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).parent;sys.path.insert(0,str(D.parent));spec=importlib.util.spec_from_file_location('gen',D.parent/'17592186115242.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
k,x,y=s.symbols('k x y')

def parse(txt):
    txt=txt.strip().rstrip('.,').replace('\\\\','\\').replace('\\left','').replace('\\right','')
    txt=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',txt)
    txt=txt.replace('{','(').replace('}',')').replace('−','-')
    return parse_expr(txt,local_dict={'x':x,'y':y,'k':k},transformations=standard_transformations+(implicit_multiplication_application,))
def equations(block):
    body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,re.S).group(1)
    result=[]
    for row in body.split('\\\\'):
        row=row.replace('&','').strip().rstrip('.,');lhs,rhs=row.split('=');result.append(parse(lhs)-parse(rhs))
    return result

def matrix_text(body):return s.Matrix([[parse(t) for t in row.split('&')] for row in body.split('\\\\')])
def same(A,B):return A.shape==B.shape and all(s.simplify(a-b)==0 for a,b in zip(A,B))
def printed_check(rec):
    assert set(rec['knowledge_point'])=={'db_id','id','title'} and rec['knowledge_point']['db_id']==g.KP_ID
    q=rec['question'];f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
    prompt=q[':question/problem'];solution=q[':question/worked-solution']
    assert prompt.count('$$')==2 and solution.count('$$')==6
    eqs=equations(prompt)
    A=s.Matrix([[s.expand(z).coeff(x),s.expand(z).coeff(y)] for z in eqs]);bvec=s.Matrix([-s.expand(z).subs({x:0,y:0}) for z in eqs]);M=A.row_join(bvec)
    roots=s.solve(A.det(),k);assert len(roots)==1
    t=roots[0];dependent='consistent dependent' in prompt
    rank=A.subs(k,t).rank();aug=M.subs(k,t).rank()
    assert (rank==aug==1) if dependent else (rank<aug)
    values=[parse(z[':answer/value'].split('=',1)[1]) for z in f[':answer-field/choices']]
    assert len(set(values))==5
    correct=f[':answer-field/correct'][1]
    assert sum(a[':answer/id']==correct for a in f[':answer-field/choices'])==1
    for a,v in zip(f[':answer-field/choices'],values):
        assert (s.simplify(v-t)==0)==(a[':answer/id']==correct)
        ar=A.subs(k,v).rank();mr=M.subs(k,v).rank()
        assert ((ar==mr==1) if dependent else ar<mr)==(a[':answer/id']==correct)
    # All matrices read from actual rendered solution; duplicate initial stage retained.
    raw=re.findall(r'\\left\[\\begin\{array\}\{[^}]+\}(.*?)\\end\{array\}\\right\]',solution,re.S)
    mats=list(map(matrix_text,raw));assert same(mats[0],M) and same(mats[1],M)
    swap='↔' in solution
    assert len(mats)==(4 if swap else 3)
    current=M
    if swap:
        current=s.Matrix([list(M.row(1)),list(M.row(0))]);assert same(mats[2],current)
    operation=re.search(r'\{R\}_\{2\} & :=\{R\}_\{2\}(.*?)\{R\}_\{1\}',solution).group(1)
    m=parse(operation if operation not in ('+','-') else operation+'1')
    expected=current.copy();expected[1,:]=current.row(1)+m*current.row(0)
    assert same(mats[-1],expected)
    # Corresponding system must be exactly the row equations, not merely rank equivalent.
    blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
    final=equations(blocks[-1])
    for j,z in enumerate(final):
        expected_expr=mats[-1][j,0]*x+mats[-1][j,1]*y-mats[-1][j,2]
        assert s.simplify(z-expected_expr)==0
    # Every numerical final k statement and contradiction is independently derived.
    for v in re.findall(r'\$k=([^$]*?)\$',solution):assert s.simplify(parse(v)-t)==0
    for v in re.findall(r'\$0=([^$]*?)\$',solution):assert parse(v)==mats[-1][1,2]
    for z in re.findall(r'(?<!\$)\$([^$\n]*[xy][^$\n]*=[^$\n]*)\$(?!\$)',solution):
        lhs,rhs=z.rstrip('.,').split('=');eq=parse(lhs)-parse(rhs)
        assert s.simplify(eq-final[0])==0
    # Escaped visible left-system braces are valid, all TeX groups balance.
    for text in [prompt,solution]:
        assert not re.search(r'(?<!\\)\{(?=\\begin\{aligned\})',text)
        stripped=re.sub(r'\\[{}]','',text)
        assert stripped.count('{')==stripped.count('}')
    return t

