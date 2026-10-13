#!/usr/bin/env python3
"""Line-segment one-form integration, local review only (math basis 1356).

Nine observed stage templates are extracted as component masks from source.json;
all source banks have explicit, interpretation-unresolved scalar-multiplier replay
profiles. These profiles vary a nonzero multiplier of the ENTIRE one-form, and
never claim to recover distractor intent. Normal banks use complete operation
recipes. Authored endpoint/coefficient variations and missing-level designs are
separate templates; see classification.md and template-extraction.md.

All answers use exact SymPy arithmetic. Mathematical stages are rendered from
ordered component masks before collection. Content UUIDs depend on actual
prompt, solution and complete bank; mathematical task fingerprints exclude banks,
level, template/profile aliases and incidental endpoint labels. No EDB writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186179728
KP_UUID='223ec615-045d-543e-96f4-fec8882bec9e'
TITLE='Evaluating Line Integrals With Respect to X and Y Over Segments'
VERSION='segment-oneforms-v1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y,t=s.symbols('x y t',real=True)
# Source-specific objects, not answer tables. Every replay answer is an operation
# on the actual parameterized one-form; unknown wrong intent is marked honestly.
OBS={
'q-124654':((-1,0,2,4),y,-x),
'q-81096':((0,1,3,3),x**2,-y),
'q-124652':((-1,2,1,0),x*y,s.Integer(1)),
'q-124658':((0,0,4,2),s.exp(x+y),-s.exp(x+y)),
'q-124663':((-1,1,1,3),y**2,x**2),
'q-39345':((1,2,3,4),x,y),
'q-81102':((0,1,2,3),s.exp(x),-s.pi*s.sin(s.pi*y/2)),
'q-124660':((0,0,1,1),s.sin(s.pi*y),-s.cos(s.pi*x)),
'q-90714':((1,0,2,3),x,-x*y),
}
TEMPLATES={qid:{'level':'easy','origin':'observed','source':qid} for qid in OBS}
TEMPLATES.update({
'easy_linear':{'level':'easy','origin':'authored','source':'q-39345'},
'easy_product':{'level':'easy','origin':'authored','source':'q-90714'},
'moderate_canonical':{'level':'moderate','origin':'authored','source':'e-9515'},
'hard_coupled':{'level':'hard','origin':'authored','source':'e-9515'},
})
BANK_PROFILES={qid+'_observed':{'template':qid,'origin':'observed-scalar-pattern','interpretation':'unresolved: uniform complete-one-form multiplier'} for qid in OBS}
BANK_PROFILES.update({'method':{'origin':'authored','recipes':['correct','omit_dy','omit_dx','reverse_dy','reverse_traversal']}})

def tex(v):
    return s.latex(v).replace(r'\log',r'\ln')

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'CourseAcademy/'+str(KP_ID)+'/'+v))
def par(v):return r'\left('+v+r'\right)'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\  '.join(rows)+r'\end{aligned}'+'\n$$'
def integral(v):return r'{\int }_{0}^{1}'+v+r'\,dt'
def vector(a,b):
    if a==0 and b==0:return r'0\,i+0\,j'
    out=''
    for n,name in ((a,'i'),(b,'j')):
        if n==0:continue
        part=('-' if n<0 else '+' if out else '')+(str(abs(n))+r'\,' if abs(n)!=1 else '')+name
        out+=part
    return out

def source_components(qid):
    """Extract fixed prose, endpoint/derivative block, and ordered integral rows.

    This is a reusable source component mask, not a literal-question replay
    branch. Rendering always applies k to every complete assessed expression.
    q-124663 receives its documented endpoint-stage mathematical repair.
    """
    q=QS[qid]
    prose,block=q[':question/worked-solution'].rsplit('$$',2)[0:2]
    if qid=='q-124663':block=block.replace(r'4[\frac{4}{3}+10]',r'4[\frac{4}{3}+1]')
    block=block.strip()
    body=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    rows=re.split(r'\\\\\s*&\s*=',body)
    left,right=rows[0].split('& =',1)
    return prose,left.strip(),[right.strip()]+[r.strip() for r in rows[1:]]

def scale_complete(v,k):
    return v if k==1 else tex(k)+par(v)

def observed(qid,p):
    coords,P,Q=OBS[qid];k=s.Integer(p['k'])
    # Complete component masks limit slots; no blind replacement of symbols.
    old=QS[qid][':question/problem']
    prefix,math=old.rsplit('$',2)[0:2]
    form=math.removesuffix('=')
    prompt=prefix+'$'+scale_complete(form,k)+'=$'
    prose,lhs,rows=source_components(qid)
    solution=prose+'$$\n'+r'\begin{aligned}'+scale_complete(lhs,k)+' & ='+scale_complete(rows[0],k)
    solution+=''.join(r' \\  & ='+scale_complete(row,k) for row in rows[1:])+r'\end{aligned}'+'\n$$'
    return prompt,solution,coords,k*P,k*Q

# ---------------------------------------------------------------------------
# EASY — endpoint-varied counterparts of observed simple polynomial one-forms.
# MODERATE — canonical x²y and xy on a shifted line segment.
# HARD — two coupled cubic products; identical segment method, no new branch.
# ---------------------------------------------------------------------------
def objects(name,p):
    a,b=p['a'],p['b']
    if name=='easy_linear':return a*x,b*y
    if name=='easy_product':return a*x,b*x*y
    if name=='moderate_canonical':return a*x**2*y,b*x*y
    if name=='hard_coupled':return a*x**2*y,b*x*y**2
    raise ValueError('Unknown template')

def oneform(P,Q):
    return par(tex(P))+r'\,dx+'+par(tex(Q))+r'\,dy'

def authored(name,p):
    coords=tuple(p[k] for k in ('x0','y0','x1','y1'));x0,y0,x1,y1=coords
    dx,dy=x1-x0,y1-y0;xt=x0+dx*t;yt=y0+dy*t
    P,Q=objects(name,p)
    prompt='If the path $C$ is the line segment $\\overline{AB}$ traversed from the point $A('+str(x0)+','+str(y0)+')$ to the point $B('+str(x1)+','+str(y1)+'),$ then $'+r'{\int }_C '+oneform(P,Q)+'=$'
    va,vb,vd=vector(x0,y0),vector(x1,y1),vector(dx,dy)
    rt=par(tex(xt))+r'\,i+'+par(tex(yt))+r'\,j'
    sol='The position vectors of the endpoints of our line segment are $a='+va+'$ and $b='+vb+'.$ So, the parametrization of the line segment is given by\n\n'
    sol+=aligned([r'r(t) & =a+t\,(b-a)',r' & ='+va+'+t'+par(vb+'-'+par(va)),r' & ='+va+'+t'+par(vd),r' & ='+rt+','])
    sol+='\n\nwhere $0\\le t\\le 1.$ Thus, we have that $x(t)='+tex(xt)+'$ and $y(t)='+tex(yt)+'$ along the segment.\n\nThe derivative of $r(t)$ is given by\n\n'
    sol+=aligned([r"{r}^{\prime}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j="+vd+'.'])
    sol+='\n\nWe can now evaluate the line integral:\n\n'
    dxt=r'\frac{\text{d}x}{\text{d}t}';dyt=r'\frac{\text{d}y}{\text{d}t}'
    symbolic=par(tex(P))+dxt+'+'+par(tex(Q))+dyt
    # Symbolic substitution preserves all products/powers until distribution.
    def sub(v):
        if name=='easy_linear':return par(tex(p['a']))+r'\cdot '+par(tex(xt)),par(tex(p['b']))+r'\cdot '+par(tex(yt))
        if name=='easy_product':return par(tex(p['a']))+r'\cdot '+par(tex(xt)),par(tex(p['b']))+r'\cdot '+par(tex(xt))+r'\cdot '+par(tex(yt))
        if name=='moderate_canonical':return par(tex(p['a']))+r'\cdot '+par(tex(xt))+'^{2}'+r'\cdot '+par(tex(yt)),par(tex(p['b']))+r'\cdot '+par(tex(xt))+r'\cdot '+par(tex(yt))
        return par(tex(p['a']))+r'\cdot '+par(tex(xt))+'^{2}'+r'\cdot '+par(tex(yt)),par(tex(p['b']))+r'\cdot '+par(tex(xt))+r'\cdot '+par(tex(yt))+'^{2}'
    pt,qt=sub(P)
    substituted=pt+r'\cdot '+par(str(dx))+'+'+qt+r'\cdot '+par(str(dy))
    ps=P.subs({x:xt,y:yt},simultaneous=True);qs=Q.subs({x:xt,y:yt},simultaneous=True)
    distributed=par(tex(s.expand(ps*dx)))+'+'+par(tex(s.expand(qs*dy)))
    R=s.expand(ps*dx+qs*dy);F=s.integrate(R,t);C=s.simplify(F.subs(t,1)-F.subs(t,0))
    # Endpoint substitution is retained in the actual printed expression, using
    # a whole t component mask before evaluation (protecting LaTeX commands).
    def at(v,n):return re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])',lambda _:par(str(n)),tex(v))
    def endpoint_components(v,n):
        # Evaluate each primitive term independently, retaining an unevaluated
        # sum of signed components until the FINAL collection row.
        return '+'.join(par(tex(term.subs(t,n))) for term in v.as_ordered_terms())
    rows=[r'{\int }_C '+oneform(P,Q)+' & ='+integral(symbolic),
          r' & ='+integral(par(symbolic)),r' & ='+integral(substituted),
          r' & ='+integral(distributed),r' & ='+integral(tex(R)),
          r' & ='+r'\left['+tex(F)+r'\right]_0^1',
          r' & ='+par(at(F,1))+'-'+par(at(F,0)),
          r' & ='+par(endpoint_components(F,1))+'-'+par(endpoint_components(F,0)),r' & ='+tex(C)]
    sol+=aligned(rows)
    return prompt,sol,coords,P,Q

def checked_parameters(name,p):
    if name in OBS:
        if set(p)!= {'k'} or isinstance(p['k'],bool) or not isinstance(p['k'],int) or not 1<=abs(p['k'])<=9:raise ValueError('Observed multiplier is a nonzero integer of magnitude <=9')
        return dict(p)
    keys={'x0','y0','x1','y1','a','b'}
    if set(p)!=keys or any(isinstance(p[k],bool) or not isinstance(p[k],int) for k in keys):raise ValueError('Require integer endpoint coordinates and a,b only')
    level=TEMPLATES[name]['level'];cb=3 if level=='hard' else 4
    if any(abs(p[k])>cb for k in ('x0','y0','x1','y1')):raise ValueError('Endpoint workload bound exceeded')
    if any(not 1<=abs(p[k])<=3 for k in ('a','b')):raise ValueError('Require nonzero coefficient magnitude <=3')
    if not 1<=abs(p['x1']-p['x0'])<=4 or not 1<=abs(p['y1']-p['y0'])<=4:raise ValueError('Both nonzero coordinate differences have magnitude <=4')
    if level in ('moderate','hard') and (not p['x0'] or not p['y0']):raise ValueError('Coupled-product levels require two shifted coordinates')
    return dict(p)

def sample(name,rng):
    if name in OBS:return {'k':rng.choice([i for i in range(-9,10) if i])}
    bound=3 if TEMPLATES[name]['level']=='hard' else 4
    p={k:rng.randint(-bound,bound) for k in ('x0','y0','x1','y1')}
    p.update({k:rng.choice([-3,-2,-1,1,2,3]) for k in ('a','b')})
    return checked_parameters(name,p)

def exact(coords,P,Q):
    x0,y0,x1,y1=coords;dx=x1-x0;dy=y1-y0
    ps=P.subs({x:x0+dx*t,y:y0+dy*t},simultaneous=True);qs=Q.subs({x:x0+dx*t,y:y0+dy*t},simultaneous=True)
    A=s.integrate(ps*dx,(t,0,1));B=s.integrate(qs*dy,(t,0,1))
    return s.simplify(A),s.simplify(B),s.simplify(A+B)

def source_pattern(qid,k):
    # Every captured scalar is an explicit coefficient of the uniform one-form
    # multiplier, not a guessed original error recipe or general default bank.
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('_segment_tex',ROOT/'texmath.py');m=module_from_spec(spec);spec.loader.exec_module(m)
    return [s.simplify(k*m.parse_tex(a[':answer/value'])) for a in QS[qid][':question/answer-fields'][0][':answer-field/choices']]

def method_bank(name,p,coords,P,Q):
    A,B,C=exact(coords,P,Q)
    if name=='q-124658':
        # Here B=-C, so reverse traversal would duplicate omit_dx. Select a
        # different COMPLETE family bank before construction, not a replacement.
        k=p['k'];return [C,A,B,s.simplify(A-B),k*s.exp(6)/3],['correct','omit_dy','omit_dx','reverse_dy','omit_lower_endpoint']
    if name=='q-124660':
        k=p['k'];return [C,-C,s.Integer(2*k),2*k*s.pi,k/s.pi],['correct','reverse_traversal','omit_chain_pi','multiply_instead_of_divide_pi','omit_lower_endpoint']
    if name=='q-81102':
        k=p['k'];return [C,-C,k*s.exp(2),C/2,k*(s.E-1)],['correct','reverse_traversal','omit_lower_exponential_endpoint','omit_dx_multiplier','halve_exponential_argument']
    return [C,A,B,s.simplify(A-B),-C],BANK_PROFILES['method']['recipes']

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source-shaped radio fields supported')
    if profile not in (None,*BANK_PROFILES):raise ValueError('Unknown profile')
    if profile and profile!='method':
        implied=BANK_PROFILES[profile]['template']
        if template and template!=implied:raise ValueError('Profile/template mismatch')
        template=implied
    rng=random.Random(seed)
    if template is None:template=rng.choice([n for n,v in TEMPLATES.items() if v['level']==level and v['origin']=='authored'])
    if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('Template/difficulty mismatch')
    profile=profile or 'method'
    attempts=1 if parameters is not None else 1000
    for _ in range(attempts):
        try:
            p=checked_parameters(template,parameters) if parameters is not None else sample(template,rng)
            prompt,solution,coords,P,Q=observed(template,p) if template in OBS else authored(template,p)
            A,B,C=exact(coords,P,Q)
            if TEMPLATES[template]['level'] in ('moderate','hard'):
                xx=coords[0]+(coords[2]-coords[0])*t;yy=coords[1]+(coords[3]-coords[1])*t
                R=s.expand(P.subs({x:xx,y:yy},simultaneous=True)*(coords[2]-coords[0])+Q.subs({x:xx,y:yy},simultaneous=True)*(coords[3]-coords[1]))
                if s.degree(R,t)!=3:raise ValueError('Cubic workload cancels')
            if profile=='method':values,recipes=method_bank(template,p,coords,P,Q)
            else:values=source_pattern(template,p['k']);recipes=['unresolved_uniform_multiplier']*5
            if any(s.simplify(v-values[j])==0 for i,v in enumerate(values) for j in range(i)):raise ValueError('Entire bank rejected: equivalent scalar choices')
            if any(v.has(s.oo,s.zoo,s.nan) for v in values):raise ValueError('Nonfinite choice')
            if sum(s.simplify(v-C)==0 for v in values)!=1:raise ValueError('Missing/ambiguous correct value')
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('Unable to sample a valid complete bank')
    displays=[tex(v) for v in values]
    # For source coefficient k=1 use captured answer notation as each slot's
    # style; the value still comes from the parameterized scalar recipe.
    if profile!='method' and p['k']==1:displays=[a[':answer/value'] for a in QS[template][':question/answer-fields'][0][':answer-field/choices']]
    content=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(displays)})
    qid=uid(content);fid=uid(content+'/selection')
    choices=[{':answer/id':uid(content+'/selection/'+d),':answer/type':':answer.type/math',':answer/value':d} for d in displays]
    correct=next(a[':answer/id'] for a,v in zip(choices,values) if s.simplify(v-C)==0)
    rng.shuffle(choices)
    canonical={'A':list(coords[:2]),'B':list(coords[2:]),'P':s.srepr(s.expand(P)),'Q':s.srepr(s.expand(Q)),'limits':[0,1]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'recipes':recipes,'origin':TEMPLATES[template]['origin'],'source':TEMPLATES[template]['source'],'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'mathematical_fingerprint':digest(canonical),'content_sha256':content,'plot_rating':'none','repairs':['q-124663 endpoint +10 → +1'] if template=='q-124663' else []}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0];g=r['generation']
    out=['## '+g['template']+' — '+q[':question/difficulty'].split('/')[-1],f"Author preview: {g['origin']}; profile `{g['bank_profile']}`; parameters `{g['parameters']}`.",'',q[':question/problem'],'']
    for label,a in zip('ABCDE',f[':answer-field/choices']):out.append('- '+label+'. $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
    return '\n'.join(out+['','**Worked solution**','',q[':question/worked-solution']])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));ap.add_argument('--field-type',choices=['radio']);args=ap.parse_args()
    if args.count<1 or args.difficulty=='all' and (args.template or args.profile):ap.error('Positive count; template/profile require specific difficulty')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    out=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(out,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in out))
if __name__=='__main__':main()
