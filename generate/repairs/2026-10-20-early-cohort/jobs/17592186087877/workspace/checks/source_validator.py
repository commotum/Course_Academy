#!/usr/bin/env python3
"""Independent printed-math, full source-bank, identity, and native-grader audit.
Raw source anomalies remain evidence exceptions; normal banks have no exceptions.
"""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent.parent/'17592186087877'
SCRIPT=ROOT.with_suffix('.py')
spec=importlib.util.spec_from_file_location('kp87877',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X;Y=g.Y;YP=g.YP
TRANSFORMS=standard_transformations+(implicit_multiplication_application,)

def group(text,pos):
    if text[pos]!='{':raise ValueError('expected TeX group at '+text[pos:])
    depth=1;j=pos+1
    while depth:
        if j>=len(text):raise ValueError('unbalanced group')
        depth+=(text[j]=='{')-(text[j]=='}');j+=1
    return text[pos+1:j-1],j

def clean(tex):
    tex=tex.replace('\\\\','\\').replace('\\u2061','').replace('\u2061','')
    tex=re.sub(r'\\(?:text|textrm)\{([^}]*)\}',r'\1',tex)
    tex=tex.replace('\\operatorname{ln}',r'\ln').replace('\\operatorname{cos}',r'\cos').replace('\\operatorname{sin}',r'\sin')
    # All generated/replayed logarithmic banks explicitly assume x>0.
    tex=re.sub(r'\\ln\s*\|([^|]+)\|',lambda m:r'\ln('+m[1]+')',tex)
    return tex.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(' ','').replace('{e}', 'e')

def expression(tex):
    tex=clean(tex).rstrip('.')
    # Differential of a product is interpreted directly using the product rule.
    # This parser has no dependency on generation parameters or computed factors.
    tex=tex.replace(r'\frac{dy}{dx}','yp').replace(r'\dfrac{dy}{dx}','yp')
    tex=re.sub(r'(?<=[A-Za-z0-9)])yp',r'*yp',tex)
    derivative=re.compile(r'\\(?:d?frac)\{d\}\{dx(?:\^\{2\})?\}')
    while (m:=derivative.search(tex)):
        if m.end()>=len(tex) or tex[m.end()]!='(':raise ValueError('derivative must have a grouped operand')
        j=m.end()+1;dep=1
        while dep:
            dep+=(tex[j]=='(')-(tex[j]==')');j+=1
        operand=expression(tex[m.end()+1:j-1])
        result=s.diff(operand,X)+s.diff(operand,Y)*YP
        if '2' in m.group():result/=2*X
        placeholder='z'+str(len(REPLACEMENTS));REPLACEMENTS[placeholder]=result
        tex=tex[:m.start()]+placeholder+tex[j:]
    def convert(z):
        out='';i=0
        while i<len(z):
            if z.startswith(r'\frac',i) or z.startswith(r'\dfrac',i):
                cmd=r'\dfrac' if z.startswith(r'\dfrac',i) else r'\frac'
                num,j=group(z,i+len(cmd));den,k=group(z,j)
                out+='(('+convert(num)+')/('+convert(den)+'))';i=k
            elif z[i]=='{':
                inside,j=group(z,i);out+='('+convert(inside)+')';i=j
            elif z.startswith(r'\cos',i):out+='cos';i+=4
            elif z.startswith(r'\sin',i):out+='sin';i+=4
            elif z.startswith(r'\ln',i):out+='log';i+=3
            elif z[i]=='^':out+='**';i+=1
            elif z[i]=='\\':raise ValueError('unsupported command in '+z[i:])
            else:out+=z[i];i+=1
        # Convert TeX e**(exponent) to exp(exponent), not Euler's constant power.
        return out
    converted=convert(tex)
    converted=re.sub(r"(cos|sin|log)x",r"\1(x)",converted)
    converted=re.sub(r"(?<=[\w)])(cos|sin|log)\(",r"*\1(",converted)
    locals={'x':X,'y':Y,'yp':YP,'e':s.E,'cos':s.cos,'sin':s.sin,'log':s.log,**REPLACEMENTS}
    value=parse_expr(converted,local_dict=locals,transformations=TRANSFORMS,evaluate=True)
    return s.expand(value)
REPLACEMENTS={}

def relation(tex):
    left,right=tex.split('=',1)
    return s.expand(expression(left)-expression(right))
def same_equation(a,b):
    if not a.has(YP) or not b.has(YP):return False
    ca,cb=a.coeff(YP),b.coeff(YP)
    return s.cancel(a.coeff(Y)/ca-b.coeff(Y)/cb)==0 and s.cancel(a.subs({Y:0,YP:0})/ca-b.subs({Y:0,YP:0})/cb)==0

def formatting(text,delimited=True):
    if delimited:assert text.count('$')%2==0
    depth=0
    for i,c in enumerate(text):
        if c=='{' and (i==0 or text[i-1]!='\\'):depth+=1
        if c=='}' and (i==0 or text[i-1]!='\\'):depth-=1
        assert depth>=0,(text,'early closing brace')
    assert depth==0,(text,'unbalanced braces')
    assert '+-' not in text and '--' not in text

def block_maths(text):return re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',text)

def verify_record(record,allow_raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];meta=record['generation']
    for k in (':question/problem',':question/worked-solution'):formatting(q[k])
    problem=q[':question/problem']
    spans=list(g.MATH_SPAN.finditer(problem))
    ode=next(m.group().strip('$\n') for m in spans if r'\frac{dy}{dx}' in m.group())
    ode=ode.split(',')[0]
    supplied=relation(ode)
    normalized=s.expand(supplied/supplied.coeff(YP))
    P=s.simplify(normalized.coeff(Y));Q=s.simplify(-normalized.subs({Y:0,YP:0}))
    # Derive I independently from the printed ODE's coefficients.
    I=s.simplify(s.exp(s.integrate(P,X)))
    expected=s.expand(I*YP+s.diff(I,X)*Y-I*Q)
    f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5
    correct=f[':answer-field/correct'][1]
    choices=f[':answer-field/choices']
    assert len({a[':answer/id'] for a in choices})==5
    values=[];good=[]
    for a in choices:
        formatting(a[':answer/value'],False)
        value=relation(a[':answer/value']);values.append(value)
        if same_equation(value,expected):good.append(a[':answer/id'])
        assert a[':answer/id']==g.identity(f[':answer-field/id']+'/'+a[':answer/value'])
    assert good==[correct],(meta,good,correct)
    duplicates=[(i,j) for i in range(5) for j in range(i) if same_equation(values[i],values[j])]
    if not allow_raw:assert not duplicates,(meta,duplicates)
    # Independently parse every displayed arithmetic equality in worked stages.
    stages=block_maths(q[':question/worked-solution'])
    odeblocks=0
    for block in stages:
        if 'P(x)' in block or r'\int' in block:continue
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        for row in block.split(r'\\'):
            row=row.replace('&','').strip().rstrip('.')
            if not row:continue
            if row.startswith('I(x)'):continue
            actual=relation(row)
            assert same_equation(actual,normalized),(meta,row,actual,normalized)
            odeblocks+=1
    assert odeblocks>=3
    # Parse integrating-factor stages separately, checking derivative logarithm.
    factorblock=next(b for b in stages if b.startswith(r'\begin{aligned}I(x)'))
    rows=factorblock.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    for row in rows:
        rhs=row.split('=',1)[1].strip()
        if 'P(x)' in rhs:continue
        if r'\int' in rhs:
            integrand=rhs.split(r'\int',1)[1].rsplit(r'\,dx',1)[0]
            assert s.simplify(expression(integrand)-P)==0
        else:
            value=expression(rhs)
            assert s.simplify(value-I)==0,(rhs,value,I)
    assert q[':question/id']==g.identity(json.dumps([g.VERSION,problem,q[':question/worked-solution'],sorted(a[':answer/value'] for a in choices),meta['domain']],ensure_ascii=False))
    assert r'\int I(x)Q(x)' not in q[':question/worked-solution'] and 'general solution' not in q[':question/worked-solution']
    return {'printed_equalities':odeblocks,'bank_choices':5,'equivalent_pairs':duplicates}

def prose(text):return g.MATH_SPAN.sub('<MATH>',text)
