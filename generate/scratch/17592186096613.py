#!/usr/bin/env python3
"""Exact source-profile generator for c ln(x), x>0. No database operations."""
import argparse, hashlib, json, math, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if not runtime.exists() or Path(sys.executable)==runtime: raise
    os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186096613
KP_UUID='a71301e9-bc7f-53b9-900e-c3bd37f96b03'
TITLE='Differentiating the Product of a Constant and the Natural Logarithm Function'
VERSION='constant-ln-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x=sp.Symbol('x',positive=True)
SUPPORTED_LEVELS=('easy',)
# Each profile is a complete observed bank, never a pooled collection of mistakes.
CASES={
 'q-11909':{'template':'legacy-radio','profile':'integer','parameters':{'n':7,'d':1,'e':False}},
 'q-11910':{'template':'legacy-radio','profile':'fraction','parameters':{'n':2,'d':3,'e':False}},
 'q-101604':{'template':'radio-dot','profile':'integer','parameters':{'n':-9,'d':1,'e':False}},
 'q-101600':{'template':'radio-dot','profile':'euler','parameters':{'n':2,'d':1,'e':True}},
 'q-339941':{'template':'blank','profile':'canonical','parameters':{'n':-11,'d':1,'e':False}},
 'q-308849':{'template':'blank','profile':'canonical','parameters':{'n':8,'d':1,'e':False}},
 'q-339949':{'template':'blank','profile':'equivalent-entry','parameters':{'n':11,'d':4,'e':False}},
 'q-339950':{'template':'blank','profile':'equivalent-entry','parameters':{'n':-7,'d':3,'e':False}},
}
TEMPLATES={'legacy-radio':('easy',('integer','fraction')),'radio-dot':('easy',('integer','euler')),'blank':('easy',('canonical','equivalent-entry'))}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def expression(text):
    """Small explicit math parser for captured c ln x and rational banks."""
    text=text.replace('\u2061','')
    text=re.sub(r'\\(?:operatorname|mathrm)\{(ln|log)\}',r'\1',text)
    text=text.replace(r'\ln','ln').replace(r'\cdot','*').replace(r'\,','').replace(r'\left','').replace(r'\right','')
    def group(pos):
        assert text[pos]=='{',text
        depth=1;j=pos+1
        while depth:
            assert j<len(text),text
            depth+=(text[j]=='{')-(text[j]=='}');j+=1
        return text[pos+1:j-1],j
    while r'\frac' in text:
        i=text.rfind(r'\frac');a,j=group(i+5);b,k=group(j)
        text=text[:i]+'(('+a+')/('+b+'))'+text[k:]
    text=re.sub(r'(?:ln|log)\s*x', ' log(x)', text)
    text=text.replace('D(', ' D(')
    text=text.replace('{','(').replace('}',')').strip().rstrip('.,')
    assert '\\' not in text,text
    return parse_expr(text,local_dict={'x':x,'e':sp.E,'log':sp.log,'D':lambda value:sp.diff(value,x)},transformations=standard_transformations+(implicit_multiplication_application,))

def coefficient(problem):
    match=re.search(r'\$y\s*=\s*(.*?)\$',problem)
    if not match:raise ValueError('No displayed function')
    f=expression(match[1]);c=sp.simplify(f/sp.log(x))
    assert not c.free_symbols and c!=0 and sp.simplify(f-c*sp.log(x))==0
    return c

def fingerprint(q):return digest(['differentiate',sp.srepr(coefficient(q[':question/problem'])),'x>0'])
def latex(e):return sp.latex(e).replace(' e','e').replace(' x','x').replace('- ','-')
def constant(p):return sp.Rational(p['n'],p['d'])*(sp.E if p['e'] else 1)

def validate_parameters(p,profile):
    if set(p)!={'n','d','e'} or type(p['n']) is not int or type(p['d']) is not int or type(p['e']) is not bool:raise ValueError('Exact parameter types')
    if not 2<=abs(p['n'])<=30 or not 1<=p['d']<=12 or math.gcd(abs(p['n']),p['d'])!=1:raise ValueError('Reduced nonunit signed rational domain: |n|2..30,d1..12')
    if profile=='integer' and (p['d']!=1 or p['e']):raise ValueError('integer profile')
    if profile in ('fraction','equivalent-entry') and (p['d']==1 or p['e']):raise ValueError('proper rational-layout profile')
    if profile=='fraction' and p['n']==p['d']:raise ValueError('duplicate fraction bank')
    if profile=='euler' and (p['d']!=1 or not p['e']):raise ValueError('Euler profile')
    if profile in ('canonical','equivalent-entry') and p['e']:raise ValueError('No observed Euler blank')

def sample(seed,profile):
    r=random.Random(seed)
    while True:
        n=r.choice([-1,1])*r.randint(2,30);d=r.randint(2,12) if profile in ('fraction','equivalent-entry') else r.randint(1,12) if profile=='canonical' else 1
        p={'n':n,'d':d,'e':profile=='euler'}
        try:validate_parameters(p,profile);return p
        except ValueError:pass

