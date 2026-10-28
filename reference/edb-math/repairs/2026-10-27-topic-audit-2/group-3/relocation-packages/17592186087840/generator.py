#!/usr/bin/env python3
"""Seeded tall-ellipse generator. Source banks remain replayable; normal radio
samples the plotted target before a compatible five-ellipse neighborhood.
Runtime assets require COURSE_ACADEMY_GENERATOR_OUTPUT_DIR. No publication.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, sys, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record
from render import render_plot
KP_ID=17592186087840
KP_UUID='de557d1d-5f27-50e3-bcba-22b21f83267f'
GENERATOR_UUID='d4491310-401d-5065-a825-13199d423032'
SUPPORTED_LEVELS=('easy','moderate')
TITLE='Determining the Equation of a Tall Ellipse'
VERSION='tall-ellipse-package-2'
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source-data.json').read_text())
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}
# Exact source-derived geometry; observed styles are kept separate from math.
SOURCE_GEOMETRY={'q-16458':(2,3),'q-279153':('3/2','9/2'),'q-7605':(3,4),'q-115123':(6,9),'q-115124':(2,6),'q-115126':(3,8),'q-115129':(1,4),'q-16451':(3,6),'q-277921':(2,7),'q-279151':('7/2',4),'q-279158':('9/2','13/2'),'q-69892':(1,2),'q-69893':(2,5),'q-73627':(4,6),'q-7602':(1,3),'q-7608':(3,5),'q-279141':(4,9),'q-279143':(4,'15/2'),'q-279145':(5,'17/2'),'q-279154':('5/2','7/2'),'q-279155':('7/2','11/2'),'q-73631':(5,7),'q-115128':(4,7)}
RECORDS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Whole bank first. Each tuple gives exact x/y denominators. No first-valid pool.
BANKS={
'q-16458':('a2,b','b,a','b2,a2','a,b','a2,b2'),
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
'q-115128':('b2,a2','b,a','2a,2b','a,b','a2,b2'),
'neighborhood':('h2,v2','(h-1)2,v2','(h+1)2,v2','h2,(v-1)2','h2,(v+1)2')}
OPAQUE={'q-73627','q-7605','q-73631'}
TEMPLATES={'integer_radio':('easy','radio'),'integer_blank':('easy','blank'),'half_blank':('moderate','blank')}

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
 if level=='easy':radii=[sp.Rational(n) for n in range(1,10)]
 elif level=='moderate':radii=[sp.Rational(n,2) for n in range(2,21)]
 else:raise ValueError('Unknown difficulty')
 return [(a,b) for a in radii for b in radii if a<b and b/a<=4 and (level!='moderate' or a.q==2 or b.q==2)]

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

def neighborhood(h,v):
 return [(h,v),(h-1,v),(h+1,v),(h,v-1),(h,v+1)]

def anchors():
 eligible=set(domain('easy'))
 return [(h,v) for h,v in sorted(eligible) if all(pair in eligible for pair in neighborhood(h,v))]

def plot(a,b,source_profile=None):
 if source_profile in RECORDS and (a,b)==tuple(map(rat,SOURCE_GEOMETRY[source_profile])):
  import re
  relative=re.search(r'!\[\]\((.*?)\)',RECORDS[source_profile][':question/problem'])[1]
  return relative,{'role':'prompt','a':str(a),'b':str(b),'original':True}
 directory=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not directory:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated assets')
 out=Path(directory).resolve();out.mkdir(parents=True,exist_ok=True)
 spec={'a':str(a),'b':str(b),'renderer_version':4,'equal_scale':True,'width':480,'height':400}
 stem=digest(spec);png=out/(stem+'.png');side=out/(stem+'.json')
 if not png.exists() or not side.exists():render_plot(spec,png,side)
 return str(png),{'role':'prompt','path':str(png),'sidecar':str(side),'original':False,**spec}

def _generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,target=None,anchor=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
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
  if profile not in (None,'neighborhood','blank'):raise ValueError('Unknown profile')
  available=[t for t,(l,k) in TEMPLATES.items() if l==level and (field_type is None or field_type.split('/')[-1]==k)]
  if not available:raise ValueError('Unsupported field type')
  template=template or rng.choice(available)
  if template not in available:raise ValueError('Template/level/field mismatch')
  kind=TEMPLATES[template][1];bank_profile='neighborhood' if kind=='radio' else 'blank'
  if profile is not None and profile!=bank_profile:raise ValueError('Profile/field mismatch')
 if field_type and field_type.split('/')[-1]!=kind:raise ValueError('Wrong field type')
 pairs=domain(level)
 normal_radio=kind=='radio' and source_id is None
 chosen_anchor=None
 if normal_radio:
  # Target assignment first; every compatible anchor supports all five roles.
  target=rng.randrange(5) if target is None else target
  if target not in range(5):raise ValueError('target must be 0..4')
  eligible=anchors()
  if parameters is not None:
   if set(parameters)!={'a','b'}:raise ValueError('Only a,b parameters')
   requested=tuple(rat(parameters[k]) for k in ('a','b'))
   eligible=[pair for pair in eligible if neighborhood(*pair)[target]==requested]
  if anchor is not None:
   chosen_anchor=tuple(map(rat,anchor))
   if chosen_anchor not in eligible:raise ValueError('Incompatible anchor')
  else:
   if not eligible:raise ValueError('No compatible neighborhood for target/parameters')
   chosen_anchor=rng.choice(eligible)
  radii=neighborhood(*chosen_anchor);a,b=radii[target]
  bp=[(u*u,v*v) for u,v in radii]
 else:
  if target is not None or anchor is not None:raise ValueError('Targets belong to normal radio')
  if parameters is not None:
   if set(parameters)!={'a','b'}:raise ValueError('Only a,b are mathematical parameters')
   a,b=rat(parameters['a']),rat(parameters['b'])
   if (a,b) not in pairs:raise ValueError('Parameters outside level domain')
  elif source_id:a,b=map(rat,SOURCE_GEOMETRY[source_id])
  else:a,b=rng.choice(pairs)
  bp=bank_pairs(bank_profile,a,b) if kind=='radio' else [(a*a,b*b)]
 plain=source_id=='q-7605';one=source_id=='q-69892'
 values=[normalize_tex(equation(u,v,one,plain) if kind=='radio' else lhs(u,v)) for u,v in bp]
 correct_index=bp.index((a*a,b*b))
 p,asset=plot(a,b,source_id if raw else None)
 problem='![]('+p+')\n\nWhat is the equation of the ellipse given above?'+('\n\n{{field-1}}$=1$' if kind=='blank' else '')
 sol=normalize_prose(solution(a,b,one))
 problem=normalize_prose(problem)
 payload={':question/problem':problem,':question/difficulty':':question.difficulty/'+level}
 if not (raw and source_id=='q-7605'):payload[':question/worked-solution']=sol
 if raw and source_id=='q-7605':payload.pop(':question/difficulty')
 has_correct=not(raw and source_id=='q-7605')
 identity_payload={k:(v.replace(p,'asset:'+Path(p).name) if k==':question/problem' else v) for k,v in payload.items()}
 content=digest({'version':VERSION,'payload':identity_payload,'bank':sorted(values),'field':kind,'correct':values[correct_index] if has_correct else None})
 qid=uid(content);key='selection' if kind=='radio' else 'field-1';fid=uid(qid+key)
 answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if has_correct:f[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':qid,**payload,':question/answer-fields':[f]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':{'a':str(a),'b':str(b)},'bank_profile':profile or bank_profile,'target':target,'anchor':list(map(str,chosen_anchor)) if chosen_anchor else None,'recipes':list(BANKS[bank_profile]) if kind=='radio' else ['reciprocal_squared_radii'],'source':PROVENANCE,'source_id':source_id,'raw_source_replay':raw,'presentation_repair':repair,'normal_eligible':source_id is None,'eligible_for_learning':source_id is None,'evidence_only':source_id is not None,'default_sampling_eligible':source_id is None,'mathematical_eligible':True,'source_bank_replay_eligible':raw,'interpretation_status':'opaque evidence' if source_id in OPAQUE else ('observed pattern hypothesis' if source_id else 'authored assessed-method operations'),'opaque_evidence':source_id in OPAQUE,'difficulty_authored':source_id=='q-7605','mathematical_fingerprint':digest({'a':str(a),'b':str(b),'skill':'origin_tall_ellipse'}),'content_identity':content,'finite_domain_tasks':len(pairs),'plot':asset}}

def generate(*args,**kwargs):
 r=_generate(*args,**kwargs)
 # The incomplete original is an evidence replay, never a delivery candidate.
 if r['generation']['raw_source_replay'] and r['generation']['source_id']=='q-7605':return r
 return validate_generated_record(r)

# EASY: observed integer radii, full equation radio or supplied-LHS blank.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed halves; at least one reduced noninteger radius, LHS blank.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 if ':question/worked-solution' in q:s+='\n'+q[':question/worked-solution']
 return s
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','all'],default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 levels=['easy','moderate'] if a.difficulty=='all' else [a.difficulty]
 records=[]
 for l in levels:
  seen=set();attempt=0;goal_count=len(records)+a.count
  if a.profile and a.count!=1:p.error('Source replay profiles support count=1')
  while len(records)<goal_count:
   if attempt>max(1000,a.count*100):p.error('Requested count exceeds available unique semantic instances')
   r=generate(l,a.seed+attempt,a.template,profile=a.profile);attempt+=1
   signature=(r['generation']['template'],r['generation']['parameters']['a'],r['generation']['parameters']['b'])
   if signature in seen:continue
   seen.add(signature);records.append(r)
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
