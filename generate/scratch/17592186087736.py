"""Trigonometric parametric ranges; exact, local-only generation (steps 3–7).

CLI: .venv/bin/python generate/scratch/17592186087736.py --difficulty all --count 2
Observed templates retain complete source prose and coordinate-stage sequences.
Observed residual banks are explicit replay profiles; authored method banks default.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
SNAP=json.loads((HERE/'source.json').read_text())
KP=SNAP['record']; SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
T=sp.Symbol('theta',real=True)
# a cos(theta)+h, b sin(theta)+k. Source-specific templates preserve distinct
# layouts and signed/scaled/translated row sequences; whole components are slots.
PARAMS={
'q-16201':(7,3,0,0),'q-70341':(3,2,-1,2),'q-276258':(4,2,0,0),
'q-327882':(5,7,-3,1),'q-123777':(1,1,3,-1),'q-276261':(3,-5,-2,0),
'q-327861':(6,-3,0,0),'q-327866':('-9/2','5/3',0,0),'q-327871':('5/2','3/4',0,2),
'q-327880':(4,'-7/2',1,0),'q-327884':('-4/3','5/2','1/3','-7/3'),
'q-70523':(1,6,5,-7),'q-73626':(-2,2,1,-3),'q-73632':(2,'1/2',1,'3/2'),
'q-123773':(-1,1,1,2),'q-123775':('1/2',1,0,3)}
TEMPLATES={sid:{'level':q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1],
 'kind':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1],
 'source':sid} for sid,q in SOURCES.items()}
TEMPLATES['hard-rational']={'level':'hard','kind':'blank','source':None}

def tex(x):return sp.latex(sp.sympify(x)).replace('- ','-')
def add(c):return '' if c==0 else ('+'+tex(c) if c>0 else tex(c))
def trig(fn,marker=True):return r'\operatorname{'+fn+'}'+('\u2061' if marker else '')+r'\theta'
def scaled(c,f):return ('' if c==1 else '-' if c==-1 else tex(c))+f
def formula(c,d,f,first=False):return tex(d)+scaled(c,f) if first else scaled(c,f)+(' '+add(d) if d else '')
def interval(l,u,var):return tex(l)+r'\le '+var+r'\le '+tex(u)
def result(p):
 a,b,h,k=[sp.Rational(p[v]) for v in ('a','b','h','k')]
 return (h-abs(a),h+abs(a),k-abs(b),k+abs(b))
def banktex(v):return interval(*v[:2],'x')+r',\,'+interval(*v[2:],'y')
def parse_parameters(p):
 if set(p)!=set('abhk'):raise ValueError('Parameters must have exactly a,b,h,k')
 return {v:sp.Rational(p[v]) for v in 'abhk'}
def canonical(p):return {v:str(p[v]) for v in 'abhk'}
def rows(c,d,f,var,first=False):
 out=[r'-1 & \le '+f+r' \le 1']
 if c<0:
  out += [tex(-c)+r' & \text{ }\ge '+scaled(c,f)+r' \text{ }\ge '+tex(c),
          tex(c)+r' & \le '+scaled(c,f)+r' \le '+tex(-c)]
 elif c!=1:out += [tex(-c)+r' & \le '+scaled(c,f)+r' \le '+tex(c)]
 if d!=0:
  left=tex(d)+tex(-abs(c)) if first else tex(-abs(c))+add(d)
  right=tex(d)+'+'+tex(abs(c)) if first else tex(abs(c))+add(d)
  out += [left+r' & \le '+formula(c,d,f,first)+(r' \le ' if first else r'\le ')+right]
 out += [tex(d-abs(c))+r' & \le '+var+r'\le '+tex(d+abs(c))+'.']
 return r'\begin{aligned}'+r' \\ '.join(out)+r'\end{aligned}'
def structure(sid):
 q=SOURCES[sid]; a,b,h,k=map(sp.Rational,PARAMS[sid]); marker='⁡' in q[':question/problem']
 first=sid in ('q-327884','q-73626','q-123773')
 return marker,first

def observed_text(sid,p):
 """Extract whole formula/row/conclusion slots, retaining source prose exactly.

 No numeric token replacements across prose or variable labels are performed.
 Stage renderers are identical at source and new values; regime guards keep the
 extracted omission/reversal/translation sequence directly applicable.
 """
 q=SOURCES[sid]; old=parse_parameters(dict(zip('abhk',PARAMS[sid])))
 marker,first=structure(sid); fx,fy=trig('cos',marker),trig('sin',marker)
 prompt=q[':question/problem']; solution=q.get(':question/worked-solution')
 if sid=='q-70341':
  prompt=prompt.replace('3\\cos θ - 1',scaled(p['a'],r'\cos θ')+' '+('- '+tex(-p['h']) if p['h']<0 else '+ '+tex(p['h'])))
  prompt=prompt.replace('2\\sin θ + 2',scaled(p['b'],r'\sin θ')+' + '+tex(p['k']))
  return prompt,authored_solution(p)
 for v,c,d,f,shiftfirst in [('x','a','h',fx,first),('y','b','k',fy,False)]:
  sourceformula=formula(old[c],old[d],f,shiftfirst)
  assert sourceformula in prompt,(sid,sourceformula)
  prompt=prompt.replace(sourceformula,formula(p[c],p[d],f,shiftfirst),1)
  oldrows=rows(old[c],old[d],f,v,shiftfirst)
  assert oldrows in solution,(sid,oldrows)
  solution=solution.replace(oldrows,rows(p[c],p[d],f,v,shiftfirst),1)
  # Whole interval component slots, separately for each coordinate.
  solution=solution.replace(interval(old[d]-abs(old[c]),old[d]+abs(old[c]),v),interval(p[d]-abs(p[c]),p[d]+abs(p[c]),v))
 return prompt,solution

def authored_solution(p):
 pieces=["Let's consider each variable in turn."]
 for v,c,d,fn in [('x','a','h','cos'),('y','b','k','sin')]:
  f=trig(fn,False)
  pieces += [f'- To find the range of ${v},$ notice that for $0\\le \\theta <2\\pi,$ we have $-1\\le {f}\\le 1.$ Consequently,',
  '$$\n'+rows(p[c],p[d],f,v)+'\n$$',
  'So, we can conclude that $'+interval(p[d]-abs(p[c]),p[d]+abs(p[c]),v)+'.$']
 return '\n\n'.join(pieces)

# Complete observed banks. Each tuple is (xmin,xmax,ymin,ymax). Residual
# profiles are bounded expression-pattern hypotheses, never presumed diagnoses.
def observed_bank(sid,p):
 a,b,h,k=[p[v] for v in 'abhk']; A,B=abs(a),abs(b); C=result(p); l,u,m,n=C
 if sid=='q-16201':return [(1,1,1,1),(-B,B,-A,A),C,(0,B,0,A),(0,A,0,B)]
 if sid=='q-123777':return [(-h,h,m,n),C,(-u,-l,-n,-m),(-h,h,-1,1),(l,u,-1,1)]
 if sid=='q-123773':return [(-u,-l,-n,-m),(-1,1,m,n),(-1,1,-n,-m),(l,u,-k,k),C]
 if sid=='q-123775':return [(-1/A,1/A,-n,-m),(-1/A,1/A,-k,k),(l,u,-k,k),C,(k-2*B,k,m,n)]
 if sid=='q-70341':return [(0,A-h,k,k+B),(h-A,-A-h,-B-k,0),(l,0,-k,n),C,(A+h,A-h,m,n)]
 if sid=='q-70523':return [(A,h,k-2*A,k+h),(-2*A,B-k,h-2*A,-k),C,(0,h,k,0),(-h-A,0,1,-k)]
 if sid=='q-73626':return [(B,B-k,-k-B,B-k),C,(h,2*B,k+B,B-k),(h,3*B,m,n),(l,0,m,0)]
 if sid=='q-73632':return [(-A,-h,-h,h+A),(-A-h,h,-A,h),C,(h,A+h,-h,n),(l,A,m,A+h)]
 raise ValueError('No observed radio bank for '+sid)

def authored_bank(p):
 a,b,h,k=[p[v] for v in 'abhk']; A,B=abs(a),abs(b); C=result(p)
 if h==k==0:return [C,(0,A,0,B),(-2*A,2*A,-2*B,2*B),(-A/2,A/2,-B/2,B/2),(-B,B,-A,A)]
 return [C,(-A,A,-B,B),(h-2*A,h+2*A,k-2*B,k+2*B),
 (h-A/2,h+A/2,k-B/2,k+B/2),(-C[1],-C[0],-C[3],-C[2])]

# ---- Shared exact parameters and deterministic sampling ----
def validate_parameters(name,p):
 if any(abs(p[v])>9 or sp.denom(p[v])>4 for v in 'abhk'):raise ValueError('Magnitude ≤9; denominator ≤4 required')
 if not p['a'] or not p['b']:raise ValueError('Nonzero scales required')
 if name=='hard-rational':
  if not all(p[v]<0 and sp.denom(p[v])>1 for v in 'ab') or not all(p[v]!=0 and sp.denom(p[v])>1 for v in 'hk'):
   raise ValueError('Hard requires two negative nonintegral scales and two nonintegral nonzero shifts')
  if any(all(sp.denom(z)==1 for z in result(p)[i:i+2]) for i in (0,2)):
   raise ValueError('Hard must retain fractional endpoint arithmetic in both coordinates')
  return
 old=parse_parameters(dict(zip('abhk',PARAMS[name])))
 for v in 'abhk':
  if sp.sign(p[v])!=sp.sign(old[v]):raise ValueError('Preserve source sign/zero regime')
 for v in 'ab':
  if (abs(old[v])==1)!=(abs(p[v])==1):raise ValueError('Preserve unit/nonunit scale row regime')
  if (sp.denom(old[v])==1)!=(sp.denom(p[v])==1):raise ValueError('Preserve source integer/fraction workload')
 for v in 'hk':
  if (sp.denom(old[v])==1)!=(sp.denom(p[v])==1):raise ValueError('Preserve source integer/fraction translation workload')
 # Unit-shift templates explicitly omit multiplication; easy and moderate have
 # the exact per-template number of rational operations and sign reversals.

def sample(name,rng):
 if name=='hard-rational':return {v:sp.Rational((-1 if v in 'ab' else rng.choice([-1,1]))*rng.choice([1,3,5,7,9]),rng.choice([2,3,4])) for v in 'abhk'}
 old=parse_parameters(dict(zip('abhk',PARAMS[name])))
 p={}
 for v in 'abhk':
  x=old[v]
  if x==0 or v in 'ab' and abs(x)==1:p[v]=x;continue
  if sp.denom(x)>1:val=rng.choice([sp.Rational(n,d) for n in range(1,10) for d in (2,3,4) if sp.denom(sp.Rational(n,d))>1 and (v not in 'ab' or sp.Rational(n,d)!=1)])
  else:val=sp.Integer(rng.randint(2 if v in 'ab' else 1,8))
  p[v]=sp.sign(x)*val
 return p

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def fingerprint(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def assemble(level,name,p,seed,profile):
 spec=TEMPLATES[name]; kind=spec['kind']; sid=spec['source']
 if sid:prompt,solution=observed_text(sid,p)
 else:
  prompt='Given that a curve is defined parametrically as\n\n$$\nx='+formula(p['a'],p['h'],trig('cos',False))+r',\,y='+formula(p['b'],p['k'],trig('sin',False))+r',\,0\le \theta <2\pi ,'+'\n$$\n\nwhat are the ranges of $x$ and $y?$\n\nThe range of $x$ is {{field-1}}{{field-2}}$x\\le ${{field-3}}.\n\nThe range of $y$ is {{field-4}}$\\le y${{field-5}}{{field-6}}.'
  solution=authored_solution(p)
 C=result(p)
 if kind=='radio':
  vals=[tuple(map(sp.sympify,v)) for v in (observed_bank(sid,p) if profile=='observed:'+sid else authored_bank(p))]
  if any(v[0]>v[1] or v[2]>v[3] for v in vals):raise ValueError('Whole bank rejected: reversed range bounds')
  if len(set(vals))!=5 or sum(v==C for v in vals)!=1:raise ValueError('Whole bank rejected: equivalent/correct distractor collision')
  values=[banktex(v) for v in vals]; correct=values[vals.index(C)]; layout=[('selection',values,correct)]
 else:
  values=[tex(C[0]),r'\le ',tex(C[1]),tex(C[2]),r'\le ',tex(C[3])]
  keys=[f[':answer-field/key'] for f in SOURCES[sid][':question/answer-fields']] if sid else ['field-'+str(i) for i in range(1,7)]
  layout=[(key,[values[int(key.split('-')[1])-1]],values[int(key.split('-')[1])-1]) for key in keys]
 content=fingerprint({'version':VERSION,'level':level,'template':name,'profile':profile,'p':canonical(p),'prompt':prompt,'solution':solution,'layout':layout})
 fields=[]
 for key,vals,correct in layout:
  fid=uid(content+':field:'+key)
  answers=[{':answer/id':uid(fid+':'+val),':answer/type':':answer.type/math',':answer/value':val} for val in vals]
  cid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
  if kind=='radio':random.Random(seed).shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]})
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},
 'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
 'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':canonical(p),'bank_profile':profile,
 'bank_origin':'observed expression-pattern replay' if profile and profile.startswith('observed:') else 'authored method-based' if kind=='radio' else 'observed' if sid else 'authored missing level',
 'distractor_recipes':(['correct range','restrict both trig values to [0,1]','double both amplitudes','halve both amplitudes','swap amplitudes'] if kind=='radio' and profile=='authored:full-period' and p['h']==p['k']==0 else ['correct range','omit both shifts','double both amplitudes','halve both amplitudes','negate both complete ranges'] if kind=='radio' and profile=='authored:full-period' else ['complete observed expression-pattern bank; see template-extraction.md for supported versus underidentified operations'] if kind=='radio' else []),
 'content_fingerprint':content,'parameter_fingerprint':fingerprint({'x':sp.srepr(p['a']*sp.cos(T)+p['h']),'y':sp.srepr(p['b']*sp.sin(T)+p['k']),'domain':'0<=theta<2*pi'}),
 'source_analysis':{'database':SNAP['database'],'basis':SNAP['basis'],'lineage':SNAP['lineage'],'question_ids':[sid] if sid else ['q-327884','q-327880']},
 'authored_extension':name=='hard-rational' or sid=='q-70341','plot_rating':'none','plot_assets':{},'domain':'0 <= theta < 2*pi','sympy_version':sp.__version__}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if profile and profile.startswith('observed:'):
  owner=profile.split(':')[1]
  if template and template!=owner:raise ValueError('Profile belongs to another template')
  template=owner
 eligible=[n for n,s in TEMPLATES.items() if s['level']==level and (field_type is None or s['kind']==field_type)]
 if not eligible or template is not None and template not in eligible:raise ValueError('Unsupported level/template/field combination')
 rng=random.Random(seed); name=template or rng.choice(eligible); kind=TEMPLATES[name]['kind']
 profile=profile or ('authored:full-period' if kind=='radio' else None)
 if profile not in (None,'authored:full-period','observed:'+name):raise ValueError('Unsupported profile')
 if kind=='blank' and profile is not None:raise ValueError('Blanks have no bank profile')
 for _ in range(128):
  p=parse_parameters(parameters) if parameters is not None else sample(name,rng)
  try:validate_parameters(name,p)
  except ValueError:
   if parameters is not None:raise
   continue
  try:return assemble(level,name,p,seed,profile)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('No valid whole instance after 128 attempts')

# ---- EASY: source scale-only, unit translations, signed/rational variants ----
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# ---- MODERATE: source signed scale plus translation, exact fractions ----
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# ---- HARD: authored two reversals + four rational endpoint additions ----
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];out=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  out.append('**'+f[':answer-field/key']+'**')
  for a in f[':answer-field/choices']:
   out.append('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 out += ['', '**Worked solution**','',q[':question/worked-solution']]
 return '\n'.join(out)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile');ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
 if args.count<1 or args.difficulty=='all' and (args.template or args.profile):ap.error('Positive count and specific difficulty for template/profile')
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
