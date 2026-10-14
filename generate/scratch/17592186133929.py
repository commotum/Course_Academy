#!/usr/bin/env python3
"""Flux-to-triple-integral setup only. math basis 1356; no database writes.

Observed easy: supplied box bounds, recover integrand. Observed moderate:
recover integrand and inner curved bounds. Authored hard: same theorem/setup,
three nonzero held-coordinate terms and two variable inner surfaces. No integral
is evaluated in learner content. Whole five-option banks are chosen before
parameters. Raw profiles are evidence-only and preserve missing attributes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
BASE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((BASE/'source.json').read_text())
KP=SNAPSHOT['record']; KP_ID=17592186133929
VERSION='flux-setup-v1'
x,y,z=sp.symbols('x y z',real=True); VARS=(x,y,z)
SOURCE=KP[':knowledge-point/questions']
# Each family retains its source field layout and solution route. The raw banks
# below are symbolic expression shapes, not correct-answer or payload lookups.
CONFIG={
 'legacy':dict(index=0,level='easy',components=(x*z,y**2,sp.Integer(1)),outer=((x,1,3),(y,-1,1)),inner=(z,0,1),bank=(y**2+z,1,y**2+x,2*y+z,2*y+x)),
 'typeII':dict(index=1,level='moderate',components=(x*y**2,x*z,y),outer=((y,-1,1),(z,0,1)),inner=(x,y-2*z,4-y**2-z**2),bank=((z+3*y,-2,4),(y**2,4-y**2-z**2,y-2*z),(y**2,y-2*z,4-y**2-z**2),(2*y+1,y-2*z,4-y**2-z**2),(2*y+1,4-y**2-z**2,y-2*z))),
 'typeI':dict(index=2,level='moderate',components=(x+y,-2*y,x**2*z),outer=((x,0,2),(y,0,1)),inner=(z,y,x**2+y),bank=((2*x*z,y,x**2+y),(x**2-1,2*y,2*x**2+1),(y+z-2,2*y,2*x**2+1),(y+z-2,y,x**2+y),(x**2-1,y,x**2+y))),
 'typeIIIbowl':dict(index=3,level='moderate',components=(y**3-z,z,2*x*y*z),outer=((x,-1,1),(z,0,1)),inner=(y,x**2+z**2,2),bank=((x+y,0,2),(2*x*y,0,2),(3*y**2+x*y,x**2+z**2,2),(3*y**2+x*y,2,z**2+x**2),(2*x*y,x**2+z**2,2))),
 'box_product':dict(index=4,level='easy',components=(x*y,2*y,x**2*z),outer=((x,-1,0),(y,1,2)),inner=(z,0,1),bank=(2*x+y+1,x*y+2,x**2+2*y,x**2+x*y,x**2+y+2)),
 'box_collect':dict(index=5,level='easy',components=(x**2+y,-y*z,4*x*z),outer=((x,0,4),(y,-1,1)),inner=(z,0,2),bank=(2*x+3*z,2*x-z+4,6*x-z,6*x+4*z,2*x-y-2*z)),
 'typeIIIlinear':dict(index=6,level='moderate',components=(z,-4*y,z**3),outer=((x,0,1),(z,0,1)),inner=(y,x**2,x-z+2),bank=((3*z**2-4,x**2,x-z+2),(3*z**2-4,x**2,2),(z**3-3,x**2,2),(z**2,x**2,x-z+2),(z**3-3,x**2,x-z+2))),
 'box_zero':dict(index=7,level='easy',components=(x**2,x*y*z,2*y),outer=((x,-1,1),(y,0,2)),inner=(z,1,2),bank=(2*x+x*z,2+z,x+2*z,y+z,x+y*z)),
}
for orientation in ('z','x','y'):
 CONFIG['hard_'+orientation]=dict(level='hard',orientation=orientation)
TEMPLATES=CONFIG

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(text):return str(uuid.uuid5(uuid.NAMESPACE_URL,'flux-setup:'+text))
def tex(e):return sp.latex(sp.sympify(e)).replace(' ', '')
def source_q(t):return SOURCE[CONFIG[t]['index']]
def integral(d,outer,inner,style=False):
 v,lo,hi=inner
 s=''.join(r'{\int }_{'+tex(a)+r'}^{'+tex(b)+'}' for _,a,b in outer)+r'{\int }_{'+tex(lo)+r'}^{'+tex(hi)+'}'
 return s+r'\,'+tex(d)+r'\,\text{d}'+str(v)+''.join(r'\,\text{d}'+str(w) for w,_,_ in reversed(outer))
def triple(d):return r'{∭}_{R}'+('('+tex(d)+')' if sp.sympify(d).is_Add else tex(d))+r'\,\text{d}V'
def field_tex(cs):
 return '+'.join('('+tex(c)+r')\,'+b for c,b in zip(cs,'ijk')).replace('+(-','-(')
def partials(cs):return tuple(sp.diff(c,v) for c,v in zip(cs,VARS))
def derivative_block(cs,ds):
 formal='+'.join(r'\frac{∂}{∂'+str(v)+'}('+tex(c)+')' for v,c in zip(VARS,cs))
 terms='+'.join('('+tex(d)+')' if d.could_extract_minus_sign() else tex(d) for d in ds)
 return r'\begin{aligned}\text{div}\,F & ='+formal+r' \\  & ='+terms+r' \\  & ='+tex(sum(ds))+r'.\end{aligned}'
THEOREM='Let $R$ be a simple solid region bounded by a closed surface $S$ with positive (outward) orientation. If a vector field $F$ has continuous partial derivatives for all its components in an open region in space that contains $R,$ then the divergence theorem states that\n\n$$\n'+r'{∬}_{S}F\cdot dS={∭}_{R}\text{div}\,F\,\text{d}V.'+'\n$$\n\nComputing the divergence of $F,$ we obtain\n\n$$\n'
def region(outer,inner):
 v,l,u=inner
 return r'R=\{(x,y,z)\,:\,'+r',\,'.join(tex(a)+r'\le '+str(w)+r'\le '+tex(b) for w,a,b in outer)+r',\,'+tex(l)+r'\le '+str(v)+r'\le '+tex(u)+r'\}.'
def normal_solution(cs,outer,inner,easy):
 ds=partials(cs);d=sp.expand(sum(ds));s=THEOREM+derivative_block(cs,ds)+'\n$$\n\n'
 if easy:
  return s+'Let $R$ be the solid region enclosed by $S.$ Then, using the divergence theorem, we have\n\n$$\n'+r'\begin{aligned}{∬}_{S}F\cdot dS & ='+triple(d)+r' \\  & ='+integral(d,outer,inner)+r'.\end{aligned}'+'\n$$'
 label={x:'II',y:'III',z:'I'}[inner[0]]
 return s+'Therefore, using the divergence theorem, we have\n\n$$\n'+r'{∬}_{S}F\cdot dS='+triple(d)+',\n$$\n\nwhere $R$ is a type '+label+' solid region that can be written as\n\n$$\n'+region(outer,inner)+'\n$$\n\nAs a result,\n\n$$\n'+r'\begin{aligned}'+triple(d)+r' & ='+integral(d,outer,inner)+r'.\end{aligned}'+'\n$$'

# Raw evidence uses source masks for prose and exact original math spellings;
# scale is a true parameter: every field component, derivative contribution,
# triple/repeated integrand and complete historical option scales together.
# Source spelling is retained for s=1 by a multiplicative identity renderer.
def scale_tex(t,s):return t if s==1 else str(s)+r'\left('+t+r'\right)'
def raw_math(t,p):
 q=source_q(t);s=p['s'];c=CONFIG[t]
 prompt=q[':question/problem'];sol=q.get(':question/worked-solution')
 # Complete field formula token only: never replace a short scalar in prose.
 m=re.search(r'\$F\s*=([^$]+)\$',prompt);original=m.group(1)
 core=original.rstrip(',.');punct=original[len(core):]
 prompt=prompt[:m.start(1)]+scale_tex(core,s)+punct+prompt[m.end(1):]
 values=[scale_tex(a[':answer/value'],s) for a in q[':question/answer-fields'][0][':answer-field/choices']] if c['level']=='easy' else []
 if c['level']=='moderate':
  # Parsed integral shape supplies exact anchor spelling and a masked integrand.
  for a in q[':question/answer-fields'][0][':answer-field/choices']:
   value=a[':answer/value'];pos=value.index(r'\,');end=value.index(r'\,\text{d}',pos+2)
   values.append(value[:pos+2]+scale_tex(value[pos+2:end],s)+value[end:])
 if sol is not None and s!=1:
  # Keep common prose/stage route; replace complete mathematical blocks.
  cs=tuple(s*e for e in c['components']);outer=c['outer'];inner=c['inner'];normal=normal_solution(cs,outer,inner,c['level']=='easy')
  old_blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);new_blocks=re.findall(r'\$\$\n(.*?)\n\$\$',normal,re.S)
  assert len(old_blocks)==len(new_blocks)
  for old,new in zip(old_blocks,new_blocks):sol=sol.replace('$$\n'+old+'\n$$','$$\n'+new+'\n$$',1)
 return prompt,sol,values

def parameters_ok(t,p,raw):
 if raw:
  if set(p)!={'s'} or type(p['s']) is not int or not 1<=p['s']<=4:raise ValueError('raw scale s must be an integer 1..4')
 else:
  if set(p)!={'a','b','c','h','u','v'}:raise ValueError('parameters require a,b,c,h,u,v')
  if any(type(p[k]) is not int or not 1<=p[k]<=4 for k in ('a','b','c')):raise ValueError('component scales 1..4')
  if type(p['h']) is not int or not 0<=p['h']<=3:raise ValueError('surface offset 0..3')
  if any(type(p[k]) is not int or not 1<=p[k]<=2 for k in ('u','v')):raise ValueError('outer rectangle extents 1..2')

def objects(t,p):
 a,b,c,h,u,v=(p[k] for k in ('a','b','c','h','u','v'));cfg=CONFIG[t]
 if t.startswith('hard_'):
  # Cyclic relabeling is a comparable setup variant, never another KP branch.
  oo=cfg['orientation'];mapping={'z':(x,y,z),'x':(y,z,x),'y':(z,x,y)};U,V,W=mapping[oo]
  cs0=(a*x*y+b*z,b*y*z+c*x,c*x*z+a*y)
  perm={x:U,y:V,z:W};raw=[sp.expand(e.xreplace(perm)) for e in cs0]
  cs=tuple(raw[(U,V,W).index(w)] for w in VARS)
  outer=((U,0,u),(V,0,v));inner=(W,U+V,U+V+h+1+U**2+V**2)
 else:
  cs=tuple(k*e for k,e in zip((a,b,c),cfg['components']));outer=list(cfg['outer']);inner=cfg['inner']
  if cfg['level']=='moderate':
   # Positive outer intervals remove odd-symmetry scalar coincidences; the
   # actual region ordering is independently checked at all critical points.
   if t=='typeIIIbowl':outer=((x,0,1),(z,0,1))
   if t=='typeII':outer=((y,0,1),(z,0,1))
   inner=(inner[0],sp.sympify(inner[1]),sp.sympify(inner[2])+h)
  else:outer=((x,0,u),(y,0,v));inner=(z,0,1)
  outer=tuple(outer)
 return cs,outer,inner

def bank(t,cs,outer,inner):
 ds=partials(cs);d=sp.expand(sum(ds));easy=CONFIG[t]['level']=='easy'
 if easy:
  # Complete operation bank: divergence; omit first nonzero term; omit second;
  # wrong held partial of one component; add components rather than derivatives.
  nz=[i for i,v in enumerate(ds) if v!=0]
  if len(nz)<2: # legacy: two nonzero contributions anyway
   raise ValueError('needs two nonzero held terms')
  i,j=nz[:2];cross=cs[i]
  return [('correct',d),('omit_first',d-ds[i]),('omit_second',d-ds[j]),('undifferentiated_component',d-ds[i]+cross),('sum_components',sum(cs))]
 # Integral-bank setup errors derive from actual components/bounds, never a
 # scalar perturbation. Omit term, differentiate every component with respect
 # to the inner variable, flatten variable upper surface, reverse inner bounds.
 nz=[e for e in ds if e!=0];wrong=d-nz[0] if len(nz)>1 else sum(sp.diff(e,inner[0]) for e in cs)
 if sp.simplify(wrong-d)==0:wrong=sum(cs)
 subs={w:0 for w,_,_ in outer}
 flatten=(inner[1],inner[2].subs(subs)) if inner[2].free_symbols else (inner[1].subs(subs),inner[2])
 return [('correct',(d,inner[1],inner[2])),('wrong_derivative',(wrong,inner[1],inner[2])),('reverse_bounds',(d,inner[2],inner[1])),('flatten_surface',(d,flatten[0],flatten[1])),('wrong_and_reverse',(wrong,inner[2],inner[1]))]
@lru_cache(maxsize=32768)
def scalar_integral(spec,outer,variable):
 d,l,u=spec;r=sp.integrate(d,(variable,l,u))
 for w,a,b in reversed(outer):r=sp.integrate(r,(w,a,b))
 return sp.simplify(r)
def eligible(t,recipes,outer,inner):
 if CONFIG[t]['level']=='easy':
  values=[sp.expand(e) for _,e in recipes]
 else:values=[scalar_integral(e,outer,inner[0]) for _,e in recipes]
 if len(set(map(sp.srepr,values)))!=5:raise ValueError('whole bank collision')
 # Polynomial extrema of the surface gap on the outer rectangle, not grid guesses.
 gap=sp.expand(inner[2]-inner[1]);points=[{}]
 for w,a,b in outer:
  candidates=[a,b];critical=sp.solve(sp.diff(gap,w),w)
  candidates += [r for r in critical if r.is_real and not r.free_symbols and a<=r<=b]
  points=[q|{w:r} for q in points for r in candidates]
 if min(gap.subs(q) for q in points)<0:raise ValueError('crossed surfaces')

def normal_prompt(cs,outer,inner,easy):
 planes=', '.join('$'+str(w)+'='+tex(bound)+'$' for w,a,b in outer for bound in (a,b))
 if easy:description='rectangular prism enclosed by the planes '+planes+', $'+str(inner[0])+'='+tex(inner[1])+'$, $'+str(inner[0])+'='+tex(inner[2])+'$'
 else:description='finite solid region enclosed by the planes '+planes+', and the surfaces $'+str(inner[0])+'='+tex(inner[1])+'$ and $'+str(inner[0])+'='+tex(inner[2])+'$'
 prompt='Let $S$ be the boundary of the '+description+'. Given that the surface $S$ is positively (outward) oriented and $F='+field_tex(cs)+'$, the flux of $F$ across $S$ can be written as\n\n$$\n'+r'{∬}_{S}F\cdot dS='
 if easy:prompt+=integral(sp.Symbol('MISSING'),outer,inner).replace('MISSING',r'\bbox[2pt,border: 1pt solid black]{\phantom{AAAAA}}')+'.\n$$\n\nWhat is the missing part of the expression?'
 else:prompt+='\n$$'
 return prompt

def build(level,seed,t,p,profile):
 raw=profile=='observed_raw';parameters_ok(t,p,raw);cfg=CONFIG[t]
 if raw:
  q0=source_q(t);prompt,solution,values=raw_math(t,p);cs=tuple(p['s']*v for v in cfg['components']);outer=cfg['outer'];inner=cfg['inner']
  has_correct=':answer-field/correct' in q0[':question/answer-fields'][0]
  correct_index=None
  if has_correct:
   original=q0[':question/answer-fields'][0];correct_index=next(i for i,a in enumerate(original[':answer-field/choices']) if a[':answer/id']==original[':answer-field/correct'][':answer/id'])
  question={k:v for k,v in q0.items() if k.startswith(':question/') and k not in (':question/answer-fields',':question/id',':question/math-academy-id',':question/problem',':question/worked-solution')}
  if ':question/difficulty' in question:question[':question/difficulty']=question[':question/difficulty'][':db/ident']
  recipes=['observed_shape_'+str(i) for i in range(5)]
 else:
  cs,outer,inner=objects(t,p);rr=bank(t,cs,outer,inner);eligible(t,rr,outer,inner)
  values=[tex(e) if level=='easy' else integral(e[0],outer,(inner[0],e[1],e[2])) for _,e in rr]
  recipes=[label for label,_ in rr];prompt=normal_prompt(cs,outer,inner,level=='easy');solution=normal_solution(cs,outer,inner,level=='easy');correct_index=0;has_correct=True
  question={':question/difficulty':':question.difficulty/'+level}
 payload={'version':VERSION,'level':question.get(':question/difficulty'),'prompt':prompt,'solution':solution,'bank':sorted(values),'presence':has_correct};identity=digest(payload)
 question[':question/id']=uid(identity);question[':question/problem']=prompt
 if raw and ':question/math-academy-id' in q0:question[':question/math-academy-id']=q0[':question/math-academy-id']
 if solution is not None:question[':question/worked-solution']=solution
 answers=[{':answer/id':uid(identity+':selection:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 field={':answer-field/id':uid(identity+':selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if has_correct:field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 random.Random(seed).shuffle(answers);question[':question/answer-fields']=[field]
 d=sp.expand(sum(partials(cs)))
 # Bounds are incidental when only a missing integrand is assessed.
 task={'level':level,'criterion':'integrand' if level=='easy' else 'complete_setup','divergence':sp.srepr(d)}
 if level!='easy':task.update(outer=[(str(w),str(a),str(b)) for w,a,b in outer],inner=[str(v) for v in inner])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'seed':seed,'template':t,'profile':profile,'parameters':p,'recipes':recipes,'mathematical_fingerprint':digest(task),'content_identity':identity,'authored_level':level=='hard' or t=='legacy','evidence_only':raw,'eligible_for_learning':not raw,'source_ids':[] if level=='hard' else [source_q(t)[':question/math-academy-id']],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio shape')
 profile=profile or 'authored_method'
 if profile not in ('observed_raw','authored_method'):raise ValueError('unknown profile')
 rng=random.Random(seed);candidates=[t for t,c in CONFIG.items() if c['level']==level and (profile!='observed_raw' or 'index' in c)]
 if not candidates:raise ValueError('no observed profile at this difficulty')
 t=template or rng.choice(candidates)
 if t not in candidates:raise ValueError('template/level/profile mismatch')
 if parameters is not None:return build(level,seed,t,dict(parameters),profile)
 for _ in range(1000):
  p={'s':rng.randint(1,4)} if profile=='observed_raw' else {'a':rng.randint(1,4),'b':rng.randint(1,4),'c':rng.randint(1,4),'h':rng.randint(0,3),'u':rng.randint(1,2),'v':rng.randint(1,2)}
  try:return build(level,seed,t,p,profile)
  except ValueError as e:
   if str(e) not in ('whole bank collision','crossed surfaces'):raise
 raise ValueError('no eligible whole bank')

# EASY: observed supplied bounds; three diagonal held partials, no setup inference.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed simple regions I/II/III; diagonal held partials plus inner bounds.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored three nonzero diagonal terms; two variable inner surfaces.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for a in q.get(':question/answer-fields',[])[0][':answer-field/choices']:s+='- $'+a[':answer/value']+'$\n'
 if ':question/worked-solution' in q:s+='\n'+q[':question/worked-solution']
 return s
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