def bank(p,profile):
    c=constant(p);n=p['n'];d=p['d']
    if profile=='integer':values=[1/x,-c/x,1/(c*x),x/c,c/x]
    elif profile=='fraction':values=[c/x,1/(d*x),n/x,d/x,1/(c*x)]
    elif profile=='euler':values=[sp.E/(n*x),n/(sp.E*x),c/x,n+sp.E/x,sp.E+n/x]
    else:values=[c/x]
    if profile not in ('canonical','equivalent-entry'):
        assert len({sp.srepr(sp.simplify(a)) for a in values})==len(values),'collision'
    rendered=[latex(a) for a in values]
    if profile=='equivalent-entry':rendered.append(f'{n}/({d}x)')
    return rendered

def representative(template,profile,p):
    matches=[sid for sid,c in CASES.items() if c['template']==template and c['profile']==profile]
    exact=next((sid for sid in matches if CASES[sid]['parameters']==p),None)
    return exact or matches[0]

def replace_values(text,original,c):
    old_c=latex(original);old_d=latex(original/x)
    # Captured coefficient and final derivative are separate semantic components.
    text=text.replace(old_d,'@@DERIVATIVE@@').replace(old_c,'@@COEFFICIENT@@')
    return text.replace('@@DERIVATIVE@@',latex(c/x)).replace('@@COEFFICIENT@@',latex(c))

def authored_solution(c):
    return ('The derivative of the natural logarithm is the reciprocal function:\n\n$$\n'+r'\frac{\text{d}}{\text{d}x}(\ln x)=\frac{1}{x}'+'\n$$\n\nWe apply our formula and get\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}('+latex(c)+r'\ln x) \\ & ='+latex(c)+r'\frac{\text{d}}{\text{d}x}(\ln x) \\ & ='+latex(c)+r'\cdot\frac{1}{x} \\ & ='+latex(c/x)+r'.\end{aligned}'+'\n$$')

def generate(level='easy',seed=0,template=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+level+'; no verified in-scope template')
    rng=random.Random(seed)
    template=template or rng.choice(tuple(TEMPLATES))
    if template not in TEMPLATES:raise ValueError('template')
    profile=profile or rng.choice(TEMPLATES[template][1])
    if profile not in TEMPLATES[template][1]:raise ValueError('profile')
    p=parameters.copy() if parameters else sample(seed,profile);validate_parameters(p,profile)
    c=constant(p);sid=representative(template,profile,p);source=QS[sid];old=constant(CASES[sid]['parameters'])
    prompt=replace_values(source[':question/problem'],old,c)
    solution=replace_values(source[':question/worked-solution'],old,c) if ':question/worked-solution' in source else authored_solution(c)
    values=bank(p,profile)
    identity=digest({'version':VERSION,'template':template,'profile':profile,'parameters':p,'problem':prompt,'solution':solution,'bank':sorted(values)})
    qid=uid('question:'+identity);fid=uid('field:'+qid)
    answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=[a[':answer/id'] for a in answers if sp.simplify(expression(a[':answer/value'])-c/x)==0]
    cid=next(a[':answer/id'] for a in answers if a[':answer/value']==latex(c/x))
    assert len(correct)==(2 if profile=='equivalent-entry' else 1)
    rng.shuffle(answers)
    f={':answer-field/id':fid,':answer-field/key':'field-1' if template=='blank' else 'selection',':answer-field/type':':answer-field.type/blank' if template=='blank' else ':answer-field.type/radio',':answer-field/correct':[':answer/id',cid],':answer-field/choices':answers}
    q={':question/id':qid,':question/difficulty':':question.difficulty/easy',':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[f]}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'domain':'x>0','math_fingerprint':fingerprint(q),'source_question_ids':[sid],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'dependencies':{'sympy':sp.__version__},'solution_authorship':'source sequence' if ':question/worked-solution' in source else 'authored from canonical e-3627'}}

def markdown(rec):
    q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def batch(level,count,seed=0,template=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+level)
    if count<1:raise ValueError('positive count required')
    candidates=[]
    for t,(_,profiles) in TEMPLATES.items():
        if template and t!=template:continue
        for b in profiles:
            if profile and b!=profile:continue
            for n in range(-30,31):
                for d in range(1,13):
                    p={'n':n,'d':d,'e':b=='euler'}
                    try:validate_parameters(p,b)
                    except ValueError:continue
                    candidates.append((t,b,p))
    if not candidates:raise ValueError('No eligible template/profile')
    random.Random(seed).shuffle(candidates)
    records=[];seen=set()
    for t,b,p in candidates:
        if len(records)>=count:break
        r=generate(level,seed,t,parameters=p,profile=b)
        fp=r['generation']['math_fingerprint']
        if fp not in seen:seen.add(fp);records.append(r)
    return records

def generate_easy(seed=0,**kwargs):
    """Observed direct constant-multiple log rule, with exact rational coefficients."""
    return generate('easy',seed,**kwargs)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
    records=batch(args.difficulty,args.count,args.seed,args.template,args.profile)
    if len(records)<args.count:print(json.dumps({'outcome':'finite-limit','requested':args.count,'produced':len(records),'shortage':args.count-len(records)}),file=sys.stderr)
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
