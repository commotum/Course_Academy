"""Restricted TeX reader and algebra checks, independent of sampler metadata."""
import math
import re
import sympy as s
import read_printed as p


def scalar(text):
    text=text.replace(r'\ln u',r'\ln(u)').replace('&','').strip().rstrip('.')
    if text in('-','+'):return s.Integer(-1 if text=='-'else 1)
    return p.scalar(text)


def integral(text):
    t=text.replace(r'\left','').replace(r'\right','').replace(r'\,','')
    start=t.index(r'\int');prefix=t[:start].strip().rstrip('(').strip();factor=scalar(prefix)if prefix else s.Integer(1)
    index=start+4;lo=hi=None
    if t[index:index+1]=='_':
        lo,index=p.group(t,index+1);assert t[index]=='^';hi,index=p.group(t,index+1);lo,hi=scalar(lo),scalar(hi)
    match=re.search(r'\\mathrm\{d\}([xu])',t[index:]);assert match,t
    return factor*scalar(t[index:index+match.start()]),{'x':p.x,'u':p.u}[match[1]],lo,hi,factor


def equal(a,b):
    diff=s.trigsimp(s.expand(a-b))
    if diff==0:return True
    if diff.has(s.sin,s.cos,s.tan,s.sec,s.csc,s.cot)and s.trigsimp(diff.rewrite(s.sin))==0:return True
    return s.simplify(s.expand_log(diff,force=True)if diff.has(s.log)else diff)==0


def primitive(f,var):
    pairs=[(s.sin(var),-s.cos(var)),(s.cos(var),s.sin(var)),(s.sec(var)**2,s.tan(var)),
           (s.csc(var)**2,-s.cot(var)),(s.sec(var)*s.tan(var),s.sec(var)),
           (s.csc(var)*s.cot(var),-s.csc(var)),(1/var,s.log(var)),(s.Integer(1),var)]
    result=0
    for term in s.expand(f).as_ordered_terms():
        for integrand,F in pairs:
            coefficient=s.simplify(term/integrand)
            if not coefficient.has(var):result+=coefficient*F;break
        else:raise AssertionError(('unsupported transformed primitive',term))
    assert equal(s.diff(result,var),f)
    return result


def arguments(text):
    values=[]
    for match in re.finditer(r'\\(?:sin|cos|tan|sec|csc|cot)(?:\^\{?\d+\}?)?\s*',text):
        index=match.end()
        if text[index:index+1]not in ('{','('):continue
        value,end=p.group(text,index);value=scalar(value)
        if value.has(p.x):values.append(value)
    return values


