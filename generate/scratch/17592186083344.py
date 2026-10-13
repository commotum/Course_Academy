#!/usr/bin/env python3
"""Improper integrals by substitution; source-faithful replay and coefficient variants."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
    import sympy as s
except ModuleNotFoundError:
    import os,sys
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if not runtime.is_file() or Path(sys.executable).absolute()==runtime.absolute():raise
    os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186083344
KP_UUID='6dc2621a-77e1-56d9-af63-1917eaa933b2'
TITLE='Calculating Improper Integrals With an Unbounded Upper Limit Using Substitution'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.1'
SUPPORTED_LEVELS=('moderate','hard')
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'reference/initial/source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if ':question/difficulty' in q}
# C*x^(n-1)/(A*x^n+B)^p, x>=L, positive affine substitution base.
# Keep all source features fixed; vary the positive numerator scale only.
DATA={
'q-118619':(1,2,1,1,2,0,'x',False),
'q-118618':(1,2,1,1,'3/2',0,'x',True),
'q-152045':(3,1,2,4,'3/2',0,'x',True),
'q-152056':(1,3,1,1,'5/2',0,'x',True),
'q-152779':(6,1,1,2,4,-1,'z',False),
'q-152785':(8,4,1,1,4,1,'z',False),
'q-350527':(3,1,1,1,5,0,'x',False),
'q-350528':(2,1,1,3,4,0,'x',True),
'q-350530':(5,1,3,2,4,0,'y',False),
'q-350531':(6,1,4,3,'3/2',0,'t',True),
'q-350532':(2,1,5,1,3,0,r'\theta',False),
'q-350534':(4,4,1,2,'3/2',0,'x',True),
'q-152053':(1,3,1,1,4,0,'x',False),
'q-346591':(1,1,1,1,'9/2',0,'x',True),
'q-350533':(3,3,1,1,'3/2',0,'x',True),
'q-350536':(10,5,1,1,'9/2',0,'x',True)}
DEFAULTS={m:{'scale':1} for m in DATA}
x=s.Symbol('x',positive=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def value(t):
    t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
    t=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',t)
    return s.sympify(t)
def expression(m,scale=1):
    C,n,A,B,p,L,_,_=DATA[m];return s.Rational(C*scale)*x**(n-1)/(A*x**n+B)**s.Rational(p)
def correct(m,scale=1):
    C,n,A,B,p,L,_,_=DATA[m];p=s.Rational(p);U=A*L**n+B
    assert U>0 and p>1
    return s.simplify(s.Rational(C*scale,A*n)/(p-1)*U**(1-p))
def fingerprint(q):
    # Generated and captured questions with the same exact integral share a task fingerprint.
    text=q[':question/problem'];m=next((m for m,o in SOURCES.items() if o[':question/problem']==text),None)
    if m:return digest([s.srepr(expression(m)),DATA[m][5]])
    match=re.search(r'\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}',text)
    return digest(text) # validation/replenishment uses fingerprint_record for generated objects.
def fingerprint_record(rec):
    m=rec['generation']['template'];k=rec['generation']['parameters']['scale']
    return digest([s.srepr(expression(m,k)),DATA[m][5]])
def render_variant(m,k):
    old=SOURCES[m];C,n,A,B,p,L,v,rad=DATA[m];p=s.Rational(p)
    vx=s.Symbol(v.lstrip('\\'),positive=True);base=s.latex(A*vx**n+B)
    # Retain the source variable token, including theta, and its radical/integer power shape.
    def latex(z):return s.latex(z)
    base=latex(A*vx**n+B);numerator=latex(C*k*vx**(n-1))
    den=r'\sqrt{('+base+')^{'+str(2*p)+'}}' if rad else '('+base+')^{'+str(p)+'}'
    fun=r'\frac{'+numerator+'}{'+den+'}'
    integral=r'{\int }_{'+str(L)+r'}^{\infty }'+fun+r'\,\text{d}'+v
    f=old[':question/answer-fields'][0]
    problem=('Evaluate the following integral. Do not round the answer.\n\n$'+integral+'=$\n{{'+f[':answer-field/key']+'}}') if f[':answer-field/type'][':db/ident']==':answer-field.type/blank' else 'Evaluate the integral $'+integral+'.$'
    U=A*L**n+B;D=s.Rational(C*k,A*n);anti=-D/(p-1);ans=correct(m,k)
    solution=(f'First, we substitute $u={base}.$ Differentiating, we get\n\n$$\n'+r'\frac{\text{d}u}{\text{d}'+v+'}='+latex(A*n*vx**(n-1))+r'\quad\Longrightarrow\quad\text{d}u='+latex(A*n*vx**(n-1))+r'\,\text{d}'+v+'.\n$$\n\n'+f'Since $u\\to \\infty$ when ${v}\\to \\infty,$ the table for the limits of integration using the rule $u={base}$ is as follows:\n\n'+f'| ${v}$ | ${L}$ | $\\infty$ |\n| --- | --- | --- |\n| $u$ | ${U}$ | $\\infty$ |\n\n'+ 'So, the integral in terms of the new variable $u$ is\n\n$$\n'+integral+'='+latex(D)+r'\int_{'+str(U)+r'}^{\infty}u^{-'+latex(p)+r'}\,\text{d}u.'+'\n$$\n\nFinally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\\to\\infty.$\n\n$$\n'+r'\begin{aligned}'+integral+' & ='+latex(D)+r'\lim_{a\to\infty}\int_{'+str(U)+'}^{a}u^{-'+latex(p)+r'}\,\text{d}u \\ & =\lim_{a\to\infty}\left['+latex(anti)+'u^{'+latex(1-p)+r'}\right]_{'+str(U)+r'}^{a} \\ & ='+latex(anti)+r'\lim_{a\to\infty}\left(a^{'+latex(1-p)+'}-'+latex(s.Integer(U)**(1-p))+r'\right) \\ & ='+latex(anti)+r'\left(0-'+latex(s.Integer(U)**(1-p))+r'\right) \\ & ='+latex(ans)+r'.\end{aligned}'+'\n$$')
    return problem,solution

def generate(difficulty,seed=0,template=None,parameters=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: no validated source evidence')
    rng=random.Random(seed);eligible=[m for m,q in SOURCES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
    m=template or rng.choice(eligible);assert m in eligible
    k=(parameters or {'scale':rng.randint(1,1000)})['scale']
    assert type(k) is int and 1<=k<=1000
    old=SOURCES[m];problem,solution=(old[':question/problem'],old[':question/worked-solution']) if k==1 else render_variant(m,k)
    task=digest([s.srepr(expression(m,k)),DATA[m][5]])
    qid=uid('question|'+task+'|'+m);of=old[':question/answer-fields'][0];fid=uid(qid+'|'+of[':answer-field/key']);choices=[];correct_id=None
    for a in of[':answer-field/choices']:
        typ=a[':answer/type'][':db/ident'];av=a[':answer/value'] if k==1 or typ==':answer.type/text' else s.latex(s.simplify(value(a[':answer/value'])*k))
        aid=uid(fid+'|'+typ+'|'+av);choices.append({':answer/id':aid,':answer/type':typ,':answer/value':av})
        if a[':answer/id']==of[':answer-field/correct'][':answer/id']:correct_id=aid
    rec={'knowledge_point':{'id':KP_UUID,'db_id':KP_ID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':m,'bank_profile':m if len(choices)>1 else None,'seed':seed,'parameters':{'scale':k},'source_basis':1980,'source_question_id':str(old[':question/id']),'dependencies':{'sympy':s.__version__},'domain':'x >= L; A*x^n+B > 0; p > 1','sampling_policy':'positive numerator scale 1..1000; all other observed parameters fixed','layout_extension':k!=1}}
    return rec

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
    ms=[m for m,q in SOURCES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)];rng=random.Random(seed)
    candidates=[(m,k) for k in range(1,1001) for m in ms];rng.shuffle(candidates);records=[];seen=set()
    for m,k in candidates:
        rec=generate(difficulty,seed,m,{'scale':k});fp=fingerprint_record(rec)
        if fp not in seen:records.append(rec);seen.add(fp)
        if len(records)==count:return records
    raise ValueError('finite coefficient pool exhausted')
def markdown(r):return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True,choices=SUPPORTED_LEVELS);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();assert a.count>0
    rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
