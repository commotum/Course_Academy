#!/usr/bin/env python3
"""Draft nonlinear exponential chain rule generator, captured math basis 1356.
Parameterized source masks retain complete family-specific worked chains.
Public observed:<q-id> profiles are evidence-only; authored method banks are
normal defaults. No registration, transactions, plots or engine changes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
KP=17592186092263
ROOT=Path(__file__).with_suffix('')
CAP=json.loads((ROOT/'source.json').read_text())
SRC={q[':question/math-academy-id']:q for q in CAP['record'][':knowledge-point/questions']}
X,U,H=s.symbols('x u h', real=True)
VERSION='nonlinear-chain-1'
# Each source has its own prompt/solution mask; differences in product and
# exponent-restoration rows and endpoint rows remain operative, not row counts.
SPECS={
'q-1953':('easy',dict(a=1,n=2,b=0,c=0),'derivative'),
'q-48628':('easy',dict(a=1,n=4,b=0,c=1),'derivative'),
'q-340948':('moderate',dict(a=-2,n=6,b=5,c=0,t=1),'slope'),
'q-340955':('moderate',dict(a=-3,n=1,b=0,c=0,t='1/3'),'slope'),
'q-167329':('moderate',dict(a=-4,scale='1/2'),'trig_product'),
'q-167783':('moderate',dict(a=-4,scale='1/2'),'trig_quotient'),
'q-107437':('easy',dict(a=1,n=5,b=0,c=1),'derivative'),
'q-107445':('easy',dict(a=1,n=2,b=-2,c=0),'derivative'),
'q-107449':('moderate',dict(a=3,n=2,b=0,c=-3,t=-1),'slope'),
'q-107452':('moderate',dict(a=1,n=3,b=-4,c=0,t=2),'slope'),
'q-312451':('easy',dict(a=4,n=5,b=0,c=0),'derivative'),
'q-340949':('moderate',dict(a=4,n=3,b=0,c=0,t=1),'slope'),
'q-48629':('easy',dict(a=-2,n=3,b=0,c=8),'derivative'),
'q-71873':('moderate',dict(a=2,n=4,b=0,c=0),'derivative'),
}
OPAQUE={'q-107437','q-107449','q-107452','q-71873'}
NORMAL={l:[k for k,v in SPECS.items() if v[0]==l and k!='q-340955'] for l in ('easy','moderate')}
NORMAL['hard']=['two_power_slope']

def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(v,sort_keys=True,separators=(',',':'))))
def content_identity(problem,solution,values,difficulty,field_type,key,designation):
 return uid([VERSION,problem,solution,sorted(values),difficulty,field_type,key,designation])

def exact(v):
 if isinstance(v,bool): raise ValueError('Boolean coefficient')
 z=s.sympify(v)
 if z.free_symbols or not z.is_Rational: raise ValueError('Exact rational parameters required')
 return z

def latex(e):
 return s.latex(e).replace(r'\log',r'\ln')
def power(v,n):
 return v if n==1 else (v+'^{'+str(n)+'}' if v.startswith('(') else '{'+v+'}^{'+str(n)+'}')
def term(a,n,v='x'):
 if a==0:return ''
 z=power(v,n) if n else ''
 return ('-' if a==-1 and z else '' if a==1 and z else latex(a))+z

def polytex(p,deriv=False,v='x'):
 a,n,b,c=p['a'],int(p['n']),p.get('b',0),p.get('c',0)
 if 'm' in p:
  parts=[term(a*n,n-1,v),term(b*int(p['m']),int(p['m'])-1,v)] if deriv else [term(a,n,v),term(b,int(p['m']),v),term(c,0,v)]
 else: parts=[term(a*n,n-1,v),term(b,0,v)] if deriv else [term(a,n,v),term(b,1,v),term(c,0,v)]
 # q48629 uses constant-first order; preserve this structure on changes.
 if p.get('constant_first') and not deriv:parts=[parts[-1]]+parts[:-1]
 out=''
 for z in parts:
  if z:out+=('+' if out and not z.startswith('-') else '')+z
 return out or '0'

def mathdata(p,kind):
 if kind.startswith('trig'):
  g=p['a']*s.sin(X); d=p['a']*s.cos(X); f=p['scale']*s.exp(g)
 else:
  g=p['a']*X**p['n']+p.get('b',0)*X**p.get('m',1)+p.get('c',0);d=s.diff(g,X);f=s.exp(g)
 ans=s.diff(f,X)
 if kind=='slope':ans=ans.subs(X,p['t'])
 if kind=='trig_product':ans=p['scale']*d
 if kind=='trig_quotient':ans=-p['scale']*d
 return g,d,f,s.simplify(ans)

def prepare(template,parameters,observed):
 if template=='two_power_slope': anchor=dict(a=1,n=3,b=-1,m=2,c=1,t=2);kind='slope';level='hard'
 else:level,anchor,kind=SPECS[template]
 p=dict(anchor if parameters is None else parameters)
 required=set(anchor)
 if set(p)!=required:raise ValueError(f'Expected complete parameters {sorted(required)}')
 p={k:exact(v) for k,v in p.items()}
 for k in ('n','m'):
  if k in p and p[k].q!=1:raise ValueError('Integer powers required')
 if not kind.startswith('trig') and any(p[k].q!=1 for k in ('a','b','c')):raise ValueError('Integer polynomial coefficients required')
 if template=='q-48629':p['constant_first']=True
 if observed:
  # Raw profiles are parameterized evidence, not a scope-guard bypass.
  if kind.startswith('trig'):
   if p['a'] not in (-2,-3,-4,-5,-6) or p['scale'] not in (s.Rational(1,2),s.Rational(1,3),s.Rational(2,3)):raise ValueError('Observed trig workload bounds')
  else:
   if not 1<=abs(p['a'])<=6 or not 1<=p['n']<=6 or abs(p.get('b',0))>5 or abs(p.get('c',0))>8:raise ValueError('Observed polynomial workload bounds')
   if (p['n']==1)!=(template=='q-340955'):raise ValueError('Only captured linear exception admits n=1')
   for k in ('b','c'):
    if bool(anchor.get(k,0))!=bool(p.get(k,0)):raise ValueError('Preserve observed primitive support')
   if kind=='slope' and (abs(p['t'])>2 or p['t']==0):raise ValueError('Observed evaluation bounds')
 if not observed:
  if kind.startswith('trig'):
   if p['a'] not in (-2,-3,-4,-5,-6) or p['scale'] not in (s.Rational(1,2),s.Rational(1,3),s.Rational(2,3)):raise ValueError('Moderate trig bounds')
  else:
   if not 1<=abs(p['a'])<=4 or not 2<=p['n']<=6 or abs(p.get('b',0))>5 or abs(p.get('c',0))>8:raise ValueError('Polynomial workload bounds')
   # Keep template's real terms, preventing collapse into another workload.
   for k in ('b','c'):
    if bool(anchor.get(k,0))!=bool(p.get(k,0)):raise ValueError('Preserve polynomial component support')
   if kind=='slope' and template!='two_power_slope' and p['t'] not in (-2,-1,1,2):raise ValueError('Familiar integer evaluation points')
   if template=='two_power_slope':
    if p['n'] not in (3,4) or p['m']!=2 or not 1<=abs(p['a'])<=3 or not 1<=abs(p['b'])<=3 or p['t'] not in (-2,2) or abs(p['c'])>4:raise ValueError('Hard requires two nonlinear powers and nonunit evaluation')
   g,d,_,ans=mathdata(p,kind)
   if kind=='slope' and (abs(g.subs(X,p['t']))>40 or abs(d.subs(X,p['t']))>100 or d.subs(X,p['t'])==0):raise ValueError('Evaluation arithmetic bounds or degenerate slope')
 return p,kind,level

def rendered_components(p,kind):
 g,d,f,ans=mathdata(p,kind)
 if kind.startswith('trig'):
  G=latex(p['a'])+r'\operatorname{sin}⁡x';D=latex(p['a'])+r'\operatorname{cos}⁡x'
  return g,d,f,ans,G,D
 return g,d,f,ans,polytex(p),polytex(p,True)

def masked_text(template,p,kind):
 """Replace only complete mathematical components, longest first, in a source mask.
 No seed or chosen error is involved. Anchors describe syntax, never answer lookup.
 """
 q=SRC[template];anchor={k:exact(v) for k,v in SPECS[template][1].items()}
 if template=='q-48629':anchor['constant_first']=True
 _,_,_,oldans,oldG,oldD=rendered_components(anchor,kind)
 g,d,f,ans,G,D=rendered_components(p,kind)
 replacements=[]
 def slot(old,new):
  if old!=new:replacements.append((old,new))
 if kind.startswith('trig'):
  # Whole trig components protect x in command names and function labels.
  for parens in (False,True):
   arg='(x)' if parens else 'x'
   for op in ('sin','cos'):
    old=latex(anchor['a'])+r'\operatorname{'+op+'}⁡'+arg
    new=latex(p['a'])+r'\operatorname{'+op+'}⁡'+arg
    slot(old,new)
   slot(latex(-anchor['a'])+r'\operatorname{sin}⁡'+arg,latex(-p['a'])+r'\operatorname{sin}⁡'+arg)
   slot(latex(anchor['a']*anchor['scale'])+r'\operatorname{cos}⁡'+arg,latex(p['a']*p['scale'])+r'\operatorname{cos}⁡'+arg)
   slot(latex(-anchor['a']*anchor['scale'])+r'\operatorname{cos}⁡'+arg,latex(-p['a']*p['scale'])+r'\operatorname{cos}⁡'+arg)
  slot(latex(anchor['scale'])+'{e}',latex(p['scale'])+'{e}')
  slot(latex(anchor['a']*anchor['scale'])+'{e}',latex(p['a']*p['scale'])+'{e}')
 else:
  # Endpoint components must precede the symbolic masks.
  if kind=='slope':
   t0=anchor['t']; t=p['t']; v0='('+str(t0)+')';v='('+str(t)+')'
   # source spells 2^3 differently from (-1)^2: include actual spellings.
   for old,new in [(polytex(anchor,True,v0),polytex(p,True,v)),(polytex(anchor,False,v0),polytex(p,False,v))]:slot(old,new)
   if template=='q-107452' and (G!=oldG or t!=t0):slot('{2}^{3}-4(2)',polytex(p,False,v))
   od=s.diff(anchor['a']*X**anchor['n']+anchor.get('b',0)*X+anchor.get('c',0),X).subs(X,t0)
   og=(anchor['a']*X**anchor['n']+anchor.get('b',0)*X+anchor.get('c',0)).subs(X,t0)
   nd=d.subs(X,t);ng=g.subs(X,t)
   # complete evaluated exponentials and scalar-final rows, not isolated digits
   for cdot in ('',r'\cdot '):slot(latex(od)+cdot+'{e}^{'+latex(og)+'}',latex(nd)+cdot+'{e}^{'+latex(ng)+'}')
   slot('x='+latex(t0),'x='+latex(t));slot('x='+str(t0),'x='+str(t))
   if og==0:
    slot('& ='+latex(od)+r'\end{aligned}','& ='+latex(ans)+r'\end{aligned}')
  slot(oldG,G);slot(oldD,D)
  if template=='q-48628' and oldG!=G:slot('x^{4} + 1',G)
 # Use masks so one replacement cannot corrupt another inserted component.
 def apply(txt):
  mp={}; ordered=sorted(set(replacements),key=lambda z:len(z[0]),reverse=True)
  for i,(old,new) in enumerate(ordered):
   token=f'@@COMPONENT{i}@@';txt=txt.replace(old,token);mp[token]=new
  for token,new in mp.items():txt=txt.replace(token,new)
  return txt
 problem=apply(q[':question/problem']);solution=apply(q.get(':question/worked-solution',''))
 if D.startswith('-'):solution=solution.replace(r'{e}^{u}\cdot '+D,r'{e}^{u}\cdot ('+D+')')
 return problem,solution

def authored_solution(p,kind,name='y'):
 g,d,f,ans,G,D=rendered_components(p,kind)
 outer=latex(p.get('scale',1)) if p.get('scale',1)!=1 else ''
 if kind.startswith('trig'):inner='h';G=latex(g);D=latex(d)
 else:inner='u'
 du=rf'\frac{{\text{{d}}{name}}}{{\text{{d}}{inner}}}';dx=rf'\frac{{\text{{d}}{name}}}{{\text{{d}}x}}';idiff=rf'\frac{{\text{{d}}{inner}}}{{\text{{d}}x}}'
 solution=f'First, we express ${name}$ as the composite function\n\n$$\n{name}={outer}e^{{{inner}}},\\,{inner}={G}.\n$$\n\nDifferentiating gives\n\n$$\n{du}={outer}e^{{{inner}}},\\,{idiff}={D}.\n$$\n\nWe now apply the chain rule and get\n\n$$\n'+rf'\begin{{aligned}}{dx} & ={du}\cdot {idiff} \\ & ={outer}e^{{{inner}}}\cdot ({D}) \\ & ={outer}({D})e^{{{inner}}} \\ & ={latex(s.diff(f,X))}.\end{{aligned}}'+'\n$$'
 if kind=='slope':
  t=p['t'];dv=d.subs(X,t);gv=g.subs(X,t)
  solution+=f'\n\nFinally, to find the slope $m$ of the tangent to the curve at $x={latex(t)}$, we have to evaluate ${dx}$ at that point as follows:\n\n$$\n'+rf'\begin{{aligned}}m={dx}|_{{x={latex(t)}}} & =({D})e^{{{G}}}|_{{x={latex(t)}}} \\ & =({polytex(p,True,"("+latex(t)+")")})e^{{{polytex(p,False,"("+latex(t)+")")}}} \\ & ={latex(dv)}\cdot e^{{{latex(gv)}}} \\ & ={latex(ans)}.\end{{aligned}}'+'\n$$'
 return solution

def bank(template,p,kind,observed):
 g,d,f,ans,_,_=rendered_components(p,kind);a=p['a'];n=p.get('n');b=p.get('b',0);c=p.get('c',0);E=s.exp(g)
 if kind.startswith('trig') or (template in SRC and SRC[template][':question/answer-fields'][0][':answer-field/type'][':db/ident'].endswith('/blank')):return [ans]
 if not observed:
  if kind=='slope':
   t=p['t'];v=d.subs(X,t);w=g.subs(X,t)
   return [ans,s.exp(w),v,v*s.exp(-w),-ans]
  return [ans,E,d,d+s.exp(g),-ans]
 if template=='q-1953':return [a*X**(n-1)*E,s.exp(n*g),a*n*E,ans,g]
 if template=='q-48628':return [a*n*X**(n+1)*E,d+E,ans,a*n*X**n*E,a*n*X**(n+1)+E]
 if template=='q-107437':return [-ans,ans,a*X**n*E,s.Rational(1,n)*X**(n-3)*E,(n-1)*a*X**n*E]
 if template=='q-107445':return [a*n*X**n*E,a*n*E,(a*n*X**(n-1)-b)*E,ans,a*n*X**(n-1)*E]
 if template=='q-48629':return [-ans,(c+d)*E,-a*n*X**(n+1)*E,ans,a*n*X**(n+1)*E]
 if template=='q-71873':return [a*n*X*s.exp(X**(n-2)),a*n*X**(n-1)*s.exp(X**(n-1)),(a*n+1)*X**(n-2)*s.exp(a*n*X**n),ans,n*X**(n-2)*E]
 if template=='q-107449':
  v=d.subs(X,p['t']);return [ans,-v*s.E,v*s.exp(a),-v*s.exp(-a),s.E/a]
 if template=='q-107452':return [-ans,a*n*p['t']**(n-1),a*n*p['t'],b,ans]
 raise ValueError('No observed bank')

# Easy: direct nonlinear polynomial chain differentiation, observed powers 2–5.
# Moderate: source-shaped tangent evaluation, trig fragments or the observed
# weighted-monomial derivative family; all source labels are retained on replay.
# Hard (authored): two nonlinear primitive derivatives plus signed evaluation
# at ±2, same exponential chain, no general base/product/implicit branch.
def sample(template,rng):
 if template=='two_power_slope':return dict(a=rng.choice([-3,-2,-1,1,2,3]),n=rng.choice([3,4]),b=rng.choice([-3,-2,-1,1,2,3]),m=2,c=rng.choice([-4,-3,-2,-1,1,2,3,4]),t=rng.choice([-2,2]))
 _,anchor,kind=SPECS[template]
 if kind.startswith('trig'):return dict(a=rng.choice([-2,-3,-4,-5,-6]),scale=rng.choice(['1/2','1/3','2/3']))
 p=dict(a=rng.choice([-4,-3,-2,-1,1,2,3,4]),n=rng.choice([2,3,4,5,6]),b=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) if anchor['b'] else 0,c=rng.choice([-8,-6,-4,-2,-1,1,2,4,6,8]) if anchor['c'] else 0)
 if kind=='slope':p['t']=rng.choice([-2,-1,1,2])
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in NORMAL:raise ValueError('Unknown difficulty')
 observed=bool(profile and profile.startswith('observed:'))
 if observed:
  source=profile.split(':',1)[1]
  if template is not None and template!=source:raise ValueError('Profile/template mismatch')
  template=source
 if profile not in (None,'method') and not observed:raise ValueError('Unknown complete bank')
 rng=random.Random(seed)
 if template is None:
  eligible=[k for k in NORMAL[level] if not field_type or default_field(k)==field_type]
  if not eligible:raise ValueError('No eligible template')
  template=rng.choice(eligible)
 if template not in NORMAL[level] and not(observed and template in SPECS):raise ValueError('Template difficulty mismatch')
 for attempt in range(1000):
  try:
   p,kind,actual=prepare(template,parameters if parameters is not None else (None if observed else sample(template,rng)),observed)
   if actual!=level:raise ValueError('Template difficulty mismatch')
   vals=bank(template,p,kind,observed)
   if any(s.simplify(v-w)==0 for i,v in enumerate(vals) for w in vals[i+1:]):raise ValueError('Ambiguous complete bank')
   break
  except ValueError:
   if parameters is not None or observed:raise
 else:raise ValueError('No valid complete instance')
 g,d,f,ans=mathdata(p,kind)
 if template in SRC:
  problem,solution=masked_text(template,p,kind)
  sourceq=SRC[template];sf=sourceq[':question/answer-fields'][0];ft=sf[':answer-field/type'][':db/ident'].split('/')[-1];key=sf[':answer-field/key']
 else:
  problem=f'Find the slope $m$ of the tangent to the curve $y=e^{{{polytex(p)}}}$ at the point where $x={latex(p["t"])}.$\n\n$m=$\n{{{{field-1}}}}';solution=authored_solution(p,kind);ft='blank';key='field-1'
 if field_type and field_type!=ft:raise ValueError('Source field layout required')
 if not observed:
  if kind.startswith('trig'):
   # Captured prompt omitted f and h: add supported complete definitions.
   defs=rf'Here $f(h)={latex(p["scale"])}e^h$ and $h(x)={latex(p["a"])}\sin x$.'
   opening,separator,layout=problem.partition('\n')
   problem=opening+'\n\n'+defs+'\n'+layout
  if template=='q-48628':solution=authored_solution(p,kind)
 # ID based on full learner content and actual difficulty, order-independent.
 vals_tex=[latex(v) for v in vals]
 difficulty=sourceq.get(':question/difficulty',{}).get(':db/ident') if observed else ':question.difficulty/'+level
 designation='missing' if observed and ':answer-field/correct' not in sourceq[':question/answer-fields'][0] else latex(ans)
 qid=content_identity(problem,solution,vals_tex,difficulty,ft,key,designation);fid=uid([qid,key]);answers=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in vals_tex]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers}
 if not(observed and ':answer-field/correct' not in sourceq[':question/answer-fields'][0]):field[':answer-field/correct']=[':answer/id',answers[next(i for i,v in enumerate(vals) if s.simplify(v-ans)==0)][':answer/id']]
 if ft=='radio':rng.shuffle(answers)
 question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
 if solution:question[':question/worked-solution']=solution
 if difficulty:question[':question/difficulty']=difficulty
 # derivative-only additive shifts do affect e^g and hence assessed derivative;
 # unlike incidental prompt shifts they remain in this mathematical fingerprint.
 task=uid(['slope' if kind=='slope' else 'derivative',s.srepr(s.diff(f,X)),str(p.get('t',''))])
 return {'knowledge_point':{'db_id':KP,'id':CAP['record'][':knowledge-point/id'],'title':CAP['record'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile or 'method','parameters':{k:str(v) for k,v in p.items() if k!='constant_first'},'mathematical_fingerprint':task,'source':{k:CAP[k] for k in ('database','basis','lineage')},'evidence_only':observed,'eligible_for_learning':not observed,'inferred_missing_key':template=='q-48628' and not observed,'authored_difficulty':level=='hard' or (template=='q-48628' and not observed),'difficulty_origin':'captured_omission' if observed and template=='q-48628' else 'authored_missing_level' if level=='hard' or (template=='q-48628' and not observed) else 'captured_label','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def default_field(k):return 'blank' if k=='two_power_slope' else SRC[k][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(rec):
 q=rec['question'];out=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):out+='\n'.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
 return out+q.get(':question/worked-solution','[Source has no worked solution.]')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=2);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (NORMAL if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
