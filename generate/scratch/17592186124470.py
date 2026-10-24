#!/usr/bin/env python3
"""Vector chain rule in three variables, frozen local review generator.

math basis 1356. All eight source banks remain explicit observed profiles;
source notation/ordered solution rows are masks, not literal payload replay.
The f coefficient c and curve translation h are genuine mathematical slots.
Observed distractor intent is underdetermined: their exact expression patterns
are scaled/substituted, never promoted to authored-default error operations.
Normal profiles use complete operation banks chosen before parameter sampling.
No EDB writes, images or registration. See adjacent extraction and validation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from functools import lru_cache
KP_ID=17592186124470
KP_UUID='112e3378-bde8-5896-822e-e815bde51501'
TITLE='Applying the Vector Form of the Chain Rule to a Function of Three Variables'
VERSION='vector-three-variables-3'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
X,Y,Z,T=sp.symbols('x y z t', real=True)
VARS=(X,Y,Z)
QUESTIONS=SOURCE['record'][':knowledge-point/questions']
NAMES=['pair_products','trig_product','constant_coordinate','quartic_trig','log_product','log_difference','exponential_cosine','log_exp']
QBY=dict(zip(NAMES,QUESTIONS))
LEVELS={'easy':['affine_polynomial'],'moderate':['pair_products','trig_product','constant_coordinate','quartic_trig','log_product','log_difference','log_exp'],'hard':['exponential_cosine','canonical_log']}
BASE={
 'pair_products':(X*Y+Y*Z+X*Z,(T,sp.exp(T),sp.E),'all real t'),
 'trig_product':(Z*(X+Y),(sp.sin(T),sp.cos(T),sp.exp(T)),'all real t'),
 'constant_coordinate':(X*Y**2+Y*Z**3,(T**3,sp.Integer(1),T),'all real t'),
 'quartic_trig':(X**4-Y**4-sp.cos(Z),(sp.sin(T),sp.cos(T),2*T),'all real t'),
 'log_product':(sp.log(X*Y*Z),(T,sp.exp(T-1),sp.exp(T)),'t+h>0'),
 'log_difference':(X*(Y**2-Z**2),(sp.log(T),T+1,T-1),'t+h>0'),
 'exponential_cosine':(Y*Z*sp.cos(X),(T**2,sp.exp(T),sp.exp(T)),'all real t'),
 'log_exp':(sp.log(X*Z)+sp.exp(Y),(sp.sin(T),T**2,1/T),'t+h != 0 and sin(t+h)/(t+h)>0'),
 'canonical_log':(X*Z*sp.log(Y),(T**2,T,T**3),'t+h>0'),
}

# Small strict TeX reader: actual displayed scalar expressions, never metadata.
def normalize(s):
 s=s.replace('\\\\','\\').replace('⁡','').replace('∇',r'\nabla').replace('′',"'")
 s=re.sub(r'\\operatorname\{(sin|cos|tan|cot|csc|ln)\}',r'\\\1 ',s)
 s=re.sub(r'\{(sin|cos|tan|cot|csc|ln)\}',r'\\\1 ',s)
 return s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\!','')
FUN={'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'cot':sp.cot,'csc':sp.csc,'ln':sp.log,'log':sp.log,'exp':sp.exp}
@lru_cache(maxsize=20000)
def read_scalar(s):
 s=normalize(s).rstrip('.')
 tok=re.findall(r'\\[A-Za-z]+|\d+|[A-Za-z]|[^\s]',s)
 pos=0
 def peek():return tok[pos] if pos<len(tok) else None
 def atom():
  nonlocal pos
  q=peek()
  if q is None:raise ValueError('missing atom: '+s)
  pos+=1
  if q in ('+','-'):a=power();return a if q=='+' else -a
  if q in ('{','(','['):
   a=expr(); close={'{':'}','(':')','[':']'}[q]
   if peek()!=close:raise ValueError('unbalanced '+s)
   pos+=1;return a
  if q==r'\frac':return atom()/atom()
  if q==r'\sqrt':return sp.sqrt(atom())
  if q==r'\pi':return sp.pi
  name=q.lstrip('\\')
  if name in FUN:
   fpower=sp.Integer(1)
   if peek()=='^':pos+=1;fpower=atom()
   arg_start=pos
   while arg_start<len(tok) and tok[arg_start]=='{':arg_start+=1
   parenthesized_argument=arg_start<len(tok) and tok[arg_start]=='('
   a=atom()
   # A power following a visibly parenthesized argument belongs to the
   # completed function. An unparenthesized source t^2 is an inner power.
   if peek()=='^' and not parenthesized_argument:pos+=1;a=a**atom()
   # Bare trig application "sin 2t" has one numeric multiplier.
   if a.is_number and peek() in ('t','x','y','z','(','{'):a*=atom()
   return FUN[name](a)**fpower
  if q.isdigit():return sp.Integer(q)
  if q=='e':return sp.E
  if q in 'xyzt' and len(q)==1:return {'x':X,'y':Y,'z':Z,'t':T}[q]
  raise ValueError('unsupported token '+q+' in '+s)
 def power():
  nonlocal pos
  a=atom()
  if peek()=='^':pos+=1;a=a**atom()
  return a
 def term():
  nonlocal pos
  a=power()
  while peek() is not None and peek() not in ('+', '-', '}', ')', ']', '=', ','):
   if peek() in ('*','/'):
    q=peek();pos+=1;b=power();a=a*b if q=='*' else a/b
   else:a*=power()
  return a
 def expr():
  nonlocal pos
  a=term()
  while peek() in ('+','-'):
   q=peek();pos+=1;b=term();a=a+b if q=='+' else a-b
  return a
 value=expr()
 if pos!=len(tok):raise ValueError('unread suffix '+str(tok[pos:])+' in '+s)
 return value

def tex(e):return sp.latex(e).replace(r'\log',r'\ln')
def choice_tex(e,name,p):
 # Expanding a sum must not expand the input of a trig function in the UI.
 if name=='exponential_cosine':
  inner=(T+p['h'])**2
  e=e.xreplace({fn(sp.expand(inner)):fn(inner,evaluate=False) for fn in (sp.sin,sp.cos)})
 return tex(e)

def final_solution_value(solution):
 return solution.rsplit(' & =',1)[1].split(r'\end{aligned}',1)[0].rstrip('.')
@lru_cache(maxsize=40000)
def equal(a,b):
 d=a-b
 for fn,replace in [(sp.cot,lambda u:sp.cos(u)/sp.sin(u)),(sp.tan,lambda u:sp.sin(u)/sp.cos(u)),(sp.csc,lambda u:1/sp.sin(u))]:
  d=d.replace(lambda e:e.func==fn,lambda e:replace(e.args[0]))
 d=sp.cancel(sp.expand(d))
 if d==0:return True
 numerator=sp.fraction(d)[0]
 atoms=sorted(numerator.atoms(sp.sin,sp.cos),key=sp.default_sort_key)
 if not atoms:return False
 try:
  if sp.Poly(numerator,*atoms).total_degree()<=1:return False
 except sp.PolynomialError:pass
 return sp.cancel(sp.trigsimp(d,method='fu'))==0
def shift_tex(raw,h):
 # Keep source bytes at h=0. On translation, the source's bare trig t^n
 # argument becomes explicitly enclosed BEFORE inserting a parenthesized
 # t+h. This avoids changing sin(t^2) into the function power sin(t+h)^2.
 # Source function powers such as {sin}^3 t are a distinct mask.
 if not h:return raw
 pattern=r'(\\operatorname\{(?:sin|cos|tan|cot|csc)\}⁡?|\\(?:sin|cos|tan|cot|csc)\s*)(\{t\}|t)(\^\{[1-9][0-9]*\})'
 raw=re.sub(pattern,lambda m:m[1]+'('+m[2]+m[3]+')',raw)
 # Commands are protected; mathematical arguments remain substitutable.
 return re.sub(r'\\operatorname\{[^}]+\}|\\[A-Za-z]+|[A-Za-z]+',lambda m:m[0] if m[0] not in ('t','ti','tj','tk','te') else '('+tex(T+h)+')'+m[0][1:],raw)
def scale_tex(raw,c):return raw if c==1 else str(c)+r'\left('+raw+r'\right)'
def vector(items):return '+'.join('('+tex(a)+r')\,'+b for a,b in zip(items,'ijk'))
def vector_parts(raw):
 raw=raw.strip().rstrip('.')
 # Basis symbols are outside command words; source prompt's ti and ek have
 # explicit normalization below before this reader is invoked.
 hits=list(re.finditer(r'(?<![A-Za-z])([ijk])(?![A-Za-z])',raw))
 if [m[1] for m in hits]!=list('ijk'):raise ValueError('vector basis '+raw)
 out=[];start=0
 for m in hits:
  piece=raw[start:m.start()].strip().replace(r'\,','').strip()
  if piece in ('','+'):piece='1'
  if piece=='-':piece='-1'
  out.append(piece);start=m.end()
 if raw[start:].strip():raise ValueError('vector suffix '+raw)
 return out

def map_vector(raw,c=1,h=0):
 # Complete coordinate components are slots; basis labels never substituted.
 parts=vector_parts(raw)
 return '+'.join('('+scale_tex(shift_tex(v,h),c)+r')\,'+b for v,b in zip(parts,'ijk')) if (c!=1 or h!=0) else raw

def prompt_parts(q):
 m=re.search(r'f\(x,\s*y,\s*z\)\s*=\s*(.*?)\$',q[':question/problem']);f=m[1]
 m=re.search(r'r\(t\)\s*=\s*(.*?)\$',q[':question/problem']);r=m[1].rstrip(',')
 # Legacy compact basis spellings are complete vector slots only.
 r=r.replace('ti','t\\,i').replace('tj','t\\,j').replace('ek','e\\,k').replace('}j','}\\,j')
 return f,r

# The full source prose and row masks are retained. Rendering applies complete
# math-component slots, including derivative operator arguments, not a global
# short-string replacement. Raw source spelling is a display convention.
def source_solution(name,c,h):
 q=QBY[name];raw=q.get(':question/worked-solution')
 if raw is None:return common_solution(*objects(name,{'c':c,'h':h})[:2])
 fraw,_=prompt_parts(q)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',raw,re.S)
 rendered=[]
 for bi,block in enumerate(blocks):
  if bi==0:rendered.append(block);continue
  prefix=r'\begin{aligned}'; suffix=r'\end{aligned}'
  assert block.startswith(prefix) and block.endswith(suffix)
  inner=block[len(prefix):-len(suffix)]
  rows=re.split(r'( \\\\  & =)',inner)
  first=rows[0]; lhs,rhs=first.split(' & =',1)
  rhs_rows=[rhs]+[rows[i] for i in range(2,len(rows),2)]
  new=[]
  for ri,r in enumerate(rhs_rows):
   period='.' if r.endswith('.') else '';r=r.rstrip('.')
   if bi==1:
    if ri==0:r=r.replace(fraw,scale_tex(fraw,c))
    else:r=map_vector(r,c,0)
   elif bi==2:r=map_vector(r,c,h)
   elif bi==3:
    if ri==0:
     # Ordered formal coordinate derivatives retain d/dt as operator.
     pat=r'(\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\()(.*?)(\)(?:\\,)?[ijk])'
     r,n=re.subn(pat,lambda m:m[1]+shift_tex(m[2],h)+m[3],r)
     assert n==3,(name,n,r)
    else:r=map_vector(r,1,h)
   elif bi==4:
    if ri==0:pass
    elif ri==1:
     left,right=r.split(r'\cdot ',1)
     assert left.startswith('(') and left.endswith(')') and right.startswith('(') and right.endswith(')')
     r='('+map_vector(left[1:-1],c,h)+r')\cdot ('+map_vector(right[1:-1],1,h)+')'
    else:r=scale_tex(shift_tex(r,h),c)
   new.append(r+period)
  rendered.append(prefix+lhs+' & ='+r' \\  & ='.join(new)+suffix)
 result=raw
 for old,new in zip(blocks,rendered):result=result.replace('$$\n'+old+'\n$$','$$\n'+new+'\n$$',1)
 # Prose equations have full coordinate RHS slots, separate from display rows.
 # Some source prose groups several coordinates in a single inline expression.
 paragraphs=result.split('\n\n')
 for i,p in enumerate(paragraphs):
  if p.startswith('Next, we substitute'):
   before,after=p.split(' into the above',1)
   before=re.sub(r'\$(.*?)\$',lambda m:'$'+shift_tex(m[1],h)+'$',before)
   paragraphs[i]=before+' into the above'+after
 return '\n\n'.join(paragraphs)

def objects(name,p):
 if name=='affine_polynomial':
  a,b,d,n=p['a'],p['b'],p['d'],p['n']
  f=a*X+b*Y+d*Z;r=(T,T**2,T**n);domain='all real t'
 else:
  f,r,domain=BASE[name];f=p['c']*f;r=tuple(e.subs(T,T+p['h']) for e in r)
 g=tuple(sp.diff(f,v) for v in VARS)
 gr=tuple(sp.expand_mul(v.subs(dict(zip(VARS,r)),simultaneous=True)) for v in g)
 rd=tuple(sp.diff(v,T) for v in r)
 terms=tuple(sp.expand_mul(a*b) for a,b in zip(gr,rd))
 answer=sp.factor_terms(sp.expand(sum(terms)))
 if name=='quartic_trig':answer=sp.trigsimp(answer,method='fu')
 return f,r,g,gr,rd,terms,answer,domain

def block(lhs,rows):return '$$\n'+r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+r'\end{aligned}'+'\n$$'
def common_solution(f,r):
 g=tuple(sp.diff(f,v) for v in VARS);gr=tuple(sp.expand_mul(v.subs(dict(zip(VARS,r)),simultaneous=True)) for v in g);rd=tuple(sp.diff(v,T) for v in r)
 formal='+'.join(r'\frac{∂}{∂'+str(v)+'}('+tex(f)+r')\,'+b for v,b in zip(VARS,'ijk'))
 rformal='+'.join(r'\frac{\text{d}}{\text{d}t}('+tex(v)+r')\,'+b for v,b in zip(r,'ijk'))
 terms=tuple(a*b for a,b in zip(gr,rd))
 product='+'.join('('+tex(a)+r')\cdot ('+tex(b)+')' for a,b in zip(gr,rd))
 distributed='+'.join('('+tex(e)+')' for e in terms)
 return ('The chain rule in vector form states that\n\n$$\n'+r'\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).'+'\n$$\n\n'
 +'First, we need to compute $∇f(x,y,z):$\n\n'+block('∇f(x,y,z)',[formal,vector(g)])
 +'\n\nNext, we substitute $x='+tex(r[0])+',y='+tex(r[1])+',$ and $z='+tex(r[2])+'$ into the above to find $∇f(r(t)):$\n\n'+block('∇f(r(t))',[vector(gr)])
 +'\n\nNow, we calculate the derivative of $r(t),$ which is\n\n'+block(r'{r}^{′}(t)',[rformal,vector(rd)])
 +'\n\nFinally, applying the chain rule, we get\n\n'+block(r'\frac{\text{d}}{\text{d}t}[f(r(t))]',[r'∇f(r(t))\cdot {r}^{′}(t)','('+vector(gr)+r')\cdot ('+vector(rd)+')',product,distributed,tex(sp.factor_terms(sp.expand(sum(terms))))+'.']))

# Complete defensive authored wrong-operation banks. No arbitrary offsets.
# Selection precedes sampling; all five outcomes must be pairwise unequal.
OP_BANKS={
 'omit_chain':('correct','omit_x','omit_y','omit_z','undifferentiated_curve'),
 'sign_chain':('correct','negate_x','negate_y','negate_z','sum_gradient'),
 'constant_active':('correct','omit_x','lose_power_factor','undifferentiated_curve','sum_gradient'),
 'xy_active':('correct','omit_x','omit_y','undifferentiated_curve','sum_gradient'),
 'log_rates':('correct','omit_y','omit_both_rates','negate_x','undifferentiated_curve'),
 'paired_exp':('correct','omit_x','omit_pair','lose_inner_chain','sum_gradient'),
}
ELIGIBLE={
 'affine_polynomial':('omit_chain','sign_chain'),
 'pair_products':('xy_active',), 'trig_product':('omit_chain','sign_chain'),
 'constant_coordinate':('constant_active',), 'quartic_trig':('omit_chain','sign_chain'),
 'log_product':('log_rates',), 'log_difference':('omit_chain','sign_chain'),
 'exponential_cosine':('paired_exp',), 'log_exp':('omit_chain','sign_chain'),
 'canonical_log':('omit_chain','sign_chain'),
}
def bank_values(profile,data):
 f,r,g,gr,rd,terms,ans,domain=data
 all_values={'correct':ans,'omit_x':terms[1]+terms[2],'omit_y':terms[0]+terms[2],'omit_z':terms[0]+terms[1],
 'negate_x':-terms[0]+terms[1]+terms[2],'negate_y':terms[0]-terms[1]+terms[2],'negate_z':terms[0]+terms[1]-terms[2],
 'undifferentiated_curve':sum(a*b for a,b in zip(gr,r)), 'sum_gradient':sum(gr),
 'omit_both_rates':terms[0],'omit_pair':terms[0],
 'lose_inner_chain':gr[0]+terms[1]+terms[2],
 'lose_power_factor':terms[0]/3+terms[1]+terms[2]}
 return [(label,ans if label=='correct' else sp.factor_terms(sp.expand(all_values[label]))) for label in OP_BANKS[profile]]
def parameters_ok(level,name,p,observed=False):
 if name not in LEVELS[level]:raise ValueError('template is outside selected level')
 if name=='affine_polynomial':
  if set(p)!={'a','b','d','n'} or any(type(p[k])!=int for k in p):raise ValueError('exact parameter keys and integers required')
  if any(not 1<=abs(p[k])<=3 for k in ('a','b','d')) or p['n'] not in (1,2):raise ValueError('easy: 3 affine partials; powers 1/2; nonzero coefficients |c|<=3')
 else:
  if set(p)!={'c','h'} or any(type(p[k])!=int for k in p):raise ValueError('exact c,h integer parameters required')
  max_c=3 if level=='moderate' else 4
  if not 1<=abs(p['c'])<=max_c or abs(p['h'])>2:raise ValueError('level coefficient/shift bounds exceeded')

def identity(prompt,solution,values,correct,domain,difficulty=None):
 payload={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':correct,'domain':domain,'difficulty':difficulty}
 return hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))

# EASY — authored missing level: affine f, three low-power coordinates; no
# products in partials, log/trig identities, point evaluation or rate context.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — five rated observations plus two explicitly assigned unrated
# records. Fixed source workloads; |c|<=3, |h|<=2 in sampling AND explicit calls.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — observed exp/trig nested product and canonical xz ln(y); |c|<=4,
# |h|<=2. Three chain contributions; no new function or sibling assessed skill.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('source response type is radio')
 rng=random.Random(seed)
 name=template or rng.choice(LEVELS[level])
 if name not in LEVELS[level]:raise ValueError('template outside level')
 profile=profile or {'constant_coordinate':'constant_active','pair_products':'xy_active','log_product':'log_rates','exponential_cosine':'paired_exp'}.get(name,'omit_chain')
 if profile not in OP_BANKS and profile not in ('observed_raw','observed_pattern'):raise ValueError('unknown bank profile')
 observed=profile.startswith('observed')
 if observed and name not in QBY:raise ValueError('no observed bank for authored template')
 if not observed and profile not in ELIGIBLE[name]:raise ValueError('bank profile ineligible for this template')
 # Entire bank selected above, before any mathematical parameters.
 for attempt in range(150):
  if parameters is not None:p=dict(parameters)
  elif name=='affine_polynomial':p={k:rng.choice([-3,-2,-1,1,2,3]) for k in ('a','b','d')} ;p['n']=rng.choice([1,2])
  else:p={'c':rng.choice([v for v in range(-4 if level=='hard' else -3,5 if level=='hard' else 4) if v]),'h':rng.randint(-2,2)}
  parameters_ok(level,name,p,observed);data=objects(name,p)
  f,r,g,gr,rd,terms,ans,domain=data
  if observed:
   q=QBY[name];raw_values=[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
   values=[scale_tex(shift_tex(v,p['h']),p['c']) for v in raw_values]
   exprs=[read_scalar(v) for v in values]
   flags=[equal(v,ans) for v in exprs]
   if sum(flags)!=1:raise ValueError('observed bank correct value not uniquely derived')
   correct_index=flags.index(True);recipes=['observed_expression_pattern_'+str(i+1) for i in range(5)]
  else:
   pairs=bank_values(profile,data);recipes=[a for a,b in pairs];exprs=[b for a,b in pairs];values=[choice_tex(v,name,p) for v in exprs];correct_index=0
  collision=any(equal(a,b) for i,a in enumerate(exprs) for b in exprs[i+1:])
  if not collision:break
  if parameters is not None:raise ValueError('entire bank rejected: equivalent options')
 else:raise ValueError('unable to sample eligible complete bank')
 if name in QBY:
  q=QBY[name];fraw,_=prompt_parts(q)
  prompt=q[':question/problem'].replace(fraw,scale_tex(fraw,p['c']),1)
  # Only the curve RHS is translated, preserving function/operator labels.
  m=re.search(r'(r\(t\)\s*=\s*)(.*?)(\$)',prompt)
  prompt=prompt[:m.start(2)]+shift_tex(m[2],p['h'])+prompt[m.end(2):]
  solution=source_solution(name,p['c'],p['h'])
 else:
  prompt='If $f(x,y,z)='+tex(f)+'$ and $r(t)='+vector(r)+r',$ compute $\frac{\text{d}}{\text{d}t}[f(r(t))].$'
  solution=common_solution(f,r)
 if not observed:
  # The source's completed derivation defines the instructional answer form.
  # Independent symbolic work still checks its value before it is keyed.
  final=final_solution_value(solution)
  assert equal(read_scalar(final),ans),'Worked solution does not derive the keyed answer'
  values[correct_index]=final
 if profile!='observed_raw':
  # The captured Unicode function-application glyph is valid notation.
  # Source bytes are preserved; no invented TeX anomaly or normalization.
  pass
 raw=profile=='observed_raw' and name in QBY
 original=QBY.get(name,{})
 shown_solution=solution if not raw or ':question/worked-solution' in original else None
 shown_difficulty=':question.difficulty/'+level if not raw or ':question/difficulty' in original else None
 shown_correct=values[correct_index] if not raw or ':answer-field/correct' in original[':question/answer-fields'][0] else None
 digest=identity(prompt,shown_solution,values,shown_correct,domain,shown_difficulty)
 qid=uid('question:'+digest);fid=uid('field:'+digest)
 answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct_ref=answers[correct_index][':answer/id'];rng.shuffle(answers)
 task=hashlib.sha256(json.dumps([sp.srepr(sp.expand(f)),[sp.srepr(v) for v in r],domain],sort_keys=True).encode()).hexdigest()
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if shown_correct is not None:field[':answer-field/correct']=[':answer/id',correct_ref]
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if shown_difficulty is not None:question[':question/difficulty']=shown_difficulty
 if shown_solution is not None:question[':question/worked-solution']=shown_solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
 'generation':{'version':VERSION,'seed':seed,'template':name,'profile':profile,'parameters':p,'domain':domain,'content_fingerprint':digest,'mathematical_fingerprint':task,
 'source':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'source_ids':[QBY[name][':db/id']] if name in QBY else [],
 'difficulty_origin':'authored assignment' if name in ('pair_products','trig_product') else 'observed' if name in QBY else 'authored scope',
 'source_completions':[k for k in (':question/worked-solution',':question/difficulty',':answer-field/correct') if k not in original and (k!=':answer-field/correct' or k not in original.get(':question/answer-fields',[{}])[0])] if name in ('pair_products','trig_product') and not raw else [],
 'authored_scope':name not in QBY,'evidence_only':observed,'eligible_for_learning':not observed,'bank_origin':'observed expression patterns; intent unresolved' if observed else 'authored complete wrong-operation bank','recipes':recipes,'dependencies':{'sympy':sp.__version__}}}

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Original source has no worked-solution attribute.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['markdown','json'],default='markdown');args=ap.parse_args()
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
