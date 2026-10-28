#!/usr/bin/env python3
"""Concrete Cartesian flux setup. Scratch only, steps 3–7, no EDB writes.
12 observed easy field families; moderate/hard are explicit authored extensions.
Observed expression banks are evidence profiles with unresolved error intent;
normal banks use four complete cross/dot operations, never random perturbations.
See adjacent extraction, source anomalies, scope bounds and independent validator.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186198389
KP_UUID='a3486150-b3c2-5faf-99d5-b42ced350996'
VERSION='cartesian-flux-setup-1-format-audit-9837-v1'
ROOT=Path(__file__).with_suffix('')
RAW=json.loads((ROOT/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
x,y,z,u,v=sp.symbols('x y z u v',real=True)
LOC={str(i):i for i in (x,y,z,u,v)}
def parse(t):
 t=t.strip(',').replace('\\,','').replace('\\left','').replace('\\right','').replace('{','').replace('}','').replace('^','**').replace('−','-')
 return parse_expr(t,local_dict=LOC,transformations=standard_transformations+(implicit_multiplication_application,))
def tex(e): return sp.latex(e).replace('u v','uv').replace('x y','xy')
def vec(es): return '⟨'+r',\,'.join(tex(e) for e in es)+'⟩'
def digest(obj): return hashlib.sha256(json.dumps(_ca_material(obj),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def eq(a,b): return sp.expand(a-b)==0

def source_parameters(q):
 p=q[':question/problem']; F=[parse(i) for i in re.search('F\\(x,y,z\\)=⟨(.*?)⟩',p).group(1).split(r'\,')]
 g=parse(re.search(r'defined by \$z=(.*?)\$',p).group(1))
 bounds=[int(i) for i in re.search(r'for \$(-?\d+)\\le x\\le (-?\d+)\$ and \$(-?\d+)\\le y\\le (-?\d+)\.\$',p).groups()]
 return {'a':int(g.coeff(x)),'b':int(g.coeff(y)),'s':1,'bounds':bounds},F
FAMILIES={k:source_parameters(q) for k,q in SOURCES.items()}
TEMPLATES={k:{'level':'easy','origin':'observed','source':k} for k in SOURCES}
TEMPLATES.update({'quadratic_graph':{'level':'moderate','origin':'authored'},'mixed_graph':{'level':'hard','origin':'authored'}})
PROFILES={k:{'origin':'observed expression pattern; intent unresolved','template':k} for k in SOURCES}
PROFILES['q-161360-legacy']={'origin':'observed duplicate legacy field, missing designation','template':'q-161360'}
PROFILES['authored_operations']={'origin':'authored','template':None}
# These are structural patterns, not empirical correct-answer ratios. The scale
# is the multiplier of every printed field component. Restricted to the source
# plane slopes, they define covariant evidence banks. They are never defaults.
# Every pattern is explicit in extraction, including implausible legacy degree
# changes. Correct is independently computed, not selected by this mapping.
PATTERNS={
'q-160887':[u*v+v,u*v-v,u**2+u*v+v**2,2*u**2*v-u*v+v**2,u+v],
'q-161360':[u**2+v**2,u**2+u*v+v**2,2*u*v,u**2-v**2,2*(u+v)**2],
'q-161358':[-7*u+4*v,4*u+7*v,7*u+8*v,8*u-7*v,-7*u-8*v],
'q-161441':[-2*u+7*v,4*u+v,4*v-u,-2*u+v,2*u+4*v],
'q-161462':[3*u-3*v,2*u+v,u+2*v,2*u-3*v,3*v+u],
'q-161381':[7*u*v-4*v,11*u-24*v,11*u+4*v,u-v,24*u*v],
'q-161467':[8*u,u-2*v,8*u-2*v,-4*v,2*u+4*v],
'q-161357':[-2*u+v,3*u*v,11*u*v,u+v,5*u-6*v],
'q-161359':[u**2-u*v+v**2,u**2-v**2,(u+v)**2,(u-v)**2,u**2+u*v-v**2],
'q-161377':[u**2,4*u*v,u**3,2*u*v,3*v],
'q-161379':[-u*v,5*u*v,3*u*v**2,u*v+v,u*v-v],
'q-161471':[8*u-23*v,12*u-v,8*u+14*v,5*u-17*v,u-6*v]}

def checked_parameters(level,template,p,profile):
 required={'a','b','s','bounds'} if level=='easy' else ({'a','b','px','py','qx','qy','rz','r0','bounds'} if level=='moderate' else {'a','b','c','p','q','r','bounds'})
 if set(p)!=required: raise ValueError('Parameter keys must be exactly '+str(sorted(required)))
 if any(type(p[k])!=int for k in required-{'bounds'}): raise ValueError('Integral coefficients required')
 B=p['bounds']
 if not isinstance(B,list) or len(B)!=4 or any(type(i)!=int or not -3<=i<=5 for i in B) or not(B[0]<B[1] and B[2]<B[3]): raise ValueError('Rectangle bounds must be ordered integers in -3..5')
 if level=='easy':
  if not(1<=abs(p['a'])<=4 and 1<=abs(p['b'])<=4 and 1<=abs(p['s'])<=3): raise ValueError('Easy coefficient bounds')
  if profile!='authored_operations' and (p['a'],p['b'])!=(FAMILIES[template][0]['a'],FAMILIES[template][0]['b']): raise ValueError('Observed patterns require original slopes')
 elif level=='moderate':
  if not(1<=abs(p['a'])<=2 and 1<=abs(p['b'])<=2 and 1<=p['px']<=3 and 1<=p['qy']<=3 and 1<=abs(p['rz'])<=2 and all(1<=abs(p[k])<=2 for k in ('py','qx','r0'))): raise ValueError('Moderate coefficient bounds')
 else:
  if not(1<=abs(p['a'])<=2 and all(abs(p[k])==1 for k in ('b','c')) and all(1<=p[k]<=2 for k in ('p','q','r'))): raise ValueError('Hard coefficient bounds')
 return p

def mathematical(level,template,p):
 if level=='easy':
  g=p['a']*x+p['b']*y; F=[p['s']*e for e in FAMILIES[template][1]]
 elif level=='moderate':
  g=p['a']*x**2+p['b']*y**2; F=[p['px']*x+p['py']*y,p['qx']*x+p['qy']*y,p['rz']*z+p['r0']]
 else:
  g=p['a']*x*y+p['b']*x+p['c']*y; F=[p['p']*z,p['q']*x*y,p['r']*(x+y)]
 G=g.subs({x:u,y:v}); R=sp.Matrix([u,v,G]); ru=R.diff(u);rv=R.diff(v);normal=ru.cross(rv)
 fv=[sp.expand(e.subs({x:u,y:v,z:G},simultaneous=True)) for e in F]
 terms=[sp.expand(e*n) for e,n in zip(fv,normal)]; I=sp.expand(sum(terms))
 return dict(g=g,F=F,G=G,r=R,ru=ru,rv=rv,normal=normal,fv=fv,terms=terms,I=I)

def candidate_operations(m):
 """Finite plausible operation sequences; matches are hypotheses, not intent."""
 A,B,C=m['terms'];P,Q,R=m['fv'];I=m['I'];out={'correct_cross_dot':I}
 # Use all three normal-component sign/omission combinations, retaining
 # component order. Coefficient zero means omit that dot contribution.
 import itertools
 for weights in itertools.product((-1,0,1),repeat=3):
  if weights==(1,1,1):continue
  out['dot_component_weights_'+','.join(map(str,weights))]=sum(w*t for w,t in zip(weights,(A,B,C)))
 for idx,component in enumerate((P,Q,R)):
  out['omit_normal_use_field_component_'+str(idx)]=component
  out['double_field_component_'+str(idx)+'_omit_others']=2*component
 out['omit_normal_sum_field_components']=P+Q+R
 out['omit_normal_first_minus_second']=P-Q
 # Errors in the collected dot polynomial or an individual distributed term.
 for coordinate in (u,v):out['multiply_dot_by_'+str(coordinate)]=I*coordinate
 for idx,term in enumerate((A,B,C)):
  for monomial in sp.Add.make_args(sp.expand(term)):
   key=sp.sstr(monomial.as_coeff_Mul()[1])
   out['omit_distributed_term_'+str(idx)+':'+key]=I-monomial
   out['reverse_distributed_term_'+str(idx)+':'+key]=I-2*monomial
 # False coordinate substitutions are applied to the actual printed F before
 # dotting, rather than changing unrelated final coefficients.
 for replacement in (sp.Integer(0),u,v):
  changed=[e.subs({x:u,y:v,z:replacement},simultaneous=True) for e in m['F']]
  out['replace_graph_coordinate_z_by_'+str(replacement)]=sum(e*n for e,n in zip(changed,m['normal']))
 # Missing/incorrect mixed terms in an isolated squared graph component, then
 # omitted first/second normal contributions. Degree/power remains explicit.
 if sp.Poly(m['G'],u,v).total_degree()==1:
  gu,gv=sp.diff(m['G'],u),sp.diff(m['G'],v)
  for idx,comp in enumerate(m['F']):
   coeff=sp.expand(comp).coeff(z,2)
   if coeff:
    remainder=comp-coeff*z**2
    for crossfactor in (0,1,-2):
     changed=sp.expand(remainder.subs({x:u,y:v,z:m['G']},simultaneous=True)+coeff*(gu**2*u**2+crossfactor*gu*gv*u*v+gv**2*v**2))
     out['graph_square_cross_factor_'+str(crossfactor)+'_use_component_'+str(idx)+'_omit_others']=changed
 return {k:sp.expand(e) for k,e in out.items()}

# Map source choices once to every supported operation match. Where multiple
# operations coincide, list all candidates and choose a deterministic first one;
# this does not claim a unique recovered learner-error mechanism.
OBSERVED_MAP={}
for _template,(_p,_F) in FAMILIES.items():
 _m=mathematical('easy',_template,_p);_ops=candidate_operations(_m)
 OBSERVED_MAP[_template]=[]
 for _pattern in PATTERNS[_template]:
  _matches=[name for name,e in _ops.items() if eq(e,_pattern)]
  OBSERVED_MAP[_template].append({'candidates':_matches,'selected':_matches[0] if _matches else None})

def bank(m,p,template,profile):
 if profile!='authored_operations':
  ops=candidate_operations(m)
  recipes=[r['selected'] or 'residual_observed_polynomial_pattern_'+str(i) for i,r in enumerate(OBSERVED_MAP[template])]
  values=[ops[r['selected']] if r['selected'] else sp.expand(p['s']*e) for e,r in zip(PATTERNS[template],OBSERVED_MAP[template])]
 else:
  A,B,C=m['terms'];values=[m['I'],-m['I'],-A+B+C,A-B+C,A+B]
  recipes=['correct_cross_dot','reverse_cross_order','reverse_first_normal_component','reverse_second_normal_component','omit_third_dot_term']
 if len(values)!=5 or any(eq(values[i],values[j]) for i in range(5) for j in range(i)): raise ValueError('Reject whole bank: equivalent choices')
 if sum(eq(e,m['I']) for e in values)!=1: raise ValueError('Reject whole bank: missing or ambiguous correct answer')
 return values,recipes

def display(e): return '$$\n'+e+'\n$$'
def aligned(rows): return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def integral(p,I):
 a,b,c,d=p['bounds'];return rf'{{\int }}_{{{a}}}^{{{b}}}{{\int }}_{{{c}}}^{{{d}}}'+I+r'\,\text{d}v\,\text{d}u'
def render(level,template,p,m):
 # Fixed source prose is extracted outside complete display components. All
 # source math blocks are rebuilt, with source row omissions retained per family.
 source=SOURCES.get(template,SOURCES['q-161360'])
 bits=source[':question/worked-solution'].split('$$')
 assert len(bits)==17
 a,b,c,d=p['bounds']; F,G=m['F'],m['G'];fv=m['fv'];normal=m['normal'];I=m['I']
 prompt=(rf'Consider the vector field $F(x,y,z)={vec(F)}$ and the surface $S$ defined by $z={tex(m["g"])}$ for ${a}\le x\le {b}$ and ${c}\le y\le {d}.$ Using the parametrization $x=u$ and $y=v,$ the flux of $F$ through $S$ can be expressed as'+ '\n\n'+display(r'{∬}_{S}F\cdot \text{d}S='+integral(p,r'\boxed{}')+'.')+'\n\nWhat is the missing expression?')
 gu,gv=sp.diff(G,u),sp.diff(G,v)
 deriv=[]
 for sym,final in ((u,m['ru']),(v,m['rv'])):
  deriv.extend([rf'{{r}}_{{{sym}}}^{{′}} & =⟨\frac{{∂x}}{{∂{sym}}},\,\frac{{∂y}}{{∂{sym}}},\,\frac{{∂z}}{{∂{sym}}}⟩',rf' & =⟨\frac{{∂}}{{∂{sym}}}(u),\,\frac{{∂}}{{∂{sym}}}(v),\,\frac{{∂}}{{∂{sym}}}({tex(G)})⟩',' & ='+vec(final)])
 determinant=rf'|\begin{{aligned}}i & j & k \\ 1 & 0 & {tex(gu)} \\ 0 & 1 & {tex(gv)}\end{{aligned}}|'
 minors=rf'⟨|\begin{{aligned}}0 & {tex(gu)} \\ 1 & {tex(gv)}\end{{aligned}}|,\,-|\begin{{aligned}}1 & {tex(gu)} \\ 0 & {tex(gv)}\end{{aligned}}|,\,|\begin{{aligned}}1 & 0 \\ 0 & 1\end{{aligned}}|⟩'
 # Preserve the observed symbolic substitution row before simplification.
 raw_sub=[]
 for e in F:
  t=tex(e.subs({x:u,y:v},simultaneous=True));t=re.sub(r'(?<![A-Za-z])z(?![A-Za-z])','('+tex(G)+')',t);raw_sub.append(t)
 raw_vec='⟨'+r',\,'.join(raw_sub)+'⟩'
 subrows=[rf'F(r(u,v)) & ={vec(F)}{{|}}_{{x=u,\,\,y=v,\,\,z={tex(G)}}}',' & ='+raw_vec]
 original_sub=bits[11]
 if original_sub.count(' & =')==3 or level!='easy': subrows.append(' & ='+vec(fv))
 # If source has no extra simplification row, keep its substituted form for
 # the subsequent dot product, exactly as the original sequence does.
 fvtex=vec(fv) if len(subrows)==3 else raw_vec
 product='+'.join('('+t+')'+r'\cdot ('+tex(n)+')' for t,n in zip([tex(e) for e in fv] if len(subrows)==3 else raw_sub,normal))
 # Distributed sum is computed term by term, never by final-answer copying.
 distributed=''.join(('+' if j and not tex(t).startswith('-') else '')+tex(t) for j,t in enumerate(m['terms']))
 if template=='q-161377':
  # This source distributes outer scalar factors but leaves the z-square
  # cancellations visibly intact. Preserve that stage rather than adding a
  # premature square-expansion step to claim row-count fidelity.
  substituted=[e.subs({x:u,y:v,z:G},simultaneous=True) for e in F]
  partial_terms=[sp.expand(e*n,multinomial=False) for e,n in zip(substituted,normal)]
  distributed=''.join(('+' if j and not tex(t).startswith('-') else '')+tex(t) for j,t in enumerate(partial_terms))
 dotrows=[r'F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′}) & ='+fvtex+r'\cdot '+vec(normal),' & ='+product]
 if bits[13].count(' & =')==4 or level!='easy': dotrows.append(' & ='+distributed)
 dotrows.append(' & ='+tex(I)+'.')
 blocks=[r'{∬}_{S}F\cdot \text{d}S={∬}_{S}F\cdot n\,\text{d}S={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.', 'r(u,v)='+vec(m['r']), rf'D=\{{(u,v)\,:\,{a}\le u\le {b},\,{c}\le v\le {d}\}}.',aligned(deriv),aligned([r'{r}_{u}^{′}\times {r}_{v}^{′} & ='+determinant,' & ='+minors,' & ='+vec(normal)+'.']),aligned(subrows),aligned(dotrows),aligned([r'{∬}_{S}'+vec(F)+r'\cdot \text{d}S & ={∬}_{D}F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})\,\text{d}A.',r' & ={∬}_{D}('+tex(I)+r')\,\text{d}A', ' & ='+integral(p,'('+tex(I)+')')+'.'])]
 for j,t in enumerate(blocks): bits[2*j+1]='\n'+t+'\n'
 return prompt,'$$'.join(bits)

def sample(level,rng,template,profile):
 bounds=[rng.randint(-3,1),rng.randint(2,5),rng.randint(-3,1),rng.randint(2,5)]
 if level=='easy':
  p=dict(FAMILIES[template][0]);p['bounds']=bounds
  if profile=='authored_operations': p.update(a=rng.choice([-4,-3,-2,-1,1,2,3,4]),b=rng.choice([-4,-3,-2,-1,1,2,3,4]),s=rng.choice([-3,-2,-1,1,2,3]))
  else: p['s']=rng.choice([1,2,3])
 elif level=='moderate': p={'a':rng.choice([-2,-1,1,2]),'b':rng.choice([-2,-1,1,2]),'px':rng.randint(1,3),'py':rng.choice([-2,-1,1,2]),'qx':rng.choice([-2,-1,1,2]),'qy':rng.randint(1,3),'rz':rng.choice([-2,-1,1,2]),'r0':rng.choice([-2,-1,1,2]),'bounds':bounds}
 else: p={'a':rng.choice([-2,-1,1,2]),'b':rng.choice([-1,1]),'c':rng.choice([-1,1]),'p':rng.randint(1,2),'q':rng.randint(1,2),'r':rng.randint(1,2),'bounds':bounds}
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Observed response is radio')
 rng=random.Random(seed)
 if template is None and profile not in (None,'authored_operations'): template=PROFILES.get(profile,{}).get('template')
 template=template or rng.choice([k for k,d in TEMPLATES.items() if d['level']==level])
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level: raise ValueError('Template does not belong to difficulty')
 profile=profile or 'authored_operations'
 if profile not in PROFILES or (PROFILES[profile]['template'] not in (None,template)): raise ValueError('Ineligible bank profile')
 for attempt in range(500):
  p=checked_parameters(level,template,dict(parameters) if parameters is not None else sample(level,rng,template,profile),profile)
  m=mathematical(level,template,p)
  try: values,recipes=bank(m,p,template,profile)
  except ValueError:
   if parameters is not None: raise
   continue
  break
 else: raise ValueError('No eligible complete bank')
 prompt,solution=render(level,template,p,m)
 prompt=_ca_problem(prompt);solution=_ca_prose(solution)
 # Presentation hash excludes seed and order; mathematical fingerprint excludes
 # template spelling, profile and scale parameter spelling.
 mathfingerprint=digest({'F':[sp.srepr(sp.expand(e)) for e in m['F']],'g':sp.srepr(sp.expand(m['g'])),'orientation':'upward'})
 key=digest({'version':VERSION,'problem':prompt,'solution':solution,'bank':sorted(tex(e) for e in values),'difficulty':level})
 qid=uid('question:'+key); fid=uid(qid+':selection')
 answers=[{':answer/id':uid(fid+':'+sp.srepr(e)),':answer/type':':answer.type/math',':answer/value':tex(e)} for e in values]
 correct=next(a[':answer/id'] for a,e in zip(answers,values) if eq(e,m['I']))
 rng.shuffle(answers)
 q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':RAW['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'mathematical_fingerprint':mathfingerprint,'presentation_fingerprint':key,'provenance':{k:RAW[k] for k in ('database','basis','lineage')},'origin':TEMPLATES[template]['origin'],'bank_origin':PROFILES[profile]['origin'],'recipes':recipes,'orientation':'ru cross rv, upward','dependencies':{'sympy':sp.__version__},'plots':[]}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q=record['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('--count must be positive')
 records=[generate(level,args.seed+j,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for j in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(q) for q in records))
if __name__=='__main__':main()
