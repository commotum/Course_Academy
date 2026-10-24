#!/usr/bin/env python3
"""Scalar surface integrals; frozen math basis 1356. No database writes.
Each source has an operative final-chain mask, not a generic integration chain.
Normal variants vary rectangle endpoints within the source polynomial workload.
Historical scalar banks are opaque evidence profiles, never sampled for learning.
Easy is authored: supplied norm, canonical cancellation to a single linear term.
Moderate retains supplied norms; hard computes full tangent/cross/norm stages.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186172131-source-policy.json'))
    raise SystemExit(0)

import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
DIR=Path(__file__).with_suffix(''); SNAPSHOT=json.loads((DIR/'source.json').read_text()); KP=SNAPSHOT['record']
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
u,v,x,y,z,theta=s.symbols('u v x y z theta',real=True)
VERSION='surface-family-masks-v2'
# family: coordinates, scalar, original rectangle, extracted factor, reduced integrand, primitive convention
DATA={
'q-160834':([2*u-v,3*u+2,u+2*v],2*x+y+z,[0,1,-1,1],s.sqrt(70),8*u+2,'product'),
'q-160835':([u,v,6-3*u-2*v],4*x*y,[0,2,0,3],s.sqrt(14),4*u*v,'split2'),
'q-167649':([x,2*x*x*s.cos(theta),2*x*x*s.sin(theta)],x*(y*y+z*z)/s.sqrt(16*x*x+1),[0,1,0,2*s.pi],1,8*x**7,'charge'),
'q-161127':([u+v,u,v],x*x-2*y*z,[-1,1,0,1],s.sqrt(3),u*u+v*v,'nested'),
'q-161180':([u-v,2*u+2*v,2*v],x+2*y-z,[0,1,0,2],6,5*u+v,'nested'),
'q-161182':([u,u+v,v],6*x*y*z,[0,1,0,1],6*s.sqrt(3),u*u*v+u*v*v,'nested'),
'q-161209':([u+v,u-v,0],x*y+z,[0,1,0,2],2,u*u-v*v,'nested'),
'q-161212':([u,u+v,2*v],2*x*z,[0,2,0,2],3,4*u*v,'split2'),
'q-161242':([2*u,-3*v,4*v],x*(y+z),[0,2,0,2],5,4*u*v,'split2'),
'q-161245':([2*u+v,2*u-2*v,u+2*v],x*x-z*z,[-1,1,1,2],9,3*u*u-3*v*v,'nested'),
'q-161181':([2*u+v,2*u+v,-v],3*x-2*y+3*z,[-1,1,-1,0],4*s.sqrt(2),u-v,'nested'),
'q-161179':([u+v,3*v,2*u-v],x+y+z,[0,1,0,1],9*s.sqrt(6),u+v,'nested'),
'q-161185':([u,2*v,6*v],x*y+x*z,[0,1,0,2],16*s.sqrt(10),u*v,'separated'),
}
DATA={k:(list(map(s.sympify,a)),s.sympify(b),list(map(s.sympify,c)),s.sympify(d),s.sympify(e),f) for k,(a,b,c,d,e,f) in DATA.items()}
LEVEL={k:SOURCES[k][':question/difficulty'][':db/ident'].split('/')[-1] for k in DATA}
ORIGINAL={k:dict(zip(('ua','ub','va','vb'),map(str,d[2]))) for k,d in DATA.items()}
ORIGINAL['q-167649']['k']='1'

def tex(e):return s.latex(s.sympify(e)).replace(' ','')
def scalar_factor(e):
    e=s.sympify(e);return '('+tex(e)+')' if e.could_extract_minus_sign() else tex(e)

def uid(e):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+e))
def scalar_parse(t):
    t=t.strip().replace(' ', '').replace(r'\theta','theta')
    def group(i):
        assert t[i]=='{'; j=i+1;depth=1
        while depth:
            if t[j]=='{':depth+=1
            if t[j]=='}':depth-=1
            j+=1
        return t[i+1:j-1],j
    out='';i=0
    while i<len(t):
        if t.startswith('\\frac',i):
            a,j=group(i+5);b,i=group(j);out+='('+str(scalar_parse(a))+')/('+str(scalar_parse(b))+')'
        elif t.startswith('\\sqrt',i):
            a,i=group(i+5);out+='sqrt('+str(scalar_parse(a))+')'
        elif t.startswith('\\pi',i):out+='pi';i+=3
        else:out+=t[i];i+=1
    from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
    return parse_expr(out.replace('{','(').replace('}',')').replace('^','**'),local_dict={'u':u,'v':v,'x':x,'y':y,'z':z,'theta':theta},transformations=standard_transformations+(implicit_multiplication_application,))

def mathematics(t,p):
    R,F,B,C,H,style=DATA[t]
    if style=='charge':F=F*s.sympify(p['k']);H=H*s.sympify(p['k'])
    a,b,c,d=[s.sympify(p[k]) for k in ('ua','ub','va','vb')];aa,bb=(x,theta) if style=='charge' else (u,v)
    ru=s.Matrix(R).diff(aa);rv=s.Matrix(R).diff(bb);cross=ru.cross(rv);norm=s.sqrt(s.trigsimp(cross.dot(cross)))
    pull=s.simplify(F.subs({x:R[0],y:R[1],z:R[2]}, simultaneous=True))
    J=s.integrate(H,(aa,a,b));P=s.integrate(J,bb);value=s.simplify(C*s.integrate(J,(bb,c,d)))
    return dict(R=R,F=F,ru=ru,rv=rv,cross=cross,norm=norm,pull=pull,H=H,C=C,J=J,P=P,value=value,bounds=(a,b,c,d),variables=(aa,bb),style=style,k=s.sympify(p.get('k',1)))

def validate_parameters(t,p):
    if set(p)!=set(('ua','ub','va','vb','k') if t=='q-167649' else ('ua','ub','va','vb')):raise ValueError('exact rectangle parameter keys required')
    a,b,c,d=map(s.sympify,[p[k] for k in ('ua','ub','va','vb')])
    if t=='q-167649':
        if not s.sympify(p['k']).is_Integer or not 1<=s.sympify(p['k'])<=8:raise ValueError('charge density coefficient 1..8')
        if a!=0 or b not in (s.Rational(1,2),1,s.Rational(3,2),2) or c!=0 or d!=2*s.pi:raise ValueError('charge x endpoint/angle bounds')
    else:
        if any(not e.is_Rational or abs(e)>3 or e.q>2 for e in (a,b,c,d)) or not(a<b and c<d) or b-a>3 or d-c>3:raise ValueError('rational half-unit endpoints, magnitude/width at most 3')
        # Preserve easy/method-specific symmetry and zero-lower product convention.
        if DATA[t][5] in ('split2','product','separated') and (a!=0 or c!=0) and t!='q-160834':raise ValueError('product families retain zero lower limits')
        if t in ('q-161127','q-161181','q-161245') and a!=-b:raise ValueError('source symmetric inner interval')
    return {k:str(s.sympify(p[k])) for k in p}

def sample(t,rng):
    if t=='q-167649':return dict(zip(('ua','ub','va','vb','k'),map(str,[0,rng.choice([s.Rational(1,2),1,s.Rational(3,2),2]),0,2*s.pi,rng.randrange(1,9)])))
    vals=[s.Rational(i,2) for i in range(-6,7)]; a=rng.choice(vals[:-1]); b=rng.choice([e for e in vals if a<e and e-a<=3]);c=rng.choice(vals[:-1]);d=rng.choice([e for e in vals if c<e and e-c<=3])
    if DATA[t][5] in ('split2','separated'):a=c=0;b=rng.choice(vals[7:]);d=rng.choice(vals[7:])
    if t in ('q-161127','q-161181','q-161245'):b=rng.choice(vals[7:10]);a=-b
    return dict(zip(('ua','ub','va','vb'),map(str,[a,b,c,d])))

def mask_bounds(text,p):
    for var,lo,hi in [('u','ua','ub'),('v','va','vb')]:
        text=re.sub(r'-?\d+\\le '+var+r'\\le -?\d+',lambda m:tex(p[lo])+r'\le '+var+r'\le '+tex(p[hi]),text)
    return text

def polytex(expr,var,ascending=False,rational_inline=False):
    terms=s.Poly(s.expand(expr),var).terms();terms=sorted(terms,key=lambda e:e[0][0],reverse=not ascending)
    out=''
    for (power,),coeff in terms:
        if coeff==0:continue
        varpart=('{' +str(var)+'}^{'+str(power)+'}' if power!=1 else str(var))
        if power and abs(coeff).is_Rational and abs(coeff).q!=1 and not rational_inline:
            numerator=('' if abs(coeff).p==1 else str(abs(coeff).p))+varpart
            term=r'\frac{'+numerator+'}{'+str(abs(coeff).q)+'}'
        else:term=tex(abs(coeff)) if power==0 else ('' if abs(coeff)==1 else tex(abs(coeff)))+varpart
        out+=('-' if coeff.could_extract_minus_sign() else ('+' if out else ''))+term
    return out or '0'

def evaluated_components(P,var,end):
    # Never simplify the endpoint as one value: each signed primitive component remains.
    terms=sorted(s.Poly(s.expand(P),var).terms(),key=lambda e:e[0][0])
    values=[s.simplify(coeff*end**power[0]) for power,coeff in terms]
    return '+'.join('('+tex(e)+')' if e.could_extract_minus_sign() else tex(e) for e in values) or '0'

def source_arithmetic_components(P,var,end):
    values=[s.simplify(coef*end**power[0]) for power,coef in sorted(s.Poly(s.expand(P),var).terms(),key=lambda e:e[0][0])]
    return ''.join(('-' if e.could_extract_minus_sign() else '+' if i else '')+tex(-e if e.could_extract_minus_sign() else e) for i,e in enumerate(values)) or '0'

def integral_mask(t,m,raw=False):
    """Parameterize source final block, retaining every factorization/order/primitive row."""
    block=SOURCES[t][':question/worked-solution'].split('$$')[-2];rows=block.replace('\\begin{aligned}','').replace('\\end{aligned}','').strip().split(r' \\ ')
    a,b,c,d=m['bounds'];C,H,J,P,style=m['C'],m['H'],m['J'],m['P'],m['style'];aa,bb=m['variables']
    if style=='charge':
        k=m['k']
        for i in range(1,5):rows[i]=rows[i].replace(r'4{x}^{5}',tex(4*k)+r'{x}^{5}').replace(r'8{x}^{7}',tex(8*k)+r'{x}^{7}').replace(r'[{x}^{8}]','['+('' if k==1 else tex(k))+r'{x}^{8}]')
    def ints(row):
        found=list(re.finditer(r'\{\\int \}_\{[^{}]*\}\^\{[^{}]*\}',row));order=[bb,aa] if len(found)==2 and style=='nested' or len(found)==2 and style=='separated' and rows.index(row)==3 else [aa,bb]
        if len(found)==1:order=[bb] if style=='nested' else [aa]
        for match,var in reversed(list(zip(found,order))):
            lo,hi=(a,b) if var==aa else (c,d);row=row[:match.start()]+r'{\int }_{'+tex(lo)+'}^{'+tex(hi)+(' ' if hi.has(s.pi) else '')+'}'+row[match.end():]
        return row
    for i,row in enumerate(rows):
        if i>=3:rows[i]=ints(row)
    # Primitive-bound masks are complete bracket components, never blind short-expression edits.
    for i,row in enumerate(rows):
        def bracket(match):
            body,wrapper,oldlo,oldhi=match.groups();var=aa if ('u' in body or style=='charge' and 'x' in body) else bb
            if t=='q-160834' and body=='u' and r'\cdot [u]' in row:var=bb
            lo,hi=(a,b) if var==aa else(c,d)
            lolabel=oldlo.split('=',1)[0]+'=' if '=' in oldlo else ''
            hilabel=oldhi.split('=',1)[0]+'=' if '=' in oldhi else ''
            return '['+body+']'+wrapper+'_{'+lolabel+tex(lo)+'}^{'+hilabel+tex(hi)+(' ' if hi.has(s.pi) else '')+'}'
        rows[i]=re.sub(r'\[(.*?)\](\}?)_\{([^{}]*)\}\^\{([^{}]*)\}',bracket,row)
    if style=='nested':
        oldJ={'q-161127':r'\frac{2}{3}+2{v}^{2}','q-161180':r'\frac{5}{2}+v','q-161182':r'\frac{v}{3}+\frac{{v}^{2}}{2}','q-161209':r'\frac{1}{3}-{v}^{2}','q-161245':r'2-6{v}^{2}','q-161181':r'0-2v','q-161179':r'\frac{1}{2}+v'}[t]
        newJ=polytex(J,bb,True)
        if t=='q-161181' and newJ.startswith('-'):newJ='0'+newJ
        rows[5]=rows[5].replace(oldJ,newJ)
        oldP={'q-161127':r'\frac{2}{3}v+\frac{2}{3}{v}^{3}','q-161180':r'\frac{5v}{2}+\frac{{v}^{2}}{2}','q-161182':r'\frac{{v}^{2}}{6}+\frac{{v}^{3}}{6}','q-161209':r'\frac{v}{3}-\frac{{v}^{3}}{3}','q-161245':r'2v-2{v}^{3}','q-161181':r'-{v}^{2}','q-161179':r'\frac{v}{2}+\frac{{v}^{2}}{2}'}[t]
        rows[6]=rows[6].replace(oldP,polytex(P,bb,True,t=='q-161127'))
        rows[6]=re.sub(r'(\]\}?)_\{[^{}]*\}\^\{[^{}]*\}',lambda hit:hit[1]+'_{'+tex(c)+'}^{'+tex(d)+'}',rows[6])
        high=source_arithmetic_components(P,bb,d);low=source_arithmetic_components(P,bb,c);lowvalue=s.simplify(P.subs(bb,c))
        endpoint=tex(s.simplify(P.subs(bb,d)-lowvalue))
        if t=='q-161127':rows[7]=r' & ='+tex(C)+'('+high+')-'+('0' if lowvalue==0 else tex(C)+'('+low+')')
        elif t in ('q-161180','q-161209'):rows[7]=r' & ='+tex(C)+'['+high+(('-('+low+')') if lowvalue!=0 else '')+']'
        elif t=='q-161182':rows[7]=r' & ='+tex(C)+'('+high+(('-('+low+')') if lowvalue!=0 else '')+')'
        elif t=='q-161245':rows[7]=r' & ='+tex(C)+r'\cdot ('+endpoint+')'
        else:rows[7]=r' & ='+tex(C)+r'\cdot '+scalar_factor(s.sympify(P.subs(bb,d)-lowvalue))
    elif style in ('split2','separated','product'):
        f1=2*u if style=='split2' else u if style=='separated' else H
        f2=2*v if style=='split2' else v if style=='separated' else s.Integer(1)
        i1=s.integrate(f1,(u,a,b));i2=s.integrate(f2,(v,c,d));idx=6 if style=='separated' else 5
        rows[idx]=r' & ='+tex(C)+r'\cdot '+scalar_factor(i1)+r'\cdot '+scalar_factor(i2)
    else:rows[5]=r' & =('+tex(s.sympify(m.get('k',1))*b**8)+'-'+tex(s.sympify(m.get('k',1))*a**8)+r')\cdot ('+tex(d)+' -'+tex(c)+')'
    rows[-1]=r' & ='+tex(m['value'])+(' ' if t=='q-167649' else '')+('.' if rows[-1].endswith('.') else '')
    # Add component-wise BOTH-endpoint evaluation without replacing source operations.
    if not raw:
        if style=='nested':
            Pu=s.integrate(H,aa)
            detail=r' & ='+tex(C)+r'{\int }_{'+tex(c)+'}^{'+tex(d)+'}[('+evaluated_components(Pu,aa,b)+')-('+evaluated_components(Pu,aa,a)+r')]\text{d}v'
            rows.insert(5,detail)
            rows.insert(-2,r' & ='+tex(C)+'[('+evaluated_components(P,bb,d)+')-('+evaluated_components(P,bb,c)+')]')
        elif style in ('split2','separated','product'):
            f1=2*u if style=='split2' else u if style=='separated' else H;f2=2*v if style=='split2' else v if style=='separated' else s.Integer(1)
            p1=s.integrate(f1,u);p2=s.integrate(f2,v)
            rows.insert(-2,r' & ='+tex(C)+'[('+evaluated_components(p1,u,b)+')-('+evaluated_components(p1,u,a)+r')]\cdot [('+evaluated_components(p2,v,d)+')-('+evaluated_components(p2,v,c)+')]')
    return '\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n'

def source_solution(t,m,p,raw):
    sol=SOURCES[t][':question/worked-solution'];old=sol.split('$$')[-2];sol=sol.replace(old,integral_mask(t,m,raw));sol=mask_bounds(sol,p)
    if t=='q-167649':
        sol=sol.replace('x\\in [0,1]','x\\in [0,'+tex(p['ub'])+']')
        k=s.sympify(p['k'])
        last=sol.rfind('$$');start=sol.rfind('$$',0,last);prefix=sol[:start];final=sol[start:]
        prefix=prefix.replace(r'\frac{x({y}^{2}+{z}^{2})}',r'\frac{'+tex(k*x)+r'({y}^{2}+{z}^{2})}')
        prefix=prefix.replace(r'\frac{x((2',r'\frac{'+tex(k*x)+r'((2')
        prefix=prefix.replace(r'4{x}^{5}',tex(4*k)+r'{x}^{5}').replace(r'8{x}^{7}',tex(8*k)+r'{x}^{7}').replace(r'[{x}^{8}]','['+('' if k==1 else tex(k))+r'{x}^{8}]')
        sol=prefix+final
    if not raw:
        sol=sol.replace(r'\sqrt{{1}^{2}+-{1}^{2}+-{1}^{2}}',r'\sqrt{{1}^{2}+(-1)^{2}+(-1)^{2}}')
        sol=sol.replace(r'\cdot [u]_',r'\cdot [v]_') if t=='q-160834' else sol
        sol=re.sub(r'D=\{\(u,v\)(.*?)\},',lambda m:r'D=\{(u,v)'+m[1]+r'\},',sol)
    return sol

def operation_bank(t,m):
    """Five-option complete method banks. Each wrong value is an actual changed operation."""
    a,b,c,d=m['bounds'];aa,bb=m['variables'];pull,norm=m['pull'],m['norm'];correct=m['value'];integ=lambda h:s.simplify(s.integrate(h,(aa,a,b),(bb,c,d)))
    if m['style']=='charge':return [correct] # observed blank
    no_metric=integ(pull);squared_metric=integ(pull*norm**2)
    if t in ('q-160835','q-161212','q-161242','q-161185'):
        coefficient=s.Poly(pull,u,v).coeff_monomial(u*v)
        return [correct,no_metric,squared_metric,integ(u*v*norm),integ(4*pull*norm)]
    if t=='q-161181':return [correct,no_metric,integ((u-v)*norm),0,-correct]
    terms=s.Add.make_args(s.expand(pull));first=terms[0];last=terms[-1]
    if t in ('q-161127','q-161182','q-161179'):
        nodiv=sum(coef*(powers[0]+1)*(powers[1]+1)*u**powers[0]*v**powers[1] for powers,coef in s.Poly(pull,u,v).terms())
        return [correct,no_metric,squared_metric,integ((pull-first)*norm),integ(nodiv*norm)]
    if t=='q-161209':return [correct,no_metric,squared_metric,integ((u*u+v*v)*norm),3*correct]
    return [correct,no_metric,squared_metric,integ((pull-first)*norm),integ((pull-last)*norm)]

def make_record(level,t,p,profile,seed,prompt,solution,bank,raw=False):
    bank=[s.simplify(e) for e in bank]
    if len(set(bank))!=len(bank):raise ValueError('whole-bank collision')
    normalized={'prompt':prompt,'solution':solution,'bank':sorted(map(str,bank)),'level':level,'version':VERSION}
    key=json.dumps(normalized,sort_keys=True);qid=uid(key);fid=uid(qid+':field');answers=[{':answer/id':uid(fid+':'+str(a)),':answer/type':':answer.type/math',':answer/value':tex(a)} for a in bank]
    if raw:
        for a,orig in zip(answers,SOURCES[t][':question/answer-fields'][0][':answer-field/choices']):
            # Original notation is an explicit symbolic print mask, evaluated at any changed input.
            target=scalar_parse(orig[':answer/value']);anchor=mathematics(t,ORIGINAL[t])['value'];ratio=s.simplify(target/anchor)
            correct_index=next(i for i,o in enumerate(SOURCES[t][':question/answer-fields'][0][':answer-field/choices']) if o[':answer/id']==SOURCES[t][':question/answer-fields'][0][':answer-field/correct'][':answer/id'])
            a[':answer/value']=tex(s.simplify(ratio*bank[correct_index]))
            if orig[':answer/value'].endswith(' '):a[':answer/value']+=' '
    correct=answers[0][':answer/id'] if not raw else next(a[':answer/id'] for a,orig in zip(answers,SOURCES[t][':question/answer-fields'][0][':answer-field/choices']) if orig[':answer/id']==SOURCES[t][':question/answer-fields'][0][':answer-field/correct'][':answer/id'])
    random.Random(seed).shuffle(answers);kind='blank' if t=='q-167649' or level=='easy' else 'radio';keyfield='field-1' if kind=='blank' else 'selection'
    q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':keyfield,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    task={'template':t,'bounds':p,'assessed_information':'supplied norm' if level!='hard' else 'compute norm'}
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':t,'profile':profile,'parameters':p,'seed':seed,'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest(),'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

# EASY: authored canonical cancellation; supplied metric, one elementary linear primitive.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    if template not in (None,'canonical_hint') or profile not in (None,'authored') or field_type not in (None,'blank',':answer-field.type/blank'):raise ValueError('easy selector')
    rng=random.Random(seed);p=parameters or {'a':rng.choice([1,2,3]),'b':rng.choice([1,2,3]),'c':rng.choice([1,2,3]),'U':rng.choice([1,2,3]),'V':rng.choice([1,2,3])}
    if set(p)!=set(('a','b','c','U','V')) or any(type(q)!=int or q not in (1,2,3) for q in p.values()):raise ValueError('easy integers 1..3')
    a,b,c,A,B=[p[k] for k in ('a','b','c','U','V')];n=s.sqrt(2*a*a*c*c+4*a*a*b*b);ans=s.simplify(b*B*B*A*n)
    R=[a*u+b*v,a*u-b*v,c*v];rtex='⟨'+r',\,'.join(tex(q) for q in R)+'⟩'
    prompt='Evaluate the surface integral\n\n$$\\iint_S(x-y)\\,\\text{d}S,$$\n\nwhere $r(u,v)='+rtex+'$ for $0\\le u\\le '+str(A)+'$ and $0\\le v\\le '+str(B)+'.$\n\n*Hint: $‖r_u′\\times r_v′‖='+tex(n)+'.$*\n\n{{field-1}}'
    sol=SOURCES['q-160834'][':question/worked-solution'].split('Next,')[0].replace(r'\sqrt{70}',tex(n))
    sol+='Next, we substitute the coordinate expressions of $r(u,v)$ into $f(x,y,z):$\n\n$$f(r(u,v))=('+tex(R[0])+')-('+tex(R[1])+')='+tex(2*b*v)+'.$$\n\nTherefore, our surface integral can be written as\n\n$$\\begin{aligned}\\iint_S(x-y)\\,\\text{d}S&=\\iint_D f(r(u,v))‖r_u′\\times r_v′‖\\,\\text{d}A\\\\&='+tex(n)+r'\iint_D '+tex(2*b*v)+r'\,\text{d}A\\&='+tex(n)+r'\int_0^{'+str(B)+'}'+tex(2*b*v)+r'\,\text{d}v\cdot\int_0^{'+str(A)+r'}1\,\text{d}u\\&='+tex(n)+'['+tex(b*v*v)+']_0^{'+str(B)+'}[u]_0^{'+str(A)+r'}\\&='+tex(n)+'('+tex(b*B*B)+'-0)('+str(A)+'-0)'+r'\\&='+tex(ans)+r'.\end{aligned}$$'
    return make_record('easy','canonical_hint',p,'authored',seed,prompt,sol,[ans])

# MODERATE: seven supplied-metric observed families; scope fixed polynomial cancellation/products.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: six observed families; full formal tangent/determinant/norm stages precede integration.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level=='easy':return generate_easy(seed,template,field_type,parameters,profile)
    if level not in ('moderate','hard'):raise ValueError('unknown level')
    candidates=[t for t in DATA if LEVEL[t]==level and (field_type is None or field_type in ('blank',':answer-field.type/blank') and t=='q-167649' or field_type in ('radio',':answer-field.type/radio') and t!='q-167649')]
    if not candidates:raise ValueError('unknown/unsupported field selector')
    rng=random.Random(seed);t=template or rng.choice(candidates)
    if t not in candidates:raise ValueError('template/field/difficulty mismatch')
    raw=profile in ('observed','observed:'+t)
    if profile not in (None,'method','observed','observed:'+t):raise ValueError('unknown profile')
    for attempt in range(400):
        p=validate_parameters(t,parameters if parameters is not None else sample(t,rng));m=mathematics(t,p);prompt=mask_bounds(SOURCES[t][':question/problem'],p)
        if t=='q-167649' and not raw:
            prompt='A shell is parametrized by $r(x,\\theta)=⟨x,2x^2\\cos\\theta,2x^2\\sin\\theta⟩$ for $0\\le x\\le '+tex(p['ub'])+'$ and $0\\le\\theta<2\\pi$. Its charge density is $d(x,y,z)=\\frac{'+tex(s.sympify(p['k'])*x)+'(y^2+z^2)}{\\sqrt{16x^2+1}}$, and $‖r_x′\\times r_\\theta′‖=2x^2\\sqrt{16x^2+1}$. Evaluate $Q=\\iint_S d\\,\\text{d}S$.\n\n{{field-1}}'
        if not raw and 'D={' in prompt:prompt=re.sub(r'D=\{\(u,v\)(.*?)\}\.\$',lambda m:r'D=\{(u,v)'+m[1]+r'\}.$',prompt)
        sol=source_solution(t,m,p,raw)
        if raw:
            anchor=mathematics(t,ORIGINAL[t])['value'];bank=[s.simplify(scalar_parse(a[':answer/value'])/anchor*m['value']) for a in SOURCES[t][':question/answer-fields'][0][':answer-field/choices']]
        else:bank=operation_bank(t,m)
        try:return make_record(level,t,p,'observed:'+t if raw else 'method',seed,prompt,sol,bank,raw)
        except ValueError:
            if parameters is not None:raise
    raise ValueError('no eligible whole bank')

def markdown(r):
    q=r['question'];parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):parts+=['\n'.join(a[':answer/value'] for a in f[':answer-field/choices'])]
    parts+=[q.get(':question/worked-solution','')];return '\n\n'.join(parts)

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186172131-source-policy.json'))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)];print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,records)))
