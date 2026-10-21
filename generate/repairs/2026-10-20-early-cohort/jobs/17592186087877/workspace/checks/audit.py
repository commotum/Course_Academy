"""Independent, read-only generator review. Run with the job's venv Python.

All output paths are relative to this file. No package/database writes.
"""
import collections, hashlib, importlib.util, json, pathlib, re, shutil, subprocess, sys
import sympy as S
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor)

HERE=pathlib.Path(__file__).resolve().parent
JOB=HERE.parent.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PKG=HERE.parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed_generator',PKG/'17592186087877.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
X=S.Symbol('x',positive=True)
Y,V=S.symbols('y yp')
def save(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def snapshot():
    return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in PKG.rglob('*') if p.is_file()}

def group_at(t,i):
    assert t[i]=='{',(t,i)
    depth=1;j=i+1
    while depth:
        if t[j]=='{':depth+=1
        if t[j]=='}':depth-=1
        j+=1
    return t[i+1:j-1],j

def clean(t):
    t=t.replace('\\\\','\\').replace('\\u2061','').replace('\u2061','')
    t=t.replace('\\left','').replace('\\right','').replace('\\,','').replace('\\!','')
    t=t.replace('\\dfrac','\\frac')
    t=re.sub(r'\\(?:text|textrm)\{d\}', 'd', t)
    t=re.sub(r'\\operatorname\{(cos|sin|ln)\}',r'\\\1',t)
    return t

def scalar(t):
    t=clean(t).strip().rstrip('.')
    t=re.sub(r'\\ln\|([^|]+)\|',r'\\ln{\\abs{\1}}',t)
    t=re.sub(r'\\(cos|sin|ln)\s*x\b',r'\\\1{x}',t)
    while '\\frac' in t:
        i=t.rfind('\\frac');j=i+5
        while t[j].isspace():j+=1
        a,j=group_at(t,j)
        while t[j].isspace():j+=1
        b,j=group_at(t,j)
        t=t[:i]+'(('+str(scalar(a))+')/('+str(scalar(b))+'))'+t[j:]
    t=t.replace('\\cdot','*').replace('\\cos',' cos').replace('\\sin',' sin').replace('\\ln',' log').replace('\\abs',' Abs')
    t=t.replace('{','(').replace('}',')').replace('^','**')
    assert '\\' not in t,t
    return parse_expr(t,local_dict={'x':X,'y':Y,'yp':V,'e':S.E,'E':S.E,
        'cos':S.cos,'sin':S.sin,'log':S.log,'Abs':S.Abs},
        transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def equation(t):
    t=clean(t).strip().rstrip('.')
    left,right=t.split('=')
    if left.startswith('\\frac{d}{dx}'):
        f=scalar(left[len('\\frac{d}{dx}'):]);lhs=S.diff(f,X)+S.diff(f,Y)*V
    else:
        left=left.replace('\\frac{dy}{dx}',' (yp) ');lhs=scalar(left)
    return S.expand(lhs-scalar(right))

def normalized(r):
    c=S.expand(r).coeff(V)
    assert c!=0,r
    return S.simplify(r/c)

def prompt_equation(record):
    t=record['question'][':question/problem']
    spans=re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$',t)
    for a,b in spans:
        v=clean(a or b)
        if '\\frac{dy}{dx}' in v:
            v=v.split(',')[0]
            return v,equation(v)
    raise AssertionError(t)

def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
    c=field(r)[':answer-field/correct']
    return c[':answer/id'] if isinstance(c,dict) else c[1]
def shortcut(r):
    """Read only the answer bank; never read prompt, metadata, or key."""
    candidates=[]
    for a in field(r)[':answer-field/choices']:
        t=clean(a[':answer/value']).split('=')[0]
        m=re.search(r'e\^',t)
        if not m:continue
        h,_=group_at(t,m.end())
        h=scalar(h)
        candidates.append((a[':answer/id'],h))
    winners=[aid for aid,h in candidates if any(S.simplify(h2-2*h)==0 for _,h2 in candidates)]
    return winners[0] if len(winners)==1 else None

def math_check(r):
    text,pr=prompt_equation(r);target=normalized(pr)
    choices=[]
    for a in field(r)[':answer-field/choices']:
        ar=equation(a[':answer/value'])
        choices.append({'id':a[':answer/id'],'valid':S.simplify(normalized(ar)-target)==0})
    good=[a['id'] for a in choices if a['valid']]
    assert good==[key(r)],(r['question'][':question/id'],good,key(r))
    # Check both printed multiply/distribution rows and final product equation.
    blocks=re.findall(r'\$\$\s*([\s\S]*?)\s*\$\$',r['question'][':question/worked-solution'])
    checked=[]
    for b in blocks:
        if '\\begin{aligned}' not in b or '\\int' in b:continue
        b=b.replace('\\begin{aligned}','').replace('\\end{aligned}','')
        for row in b.split('\\\\'):
            row=row.replace('&','').strip()
            rr=equation(row)
            assert S.simplify(normalized(rr)-target)==0,(row,target)
            checked.append(row)
    assert len(checked)==3
    return {'question_id':r['question'][':question/id'],'prompt_equation':text,
            'normalized_residual':str(target),'choices':choices,'solution_rows':checked,'passed':True}
