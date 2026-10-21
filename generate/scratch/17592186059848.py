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
VERSION='singularity-cofactor-checkbox-4-bmatrix'
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
    return '|'+core+'|' if bars else r'\begin{bmatrix}'+r' \\ '.join(' & '.join(tex(v)for v in vals[i:i+3])for i in range(0,9,3))+r'\end{bmatrix}'
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

# These bounds are maxima measured over the source questions, rather than a
# claim that entry size alone determines difficulty. Explicit replay is exempt.
ARITHMETIC_LIMITS={
    'easy':{'entry':8,'product':35,'term':48,'term_sum':89,'determinant':30},
    'moderate':{'entry':8,'product':42,'term':28,'term_sum':33,'determinant':23},
}
MODERATE_FAMILIES=('fraction_columns','fraction_rows','mixed_additive_radical',
                   'sparse_rational_radical','fraction_radical_dependent_rows',
                   'radical_column_fraction_entry')

def cofactor_arithmetic(m):
    a,b,c,d,e,f,g,h,i=list(m)
    coeff=[a,-b,c];products=[(e*i,f*h),(d*i,f*g),(d*h,e*g)]
    minors=[sp.expand(x-y)for x,y in products]
    terms=[sp.expand(k*v)for k,v in zip(coeff,minors)]
    det=sp.expand(sum(terms))
    return coeff,products,minors,terms,det

def arithmetic_workload(m):
    _,products,_,terms,det=cofactor_arithmetic(m)
    return {'entry':max(abs(v)for v in m),
            'product':max(abs(v)for pair in products for v in pair),
            'term':max(abs(v)for v in terms),
            'term_sum':sum(abs(v)for v in terms),'determinant':abs(det)}

def integer_structure(rng,singular):
    # Row and column dependencies both occur in the source. Nonzero axes and
    # rank two are checked after construction, so rank-one shortcuts are absent.
    vals=[sp.Integer(rng.randint(-3,4))for _ in range(9)]
    dependency='independent'
    if singular:
        dependency=rng.choice(['row_combination','proportional_rows','proportional_columns'])
        if dependency=='row_combination':
            u,v=rng.choice([(1,1),(2,-1),(-1,2),(1,-2)])
            vals[6:9]=[u*vals[j]+v*vals[j+3]for j in range(3)]
        elif dependency=='proportional_rows':
            factor=rng.choice([-2,-1,1,2]);vals[6:9]=[factor*v for v in vals[:3]]
        else:
            factor=rng.choice([-2,-1,1,2])
            for j in (0,3,6):vals[j+2]=factor*vals[j]
    return vals,dependency

