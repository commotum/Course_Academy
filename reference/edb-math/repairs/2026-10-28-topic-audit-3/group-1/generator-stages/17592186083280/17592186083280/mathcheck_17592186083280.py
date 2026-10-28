"""Independent limited TeX reader: uses displayed expressions, not curve metadata."""
import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
T=s.Symbol('t',real=True)
def brace(text,start):
    assert text[start]=='{';depth=1;i=start+1
    while depth:
        if text[i]=='{':depth+=1
        if text[i]=='}':depth-=1
        i+=1
    return text[start+1:i-1],i

def expression(text):
    z=text.strip().rstrip('.,');z=re.sub(r'\\(?:begin|end)\{aligned\}','',z)
    z=re.sub(r'\\operatorname\{(ln|cos|sin)\}⁡',r'\1',z)
    z=z.replace('π','pi').replace(r'\pi','pi').replace(r'\ln','ln').replace(r'\cos','cos').replace(r'\sin','sin').replace(r'\cdot','*').replace(r'\times','*').replace(r'\,','').replace('⁡','')
    for command in ('frac','sqrt'):
        while '\\'+command in z:
            i=z.index('\\'+command);b=i+len(command)+1;arg,end=brace(z,b)
            if command=='frac':den,end=brace(z,end);new='(('+str(expression(arg))+')/('+str(expression(den))+'))'
            else:new='sqrt('+str(expression(arg))+')'
            z=z[:i]+new+z[end:]
    z=expression_text(z).strip().rstrip('.,')
    return parse_expr(z,local_dict={'t':T,'pi':s.pi,'e':s.E,'ln':s.log,'cos':s.cos,'sin':s.sin,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def expression_text(z):
    z=z.replace('{','(').replace('}',')').replace('^','**')
    z=re.sub(r'(sin|cos)\s*(\d+)t',r'\1(\2*t)',z)
    return z

def value_set(value):
    pieces=re.findall(r'\$t\s*=\s*([^$]+)\$',value)
    if not pieces:pieces=[value.split('=',1)[-1]]
    roots=[]
    for p in [item for piece in pieces for item in piece.split(',')]:
        if r'\pm' in p:
            e=expression(p.replace(r'\pm',''));roots.extend([-e,e])
        else:roots.append(expression(p))
    return tuple(sorted(set(roots),key=lambda q:float(q)))

def prompt_curve(record):
    text=record['question'][':question/problem'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
    z=blocks[0] if blocks else re.search(r'\$(x = .*?)\$',text).group(1)
    z=z.strip().rstrip('.')
    pair=z.split('y=',1) if 'y='in z else z.split('y =',1)
    x=pair[0].split('=',1)[1].replace(r'\,','').rstrip(' ,')
    y=pair[1]
    if r',\,'in y:y=y.split(r',\,',1)[0]
    elif ', 0 'in y:y=y.split(', 0 ',1)[0]
    if re.search(r'0<t<',z):domain=s.Interval.open(0,s.oo)
    elif '-\\infty'in z:domain=s.S.Reals
    elif not re.search(r'\\le t',z):domain=s.S.Reals
    else:
        interval=z.rsplit(r',\,',1)[-1] if r',\,'in z else z.rsplit(', ',1)[-1]
        m=re.search(r'(.*?)\s*\\le t\s*(<|\\le)\s*(.*)$',interval);assert m,z
        domain=s.Interval(expression(m[1]),expression(m[3]),right_open=m[2]=='<')
    return expression(x),expression(y),domain

def verify(record):
    q=record['question'];x,y,domain=prompt_curve(record);dx,dy=s.diff(x,T),s.diff(y,T)
    target=dx if 'horizontal'in q[':question/problem'] else dy
    other=dy if target==dx else dx
    roots=s.solveset(target,T,domain=domain)
    assert isinstance(roots,s.FiniteSet),(target,domain,roots)
    complete=tuple(sorted([r for r in roots if s.simplify(other.subs(T,r))!=0],key=lambda z:float(z)))
    # Public instances avoid zero/zero; stationary curves need a geometry/limit
    # analysis and are deliberately outside this lesson-grounded family domain.
    assert all(s.simplify(other.subs(T,r))!=0 for r in roots)
    assert complete==tuple(s.sympify(r)for r in record['generation']['roots']),(complete,record['generation']['roots'])
    incidental_bound=isinstance(domain,s.Interval) and domain.end.is_finite and target.is_polynomial(T) and s.solveset(target,T,domain=s.S.Reals)==s.FiniteSet(*complete)
    canonical={'orientation':'horizontal'if target==dx else'vertical','interval':None if incidental_bound else s.srepr(domain),'zero_candidates':[[s.srepr(r),s.simplify(other.subs(T,r))!=0]for r in complete]}
    assert canonical==record['generation']['mathematical_task']
    import hashlib,json
    assert hashlib.sha256(json.dumps(canonical,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==record['generation']['mathematical_fingerprint']
    fields=q[':question/answer-fields'];isblank=all(f[':answer-field/type'].endswith('/blank')for f in fields)
    chosen=[]
    for f in fields:
        sets=[value_set(a[':answer/value'])for a in f[':answer-field/choices']]
        assert len(sets)==len(set(sets)),sets
        if ':answer-field/correct'in f:
            correct=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
            chosen.extend(value_set(correct[':answer/value']))
            if not isblank:assert value_set(correct[':answer/value'])==complete,(correct,complete)
    if isblank:assert tuple(sorted(chosen,key=lambda z:float(z)))==complete
    sol=q.get(':question/worked-solution')
    if sol:
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
        dblock=blocks[0]
        parts=dblock.split(',\\,')
        for label,expected,part in zip(('x','y'),(dx,dy),parts):
            raw=part.split('=',1)[1];assert s.simplify(expression(raw)-expected)==0,(raw,expected)
        # Check the actual zero-solving equation before its implication.
        solve=blocks[1].split('⟹')[0]
        solve=re.sub(r'\\(?:begin|end)\{aligned\}','',solve)
        first=solve.split(r'\\')[0].replace('&','').replace(r'\,','').strip()
        left,right=first.split('=',1)
        assert s.simplify(expression(left)-expression(right)-target)==0,(first,target)
        family=record['generation']['template']
        if family=='cubic':assert re.search(r'\d+\(\{t\}\^\{2\}-\d+\)=0',first),first
        if family=='quadratic':assert blocks[1].count(r'\\')==2
        checks=blocks[-1];rows=re.sub(r'\\(?:begin|end)\{aligned\}','',checks).split(r'\\')
        expected_rows=4 if family=='two_period_trig' else 2 if family in ('cubic','shifted_trig','frequency_trig','legacy_trig') else 1
        assert len(rows)==expected_rows
        expected_equalities=2 if family in ('exponential','logarithmic','quadratic','frequency_trig','legacy_trig') else 1
        for row in rows:
            assert row.count('=')==expected_equalities
            m=re.search(r'\{([xy])\}\^\{′\}\((.*?)\)\s*(?:&\s*)?=(.*)',row)
            assert m,row
            r=expression(m[2]);expected=(dx if m[1]=='x'else dy).subs(T,r)
            chain=m[3].split(r'\ne')[0].rstrip(' ,')
            for rhs in chain.split('='):
                assert s.simplify(expression(rhs)-expected)==0,(rhs,expected)
        # Every complete conclusion set must match, not merely the aligned rows.
        end=sol.split('which confirms')[-1]
        vals=re.findall(r'\$t=(.*?)\$',end)
        if vals:
            seen=[]
            for v in vals:seen.extend(value_set('t='+v.rstrip('.')))
            assert tuple(sorted(seen,key=lambda z:float(z)))==complete,(end,seen,complete)
    return complete
