#!/usr/bin/env python3
"""Finding inverse Jacobians, immutable math basis 1356; steps 3–7 only.

Observed templates: six moderate and six hard, five-option radio fields.
Every source is a full parameterized inverse-coordinate scaling recipe:
(u,v,w)=(a*f,b*g,c*h). Jacobian rows scale by a,b,c. The original opaque
banks transport by B(u/a,v/b,w/c)/(abc) as explicit evidence-only profiles;
this is an exact coordinate change, not an inferred historical error recipe.
Normal banks use actual erroneous Jacobian operations: no reciprocal,
cofactor sign reversal, first derivative row missing its scale a, and that
row applying a twice. The entire five-member bank is rejected on collision.
One fixed source-derived worked solution includes formal matrix, all nine
partials, cofactor expansion, arithmetic, coordinate rewrite when applicable,
and reciprocal. Source omissions and exact spelling are preserved at a=b=c=1.

Easy is authored: a single nonunit diagonal inverse-coordinate coefficient.
Moderate defaults select all six observed inverse-map families before sampling;
the authored two-factor diagonal map remains an explicit template. Hard needs nonlinear
inverse components and the additional uvw rewrite. Bounds are finite and checked
on explicit parameters. No critical-point, direct-map, or integration assessment.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, hashlib, importlib.util, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
DIR=Path(__file__).with_suffix('')
_spec=importlib.util.spec_from_file_location('inverse_jacobian_readback',DIR/'readback.py')
rb=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(rb)
x,y,z,u,v,w=(getattr(rb,k) for k in ('x','y','z','u','v','w'))
WRAPPER=json.loads((DIR/'source.json').read_text()); RAW=WRAPPER['record']
KP_ID=17592186129269; KP_UUID=RAW[':knowledge-point/id']; TITLE=RAW[':knowledge-point/title']
VERSION='inverse-jacobian-v3-audit9837'
import math_format
SOURCE={k:WRAPPER[k] for k in ('database','basis','lineage')}
Q={q[':question/math-academy-id']:q for q in RAW[':knowledge-point/questions']}
TEMPLATES={key.replace('q-','source_'):key for key in Q}
LEVELS={t:Q[k][':question/difficulty'][':db/ident'].split('/')[-1] for t,k in TEMPLATES.items()}
LEVELS.update(easy_diagonal='easy',moderate_diagonal='moderate')

def scalar(s): return rb.scalar(s)
def tex(e): return sp.latex(e).replace(r'\log',r'\ln')
def displays(s): return [m[1] for m in re.finditer(r'\$\$(.*?)\$\$',s,re.S)]
def base_components(key):
    block=displays(Q[key][':question/problem'])[0].strip()
    if key=='q-161797' or Q[key][':question/difficulty'][':db/ident'].endswith('moderate'):
        return tuple(part.split('=',1)[1].strip().rstrip('.') for part in block.split(r'\,'))
    return tuple(block.split('⟶',1)[1][len(r'[\begin{aligned}'):-len(r'\end{aligned}].')].split(r'\\'))
BASE={k:tuple(scalar(a) for a in base_components(k)) for k in Q}

# Complete-component masks: grouping prevents numerical juxtaposition and signs.
def scaled(raw,k):
    if scalar(raw)==0: return raw
    if k==1:return raw
    match=re.fullmatch(r'(\s*)(.*?)([.,]?\s*)',raw,re.S)
    return match[1]+tex(k)+r'\left('+match[2]+r'\right)'+match[3]
def transported(raw,p,factor=1):
    # Protect command names only; their mathematical arguments remain variable.
    pieces=re.split(r'(\\[A-Za-z]+)',raw)
    subs={letter:(letter if p[letter]==1 else r'\left(\frac{'+letter+'}{'+str(p[letter])+r'}\right)') for letter in ('u','v','w')}
    raw=''.join(piece if piece.startswith('\\') else re.sub('[uvw]',lambda m:subs[m[0]],piece) for piece in pieces)
    return scaled(raw,factor)
def array(cells):
    return r'|\begin{aligned}'+r' \\ '.join(' & '.join(row) for row in cells)+r'\end{aligned}|'
def protect_arrays(block):
    arrays=[]
    def save(m):
        arrays.append(m[0]); return 'ARRAY'+str(len(arrays)-1)+'TOKEN'
    block=re.sub(r'\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}',save,block,flags=re.S)
    return block,arrays

def render_source(key,p,repair=False):
    """Render masks for any permitted coordinate scales, including source replay."""
    q=Q[key]; coeff=(p['u'],p['v'],p['w']); product=sp.prod(coeff)
    original=base_components(key)
    prompt=q[':question/problem']
    block=displays(prompt)[0]
    if q[':question/difficulty'][':db/ident'].endswith('moderate'):
        parts=block.split(r'\,')
        out=[]
        for i,part in enumerate(parts):
            lhs,rhs=part.split('=',1); ending=''
            if rhs.endswith('.\n'):rhs=rhs[:-2];ending='.\n'
            out.append(lhs+'='+scaled(rhs,coeff[i])+ending)
        newblock=r'\,'.join(out)
    else:
        before,after=block.split('⟶',1)
        cells=after[len(r'[\begin{aligned}'):after.index(r'\end{aligned}')].split(r'\\')
        newblock=before+'⟶'+r'[\begin{aligned}'+r'\\'.join(scaled(a,c) for a,c in zip(cells,coeff))+after[after.index(r'\end{aligned}'):]
    prompt=prompt.replace('$$'+block+'$$','$$'+newblock+'$$')
    sol=q[':question/worked-solution']
    if repair and key=='q-39300':
        sol=sol.replace('y(x,y,z)=', 'v(x,y,z)=').replace('z(x,y,z)={y}', 'w(x,y,z)={y}')
    if repair and key=='q-161807':
        sol=sol.replace(r'-{z}^{2}|\begin{aligned}2xy & {x}^{2}',r'-{z}^{2}|\begin{aligned}2xz & {x}^{2}')
    # Work by stage position and complete displayed components, retaining prose.
    start=sol.index('First, we find the partial derivatives:')
    first=sol[:start]; rest=sol[start:]
    if 'Here, we have' in first:
        here=displays(first)[-1]
        parts=here.split(r'\,');out=[]
        for i,part in enumerate(parts):
            lhs,rhs=part.split('=',1);ending=''
            if rhs.endswith('.\n'):rhs=rhs[:-2];ending='.\n'
            out.append(lhs+'='+scaled(rhs,coeff[i])+ending)
        changed=r'\,'.join(out)
        first=first.replace('$$'+here+'$$','$$'+changed+'$$')
    blocks=displays(rest)
    # All nine partials, including zero contributions.
    partial=blocks[0]; rows=partial.strip()[len(r'\begin{aligned}'):-len(r'\end{aligned}')].split(r'\\')
    newrows=[]
    for i,row in enumerate(rows):
        newrows.append(re.sub(r'& =([^&]+)',lambda m:'& ='+scaled(m[1],coeff[i]),row))
    partial_new=partial[:partial.index(r'\begin{aligned}')]+r'\begin{aligned}'+r'\\'.join(newrows)+r'\end{aligned}'+partial[partial.index(r'\end{aligned}')+len(r'\end{aligned}'):]
    rest=rest.replace('$$'+partial+'$$','$$'+partial_new+'$$')
    # Det expansion: row-scaled matrix, then factor abc around the source's
    # complete cofactor masks. This preserves each ordered arithmetic stage.
    det=blocks[1]; protected,arrays=protect_arrays(det)
    rows=protected.split(r'\\')
    if len(rows)<3: raise ValueError('Lost source determinant stages')
    numeric=arrays[1]; body=numeric[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
    cells=[row.split('&') for row in body.split(r'\\')]
    arrays[1]=r'\begin{aligned}'+r'\\'.join('&'.join(scaled(cell,coeff[i]) for cell in row) for i,row in enumerate(cells))+r'\end{aligned}'
    for i in range(2,len(rows)):
        head,rhs=rows[i].split('=',1)
        suffix=''
        if rhs.rstrip().endswith(r'\end{aligned}'):
            suffix=rhs[rhs.index(r'\end{aligned}'):]; rhs=rhs[:rhs.index(r'\end{aligned}')]
        if product!=1: rhs=tex(product)+r'\left('+rhs.strip().rstrip('.')+r'\right)'+('.' if rhs.strip().endswith('.') else '')
        if i==len(rows)-1 and product!=1:
            rhs=tex(sp.prod(coeff)*sp.Matrix(BASE[key]).jacobian((x,y,z)).det())+('.' if rhs.strip().endswith('.') else '')
        rows[i]=head+'='+rhs+suffix
    det_new=r'\\'.join(rows)
    for i,a in enumerate(arrays): det_new=det_new.replace('ARRAY'+str(i)+'TOKEN',a)
    rest=rest.replace('$$'+det+'$$','$$'+det_new+'$$')
    # Conversion rows and reciprocal rows carry the exact coordinate transport.
    for b in blocks[2:]:
        if '\\frac{∂(x,y,z)}' in b:
            protected=b; arrays=[]; rows=protected.split(r'\\')
            for i in range(1,len(rows)):
                head,rhs=rows[i].split('=',1); suffix=''
                if rhs.rstrip().endswith(r'\end{aligned}'):
                    suffix=rhs[rhs.index(r'\end{aligned}'):]; rhs=rhs[:rhs.index(r'\end{aligned}')]
                match=re.fullmatch(r'(\s*)(.*?)(\.?\s*)',rhs,re.S)
                rhs=match[1]+transported(match[2],p,sp.Rational(1,product))+match[3]
                if i==len(rows)-1 and coeff!=(1,1,1):
                    rhs=tex(1/inverse_data(key,p)[3])+('.' if rhs.strip().endswith('.') else '')
                rows[i]=head+'='+rhs+suffix
            changed=r'\\'.join(rows)
            for i,a in enumerate(arrays): changed=changed.replace('ARRAY'+str(i)+'TOKEN',a)
        else:
            # Every equation side in uvw rewrite is independently transported.
            text=b[b.index(r'\begin{aligned}')+len(r'\begin{aligned}'):b.index(r'\end{aligned}')]; rows=text.split(r'\\'); out=[]
            for row in rows:
                left,right=row.split('& =',1)
                def carry(raw,conversion):
                    match=re.fullmatch(r'(\s*)(.*?)(\.?\s*)',raw,re.S)
                    return match[1]+conversion(match[2])+match[3] if match[2] else raw
                left=carry(left,lambda value:scaled(value,product))
                right=carry(right,lambda value:transported(value,p,product))
                out.append(left+'& ='+right)
            changed=b[:b.index(r'\begin{aligned}')]+r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'+b[b.index(r'\end{aligned}')+len(r'\end{aligned}'):]
        rest=rest.replace('$$'+b+'$$','$$'+changed+'$$')
    if coeff!=(1,1,1):
        rest=rest.replace('Therefore, the corresponding Jacobian determinant', 'Scaling the three derivative rows by $'+', '.join(map(str,coeff))+'$ multiplies the determinant by $'+str(product)+'$.\n\nTherefore, the corresponding Jacobian determinant',1)
    return prompt,first+rest

def inverse_data(key,p):
    factors=(p['u'],p['v'],p['w']); F=tuple(a*b for a,b in zip(factors,BASE[key]))
    J=sp.Matrix(F).jacobian((x,y,z)); Dxy=sp.factor(J.det())
    D0=sp.factor(sp.Matrix(BASE[key]).jacobian((x,y,z)).det())
    # Canonical rewrites are mathematical formulas, not answer lookups.
    family={
      'q-39300':2*u**2*sp.sqrt(w),
      'q-161804':u*v*w,
      'q-161805':-u,
      'q-161806':2*sp.sqrt(u*v*w),
      'q-161807':9*(u*v*w)**sp.Rational(2,3),
      'q-161808':-u,
    }
    D=family.get(key,D0)
    D=sp.prod(factors)*D.subs({u:u/p['u'],v:v/p['v'],w:w/p['w']}, simultaneous=True)
    return F,J,Dxy,sp.factor(D)

# Easy: authored single diagonal scale; 22 genuine signed coefficient tasks.
def _easy(p):
    a=p['a']; F=(a*x,y,z); J=sp.diag(a,1,1); D=sp.Integer(a)
    return F,J,D,D
# Moderate: authored two nonunit diagonal scales, determinant arithmetic <=40.
def _moderate(p):
    a,b=p['a'],p['b']; F=(a*x,b*y,z); J=sp.diag(a,b,1);D=sp.Integer(a*b)
    return F,J,D,D
# Hard uses the six observed nonlinear inverse-map families with uvw rewrites.

def bounds(level,template,p,raw=False):
    if template=='easy_diagonal':
        if set(p)!={'a'} or type(p['a']) is not int or not 2<=abs(p['a'])<=12:raise ValueError('easy: integer 2<=|a|<=12')
    elif template=='moderate_diagonal':
        if set(p)!={'a','b'} or any(type(p[k]) is not int or not 2<=abs(p[k])<=8 for k in p) or abs(p['a']*p['b'])>40:raise ValueError('moderate: two nonunit scales 2..8, product<=40')
    else:
        if set(p)!={'u','v','w'} or any(type(p[k]) is not int or not 1<=p[k]<=4 for k in p) or sp.prod(p.values())>32:raise ValueError('source scale integers 1..4, product<=32')
        if not raw and p['u']==1:raise ValueError('normal method bank requires first row nonunit scale')
        if level=='moderate':
            F,J,Dxy,D=inverse_data(TEMPLATES[template],p)
            if abs(D)>120 or any(abs(c)>12 for e in J for c in sp.Poly(e,x,y,z).coeffs()):raise ValueError('moderate coefficient/determinant ceiling')

def domain(level,template,key=None):
    if key=='q-39300':return 'x != 0, y > 0; u != 0, w > 0'
    if key=='q-161804':return 'x,y,z real; u,v,w > 0'
    if key=='q-161805':return 'x != 0; u != 0'
    if key=='q-161806':return 'x,y,z > 0; u,v,w > 0'
    if key=='q-161807':return 'normal: x,y,z > 0; raw source: x,y,z != 0, fractional powers use real cube roots'
    if key=='q-161808':return 'y,z != 0; u,v != 0'
    return 'x,y,z real; nonzero constant inverse determinant'

def authored_solution(F,J,Dxy,D):
    formal=array([[r'\frac{\partial '+out+r'}{\partial '+inp+'}' for inp in ('x','y','z')] for out in ('u','v','w')])
    partial=r'\begin{aligned}'+r' \\ '.join(' & '.join(r'\frac{\partial '+out+r'}{\partial '+inp+r'}='+tex(J[i,j]) for j,inp in enumerate(('x','y','z'))) for i,out in enumerate(('u','v','w')))+r'\end{aligned}'
    numeric=array([[tex(e) for e in J.row(i)] for i in range(3)])
    det=tex(J[0,0])+array([[tex(e) for e in J.row(i)[1:]] for i in (1,2)])
    evaluated=tex(J[0,0])+r'\left('+tex(J[1,1])+r'\cdot '+tex(J[2,2])+r'-0\right)'
    return ('For a transformation\n\n$$T:(u,v,w)\\to(x(u,v,w),y(u,v,w),z(u,v,w)),$$\n\nthe Jacobian determinant of $T$ is $\\frac{\\partial(x,y,z)}{\\partial(u,v,w)}$.\n\nIn this case, we\'re only given ${T}^{-1}.$ So, we compute the Jacobian determinant of $T$ as follows:\n\n- First, we compute $\\frac{\\partial(u,v,w)}{\\partial(x,y,z)}$, the Jacobian determinant of ${T}^{-1}$.\n\n- Then, we will compute the Jacobian determinant of $T$ using the relation\n\n$$\\frac{\\partial(x,y,z)}{\\partial(u,v,w)}=\\left(\\frac{\\partial(u,v,w)}{\\partial(x,y,z)}\\right)^{-1}.$$\n\nFirst, we find the partial derivatives:\n\n$$'+partial+'$$\n\nTherefore, the corresponding Jacobian determinant of ${T}^{-1}$ is\n\n$$\\begin{aligned}\\frac{\\partial(u,v,w)}{\\partial(x,y,z)}&='+formal+r' \\ &='+numeric+r' \\ &='+det+r' \\ &='+evaluated+r' \\ &='+tex(Dxy)+r'\end{aligned}'+'$$\n\nFinally, we take the reciprocal:\n\n$$\\begin{aligned}\\frac{\\partial(x,y,z)}{\\partial(u,v,w)}&=\\left(\\frac{\\partial(u,v,w)}{\\partial(x,y,z)}\\right)^{-1}'+r' \\ &='+tex(1/D)+r'\end{aligned}'+'$$')

def eligible_parameters(level,template,profile):
    raw=profile in ('observed','source-repaired')
    if template=='easy_diagonal':pool=({'a':a} for a in range(-12,13) if abs(a)>=2)
    elif template=='moderate_diagonal':pool=({'a':a,'b':b} for a,b in itertools.product(range(-8,9),repeat=2) if abs(a)>=2 and abs(b)>=2 and abs(a*b)<=40)
    else:pool=({'u':a,'v':b,'w':c} for a,b,c in itertools.product(range(1,5),repeat=3))
    result=[]
    for p in pool:
        try:bounds(level,template,p,raw)
        except ValueError:continue
        result.append(p)
    return result

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio fields supported')
    rng=random.Random(seed)
    if template is None:
        # Choose a whole observed method family before its finite parameter bank.
        # Authored moderate_diagonal stays available by explicit template only.
        template='easy_diagonal' if level=='easy' else rng.choice([t for t in TEMPLATES if LEVELS[t]==level])
    if template not in LEVELS or LEVELS[template]!=level:raise ValueError('template difficulty mismatch')
    profile=profile or 'method'
    if profile not in ('method','observed','source-repaired'):raise ValueError('unknown complete bank')
    if template not in TEMPLATES and profile!='method':raise ValueError('authored template has no observed bank')
    raw=profile in ('observed','source-repaired')
    pool=eligible_parameters(level,template,profile)
    p=dict(parameters) if parameters is not None else dict(rng.choice(pool))
    bounds(level,template,p,raw)
    key=TEMPLATES.get(template)
    if key:
        F,J,Dxy,D=inverse_data(key,p)
        prompt,solution=render_source(key,p,repair=profile!='observed')
        if profile!='observed' and key=='q-161807':prompt=prompt.replace(r'x,y,z\ne 0',r'x,y,z>0')
        a=p['u']
    else:
        F,J,Dxy,D=(_easy(p) if level=='easy' else _moderate(p))
        prompt='Find the Jacobian determinant of the transformation $T:(u,v,w)\\to(x(u,v,w),y(u,v,w),z(u,v,w))$, given that\n\n$$'+r'\qquad '.join(letter+'='+tex(f) for letter,f in zip(('u','v','w'),F))+'.$$'
        solution=authored_solution(F,J,Dxy,D); a=p['a']
    C=sp.factor(1/D)
    if raw:
        field=Q[key][':question/answer-fields'][0]
        strings=[transported(ans[':answer/value'],p,sp.Rational(1,sp.prod(p.values()))) for ans in field[':answer-field/choices']]
        expressions=[scalar(s) for s in strings]
        correct_index=next(i for i,ans in enumerate(field[':answer-field/choices']) if ans[':answer/id']==field[':answer-field/correct'][':answer/id'])
        recipes=['coordinate_transport_of_observed_'+str(i) for i in range(5)]
    else:
        if level=='easy':
            expressions=[C,D,-C,sp.Integer(1),C/a]
            recipes=['correct','no_reciprocal','reverse_sign','omit_nonunit_derivative','apply_coefficient_twice']
        else:
            expressions=[C,D,-C,a*C,C/a]
            recipes=['correct','no_reciprocal','reverse_cofactor_sign','omit_first_row_scale','apply_first_row_scale_twice']
        strings=[tex(e) for e in expressions];correct_index=0
    for i,e in enumerate(expressions):
        if e.has(sp.zoo,sp.nan,sp.oo,-sp.oo):raise ValueError('nonfinite complete bank')
        for other in expressions[:i]:
            if sp.simplify(e-other)==0:raise ValueError('whole bank collision')
    if sp.simplify(expressions[correct_index]-C)!=0:raise ValueError('source correct answer mismatch')
    if not raw:
        prompt=math_format.normalize_prose(prompt)
        solution=math_format.normalize_prose(solution)
        strings=[math_format.normalize_tex(s) for s in strings]
    effective_domain=domain(level,template,key)
    if key=='q-161807':effective_domain='x,y,z != 0; real cube-root interpretation' if profile=='observed' else 'x,y,z > 0; u,v,w > 0'
    fingerprint=hashlib.sha256(json.dumps({'level':level,'inverse_components':[sp.srepr(e) for e in F],'domain':effective_domain},sort_keys=True).encode()).hexdigest()
    content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(strings)}
    content_hash=hashlib.sha256(json.dumps(asset_payload(content),sort_keys=True).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content_hash));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),s)),':answer/type':':answer.type/math',':answer/value':s} for s in strings]
    correct=choices[correct_index][':answer/id'];rng.shuffle(choices)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':template,'profile':profile,'parameters':p,'domain':effective_domain,'mathematical_fingerprint':fingerprint,'content_hash':content_hash,'recipes':recipes,'source_id':key,'evidence_only':raw,'eligible_for_learning':not raw,'solution_repairs':(['incorrect_component_labels'] if key=='q-39300' else ['incorrect_cofactor_minor','positive_branch_clarification'] if key=='q-161807' else []) if profile!='observed' else [],'dependencies':{'python':sys.version,'sympy':sp.__version__},'plot_rating':'none'}}
    if not raw:math_format.validate_generated_record(record)
    return record

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
