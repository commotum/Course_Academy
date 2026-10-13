#!/usr/bin/env python3
"""Tangent lines to level curves, math/basis 1356. Local review records only.

Fidelity first: seven extracted component masks and complete opaque banks are
public evidence-only profiles raw:q-ID (unrated omissions preserved). A diagonal
coordinate pullback f(r*x,s*y), P=(P0x/r,P0y/s) parameterizes these recipes;
normal records use separately authored complete method banks. Historical vectors
are transformed as covectors, never presented as recovered error operations.
completed:q-ID infers absent keys/stages, and remains evidence-only.

EASY: observed polynomial/logarithmic and familiar trig partial derivatives,
coefficients 1..5 (signed), integer points -2..2, nonzero gradient.
MODERATE (authored): canonical three-term ax²+by²+cxy², all coefficients nonzero
integers |a,b,c|<=6, integer nonzero |p,q|<=3, two nonzero unequal components.
HARD (authored): the same three terms and same method, reduced rational p,q with
numerator <=5, denominator 2..3. No new mathematical branch or added response.
All arithmetic coefficients/components <=200; reduced rational denominators<=27.
The bounds apply to explicit inputs, source transforms, and sampling equally.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
DIR=Path(__file__).with_suffix(''); VERSION='level-tangent-1.0'
KP_ID=17592186124454;KP_UUID='5ae7e9c8-60e9-5f5e-afbf-1de6bb01bf07';TITLE='Finding the Tangent Line to a Level Curve'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X,Y=sp.symbols('x y',real=True); LOC={'x':X,'y':Y,'pi':sp.pi,'cos':sp.cos,'sin':sp.sin,'log':sp.log,'sqrt':sp.sqrt}
PROFILES=json.loads((DIR/'templates.json').read_text());TEMPLATES={v['template']:k for k,v in PROFILES.items()}
TRANS=standard_transformations+(implicit_multiplication_application,)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(v)))
def tex(e):return sp.latex(e).replace(r'\log',r'\ln')
def parse_math(t):
 """Small independent parser for the actually displayed source/generator subset."""
 t=t.replace(r'\pi','pi').replace('⁡','').replace('π','pi').replace('−','-').replace(r'\operatorname{ln}','log').replace(r'\ln','log')
 t=t.replace(r'\text{ }','').replace(r'\,','').replace(r'\:','').replace(r'\!','').replace(r'\left','').replace(r'\right','')
 def group(s,i):
  if s[i]!='{': raise ValueError('group required')
  depth=1;j=i+1
  while depth:
   if j>=len(s):raise ValueError('unbalanced group')
   depth+=(s[j]=='{')-(s[j]=='}');j+=1
  return s[i+1:j-1],j
 while r'\frac' in t or r'\sqrt' in t:
  positions=[(t.find(c),c) for c in [r'\frac',r'\sqrt'] if c in t];i,c=min(positions);a,j=group(t,i+len(c))
  if c==r'\frac':b,k=group(t,j);rep='(('+str(parse_math(a))+')/('+str(parse_math(b))+'))';j=k
  else:rep='sqrt('+str(parse_math(a))+')'
  t=t[:i]+rep+t[j:]
 for c in ['cos','sin','log']:t=t.replace('\\'+c,c)
 t=t.replace('^{','**(').replace('{','(').replace('}',')').replace('^','**')
 if '\\' in t:raise ValueError('unsupported command '+t)
 return parse_expr(t,local_dict=LOC,transformations=TRANS,evaluate=True)
def displacement(p,q):return f'⟨{tex(X-p)},\\,{tex(Y-q)}⟩'
def line(u,v,p,q):return f'⟨{tex(u)},{tex(v)}⟩\\cdot {displacement(p,q)}=0'
def read_line(s):
 m=re.fullmatch(r'⟨(.*?),(.*?)⟩\s*\\cdot\s*⟨(.*?),(.*?)⟩\s*=\s*0',s)
 if not m:raise ValueError('invalid whole line '+s)
 u,v,a,b=map(parse_math,m.groups());return sp.expand(u*a+v*b)
def line_key(expr):
 poly=sp.Poly(expr,X,Y);a=poly.coeff_monomial(X);b=poly.coeff_monomial(Y);c=poly.coeff_monomial(1)
 if not (a or b):raise ValueError('zero/constant line')
 scale=a if a else b;return tuple(sp.simplify(t/scale) for t in (a,b,c))
def equivalent(a,b):return line_key(a)==line_key(b)
def scaled_tex(original,r,s):
 # Token masking prevents variable replacement inside command names/arguments.
 return re.sub(r'\\[A-Za-z]+|[xy]',lambda m:m.group() if m.group().startswith('\\') or (r if m.group()=='x' else s)==1 else '('+tex(r if m.group()=='x' else s)+m.group()+')',original)
def subst_tex(e,p,q):
 t=tex(e)
 # Generated SymPy TeX has single-letter coordinate tokens; command protection.
 return re.sub(r'\\[A-Za-z]+|[xy]',lambda m:m.group() if m.group().startswith('\\') else '('+tex(p if m.group()=='x' else q)+')',t)
def bounds(e):
 if e.is_Rational and (abs(e.p)>200 or e.q>27):raise ValueError('arithmetic ceiling')
 if e.has(sp.oo,sp.zoo,sp.nan):raise ValueError('nonfinite')
def source_data(profile,parameters):
 h=PROFILES[profile.split(':',1)[1]];p=dict(parameters or {'r':1,'s':1})
 if set(p)!={'r','s'}:raise ValueError('raw parameters are r,s')
 r,s=(sp.sympify(p[k]) for k in ('r','s'))
 if any(v.is_Integer is not True or not 1<=v<=3 for v in (r,s)):raise ValueError('raw scale 1..3')
 f0=sp.sympify(h['expression'],locals=LOC);p0,q0=[sp.sympify(v,locals=LOC) for v in h['point']]
 f=f0.subs({X:r*X,Y:s*Y},simultaneous=True);pt=(p0/r,q0/s);g=(sp.diff(f,X).subs({X:pt[0],Y:pt[1]}),sp.diff(f,Y).subs({X:pt[0],Y:pt[1]}))
 return h,p,f,pt,tuple(map(sp.simplify,g)),r,s

def authored_solution(f,p,q):
 dx,dy=sp.diff(f,X),sp.diff(f,Y);u,v=[sp.simplify(d.subs({X:p,Y:q})) for d in (dx,dy)]
 return (r'The equation of the tangent line to the level curve $f(x,y)=k$ at the point $({x}_{0},{y}_{0})$ can be expressed as'+'\n\n$$\n'+r'∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩=0.'+'\n$$\n\n'+
 f'First, we find the gradient of $f(x,y)$ and evaluate it at $(x,y)=({tex(p)},{tex(q)}):$\n\n$$\n'+
 r'\begin{aligned}∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j \\  & ='+
 f'\\frac{{∂}}{{∂x}}({tex(f)})\\,i+\\frac{{∂}}{{∂y}}({tex(f)})\\,j \\\\  & =({tex(dx)})\\,i+({tex(dy)})\\,j \\\\ ∇f({tex(p)},{tex(q)}) & =({subst_tex(dx,p,q)})\\,i+({subst_tex(dy,p,q)})\\,j \\\\  & =({tex(u)})\\,i+({tex(v)})\\,j \\\\  & =⟨{tex(u)},{tex(v)}⟩\\end{{aligned}}\n$$\n\n'+
 r'Now, the Cartesian equation of the tangent line to the level curve that passes through the point $({x}_{0},{y}_{0})$ can be written as'+'\n\n$$\n'+
 r'\begin{aligned}∇f({x}_{0},{y}_{0})\cdot ⟨x-{x}_{0},\,y-{y}_{0}⟩ & =0 \\ '+f'∇f({tex(p)},{tex(q)})\\cdot ⟨x-({tex(p)}),\\,y-({tex(q)})⟩ & =0 \\\\ ⟨{tex(u)},{tex(v)}⟩\\cdot {displacement(p,q)} & =0.\\end{{aligned}}\n$$')

def raw_solution(h,f,p,q,u,v,r,s):
 slots=h['solution_slots'];vals={}
 for k,orig in slots.items():
  if k=='F':vals[k]=scaled_tex(orig,r,s)
  elif k in ('DX','DY'):
   factor=r if k=='DX' else s;vals[k]=scaled_tex(orig,r,s) if factor==1 else tex(factor)+'('+scaled_tex(orig,r,s)+')'
  elif k in ('EX','EY'):
   vals[k]=orig if r==s==1 else '('+subst_tex(sp.diff(f,X if k=='EX' else Y),p,q)+')'
  elif k=='P':vals[k]=h['point_tex'] if r==s==1 else '('+tex(p)+','+tex(q)+')'
  elif k=='BASIS':vals[k]=orig if r==s==1 else '('+tex(u)+r')\,i+('+tex(v)+r')\,j'
  elif k=='GRAD':vals[k]='⟨'+tex(u)+','+tex(v)+'⟩'
  elif k=='DISP_RAW':vals[k]=orig if r==s==1 else '⟨x-('+tex(p)+r'),\,y-('+tex(q)+')⟩'
  elif k=='DISP':vals[k]=orig if r==s==1 else displacement(p,q)
 return re.sub(r'@@(\w+)@@',lambda m:vals[m.group(1)],h['solution_mask']) if h['solution_mask'] else None

def make_record(level,seed,template,p,profile,f,point,values,correct,problem,solution,origin,raw_h=None):
 # Complete bank/prompt/fixed solution, independent of choice order, own identity.
 identity={'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(values),'correct':None if correct is None else values[correct],'difficulty':None if raw_h and ':question/difficulty' not in raw_h['raw_keys'] else level}
 qid=uid(identity);fid=uid([qid,'selection']);answers=[{':answer/id':uid([fid,i,v]),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
 # Stable identity uses content; duplicate raw values still receive distinct owned IDs.
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers.copy()}
 if correct is not None:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
 random.Random(seed).shuffle(field[':answer-field/choices'])
 question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
 if solution is not None:question[':question/worked-solution']=solution
 if not raw_h or ':question/difficulty' in raw_h['raw_keys']:question[':question/difficulty']=':question.difficulty/'+level
 dx,dy=sp.diff(f,X),sp.diff(f,Y);g=[sp.simplify(e.subs({X:point[0],Y:point[1]})) for e in (dx,dy)]
 # Assessment includes partial derivatives evaluated at P and line; constants and
 # all bank/layout aliases are absent. Equivalent scalar function rescaling is
 # normalized to avoid inflating the number of meaningful tangent tasks.
 scale=next(c for c in sp.Poly(sp.expand(f),X,Y).coeffs() if c) if f.is_polynomial(X,Y) else 1
 task=[sp.srepr(sp.simplify(dx/scale)),sp.srepr(sp.simplify(dy/scale)),*[sp.srepr(x) for x in point],*[str(x) for x in line_key(g[0]*(X-point[0])+g[1]*(Y-point[1]))]]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile,'source_id':None if raw_h is None else raw_h['source_id'],'parameters':{k:str(v) for k,v in p.items()},'seed':seed,'origin':origin,'evidence_only':profile.startswith(('raw:','completed:')),'eligible_for_learning':not profile.startswith(('raw:','completed:')),'source':SOURCE,'mathematical_fingerprint':digest(task),'content_fingerprint':digest(identity),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'domain':'real, finite; gradient nonzero','recipes':(['covector coordinate pullback; historical intention unresolved'] if raw_h else (['gradient','flip x component','swap components','reverse x coordinate','reverse y coordinate'] if profile=='method:regular' else ['gradient','omit xy contribution to x derivative','omit xy contribution to y derivative','swap components','flip x component'] if profile=='method:product' else ['gradient','swap components','replace sin evaluation by 1','omit y coordinate','reverse y coordinate']))}}

# EASY observed families, with explicitly authored safe default banks.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE authored canonical polynomial workload: integer point.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD authored same polynomial workload: familiar reduced rational point.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def normal_data(level,template,p):
 if set(p)!={'a','b','c','p','q'}:raise ValueError('parameters require a,b,c,p,q')
 a,b,c,pt,qt=[sp.sympify(p[k],locals=LOC) for k in ('a','b','c','p','q')]
 limit=5 if level=='easy' else 6
 if any(v.is_Integer is not True or not 1<=abs(v)<=limit for v in (a,b,c)):raise ValueError('nonzero signed bounded integer coefficients')
 if template=='trig_cubic':
  if level!='easy' or a!=1 or pt!=sp.sqrt(sp.pi) or qt.is_Integer is not True or not 1<=abs(qt)<=2:raise ValueError('familiar trig input only')
 else:
  if any(v.is_Rational is not True for v in (pt,qt)):raise ValueError('rational coordinates')
  if level=='hard':
   if any(v.q not in (2,3) or not 1<=abs(v.p)<=5 for v in (pt,qt)):raise ValueError('hard reduced rational bounds')
  elif any(v.is_Integer is not True or not 1<=abs(v)<=(2 if level=='easy' else 3) for v in (pt,qt)):raise ValueError('nonzero bounded integer coordinates')
 if level=='easy' and template not in TEMPLATES:raise ValueError('easy template must be observed family')
 if level in ('moderate','hard') and template!='canonical':raise ValueError('authored level canonical family only')
 families={'cross_cubic':a*X**2+b*X*Y**2+c*Y,'trig_cubic':sp.cos(X**2)+b*Y**3,'log_quadratic':sp.log(abs(a)*X**2+abs(b)*Y**2+abs(c)),'quadratic':a*X**2+b*X*Y+c*Y**2,'product':a*X**2*Y**2+b*X*Y,'cubic_linear':a*X*Y**2+b*X+c*Y,'cubic_xy':a*X*Y**2+b*X*Y+c*X,'canonical':a*X**2+b*Y**2+c*X*Y**2}
 if template not in families:raise ValueError('unknown template')
 f=families[template];g=tuple(sp.simplify(sp.diff(f,z).subs({X:pt,Y:qt})) for z in (X,Y))
 for e in g:bounds(e)
 if g==(0,0):raise ValueError('singular gradient')
 return f,(pt,qt),g

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('sources are radio only')
 rng=random.Random(seed)
 if profile and profile.startswith(('raw:','completed:')):
  if level!='easy':raise ValueError('raw/completed source scope is easy or unrated authored-easy only')
  h,p,f,(pt,qt),(u,v),r,s=source_data(profile,parameters)
  if template not in (None,h['template']):raise ValueError('profile/template mismatch')
  problem=h['prompt_mask'].replace('@@F@@',scaled_tex(h['function_tex'],r,s)).replace('@@P@@',h['point_tex'] if r==s==1 else '('+tex(pt)+','+tex(qt)+')')
  values=[mask.replace('@@VECTOR@@',(h['vector_tex'][i] if r==s==1 else '⟨'+tex(r*sp.sympify(vector[0]))+','+tex(s*sp.sympify(vector[1]))+'⟩')).replace('@@D@@',h['displacement_tex'][i] if r==s==1 else displacement(pt,qt)[1:-1]) for i,(vector,mask) in enumerate(zip(h['vectors'],h['choice_masks']))]
  solution=raw_solution(h,f,pt,qt,u,v,r,s);ci=h['correct_index'];raw_h=h
  if profile.startswith('completed:'):
   if ci is None:
    exact=[i for i,(a,b) in enumerate(h['vectors']) if sp.simplify(r*sp.sympify(a)-u)==0 and sp.simplify(s*sp.sympify(b)-v)==0]
    if len(exact)!=1:raise ValueError('missing source key has no unique exact-gradient representation')
    ci=exact[0] # independently inferred canonical gradient representation; not original key
   if solution is None:solution=authored_solution(f,pt,qt)
   raw_h=None
  rec=make_record(level,seed,h['template'],p,profile,f,(pt,qt),values,ci,problem,solution,'observed raw' if raw_h else 'inferred completion; opaque bank',raw_h)
  rec['generation']['source_id']=h['source_id']
  rec['generation']['completion_inferences']=[k for k in (':question/difficulty',':question/worked-solution',':answer-field/correct') if (k not in h['raw_keys'] if k.startswith(':question') else k not in h['field_keys'])] if profile.startswith('completed:') else []
  return rec
 template=template or (rng.choice(list(TEMPLATES)) if level=='easy' else 'canonical')
 selected=profile or ('method:horizontal' if template=='trig_cubic' else 'method:product' if template=='product' else 'method:regular') # WHOLE bank selected before parameters
 if selected not in ('method:regular','method:horizontal','method:product') or (selected=='method:horizontal')!=(template=='trig_cubic') or (selected=='method:product')!=(template=='product'):raise ValueError('ineligible profile')
 for attempt in range(1000):
  p=parameters or {'a':rng.choice([i for i in range(-(5 if level=='easy' else 6),(5 if level=='easy' else 6)+1) if i]),'b':rng.choice([i for i in range(-(5 if level=='easy' else 6),(5 if level=='easy' else 6)+1) if i]),'c':rng.choice([i for i in range(-(5 if level=='easy' else 6),(5 if level=='easy' else 6)+1) if i]),'p':rng.choice([-2,-1,1,2] if level=='easy' else [-3,-2,-1,1,2,3]),'q':rng.choice([-2,-1,1,2] if level=='easy' else [-3,-2,-1,1,2,3])}
  if parameters is None and level=='hard':
   p={**p,'p':rng.choice([sp.Rational(n,d) for d in (2,3) for n in range(-5,6) if n and sp.gcd(n,d)==1]),'q':rng.choice([sp.Rational(n,d) for d in (2,3) for n in range(-5,6) if n and sp.gcd(n,d)==1])}
  if parameters is None and template=='trig_cubic':p={**p,'a':1,'p':'sqrt(pi)'}
  try:
   f,(pt,qt),(u,v)=normal_data(level,template,p)
   if selected=='method:regular':
    if not u or not v or u==v or u==-v:raise ValueError('regular bank requires two unequal nonzero components')
    values=[line(u,v,pt,qt),line(-u,v,pt,qt),line(v,u,pt,qt),line(u,v,-pt,qt),line(u,v,pt,-qt)]
   elif selected=='method:product':
    a=sp.sympify(p['a']);b=sp.sympify(p['b'])
    values=[line(u,v,pt,qt),line(2*a*pt*qt**2,v,pt,qt),line(u,2*a*qt*pt**2,pt,qt),line(v,u,pt,qt),line(-u,v,pt,qt)]
   else:values=[line(u,v,pt,qt),line(v,u,pt,qt),line(-2*pt,v,pt,qt),line(u,v,pt,0),line(u,v,pt,-qt)]
   keys=[line_key(read_line(z)) for z in values]
   if len(set(keys))!=5:raise ValueError('whole bank collision')
  except ValueError:
   if parameters is not None:raise
   continue
  problem=f'Given the function $f(x,y)={tex(f)}$, find the equation of the tangent line to the level curve that passes through the point where $(x,y)=({tex(pt)},{tex(qt)}).$'
  return make_record(level,seed,template,p,selected,f,(pt,qt),values,0,problem,authored_solution(f,pt,qt),'observed family / authored bank' if level=='easy' else 'authored missing-level family')
 raise ValueError('no eligible whole instance')

def markdown(record,label=None):
 q=record['question'];g=record['generation'];s=f"### {label or g['template']} — {q.get(':question/difficulty','unrated')} — {g['origin']}\n\n{q[':question/problem']}\n\n"
 for field in q.get(':question/answer-fields',[]):
  correct=field.get(':answer-field/correct',[None,None])[1]
  for a in field[':answer-field/choices']:s+=('- [x]' if a[':answer/id']==correct else '- [ ]')+' $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==correct else '')+'\n'
 if ':question/worked-solution' in q:s+='\n'+q[':question/worked-solution']+'\n'
 else:s+='\n*Original worked solution absent.*\n'
 if any(':answer-field/correct' not in f for f in q.get(':question/answer-fields',[])):s+='\n*Original correct designation absent; the separate completion shows the inferred gradient representation.*\n'
 return s+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else ''.join(markdown(r) for r in records))