def sample_matrix(rng,level,family=None):
    singular=rng.choice([True,False]);dependency='structured'
    if level=='easy':
        vals,dependency=integer_structure(rng,singular);family='integer'
    elif level=='hard':
        vals,dependency=integer_structure(rng,singular);family='authored_dense_scaled_columns'
        q=rng.choice([2,3,5,7]);den=rng.choice([2,3,4,5])
        scales=[sp.sqrt(q)/den,sp.Rational(1,rng.choice([2,3,5])),sp.sqrt(q)/rng.choice([2,3,4])]
        vals=[v*scales[j%3]for j,v in enumerate(vals)]
        if any(v==0 for v in vals):raise SampleRejected('Hard requires a dense matrix')
    else:
        family=family or rng.choice(MODERATE_FAMILIES)
        q=rng.choice([2,3,5,7]);r=sp.sqrt(q);den=rng.choice([2,3,5,7])
        small=lambda:rng.choice([-2,-1,1,2])
        if family in ('fraction_columns','fraction_rows'):
            vals,dependency=integer_structure(rng,singular)
            scales=[sp.Integer(1)]*3;pos=rng.randrange(3);scales[pos]=sp.Rational(1,den)
            if rng.choice([True,False]):scales[(pos+1)%3]=sp.Rational(1,rng.choice([2,3,5]))
            vals=[v*scales[j%3 if family=='fraction_columns' else j//3]for j,v in enumerate(vals)]
        elif family=='mixed_additive_radical':
            # q-77477: rational plus radical determinant; scaling an entire
            # column cannot create this mixed placement of square roots.
            a,b,d=small(),small(),small()
            c=d if singular else d+rng.choice([-2,-1,1,2])
            e=sp.Rational(q,d) if singular else rng.randint(-3,5)
            vals=[a,b,0,c,r,-d,r,e,-r]
            if not singular and (a*(-q+d*e)==0 or b*(c-d)==0):
                raise SampleRejected('Require both rational and radical determinant terms')
        elif family=='sparse_rational_radical':
            # q-128491: radicals in separated positions, a rational entry,
            # and a rational determinant after radical products cancel.
            a,c,e,g=small(),small(),small(),small();b=rng.choice([-1,1])
            if singular:
                # Keep the exact dependence affordable at the source workload.
                q=rng.choice([2,3]);r=sp.sqrt(q);den=2
                a,g=rng.choice([-1,1]),rng.choice([-1,1])
            f=sp.Rational(a*g*q*den,b) if singular else rng.randint(-5,5)
            vals=[a*r,0,sp.Rational(b,den),c*r,e,0,f,0,g*r]
        elif family=='fraction_radical_dependent_rows':
            # q-128490, with an optional final-entry offset breaking the relation.
            e,f,j=small(),rng.randint(-3,5),small()
            delta=0 if singular else rng.choice([-2,-1,1,2])
            vals=[r,0,sp.Rational(1,den),0,e,f,-den*j*r,e,f-j+delta]
        else:
            # q-128484: one radical column plus a rational entry in another.
            a,c,b,e,j=small(),small(),small(),small(),small();k=den*j
            delta=0 if singular else rng.choice([-2,-1,1,2])
            vals=[a,r,c,sp.Rational(b,den),0,e,a-j*b,r,c-k*e+delta]
    m=sp.Matrix(3,3,vals)
    # The originals require arithmetic even when two rows/columns are
    # proportional. A completely zero axis introduces an easier shortcut.
    if any(all(v==0 for v in axis)for j in range(3)for axis in (m.row(j),m.col(j))):
        raise SampleRejected('Zero rows and columns bypass the intended arithmetic')
    det=cofactor_arithmetic(m)[-1]
    if (det==0)!=singular:raise SampleRejected('Unexpected determinant structure')
    if singular and m.rank()!=2:raise SampleRejected('Require rank-two singular matrices')
    if level=='moderate' and all(v.is_Integer for v in m):raise SampleRejected('Moderate needs fractions or radicals')
    workload=arithmetic_workload(m)
    if level in ARITHMETIC_LIMITS and any(workload[k]>limit for k,limit in ARITHMETIC_LIMITS[level].items()):
        raise SampleRejected('Exceeds source arithmetic workload')
    return m,{'matrix_family':family,'dependency':dependency,
              'arithmetic_workload':{k:str(v)for k,v in workload.items()}}

def false_claims(m):
    """Authored arithmetic mistakes, never inferred source misconception labels.

    Candidates inherit the matrix's fractions, radicals and scale. In particular,
    a large integer or radical claim is no longer automatically a true claim.
    """
    coeff,products,minors,terms,det=cofactor_arithmetic(m)
    candidates=[(-det,'reverse_determinant_sign'),(sp.Integer(0),'assume_zero'),
                (sp.trace(m),'report_trace')]
    for j in range(3):
        candidates.extend([(det-2*terms[j],f'reverse_cofactor_sign_{j}'),
                           (det-terms[j],f'omit_cofactor_{j}'),
                           (det+2*coeff[j]*products[j][1],f'add_minor_products_{j}'),
                           (det-terms[j]+minors[j],f'omit_coefficient_{j}'),
                           (terms[j],f'report_cofactor_{j}')])
    candidates.extend((v,f'report_entry_{j}')for j,v in enumerate(m))
    result=[];seen=set()
    for value,recipe in candidates:
        value=sp.expand(value)
        if value!=det and value not in seen:result.append((value,recipe));seen.add(value)
    return result

def sample_parameters(rng,level,spec,return_metadata=False,matrix_family=None):
    m,metadata=sample_matrix(rng,level,matrix_family);det=cofactor_arithmetic(m)[-1]
    pool=false_claims(m);claims=[];recipes=[];used=set()
    for kind in spec['statements']:
        if kind!='det':claims.append(None);recipes.append(None);continue
        choices=[(v,recipe)for v,recipe in pool if v not in used]
        if det not in used and rng.choice([True,False]):value,recipe=det,'correct_determinant'
        elif choices:value,recipe=rng.choice(choices)
        else:raise SampleRejected('No distinct arithmetic claim')
        used.add(value);claims.append(str(value));recipes.append(recipe)
    p={'matrix':[str(v)for v in m],'claims':claims,'name':rng.choice('ADEFMNPQRST')}
    metadata['claim_recipes']=recipes
    return (p,metadata) if return_metadata else p

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
    # Choose the family before whole-instance rejection; arithmetic rejection
    # must not quietly suppress the less frequently accepted source structures.
    matrix_family=rng.choice(MODERATE_FAMILIES) if level=='moderate' and parameters is None else None
    for attempt in range(10000):
        try:
            if parameters is not None:p=parameters;sampling=None
            else:p,sampling=sample_parameters(rng,level,spec,return_metadata=True,matrix_family=matrix_family)
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
            'domain':'finite real algebraic constants; numeric 3x3 matrix','sampling_origin':'explicit parameters' if parameters is not None else 'authored variation of observed scope',
            'sampling':sampling}}

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

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
