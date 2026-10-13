"""Second-order direct integration, basis 1356; no database writes.

Observed profiles are complete replay-only banks. Their scaling recipe is the
linear covariance of the entire forced part under g -> scale*g, not a recovered
error algorithm. Defaults use a complete authored method bank selected before
sampling. Easy: one basic term. Moderate: two basic terms and scalar isolation.
Hard (authored absent level): three basic terms and scalar isolation, no new
integration technique, IVP, dependent-variable forcing, or nonlinear equation.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, uuid, sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'17592186096697'
VERSION='second-order-direct-v1'
x=sp.Symbol('x',real=True); C,D=sp.symbols('C D',real=True)
NS=uuid.UUID('192bb38b-b609-56ff-b560-becfc38ea070')
SOURCE=json.loads((EVIDENCE/'source.json').read_text())
KP=SOURCE['record']; SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
LEVELS=('easy','moderate','hard')
NOTE='Note that because we had a second-order equation, our general solution contains *two* arbitrary constants, $C$ and $D.$'
D2=r'\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}'; D1=r'\frac{\text{d}y}{\text{d}x}'
TEMPLATES={'single_power':'easy','single_exp':'easy','single_sin':'easy','single_cos':'easy',
 'power_exp':'moderate','power_trig':'moderate','two_powers':'moderate','base_trig':'moderate',
 'power_exp_trig':'hard','two_powers_trig':'hard','power_base_trig':'hard'}
BANK_PROFILES={**{f'observed-{key}':{'source':key,'eligible_default':False,'interpretation':'Explicit scaled expression bank; wrong-operation intent unresolved.'} for key in SOURCES},
 **{f'completed-{key}':{'source':key,'eligible_default':False,'interpretation':'Presentation-normalized observed bank, duplicate legacy fields removed.'} for key in SOURCES},
 'authored-method':{'eligible_default':True,'recipes':['correct','reverse_forcing','integrate_only_once','lose_first_constant','lose_second_constant']}}
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def ident(text):return str(uuid.uuid5(NS,text))
def tex(value):return sp.latex(value).replace(r'\log',r'\ln')
def normalize(s):
 # Decoded source bytes have no doubled-backslash or literal Unicode-escape
 # anomaly. Preserve them; ln typography is normalized only in completion.
 return s
def additive(s):
 """Split complete top-level terms; braces/parentheses protect function inputs."""
 out=[];start=0;depth=0
 for i,ch in enumerate(s):
  if ch in '({':depth+=1
  elif ch in ')}':depth-=1
  elif ch in '+-' and depth==0 and i>start:
   out.append(s[start:i]);start=i
 out.append(s[start:]);return out
def scale_expression(raw,a):
 """Parameterized complete-component masks. Neutral scaling preserves source bytes.

 Arbitary C,D components and derivative coefficients are protected. A formal
 integral with a parenthesized argument scales the forced components inside,
 retaining its C component and its outer operation. All multiplied numerical
 factors have visible grouping, never concatenated digits.
 """
 if a==1:return raw
 trailing=''
 while raw and (raw[-1]=='.' or raw[-1].isspace()):trailing=raw[-1]+trailing;raw=raw[:-1]
 parts=[]
 for part in additive(raw):
  sign='';p=part
  if p.startswith(('+','-')):sign,p=p[0],p[1:]
  if D2 in p or D1 in p or p.strip()=='y':v=p
  elif re.search(r'\b[CD]\b',p) or re.search(r'[CD](?:x|\{|\\|\s|$)',p):
   # Formal integral contains C in its argument; recursively transform that
   # argument, rather than freezing a mixture of forced and arbitrary terms.
   m=re.match(r'(\s*\\int\s*)\(',p)
   if m:
    start=m.end();depth=1;j=start
    while depth:
     if p[j]=='(':depth+=1
     if p[j]==')':depth-=1
     j+=1
    v=p[:start]+scale_expression(p[start:j-1],a)+p[j-1:]
   else:v=p
  else:v=tex(a)+r'\left('+p+r'\right)'
  parts.append(sign+v)
 return ''.join(parts)+trailing
def scale_math(block,a):
 if r'\begin{aligned}' in block:
  middle=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  rows=middle.split(r'\\'); rendered=[]
  for row in rows:
   lhs,rhs=row.split('=',1);rendered.append(lhs+'='+scale_expression(rhs,a))
  return block.replace(middle,r'\\'.join(rendered))
 if '=' in block:
  lhs,rhs=block.split('=',1)
  return scale_expression(lhs,a)+'='+scale_expression(rhs,a)
 return block

def render_source_text(text,a):
 # Only complete delimited mathematical components become parameter slots;
 # shared prose remains literal. No short-expression global substitutions.
 return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)',
  lambda m:('$$'+scale_math(m[0][2:-2],a)+'$$') if m[0].startswith('$$') else '$'+scale_math(m[0][1:-1],a)+'$',text,flags=re.S)

def inner(raw):
 if isinstance(raw,list):return [inner(z) for z in raw]
 if isinstance(raw,dict):
  if set(raw)=={':db/ident'}:return raw[':db/ident']
  return {k:inner(v) for k,v in raw.items() if k!=':db/id'}
 return raw

def observed_record(level,seed,template,p,profile):
 key=BANK_PROFILES[profile]['source'];source=SOURCES[key]
 actual=source.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
 if level!=actual:raise ValueError('Observed difficulty must match capture')
 if template not in (None,key):raise ValueError('Observed profile requires its source template')
 if set(p)!={'scale'}:raise ValueError('Observed scale parameter required')
 a=sp.Rational(str(p['scale']))
 if not 0<a<=8:raise ValueError('Replay scale must be in (0,8]')
 q=inner(copy.deepcopy(source))
 q[':question/problem']=render_source_text(source[':question/problem'],a)
 if ':question/worked-solution' in source:q[':question/worked-solution']=render_source_text(source[':question/worked-solution'],a)
 for f in q.get(':question/answer-fields',[]):
  old_correct=f.get(':answer-field/correct',{}).get(':answer/id')
  for answer in f.get(':answer-field/choices',[]):answer[':answer/value']=scale_expression(answer[':answer/value'].split('=',1)[1],a).join(['y=','']) if a!=1 else answer[':answer/value']
  if old_correct:f[':answer-field/correct']=[':answer/id',old_correct]
 if profile.startswith('completed-'):
  q[':question/answer-fields']=[q[':question/answer-fields'][-1]]
  for attr in (':question/problem',':question/worked-solution'):
   if attr in q:q[attr]=normalize(q[attr]).replace('{ln}^{2}⁡',r'\ln^{2}')
  for f in q[':question/answer-fields']:
   for answer in f[':answer-field/choices']:answer[':answer/value']=normalize(answer[':answer/value']).replace('{ln}^{2}⁡',r'\ln^{2}')
  if key=='q-119041':
   # The source's first primitive evaluation omits C before the reduced row
   # adds it. Keep raw evidence and repair this one primitive stage only.
   sol=q[':question/worked-solution'];first=sol.split('Integrating a second time')[0]
   target=first.split(r' \\ ')[1];first=first.replace(target,target.rstrip()+'+C ')
   q[':question/worked-solution']=first+'Integrating a second time'+sol.split('Integrating a second time',1)[1]
 return finish(q,seed,key,{'scale':str(a)},profile,'observed-completed' if profile.startswith('completed-') else 'observed-raw',None)

def terms_for(template,p):
 a,b,c=map(lambda k:sp.Rational(str(p[k])),('a','b','c'))
 n=int(p['n']);k=sp.Rational(str(p['k']));base=int(p['base'])
 trig=sp.sin if p['trig']=='sin' else sp.cos
 power=a*x**n; exp=b*sp.exp(k*x);trigterm=c*trig(k*x);base_term=b*base**x
 return {'single_power':[power],'single_exp':[a*sp.exp(k*x)],'single_sin':[a*sp.sin(k*x)],'single_cos':[a*sp.cos(k*x)],
 'power_exp':[power,exp],'power_trig':[power,trigterm],'two_powers':[power,b*x**(n+1)],'base_trig':[base_term,trigterm],
 'power_exp_trig':[power,exp,trigterm],'two_powers_trig':[power,b*x**(n+1),trigterm],'power_base_trig':[power,base_term,trigterm]}[template]

def guard(level,template,p):
 required={'a','b','c','n','k','base','trig','m'}
 if set(p)!=required:raise ValueError('Parameters require exactly '+str(sorted(required)))
 if TEMPLATES.get(template)!=level:raise ValueError('Template/level mismatch')
 for key in ('a','b','c'):
  z=sp.Rational(str(p[key]));
  if z.q!=1 or not 1<=abs(z)<=8:raise ValueError('Coefficients must be nonzero integers |c|<=8')
 if int(p['n'])!=p['n'] or p['n'] not in (0,1,2,3):raise ValueError('n in 0..3')
 if sp.Rational(str(p['k'])) not in (-3,-2,-1,sp.Rational(-1,2),sp.Rational(1,2),1,2,3):raise ValueError('Familiar nonzero frequency required')
 if p['base'] not in (2,3,4) or p['trig'] not in ('sin','cos'):raise ValueError('Base/trig guard')
 if p['m'] not in ((1,) if level=='easy' else (2,3,4)):raise ValueError('Scalar isolation workload guard')
 return p

def sample(level,rng):
 return {'a':rng.choice([z for z in range(-8,9) if z]),'b':rng.choice([z for z in range(-8,9) if z]),'c':rng.choice([z for z in range(-8,9) if z]),'n':rng.randrange(4),'k':rng.choice([-3,-2,-1,'-1/2','1/2',1,2,3]),'base':rng.choice([2,3,4]),'trig':rng.choice(['sin','cos']),'m':1 if level=='easy' else rng.choice([2,3,4])}

def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(lhs+' & ='+rhs for lhs,rhs in rows)+r'\end{aligned}'+'\n$$'
def signed_sum(parts):return ' + '.join('('+z+')' for z in parts)
def integral(term):return r'\int \left('+tex(term)+r'\right)\,\text{d}x'
def stage(terms):
 # Ordered explicit coefficient*primitive nodes survive CAS simplification.
 components=[];distributed=[];primitives=[]
 for term in terms:
  coefficient,body=term.as_independent(x,as_Add=False)
  primitive=sp.integrate(body,x)
  distributed.append('('+tex(coefficient)+')'+integral(body))
  primitives.append('('+tex(coefficient)+r')\left('+tex(primitive)+r'\right)')
  components.append(sp.simplify(coefficient*primitive))
 return components,signed_sum(distributed),signed_sum(primitives)

def build_normal(level,seed,template,p,profile):
 guard(level,template,p);terms=terms_for(template,p);force=sp.Add(*terms);m=int(p['m'])
 first,dist1,eval1=stage(terms);second,dist2,eval2=stage(first)
 P=sp.Add(*second);F=sp.Add(*first)
 # Complete method-based bank chosen before parameters are sampled. No option
 # pool and no adaptive fallback are permitted; a collision rejects instance.
 values=[P+C*x+D,-P+C*x+D,F+C*x+D,P+D,P+C*x]
 if any(families_equivalent(a,b) for i,a in enumerate(values) for b in values[i+1:]):raise ValueError('Whole instance collision')
 prompt='Solve the differential equation\n\n$$\n'+('' if m==1 else str(m))+D2+'='+tex(m*force)+'.\n$$'
 sol=''
 if m!=1:sol='First, we rearrange the equation to give\n\n$$\n'+D2+'='+tex(force)+'.\n$$\n\nNow, integrating the equation once, we get\n\n'
 else:sol='Integrating the equation once, we get\n\n'
 sol+=aligned([(r'\int '+D2+r'\,\text{d}x',integral(force)),('',dist1),(D1,eval1+'+C'),('',tex(F+C)+'.')])
 sol+='\n\nIntegrating a second time, we get\n\n'
 sol+=aligned([(r'\int '+D1+r'\,\text{d}x',integral(F+C)),('y',dist2+r'+C\int \text{d}x'),('',eval2+'+Cx+D'),('',tex(P+C*x+D)+'.')])
 sol+='\n\n'+NOTE
 q={':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,
 ':question/answer-fields':[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':'y='+tex(v)} for v in values],':answer-field/correct-index':0}]}
 return finish(q,seed,template,p,profile,'authored-method',sp.srepr(force))

def family_signature(expr):
 """Affine arbitrary-constant family modulo invertible reparameterization.

 Both rank and affine displacement matter. Two letters with identical basis
 (C+D), one constant, or a particular solution cannot cover span{1,x}.
 """
 expr=sp.expand(expr);base=expr.subs({C:0,D:0});basis=[sp.diff(expr,z) for z in (C,D)]
 if any(z.has(C,D) for z in basis):raise ValueError('Nonlinear arbitrary-constant bank')
 return base,basis

def in_span(expr,basis):
 nonzero=[z for z in basis if z!=0]
 if not nonzero:return sp.simplify(expr)==0
 if all(sp.diff(z,x,2)==0 for z in nonzero):
  if sp.simplify(sp.diff(expr,x,2))!=0:return False
  matrix=sp.Matrix([[z.coeff(x),z.subs(x,0)] for z in nonzero]).T
  target=sp.Matrix([sp.diff(expr,x),expr.subs(x,0)])
  return matrix.rank()==matrix.row_join(target).rank()
 coeff=sp.symbols('u:'+str(len(nonzero)))
 eq=sp.expand(expr-sum(a*b for a,b in zip(coeff,nonzero)))
 # Derivative equations at symbolic x are converted to coefficients where
 # possible; independent elementary functions are solved symbolically.
 solution=sp.linsolve([sp.diff(eq,x,j).subs(x,1) for j in range(len(nonzero)+1)],coeff)
 return any(sp.simplify(eq.subs(dict(zip(coeff,values))).subs({z:0 for z in coeff}))==0 for values in solution)

def families_equivalent(a,b):
 p,u=family_signature(a);q,v=family_signature(b)
 return in_span(p-q,u) and all(in_span(z,v) for z in u) and all(in_span(z,u) for z in v)

def finish(q,seed,template,p,profile,origin,fingerprint):
 q=copy.deepcopy(q)
 # Mathematical task identity excludes bank and layout and incidental params.
 # Raw source scaling deduplicates by its independently readable printed ODE.
 if fingerprint is None:
  from importlib.machinery import SourceFileLoader
  parser=SourceFileLoader('secondorder_readback',str(EVIDENCE/'readback.py')).load_module()
  fingerprint=sp.srepr(parser.forcing(q[':question/problem']))
 content=copy.deepcopy({k:v for k,v in q.items() if k not in (':question/id',':question/math-academy-id')})
 # Strip original owned IDs for stable identity under choice order changes.
 for f in content.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct'); correctid=correct[1] if isinstance(correct,list) else None
  for a in f.get(':answer-field/choices',[]):
   a['_correct']=a.get(':answer/id')==correctid if correctid else f.get(':answer-field/correct-index')==f[':answer-field/choices'].index(a)
   a.pop(':answer/id',None)
  f.pop(':answer-field/id',None);f.pop(':answer-field/correct',None);f.pop(':answer-field/correct-index',None)
  f[':answer-field/choices']=sorted(f.get(':answer-field/choices',[]),key=lambda z:z[':answer/value'])
 domain='x >= 0' if template=='q-79554' else 'a connected real interval excluding x=0' if template=='q-50146' else 'x real'
 cid=digest({'version':VERSION,'content':content,'domain':domain});qid=ident(cid)
 q[':question/id']=qid
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  oldcorrect=f.get(':answer-field/correct');oldid=oldcorrect[1] if isinstance(oldcorrect,list) else None
  index=f.pop(':answer-field/correct-index',None);hascorrect=oldid is not None or index is not None
  fid=ident(cid+f'/field/{i}');f[':answer-field/id']=fid;correct=None
  for j,a in enumerate(f.get(':answer-field/choices',[])):
   iscorrect=a.get(':answer/id')==oldid if oldid else j==index
   a.pop('_correct',None);a[':answer/id']=ident(fid+'/'+a[':answer/value'])
   if iscorrect:correct=a[':answer/id']
  if hascorrect:f[':answer-field/correct']=[':answer/id',correct]
  random.Random(str(seed)+'/field/'+str(i)).shuffle(f.get(':answer-field/choices',[]))
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,
 'generation':{'version':VERSION,'dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'source_references':[template] if template in SOURCES else ['e-529',*SOURCES],'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'origin':origin,'basis':SOURCE['basis'],'database':SOURCE['database'],'lineage':SOURCE['lineage'],'content_fingerprint':cid,'mathematical_fingerprint':digest({'forcing':fingerprint,'domain':domain}),'domain':domain,'bank_eligible_default':BANK_PROFILES[profile]['eligible_default'],'eligible_for_learning':BANK_PROFILES[profile]['eligible_default'],'evidence_only':not BANK_PROFILES[profile]['eligible_default']}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS or field_type not in (None,'radio'):raise ValueError('Supported levels easy/moderate/hard and radio only')
 rng=random.Random(seed)
 profile=profile or 'authored-method' # whole bank selected BEFORE sampling
 if profile not in BANK_PROFILES:raise ValueError('Unknown complete bank profile')
 if profile.startswith(('observed-','completed-')):return observed_record(level,seed,template,parameters or {'scale':1},profile)
 template=template or rng.choice([t for t,l in TEMPLATES.items() if l==level])
 if parameters is not None:return build_normal(level,seed,template,parameters,profile)
 for attempt in range(100):
  p=sample(level,rng)
  try:return build_normal(level,seed,template,p,profile)
  except ValueError as exc:
   if 'collision' not in str(exc):raise
 raise ValueError('No valid complete-bank instance in 100 attempts')
# EASY: one term, coefficients |a|<=8, power 0..3 or familiar frequency.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: two nonzero terms; isolate y'' through coefficient 2,3,4.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: missing-source authored level, three terms using already-known primitives.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q=record['question'];lines=[q[':question/problem'],'']
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  lines+=['Field '+str(i+1)+' ('+f[':answer-field/key']+')']
  for a in f.get(':answer-field/choices',[]):lines.append('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
 if ':question/worked-solution' in q:lines+=['',q[':question/worked-solution']]
 return '\n'.join(lines)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('positive count required')
 if args.difficulty=='all' and (args.template or args.profile):parser.error('specific level required with template/profile')
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
