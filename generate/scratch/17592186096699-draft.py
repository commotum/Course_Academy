#!/usr/bin/env python3
"""Particular first-order solutions by direct integration.
Observed profiles parameterize a complete dependent-function rescaling, with
complete original stages preserved. Opaque observed banks are replay-only.
Authored defaults vary integrands as well; all levels use one integration and C.
No database access, plots, second-order equations, separation or integrating factors.
"""
import argparse,hashlib,json,random,re,uuid,sys,copy,importlib.util
sys.dont_write_bytecode=True
from pathlib import Path
try:
    import sympy as s
except ModuleNotFoundError:
    import os, sys
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if Path(sys.executable).resolve()==interpreter.resolve():raise
    os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).with_suffix(''); X=s.Symbol('x',real=True); C=s.Symbol('C',real=True)
VERSION='particular-direct-draft-2275-2'; KP_ID=17592186096699
SOURCE=json.loads((HERE/'source.json').read_text()); KP=SOURCE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' in q}
INDEPENDENT=[q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' not in q]
_fs=importlib.util.spec_from_file_location('math_format',Path(__file__).resolve().parents[2]/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(_fs);_fs.loader.exec_module(fmt)

def tex(e):return s.latex(e).replace(r'\log',r'\ln').replace(r'\left', '').replace(r'\right','')
def parse(t):
    """Independent readback parser for the displayed elementary TeX subset."""
    t=t.replace('\u2061','').replace('′',"'").replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
    t=re.sub(r'\\operatorname\{(sin|cos|ln|arctan)\}',r'\1',t)
    t=t.replace(r'\text{d}x','').replace(r'\text{d}u','').replace(r'\,','').replace(r'\!','')
    for cmd in ('sin','cos','ln','arctan') :t=t.replace('\\'+cmd,cmd)
    def group(pos):
        assert t[pos]=='{',(t,pos)
        n=1;i=pos+1
        while n:
            if t[i]=='{':n+=1
            if t[i]=='}':n-=1
            i+=1
        return t[pos+1:i-1],i
    while r'\frac' in t or r'\dfrac' in t:
        m=re.search(r'\\d?frac',t);a,j=group(m.end());b,k=group(j);t=t[:m.start()]+'(('+a+')/('+b+'))'+t[k:]
    while r'\sqrt' in t:
        i=t.index(r'\sqrt');a,j=group(i+5);t=t[:i]+'sqrt('+a+')'+t[j:]
    t=t.replace('{','(').replace('}',')').replace('ln','log').replace('arctan','atan')
    t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
    t=re.sub(r'(sin|cos|log|atan)\s*([x0-9]+)(?![a-z])',r'\1(\2)',t)
    t=re.sub(r'log(Abs\([^)]*\))',r'log(\1)',t)
    t=t.replace('e^','E^')
    return parse_expr(t,local_dict={'x':X,'Q':s.Symbol('Q',real=True),'C':C,'E':s.E,'e':s.E,'Abs':s.Abs,'sin':s.sin,'cos':s.cos,'log':s.log,'atan':s.atan,'y':s.Symbol('y'),'u':s.Symbol('u',real=True)},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def uid(content):return str(uuid.uuid5(uuid.NAMESPACE_URL,content))
def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
# Observed template definitions: derivative primitive, actual evaluation input and
# target, required blank fragment, and complete bank expressions. Each expression
# is an explicit rescaling prototype r*q_i(x), not an answer lookup or fitted error.
DEFS={
'q-119078':(-2/(X-1)**2,2/(X-1),2,1,0,[-1/(2*(X-1))+s.Rational(3,2),1/(X-1)+s.Rational(1,2),2/(X-1)-1,1/(X-1),2/(X-1)+3]),
'q-49942':(-s.exp(X)/2,-s.exp(X)/2,0,-1,0,[s.exp(X)/2-1,s.exp(X)-2,-s.exp(X)/2+1,(s.exp(X)-3)/2,-(s.exp(X)+1)/2]),
'q-119045':(-2*s.cos(X),-2*s.sin(X),0,-1,0,[-2*s.sin(X)-1,2*s.cos(X)-3,s.sin(X)/2-1,2*s.sin(X)-3,-2*s.cos(X)+1]),
'q-119046':(4*X+1,2*X**2+X,1,-1,0,[2*X**2+X-4,X**2-2*X,X**2+2*X-4,2*X**2+3*X-6,2*X**2+X-1]),
'q-119075':(8*X-s.exp(-2*X),4*X**2+s.exp(-2*X)/2,0,1,0,[2*X**2-2*s.exp(-2*X)+3,8*X**2+2*s.exp(-2*X)-1,2*X**2+s.exp(-2*X)/2+s.Rational(1,2),4*X**2+s.exp(-2*X)/2-s.Rational(3,2),4*X**2+s.exp(-2*X)/2+s.Rational(1,2)]),
'q-119083':(2*X+s.exp(X/2),X**2+2*s.exp(X/2),0,2,0,[X-s.exp(X/2)/2+s.Rational(5,2),X**2+2*s.exp(X/2)+2,2*X+s.exp(X/2)+1,X**2+2*s.exp(X/2),X**2+s.exp(X/2)/2+s.Rational(3,2)]),
'q-347842':(-X**2+8*X,-X**3/3+4*X**2,2,5,-X**3/3,[4*X**2-s.Rational(25,3)]),
'q-352066':(8/(X-3)**2,-8/(X-3),4,1,0,[-8/(X-3)+9]),
'q-352068':(4/s.sqrt(X+1),8*s.sqrt(X+1),3,10,0,[8*s.sqrt(X+1)-6]),
'q-352075':(-3*s.sin(X),3*s.cos(X),0,2,0,[3*s.cos(X)-1]),
'q-50044':(6*X**2,2*X**3,-1,2,0,[6*X**3+8,-2*X**2+4,X**3+3,3*X**2-1,2*X**3+4]),
'q-50092':(X**2+2*X,X**3/3+X**2,1,1,0,[X**3+X**2-1,X**3/3+X**2-s.Rational(1,3),X**3+2*X**2-2,X**3/3-X**2+s.Rational(5,3),X**3/3+2*X**2-s.Rational(4,3)]),
'q-50159':(2/(1+2*X),s.log(s.Abs(1+2*X)),0,-2,0,[2*s.log(s.Abs(1+2*X))-2,s.log(s.Abs(1+2*X))-2,s.log(s.Abs(1+2*X))-1,2*X-2,2*X**2+X-2]),
'q-8311':(-4,-4*X,-1,4,0,[4*X**2,4,-4*X,-4,-2*X-2])}
# Number count is fourteen, including two legacy unrated originals.


Q=s.Symbol('Q',real=True)
def kind_of(template):return QUESTIONS[template][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
def level_of(template):return QUESTIONS[template].get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
def derivative_tex(template):
    prompt=QUESTIONS[template][':question/problem']
    if r'\frac{\text{d}y}{\text{d}x}' in prompt:return r'\frac{\text{d}y}{\text{d}x}'
    return r'{f}^{′}(x)' if ('f(' in prompt or '{f}' in prompt) else r'{y}^{′}'
def derivative_replace(math,template):
    math=math.replace(r'\frac{\text{d}y}{\text{d}x}','Q')
    math=re.sub(r'\{?[fgy]\}?\^\{′\}(?:\(x\))?','Q',math)
    math=re.sub(r"[fgy]'(?:\(x\))?",'Q',math)
    return math

def scalar_mask(math,r):
    """One unevaluated complete-component multiplier, with grouped signs.
    Unit multipliers suppress themselves as a general notation rule. The
    underlying integral/primitive/substitution structure is never simplified.
    """
    return math if r==1 else '('+tex(r)+r')\cdot('+math+')'
def c_rhs(rhs,r):
    match=re.search(r'\+\s*C',rhs)
    if match:return scalar_mask(rhs[:match.start()],r)+'+C'+rhs[match.end():]
    punctuation='.' if rhs.endswith('.') else ''
    return scalar_mask(rhs[:-1] if punctuation else rhs,r)+punctuation

def source_render(template,r,v,raw=True):
    q=QUESTIONS[template];der,P,t,b,fragment,bank=DEFS[template];P=s.sympify(P);r=s.Rational(r);v=s.Rational(v);K=s.simplify(v-r*P.subs(X,t))
    name='f(x)' if ('f(' in q[':question/problem'] or '{f}' in q[':question/problem']) else 'y'
    source_prompt=q[':question/problem'];cond=re.search(r'(?:f|y)\([^)]*\)\s*=\s*-?\d+',source_prompt).group()
    newcond=re.sub(r'-?\d+$',lambda m:tex(v),cond)
    prompt=source_prompt.replace(cond,newcond)
    def prompt_math(match):
        whole=match.group();width=2 if whole.startswith('$$') else 1;math=whole[width:-width].strip()
        if ('′' in math or r'\text{d}y' in math or "'" in math):
            original=math;left,right=derivative_replace(math,template).rstrip('.').split('=')
            def side(z):
                z=parse(z);return z.coeff(Q)*Q+r*z.subs(Q,0)
            replacement=tex(side(left))+'='+tex(side(right))
            replacement=replacement.replace('Q',derivative_tex(template))
            if r==1:replacement=original
            elif original.endswith('.'):replacement+='.'
            return ('$$\n'+replacement+'\n$$') if width==2 else '$'+replacement+'$'
        if '{{field-1}}' in prompt and math.startswith('y=') and fragment!=0:
            supplied=math.split('=',1)[1].rstrip('+').strip();return '$y='+scalar_mask(supplied,r)+'+$'
        return whole
    prompt=fmt.MATH.sub(prompt_math,prompt)
    sol=q.get(':question/worked-solution')
    if sol is not None and not raw:
        if template=='q-119045':sol=sol.replace('general solution is $y=', 'general solution is $f(x)=')
        if template=='q-50044':sol=sol.replace(r'6(\frac{{x}^{3}}{3})\,\text{d}x',r'6(\frac{{x}^{3}}{3})+C').replace('f(x)=','y=')
    if sol is not None:
        sol=sol.replace(cond,newcond)
        def solution_math(match):
            whole=match.group();width=2 if whole.startswith('$$') else 1;math=whole[width:-width].strip()
            if r'\begin{aligned}' in math:
                head=r'\begin{aligned}';tail=r'\end{aligned}';body=math[len(head):-len(tail)];rows=body.split(chr(92)*2);new=[]
                for row in rows:
                    lhs,rhs=row.split('&',1);eqmatch=re.match(r'(\s*=)(.*)',rhs,re.S);equal_space=eqmatch[1];value=eqmatch[2]
                    numeric=lhs.strip()
                    if numeric=='C':value=tex(K).replace('- ','-')+('.' if value.rstrip().endswith('.') else '')
                    elif numeric==str(b):
                        lhs=lhs.replace(str(b),tex(v));value=c_rhs(value,r)
                    elif numeric=='0' and template=='q-8311' and 'C' in value:lhs=lhs.replace('0',tex(K))
                    else:value=c_rhs(value,r)
                    new.append(lhs+'&'+equal_space+value)
                replacement=head+(chr(92)*2).join(new)+tail
            elif math.startswith(('f(x)=','y=')) and '+C' in math:
                left,right=math.split('=',1);replacement=left+'='+c_rhs(right,r)
            elif '′' in math or r'\text{d}y' in math:
                left,right=math.split('=',1);replacement=left+'='+c_rhs(right,r)
            elif math.startswith(('f(x)=','y=')) and width==2:
                left,_=math.split('=',1)
                # A complete explicit-function slot; recover source notation at
                # the identity scale by generic component rendering only.
                replacement=left+'='+tex(r*P+K)+'.'
                if r==1 and v==b:replacement=math
            else:return whole
            return ('$$\n'+replacement+'\n$$') if width==2 else '$'+replacement+'$'
        sol=fmt.MATH.sub(solution_math,sol)
    values=[(name+'=' if kind_of(template)=='radio' else '')+tex(r*s.sympify(expr)) for expr in bank]
    return prompt,sol,values,r*P+K,r*s.sympify(fragment),name

def completed_solution(der,P,t,B,name):
    P=s.sympify(P);der=s.sympify(der);K=s.simplify(B-P.subs(X,t));coeff=der.as_coeff_Mul()[0]
    first=name+"'" if name=='y' else name.replace('(x)',"'(x)")
    rows=r'\int '+first+r'\,\text{d}x & =\int ('+tex(der)+r')\,\text{d}x \\ '+name+' & =('+tex(coeff)+r')\int ('+tex(der/coeff)+r')\,\text{d}x \\ & =('+tex(coeff)+')('+tex(P/coeff)+r')+C \\ & ='+tex(P)+'+C'
    condition=tex(B)+' & =('+tex(P).replace('x','('+tex(t)+')')+r')+C \\ '+tex(B)+' & ='+tex(s.simplify(P.subs(X,t)))+r'+C \\ C & ='+tex(K)
    initial=(name.split('(')[0]+'('+tex(t)+')='+tex(B))
    return 'First, we rearrange the equation to give\n\n$$\n'+first+'='+tex(der)+'.\n$$\n\nThen, we integrate both sides with respect to $x,$ and get\n\n$$\n'+r'\begin{aligned}'+rows+r'.\end{aligned}'+'\n$$\n\nSo our general solution is $'+name+'='+tex(P)+'+C.$ To find a particular solution, we substitute the condition $'+initial+'$ into our solution and obtain a value for $C,$ as follows:\n\n$$\n'+r'\begin{aligned}'+condition+r'.\end{aligned}'+'\n$$\n\nTherefore, our particular solution is\n\n$$\n'+name+'='+tex(P+K)+'.\n$$'

def record(level,prompt,solution,values,correct,kind,key,meta,presence=None):
    prompt=fmt.normalize_prose(prompt)
    solution=fmt.normalize_prose(solution) if solution is not None else None
    values=[fmt.normalize_tex(v) for v in values]
    assessment_presence={'difficulty':level if presence is None or presence['difficulty'] else None,'solution':solution is not None,'correct_value':values[correct] if correct is not None else None}
    content=fingerprint([VERSION,prompt,solution,kind,key,sorted(values),assessment_presence]);qid=uid(content);fid=uid(qid+':field')
    answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
    if correct is not None:f[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
    random.Random(meta['seed']).shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
    if presence is None or presence['difficulty']:q[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:q[':question/worked-solution']=solution
    meta['content_hash']=content
    meta['mathematical_fingerprint']=meta['math_fingerprint']
    meta['evidence_only']=meta['profile'].startswith('observed_')
    meta['eligible_for_learning']=not meta['evidence_only']
    meta['provenance']={k:v for k,v in SOURCE.items() if k!='record'}
    meta['sympy_version']=s.__version__
    meta['python_version']=sys.version.split()[0]
    meta['math_format']=fmt.FORMAT_VERSION
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':meta}

# Easy normal generation serves all twelve source-shaped masks with signed
# bounded coefficients and a varied initial target, preserving their layouts.
# Moderate normal generation serves both observed polynomial/exponential masks;
# each requires two primitive components before one initial-value equation.
# Hard (authored absent-source): three nonzero standard primitive components,
# polynomial + exponential + trigonometric; still direct integration and one C.
# They are peers at one workload, with bounded coefficients and familiar inputs.
def authored_parts(level,p):
    A=s.Rational(p['a']);B=s.Rational(p['b']);d=s.Rational(p['d']);k=s.Rational(p['k']);t=s.Rational(p['t']);v=s.Rational(p['v']);family=p['family']
    assert p['name'] in ('y','f','g')
    assert A.q==1 and v.q==1
    if level in ('moderate','hard'):assert B.q==1
    if level=='hard':assert d.q==1
    if level=='easy':
        assert family in ('power','trig') and 1<=abs(A)<=8 and t in (-2,-1,0,1,2)
        terms=[A*X] if family=='power' else [A*s.cos(X)]
        prim=[A*X**2/2] if family=='power' else [A*s.sin(X)]
        assert family!='trig' or t==0
    elif level=='moderate':
        assert family=='mixed' and 1<=abs(A)<=8 and 1<=abs(B)<=4 and k in (-2,-1,s.Rational(1,2),1,2) and t==0
        terms=[A*X,B*s.exp(k*X)];prim=[A*X**2/2,B*s.exp(k*X)/k]
    else:
        assert family=='three' and 1<=abs(A)<=6 and 1<=abs(B)<=3 and 1<=abs(d)<=4 and k in (-2,-1,1,2) and t==0
        terms=[A*X**2,B*s.exp(k*X),d*s.cos(X)];prim=[A*X**3/3,B*s.exp(k*X)/k,d*s.sin(X)]
    assert abs(v)<=12
    return terms,prim,t,v

def signed_sum(values):
    out=''
    for e in values:
        txt=tex(e);out+=('+' if out and not txt.startswith('-') else '')+txt
    return out

def authored(level,seed,template,kind,p,profile):
    terms,prim,t,v=authored_parts(level,p);P=sum(prim);K=s.simplify(v-P.subs(X,t));F=s.simplify(P+K)
    name=p['name']+'(x)' if p['name']!='y' else 'y';der=p['name']+"'(x)" if p['name']!='y' else "y'"
    g=signed_sum(terms);general=signed_sum(prim)+'+C';initial=p['name']+'('+tex(t)+')='+tex(v)
    prompt='Find the particular solution to the differential equation $'+der+'='+g+'$ that satisfies the condition $'+initial+'.$'
    if kind=='blank':prompt+='\n\n$'+name+r'=\,${{field-1}}'
    integrals=signed_sum([s.Symbol('I'+str(i)) for i in range(len(terms))])
    integral_rows=r'\int '+der+r'\,\text{d}x & =\int ('+g+r')\,\text{d}x \\ '+name+' & ='+ ' + '.join(r'\int ('+tex(e)+r')\,\text{d}x' for e in terms)
    # Preserve unevaluated individual coefficient-times-primitive factors.
    base=[]
    for e,h in zip(terms,prim):
        coeff=e.as_coeff_Mul()[0];base.append('('+tex(coeff)+')('+tex(h/coeff)+')')
    integral_rows+=r' \\ & ='+ ' + '.join(base)+r'+C \\ & ='+general
    substituted=' + '.join('('+tex(h)+')'+r'\big|_{x='+tex(t)+'}' for h in prim)
    # Actual substituted primitive expressions, no evaluation-bar-only collapse.
    subparts=[tex(h).replace('x','('+tex(t)+')') for h in prim]
    evaluated=[s.simplify(h.subs(X,t)) for h in prim]
    condition=tex(v)+' & ='+ ' + '.join('('+z+')' for z in subparts)+r'+C \\ '+tex(v)+' & ='+ ' + '.join('('+tex(z)+')' for z in evaluated)+r'+C \\ C & ='+tex(K)
    solution='The derivative is already isolated, so we have\n\n$$\n'+der+'='+g+'.\n$$\n\nThen, we integrate both sides with respect to $x,$ and get\n\n$$\n'+r'\begin{aligned}'+integral_rows+r'.\end{aligned}'+'\n$$\n\nSo our general solution is $'+name+'='+general+'.$ To find a particular solution, we substitute the condition $'+initial+'$ into our solution and obtain a value for $C,$ as follows:\n\n$$\n'+r'\begin{aligned}'+condition+r'.\end{aligned}'+'\n$$\n\nTherefore, our particular solution is\n\n$$\n'+name+'='+tex(F)+'.\n$$'
    wrong_primitives=[-P,sum(terms),3*prim[0]+sum(prim[1:])]
    candidates=[F,P-P.subs(X,t)]+[h+v-h.subs(X,t) for h in wrong_primitives]
    if kind=='radio':
        assert len(set(map(s.srepr,map(s.simplify,candidates))))==5,'whole bank collision'
        for i,a in enumerate(candidates):
            for b in candidates[i+1:]:assert s.simplify(a-b)!=0,'whole bank equivalent collision'
        values=[name+'='+tex(z) for z in candidates];correct=0
    else:values=[tex(F)];correct=0
    return record(level,prompt,solution,values,correct,kind,'selection' if kind=='radio' else 'field-1',{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'authorship':'authored defaults','math_fingerprint':fingerprint([s.srepr(s.factor(s.cancel(sum(terms)))),str(t),str(v)]),'domain':'real x','recipes':['correct','discard supplied initial value','reverse primitive sign then condition','use derivative as primitive then condition','omit new-power divisor 3 in polynomial component'] if kind=='radio' else []})


def normal_source(level,seed,template,p):
    assert set(p)=={'scale','target'}
    r=s.Rational(p['scale']);v=s.Rational(p['target']);assert r.q==1 and r in (-2,-1,1,2,3,4) and v.q==1 and 0<abs(v)<=12
    der,P,t,b,fragment,bank=DEFS[template];der=r*s.sympify(der);P=r*s.sympify(P);K=s.simplify(v-P.subs(X,t));F=P+K
    prompt,solution,_,_,supplied,name=source_render(template,r,v,False)
    if template=='q-119045':solution=solution.replace('general solution is $y=', 'general solution is $f(x)=')
    if template=='q-50044':
        solution=solution.replace(r'6(\frac{{x}^{3}}{3})\,\text{d}x',r'6(\frac{{x}^{3}}{3})+C').replace('f(x)=','y=')
        # The raw source's dx is not part of an evaluated primitive. Its repair
        # applies inside the scaled complete-component mask as well.
        solution=solution.replace(r')+C)','.placeholder)') if False else solution
    if solution is None:solution=completed_solution(der,P,t,v,name)
    if template in ('q-119078','q-352066'):
        wrong=P+v+P.subs(X,t);recipe='add primitive value when solving C instead of subtracting'
    elif template=='q-49942':
        wrong=P+v+P.subs(X,t);recipe='add primitive value when solving C instead of subtracting'
    elif template in ('q-119045','q-352075'):
        primitive_basis=P/r;original_amplitude=primitive_basis.as_coeff_Mul()[0];basis=primitive_basis/original_amplitude
        wrong_primitive=basis/(r*original_amplitude);wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='reciprocate displayed integral coefficient'
    elif template in ('q-119075','q-119083'):
        k=-2 if template=='q-119075' else s.Rational(1,2)
        exponential=next(z for z in s.Add.make_args(der) if z.has(s.exp));poly=der-exponential
        wrong_primitive=s.integrate(poly,X)+exponential*k;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='differentiate exponential scale instead of integrating it'
    elif template=='q-352068':
        wrong_primitive=P/2;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='omit division by new exponent 1/2'
    elif template=='q-50159':
        wrong_primitive=2*P;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='omit inner-linear divisor 2'
    elif template=='q-8311':
        wrong_primitive=der*X**2/2;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='treat constant derivative as a linear power term'
    else:
        wrong_primitive=sum(z*X for z in s.Add.make_args(der));wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='raise each power but omit each new-degree divisor'
    wrong_derivative_primitive=2*P if template=='q-49942' else der
    candidates=[F,P-P.subs(X,t),-P+v+P.subs(X,t),wrong_derivative_primitive+v-wrong_derivative_primitive.subs(X,t),wrong]
    kind=kind_of(template)
    if kind=='radio':
        for i,a in enumerate(candidates):
            for z in candidates[i+1:]:assert s.simplify(a-z)!=0,'whole bank collision'
        values=[name+'='+tex(z) for z in candidates]
    else:values=[tex(F-supplied)]
    domain={'q-119078':'x>1','q-352066':'x>3','q-352068':'x>-1','q-50159':'x>-1/2','q-50044':'x<0'}.get(template,'real x')
    return record(level,prompt,solution,values,0,kind,QUESTIONS[template][':question/answer-fields'][0][':answer-field/key'],{'version':VERSION,'seed':seed,'template':template,'profile':'authored_operations','parameters':dict(p),'authorship':'authored complete method-derived bank with observed family solution masks','math_fingerprint':fingerprint([s.srepr(s.factor(s.cancel(der))),str(t),str(v)]),'domain':domain,'recipes':['correct','discard supplied initial value','reverse primitive sign then impose condition','ignore derivative coefficient 2 while isolating' if template=='q-49942' else 'use derivative as primitive then impose condition',recipe] if kind=='radio' else [],'source_id':template})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    assert level in ('easy','moderate','hard')
    rng=random.Random(seed)
    if template in QUESTIONS and profile in ('observed_raw','observed_repaired'):
        assert profile in ('observed_raw','observed_repaired'), 'source banks require explicit replay profile'
        q=QUESTIONS[template];sourcelevel=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1];assert sourcelevel==level
        params=parameters or {'scale':1};assert set(params)=={'scale'}
        scale=s.Rational(params['scale']);assert scale.q==1 and scale in (-2,-1,1,2,3,4)
        B=scale*DEFS[template][3]
        prompt,sol,values,F,fragment,name=source_render(template,scale,B,profile=='observed_raw');f=q[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
        assert field_type in (None,kind)
        correct=None
        if ':answer-field/correct' in f:correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        if profile=='observed_repaired':
            if template=='q-119045':sol=sol.replace('general solution is $y=', 'general solution is $f(x)=')
            if template=='q-50044':sol=sol.replace(r'6(\frac{{x}^{3}}{3})\,\text{d}x',r'6(\frac{{x}^{3}}{3})+C').replace('f(x)=','y=')
            if correct is None:correct=next(i for i,a in enumerate(values) if s.simplify(parse(a.split('=')[-1])-F)==0)
            if sol is None:
                der,P,t,b,frag,bank=DEFS[template];sol=completed_solution(scale*s.sympify(der),scale*s.sympify(P),t,B,name)
        presence={'difficulty':':question/difficulty' in q} if profile=='observed_raw' else None
        return record(level,prompt,sol,values,correct,kind,f[':answer-field/key'],{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{'scale':str(scale)},'authorship':'observed complete-bank dependent-variable scaling; opaque error intent; replay-only','source_id':template,'source_attribute_presence':{'difficulty':':question/difficulty' in q,'worked_solution':':question/worked-solution' in q,'correct':':answer-field/correct' in f},'completion_is_authored':profile=='observed_repaired' and (':question/difficulty' not in q or ':question/worked-solution' not in q or ':answer-field/correct' not in f),'math_fingerprint':fingerprint([s.srepr(s.factor(s.cancel(scale*s.sympify(DEFS[template][0])))),str(DEFS[template][2]),str(B)]),'domain':{'q-119078':'x>1','q-352066':'x>3','q-352068':'x>-1','q-50159':'x>-1/2','q-50044':'x<0'}.get(template,'real x')},presence)

    assert profile in (None,'authored_operations');profile='authored_operations'
    if level!='hard':
        eligible=[t for t in QUESTIONS if level_of(t)==level]
        template=template or rng.choice(eligible);assert template in eligible
        kind=kind_of(template);assert field_type in (None,kind)
        for attempt in range(1000):
            p=parameters if parameters is not None else {'scale':rng.choice([-2,-1,1,2,3,4]),'target':rng.choice([n for n in range(-12,13) if n])}
            try:return normal_source(level,seed,template,p)
            except AssertionError:
                if parameters is not None:raise
        raise ValueError('No eligible whole method-derived bank')
    template=template or 'three';assert template=='three'
    kind=field_type or rng.choice(['blank','radio']);assert kind in ('blank','radio')
    for attempt in range(1000):
        if parameters is None:
            p={'a':rng.choice([-6,-4,-2,2,4,6]),'b':rng.choice([-3,-2,-1,1,2,3]),'d':rng.choice([-4,-3,-2,2,3,4]),'k':rng.choice([-2,-1,1,2]),'t':0,'v':rng.randint(-8,8),'name':rng.choice(['y','f','g']),'family':'three'}
        else:p=dict(parameters);assert set(p)=={'a','b','d','k','t','v','name','family'}
        try:return authored(level,seed,template,kind,p,profile)
        except AssertionError:
            if parameters is not None:raise
    raise ValueError('no eligible whole-bank instance')

_unchecked_generate=generate
def generate(*args,**kwargs):
    result=_unchecked_generate(*args,**kwargs)
    checked=copy.deepcopy(result)
    checked['question'].setdefault(':question/worked-solution','')
    fmt.validate_generated_record(checked)
    for text in [result['question'][':question/problem'],result['question'].get(':question/worked-solution','')]+[a[':answer/value'] for f in result['question'].get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])]:
        assert not any(ord(c)<32 and c not in '\n\t' for c in text),'unexpected control character'
    return result

def generate_easy(seed=0,**kwargs):
    """Easy peers: all source-shaped elementary families; one given condition."""
    return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):
    """Moderate peers: two observed polynomial/exponential stage masks."""
    return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):
    """Authored hard peers: three nonzero familiar primitive components."""
    return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];out=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):out+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
    return out+q.get(':question/worked-solution','[No captured worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    result=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(result,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,result)))
