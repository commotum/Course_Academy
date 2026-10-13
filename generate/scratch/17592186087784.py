#!/usr/bin/env python3
"""Parametrizing Part of a Circle — local step 3–7 generator, no database writes.

Exact angle-domain answers are derived from a common x=r*cos(theta)+h,
y=r*sin(theta)+k parametrization, always unit angular speed, counterclockwise.
Eleven extracted presentation templates and eleven whole observed radio banks
preserve 15 sources; one missing designation/solution is explicitly repaired.
Observed profiles are categorical angular-recognition banks, not inferred
student-error algorithms. Their eligible arc is fixed, while r/center vary.
Authored defaults vary the assessed angular interval using familiar angles;
all options are computed by complete half-arc/full/complement operations.
Profile, layout, and seed are excluded from canonical mathematical fingerprints.
Version, full displayed prompt, solution, and owned bank determine content IDs.

Run with .venv/bin/python; Matplotlib uses an already-cached renderer runtime.
API explicit inputs are validated and never silently altered or resampled.
See evidence/contract.json, classification.md and README.md for scope and tests.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186087784
KP_UUID='1d81c7ff-8459-5559-bfae-c2a9c3bc739e'
TITLE='Parametrizing Part of a Circle'
VERSION='circle-arc-1'
HERE=Path(__file__).resolve().parent/str(KP_ID)
CONTRACT=json.loads((HERE/'contract.json').read_text())
TEMPLATES=CONTRACT['templates']
BANK_PROFILES=CONTRACT['profiles']
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+s))
def angle(c):
 c=sp.Rational(c)
 if c==0:return '0'
 n,d=c.p,c.q
 sign='-' if n<0 else '';n=abs(n)
 top=('' if n==1 else str(n))+r'\pi '
 return sign+top if d==1 else sign+r'\frac{'+top+'}{'+str(d)+'}'
def interval(a,b,close=']'):
 return '['+angle(a)+','+angle(b)+close

def validate_parameters(name,p):
 if set(p)!={'r','h','k','start','end'}:raise ValueError('Parameters must be r,h,k,start,end')
 if any(type(p[x]) is not int for x in ('r','h','k')):raise ValueError('r,h,k must be integers')
 if not 1<=p['r']<=8 or any(abs(p[x])>8 for x in ('h','k')):raise ValueError('Radius 1..8, shifts -8..8')
 a,b=sp.Rational(p['start']),sp.Rational(p['end'])
 if not (0<=a<b<=2):raise ValueError('Require 0 <= start < end <= 2 (multiples of pi)')
 t=TEMPLATES[name]
 if t['centered']:
  if p['h']==p['k']==0:raise ValueError('Hard sources require a translated center')
 elif p['h'] or p['k']:raise ValueError('Origin template cannot introduce translations')
 if t['level']=='easy' and a!=0:raise ValueError('Easy scope starts at zero')
 noun='quarter' if 'quarter' in name and 'threequarter' not in name else 'threequarter' if 'threequarter' in name else 'semi' if 'semi' in name else 'arc'
 spans={'quarter':sp.Rational(1,2),'threequarter':sp.Rational(3,2),'semi':sp.Integer(1)}
 if noun in spans and b-a!=spans[noun]:raise ValueError('Arc extent must match the printed circle fraction')
 if a.q not in (1,2,4,6) or b.q not in (1,2,4,6):raise ValueError('Use familiar multiples of pi/2, pi/4 or pi/6')
 if t['level']=='moderate' and a==0:raise ValueError('Moderate sources have nonzero angular start')
 return {'r':p['r'],'h':p['h'],'k':p['k'],'start':str(a),'end':str(b)}

def sample(name,rng,profile):
 t=TEMPLATES[name]
 if profile and profile in BANK_PROFILES:a,b=BANK_PROFILES[profile]['required_interval']
 elif t['level']=='easy':
  a='0';b=rng.choice(['1/4','3/4','5/4','7/6']) if 'arc' in name else t['default_end']
 elif t['level']=='moderate':
  if 'arc' in name:a,b=rng.choice([('1','2'),('1/2','3/2'),('1/4','5/4'),('3/4','7/4')])
  else:a=rng.choice(['1/2','1','3/2']);b=str(sp.Rational(a)+sp.Rational(1,2))
 else:
  if 'threequarter' in name:a,b=rng.choice([('0','3/2'),('1/2','2')])
  else:a=rng.choice(['0','1/2','1','3/2']);b=str(sp.Rational(a)+sp.Rational(1,2))
 r=rng.randint(1,8);h=k=0
 if t['centered']:
  while h==k==0:h,k=rng.randint(-6,6),rng.randint(-6,6)
 return {'r':r,'h':h,'k':k,'start':a,'end':b}

def equations(p,style):
 r,h,k=p['r'],p['h'],p['k'];c='' if r==1 else str(r)
 def shift(v):return ('+' if v>0 else '-')+str(abs(v)) if v else ''
 if style=='compact':return f'x = {c}'+r'\cos θ'+shift(h)+f', y = {c}'+r'\sin θ'+shift(k)
 x=c+r'\operatorname{cos}⁡\theta'+(' '+shift(h) if h else '')
 y=c+r'\operatorname{sin}⁡\theta'+(' '+shift(k) if k else '')
 return 'x='+x+r' ,\,y='+y if not h else 'x='+x+r',\,y='+y

def render_plots(p):
 """Render exactly this instance through Matplotlib, with no sampling."""
 key=digest({'p':p,'plot_version':4})[:24];out=HERE/'plots'/key;out.mkdir(parents=True,exist_ok=True)
 files={role:str(out/(role+'.png')) for role in ('prompt','solution')}
 if not all(Path(f).exists() for f in files.values()):
  data={'parameters':p,'output_dir':str(out)}
  subprocess.run([sys.executable,str(HERE/'renderer.py')],input=json.dumps(data),text=True,check=True,stdout=subprocess.DEVNULL)
 return {role:{'path':str(Path(path).resolve()),'role':role,'renderer':'matplotlib','parameter_fingerprint':digest(p)} for role,path in files.items()}

def fill(text,tokens):
 for k,v in tokens.items():text=text.replace('{'+k+'}',str(v))
 return text

def bank(p,profile):
 a,b=sp.Rational(p['start']),sp.Rational(p['end']);correct=(a,b,']')
 if profile in BANK_PROFILES:
  prof=BANK_PROFILES[profile]
  if [str(a),str(b)]!=prof['required_interval']:raise ValueError('Explicit arc not eligible for observed whole bank')
  opts=[(sp.Rational(x),sp.Rational(y),c) for x,y,c in prof['options']];prefix=prof['prefix']
 else:
  mid=(a+b)/2
  opts=[correct,(a,mid,']'),(mid,b,']'),(sp.Integer(0),sp.Integer(2),')'),(sp.Integer(0),a,']') if a>0 else (b,sp.Integer(2),']')]
  prefix='none' if TEMPLATES[profile.removeprefix('authored-')]['level'] in ('moderate','hard') else 'theta'
 if len(opts)!=5 or len(set(opts))!=5 or any(x>=y for x,y,c in opts):raise ValueError('Whole bank is invalid or colliding')
 if sum(o==correct for o in opts)!=1:raise ValueError('Whole bank lacks one unique correct domain')
 vals=[]
 for x,y,c in opts:
  v=interval(x,y,c)
  if prefix=='theta':v=r'\theta \in '+v
  if prefix=='unicode':v='θ ∈ '+v.replace(r'\pi ','π')
  vals.append(v)
 return vals,opts.index(correct),[{'start':str(x),'end':str(y),'right_closed':c==']'} for x,y,c in opts]

# EASY: origin, angular start zero, familiar endpoint angle cue or cardinal endpoint.
# MODERATE: origin, nonzero start, identify both endpoint angles against x-axis.
# HARD: same angular restriction for translated circles, reference through center.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile in BANK_PROFILES:
  pn=BANK_PROFILES[profile]['template']
  if template and template!=pn:raise ValueError('Profile/template mismatch')
  template=pn
 eligible=[n for n,t in TEMPLATES.items() if t['level']==level and (field_type is None or field_type==t['kind'])]
 if not eligible or template and template not in eligible:raise ValueError('Unsupported template/field type/level combination')
 rng=random.Random(seed)
 # An explicit mathematical instance must not choose presentation randomly.
 name=template or (eligible[0] if parameters is not None else rng.choice(eligible));t=TEMPLATES[name]
 if t['kind']=='blank' and profile is not None:raise ValueError('Blank has no bank profile')
 if profile is not None and profile not in BANK_PROFILES and profile!='authored-'+name:raise ValueError('Unknown profile')
 profile=profile or ('authored-'+name if t['kind']=='radio' else None)
 p=validate_parameters(name,parameters if parameters is not None else sample(name,rng,profile))
 plots=render_plots(p)
 tokens={**p,'equations':equations(p,t['eq_style']),'interval':interval(p['start'],p['end']),**{role+'_plot':'![]('+asset['path']+')' for role,asset in plots.items()}}
 problem=fill(t['problem'],tokens);solution=fill(t['solution'],tokens)
 values,index,domains=bank(p,profile) if profile else (None,None,None)
 rawfields=[]
 for key in t['field_keys']:
  rawfields.append({'key':key,'kind':t['kind'],'values':values if values else [angle(p['start'] if key=='field-1' else p['end'])],'correct':index if values else 0})
 # Includes complete banks and fixed prose; excludes option order and seed.
 content=digest({'version':VERSION,'problem':problem,'solution':solution,'fields':[{'key':f['key'],'kind':f['kind'],'values':sorted(f['values']),'correct':f['values'][f['correct']]} for f in rawfields]})
 qid=uid(content);fields=[]
 for f in rawfields:
  fid=uid(qid+':'+f['key']);choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in f['values']]
  fields.append({':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/'+f['kind'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[f['correct']][':answer/id']]})
 task={'curve':[p['h'],p['k'],p['r']],'parametrization':['cos','sin'],'domain':[p['start'],p['end'],True,True],'orientation':'counterclockwise','angular_speed':1,'task':'identify arc parameter domain'}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':profile,'origin':'observed' if profile in BANK_PROFILES else 'authored bank/parameter variation','parameters':p,'source':PROVENANCE,'source_questions':t['sources'],'mathematical_fingerprint':digest(task),'parameter_fingerprint':digest(task),'content_identity':content,'mathematics':task,'choice_domains':domains,'plots':plots,'solution_stages':['full-circle formula','identify radius/center','central-angle reference','restrict interval','parametric equations with domain'],'exact_answer_compatibility':'No rounding requirement. Original wording retained. Two-blank fields grade endpoints separately.'}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines.append('Field `'+f[':answer-field/key']+'`:')
  for a in f[':answer-field/choices']:lines.append('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 lines+=['','**Worked solution**','',q[':question/worked-solution']]
 return '\n'.join(lines)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 rs=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
