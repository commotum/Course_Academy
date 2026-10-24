"""Read the actual restricted TeX independently of generator metadata."""
import re
import hashlib
import json
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X,U,C=sp.symbols('x u C',real=True)


def group(text,index):
    assert text[index]=='{',(text,index)
    depth=1;end=index+1
    while depth:
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[index+1:end-1],end


def scalar(text):
    text=text.replace(r'\,','').strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\pi','pi')
    # Expand nested TeX fractions and roots from the outside, recursively.
    pattern=re.compile(r'\\(?:d?frac|sqrt)')
    while match:=pattern.search(text):
        index=match.end()
        while text[index].isspace():index+=1
        first,index=group(text,index)
        if match[0]==r'\sqrt':replacement='sqrt('+str(scalar(first))+')'
        else:
            while text[index].isspace():index+=1
            second,index=group(text,index)
            replacement='(('+str(scalar(first))+')/('+str(scalar(second))+'))'
        text=text[:match.start()]+replacement+text[index:]
    text=text.replace(r'\sin','sin').replace(r'\cos','cos').replace('{','(').replace('}',')')
    assert '\\' not in text,text
    return parse_expr(text,local_dict={'x':X,'u':U,'C':C,'pi':sp.pi,'sin':lambda z:sp.sin(z,evaluate=False),'cos':lambda z:sp.cos(z,evaluate=False),'sqrt':sp.sqrt},
        transformations=standard_transformations+(implicit_multiplication_application,))


def integral(text):
    text=text.replace('&','').strip().rstrip('.')
    start=text.index(r'\int');prefix=text[:start];index=start+4;lower=upper=None
    if text[index:index+1]=='_':
        lower,index=group(text,index+1);assert text[index]=='^'
        upper,index=group(text,index+1);lower,upper=scalar(lower),scalar(upper)
    match=re.search(r'\\(?:mathrm|text)\{d\}([xu])',text[index:]);assert match,text
    variable={'x':X,'u':U}[match[1]]
    body=text[index:index+match.start()].strip()
    coefficient=scalar(prefix) if prefix.strip() else sp.Integer(1)
    return coefficient*scalar(body),variable,lower,upper


def prompt(problem):
    block=re.findall(r'\$\$\s*(.*?)\s*\$\$',problem,re.S)[0]
    return integral(block)


def source_prompt(problem):
    text=problem.replace('⁡','').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
    text=text.replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace('z','x')
    text=text.replace(r'\text{d}x',r'\mathrm{d}x').replace(r'\textrm{d}x',r'\mathrm{d}x')
    text=re.sub(r'\\(?:textrm|mathrm)\s+d\s*x',lambda _:r'\mathrm{d}x',text)
    text=re.sub(r'\\dfrac\s+([xu])\s+(\d+)',r'\\frac{\1}{\2}',text)
    text=re.sub(r'(?<![A-Za-z])dx',lambda _:r'\mathrm{d}x',text)
    return integral(text[text.index(r'\int'):])


def mathematical_key(body,lo,hi):
    return hashlib.sha256(json.dumps([sp.srepr(sp.expand(sp.expand_trig(body))),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)]).encode()).hexdigest()


def integrate_linear(body,variable,lo=None,hi=None):
    atoms=list(body.atoms(sp.sin,sp.cos));assert len(atoms)==1,body
    atom=atoms[0];arg=atom.args[0];slope=sp.diff(arg,variable)
    assert slope!=0 and not slope.has(variable) and sp.diff(arg,variable,2)==0
    amplitude=sp.simplify(body/atom);assert not amplitude.has(variable)
    primitive=-amplitude/slope*sp.cos(arg) if atom.func==sp.sin else amplitude/slope*sp.sin(arg)
    return primitive if lo is None else sp.simplify(primitive.subs(variable,hi)-primitive.subs(variable,lo))


def expression(text):
    text=text.replace(r'\left','').replace(r'\right','').replace('&','').strip().rstrip('.')
    if r'\int' in text:
        body,var,lo,hi=integral(text)
        return integrate_linear(body,var,lo,hi)
    if '[' in text:
        prefix,rest=text.split('[',1);inner,tail=rest.split(']',1)
        assert tail.startswith('_'),tail
        lo,index=group(tail,1);assert tail[index]=='^'
        hi,end=group(tail,index+1);assert not tail[end:].strip(),tail
        primitive=scalar(inner);coefficient=scalar(prefix) if prefix.strip() else 1
        return sp.simplify(coefficient*(primitive.subs(U,scalar(hi))-primitive.subs(U,scalar(lo))))
    return scalar(text)


def check(record):
    q=record['question'];body,var,lo,hi=prompt(q[':question/problem']);assert var==X
    result=integrate_linear(body,X,lo,hi)
    atom=next(iter(body.atoms(sp.sin,sp.cos)));arg=atom.args[0]
    blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
    derivative,dx=blocks[0].split(r',\qquad')
    assert sp.simplify(scalar(derivative.split('=',1)[1])-sp.diff(arg,X))==0
    dx=dx.split('=',1)[1].split(r'\mathrm{d}u')[0]
    assert sp.simplify(scalar(dx)*sp.diff(arg,X)-1)==0
    equalities=2
    if lo is not None:
        rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
        for row,endpoint in zip(rows,(lo,hi)):
            lhs,rhs=row.split(r'\Longrightarrow',1)
            assert sp.simplify(scalar(lhs.split('=',1)[1].split('&')[0])-endpoint)==0
            first,last=rhs.split('u=',1)[1].split('=')
            assert sp.simplify(scalar(first)-arg.subs(X,endpoint))==0
            assert sp.simplify(scalar(last)-arg.subs(X,endpoint))==0
            equalities+=2
    derivation=blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
    final=None
    for row in derivation.split(r'\\'):
        for part in row.replace('&','').split('='):
            if not part.strip():continue
            value=expression(part).subs(U,arg)
            if lo is None:assert sp.trigsimp(sp.diff(value,X)-body)==0,(part,value,body)
            else:assert sp.simplify(value-result)==0,(part,value,result)
            final=value;equalities+=1
    for field in q[':question/answer-fields']:
        correct=field[':answer-field/correct'][1];answers=[]
        for answer in field[':answer-field/choices']:
            value=scalar(answer[':answer/value'])
            matches=sp.trigsimp(sp.diff(value,X)-body)==0 if lo is None else sp.simplify(value-result)==0
            answers.append((answer[':answer/id'],matches,value))
        assert [aid for aid,matches,_ in answers if matches]==[correct],(q[':question/id'],answers)
        keyed=next(value for aid,_,value in answers if aid==correct)
        assert sp.simplify(final-keyed)==0 or (lo is None and sp.trigsimp(sp.diff(final-keyed,X))==0)
    return {'equalities':equalities,'result':result,'integrand':body,'argument':arg,'lower':lo,'upper':hi}
