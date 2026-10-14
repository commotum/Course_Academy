#!/usr/bin/env python3
"""Exact tangent-slope blanks; bounded source-faithful generation, no DB writes."""
import argparse, hashlib, itertools, json, random, re, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os,sys
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if Path(sys.executable).absolute()==runtime.absolute():raise
    os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).with_suffix('')
S=json.loads((HERE/'source.json').read_text())
KP_ID=17592186064343
KP_UUID=S['record'][':knowledge-point/id']
TITLE=S['record'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('easy','moderate')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
x=sp.Symbol('x',positive=True)

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def latex(v):return sp.latex(sp.sympify(v)).replace('- ', '-')
def expression(text):
    """Small exact source grammar: rational powers, radicals, arithmetic."""
    def group(s,i):
        if i>=len(s) or s[i]!='{':raise ValueError(('brace expected',s,i))
        start=i+1;depth=1;i+=1
        while depth:
            if i>=len(s):raise ValueError('unbalanced LaTeX')
            if s[i]=='{':depth+=1
            elif s[i]=='}':depth-=1
            i+=1
        return s[start:i-1],i
    def convert(s):
        result='';i=0
        while i<len(s):
            if s.startswith('\\frac',i) or s.startswith('\\dfrac',i):
                i+=6 if s.startswith('\\dfrac',i) else 5
                a,i=group(s,i);b,i=group(s,i)
                result+='(('+convert(a)+')/('+convert(b)+'))'
            elif s.startswith('\\sqrt',i):
                i+=5;n='2'
                while i<len(s) and s[i]==' ':i+=1
                if s[i]=='[':
                    j=s.index(']',i);n=s[i+1:j];i=j+1
                a,i=group(s,i);result+='(('+convert(a)+')**(1/('+n+')))'
            elif s[i]=='^':
                i+=1
                if i<len(s) and s[i]=='{':a,i=group(s,i)
                else:a=s[i];i+=1
                result+='**('+convert(a)+')'
            elif s[i] in '{}':i+=1
            else:result+=s[i];i+=1
        return result
    text=text.replace(r'\cdot','*').replace(r'\,','').replace(r'\left','').replace(r'\right','').strip().rstrip('.,')
    return parse_expr(convert(text),local_dict={'x':x},transformations=standard_transformations+(implicit_multiplication_application,))

def prompt_data(problem):
    m=re.search(r'\$y\s*=\s*(.*?)\$ at the point \$\(([^,]+),\s*([^)]*)\)',problem)
    if not m:raise ValueError('unknown tangent prompt')
    return expression(m[1]),expression(m[2]),expression(m[3])
def fingerprint_text(problem):
    curve,t,y=prompt_data(problem)
    return digest([sp.srepr(sp.expand(curve)),str(t)])
def fingerprint(q):return fingerprint_text(q[':question/problem'])

def values(profile,p):
    a,b,k=p['a'],p['b'],p['k']
    if profile=='q-304130':
        t=k**2;y=a*t-b*k;d=a-b/sp.Integer(2*k)
        return {'a':str(a),'b':str(b),'k':str(k),'t':str(t),'y':str(y),'half_b':latex(sp.Rational(b,2)),'m':latex(d),'term1':str(a),'term2':latex(sp.Rational(b,2*k))}
    t=k**4;y=a*k*k-b*k**3;d=sp.Rational(a,2*k*k)-sp.Rational(3*b,4*k)
    return {'a':str(a),'b':str(b),'k':str(k),'t':str(t),'y':str(y),'half_a':latex(sp.Rational(a,2)),'three_quarter_b':latex(sp.Rational(3*b,4)),'k2':str(k*k),'m':latex(d)}

def validate_parameters(profile,p):
    if set(p)!= {'a','b','k'} or any(type(v)is not int for v in p.values()):raise ValueError('integer parameter keys a,b,k')
    if not 2<=p['a']<=9 or p['b'] not in (range(2,11,2) if profile=='q-304130' else range(2,13,2)) or p['k'] not in (range(2,6) if profile=='q-304130' else range(2,5)):
        raise ValueError('outside documented coefficient/root bounds')
    return dict(p)
def render(s,p):return re.sub(r'__([a-z0-9_]+)__',lambda m:p[m[1]],s)

def generate(level,seed=0,template=None,parameters=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty '+str(level))
    profile=template or ('q-304130' if level=='easy' else 'q-343079')
    if profile not in TEMPLATES or TEMPLATES[profile]['difficulty']!=level:raise ValueError('ineligible template')
    rng=random.Random(seed)
    p=validate_parameters(profile,parameters or {'a':rng.randint(2,9),'b':rng.choice(list(range(2,11 if level=='easy' else 13,2))),'k':rng.randint(2,5 if level=='easy' else 4)})
    v=values(profile,p);problem=render(TEMPLATES[profile]['problem'],v);solution=render(TEMPLATES[profile]['solution'],v)
    content=digest([profile,problem,solution,v['m']]);qid=uid('question:'+content);fid=uid(qid+':field:field-1');aid=uid(fid+':answer:'+v['m'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':v['m']}],':answer-field/correct':[':answer/id',aid]}]},'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':profile,'parameters':p,'parameter_fingerprint':fingerprint_text(problem),'content_fingerprint':content,'domain':'x>0; evaluation at a positive perfect square (easy) or fourth power (moderate)','source_basis':S['basis'],'lineage':S['lineage'],'source_id':profile,'bank_profile':None,'assets':[],'plot_rating':'none','sampling_policy':'a=2..9; positive even b=2..10 easy /2..12 moderate; root k=2..5 easy /2..4 moderate. Exponents, sign pattern, blank and solution stages fixed.'}}

def batch(level,count=5,seed=0):
    if level not in SUPPORTED_LEVELS or type(count)is not int or count<0:raise ValueError('unsupported difficulty/count')
    profile='q-304130' if level=='easy' else 'q-343079'
    domain=list(itertools.product(range(2,10),range(2,11 if level=='easy' else 13,2),range(2,6 if level=='easy' else 5)))
    random.Random(seed).shuffle(domain)
    return [generate(level,seed,profile,dict(zip(('a','b','k'),p))) for p in domain[:count]]
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\nAnswer: $'+q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+'$\n\n'+q[':question/worked-solution']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
    rows=batch(args.difficulty,args.count,args.seed)
    print(json.dumps({'instances':rows,'generator_path':'generate/scratch/17592186064343.py'},indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
