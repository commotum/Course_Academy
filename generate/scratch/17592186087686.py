#!/usr/bin/env python3
"""Parallel slope-intercept recognition, frozen math basis 1356.

Direct coefficient completion reads m from y=mx+b; it never solves an equation
for a parameter. Authored line-choice identification uses the identical criterion.
The three unrated originals have no keys or solutions: public raw profiles retain
these omissions, while completed profiles infer answers and reuse canonical prose.
Only raw_scalar_radio / completed_scalar_radio carry the opaque historical bank;
they are evidence-only and never enter random practice. See evidence/README.md.
No database writes, plots, standard-form isolation, or perpendicular branches.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186087686
KP_UUID='353a2fb8-5677-5047-8f39-595f43d9eeb9'
TITLE='Identifying Parallel Lines Given in Slope-Intercept Form'
VERSION='parallel-slope-intercept-v1'
HERE=Path(__file__).with_suffix('')
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING='For two lines to be parallel, they must have the same slope.'
READING='Both lines are in slope-intercept form, so we can pick out the slope of each equation by looking at the $x$-coefficient.'
TEMPLATES=('coefficient_blank','coefficient_radio','line_choice')
PROFILES=('default','raw_blank_integer','raw_blank_fraction','raw_scalar_radio','completed_blank_integer','completed_blank_fraction','completed_scalar_radio')
PROFILE_SOURCE={'blank_integer':17592186088072,'blank_fraction':17592186088073,'scalar_radio':17592186088176}
# Source identity values are provenance, not mathematical or answer lookup tables.
SOURCE_IDENTITIES={
 'blank_integer':('8abba1b4-cf74-5469-9ad3-fd07f923a0f6','q-215719','c12cfecd-6908-57f1-91b4-ad6618d6b44c',17592186085140),
 'blank_fraction':('570f0d0a-a716-58d6-9635-7e7137caf659','q-215726','51594eb3-a520-5a77-a55d-36ea7b41a396',17592186085141),
 'scalar_radio':('9944ab8b-e161-5e8d-b3cc-b5e68c5e2162','q-44314','ae270df8-9bf6-5641-82b1-ee2708e40405',17592186085710)}

def canonical_json(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(x):return hashlib.sha256(canonical_json(x).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+x))
def tex(v):
 v=sp.Rational(v)
 if v.q==1:return str(v)
 return ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def line(m,b,source_spacing=False):
 """All prompts remain y=mx+b, with source coefficient +1/-1 conventions."""
 m=str(m) if isinstance(m,str) and m in ('m','c','k') else tex(m)
 if source_spacing:
  return 'y ='+(' ' if not m.startswith('-') else '')+m+'x '+('+' if b>=0 else '-')+' '+tex(abs(b))
 coef='' if m=='1' else '-' if m=='-1' else m
 return 'y='+coef+'x'+('+' if b>=0 else '-')+tex(abs(b))

def domains(level):
 # Easy integer reading, moderate signed unit fractions, hard general reduced
 # rational reading. Number-form tiers are authored, never observed labels.
 if level=='easy':return [sp.Integer(n) for n in range(-12,13) if n]
 if level=='moderate':return [sp.Rational(s,d) for s in (-1,1) for d in range(2,13)]
 if level=='hard':return sorted({sp.Rational(s*n,d) for s in (-1,1) for n in range(2,13) for d in range(2,13) if sp.gcd(n,d)==1})
 raise ValueError('unknown difficulty')

def parameters_checked(level,p,evidence=False):
 if set(p)!={'slope','b','k'}:raise ValueError('parameters require exactly slope,b,k')
 try:m,b,k=map(sp.Rational,(p['slope'],p['b'],p['k']))
 except Exception as exc:raise ValueError('exact rational parameters required') from exc
 if m not in domains(level):raise ValueError('slope violates level number-form bounds')
 if b.q!=1 or k.q!=1 or max(abs(b),abs(k))>12:raise ValueError('intercepts must be integers of magnitude <=12')
 if b==k:raise ValueError('identical lines at the inferred slope are excluded')
 return m,b,k

def bank(template,m,b,k,profile):
 """Complete operation banks, selected before parameters, never pooled."""
 if template=='coefficient_blank':return [tex(m)]
 if profile.endswith('scalar_radio'):
  # Historical expression profile b,b/m,1,m,m/b. Intent underdetermined.
  if b==0:raise ValueError('historical ratio bank requires nonzero b')
  vals=[b,b/m,sp.Integer(1),m,m/b]
 elif template=='coefficient_radio':
  # coefficient sign loss/reversal, intercept confusion for either line,
  # and reciprocal of the coefficient. No arbitrary additive perturbations.
  vals=[m,-m,b,k,1/m]
 else:
  # Same complete error operations as scalar choices, rendered as lines.
  vals=[m,-m,b,k,1/m]
 if len(set(vals))!=len(vals):raise ValueError('whole bank rejected: equivalent scalar slopes')
 if template=='line_choice':
  # Correct offset is different from target; each other bank slope differs.
  return [line(v,k) for v in vals]
 return [tex(v) for v in vals]

def solution(template,m,b,k,values):
 first,second=line(m,b),line('m',k)
 if template!='line_choice':
  return OPENING+'\n\n'+READING+'\n\n- The slope of the line $'+first+'$ is $'+tex(m)+'$.\n- The slope of the line $'+second+'$ is $m$.\n\nBecause the slopes must be the same, we must have $m='+tex(m)+'$.'
 # Canonical operator/slope-reading prose, adapted only to plural answer bank.
 parts=[OPENING,'All the lines are in slope-intercept form, so we can pick out the slope of each equation by looking at the $x$-coefficient.',
        '- The slope of the line $'+first+'$ is $'+tex(m)+'$.']
 for value,v in zip(values,[m,-m,b,k,1/m],strict=True):parts[-1]+='\n- The slope of the line $'+value+'$ is $'+tex(v)+'$.'
 parts.append('The only choice with the same slope is $'+values[0]+'$. Its $y$-intercept differs from that of the given line, so the two lines are parallel.')
 return '\n\n'.join(parts)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 profile=profile or 'default'
 if profile not in PROFILES:raise ValueError('unknown profile')
 raw=profile.startswith('raw_'); evidence=profile!='default'
 family=profile.split('_',1)[1] if evidence else None
 expected='coefficient_radio' if family=='scalar_radio' else 'coefficient_blank' if evidence else None
 if expected and template and expected!=template:raise ValueError('profile/template mismatch')
 template=template or expected
 rng=random.Random(seed)
 # Select supported family BEFORE parameter sampling; no hidden source-only masks.
 if template is None:
  choices=[t for t in TEMPLATES if field_type is None or ('blank' if t=='coefficient_blank' else 'radio')==field_type]
  if not choices:raise ValueError('unsupported field type')
  template=rng.choice(choices)
 if template not in TEMPLATES:raise ValueError('unknown template')
 kind='blank' if template=='coefficient_blank' else 'radio'
 if field_type and field_type!=kind:raise ValueError('field type/template mismatch')
 if evidence:
  valid_level='moderate' if family=='blank_fraction' else 'easy'
  if level!=valid_level:raise ValueError('source-profile authored tier mismatch')
 # Explicit invalid inputs are never silently changed. Random invalid whole
 # instances are resampled, preserving family/profile selection.
 for attempt in range(1000):
  p=parameters if parameters is not None else {'slope':str(rng.choice(domains(level))),'b':rng.randint(-12,12),'k':rng.randint(-12,12)}
  try:
   m,b,k=parameters_checked(level,p,evidence)
   values=bank(template,m,b,k,profile)
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no eligible bank instance')
 p={'slope':str(m),'b':str(b),'k':str(k)}
 if evidence:
  first,second=line(m,b,True),line('m',k,True)
  if family=='scalar_radio':prompt=f'The lines ${first}$ and ${second}$ are parallel. The value of $m =$'
  else:prompt=f'The lines ${first}$ and ${second}$ are parallel. What is the value of $m$?$m =$\n{{{{field-1}}}}'
 else:
  prompt=(f'Which of the following lines is parallel to ${line(m,b)}$?' if template=='line_choice' else
          f'The lines ${line(m,b)}$ and ${line("m",k)}$ are parallel. What is the value of $m$?')
  if kind=='blank':prompt+='\n\n$m =$\n{{field-1}}'
 solved=solution(template,m,b,k,values)
 key='field-1' if kind=='blank' else 'selection'
 # Mathematical workload: offsets only establish distinct lines and do not
 # change coefficient reading. Line-choice banks contribute actual compared
 # slopes; offsets, option order, profiles and notation aliases do not.
 task={'assessment':'line_choice' if template=='line_choice' else 'coefficient_read',
       'number_form':level,'target_slope':str(m)}
 if template=='line_choice':task['compared_slopes']=sorted([str(v) for v in (m,-m,b,k,1/m)])
 content={'version':VERSION,'difficulty':None if raw else level,'prompt':prompt,
          'solution':None if raw else solved,'kind':kind,'key':key,'bank':[] if raw and kind=='blank' else sorted(values),'correct':None if raw else (values[3] if family=='scalar_radio' else values[0])}
 identity=digest(content); fid=uid(identity+':'+key)
 answers=[]
 if not(raw and kind=='blank'):
  answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
 if answers:f[':answer-field/choices']=answers
 if not raw:
  correct=values[3] if family=='scalar_radio' else values[0]
  f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]
 rng.shuffle(answers)
 q={':question/id':uid(identity),':question/problem':prompt,':question/answer-fields':[f]}
 if not raw:
  q[':question/difficulty']=':question.difficulty/'+level
  q[':question/worked-solution']=solved
 if raw:
  # Preserve source non-mathematical attributes and their presence too; IDs are
  # generated except :db/id, which is retained solely as local evidence.
  _,ma,_,dbfield=SOURCE_IDENTITIES[family]
  q[':db/id']=PROFILE_SOURCE[family];q[':question/math-academy-id']=ma
  f[':db/id']=dbfield
  if kind=='radio':
   # Original answer database IDs travel with their parameterized operation slot.
   for a in answers:a[':db/id']=17592186085711+values.index(a[':answer/value'])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
  'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'difficulty':level,
   'source':PROVENANCE,'source_id':PROFILE_SOURCE.get(family),'evidence_only':raw or family=='scalar_radio',
   'eligible_for_learning':not raw and family!='scalar_radio','inferred_completion':evidence and not raw,
   'level_authorship':'authored number-form tier; sources unrated','mathematical_fingerprint':digest(task),
   'content_identity':identity,'task':task,'python':sys.version.split()[0],'sympy':sp.__version__,
   'scope':'compare already-visible slope-intercept x-coefficients only; distinct intercepts',
   'bank_recipes':(['b','b/m','1','m','m/b; opaque intent'] if family=='scalar_radio' else ['m','-m','b','k','1/m'] if kind=='radio' else ['m'])}}

# EASY: signed nonzero integer x-coefficient, magnitude <=12, no fraction reading.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: signed reduced unit fraction x-coefficient, denominator 2..12.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: signed reduced nonunit rational x-coefficient; numerator/denominator 2..12.
# This is an authored number-form tier, not an observed MA hard rating.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
 out=[f"Generated {g['difficulty']} — {g['template']} / {g['profile']}",q[':question/problem']]
 out += ['$'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[])]
 if ':answer-field/correct' in f:out += ['Correct: $'+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])+'$']
 out += [q.get(':question/worked-solution','Raw source evidence: solution and correct designation absent.')]
 return '\n\n'.join(out)
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
 parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile',choices=PROFILES)
 parser.add_argument('--field-type',choices=['blank','radio']);parser.add_argument('--format',choices=['markdown','json'],default='markdown')
 a=parser.parse_args()
 if a.count<1:parser.error('count must be positive')
 try:records=[generate(l,a.seed+i,a.template,a.field_type,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 except ValueError as exc:parser.error(str(exc))
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
