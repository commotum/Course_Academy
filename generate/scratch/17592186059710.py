#!/usr/bin/env python3
"""Steps 3–7 local component-form vector generator, math/basis 1356.

Observed easy: four distinct source prompt/solution masks. Original attribute
omissions are public through raw-q-* profiles. Raw banks are parameterized
expression patterns, never literal source-return branches. Completed source
records separately label inferred correct refs, authored fields and solutions.
No original source has a captured correct designation. No plots are assessed.

Authored moderate: exactly three full vectors, all scaled, flat sum.
Authored hard: exactly three full vectors, nested subtraction/scaling.
Both retain component arithmetic in i,j; their missing-level assignments are
explicit design claims grounded in the lesson and its three-vector sibling.
Each level has fixed workload; there is no progression within a level.

Choose the family and complete bank before parameters. Reject whole colliding
banks. Historical q70402 patterns are opaque and always ineligible for default
learning. q70401's operations are defensible hypotheses, not recovered intent.
Task fingerprints exclude banks, seeds, presentation and unused scalar aliases;
content IDs include actual prompt, solution, complete bank and actual difficulty.
See accompanying README and extraction for boundaries and fidelity denominators.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059710
KP_UUID='d63a46dd-b963-5ecc-a96d-e0204ca480a9'
TITLE='Addition and Scalar Multiplication of Vectors in Component Form'
VERSION='component-vector-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}
SUPPORTED_LEVELS=('easy','moderate','hard')
TEMPLATES={'add':'easy','left_scale':'easy','right_scale':'easy','both_scale':'easy','flat_three':'moderate','nested_three':'hard'}
ANCHORS={
 'q-70401':('add',dict(ax=7,ay=-6,bx=3,by=2)),
 'q-70402':('left_scale',dict(ax=4,ay=2,bx=6,by=-4,p=2)),
 'q-125086':('right_scale',dict(ax=8,ay=-5,bx=-3,by=2,q=3)),
 'q-125088':('both_scale',dict(ax=-2,ay=-2,bx=4,by=-3,p=3,q=-2)),
}
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/component-vector/'+x))
def term(n,var):
 n=int(n)
 return ('-' if n<0 else '')+('' if abs(n)==1 else str(abs(n)))+var

def join(parts,space=False):
 sep=' ' if space else '';out=''
 for i,t in enumerate(parts):
  if i==0:out=t
  elif t.startswith('-'):out+=sep+'-'+sep+t[1:]
  else:out+=sep+'+'+sep+t
 return out

def vector(x,y,space=False,zeros=False):
 parts=[term(n,v) for n,v in ((x,'i'),(y,'j')) if zeros or n!=0]
 return join(parts,space) if parts else '0'

def expr(t,p,space=False):
 if t=='nested_three':return f"{term(p['p'],'a')}-{p['q']}(b-{term(p['r'],'c') if p['r']>0 else '('+term(p['r'],'c')+')'})"
 if t=='flat_three':return join([term(p[k],v) for k,v in [('p','a'),('q','b'),('r','c')]],space)
 c,d=scalars(t,p);return join([term(c,'a'),term(d,'b')],space)

def scalars(t,p):return (p.get('p',1) if t in ('left_scale','both_scale') else 1,p.get('q',1) if t in ('right_scale','both_scale') else 1)

def weights(t,p):
 if t=='flat_three':return [p['p'],p['q'],p['r']]
 if t=='nested_three':return [p['p'],-p['q'],p['q']*p['r']]
 return list(scalars(t,p))

def operands(t,p):return [(p[k+'x'],p[k+'y']) for k in ('abc' if t.endswith('three') else 'ab')]
def result(t,p):return tuple(sum(w*v[d] for w,v in zip(weights(t,p),operands(t,p))) for d in (0,1))

def checked_parameters(level,t,parameters,raw=False):
 keys=['ax','ay','bx','by']
 if t in ('left_scale','both_scale','flat_three','nested_three'):keys+=['p']
 if t in ('right_scale','both_scale','flat_three','nested_three'):keys+=['q']
 if t.endswith('three'):keys+=['cx','cy','r']
 if set(parameters)!=set(keys):raise ValueError('Parameters must be exactly '+str(keys))
 if any(type(v)!=int for v in parameters.values()):raise ValueError('Integer parameters required')
 p=dict(parameters)
 coords=[v for k,v in p.items() if k.endswith(('x','y'))]
 if not all(1<=abs(v)<=12 for v in coords):raise ValueError('Full nonzero integer vectors, magnitude <=12 required')
 if level=='easy':
  if any(not 1<=abs(p[k])<=3 for k in ('p','q') if k in p):raise ValueError('Easy scalar magnitude 1..3')
 elif level=='moderate':
  if any(not 2<=abs(p[k])<=4 for k in ('p','q','r')):raise ValueError('Moderate: all three scalar magnitudes 2..4')
  if not all(abs(v)<=9 for v in coords):raise ValueError('Moderate coordinates magnitude <=9')
 else:
  if p['p'] not in (-3,-2,2,3) or p['q'] not in (2,3) or p['r'] not in (-3,-2,2,3):raise ValueError('Hard p,r signed2..3; outer q positive2..3')
  if not all(abs(v)<=6 for v in coords):raise ValueError('Hard coordinates magnitude <=6')
 if max(abs(x) for x in result(t,p))>120:raise ValueError('Final arithmetic ceiling 120')
 return p

def sample(level,t,rng):
 bound={'easy':12,'moderate':9,'hard':6}[level]
 nz=[x for x in range(-bound,bound+1) if x]
 p={k:rng.choice(nz) for k in ['ax','ay','bx','by']}
 if t.endswith('three'):p.update(cx=rng.choice(nz),cy=rng.choice(nz))
 if t in ('left_scale','both_scale','flat_three','nested_three'):p['p']=rng.choice([2,3] if level=='easy' else [-4,-3,-2,2,3,4] if level=='moderate' else [-3,-2,2,3])
 if t in ('right_scale','both_scale','flat_three','nested_three'):p['q']=rng.choice([-3,-2,2,3] if level=='easy' else [-4,-3,-2,2,3,4] if level=='moderate' else [2,3])
 if t.endswith('three'):p['r']=rng.choice([-4,-3,-2,2,3,4] if level=='moderate' else [-3,-2,2,3])
 return p

def bank_values(t,p,profile):
 x,y=result(t,p);ax,ay,bx,by=(p[k] for k in ('ax','ay','bx','by'))
 if profile.endswith('q-70401') or profile=='observed-add':
  return [('correct',(x,y)),('subtract_x_reverse_y',(ax-bx,-ay-by)),('reverse_y_sum',(x,-y)),('reverse_x_subtract_y',(bx-ax,ay-by)),('subtract_x_add_y',(ax-bx,y))]
 if profile.endswith('q-70402'):
  # Exact observed expression patterns; cross-input 6j intent is unresolved.
  return [('correct',(x,y)),('opaque_keep_unscaled_ay',(x,ay)),('opaque_negate_unscaled_ay',(x,-ay)),('omit_scale_reverse_x',(bx-ax,ay+by)),('opaque_bx_as_y',(0,bx))]
 ws=weights(t,p);vs=operands(t,p)
 if t=='add':
  return [('correct',(x,y)),('subtract_b',(ax-bx,ay-by)),('reverse_y_sum',(x,-y)),('subtract_x_add_y',(ax-bx,y)),('add_x_subtract_y',(x,ay-by))]
 if t=='nested_three':
  a,b,c=vs;h,j,k=p['p'],p['q'],p['r']
  recipes=[('correct',(x,y)),('outer_sign_error',tuple(h*a[d]-j*b[d]-j*k*c[d] for d in (0,1))),('omit_outer_on_c',tuple(h*a[d]-j*b[d]+k*c[d] for d in (0,1))),('omit_inner_scale',tuple(h*a[d]-j*b[d]+j*c[d] for d in (0,1))),('scale_x_only',tuple(sum(w*v[0] for w,v in zip(ws,vs)) if d==0 else sum(v[1] for v in vs) for d in (0,1)))]
  return recipes
 # A complete four-error bank follows the actual scalar/distribution method.
 # Choose a genuinely scaled vector, not a unit coefficient alias.
 idx=next((i for i,w in enumerate(ws) if abs(w)>1),None)
 if idx is None:raise ValueError('Scaling bank requires nonunit scalar')
 w=ws[idx];v=vs[idx]
 return [('correct',(x,y)),('omit_one_scalar',(x+(1-w)*v[0],y+(1-w)*v[1])),('reverse_last_term',(x-2*ws[-1]*vs[-1][0],y-2*ws[-1]*vs[-1][1])),('scale_x_only',(x,sum(v[1] for v in vs))),('scale_y_only',(sum(v[0] for v in vs),y))]

def solution(t,p):
 e=expr(t,p);a=vector(p['ax'],p['ay']);b=vector(p['bx'],p['by']);x,y=result(t,p)
 opening=f"To compute ${e},$ we just need to compute all of the $i$'s and $j$'s, as follows:"
 if t in ('right_scale','both_scale'):
  u,v=scalars(t,p)
  sub=join([('' if u==1 else '-' if u==-1 else str(u))+f'({a})',('' if v==1 else '-' if v==-1 else str(v))+f'({b})'])
  dist=join([term(u*p['ax'],'i'),term(u*p['ay'],'j'),term(v*p['bx'],'i'),term(v*p['by'],'j')])
  collect=f"({join([term(u*p['ax'],'i'),term(v*p['bx'],'i')])})+({join([term(u*p['ay'],'j'),term(v*p['by'],'j')])})"
  rows=[sub,dist,collect]
  if x==0 or y==0:rows.append(vector(x,y,zeros=True))
  rows.append(vector(x,y))
  return opening+'\n\n$$\n'+r'\begin{aligned}'+e+' & ='+rows[0]+''.join(' '+r'\\'+'  & ='+r for r in rows[1:])+r'\end{aligned}'+'\n$$'
 # Ordered formal substitution, full distribution, component collection, reduction.
 vs=operands(t,p);ws=weights(t,p)
 if t=='nested_three':
  c=vector(p['cx'],p['cy']);inner_scalar=str(p['r']) if p['r']>0 else '('+str(p['r'])+')'
  c=vector(p['cx'],p['cy']);sub=f"{p['p']}({a})-{p['q']}(({b})-{inner_scalar}({c}))"
  # Nested operations are printed before the flattened component arithmetic.
  inner=tuple(p['b'+d]-p['r']*p['c'+d] for d in ('x','y'))
  after=f"{p['p']}({a})-{p['q']}({vector(*inner)})"
 else:
  sub=join([('' if w==1 else '-' if w==-1 else str(w))+f'({vector(*v)})' for w,v in zip(ws,vs)],True);after=None
 dist=join([term(w*v[d],'ij'[d]) for w,v in zip(ws,vs) for d in (0,1)],True)
 collect='('+join([term(w*v[0],'i') for w,v in zip(ws,vs)],True)+') + ('+join([term(w*v[1],'j') for w,v in zip(ws,vs)],True)+')'
 rows=[sub]+([after] if after else [])+[dist,collect]
 if x==0 or y==0:rows.append(vector(x,y,True,True))
 rows.append(vector(x,y,True))
 return opening+'\n\n$$\n'+r'\begin{aligned}'+'\n'+e+' &= '+rows[0]+''.join(' '+r'\\'+'\n&= '+r for r in rows[1:])+'\n'+r'\end{aligned}'+'\n$$'

def prompt(t,p):
 space=t in ('add','left_scale');e=expr(t,p,space);a=vector(p['ax'],p['ay'],space);b=vector(p['bx'],p['by'],space)
 if t.endswith('three'):
  return f"Find ${e}$ if $a={a}$, $b={b}$, and $c={vector(p['cx'],p['cy'])}$."
 if space:return f'Find ${e}$ if $a = {a}$ and $b = {b}$.'
 return f'Find ${e}$ if $a={a}$ and $b={b}.$'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed supported radio fields are authored')
 rng=random.Random(seed);sid=None;raw=False
 if profile and profile.startswith(('raw-','completed-')):
  sid=profile.split('-',1)[1]
  if sid not in ANCHORS:raise ValueError('Unknown source profile')
  expected=ANCHORS[sid][0]
  if template is not None and template!=expected:raise ValueError('Source profile/template mismatch')
  template=expected;raw=profile.startswith('raw-')
 templates=[t for t,l in TEMPLATES.items() if l==level]
 if template is None:template=rng.choice(templates)
 if template not in templates:raise ValueError('Template outside requested difficulty')
 if profile is None:profile=rng.choice(['observed-add','authored-operations']) if template=='add' else 'authored-operations'
 if profile=='observed-add' and template!='add':raise ValueError('Observed-add needs add family')
 if profile not in ('observed-add','authored-operations') and sid is None:raise ValueError('Unknown profile')
 explicit=parameters is not None
 for attempt in range(10000):
  p=checked_parameters(level,template,parameters if explicit else sample(level,template,rng),raw)
  values=[] if raw and sid in ('q-125086','q-125088') else bank_values(template,p,profile)
  # Raw fieldless cases have no displayed bank; internal correct math still derived.
  if raw and sid in ('q-125086','q-125088'):break
  if len({v for _,v in values})==5:break
  if explicit:raise ValueError('Whole complete bank is ambiguous')
 else:raise ValueError('No eligible whole instance sampled')
 q={':question/problem':prompt(template,p)}
 if not (raw and sid in ('q-70401','q-70402')):q[':question/worked-solution']=solution(template,p)
 if not (raw and sid in ('q-70401','q-70402')):q[':question/difficulty']=':question.difficulty/'+level
 display_values=[vector(*v,space=True) for _,v in values]
 # Source q125 masks do not have a bank. Completed fields are explicitly authored.
 if not (raw and sid in ('q-125086','q-125088')):
  q[':question/answer-fields']=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[]}]
 actual_bank=sorted(display_values) if ':question/answer-fields' in q else None
 identity=digest({'version':VERSION,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':actual_bank,'difficulty':q.get(':question/difficulty'),'correct_present':not raw})
 q[':question/id']=uid(identity)
 if ':question/answer-fields' in q:
  field=q[':question/answer-fields'][0];field[':answer-field/id']=uid(identity+'/selection')
  answers=[{':answer/id':uid(identity+'/selection/'+s),':answer/type':':answer.type/math',':answer/value':s} for s in display_values]
  correct_id=answers[0][':answer/id'];rng.shuffle(answers);field[':answer-field/choices']=answers
  if not raw:field[':answer-field/correct']=[':answer/id',correct_id]
 # Canonical task = actual operands and normalized operator tree. No unused
 # scalars are accepted; presentation spacing, bank aliases, seeds are excluded.
 task={'operands':operands(template,p),'operator':('nested',p['p'],p['q'],p['r']) if template=='nested_three' else ('flat',weights(template,p))}
 fp=digest(task)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':PROVENANCE,'seed':seed,'level':level,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fp,'mathematical_fingerprint':fp,'content_identity':identity,'evidence_only':raw or (sid=='q-70402'),'eligible_for_learning':not raw and sid!='q-70402','source_id':sid,'completion':{'correct_ref':'preserved absent' if raw else 'independently inferred' if sid else 'authored','fields':'preserved absent' if raw and sid in ('q-125086','q-125088') else 'authored from observed radio layout' if sid in ('q-125086','q-125088') else 'observed radio layout','solution':'preserved absent' if raw and sid in ('q-70401','q-70402') else 'authored canonical component stages' if template in ('add','left_scale') else 'observed shared stages' if template in ('right_scale','both_scale') else 'authored same-method extension'},'recipe_operations':[label for label,v in values],'difficulty_origin':'observed easy / unrated authored easy completion' if level=='easy' else 'authored missing-level design','plot_rating':'none','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: observed two-vector addition/scaling masks, integer arithmetic.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: authored fixed six scalar products and four component additions.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored fixed three-vector nested scaling/subtraction, same component method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
 q=rec['question'];text=q[':question/problem']
 for f in q.get(':question/answer-fields',[]):
  text+='\n\n'+'\n'.join(f"- ${a[':answer/value']}$" for a in f[':answer-field/choices'])
 if ':question/worked-solution' in q:text+='\n\n'+q[':question/worked-solution']
 return text

def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=[*SUPPORTED_LEVELS,'all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json','markdown'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 if args.count<1:raise ValueError('Count must be positive')
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
