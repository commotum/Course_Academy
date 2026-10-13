#!/usr/bin/env python3
"""Determining the equation of a tall origin-centered ellipse (basis 1356).

Public API: generate(level, seed=0, template=None, field_type=None,
parameters=None, profile=None), plus generate_easy/moderate/hard.
Only private review records and Matplotlib assets; no database writes.
Source profiles are complete explicitly selectable replay banks, not defaults.
Unresolved distractor operations are labeled opaque evidence. See extraction.
Hard is an authored scope claim: thirds/quarters replace observed halves, with
exactly the same reading/substitution/squaring method. All domains are finite.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186087840
KP_UUID='de557d1d-5f27-50e3-bcba-22b21f83267f'
TITLE='Determining the Equation of a Tall Ellipse'
VERSION='tall-ellipse-1'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}
X,Y=sp.symbols('x y')
# Exact source-derived geometry; observed styles are kept separate from math.
SOURCE_GEOMETRY={'q-279153':('3/2','9/2'),'q-7605':(3,4),'q-115123':(6,9),'q-115124':(2,6),'q-115126':(3,8),'q-115129':(1,4),'q-16451':(3,6),'q-277921':(2,7),'q-279151':('7/2',4),'q-279158':('9/2','13/2'),'q-69892':(1,2),'q-69893':(2,5),'q-73627':(4,6),'q-7602':(1,3),'q-7608':(3,5),'q-279141':(4,9),'q-279143':(4,'15/2'),'q-279145':(5,'17/2'),'q-279154':('5/2','7/2'),'q-279155':('7/2','11/2'),'q-73631':(5,7)}
RECORDS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Whole bank first. Each tuple gives exact x/y denominators. No first-valid pool.
BANKS={
'q-115123':('a2,b2','b,a','2a,2b','b2,a2','a,b'),
'q-115124':('b2,a2','a2,2b','a2,b2','a,b','b,a2'),
'q-115126':('2a,2b','b2,a2','a2,b2','b,a','a,b'),
'q-115129':('2a,2b','b,a','b2,a2','a,b','a2,b2'),
'q-16451':('2a,2b','a2,b2','a,b','b,a','b2,a2'),
'q-69892':('a2,2b2','a,b','b,a','b2,a2','a2,b2'),
'q-69893':('a2,b2','b2,a2','a,b','b,a','a2,2b'),
'q-7602':('b2,a2','2a,b2','b,a','a2,b2','a,b'),
'q-7608':('a2,b2','a2,b','a,b','2a2,b2','b2,a2'),
'q-73631':('a2,b2','(a-1)2,b2','a,b','b2,a2','b,a'),
# These two complete banks contain opaque operations. Proportional denominator
# families are evidence parameterizations, never alleged cognitive error models.
'q-73627':('b2,a2','a,a2','a2,a2','a2,b2','opaque12,opaque32'),
'q-7605':('a2,opaque4','(a+1)2,a2','a,b','a2,b2','b,a'),
'authored':('a2,b2','b2,a2','a,b','b,a','2a,2b')}
OPAQUE={'q-73627','q-7605','q-73631'}
TEMPLATES={'integer_radio':('easy','radio'),'integer_blank':('easy','blank'),'half_blank':('moderate','blank'),'rational_blank':('hard','blank')}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'tall-ellipse:'+str(v)))
def rat(v):
 try:r=sp.Rational(v)
 except Exception as e:raise ValueError('Exact rational parameters required') from e
 return r

def tex(r):
 r=rat(r)
 return str(r.p) if r.q==1 else rf'\frac{{{r.p}}}{{{r.q}}}'

def term(var,d,one=False,plain=False):
 d=rat(d);v=var+'^{2}' if plain else '{'+var+'}^{2}'
 if d==1 and one:return v
 if d.q==1:return rf'\frac{{{v}}}{{{d.p}}}'
 return rf'\frac{{{d.q}{v}}}{{{d.p}}}'

def lhs(a2,b2,one=False,plain=False):
 sep=' + ' if plain else '+'
 return term('x',a2,one,plain)+sep+term('y',b2,one,plain)

def equation(a2,b2,one=False,plain=False):return lhs(a2,b2,one,plain)+(' = 1' if plain else '=1')

def denominator(node,a,b):
 operations={'a':a,'b':b,'a2':a*a,'b2':b*b,'2a':2*a,'2b':2*b,'2a2':2*a*a,'2b2':2*b*b,'(a-1)2':(a-1)**2,'(a+1)2':(a+1)**2,
 'opaque12':sp.Rational(3,4)*a*a,'opaque32':sp.Rational(8,9)*b*b,'opaque4':b*b/4}
 if node not in operations:raise ValueError(node)
 return operations[node]

def bank_pairs(profile,a,b):
 recipes=BANKS[profile]
 out=[tuple(denominator(t,a,b) for t in recipe.split(',')) for recipe in recipes]
 if any(d<=0 for pair in out for d in pair):raise ValueError('Bank denominator must be positive')
 if len(set(out))!=len(out):raise ValueError('Reject whole bank: equivalent options')
 if out.count((a*a,b*b))!=1:raise ValueError('Exactly one correct equation required')
 return out

def domain(level):
 if level=='easy':radii=[sp.Rational(n) for n in range(1,13)]
 elif level=='moderate':radii=[sp.Rational(n,2) for n in range(2,21)]
 elif level=='hard':radii=sorted(set(sp.Rational(n,d) for d in (3,4) for n in range(d,8*d+1) if sp.Rational(n,d).q==d))
 else:raise ValueError('Unknown difficulty')
 return [(a,b) for a in radii for b in radii if a<b and b/a<=4 and (level!='moderate' or a.q==2 or b.q==2) and (level!='hard' or b/a<=3)]

def solution(a,b,one=False):
 def squared_radius(r):return '{'+(tex(r) if r.q==1 else '('+tex(r)+')')+'}^{2}'
 def squared_value(r):return str(r*r) if r.q==1 else '('+tex(r*r)+')'
 formal=r'\frac{{x}^{2}}{{a}^{2}}+\frac{{y}^{2}}{{b}^{2}}'
 sub=rf'\frac{{{{x}}^{{2}}}}{{{squared_radius(a)}}}+\frac{{{{y}}^{{2}}}}{{{squared_radius(b)}}}'
 # Preserve separate square evaluation and reciprocal simplification for fractions.
 evaluated=rf'\frac{{{{x}}^{{2}}}}{{{squared_value(a)}}}+\frac{{{{y}}^{{2}}}}{{{squared_value(b)}}}'
 rows=[formal+r' & =1',sub+r' & =1']
 if a.q!=1 or b.q!=1:rows.append(evaluated+r' & =1')
 rows.append(lhs(a*a,b*b,one)+r' & =1.')
 return ('Remember that the equation of an ellipse centered at the origin with a horizontal radius of length $a$ and a vertical radius of length $b$ is given by\n\n$$\n'+formal+'=1.\n$$\n\n \n\nHere, the horizontal radius has length $a='+tex(a)+'$ and the vertical radius has length $b='+tex(b)+'.$ Therefore, the equation of the ellipse is\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$')

def plot(a,b,source_profile=None):
 if source_profile in RECORDS and (a,b)==tuple(map(rat,SOURCE_GEOMETRY[source_profile])):
  # Unchanged exact source asset remains read-only. Parameter changes render anew.
  import re
  relative=re.search(r'!\[\]\((.*?)\)',RECORDS[source_profile][':question/problem'])[1]
  return relative,{'role':'prompt','source_asset':'/media/jake/SSD/EDB/math/'+relative,'a':str(a),'b':str(b),'original':True}
 spec={'a':str(a),'b':str(b),'renderer_version':3,'equal_scale':True,'width':480,'height':400,'origin':[0,0],'intercepts':[[str(a),'0'],[str(-a),'0'],['0',str(b)],['0',str(-b)]],'bounds':[-str_float(b*sp.Rational(6,5)),str_float(b*sp.Rational(6,5)),-str_float(b*sp.Rational(6,5)),str_float(b*sp.Rational(6,5))]}
 out=HERE/'plots';out.mkdir(exist_ok=True);stem=digest(spec);png=out/(stem+'.png');side=out/(stem+'.json')
 if not png.exists() or not side.exists():
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-',dir=out,delete=False) as f:
   json.dump({'spec':spec,'png':str(png),'sidecar':str(side)},f);input_path=f.name
  try:subprocess.run([sys.executable,str(HERE/'render.py'),input_path],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  finally:Path(input_path).unlink(missing_ok=True)
 return str(png),{'role':'prompt','path':str(png),'sidecar':str(side),'original':False,**spec}

def str_float(v):return float(v)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);raw=False;repair=False;source_id=None
 if profile and profile.startswith('repair-'):
  source_id=profile[len('repair-'):];repair=True
  if source_id!='q-7605':raise ValueError('Only q-7605 has a supported repair profile')
 elif profile in RECORDS:source_id=profile;raw=True
 if source_id:
  sq=RECORDS[source_id];kind=sq[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
  inferred_level=sq.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
  if level!=inferred_level:raise ValueError('Replay level must equal observed/inferred assignment')
  stemplate='half_blank' if level=='moderate' else 'integer_'+kind
  if template and template!=stemplate:raise ValueError('Source/template mismatch')
  template=stemplate;bank_profile=source_id if kind=='radio' else 'blank'
 else:
  if profile not in (None,'authored','blank'):raise ValueError('Unknown profile')
  available=[t for t,(l,k) in TEMPLATES.items() if l==level and (field_type is None or field_type.split('/')[-1]==k)]
  if not available:raise ValueError('Unsupported field type')
  template=template or rng.choice(available)
  if template not in available:raise ValueError('Template/level/field mismatch')
  kind=TEMPLATES[template][1];bank_profile='authored' if kind=='radio' else 'blank'
  if profile is not None and profile!=bank_profile:raise ValueError('Profile/field mismatch')
 if field_type and field_type.split('/')[-1]!=kind:raise ValueError('Wrong field type')
 pairs=domain(level)
 if parameters is not None:
  if set(parameters)!={'a','b'}:raise ValueError('Only a,b are mathematical parameters')
  a,b=rat(parameters['a']),rat(parameters['b'])
  if (a,b) not in pairs:raise ValueError('Parameters outside reduced level domain')
 elif source_id:a,b=map(rat,SOURCE_GEOMETRY[source_id])
 else:a,b=rng.choice(pairs)
 if kind=='radio':
  # Selection of the complete bank precedes parameter sampling and validation.
  # The fixed bank_profile above identifies all required operations.
  if parameters is None and not source_id:
   for _ in range(len(pairs)*2):
    try:bp=bank_pairs(bank_profile,a,b);break
    except ValueError:a,b=rng.choice(pairs)
   else:raise ValueError('No eligible complete bank')
  else:bp=bank_pairs(bank_profile,a,b)
 else:bp=[(a*a,b*b)]
 plain=source_id=='q-7605';one=source_id=='q-69892'
 values=[equation(u,v,one,plain) if kind=='radio' else lhs(u,v) for u,v in bp]
 correct_index=bp.index((a*a,b*b))
 p,asset=plot(a,b,source_id if raw else None)
 problem='![]('+p+')\n\nWhat is the equation of the ellipse given above?'+('\n\n{{field-1}}$=1$' if kind=='blank' else '')
 sol=solution(a,b,one)
 payload={':question/problem':problem,':question/difficulty':':question.difficulty/'+level}
 if not (raw and source_id=='q-7605'):payload[':question/worked-solution']=sol
 if raw and source_id=='q-7605':payload.pop(':question/difficulty')
 has_correct=not(raw and source_id=='q-7605')
 content=digest({'version':VERSION,'payload':payload,'bank':sorted(values),'field':kind,'correct':values[correct_index] if has_correct else None})
 qid=uid(content);key='selection' if kind=='radio' else 'field-1';fid=uid(qid+key)
 answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if has_correct:f[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':qid,**payload,':question/answer-fields':[f]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{'a':str(a),'b':str(b)},'bank_profile':profile or bank_profile,'recipes':list(BANKS[bank_profile]) if kind=='radio' else ['reciprocal_squared_radii'],'source':PROVENANCE,'source_id':source_id,'raw_source_replay':raw,'presentation_repair':repair,'normal_eligible':source_id is None,'eligible_for_learning':source_id is None,'evidence_only':source_id is not None,'default_sampling_eligible':source_id is None,'mathematical_eligible':True,'source_bank_replay_eligible':raw,'interpretation_status':'opaque evidence' if source_id in OPAQUE else ('observed pattern hypothesis' if source_id else 'authored assessed-method operations'),'opaque_evidence':source_id in OPAQUE,'difficulty_authored':level=='hard' or source_id=='q-7605','mathematical_fingerprint':digest({'a':str(a),'b':str(b),'skill':'origin_tall_ellipse'}),'content_identity':content,'finite_domain_tasks':len(pairs),'plot':asset}}

# EASY: observed integer radii, full equation radio or supplied-LHS blank.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed halves; at least one reduced noninteger radius, LHS blank.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored thirds/quarters, both noninteger; same operation and LHS shape.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 if ':question/worked-solution' in q:s+='\n'+q[':question/worked-solution']
 return s
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
