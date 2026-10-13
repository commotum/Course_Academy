#!/usr/bin/env python3
"""Particular first-order solutions by direct integration.
Observed profiles parameterize the initial ordinate (vertical translation), with
complete original stages preserved. Opaque observed banks are replay-only.
Authored defaults vary integrands as well; all levels use one integration and C.
No database access, plots, second-order equations, separation or integrating factors.
"""
import argparse,hashlib,json,random,re,uuid
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
VERSION='particular-direct-1'; KP_ID=17592186096699
SOURCE=json.loads((HERE/'source.json').read_text()); KP=SOURCE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}

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
# is a parameter recipe q_i(x)+(B-B0), not a literal-answer lookup or fitted error.
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

def source_render(template,B):
    q=QUESTIONS[template];g,P,a,b,fragment,bank=DEFS[template];P=s.sympify(P);delta=B-b;K=s.simplify(B-P.subs(X,a));K0=s.simplify(b-P.subs(X,a))
    f=q[':question/answer-fields'][0];name='f(x)' if 'f(' in q[':question/problem'] or '{f}' in q[':question/problem'] else 'y'
    prompt=q[':question/problem']
    # Whole condition component only: no unprotected number/prose substitution.
    cond=re.search(r'(?:f|y)\([^)]*\)\s*=\s*-?\d+',prompt).group()
    newcond=re.sub(r'-?\d+$',lambda m:tex(B),cond)
    prompt=prompt.replace(cond,newcond)
    sol=q.get(':question/worked-solution')
    if sol is not None:
        sol=sol.replace(cond,newcond)
        # Condition rows: replace the whole left numeric component, leaving
        # individually evaluated primitive components and original row count intact.
        def left(m):return m.group(1)+tex(B)+m.group(3)
        sol=re.sub(r'(\\begin\{aligned\}|\\\\\s*)('+re.escape(str(b))+r')(\s*&\s*=)',left,sol)
        sol=re.sub(r'(C\s*&\s*=\s*)(.*?)(?=\\end\{aligned\}|\\\\)',lambda m:m.group(1)+(m.group(2) if delta==0 else tex(K)+('.' if m.group(2).endswith('.') else '')),sol)
        # Constant on left in the observed zero-C source is a complete slot.
        if template=='q-8311':sol=sol.replace('0 & =C',tex(K)+' & =C')
        # Replace only final explicit solution block; source spelling is the base
        # component and the displacement gives a genuine parameterized formula.
        blocks=list(re.finditer(r'\$\$\n(.*?)\n\$\$',sol,re.S));last=blocks[-1]
        expr=last.group(1).rstrip('.').replace(r'\,.','').replace(r'\,','')
        if delta!=0:sol=sol[:last.start(1)]+expr+('+' if delta>0 else '-')+tex(abs(delta))+'.'+sol[last.end(1):]
    kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
    values=[(name+'=' if kind=='radio' else '')+tex(s.sympify(expr)+delta) for expr in bank]
    return prompt,sol,values,P+K,s.sympify(fragment),name

def completed_solution(der,P,t,B,name):
    P=s.sympify(P);der=s.sympify(der);K=s.simplify(B-P.subs(X,t));coeff=der.as_coeff_Mul()[0]
    first=name+"'" if name=='y' else name.replace('(x)',"'(x)")
    rows=r'\int '+first+r'\,\text{d}x & =\int ('+tex(der)+r')\,\text{d}x \\ '+name+' & =('+tex(coeff)+r')\int ('+tex(der/coeff)+r')\,\text{d}x \\ & =('+tex(coeff)+')('+tex(P/coeff)+r')+C \\ & ='+tex(P)+'+C'
    condition=tex(B)+' & =('+tex(P).replace('x','('+tex(t)+')')+r')+C \\ '+tex(B)+' & ='+tex(s.simplify(P.subs(X,t)))+r'+C \\ C & ='+tex(K)
    initial=(name.split('(')[0]+'('+tex(t)+')='+tex(B))
    return 'First, we rearrange the equation to give\n\n$$\n'+first+'='+tex(der)+'.\n$$\n\nThen, we integrate both sides with respect to $x,$ and get\n\n$$\n'+r'\begin{aligned}'+rows+r'.\end{aligned}'+'\n$$\n\nSo our general solution is $'+name+'='+tex(P)+'+C.$ To find a particular solution, we substitute the condition $'+initial+'$ into our solution and obtain a value for $C,$ as follows:\n\n$$\n'+r'\begin{aligned}'+condition+r'.\end{aligned}'+'\n$$\n\nTherefore, our particular solution is\n\n$$\n'+name+'='+tex(P+K)+'.\n$$'

