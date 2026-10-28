#!/usr/bin/env python3
"""Volume by a change of variables, frozen basis 1356, draft 1.

Six observed families, seven complete raw banks (including legacy fields), and
eight supported normal families. Raw banks are opaque/incomplete designation
EVIDENCE, not default learner generation. Raw recipes genuinely stretch the v
interval by h, and recompute every occurrence and volume; h=1 replays the source.
Default banks consist of complete, family-specific integration errors.
Easy: authored affine shear with constant Jacobian and integer box endpoints.
Moderate: observed affine yz/xz or quadratic triangular shear, constant Jacobian.
Hard: observed product/log, square root, reciprocal, or canonical cube-root maps,
variable Jacobian; familiar primitive/endpoints only. No general integrands.
No database writes, engine changes, registration, or plotting needed: the practice
sources contain no plots, and canonical pictures are symbolic map notation.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('');KP_ID=17592186198399
SOURCE=json.loads((HERE/'source.json').read_text()); RECORD=SOURCE['record']
KP_UUID=RECORD[':knowledge-point/id'];TITLE=RECORD[':knowledge-point/title'];VERSION='volume-change-1-audit9837'
x,y,z=s.symbols('x y z',real=True);u,v,w=s.symbols('u v w',positive=True)
XYZ=(x,y,z);UVW=(u,v,w)
FAMILIES={'easy':('affine',),'moderate':('linear_yz','shear','linear_xz'),'hard':('log','sqrt','reciprocal','cube')}
SOURCE_FAMILIES=dict(zip([q[':db/id'] for q in RECORD[':knowledge-point/questions']],('linear_yz','reciprocal','log','shear','linear_xz','sqrt')))
RAW=json.loads((HERE/'raw-recipes.json').read_text())
class SampleRejected(ValueError):pass

def tex(e):return s.latex(s.expand_log(s.sympify(e),force=True),order='lex').replace(r'\log',r'\ln')
def group(a):return r'\left('+a+r'\right)'
def block(a):return '$$\n'+a+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}')
def stable(q):return hashlib.sha256(json.dumps(asset_payload(q),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(q):return str(uuid.uuid5(uuid.NAMESPACE_URL,TITLE+':'+q))
def enum(q):return q[':db/ident'] if isinstance(q,dict) else q

def model(f,p):
    a,b,c,d=(p[k] for k in 'abcd')
    if f=='affine':trans=(a*x,y+b*x,c*z);inverse=(u/a,v-b*u/a,w/c)
    elif f=='linear_yz':
        trans=(x,a*y+b*z,c*y+d*z);D=a*d-b*c;inverse=(u,(d*v-b*w)/D,(a*w-c*v)/D)
    elif f=='shear':trans=(x,a*x+y,z+b*x*x+c*y*y);inverse=(u,v-a*u,w-b*u*u-c*(v-a*u)**2)
    elif f=='linear_xz':trans=(a*x+b*z,y,c*y+d*z);inverse=((u-b*(w-c*v)/d)/a,v,(w-c*v)/d)
    elif f=='log':trans=(x,y+a*x*x,b*x*z);inverse=(u,v-a*u*u,w/(b*u))
    elif f=='sqrt':trans=(x,a*x*x-y-b*z,s.sqrt(z));inverse=(u,a*u*u-b*w*w-v,w*w)
    elif f=='reciprocal':trans=(y,s.sqrt(y)+x,1/(z+a));inverse=(v-s.sqrt(u),u,1/w-a)
    elif f=='cube':
        trans=(a*x+b*y,c*x+d*y,z**3);D=a*d-b*c;inverse=((d*u-b*v)/D,(a*v-c*u)/D,w**s.Rational(1,3))
    else:raise ValueError('Unknown template')
    M=s.Matrix(trans).jacobian(XYZ);det=s.factor(M.det())
    if det==0:raise ValueError('Singular map')
    detuv=s.simplify(det.subs(dict(zip(XYZ,inverse)),simultaneous=True))
    if f=='reciprocal':detuv=w*w # y,x swap and reciprocal derivative both negative
    if f=='sqrt':detuv=-1/(2*w)
    jac=s.simplify(1/detuv)
    if f in ('log','cube'):J=s.simplify(1/s.Abs(p['b']*u if f=='log' else 3*(a*d-b*c)*w**s.Rational(2,3)))
    elif f=='sqrt':J=2*w
    elif f=='reciprocal':J=1/w**2
    else:J=1/abs(detuv)
    bounds=tuple((p['l'+t],p['h'+t]) for t in ('u','v','w'))
    primitive=tuple(s.integrate(J if J.has(t) else 1,t) for t in UVW)
    const=J if not J.free_symbols else s.Integer(1)
    endpoints=tuple((s.simplify(P.subs(t,hi)),s.simplify(P.subs(t,lo))) for t,P,(lo,hi) in zip(UVW,primitive,bounds))
    volume=s.simplify(const*s.prod(hi-lo for hi,lo in endpoints))
    return dict(trans=trans,inverse=inverse,matrix=M,det=det,detuv=detuv,jac=jac,J=J,bounds=bounds,primitive=primitive,const=const,endpoints=endpoints,volume=volume)

def guard(level,f,p):
    if set(p)!=set('abcd')|{'lu','hu','lv','hv','lw','hw'}:raise ValueError('Need coefficients a,b,c,d and all six bounds')
    for k in 'abcd':
        if p[k].is_Integer is not True or not 1<=abs(p[k])<=3:raise ValueError('Nonzero integer coefficients, magnitude 1..3')
    if f not in FAMILIES[level]:raise ValueError('Template outside authored/observed difficulty scope')
    for t in 'uvw':
        lo,hi=p['l'+t],p['h'+t]
        if lo.is_Rational is not True or hi.is_Rational is not True:raise ValueError('Exact rational endpoints required')
        if not (hi-lo).is_positive or abs(lo)>6 or abs(hi)>12:raise ValueError('Ordered endpoints within arithmetic ceiling')
        if lo.q>2 or hi.q>2:raise ValueError('Integer or half-integer endpoints only')
    if level=='easy':
        if f!='affine' or p['lu']!=0 or p['lv']!=0 or p['lw']!=0 or p['hu']>6 or p['hv']>6 or p['hw']>6:raise ValueError('Easy zero lower bounds; widths <=6')
        if p['a']<2 or p['c']<2:raise ValueError('Easy keeps two nonunit scale factors')
    if f=='shear' and p['a']*p['b']*p['c']==0:raise ValueError('Preserve all nonlinear shear derivative demands')
    if f in ('log','reciprocal','sqrt','cube'):
        if any(p['l'+t]<=0 for t in ('u',) if f=='log') or p['lw']<=0:raise ValueError('Positive branch away from singularities')
    if f=='reciprocal' and p['lu']<=0:raise ValueError('Square root shear uses positive y')
    if f=='cube' and any(s.real_root(p[k],3).is_Integer is not True for k in ('lw','hw')):raise ValueError('Cube endpoints must be perfect cubes')
    model(f,p)

def sample(level,f,r):
    widths=r.sample((2,3,4,5,6),3)
    p={k:s.Integer(r.choice((-3,-2,-1,1,2,3))) for k in 'abcd'}
    for t,width in zip('uvw',widths):p['l'+t]=s.Integer(r.choice((-2,-1,1,2)));p['h'+t]=p['l'+t]+width
    if level=='easy':
        p.update(a=s.Integer(r.choice((2,3))),c=s.Integer(r.choice((2,3))))
        for t,width in zip('uvw',widths):p['l'+t]=s.Integer(0);p['h'+t]=s.Integer(width)
    if f=='log':p.update(lu=s.Rational(1,2),hu=s.Integer(r.choice((2,3,4))),lw=s.Integer(1));p['hw']=1+widths[2]
    if f in ('sqrt','reciprocal'):p.update(lw=s.Integer(1),hw=s.Integer(r.choice((3,4,5))));
    if f=='reciprocal':p.update(lu=s.Integer(1),hu=s.Integer(1+widths[0]))
    if f=='cube':p.update(lw=s.Integer(1),hw=s.Integer(8))
    return {k:s.sympify(v) for k,v in p.items()}

def bank(f,p,m):
    """One fixed complete operation bank per family; reject all on collision."""
    V=m['volume'];du,dv,dw=[hi-lo for lo,hi in m['bounds']];B=du*dv*dw
    if f in ('affine','linear_yz','shear','linear_xz'):
        if f=='affine':wrong=[('omit_J',B),('use_forward_J',B/ m['J']),('omit_u_width',V/du),('omit_v_width',V/dv)]
        else:wrong=[('omit_u_width',V/du),('omit_v_width',V/dv),('omit_w_width',V/dw),('use_upper_u_instead_of_difference',V*p['hu']/du)]
    elif f=='log':wrong=[('omit_J',B),('use_forward_J',abs(p['b'])*dv*dw*(p['hu']**2-p['lu']**2)/2),('omit_v_width',V/dv),('omit_lower_log_endpoint',dv*dw*s.log(p['hu'])/abs(p['b']))]
    elif f=='sqrt':wrong=[('omit_J',B),('omit_chain_factor_two',V/2),('use_z_instead_of_dz_dw',du*dv*(p['hw']**3-p['lw']**3)/3),('omit_lower_squared_endpoint',du*dv*p['hw']**2)]
    elif f=='reciprocal':wrong=[('omit_J',B),('use_forward_J',du*dv*(p['hw']**3-p['lw']**3)/3),('keep_only_upper_reciprocal_magnitude',du*dv/p['hw']),('use_absolute_derivative_of_density',du*dv*(1/p['lw']**2-1/p['hw']**2))]
    else:wrong=[('omit_J',B),('omit_chain_factor_three',3*V),('omit_inverse_linear_determinant',abs(p['a']*p['d']-p['b']*p['c'])*V),('omit_u_width',V/du)]
    values=[V]+[s.simplify(e) for _,e in wrong]
    if any(e.is_positive is not True or e.has(s.nan,s.oo,s.zoo) for e in values):raise SampleRejected('Entire bank violates positive finite volume convention')
    if any(s.simplify(a-b)==0 for i,a in enumerate(values) for b in values[i+1:]):raise SampleRejected('Entire bank has mathematically equal choices')
    return ['correct']+[name for name,_ in wrong],values

def integral(bounds,density):return ''.join(r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}' for lo,hi in bounds)+density+r'\,\mathrm{d}w\,\mathrm{d}v\,\mathrm{d}u'
def matrix(M):return r'\begin{vmatrix}'+r' \\ '.join(' & '.join(tex(e) for e in M.row(i)) for i in range(M.rows))+r'\end{vmatrix}'

def normal_text(f,p,m):
    inequalities=r',\quad '.join(tex(lo)+r'\le '+tex(e)+r'\le '+tex(hi) for e,(lo,hi) in zip(m['trans'],m['bounds']))
    prompt='Find the volume bounded by the region $R,$ given by\n\n'+block(r'R=\big\{(x,y,z)\, :\, '+inequalities+r'\big\}.')
    # Common source prose and four-stage sequence. Every nine-partial entry and
    # cofactor is shown before its reduction; inverse map adds branch evidence.
    shared=RECORD[':knowledge-point/questions'][0][':question/worked-solution'].split('$$')
    solution='$$'.join(shared[:7]) # opening/formal T/change-of-variables formula
    solution+='$$\n'+inequalities+',\n$$'+shared[8]+'$$\n'+r',\quad '.join(str(t)+'='+tex(e) for t,e in zip(UVW,m['trans']))+'.\n$$'
    solution+=''.join(['\n\nThis change of variables gives us the *inverse* function ${T}^{-1},$ that is\n\n',block(r'T^{-1}:(x,y,z)\longmapsto(u(x,y,z),v(x,y,z),w(x,y,z)).')])
    solution+='\n\nTo compute the required volume, we proceed in four steps:\n\n**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$\n\nOur domain in the $uvw$-space is\n\n'+block(r'\Delta=\big\{(u,v,w):'+r',\quad '.join(tex(lo)+r'\le '+str(t)+r'\le '+tex(hi) for t,(lo,hi) in zip(UVW,m['bounds']))+r'\big\}.')
    solution+='\n\n**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$\n\nThe Jacobian determinant corresponding to ${T}^{-1}$ is\n\n'
    formal=r'\begin{vmatrix}'+r' \\ '.join(' & '.join(r'\frac{\partial '+str(a)+r'}{\partial '+str(b)+'}' for b in XYZ) for a in UVW)+r'\end{vmatrix}'
    M=m['matrix']; cofactor='+'.join(group(tex(M[0,j]))+r'(-1)^{1+'+str(j+1)+'}'+matrix(M.minor_submatrix(0,j)) for j in range(3))
    rows=[(r'\frac{\partial(u,v,w)}{\partial(x,y,z)}',formal),('',matrix(M)),('',cofactor),('',tex(m['det']))]
    if m['detuv']!=m['det']:rows.append(('',tex(m['detuv'])))
    solution+=aligned(rows)
    solution+='\n\n**Step 3**: Compute the Jacobian determinant corresponding to $T:$\n\nThe Jacobian determinant corresponding to $T$ is\n\n'+block(r'\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}='+tex(m['jac'])+'.')
    solution+='\n\nNote that $\\frac{∂(x,y,z)}{∂(u,v,w)}\\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$'
    solution+='\n\nThe map to $R$ is\n\n'+block(r'T(u,v,w)=\left('+','.join(tex(q) for q in m['inverse'])+r'\right).')
    solution+='\n\n**Step 4**: Perform the change of variables:\n\n'
    separated=tex(m['const'])+r'\cdot '+'\\cdot '.join(r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+(tex(m['J']) if m['J'].has(t) else '1')+r'\,\mathrm{d}'+str(t) for t,(lo,hi) in zip(UVW,m['bounds']))
    primitives=tex(m['const'])+r'\cdot '+r'\cdot '.join('['+tex(P)+']_{'+tex(lo)+'}^{'+tex(hi)+'}' for P,(lo,hi) in zip(m['primitive'],m['bounds']))
    substitutions=tex(m['const'])+r'\cdot '+r'\cdot '.join(group(tex(P).replace(str(t),group(tex(hi))))+'-'+group(tex(P).replace(str(t),group(tex(lo)))) for t,P,(lo,hi) in zip(UVW,m['primitive'],m['bounds']))
    # Parenthesize each difference so products retain the source operation.
    substitutions=tex(m['const'])+r'\cdot '+r'\cdot '.join(group(group(tex(P).replace(str(t),group(tex(hi))))+'-'+group(tex(P).replace(str(t),group(tex(lo))))) for t,P,(lo,hi) in zip(UVW,m['primitive'],m['bounds']))
    evaluated=tex(m['const'])+r'\cdot '+r'\cdot '.join(group(group(tex(hi))+'-'+group(tex(lo))) for hi,lo in m['endpoints'])
    solution+=aligned([(r'\iiint_R\mathrm{d}V',r'\iiint_\Delta 1\cdot |'+tex(m['jac'])+r'|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w'),('',integral(m['bounds'],tex(m['J']))),('',separated),('',primitives),('',substitutions),('',evaluated),('',tex(m['volume']))])
    return prompt,solution

# Raw replay masks are extracted complete mathematical components, never short
# number replacements in prose. Original h=1 requires no payload-return branch.
def raw_text(recipe,h):
    def render(mask):
        for key,expr in recipe['slots'].items():
            e=s.sympify(expr,locals={'h':h});value=tex(e)
            if key=='final' and recipe['family']=='log':value=str(7*h)+r'\operatorname{ln}⁡2'
            mask=mask.replace('@@'+key+'@@',value)
        return mask
    return render(recipe['prompt_mask']),render(recipe.get('solution_mask',''))

def assemble(level,seed,f,p,profile,prompt,solution,values,recipes,raw_source=None):
    normal=raw_source is None
    m=model(f,p)
    canonical_region=[]
    for expression,(lo,hi) in zip(m['trans'],m['bounds']):
        content,primitive=s.primitive(expression)
        # Exact same inequality under a positive common factor is one region.
        # Sign reversal also reverses the endpoint order.
        leading=primitive.as_ordered_terms()[0].as_coeff_Mul()[0]
        factor=content*(-1 if leading<0 else 1)
        normalized=s.expand(expression/factor)
        low,high=(lo/factor,hi/factor) if factor>0 else (hi/factor,lo/factor)
        canonical_region.append([s.srepr(normalized),s.srepr(low),s.srepr(high)])
    mathematical=stable({'region':sorted(canonical_region),'criterion':'volume_from_region'})
    if normal:prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    signature={'version':VERSION,'level':level if normal else raw_source.get(':question/difficulty'),'prompt':prompt,'solution':solution if normal or ':question/worked-solution' in raw_source else None,'banks':[[str(e) for e in values]],'shape':'radio'}
    fingerprint=stable(signature);q={':question/id':uid(fingerprint),':question/problem':prompt}
    if normal:q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=solution
    else:
        if ':question/difficulty' in raw_source:q[':question/difficulty']=enum(raw_source[':question/difficulty'])
        if ':question/worked-solution' in raw_source:q[':question/worked-solution']=solution
    fields=[]
    original_fields=raw_source[':question/answer-fields'] if raw_source else [None]
    for n,source_field in enumerate(original_fields):
        fieldid=uid(fingerprint+':field:'+str(n));choices=[]
        # Original scalar notation is regenerated from mathematical components;
        # evidence-only presentation follows the source command spelling.
        for i,value in enumerate(values):
            text=tex(value)
            if raw_source:
                sourcevalue=source_field[':answer-field/choices'][i][':answer/value'];base=s.sympify(RAW[str(raw_source[':db/id'])]['bank_expressions'][n][i]);h=values[i]/base
                if base.has(s.log(2)):text=str(s.simplify(base/s.log(2)*h))+r'\operatorname{ln}⁡2'
                if '\\\\' in sourcevalue:text=text.replace('\\','\\\\')
            choices.append({':answer/id':uid(fieldid+':'+str(value)),':answer/type':':answer.type/math',':answer/value':text})
        field={':answer-field/id':fieldid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if normal:field[':answer-field/correct']=[':answer/id',choices[0][':answer/id']]
        elif ':answer-field/correct' in source_field:
            correct=source_field[':answer-field/correct'][':answer/id'];index=next(i for i,a in enumerate(source_field[':answer-field/choices']) if a[':answer/id']==correct)
            field[':answer-field/correct']=[':answer/id',choices[index][':answer/id']]
        random.Random(seed+n).shuffle(choices);fields.append(field)
    q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':f,'profile':profile,'parameters':{k:str(v) for k,v in p.items()},'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':raw_source.get(':db/id') if raw_source else None,'authored':normal,'evidence_only':not normal,'eligible_for_learning':normal,'math_fingerprint':mathematical,'content_fingerprint':fingerprint,'recipes':recipes,'python':sys.version.split()[0],'sympy':s.__version__,'domain':'Bijective branch; positive nonlinear coordinates; no critical points inside box','plots':[]}}

def finalize_identity(record):
    """Actual prompt, fixed solution, attribute presence and complete displayed
    banks determine identity. Seed/profile/unused coefficient aliases do not."""
    if not record['generation'].get('evidence_only'):record['question']=normalize_question(record['question'])
    q=record['question'];field_signatures=[];correct_values=[]
    for f in q[':question/answer-fields']:
        correct=next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1]),None)
        correct_values.append(correct)
        field_signatures.append({'key':f[':answer-field/key'],'type':f[':answer-field/type'],'choices':sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices']),'correct':correct,'has_correct':':answer-field/correct' in f})
    signature={'version':VERSION,'question':{k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')},'fields':field_signatures}
    fingerprint=stable(signature);q[':question/id']=uid(fingerprint)
    for i,(f,correct) in enumerate(zip(q[':question/answer-fields'],correct_values)):
        fid=uid(fingerprint+':field:'+str(i));f[':answer-field/id']=fid
        for a in f[':answer-field/choices']:a[':answer/id']=uid(fid+':'+a[':answer/type']+':'+a[':answer/value'])
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==correct)]
    record['generation']['content_fingerprint']=fingerprint
    return record

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in FAMILIES:raise ValueError('Unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio shape supported')
    if profile and profile.startswith('raw_'):
        sid=int(profile[4:]);r=RAW[str(sid)];f=r['family']
        if template not in (None,f):raise ValueError('Raw template mismatch')
        hp=parameters or {'h':'1'}
        if set(hp)!={'h'}:raise ValueError('Raw parameters require exactly h')
        h=s.sympify(hp['h'])
        if h.is_Integer is not True or not 1<=h<=4:raise ValueError('Raw region stretch h=1..4')
        p={k:s.sympify(v) for k,v in r['parameters'].items()};p.update(lv=p['lv']*h,hv=p['hv']*h)
        sourceq=next(q for q in RECORD[':knowledge-point/questions'] if q[':db/id']==sid)
        prompt,solution=raw_text(r,h);values=[s.sympify(e)*h for e in r['bank_expressions'][0]]
        # Duplicate source fields have the same scalar set in different order.
        record=assemble(level,seed,f,p,profile,prompt,solution,values,['opaque_homogeneous_region_stretch'],sourceq)
        if len(sourceq[':question/answer-fields'])>1:
            # Rebuild each field using its original order, prior to shuffling.
            for n,field in enumerate(record['question'][':question/answer-fields']):
                original=sourceq[':question/answer-fields'][n];own={}
                for i,e in enumerate(r['bank_expressions'][n]):own[original[':answer-field/choices'][i][':answer/id']]=s.sympify(e)*h
                fid=field[':answer-field/id'];choices=[{':answer/id':uid(fid+':'+str(e)),':answer/type':':answer.type/math',':answer/value':tex(e).replace('\\','\\\\') if '\\\\' in a[':answer/value'] else tex(e)} for a,e in [(a,own[a[':answer/id']]) for a in original[':answer-field/choices']]]
                if ':answer-field/correct' in original:field[':answer-field/correct']=[':answer/id',uid(fid+':'+str(own[original[':answer-field/correct'][':answer/id']]))]
                random.Random(seed+n).shuffle(choices);field[':answer-field/choices']=choices
        record['generation']['parameters']={'h':str(h)};record['generation']['resolved_model_parameters']={k:str(v) for k,v in p.items()};return finalize_identity(record)
    f=template or random.Random(seed).choice(FAMILIES[level])
    if f not in FAMILIES[level]:raise ValueError('Unsupported level/template')
    if profile not in (None,'method_'+f):raise ValueError('Unsupported bank profile')
    r=random.Random(seed)
    for attempt in range(1000):
        p={k:s.sympify(v) for k,v in parameters.items()} if parameters is not None else sample(level,f,r)
        try:
            guard(level,f,p);m=model(f,p);recipes,values=bank(f,p,m)
        except ValueError:
            if parameters is not None:raise
            continue
        prompt,solution=normal_text(f,p,m)
        return finalize_identity(assemble(level,seed,f,p,'method_'+f,prompt,solution,values,recipes))
    raise RuntimeError('No eligible complete bank')

# EASY: authored affine map, no nonlinear Jacobian primitive.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: three observed constant-determinant map families.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: three observed variable-determinant families and canonical cube family.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];parts=['## '+('Original evidence replay' if r['generation']['evidence_only'] else 'Generated variant')+' / '+q.get(':question/difficulty','unrated').split('/')[-1]+' / '+r['generation']['template'],q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):parts.extend(' - $'+a[':answer/value']+'$'+(' **CORRECT**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])
    if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
    return '\n\n'.join(parts)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=tuple(FAMILIES)+('all',),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=tuple(FAMILIES) if args.difficulty=='all' else (args.difficulty,)
    records=[generate(level,args.seed+n,template=args.template,profile=args.profile) for level in levels for n in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
