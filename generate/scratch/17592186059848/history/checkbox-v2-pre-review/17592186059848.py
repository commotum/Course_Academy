#!/usr/bin/env python3
"""Identifying singular 3x3 matrices; local steps 3–7 draft.

All records are local review JSON, never transactions. Exact cofactor expansion,
three statement truth values, and three Boolean checkbox fields are parameterized.
The companion recipes.json holds extracted structure, not source payloads or
answer lookups. Source replay uses the same path as sampled questions. Original
math/layout, field profiles, short and full solution sequences are preserved;
arithmetic is canonically formatted (parentheses/product order/spacing may vary).
Hard is explicitly authored: denser exact fraction/radical arithmetic, still
only calculating a numeric determinant then identifying singularity. No unknown
entries, inverse computation, rank, row-reduction, or other KP is assessed.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059848
KP_UUID='32df8909-a239-5167-b8ea-412f7cdaea93'
TITLE='Identifying Singular Matrices'
VERSION='singularity-cofactor-checkbox-2'
D=Path(__file__).with_suffix('')
EXTRACTION=json.loads((D/'recipes.json').read_text())
TEMPLATES=EXTRACTION['templates']
BANK_PROFILES=EXTRACTION['profiles']
SOURCE=EXTRACTION['source']
OPENING='Remember that a square matrix is singular if its determinant is equal to $0.$'
METHOD='Using the formula, we take the alternating sum of the entries in the top row of the matrix, multiplied by their respective minors, as follows:'
class SampleRejected(ValueError): pass

def exact(value):
    if isinstance(value,float): raise ValueError('Floating-point inputs are unsupported; use exact strings')
    expr=sp.sympify(value)
    if expr.free_symbols or expr.is_real is not True or expr.has(sp.Float) or expr.is_finite is not True:
        raise ValueError('Entries and claims must be finite, real, exact constants')
    if not expr.is_algebraic: raise ValueError('Only algebraic constants are in scope')
    return sp.simplify(expr)

def tex(x):return sp.latex(sp.simplify(x)).replace(r'\frac{',r'\frac{')
def par(x):return '('+tex(x)+')' if x.is_Add or x.could_extract_minus_sign() else tex(x)
def matrix_latex(vals, bars=False):
    core=r'\begin{aligned}'+r' \\ '.join(' & '.join(tex(v)for v in vals[i:i+3])for i in range(0,9,3))+r'\end{aligned}'
    return '|'+core+'|' if bars else '['+core+']'
def minor_latex(vals):return r'|\begin{aligned}'+tex(vals[0])+' & '+tex(vals[1])+r' \\ '+tex(vals[2])+' & '+tex(vals[3])+r'\end{aligned}|'
def sum_tex(vals,skip_zero=False):
    parts=[]
    for v in vals:
        v=sp.simplify(v)
        if skip_zero and v==0:continue
        t=tex(v)
        if parts and not t.startswith('-'):t='+'+t
        parts.append(t)
    return ''.join(parts) or '0'
def expression_sum(parts):
    return ''.join(('+' if i and not t.startswith('-')else '')+t for i,t in enumerate(parts))or '0'
def subset(value):
    if value.startswith('None'):return ()
    return tuple(i+1 for i,n in enumerate(('I','II','III'))if n in value.split())
def truth(m,claims,kinds):
    det=sp.simplify(m.det());singular=det==0
    return tuple(i+1 for i,(kind,c)in enumerate(zip(kinds,claims))if
                 (singular if kind=='singular' else not singular if kind=='nonsingular' else sp.simplify(det-c)==0))
def conclusion(indices):
    if not indices:return 'Therefore, none of the statements are true.'
    names=['I','II','III'];labels=' and '.join(names[i-1]for i in indices)
    return 'Therefore, only statement'+('s ' if len(indices)>1 else ' ')+labels+(' are true.' if len(indices)>1 else ' is true.')

def solution(m,name,indices,spec,style):
    vals=list(m);a,b,c,d,e,f,g,h,i=vals
    mins=[(e,f,h,i),(d,f,g,i),(d,e,g,h)]
    coeff=[a,-b,c]
    products=[(e*i,f*h),(d*i,f*g),(d*h,e*g)]
    minor_values=[sp.simplify(x-y)for x,y in products]
    terms=[sp.simplify(x*y)for x,y in zip(coeff,minor_values)]
    expanded=expression_sum([par(k)+minor_latex(v)for k,v in zip(coeff,mins)])
    prodline=expression_sum(['0' if k==0 else par(k)+'('+sum_tex([x,-y])+')'for k,(x,y)in zip(coeff,products)])
    minorline=expression_sum([par(k)+r'\cdot '+par(v)for k,v in zip(coeff,minor_values)if k!=0])
    rows=[f'det({name}) & ='+matrix_latex(vals,True),' & ='+expanded,' & ='+prodline]
    if spec['solution_rows']==5:
        # Observed compact expansion evaluates the first unit coefficient's
        # minor in its two-product form and keeps the remaining nonzero terms.
        compact=expression_sum(['('+sum_tex([x,-y])+')' if k==1 else par(k)+r'\cdot '+par(v)
                                for k,v,(x,y)in zip(coeff,minor_values,products)if k!=0])
        rows.extend([' & ='+compact,' & ='+tex(sum(terms))])
    else:rows.extend([' & ='+minorline,' & ='+sum_tex(terms,True),' & ='+tex(sum(terms))])
    det=sp.simplify(m.det());nonzero=(r'\ne 0' if style.get('use_ne',True)and det!=0 else '')
    since=f'Since $det({name})={tex(det)}{nonzero}$, the matrix is '+('singular.' if det==0 else '**not** singular.')+' '
    rendered=OPENING+'\n\n'+METHOD+style.get('intro_suffix','')+'\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'+style.get('blank_before_since','\n\n')+since+'\n\n'+conclusion(indices)
    return rendered,{'products':[[str(x),str(y)]for x,y in products],'minors':[str(v)for v in minor_values],'terms':[str(v)for v in terms],'determinant':str(det),'rows':len(rows)}

def validate_parameters(p,spec):
    if set(p)-{'matrix','name','claims','style'}:raise ValueError('Unknown parameter keys')
    if not isinstance(p.get('matrix'),list)or len(p['matrix'])!=9:raise ValueError('matrix must have nine entries')
    vals=[exact(v)for v in p['matrix']];m=sp.Matrix(3,3,vals)
    if spec['level']=='easy' and any(v.is_Integer is not True for v in vals):
        raise ValueError('Easy matrices use signed integer entries')
    if spec['level']!='easy' and any(sp.simplify(v**2).is_Rational is not True for v in vals):
        raise ValueError('Entries must be rational or one rational multiple of a square root')
    radicals={power.base for v in vals for power in v.atoms(sp.Pow) if power.exp==sp.Rational(1,2)}
    if len(radicals)>1:
        raise ValueError('One repeated radical family per matrix is supported')
    if spec['level']=='hard' and any(v==0 for v in vals):
        raise ValueError('Authored hard scope requires nine nonzero entries')
    if not isinstance(p.get('claims'),list)or len(p['claims'])!=3:raise ValueError('claims must have three entries')
    claims=[]
    for kind,c in zip(spec['statements'],p['claims']):
        if kind=='det':
            if c is None:raise ValueError('A determinant statement requires its claim')
            claims.append(exact(c))
        else:
            if c is not None:raise ValueError('Singularity statements have no numeric claim')
            claims.append(None)
    nums=[c for c in claims if c is not None]
    if any(sp.simplify(x-y)==0 for j,x in enumerate(nums)for y in nums[j+1:]):raise SampleRejected('Duplicate determinant claims')
    name=p.get('name','A')
    if name not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or len(name)!=1:raise ValueError('Use one capital matrix name')
    style=p.get('style',{})
    if set(style)-{'use_ne','intro_suffix','blank_before_since'}:raise ValueError('Unknown source formatting keys')
    if style.get('intro_suffix','') not in ('','  ')or style.get('blank_before_since','\n\n')not in ('\n\n','\n\n \n\n'):raise ValueError('Unsupported formatting')
    if 'use_ne'in style and type(style['use_ne'])is not bool:raise ValueError('use_ne must be boolean')
    return m,claims,name,style

# Easy: signed integers. Moderate: fractions or one square-root family.
# Hard: authored dense exact fraction/radical entries; unchanged reasoning method.
def sample_parameters(rng,level,spec):
    lo,hi=(-4,4) if level=='hard' else (-5,8)
    raw=[rng.randint(lo,hi)for _ in range(6)]
    singular=rng.choice([True,False])
    if singular:
        u,v=rng.choice([(1,1),(2,-1),(-1,2),(1,-2)])
        raw.extend([u*raw[j]+v*raw[j+3]for j in range(3)])
    else:raw.extend(rng.randint(lo,hi)for _ in range(3))
    if level=='easy':vals=[sp.Integer(v)for v in raw]
    elif level=='moderate':
        q=rng.choice([2,3,5,7]);den=rng.choice([2,3,5,7])
        col=rng.randrange(3);mode=rng.choice(['fraction','radical','mixed'])
        scales=[sp.Integer(1)]*3
        scales[col]=sp.Rational(1,den) if mode=='fraction' else sp.sqrt(q)
        if mode=='mixed':scales[(col+rng.choice([1,2]))%3]=sp.Rational(1,den)
        vals=[sp.simplify(v*scales[j%3])for j,v in enumerate(raw)]
    else:
        q=rng.choice([2,3,5,7]);den=rng.choice([2,3,4,5])
        # Diagonal column scaling keeps exact singularity structure, while
        # cofactor products require a repeated radical and exact rational arithmetic.
        scales=[sp.sqrt(q)/den,sp.Rational(1,rng.choice([2,3,5])),sp.sqrt(q)/rng.choice([2,3,4])]
        vals=[sp.simplify(v*scales[j%3])for j,v in enumerate(raw)]
        if any(v==0 for v in vals):raise SampleRejected('Hard requires a dense matrix')
    m=sp.Matrix(3,3,vals);det=sp.simplify(m.det())
    if (det==0)!=singular:raise SampleRejected('Unexpected determinant structure')
    claims=[]
    for kind in spec['statements']:
        if kind!='det':claims.append(None)
        else:claims.append(str(rng.choice([det,sp.Integer(0),sp.Integer(1),sp.Integer(-1),sp.Integer(rng.randint(-10,10))])))
    return {'matrix':[str(v)for v in vals],'claims':claims,'name':rng.choice('ADEFMNPQRST')}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Only source checkbox fields are supported')
    rng=random.Random(seed)
    names=[k for k,v in TEMPLATES.items()if v['level']==level]
    template=template or rng.choice(names)
    if template not in names:raise ValueError('Template is not in this level')
    spec=TEMPLATES[template]
    if profile is not None and profile not in BANK_PROFILES:raise ValueError('Unknown complete bank')
    # All three statements are independently represented by Boolean fields.
    eligible=[key for key,bank in BANK_PROFILES.items() if any(sid in spec['source_ids']for sid,_ in bank['source_fields'])]
    profile=profile or rng.choice(eligible or list(BANK_PROFILES))
    profile_extension=profile not in eligible
    bank=BANK_PROFILES[profile]
    for attempt in range(10000):
        try:
            p=parameters if parameters is not None else sample_parameters(rng,level,spec)
            m,claims,name,style=validate_parameters(p,spec)
            indices=truth(m,claims,spec['statements'])
            break
        except SampleRejected:
            if parameters is not None:raise
    else:raise RuntimeError('No valid bank instance within sampling limit')
    p={'matrix':[str(v)for v in m],'name':name,'claims':[None if c is None else str(c)for c in claims],**({'style':style}if style else {})}
    lines=[]
    for n,(kind,c)in enumerate(zip(spec['statements'],claims)):
        value=f'$det({name})={tex(c)}$'if kind=='det'else f'${name}$ is '+('**not** a singular matrix'if kind=='nonsingular'else'a singular matrix')
        lines.append('- **'+('I','II','III')[n]+'.** '+value)
    prompt=f'Which of the following statements are true regarding the matrix ${name}$ given below?\n\nSelect all that apply.\n\n'+('\n\n'if spec['layout']=='checkbox-spaced'else'\n').join(lines)+'\n\n$$\n'+name+'='+matrix_latex(list(m))+'\n$$'
    worked,math_data=solution(m,name,indices,spec,style)
    mathematical={'matrix':p['matrix'],'claims':p['claims'],'statements':spec['statements']}
    paramkey=hashlib.sha256(json.dumps(mathematical,sort_keys=True).encode()).hexdigest()
    content={'version':VERSION,'level':level,'prompt':prompt,'solution':worked,'fields':['I','II','III'],'values':['false','true']}
    contentkey=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    qid=uuid.uuid5(uuid.UUID(KP_UUID),contentkey)
    fields=[]
    for index,label in enumerate(('I','II','III'),1):
        fid=uuid.uuid5(qid,label)
        choices=[{':answer/id':str(uuid.uuid5(fid,'text:'+v)),':answer/type':':answer.type/text',':answer/value':v}for v in ('false','true')]
        correct=choices[int(index in indices)][':answer/id']
        fields.append({':answer-field/id':str(fid),':answer-field/key':label,':answer-field/type':':answer-field.type/checkbox',
            ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,
        ':question/worked-solution':worked,':question/answer-fields':fields},
        'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,
            'parameter_fingerprint':paramkey,'content_fingerprint':contentkey,'bank_profile':profile,'bank_origin':'authored-reuse' if profile_extension else 'observed','profile_extension':profile_extension,
            'authored_extension':level=='hard' or profile_extension,'source_analysis':{**SOURCE,'question_ids':spec['source_ids']},
            'plot_rating':'none','plot_assets':{},'mathematics':math_data,'truth_indices':indices,
            'domain':'finite real algebraic constants; numeric 3x3 matrix','sampling_origin':'authored variation of observed scope'}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question']
    selected=[f[':answer-field/key'] for f in q[':question/answer-fields'] if next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true']
    return q[':question/problem']+'\n\nCorrect selections: '+(', '.join(selected) or 'leave all boxes unchecked')+'\n\n'+q[':question/worked-solution']
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
    print(json.dumps(records,indent=2)if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records))
if __name__=='__main__':main()