def check(record):
    q=record['question'];problem=q[':question/problem'];sol=q[':question/worked-solution']
    body,var,lo,hi,_=integral(re.findall(r'\$\$\s*(.*?)\s*\$\$',problem,re.S)[0]);assert var==p.x
    inner=scalar(re.search(r'Let \$u=(.*?)\$\.',sol).group(1));blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
    du=scalar(blocks[0].split('=',1)[1]);assert equal(du,s.diff(inner,p.x)),('derivative',sol)
    substitution=next(block for block in blocks if block.count(r'\int')==2)
    substitution=substitution.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\\','').replace('&','')
    left,right=substitution.split('=',1)
    left_body,left_var,left_lo,left_hi,_=integral(left)
    assert left_var==p.x and equal(left_body,body)and left_lo==lo and left_hi==hi
    transformed,u,u0,u1,factor=integral(right);assert u==p.u
    assert equal(body,transformed.subs(p.u,inner)*du),('substitution',sol)
    if lo is not None:
        assert lo<hi and equal(u0,inner.subs(p.x,lo))and equal(u1,inner.subs(p.x,hi))
        bound=next(block for block in blocks if r'\Longrightarrow'in block)
        for row,a,b in zip(bound.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'),(lo,hi),(u0,u1)):
            lhs,rhs=row.replace('&','').split(r'\Longrightarrow')
            assert equal(scalar(lhs.split('=',1)[1]),a)and equal(scalar(rhs.split('=',1)[1]),b)
    field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
    key=next(a[':answer/value']for a in choices if a[':answer/id']==correct)
    easy=field[':answer-field/type']==':answer-field.type/radio'
    if easy:
        supplied=scalar(re.search(r'Use the substitution \$u=(.*?)\$',problem).group(1));assert equal(supplied,inner)
        values=[];matches=[]
        for a in choices:
            f,v,l,h_,_=integral(a[':answer/value']);assert v==p.u and not f.has(p.x)
            if l is None:
                ratio=s.trigsimp(f.subs(p.u,inner)*du/body);assert not ratio.has(p.x)
                value=s.simplify(ratio);is_correct=value==1
            else:
                F=primitive(f,p.u);value=s.simplify(F.subs(p.u,h_)-F.subs(p.u,l))
                expected=primitive(transformed,p.u);expected=s.simplify(expected.subs(p.u,u1)-expected.subs(p.u,u0))
                is_correct=equal(value,expected)
            assert not any(equal(value,other)for other in values),'Equivalent choices'
            values.append(value)
            if is_correct:matches.append(a[':answer/id'])
        assert matches==[correct],('ambiguous key',matches,correct)
        f,v,l,h_,_=integral(key);assert v==p.u and equal(f,transformed)and l==u0 and h_==u1
        assert blocks[-1].strip().rstrip('.')==key
        answer=None
    else:
        # Inspect the primitive formula explained in the worked solution.
        formula=next(b for b in blocks if b.lstrip().startswith(r'\int') and b.count(r'\int')==1 and b.strip().rstrip('.').endswith('+C')).strip().rstrip('.');given,antiderivative=formula.split('=',1)
        gf,gv,gl,gh,_=integral(given);assert gv==p.u and gl is None
        assert equal(s.diff(scalar(antiderivative),p.u),gf),'Incorrect worked-solution formula'
        if lo is not None:
            facts=re.search(r'Endpoint values: \$(.*?)\$',sol).group(1)
            for fact in facts.split(r',\quad '):
                lhs,rhs=fact.split('=',1);assert equal(scalar(lhs),scalar(rhs)),'Incorrect worked-solution endpoint value'
            evaluation=blocks[-2];lhs,rhs=evaluation.split('=',1)
            prefix,rest=lhs.split(r'\left[',1);prefix=prefix.replace(r'\left(','')
            printed_F=scalar(rest.split(r'\right]',1)[0])*(scalar(prefix)if prefix.strip()else 1)
            assert equal(s.diff(printed_F,p.u),transformed)
            expected=s.simplify(printed_F.subs(p.u,u1)-printed_F.subs(p.u,u0))
            assert equal(scalar(rhs),expected)
        else:
            integration=[block for block in blocks if block.count(r'\int')==1 and '='in block][-1]
            F=scalar(integration.split('=',1)[1]);assert equal(s.diff(F,p.u),transformed)
            expected=F.subs(p.u,inner).subs(p.C,0)
        answer=scalar(key);assert equal(answer,expected),('answer',key,expected)
        assert blocks[-1].strip().rstrip('.')==key+('+C'if lo is None else '')
        if lo is not None:assert not equal(answer,0)
        # Operator inputs remain visible. A CAS-normalized sign or phase must
        # not silently require another identity between prompt and answer.
        if lo is None:
            old_arguments=arguments(problem.split('You may use')[0])
            assert old_arguments and all(any(equal(a,b)for b in old_arguments)for a in arguments(key))
    if lo is not None:
        for atom in body.atoms(s.sec,s.csc,s.tan,s.cot):
            angle=atom.args[0];ends=sorted(float(s.N(angle.subs(p.x,v)))for v in(lo,hi))
            shift=float(s.pi/2)if atom.func in(s.sec,s.tan)else 0
            bins=[(v+shift)/float(s.pi)for v in ends]
            assert all(abs(v-round(v))>1e-9 for v in bins)and math.floor(bins[0])==math.floor(bins[1])
    # Independent workload checks use the parsed instance, not its metadata.
    kp=record['knowledge_point']['db_id'];band=q[':question/difficulty'].rsplit('/',1)[-1]
    if kp in(17592186068915,17592186068916):
        assert not du.has(p.x)and du.is_Integer and 1<=abs(du)<=4
        assert(du<0)==(band=='hard')
        A=s.trigsimp(body/(transformed/factor).subs(p.u,inner));assert A.is_Integer and 1<=A<=4
        if lo is not None:assert all(s.simplify(v/s.pi).q<=6 for v in(u0,u1))
    elif kp==17592186068917:
        assert lo is None
        if band=='hard':assert inner.is_Pow and inner.exp in(-1,s.Rational(1,2))
        else:assert s.Poly(inner,p.x).degree()in(2,3)and s.Poly(inner,p.x).LC()==1
    else:
        args=[atom.args[0]for atom in inner.atoms(s.sin,s.cos,s.sec,s.csc,s.tan,s.cot)]
        assert args and all(a in(p.x,p.x**2)for a in args)
    return {'key':key,'answer':answer,'body':body,'inner':inner,'du':du,'lower':lo,'upper':hi,'factor':factor}
