#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
"""Direct three-dimensional Jacobians, basis 2579; local review data only.

Observed banks with opaque error intent are public, evidence-only replay profiles.
Normal defaults use complete method-derived banks. Source display notation is
normalized, with its full prose and ordered calculation stages retained. No EDB.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sys
import sympy as s

from math_format import normalize_prose, normalize_tex

VERSION = '1.1.0-audit9837'
KP_ID = 17592186129271
KP_UUID = 'd433063f-f145-5bf4-8bd4-8d5e5b36b3d8'
TITLE = 'Finding the Jacobian of a Three-Dimensional Transformation'
BASE = Path(__file__).with_suffix('')
SOURCE = {'database':'math','basis':2579,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
u,v,w,theta,a,b,c = s.symbols('u v w theta a b c', real=True)
VARS = (u,v,w)
CAPTURE = json.loads((BASE/'source.json').read_text())['record']
ORIGINALS = {q[':question/math-academy-id']:q for q in CAPTURE[':knowledge-point/questions']}
TEMPLATES = {
 'sparse_trig':('easy','q-39666',{'a':4,'b':3,'c':2,'d':1}),
 'sparse_exp':('easy','q-161793',{'a':1,'b':1,'c':1,'d':3}),
 'sparse_square':('easy','q-161794',{'a':1,'b':1,'c':1,'d':3,'e':1}),
 'log_product':('easy','q-161796',{'a':1,'b':1,'c':2,'d':1}),
 'rotation':('moderate','q-39299',{'a':1,'b':1,'c':1}),
 'polynomial_column':('moderate','q-161792',{'a':1,'b':1,'c':1,'d':1,'e':1}),
 'polynomial_mixed':('moderate','q-39710',{'a':1,'b':1,'c':1,'d':1,'k':2}),
 'linear_offdiag':('moderate','q-39294',{'a':1,'b':1,'c':1,'d':1,'e':1,'f':1}),
 'symbolic_diagonal':('moderate','q-39664',{'a':1,'b':1,'c':1}),
 'sparse_cos':('easy','q-161795',{'a':1,'b':1,'c':1,'d':1,'e':1}),
 'sparse_angle':('easy','q-161799',{'a':1,'b':3,'c':1}),
 'spherical':('hard',None,{'a':1,'b':1,'c':1}),
}
PROFILES = {name+'-observed':{'template':name,'origin':'observed','evidence_only':True}
            for name,(_,sid,_) in TEMPLATES.items() if sid}
PROFILES.update({name+'-method':{'template':name,'origin':'authored','evidence_only':False} for name in TEMPLATES})

class SampleRejected(ValueError): pass

def tex(x):
    return s.latex(s.sympify(x),mul_symbol=None).replace(r'\log',r'\ln')
def par(x): return r'\left('+tex(x)+r'\right)'
def det(m): return r'|\begin{aligned}'+r' \\ '.join(' & '.join(tex(x) for x in row) for row in m.tolist())+r'\end{aligned}|'
def block(t): return '$$\n'+t+'\n$$'
def digest(x): return hashlib.sha256(json.dumps(asset_payload(x),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.NAMESPACE_URL,'jacobian3:'+x))
def simplify(x): return s.trigsimp(s.expand(x))
def equivalent(x,y): return simplify(x-y)==0

def guard(name,p,profile):
    if set(p)!=set(TEMPLATES[name][2]): raise ValueError('Exact parameter keys required')
    if any(type(z) is not int for z in p.values()): raise ValueError('Parameters must be integers, not booleans')
    if any(not 1<=abs(z)<=4 for k,z in p.items() if k!='k'): raise ValueError('Nonzero coefficient magnitudes must be 1..4')
    if 'k' in p and not -4<=p['k']<=4: raise ValueError('Constant offset must be -4..4')
    if profile.endswith('-method'):
        if name=='sparse_trig' and abs(p['a'])==1: raise ValueError('Method bank requires |a|>1')
        if name in ('sparse_exp','sparse_square') and abs(p['d'])==1: raise ValueError('Method bank requires |d|>1')
        if name=='linear_offdiag' and p['a']*p['d']*p['e']==p['b']*p['c']*p['f']: raise ValueError('Two nonzero Laplace products must be unequal')

def components(name,p):
    z=p
    A,B,C=z['a'],z['b'],z['c']
    if name=='sparse_trig': return [A*v,B*u**2+C*s.cos(v*w),z['d']*v*w]
    if name=='sparse_exp': return [A*u*s.exp(w),C*w-B*u,w*s.exp(u)-z['d']*v]
    if name=='sparse_square': return [A*u**2+B*v**2,C*u+z['d']*w,-z['e']*v]
    if name=='log_product': return [A*s.log(u*v*w),B*u+C*w,z['d']*u*v]
    if name=='rotation': return [A*(u*s.cos(theta)+v*s.sin(theta)),B*(v*s.cos(theta)-u*s.sin(theta)),C*w]
    if name=='polynomial_column': return [A*u*v**2+B*w,C*u**3+z['d']*v,z['e']*u*v]
    if name=='polynomial_mixed': return [A*u**2+B*v*w,z['k']-C*u*v,z['d']*v**2-w]
    if name=='linear_offdiag': return [A*v+B*w,C*u+z['d']*w,z['e']*u+z['f']*v]
    if name=='symbolic_diagonal': return [A*a*u,B*b*v,C*c*w]
    if name=='sparse_cos': return [A*u+B*s.cos(w),C*v,z['d']*s.cos(u)+z['e']*w]
    if name=='sparse_angle': return [A*(u+v*s.cos(theta)+w*s.sin(theta)),B*v,C*(u*s.sin(theta)+w)]
    if name=='spherical': return [A*u*s.sin(v)*s.cos(w),B*u*s.sin(v)*s.sin(w),C*u*s.cos(v)]
    raise ValueError(name)

# Complete banks. Observed expression patterns reproduce every displayed source
# value but opaque patterns are not claimed as recovered learner mistakes.
def bank(name,p,J,D,profile):
    A,B,C=p['a'],p['b'],p['c'];d=p.get('d',1);e=p.get('e',1)
    if profile.endswith('-observed'):
        if name=='sparse_trig': vals=[A*B*u*v,-C*v*w*s.cos(v*w),A*v*w,A*v*w*s.cos(v*w),D]
        elif name=='sparse_exp': vals=[A*s.exp(w),D,-A*u*w*s.exp(u+w),s.exp(u+v)-d*s.exp(w),d*w*s.exp(u+v)]
        elif name=='sparse_square': vals=[2*(A*u-B*v),-2*A*u,D,D-2*B*v,0]
        elif name=='log_product': vals=[A/w,-A*B*d*u*v/w,0,D-A/v,D]
        elif name=='rotation': vals=[A*B*C*s.cos(theta),A*B*C*s.sin(theta),0,D,A*B*C*s.sin(theta)*s.cos(theta)]
        elif name=='polynomial_column': vals=[6*A*C*u**3*v-A*d*v**2,v*(3*C*u**2+2*A),D,2*A*e*u**2*v**2,-A*e*u*v**2]
        elif name=='polynomial_mixed': vals=[2*A*C*u*v-2*B*C*d*u*v**2-C*v*u,D,2*B*v*w,2*A*C*u*v-2*B*C*d*u*v**2+C*v*u,2*A*C*u**2-2*B*C*d*v**3+B*C*v*w]
        elif name=='linear_offdiag': vals=[D,0,-A,-D,A]
        elif name=='symbolic_diagonal': vals=[-(A*a+B*b+C*c),-D,A*a+B*b+C*c,D,0]
        elif name=='sparse_cos': vals=[d*s.sin(u)+B*s.sin(w),-d*s.sin(u),C*A*e,D,C*A*e+C*B*d*s.sin(u)**2]
        elif name=='sparse_angle': vals=[D,A*B*C,A*B*C*s.cos(theta),s.sin(theta)*s.cos(theta),A*B*C*s.sin(theta)**2]
        else: raise ValueError('No observed spherical bank')
        return list(map(s.sympify,vals)),['observed-pattern-'+str(i) for i in range(5)]
    if name=='sparse_trig': vals=[D,-D,D/2,-2*A*B*d*u*w,-2*B*d*u*v]; recipes=['determinant','omit-cofactor-sign','omit-power-factor','wrong-held-coordinate','omit-pivot-scale']
    elif name=='sparse_exp': vals=[D,-D,A*d*C*s.exp(w),A*d*B*u*s.exp(w),A*s.exp(w)*(C+B*u)];recipes=['determinant','omit-cofactor-sign','omit-minor-offdiagonal-product','omit-minor-diagonal-product','omit-pivot-scale']
    elif name=='sparse_square': vals=[D,-D,2*A*e*u,2*A*d*e*v,0];recipes=['determinant','omit-cofactor-sign','omit-linear-w-scale','swap-held-coordinate','multiply-zero-diagonal']
    elif name=='log_product': vals=[D,-D,A*B*d/w,A*B*d*u/v,0];recipes=['determinant','wrong-cofactor-sign','omit-minor-u-factor','use-v-derivative-in-w-column','keep-only-canceling-minor']
    elif name=='rotation': vals=[D,-D,A*B*C*s.cos(theta)**2,A*B*C*s.sin(theta)**2,0];recipes=['determinant','wrong-cofactor-sign','omit-sine-product','omit-cosine-product','cancel-instead-of-add']
    elif name=='polynomial_column': vals=[D,-D,B*e*(C*u**3-d*v),B*e*(3*C*u**3+d*v),3*B*C*e*u**3];recipes=['determinant','wrong-cofactor-sign','omit-cubic-power-factor','add-minor-products','omit-second-minor-product']
    elif name=='polynomial_mixed': vals=[D,-D,2*A*C*u**2+2*B*C*d*v**3+B*C*v*w,2*A*C*u**2-2*B*C*d*v**3+B*C*v*w,2*A*C*u**2-B*C*v*w];recipes=['determinant','reverse-all-signs','wrong-second-cofactor-sign','wrong-linear-minor-sign','omit-v-cubed-product']
    elif name=='linear_offdiag':
        P=A*d*e;Q=B*C*p['f'];vals=[D,-D,P-Q,P,Q];recipes=['determinant','reverse-cofactor-signs','subtract-laplace-products','omit-second-cofactor','omit-first-cofactor']
    elif name=='symbolic_diagonal': vals=[D,-D,A*a+B*b+C*c,-(A*a+B*b+C*c),0];recipes=['determinant','reverse-cofactor-sign','sum-diagonal','negative-trace','multiply-offdiagonal-zeros']
    elif name=='sparse_cos':
        vals=[D,-D,C*A*e,C*B*d*s.sin(u)*s.sin(w),C*A*e+C*B*d*s.sin(u)*s.sin(w)];recipes=['determinant','wrong-cofactor-sign','omit-offdiagonal-product','omit-diagonal-product','add-minor-products']
    elif name=='sparse_angle':
        vals=[D,-D,A*B*C,A*B*C*s.sin(theta)**2,A*B*C*s.cos(theta)];recipes=['determinant','wrong-cofactor-sign','omit-offdiagonal-product','keep-offdiagonal-product','omit-square']
    else:
        vals=[D,-D,A*B*C*u*s.sin(v),A*B*C*u**2*s.sin(v)**3,A*B*C*u**2*s.sin(v)*s.cos(v)**2];recipes=['determinant','wrong-cofactor-sign','omit-radial-product-factor','omit-first-cofactor','omit-second-cofactor']
    return list(map(s.sympify,vals)),recipes

def expansion(name,J):
    # Exactly the source row/column and nonzero entries, in their observed order.
    rc={'sparse_trig':('row',0),'sparse_exp':('col',1),'sparse_square':('row',2),
        'log_product':('col',2),'rotation':('row',2),'polynomial_column':('col',2),
        'polynomial_mixed':('col',0),'linear_offdiag':('row',0),'symbolic_diagonal':('row',0),
        'spherical':('row',2),'sparse_cos':('row',1),'sparse_angle':('row',1)}[name]
    kind,index=rc; terms=[]
    for n in range(3):
        i,j=(index,n) if kind=='row' else (n,index)
        if J[i,j]!=0:
            minor=J.minor_submatrix(i,j)
            terms.append((i,j,J[i,j],minor,(-1)**(i+j)))
    return terms

def stages(name,J,D):
    terms=expansion(name,J)
    cofactor='+'.join(par(p)+r'(-1)^{'+str(i+1)+'+'+str(j+1)+'}'+det(m) for i,j,p,m,sign in terms)
    products=[m[0,0]*m[1,1] for _,_,_,m,_ in terms]
    opposites=[m[0,1]*m[1,0] for _,_,_,m,_ in terms]
    arithmetic='+'.join(('' if sign*p==1 else par(sign*p))+r'\left('+tex(x)+'-'+par(y)+r'\right)' for (i,j,p,m,sign),x,y in zip(terms,products,opposites))
    if name in ('polynomial_column','sparse_cos'): return [cofactor,tex(D)]
    if name=='spherical':
        # Keep the separate w-identity and v-identity instructional stages.
        scale=s.simplify(J[0,0]/(s.sin(v)*s.cos(w))*J[1,0]/(s.sin(v)*s.sin(w))*J[2,0]/s.cos(v))
        stage1=par(scale*u**2*s.cos(v)**2*s.sin(v)) + r'\left(\cos^2 w+\sin^2 w\right)+' + par(scale*u**2*s.sin(v)**3)+r'\left(\cos^2 w+\sin^2 w\right)'
        stage2=par(scale*u**2*s.cos(v)**2*s.sin(v))+'+'+par(scale*u**2*s.sin(v)**3)
        stage3=tex(scale*u**2*s.sin(v))+r'\left(\cos^2 v+\sin^2 v\right)'
        return [cofactor,stage1,stage2,stage3,tex(D)]
    if name=='rotation': arithmetic=par(D*s.cos(theta)**2)+'+'+par(D*s.sin(theta)**2)
    return [cofactor,arithmetic,tex(s.factor(D) if name=='sparse_exp' else D)]

def solution(name,F,J,D):
    sid=TEMPLATES[name][1]
    original=ORIGINALS[sid or 'q-39710'][':question/worked-solution']
    # Source common formal operator blocks and all prose remain fixed. Replace
    # full display components; never substring-replace expressions in prose.
    displays=list(re.finditer(r'\$\$(.*?)\$\$',original,re.S))
    replacements={}
    here='Here, we have' in original
    if here:
        replacements[2]=r'\, '.join(f'{label}(u,v,w)='+tex(f) for label,f in zip('xyz',F))+'.'
    partial_index=3 if here else 2
    rows=[]
    for i,label in enumerate('xyz'):
        row=' & '.join(r'\frac{∂'+label+r'}{∂'+str(var)+r'} & ='+tex(J[i,j])+(',' if here and i==2 and j==1 else '') for j,var in enumerate(VARS))
        rows.append(row)
    replacements[partial_index]=r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
    calculated=[det(J)]+stages(name,J,D)
    replacements[partial_index+1]=r'\begin{aligned}\frac{∂(x,y,z)}{∂(u,v,w)} & ='+calculated[0]+r' \\  & ='+r' \\  & ='.join(calculated[1:])+r'.\end{aligned}'
    out=original
    for n,m in reversed(list(enumerate(displays))):
        if n in replacements: out=out[:m.start()]+block(replacements[n])+out[m.end():]
    return out

def prompt(name,F):
    sid=TEMPLATES[name][1]
    original=ORIGINALS[sid or 'q-39710'][':question/problem']
    m=re.search(r'\$\$(.*?)\$\$',original,re.S)
    if name.startswith('sparse_') or name=='log_product':
        math=r'T:[\begin{aligned}u \\ v \\ w\end{aligned}]⟶[\begin{aligned}'+r' \\ '.join(tex(f) for f in F)+r'\end{aligned}].'
    else: math=r'\, '.join(label+'='+tex(f) for label,f in zip('xyz',F))+'.'
    return original[:m.start()]+block(math)+original[m.end():]


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio'): raise ValueError('Only observed radio field layout supported')
    if profile is not None:
        if profile not in PROFILES: raise ValueError('Unknown bank profile')
        t=PROFILES[profile]['template']
        if template is not None and template!=t: raise ValueError('Profile/template mismatch')
        template=t
    eligible=[t for t,(l,_,_) in TEMPLATES.items() if l==level]
    if template is not None and template not in eligible: raise ValueError('Template/difficulty mismatch')
    rng=random.Random(seed);name=template or rng.choice(eligible);profile=profile or name+'-method'
    for _ in range(256):
        p=dict(parameters) if parameters is not None else {k:(rng.randint(-4,4) if k=='k' else rng.choice([-4,-3,-2,-1,1,2,3,4])) for k in TEMPLATES[name][2]}
        try:
            guard(name,p,profile)
            F=components(name,p);J=s.Matrix(F).jacobian(VARS);D=simplify(J.det())
            values,recipes=bank(name,p,J,D,profile)
            if len(values)!=5 or any(equivalent(x,y) for i,x in enumerate(values) for y in values[i+1:]): raise SampleRejected('Complete bank collision')
            hits=[i for i,x in enumerate(values) if equivalent(x,D)]
            if len(hits)!=1: raise SampleRejected('Bank must have exactly one correct determinant')
        except ValueError:
            if parameters is not None: raise
            continue
        break
    else: raise SampleRejected('No valid whole-bank sample in 256 attempts')
    problem=normalize_prose(prompt(name,F));worked=normalize_prose(solution(name,F,J,D))
    mathfp=digest([s.srepr(s.expand(f)) for f in J])
    displayed=[normalize_tex(tex(z)) for z in values]
    content=digest([VERSION,level,problem,worked,sorted(displayed),displayed[hits[0]],'radio','selection'])
    qid=uid(content);fid=uid(content+':selection')
    answers=[{':answer/id':uid(fid+':'+z),':answer/type':':answer.type/math',':answer/value':z} for z in displayed]
    correct=answers[hits[0]][':answer/id'];random.Random(seed).shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,
         ':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[
          {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
      'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,
        'bank_origin':PROFILES[profile]['origin'],'evidence_only':PROFILES[profile]['evidence_only'],
        'eligible_for_learning':not PROFILES[profile]['evidence_only'],'authored_extension':level=='hard',
        'parameter_fingerprint':mathfp,'content_fingerprint':content,'domain':'u*v*w>0' if name=='log_product' else 'u,v,w real; theta,a,b,c fixed real constants',
        'source':{**SOURCE,'question_ids':[TEMPLATES[name][1]] if TEMPLATES[name][1] else [],'method_reference':'lesson Introduction spherical transformation' if level=='hard' else TEMPLATES[name][1]},
        'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plot_rating':'none','plot_assets':{},
        'distractor_recipes':recipes,'notation_normalization':'SymPy LaTeX; same prose and stage sequence'}}

# EASY — four observed nonlinear sparse families, unchanged derivative workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Sparse trig/exp/quadratic/log transforms; signed integer scales 1..4."""
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — all five observed families; observed labels preserved even where
# structural arithmetic is simpler. No invented between-family progression.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Constant rotation/diagonal/linear and two polynomial source families."""
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored from the lesson's spherical direct-Jacobian demonstration.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Nine derivatives, two 2x2 minors, w-identity then v-identity; 512 scales."""
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
    lines=['### Generated — '+q[':question/difficulty'].split('/')[-1],
      'Template: `'+g['template']+'`; bank: `'+g['bank_profile']+'`; '+('evidence-only replay' if g['evidence_only'] else 'eligible learner variant')+'.','',q[':question/problem'],'']
    for a in f[':answer-field/choices']:
        lines.append('- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
    return '\n'.join(lines+['','**Worked solution**','',q[':question/worked-solution']])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=PROFILES)
    ap.add_argument('--format',choices=['markdown','json'],default='markdown');args=ap.parse_args()
    if args.count<1 or args.difficulty=='all' and (args.template or args.profile):ap.error('Positive count; choose a difficulty with template/profile')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
