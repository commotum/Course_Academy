#!/usr/bin/env python3
"""Normal lines, math snapshot 1356. Read README and extraction beside this script.

Source masks retain each family's complete operative solution, including its
cancellation/product/reciprocal and rearrangement stages. Translation changes
coordinates and line intercepts, with source algebra shown in translated
coordinates. It does not create additional recovered templates or skills.
Historical whole banks are public evidence-only profiles; normal radio banks
use the assessed slope/point operations. No engine or database mutations.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP=17592186083245
HERE=Path(__file__).with_suffix('')
CAP=json.loads((HERE/'source.json').read_text())
SOURCE=CAP['record']; QUESTIONS=SOURCE[':knowledge-point/questions']
VERSION='normal-parametric-1-format-audit-9837-v1'
t,x,y=sp.symbols('t x y', real=True)
# Each source family remains separate: its fixed workload and solution mask are
# taken from that source, rather than replaced by a generic CAS stage sequence.
FAMILIES={
 'quartic_axis':('hard',0,t**4+t,t**2,-1,'x'),
 'log_sine':('moderate',1,sp.log(sp.sin(t)),1/sp.sin(t),sp.pi/2,None),
 'log_power':('moderate',2,sp.log(t**2),2*t**3-3*t,1,None),
 'cubic_axis':('hard',3,t**2+t/2+sp.Rational(1,2),t**3+7*t**2+8*t,-1,'x'),
 'sixth_axis':('hard',4,7*t**2-9*t,t**6+2*t**2,1,'y'),
 'cubic_linear':('moderate',5,t**3-3*t,2-t,0,None),
 'exponential':('moderate',6,sp.exp(t),2*t*sp.exp(t)-2*sp.exp(t),1,None),
 'quartic_cubic':('moderate',7,t**4-3*t**2,2*t**3-t,1,None),
}
NAMESPACE=uuid.UUID(SOURCE[':knowledge-point/id'])

def tex(v):return sp.latex(sp.simplify(v)).replace(r'\log',r'\ln')
def signed_append(expr,v):
 v=sp.sympify(v)
 return expr if v==0 else expr+('+' if v>0 else '-')+tex(abs(v))
def translated_symbol(name,v):
 return name if v==0 else '('+name+('-' if v>0 else '+')+tex(abs(v))+')'
def translate_math(body,k,h):
 # Complete coordinate symbols only: exclude derivatives, d/dx and subscripted
 # point-variable notation. This function operates only on known line blocks.
 body=re.sub(r'(?<![A-Za-z\\])x(?![A-Za-z_\'′])',lambda _:translated_symbol('x',k),body)
 body=re.sub(r'(?<![A-Za-z\\])y(?![A-Za-z_\'′])',lambda _:translated_symbol('y',h),body)
 return body

def coordinate_block(body,k,h):
 """Add translation to every individual source substitution/evaluation stage."""
 pieces=re.split(r'(\\\\)',body)
 for j,row in enumerate(pieces):
  match=re.search(r'([xy])\s*&\s*=',row)
  if not match:continue
  shift=k if match[1]=='x' else h
  if not shift:continue
  prefix=row[:match.end()]; tail=row[match.end():]
  end=''
  if r'\end{aligned}' in tail:tail,end=tail.split(r'\end{aligned}',1);end=r'\end{aligned}'+end
  # Trailing punctuation belongs outside each complete mathematical component.
  terms=tail.split('='); out=[]
  for term in terms:
   m=re.match(r'(.*?)([,.]?\s*)$',term,re.S); expr,punct=m.groups()
   out.append(signed_append(expr,shift)+punct)
  pieces[j]=prefix+'='.join(out)+end
 return ''.join(pieces)

def source_solution(q,k,h,axis,data,raw=False):
 X0,Y0,m,mn,intercept=data
 original=q.get(':question/worked-solution')
 if original is None:return None
 sections=re.split(r'(\$\$.*?\$\$)',original,flags=re.S)
 blocks=[i for i,s in enumerate(sections) if s.startswith('$$')]
 sections[blocks[0]]='$$'+coordinate_block(sections[blocks[0]][2:-2],k,h)+'$$'
 # Last normal-equation block is the 6th displayed block in every practice
 # family. It retains every source point-slope/distribution/collection row.
 sections[blocks[5]]='$$'+translate_math(sections[blocks[5]][2:-2],k,h)+'$$'
 if axis and (k or h):
  X0,Y0,m,mn,intercept=data
  if axis=='x':
   sections[blocks[6]]='$$\n'+r'\begin{aligned}0-('+tex(Y0)+') & ='+tex(mn)+r'(x-('+tex(X0)+r')) \\ '+tex(mn)+r'(x-('+tex(X0)+r')) & ='+tex(-Y0)+r' \\ x-('+tex(X0)+r') & ='+tex(-Y0/mn)+r' \\ x & ='+tex(intercept)+r'.\end{aligned}'+'\n$$'
  else:
   sections[blocks[6]]='$$\n'+r'\begin{aligned}y & ='+tex(mn)+r'(0-('+tex(X0)+'))'+('+' if Y0>=0 else '-')+tex(abs(Y0))+r' \\ y & ='+tex(intercept)+r'.\end{aligned}'+'\n$$'
 # Mask complete coordinate tuples in prose only; source point notation differs
 # from normal displayed equations so it receives its own complete-component mask.
 _,_,baseX,baseY,T,_=FAMILIES[next(n for n,d in FAMILIES.items() if QUESTIONS[d[1]] is q)]
 a,b=sp.simplify(baseX.subs(t,T)),sp.simplify(baseY.subs(t,T))
 for i,s in enumerate(sections):
  if s.startswith('$$'):continue
  # Only point tuples (not function arguments) occur in source prose.
  oldpoint='('+tex(a)+','+tex(b)+')'
  s=s.replace(oldpoint,'('+tex(a+k)+','+tex(b+h)+')')
  if axis:
   oldcoord=(tex(data[4]-k+h/mn)+r',\,0') if axis=='x' else '0,'+r'\,'+tex(data[4]-h+mn*k)
   newcoord=(tex(data[4])+r',\,0') if axis=='x' else '0,'+r'\,'+tex(data[4])
   s=s.replace(oldcoord,newcoord)
  if not raw and q[':question/math-academy-id']=='q-122931':s=s.replace('equation of the tangent line','equation of the normal')
  sections[i]=s
 if not raw and q[':question/math-academy-id']=='q-15570':
  sections.insert(0,'The parameter derivatives both vanish here. The curve lies on $'+translated_symbol('y',h)+'=e^{-'+translated_symbol('x',k)+'}$ with $x\\leq '+str(k)+'$, so its endpoint tangent is obtained by the limiting derivative ratio.\n\n')
 return ''.join(sections)

def data_for(family,k,h):
 level,idx,X,Y,T,axis=FAMILIES[family]
 X0=sp.simplify(X.subs(t,T)+k);Y0=sp.simplify(Y.subs(t,T)+h)
 ratio=sp.simplify(sp.diff(Y,t)/sp.diff(X,t))
 m=sp.simplify(ratio.subs(t,T))
 if m.has(sp.nan,sp.zoo):m=sp.limit(ratio,t,T)
 if m==0 or not m.is_finite:raise ValueError('Horizontal/vertical normal branches belong to sibling KPs')
 mn=sp.simplify(-1/m)
 intercept=sp.simplify(X0-Y0/mn) if axis=='x' else sp.simplify(Y0-mn*X0)
 return X0,Y0,m,mn,intercept

def prompt(q,k,h,raw=False):
 text=q[':question/problem']
 # Replace the entire coordinate equation RHS in the captured displayed block.
 # Source finite formula strings are fixed complete masks, never global short
 # coefficient substitutions. The original formatting survives zero shifts.
 match=re.search(r'(x\s*=)(.*?)(,\\,y=|, y =|,\\quad y=)(.*?)(,\\,|, -)',text,re.S)
 if not match:raise ValueError('Unknown captured formula mask')
 left,XR,sep,YR,end=match.groups()
 text=text[:match.start()]+left+signed_append(XR,k)+sep+signed_append(YR,h)+end+text[match.end():]
 if not raw:text=text.replace('Do not round the answers.','Give exact answers.')
 if not raw and q[':question/math-academy-id']=='q-15558':
  text=re.sub(r'!\[\]\([^\n]+\)\n\n','',text).replace('The curve shown above','A curve')
 return text

def equation(mn,X0,Y0):return 'y='+tex(sp.expand(mn*(x-X0)+Y0))
def historical_bank(q,k,h,axis,mn):
 banks=[]
 for field in q[':question/answer-fields']:
  vals=[]
  for ans in field[':answer-field/choices']:
   v=ans[':answer/value']
   if axis and field[':answer-field/type'][':db/ident'].endswith('/blank'):
    vals.append(v) # Replaced with derived coordinate below.
   elif axis:
    # Legacy coordinate banks are opaque. Their whole observed pattern is
    # translated as geometry; no claim of inferred learner error operations.
    original=sp.Rational(re.search(r'frac\{(\d+)\}\{(\d+)\}',v)[1],re.search(r'frac\{(\d+)\}\{(\d+)\}',v)[2])
    vals.append(v if not(k or h) else '('+tex(original+k-h/mn)+', 0)')
   else:
    lhs,rhs=v.split('=');vals.append(v if not(k or h) else lhs+'='+signed_append(translate_math(rhs,k,0),h))
  banks.append(vals)
 return banks

def make_record(level,family,p,profile,problem,solution,banks,correct,keys,kind,rawq=None,extra=None):
 if rawq is None:problem=_ca_problem(problem);solution=_ca_prose(solution);banks=[_ca_values(b)for b in banks]
 material={'version':VERSION,'level':level if rawq is None or ':question/difficulty' in rawq else None,'problem':problem,'solution':solution,'bank':[(key,sorted(bank)) for key,bank in zip(keys,banks)],'correct':correct}
 digest=hashlib.sha256(json.dumps(_ca_material(material),sort_keys=True).encode()).hexdigest();qid=str(uuid.uuid5(NAMESPACE,digest))
 fields=[]
 for key,bank,corr in zip(keys,banks,correct):
  fid=str(uuid.uuid5(uuid.UUID(qid),key)); choices=[]
  for value in bank:
   aid=str(uuid.uuid5(uuid.UUID(fid),value));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  random.Random(extra['seed']).shuffle(choices)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
  if corr is not None:f[':answer-field/correct']=[':answer/id',str(uuid.uuid5(uuid.UUID(fid),bank[corr]))]
  fields.append(f)
 question={':question/id':qid,':question/problem':problem,':question/answer-fields':fields}
 if rawq is None or ':question/difficulty' in rawq:question[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:question[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':family,'profile':profile,'parameters':p,'seed':extra['seed'],'source':{k:CAP[k] for k in ('database','basis','lineage')},'source_id':extra.get('source_id'),'evidence_only':profile=='observed','eligible_for_learning':profile!='observed','mathematical_fingerprint':hashlib.sha256(json.dumps([level,family,p],sort_keys=True).encode()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__}}

# EASY: authored missing-level design. Linear x and single quadratic y, t=±1;
# two one-term derivative evaluations then negative reciprocal and point-slope.
def easy_instance(seed,p=None,profile=None):
 rng=random.Random(seed)
 if profile not in (None,'method'):raise ValueError('Easy has only authored method profile')
 if p is None:
  a,b=rng.choice([(a,b) for a in range(1,5) for b in range(1,5) if a!=2*b])
  p={'a':a,'b':b,'k':rng.randint(-4,4),'h':rng.choice([-4,-3,-2,-1,1,2,3,4]),'t0':rng.choice([-1,1])}
 if set(p)!={'a','b','k','h','t0'} or not all(isinstance(v,int) for v in p.values()) or not(1<=p['a']<=4 and 1<=p['b']<=4 and abs(p['k'])<=4 and 1<=abs(p['h'])<=4 and abs(p['t0'])==1):raise ValueError('Easy workload bounds')
 if p['a']==2*p['b']:raise ValueError('Easy fixed bank requires tangent slope magnitude unequal to one')
 a,b,k,h,T=[sp.Integer(p[q]) for q in ('a','b','k','h','t0')];X=a*t+k;Y=b*t*t+h;X0=X.subs(t,T);Y0=Y.subs(t,T);m=2*b*T/a;mn=-1/m
 problem='A curve is defined by the parametric equations\n\n$$\nx='+tex(X)+r',\,y='+tex(Y)+r',\,-\infty<t<\infty.'+'\n$$\n\nLet $C$ be the point that corresponds to $t='+str(T)+'$ on the curve. Find the equation of the normal to the curve at $C.$'
 solution='First, we find the coordinates of the point $C$ by substituting $t='+str(T)+'$ into the parametric equations:\n\n$$\n'+r'\begin{aligned}x & ='+str(a)+'('+str(T)+')'+('+' if k>=0 else '-')+str(abs(k))+'='+tex(X0)+r', \\ y & ='+str(b)+'('+str(T)+')^2'+('+' if h>=0 else '-')+str(abs(h))+'='+tex(Y0)+r'.\end{aligned}'+'\n$$\n\nSo we\'re looking to find the equation of the normal at the point $('+tex(X0)+','+tex(Y0)+').$ For this, we need to find $\\frac{\\text{d}y}{\\text{d}x},$ which means we first need to find the derivatives of $x$ and $y,$ as follows:\n\n$$\nx\'(t)='+str(a)+r',\quad y\prime(t)='+tex(2*b*t)+'.\n$$\n\nSo, we have\n\n$$\n'+r'\frac{dy}{dx}=\frac{y\prime(t)}{x\prime(t)}=\frac{'+tex(2*b*t)+'}{'+str(a)+'}.\n$$\n\nAt the point where $t='+str(T)+'$, the slope $m$ of the tangent line is given by\n\n$$\nm=\\frac{'+str(2*b)+'('+str(T)+')}{'+str(a)+'}='+tex(m)+'.\n$$\n\nTo find the slope $m_n$ of the normal line, we take the negative reciprocal of $m$:\n\n$$\nm_n=-\\frac{1}{m}=-\\frac{1}{('+tex(m)+')}='+tex(mn)+'.\n$$\n\nTo calculate the equation of the normal, we use point-slope form:\n\n$$\n'+r'\begin{aligned}y-('+tex(Y0)+') & ='+tex(mn)+'(x-('+tex(X0)+r')) \\ y & ='+tex(sp.expand(mn*(x-X0)+Y0))+r'.\end{aligned}'+'\n$$'
 bank=method_bank(X0,Y0,m,mn)
 return make_record('easy','linear_quadratic',p,'method',problem,solution,[bank],[0],['selection'],'radio',extra={'seed':seed})

def method_bank(X0,Y0,m,mn):
 # Choose this entire bank before parameters: true normal; tangent; positive
 # reciprocal; omitted point x-coordinate; reversed point y-coordinate.
 pairs=[(mn,Y0-mn*X0),(m,Y0-m*X0),(-mn,Y0+mn*X0),(mn,Y0),(mn,-Y0-mn*X0)]
 if abs(m)==1:
  # A separate complete eligible bank for the endpoint log-sine family.
  pairs=[(mn,Y0-mn*X0),(m,Y0-m*X0),(mn,0),(mn,-Y0-mn*X0),(m,0)]
 if len(set((sp.simplify(a),sp.simplify(b)) for a,b in pairs))!=5:raise ValueError('Whole method bank collision')
 return ['y='+tex(sp.expand(a*x+b)) for a,b in pairs]

# MODERATE: five captured curve families, fixed source t and derivative workload.
# Translations k,h ∈ [-6,6] vary both coordinates and line/intercept arithmetic.
# Historical banks are not inferred recipes; they remain evidence-only.
# HARD: the two captured polynomial intersection chains plus explicitly authored
# completion of the unrated quartic-axis source, always coordinates in two blanks.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Invalid difficulty')
 if level=='easy':
  if template not in (None,'linear_quadratic') or field_type not in (None,'radio'):raise ValueError('Easy template/layout')
  if parameters is not None:return easy_instance(seed,parameters,profile)
  for retry in range(100):
   try:return easy_instance(seed+retry,None,profile)
   except ValueError as e:
    if 'collision' not in str(e):raise
  raise ValueError('Whole-bank sampling exhausted')
 names=[n for n,d in FAMILIES.items() if d[0]==level];rng=random.Random(seed)
 if template is None:template=rng.choice(names)
 if template not in names:raise ValueError('Template workload/difficulty mismatch')
 profile=profile or 'method'
 if profile not in ('observed','method'):raise ValueError('Unknown complete profile')
 q=QUESTIONS[FAMILIES[template][1]];axis=FAMILIES[template][-1]
 kind='radio' if level=='moderate' or (profile=='observed' and template=='quartic_axis') else 'blank'
 if field_type not in (None,kind):raise ValueError('Unsupported source layout')
 if parameters is None:
  if profile=='observed' and template=='quartic_axis':return generate(level,seed,template,field_type,{'k':0,'h':0},profile)
  for retry in range(200):
   p={'k':rng.randint(-6,6),'h':rng.randint(-6,6)}
   try:return generate(level,seed,template,field_type,p,profile)
   except ValueError as e:
    if 'collision' not in str(e):raise
  raise ValueError('Whole-bank sampling exhausted')
 p=dict(parameters)
 if set(p)!={'k','h'} or not all(isinstance(v,int) and abs(v)<=6 for v in p.values()):raise ValueError('Translated source workload bounds')
 k,h=p['k'],p['h'];d=data_for(template,k,h);X0,Y0,m,mn,intercept=d
 raw=profile=='observed'
 if raw and template=='quartic_axis' and (k or h):raise ValueError('Fixed raw raster permits only original geometry; method profile supplies textual changed geometry')
 text=prompt(q,k,h,raw);solution=source_solution(q,k,h,axis,d,raw)
 if profile=='observed':
  banks=historical_bank(q,k,h,axis,mn);keys=[f[':answer-field/key'] for f in q[':question/answer-fields']]
  correct=[next((i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')),None) for f in q[':question/answer-fields']]
  if kind=='blank':
   vals={'field-1':intercept if axis=='x' else 0,'field-2':0 if axis=='x' else intercept};banks=[[tex(vals[key])] for key in keys]
 else:
  if kind=='radio':banks=[method_bank(X0,Y0,m,mn)];keys=['selection'];correct=[0]
  else:
   keys=['field-1','field-2'];banks=[[tex(intercept if axis=='x' else 0)],[tex(0 if axis=='x' else intercept)]];correct=[0,0]
   if template=='quartic_axis':
    text+='\n\nThe normal crosses the $x$-axis at $(${{field-1}}, {{field-2}}$).$ Give exact answers.'
    solution=authored_axis_solution(template,k,h,d)
 return make_record(level,template,p,profile,text,solution,banks,correct,keys,kind,rawq=q if raw else None,extra={'seed':seed,'source_id':q[':db/id']})

def authored_axis_solution(family,k,h,d):
 X0,Y0,m,mn,intercept=d
 return 'First, we find the coordinates of the point $C$ by substituting $t=-1$ into the parametric equations:\n\n$$\n'+r'\begin{aligned}x & =(-1)^4+(-1)'+('+' if k>=0 else '-')+str(abs(k))+'='+tex(X0)+r' \\ y & =(-1)^2'+('+' if h>=0 else '-')+str(abs(h))+'='+tex(Y0)+r'.\end{aligned}'+'\n$$\n\nFor the normal at $('+tex(X0)+','+tex(Y0)+')$, first find the derivatives:\n\n$$\nx\\prime(t)=4t^3+1,\\quad y\\prime(t)=2t.\n$$\n\nSo, we have\n\n$$\n\\frac{dy}{dx}=\\frac{y\\prime(t)}{x\\prime(t)}=\\frac{2t}{4t^3+1}.\n$$\n\nAt $t=-1$, the tangent slope is\n\n$$\nm=\\frac{2(-1)}{4(-1)^3+1}=\\frac{-2}{-3}=\\frac{2}{3}.\n$$\n\nTo find the normal slope, take the negative reciprocal:\n\n$$\nm_n=-\\frac{1}{m}=-\\frac{1}{(2/3)}=-\\frac{3}{2}.\n$$\n\nUsing point-slope form,\n\n$$\ny-('+tex(Y0)+')=-\\frac{3}{2}(x-('+tex(X0)+')).\n$$\n\nThe normal intersects the $x$-axis when $y=0$. At this point,\n\n$$\n'+r'\begin{aligned}0-('+tex(Y0)+') & ='+tex(mn)+'(x-('+tex(X0)+r')) \\ x-('+tex(X0)+') & ='+tex(-Y0/mn)+r' \\ x & ='+tex(intercept)+r'.\end{aligned}'+'\n$$\n\nConsequently, the normal crosses the $x$-axis at $('+tex(intercept)+',0).$'

# EASY entrypoint: authored linear/quadratic, one derivative term per coordinate.
def generate_easy(seed=0,**kwargs):
 """One-term derivative evaluations, reciprocal slope and point-slope line."""
 return generate('easy',seed,**kwargs)
# MODERATE entrypoint: five observed equal-level families, captured t and chain.
def generate_moderate(seed=0,**kwargs):
 """Complete normal equation from captured nonlinear coordinate families."""
 return generate('moderate',seed,**kwargs)
# HARD entrypoint: normal-line method plus one specified axis intersection.
def generate_hard(seed=0,**kwargs):
 """Two observed coordinate layouts and an authored unrated completion."""
 return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];lines=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):lines+=['\n'+f[':answer-field/key']+':']+['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
 if ':question/worked-solution' in q:lines+=['\nWorked solution:\n'+q[':question/worked-solution']]
 return '\n'.join(lines)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args();levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in levels for i in range(a.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
