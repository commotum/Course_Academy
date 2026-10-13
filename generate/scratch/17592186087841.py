#!/usr/bin/env python3
"""Ellipse axes; read two squared radii, take roots, order and double.

Snapshot math basis 1356; no DB access. All recipes and source layout flags are
parameterized. Opaque observed numerical transformations are evidence-only,
never default learner banks. Moderate/hard are authored bounded number-form
extensions, not recovered difficulty labels. See private evidence README.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186087841
KP_UUID='4e43e393-8752-58bc-b87c-b72f679cbfd9'
TITLE='Determining the Lengths of the Major and Minor Axes Given the Equation of an Ellipse'
VERSION='ellipse-axes-v1'
ROOT=Path(__file__).resolve().parent/str(KP_ID)
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
U,V=sp.symbols('U V',positive=True)
A,B=sp.sqrt(U),sp.sqrt(V)
# COMPLETE observed banks in original order. U,V are larger/smaller squared
# radii. Opaque flags separate evidence transforms from authored error operations.
BANK_PROFILES={
 'observed_q-7598':[(A+B,B),(2*A,2*B),(A+B,2*B),(A,B),(2*A,B)],
 'observed_q-7600':[(2*B,sp.Rational(5,3)*B),(2*A,2*B),(2*B,sp.Rational(2,3)*B),(A,B),(sp.Rational(5,3)*B,B)],
 'observed_q-115132':[(U,V),(2*V,2*A),(U/2,V/2),(A,B),(2*A,2*B)],
 'observed_q-115135':[(2*A,2*B),(A/2,B/2),(U/2,V/2),(U,V),(A,B)],
 'observed_q-16452':[(sp.sqrt(2)*A,B),(2*A,2*B),(2*U,2*V),(U,V),(sp.sqrt(2)*A,A)],
 'observed_q-16454':[(2*A,B),(A,B),(U,V),(2*A,2*B),(U/2,V)],
 'observed_q-69563':[(2*A,2*B),(2*sp.sqrt(2)*A,2*sp.sqrt(2)*B),(A,2*B),(A,B),(sp.sqrt(2)*A,sp.sqrt(2)*B)],
 'observed_q-7595':[(A,B),(2*B,A),(4*B,2*A),(2*A,2*B),(2*A,B)],
 'observed_q-7601':[(A,B),(U,V),(sp.sqrt(A),sp.sqrt(B)),(2*A,2*B),(2*U,2*V)],
 'observed_q-7596':[(2*A,B),(A,B),(2*B,B),(U,V),(2*A,2*B)],
 'observed_q-7597':[(2*A,2*B),(A,B),(U,V),(U/2,V/2),(A/2,B/2)],
 'observed_q-115134':[(4*A,4*B),(U/2,V/2),(2*A,2*B),(U,V),(A,B)],
 'observed_q-16455':[(U,V),(A,B),(2*A,2*B),(U/2,2*V),(A,2*B)],
 'authored_axes':[(2*A,2*B),(A,B),(2*A,B),(A,2*B),(U,V)],
}
OPAQUE={'observed_q-7600':[0,2,4], 'observed_q-115132':[1],
        'observed_q-16454':[4], 'observed_q-16455':[3]}
# These names describe actual arithmetic, not claims about original intent.
RECIPES={k:[{'expression':[str(a),str(b)],'interpretation':'opaque numerical evidence' if i in OPAQUE.get(k,[]) else 'explicit arithmetic generalization; original intent unverified'} for i,(a,b) in enumerate(v)] for k,v in BANK_PROFILES.items()}
TEMPLATES={'radio_so':'radio','radio_thus':'radio','radio_so_space':'radio',
           'radio_unrated':'radio','blank':'blank','blank_newline':'blank'}

def tex(value):
 return sp.latex(sp.simplify(value)).replace(' ','')
def ident(value):
 return str(uuid.uuid5(uuid.UUID(KP_UUID),value))
def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rational(value):
 # No floating input or symbolic syntax: workload guards apply to reduced objects.
 if isinstance(value,bool) or isinstance(value,float):raise ValueError('Exact integer or rational string required')
 try:r=sp.Rational(value)
 except Exception as exc:raise ValueError('Exact rational denominator required') from exc
 return r

def validate_parameters(level, parameters, evidence=False):
 if set(parameters)!={'dx','dy'}:raise ValueError('Exactly dx and dy required')
 p={k:rational(v) for k,v in parameters.items()}
 if p['dx']==p['dy']:raise ValueError('Unequal squared radii required')
 for value in p.values():
  if value<=0 or value.p>100 or value.q>16:raise ValueError('Positive reduced numerator <=100 and denominator <=16 required')
 if level=='easy':
  if any(v.q!=1 for v in p.values()):raise ValueError('Easy uses positive integer squared radii')
 elif level=='moderate':
  if sum(v.q>1 for v in p.values())!=1:raise ValueError('Moderate requires exactly one fractional squared radius')
  for v in p.values():
   if v.q not in (1,4,9):raise ValueError('Moderate denominator must be 1,4,9')
  # Noninteger fractional radius keeps rational-root work substantive.
 elif level=='hard':
  for v in p.values():
   if v.q not in (4,9,16) or sp.sqrt(v.p).is_Integer:raise ValueError('Hard requires two fractional nonsquare radicands')
   squarefree=sp.prod(prime for prime,power in sp.factorint(v.p).items() if power%2)
   if squarefree not in (2,3,5,6,7):raise ValueError('Hard squarefree part must be 2,3,5,6,7')
   if sp.sqrt(v.p/squarefree)>3:raise ValueError('Hard radical coefficient must be at most3 after reduction')
 else:raise ValueError('Unknown difficulty')
 return p

# EASY: observed integer squared radii, including one or two exact radicals.
def sample_easy(rng):return {'dx':rng.randint(1,100),'dy':rng.randint(1,100)}
# MODERATE: authored; one reduced fractional squared radius, other integer.
def sample_moderate(rng):
 vals=[sp.Rational(rng.randint(1,100),rng.choice((4,9))),sp.Integer(rng.randint(1,100))]
 rng.shuffle(vals);return dict(zip(('dx','dy'),vals))
# HARD: authored; two rational radicals with small squarefree parts and roots
# of denominators at most4. Same standard equation and root/order/double stages.
def sample_hard(rng):
 return {k:sp.Rational(rng.randint(1,3)**2*rng.choice((2,3,5,6,7)),rng.choice((4,9,16))) for k in ('dx','dy')}

OPEN='Remember that the equation of an ellipse centered at the origin with a horizontal radius of length $a$ and a vertical radius of length $b$ is given by'
GENERAL='\\frac{{x}^{2}}{{a}^{2}}+\\frac{{y}^{2}}{{b}^{2}}=1.'
def standard_equation(p):
 return r'\frac{{x}^{2}}{'+tex(p['dx'])+r'}+\frac{{y}^{2}}{'+tex(p['dy'])+'}=1'
def prompt(p,template):
 eq=standard_equation(p)
 if template=='radio_unrated':
  return 'What are the lengths of the major and minor axes of an ellipse with equation\n$\\frac{x^{2}}{'+tex(p['dx'])+'} + \\frac{y^{2}}{'+tex(p['dy'])+'} = 1$?'
 if TEMPLATES[template]=='radio':
  return 'What are the lengths of the major and minor axes of an ellipse with equation \n$'+eq+'?$'
 return 'For the ellipse '+ ('\n' if template=='blank_newline' else '')+'$'+eq+',$ find the lengths of its major and minor axes.\n\n$\\,$ The length of the major axis is \n{{field-1}}.\n\n$\\,$ The length of the minor axis is \n{{field-2}}.'
def solution(p,template):
 dx,dy=p['dx'],p['dy']; a,b=sp.sqrt(dx),sp.sqrt(dy)
 maj,mi=('a','b') if dx>dy else ('b','a'); values={'a':a,'b':b}
 def rootrow(name,n):
  radical=r'\sqrt{'+tex(n)+'}'
  result=tex(sp.sqrt(n));return name+'='+radical+('='+result if radical!=result else '')
 transition='Thus' if template in ('radio_thus','blank','blank_newline') else 'So'
 space='  ' if template=='radio_so_space' else ' '
 return (OPEN+'\n\n$$\n'+GENERAL+'\n$$\n\n \n\n'
  +'In the given equation, we have ${a}^{2}='+tex(dx)+'$ and ${b}^{2}='+tex(dy)+'.$\n\n'
  +'- Since ${a}^{2}='+tex(dx)+',$ the length of the horizontal radius must be'+space+'$'+rootrow('a',dx)+'.$\n\n'
  +'- Since ${b}^{2}='+tex(dy)+',$ the length of the vertical radius must be $'+rootrow('b',dy)+'.$\n\n'
  +transition+(', the semi-major' if transition=='Thus' else ' the semi-major')+' axis has length $'+maj+'='+tex(values[maj])+',$ and the semi-minor axis has length $'+mi+'='+tex(values[mi])+'.$\n\n'
  +'Therefore, the major axis has length $2'+maj+'=2\\cdot '+tex(values[maj])+'='+tex(2*values[maj])+',$ and the minor axis has length $2'+mi+'=2\\cdot '+tex(values[mi])+'='+tex(2*values[mi])+'.$')

def decimal_or_tex(expr,decimal=False):
 if decimal and expr.is_Rational and expr.q in (1,2):
  return str(int(expr)) if expr.q==1 else str(float(expr))
 return tex(expr)

def source_cases():return json.loads((ROOT/'source-cases.json').read_text())
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 evidence=profile is not None and profile.startswith('observed_')
 case=None
 if evidence:
  cases=[c for c in source_cases() if c.get('bank_profile')==profile]
  if not cases:raise ValueError('Unknown observed profile')
  case=cases[0]
 elif profile and profile.startswith('source_'):
  cases=[c for c in source_cases() if 'source_'+c['source_id']==profile]
  if not cases:raise ValueError('Unknown source profile')
  case=cases[0];evidence=True
 if case:
  if level!='easy':raise ValueError('Observed and unrated source replay is scoped to easy integer arithmetic')
  if template is None:template=case['template']
  if template!=case['template']:raise ValueError('Source profile owns its layout template')
 if template is None:template='blank' if field_type=='blank' else 'radio_so'
 if template not in TEMPLATES:raise ValueError('Unknown template')
 kind=TEMPLATES[template]
 if field_type and field_type!=kind:raise ValueError('Field type conflicts with template')
 if kind=='blank' and profile and not case:raise ValueError('Blanks have no choice profile')
 if kind=='radio' and profile is None:profile='authored_axes'
 if kind=='radio' and profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
 if template=='radio_unrated' and not case:raise ValueError('Unrated presentation requires source replay profile')
 attempts=1 if parameters is not None else 2000
 for _ in range(attempts):
  raw=parameters if parameters is not None else {'easy':sample_easy,'moderate':sample_moderate,'hard':sample_hard}[level](rng)
  try:
   p=validate_parameters(level,raw,evidence)
   big,small=max(p.values()),min(p.values());correct=(2*sp.sqrt(big),2*sp.sqrt(small))
   if kind=='radio':
    pairs=[tuple(sp.simplify(e.subs({U:big,V:small})) for e in pair) for pair in BANK_PROFILES[profile]]
    if any(v<=0 or v.is_real is not True for pair in pairs for v in pair):raise ValueError('Invalid complete bank')
    if len(set(pairs))!=5 or pairs.count(correct)!=1:raise ValueError('Ambiguous complete bank')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No eligible complete instance found')
 q={':question/problem':prompt(p,template)}
 # Raw attribute presence is source evidence, separate from authored completion.
 if not case or case['has_difficulty']:q[':question/difficulty']=':question.difficulty/'+level
 if not case or case['has_solution']:q[':question/worked-solution']=solution(p,template)
 fields=[]
 if kind=='radio':
  values=[]
  decimals=case.get('decimal_indices',[]) if case else []
  for i,pair in enumerate(pairs):values.append('$'+decimal_or_tex(pair[0],i in decimals)+'$ and $'+decimal_or_tex(pair[1],i in decimals)+'$')
  specs=[('selection','text',values,pairs.index(correct),not case or case['has_correct'])]
 else:
  order=case['field_order'] if case else ['field-1','field-2']
  specs=[(key,'math',[tex(correct[0 if key=='field-1' else 1])],0,True) for key in order]
 # Presentation identities use the complete learner content, not seed, profile
 # aliases, order, or unused metadata. Mathematical tasks ignore layout/banks.
 identity=digest({'version':VERSION,'question':q,'fields':sorted([(k,t,sorted(v),v[c] if hc else None) for k,t,v,c,hc in specs])})
 q[':question/id']=ident('question:'+identity)
 for key,at,vals,ci,hc in specs:
  fid=ident(identity+':field:'+key)
  choices=[{':answer/id':ident(fid+':answer:'+v),':answer/type':':answer.type/'+at,':answer/value':v} for v in vals]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
  if hc:f[':answer-field/correct']=[':answer/id',choices[ci][':answer/id']]
  if kind=='radio':rng.shuffle(choices)
  fields.append(f)
 q[':question/answer-fields']=fields
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
  'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},
   'level':level,'evidence_only':bool(case),'eligible_for_learning':not bool(case),'source':SOURCE,'source_id':case['source_id'] if case else None,'origin':'observed replay' if case else 'authored default',
   'mathematical_fingerprint':digest(sorted(str(v) for v in p.values())), 'content_fingerprint':identity,
   'recipes':RECIPES.get(profile,[]),'opaque_evidence_indices':OPAQUE.get(profile,[]),'plot_requirement':'none'}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];parts=[q[':question/problem']]
 for f in q[':question/answer-fields']:
  parts.append('\n'+f[':answer-field/key']+':')
  parts.extend('- '+a[':answer/value'] for a in f[':answer-field/choices'])
 if ':question/worked-solution' in q:parts.append('\n'+q[':question/worked-solution'])
 return '\n'.join(parts)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args();levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