def record(level,prompt,solution,values,correct,kind,key,meta,presence=None):
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
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':meta}

# Easy: observed one/two elementary primitives; authored peers vary signed
# single-power or trig coefficients, using familiar exact evaluation inputs.
# Moderate: observed polynomial + exponential pair; coefficient and exponent
# scaling requires two primitive components before one initial-value equation.
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
    wrong_primitives=[-P,sum(terms),P/2]
    candidates=[F,P]+[h+v-h.subs(X,t) for h in wrong_primitives]
    if kind=='radio':
        assert len(set(map(s.srepr,map(s.simplify,candidates))))==5,'whole bank collision'
        for i,a in enumerate(candidates):
            for b in candidates[i+1:]:assert s.simplify(a-b)!=0,'whole bank equivalent collision'
        values=[name+'='+tex(z) for z in candidates];correct=0
    else:values=[tex(F)];correct=0
    return record(level,prompt,solution,values,correct,kind,'selection' if kind=='radio' else 'field-1',{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'authorship':'authored defaults','math_fingerprint':fingerprint([s.srepr(sum(terms)),str(t),str(v)]),'domain':'real x; no singularities','recipes':['correct','omit constant','reverse primitive sign then condition','use derivative as primitive then condition','halve primitive then condition'] if kind=='radio' else []})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    assert level in ('easy','moderate','hard')
    rng=random.Random(seed)
    if template in QUESTIONS:
        assert profile in ('observed_raw','observed_repaired'), 'source banks require explicit replay profile'
        q=QUESTIONS[template];sourcelevel=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1];assert sourcelevel==level
        params=parameters or {'target':DEFS[template][3]};assert set(params)=={'target'}
        B=s.Rational(params['target']);assert B.q==1 and abs(B)<=20
        prompt,sol,values,F,fragment,name=source_render(template,B);f=q[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
        assert field_type in (None,kind)
        correct=None
        if ':answer-field/correct' in f:correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        if profile=='observed_repaired':
            if template=='q-119045':sol=sol.replace('general solution is $y=', 'general solution is $f(x)=')
            if template=='q-50044':sol=sol.replace(r'6(\frac{{x}^{3}}{3})\,\text{d}x',r'6(\frac{{x}^{3}}{3})+C').replace('f(x)=','y=')
            if correct is None:correct=next(i for i,a in enumerate(values) if s.simplify(parse(a.split('=')[-1])-F)==0)
            if sol is None:
                der,P,t,b,frag,bank=DEFS[template];sol=completed_solution(der,P,t,B,name)
        presence={'difficulty':':question/difficulty' in q} if profile=='observed_raw' else None
        return record(level,prompt,sol,values,correct,kind,f[':answer-field/key'],{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{'target':str(B)},'authorship':'observed bank; interpretation opaque; replay-only','source_id':template,'source_attribute_presence':{'difficulty':':question/difficulty' in q,'worked_solution':':question/worked-solution' in q,'correct':':answer-field/correct' in f},'completion_is_authored':profile=='observed_repaired' and (':question/difficulty' not in q or ':question/worked-solution' not in q or ':answer-field/correct' not in f),'math_fingerprint':fingerprint([s.srepr(s.sympify(DEFS[template][0])),str(DEFS[template][2]),str(B)]),'domain':'connected real interval containing the given input; denominators nonzero and radicals positive'},presence)
    assert profile in (None,'authored_operations');profile='authored_operations'
    template=template or {'easy':'elementary','moderate':'mixed','hard':'three'}[level];assert template=={'easy':'elementary','moderate':'mixed','hard':'three'}[level]
    kind=field_type or rng.choice(['blank','radio']);assert kind in ('blank','radio')
    # Whole profile selected before parameters; no adaptive fallback to blank.
    for attempt in range(1000):
        if parameters is None:
            p={'a':rng.choice([-6,-4,-2,2,4,6]),'b':rng.choice([-3,-2,-1,1,2,3]),'d':rng.choice([-4,-3,-2,2,3,4]),'k':rng.choice([-2,-1,1,2]),'t':0,'v':rng.randint(-8,8),'name':rng.choice(['y','f','g']),'family':{'easy':rng.choice(['power','trig']),'moderate':'mixed','hard':'three'}[level]}
            if level=='easy' and p['family']=='power':p['t']=rng.choice([-2,-1,1,2])
        else:
            p=dict(parameters);assert set(p)=={'a','b','d','k','t','v','name','family'}
        try:return authored(level,seed,template,kind,p,profile)
        except AssertionError:
            if parameters is not None:raise
    raise ValueError('no eligible whole-bank instance')

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];out=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):out+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
    return out+q.get(':question/worked-solution','[No captured worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    result=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(result,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,result)))
