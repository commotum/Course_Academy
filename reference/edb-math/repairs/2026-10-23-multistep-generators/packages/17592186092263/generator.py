#!/usr/bin/env python3
"""Portable nonlinear exponential chain-rule generator, source basis 3949.
Observed profiles replay complete source records for evidence only.
Normal questions repair missing definitions and use arithmetic-neighbor banks.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186092263-source-policy.json'))
    raise SystemExit(0)

import sys
sys.dont_write_bytecode=True
import argparse, json, random, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose,normalize_tex,validate_prose,validate_tex,FORMAT_VERSION,validate_generated_record
KP=17592186092263
ROOT=Path(__file__).resolve().parent
CAP=json.loads((ROOT/'source-data.json').read_text())
SRC={q[':question/math-academy-id']:q for q in CAP['material']['kp'][':knowledge-point/questions']}
X,U,H=s.symbols('x u h', real=True)
VERSION='nonlinear-chain-portable-4'
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
'q-340954':('moderate',dict(a=-2,n=7,b=0,c=0,t=1),'slope'),
'q-166076':('moderate',dict(a=-4,scale='1/2'),'trig_full'),
'q-48629':('easy',dict(a=-2,n=3,b=0,c=8),'derivative'),
'q-71873':('moderate',dict(a=2,n=4,b=0,c=0),'derivative'),
'q-71877':('easy',dict(a=2,n=4,b=0,c=3),'derivative'),
'q-167319':('moderate',dict(a=2,n=2,b=4,c=1,k=2),'composite_factor'),
'q-167772':('moderate',dict(a=2,n=2,b=4,c=1,k=2),'composite_factored'),
}
NORMAL={l:[k for k,v in SPECS.items() if v[0]==l and k not in ('q-340955','q-166076')] for l in ('easy','moderate')}


def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(v,sort_keys=True,separators=(',',':'))))
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
 parts=[term(a*n,n-1,v),term(b,0,v)] if deriv else [term(a,n,v),term(b,1,v),term(c,0,v)]
 # q48629 uses constant-first order; preserve this structure on changes.
 if p.get('constant_first') and not deriv:parts=[parts[-1]]+parts[:-1]
 out=''
 for z in parts:
  if z:out+=('+' if out and not z.startswith('-') else '')+z
 return out or '0'

def mathdata(p,kind):
 if kind.startswith('composite'):
  g=p['k']*(p['a']*X**2+p['b']*X+p['c']);d=p['k']*(2*p['a']*X+p['b']);f=s.exp(g)
 elif kind.startswith('trig'):
  g=p['a']*s.sin(X); d=p['a']*s.cos(X); f=p['scale']*s.exp(g)
 else:
  g=p['a']*X**p['n']+p.get('b',0)*X+p.get('c',0);d=s.diff(g,X);f=s.exp(g)
 ans=s.diff(f,X)
 if kind=='slope':ans=ans.subs(X,p['t'])
 if kind=='trig_product':ans=p['scale']*d
 if kind=='trig_quotient':ans=-p['scale']*d
 if kind=='composite_factor':ans=d
 if kind=='composite_factored':ans=d/(2*p['k']*p['a'])
 return g,d,f,s.simplify(ans)

def prepare(template,parameters):
 level,anchor,kind=SPECS[template]
 if set(parameters)!=set(anchor):raise ValueError('Expected complete parameters')
 p={k:exact(v) for k,v in parameters.items()}
 if kind.startswith('trig'):
  if not 1<=abs(p['a'])<=6 or p['a'].q!=1 or p['scale'] not in (s.Rational(1,2),s.Rational(1,3),s.Rational(2,3)):raise ValueError('Trig bounds')
 elif kind.startswith('composite'):
  if p['n']!=2 or p['a'] not in (-3,-2,-1,1,2,3) or p['k'] not in (-3,-2,-1,1,2,3) or p['b']/(2*p['a']) not in (-2,-1,1,2) or abs(p['c'])>4 or p['c'].q!=1:raise ValueError('Composite bounds')
 else:
  if p['a'].q!=1 or not 1<=abs(p['a'])<=4 or p['n'].q!=1 or not 2<=p['n']<=6 or abs(p['b'])>5 or abs(p['c'])>8 or p['b'].q!=1 or p['c'].q!=1:raise ValueError('Polynomial bounds')
  for k in ('b','c'):
   if bool(anchor[k])!=bool(p[k]):raise ValueError('Preserve polynomial component support')
  if kind=='slope':
   if p['t'] not in (-2,-1,1,2):raise ValueError('Evaluation bounds')
   g,d,_,ans=mathdata(p,kind)
   if abs(g.subs(X,p['t']))>12 or abs(d.subs(X,p['t']))>100:raise ValueError('Evaluation workload bounds')
 if template=='q-48629':p['constant_first']=True
 return p,kind,level

def rendered_components(p,kind):
 g,d,f,ans=mathdata(p,kind)
 if kind.startswith('trig'):return g,d,f,ans,latex(g),latex(d)
 return g,d,f,ans,polytex(p),polytex(p,True)

def authored_solution(p,kind,name='y'):
 g,d,f,ans,G,D=rendered_components(p,kind)
 outer=latex(p.get('scale',1)) if p.get('scale',1)!=1 else ''
 if kind.startswith('trig'):inner='h';G=latex(g);D=latex(d)
 else:inner='u'
 du=rf'\frac{{\text{{d}}{name}}}{{\text{{d}}{inner}}}';dx=rf'\frac{{\text{{d}}{name}}}{{\text{{d}}x}}';idiff=rf'\frac{{\text{{d}}{inner}}}{{\text{{d}}x}}'
 solution=f'First, we express ${name}$ as the composite function\n\n$$\n{name}={outer}e^{{{inner}}},\\,{inner}={G}.\n$$\n\nDifferentiating gives\n\n$$\n{du}={outer}e^{{{inner}}},\\,{idiff}={D}.\n$$\n\nWe now apply the chain rule and get\n\n$$\n'+rf'\begin{{aligned}}{dx} & ={du}\cdot {idiff} \\ & ={outer}e^{{{inner}}}\cdot ({D}) \\ & ={outer}({D})e^{{{inner}}} \\ & ={latex(s.diff(f,X))}.\end{{aligned}}'+'\n$$'
 if kind=='trig_quotient':
  solution=solution.replace(r'.\end{aligned}',r' \\ & =-\frac{'+latex(ans)+'}{e^{'+latex(-g)+r'}}.\end{aligned}')
 if kind=='slope':
  t=p['t'];dv=d.subs(X,t);gv=g.subs(X,t)
  solution+=f'\n\nFinally, to find the slope $m$ of the tangent to the curve at $x={latex(t)}$, we have to evaluate ${dx}$ at that point as follows:\n\n$$\n'+rf'\begin{{aligned}}m={dx}|_{{x={latex(t)}}} & =({D})e^{{{G}}}|_{{x={latex(t)}}} \\ & =({polytex(p,True,"("+latex(t)+")")})e^{{{polytex(p,False,"("+latex(t)+")")}}} \\ & ={latex(dv)}\cdot e^{{{latex(gv)}}} \\ & ={latex(ans)}.\end{{aligned}}'+'\n$$'
 return solution

def source_bank(template,p,kind):
 g,d,f,ans,_,_=rendered_components(p,kind);a=p['a'];n=p.get('n');b=p.get('b',0);c=p.get('c',0);E=s.exp(g)
 if kind.startswith('trig') or (template in SRC and SRC[template][':question/answer-fields'][0][':answer-field/type'][':db/ident'].endswith('/blank')):return [ans]
 if template=='q-71877':return [X**(n-3)*s.exp(X**n+c),ans,a*n*X**(n-3)*s.exp(a*X**(n-3)+c),(n+1)*X**(n-2)*s.exp(a*X**n+c+2),a*n*X**(n-3)*s.exp(a*c*X**n+1)]
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


def sample(template,rng):
 """Select sign/parity/evaluation cases before magnitude and decorations."""
 _,anchor,kind=SPECS[template]
 sign=rng.choice([-1,1])
 if kind.startswith('trig'):return dict(a=sign*rng.randint(1,6),scale=rng.choice(['1/2','1/3','2/3']))
 if kind.startswith('composite'):
  r=rng.choice([-2,-1,1,2]);a=sign*rng.randint(1,3)
  return dict(a=a,n=2,b=2*a*r,c=rng.randint(-4,4),k=rng.choice([-3,-2,-1,1,2,3]))
 parity=rng.choice(['even','odd']);n=rng.choice([2,4,6] if parity=='even' else [3,5])
 target=rng.choice([-2,-1,1,2]) if kind=='slope' else None
 p=dict(a=sign*rng.randint(1,4),n=n,b=rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5]) if anchor['b'] else 0,c=rng.choice([-8,-6,-4,-2,-1,1,2,4,6,8]) if anchor['c'] else 0)
 if target is not None:p['t']=target
 return p

def nearby_bank(p,kind,rng):
 """Select an eligible correct rank before choosing compatible error pairs.
 This prevents symmetric neighbor sampling from making the median a shortcut.
 Polynomial banks use leading-coefficient order (then constant), not a test x.
 """
 g,d,f,ans=mathdata(p,kind)
 rank=rng.randrange(5)
 if kind=='slope':
  v=d.subs(X,p['t']);w=g.subs(X,p['t'])
  candidates=[(i,j) for i in range(-8,9) for j in range(-2,3) if (i,j)!=(0,0) and v+i!=0]
  lower=[pair for pair in candidates if float((v+pair[0])*s.exp(pair[1])-v)<0]
  upper=[pair for pair in candidates if pair not in lower]
  pairs=rng.sample(lower,rank)+rng.sample(upper,4-rank)
  return [ans]+[(v+i)*s.exp(w+j) for i,j in pairs],pairs
 a=p['a'];n=p['n'];b=p['b'];E=s.exp(g)
 if b:
  candidates=[(i,j) for i in range(-8,9) for j in range(-2,3) if (i,j)!=(0,0) and a*n+i!=0 and b+j!=0]
 else:candidates=[(i,0) for i in range(-8,9) if i and a*n+i!=0]
 lower=[pair for pair in candidates if pair<(0,0)]
 upper=[pair for pair in candidates if pair>(0,0)]
 pairs=rng.sample(lower,rank)+rng.sample(upper,4-rank)
 return [ans]+[((a*n+i)*X**(n-1)+b+j)*E for i,j in pairs],pairs

def composite_solution(p,kind):
 g,d,f,ans=mathdata(p,kind);base=p['a']*X**2+p['b']*X+p['c']
 final=r'\left('+latex(d)+r'\right)e^{'+latex(s.expand(g))+'}'
 if kind=='composite_factored':final=latex(2*p['k']*p['a'])+'('+latex(ans)+r')e^{'+latex(s.expand(g))+'}'
 return ('First, notice that $y$ is a composite function:\n\n$$\n'+r'\begin{aligned}y&=e^s,\quad s='+latex(p['k']*s.Symbol('g'))+r' \\ s&='+latex(p['k'])+r'\left('+latex(base)+r'\right) \\ &='+latex(s.expand(g))+r'.\end{aligned}'+'\n$$\n\nDifferentiating gives\n\n$$\n'+r'\frac{\mathrm{d}y}{\mathrm{d}s}=e^s,\quad \frac{\mathrm{d}s}{\mathrm{d}x}='+latex(d)+'.\n$$\n\nWe now apply the chain rule and get\n\n$$\n'+r'\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x}&=\frac{\mathrm{d}y}{\mathrm{d}s}\cdot\frac{\mathrm{d}s}{\mathrm{d}x}\\&=e^s\cdot ('+latex(d)+r')\\&='+final+r'.\end{aligned}'+'\n$$')

def normal_text(template,p,kind,key):
 g,d,f,ans=mathdata(p,kind);placeholder='{{'+key+'}}'
 if kind.startswith('composite'):
  base=p['a']*X**2+p['b']*X+p['c']
  problem=rf'Given that $y=h(g(x))$, where $h(z)=e^{{{latex(p["k"]*s.Symbol("z"))}}}$ and $g(x)={latex(base)}$, calculate $\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}x}}$.'
  factor='' if kind=='composite_factor' else latex(2*p['k']*p['a'])
  problem+='\n\n'+r'$\frac{\mathrm{d}y}{\mathrm{d}x}='+factor+'($\n'+placeholder+'\n$)e^{'+latex(s.expand(g))+'}$'
  return problem,composite_solution(p,kind)
 if kind.startswith('trig'):
  problem=rf'Given that $y=f(h(x))$, where $f(h)={latex(p["scale"])}e^h$ and $h(x)={latex(g)}$, calculate $\frac{{\mathrm{{d}}y}}{{\mathrm{{d}}x}}$.'
  if kind=='trig_full':layout=r'$\frac{\mathrm{d}y}{\mathrm{d}x}=$'+'\n'+placeholder
  elif kind=='trig_product':layout=r'$\frac{\mathrm{d}y}{\mathrm{d}x}=($'+'\n'+placeholder+'\n$)e^{'+latex(g)+'}$'
  else:layout=r'$\frac{\mathrm{d}y}{\mathrm{d}x}= -($'+'\n'+placeholder+'\n$)/e^{'+latex(-g)+'}$'
  return problem+'\n\n'+layout,authored_solution(p,kind)
 name='f' if template in ('q-1953','q-107437','q-312451','q-48629','q-71877') else 'y'
 if kind=='slope':problem=f'Find the slope $m$ of the tangent to the curve $y=e^{{{polytex(p)}}}$ at the point where $x={latex(p["t"])}$.'
 elif name=='f':problem=f'Find $f\u2032(x)$ for $f(x)=e^{{{polytex(p)}}}$.'
 else:problem=f'Given that $y=e^{{{polytex(p)}}}$, find $'+r'\frac{\mathrm{d}y}{\mathrm{d}x}$.'
 if default_field(template)=='blank':problem+='\n\n'+('$m=$' if kind=='slope' else '$f\u2032(x)=$')+'\n'+placeholder
 return problem,authored_solution(p,kind,name)

def source_replay(template,seed=0):
 """Exact complete source records, normalized only; not deliverable practice."""
 import copy
 q=copy.deepcopy(SRC[template])
 def clean(obj):
  if isinstance(obj,list):return [clean(v) for v in obj]
  if not isinstance(obj,dict):return obj
  return {k:clean(v) for k,v in obj.items() if k!=':db/id'}
 q=clean(q)
 q[':question/problem']=normalize_prose(q[':question/problem'])
 if ':question/worked-solution' in q:q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
 for field in q[':question/answer-fields']:
  for a in field[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
  if ':answer-field/correct' in field:
   field[':answer-field/correct']=[':answer/id',field[':answer-field/correct'][':answer/id']]
 return {'knowledge_point':kp_identity(),'question':q,'generation':{'version':VERSION,'template':template,'profile':'observed:'+template,'seed':seed,'evidence_only':True,'parameters':SPECS[template][1]}}

def kp_identity():
 k=CAP['material']['kp']
 return {'db_id':KP,'id':k[':knowledge-point/id'],'title':k[':knowledge-point/title']}

def generate(level,seed=0,template=None,parameters=None,profile=None):
 if profile and profile.startswith('observed:'):
  template=profile.split(':',1)[1]
  if parameters is not None:raise ValueError('Source replay uses original complete parameters')
  if SPECS[template][0]!=level:raise ValueError('Source difficulty mismatch')
  return source_replay(template,seed)
 if level not in NORMAL:raise ValueError('Unsupported difficulty: '+level)
 if profile not in (None,'arithmetic-neighbors'):raise ValueError('Unsupported normal bank profile')
 rng=random.Random(seed)
 if template is None:template=rng.choice(NORMAL[level])
 if template not in NORMAL[level]:raise ValueError('Template difficulty mismatch')
 attempts=0
 for attempts in range(1,1001):
  try:
   p,kind,actual=prepare(template,parameters if parameters is not None else sample(template,rng))
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No valid instance after 1000 attempts')
 sf=SRC[template][':question/answer-fields'][0];key=sf[':answer-field/key'];ft=default_field(template)
 g,d,f,ans=mathdata(p,kind)
 offsets=[]
 if ft=='radio':vals,offsets=nearby_bank(p,kind,rng)
 else:vals=[ans]
 problem,solution=normal_text(template,p,kind,key)
 problem=normalize_prose(problem);solution=normalize_prose(solution)
 validate_prose(problem);validate_prose(solution)
 if ft=='radio':
  # Render the key and every distractor by the SAME rule. Algebraic
  # simplification of only the key can otherwise reveal its identity.
  vals_tex=[]
  for i,j in [(0,0),*offsets]:
   if kind=='slope':
    coefficient=d.subs(X,p['t'])+i;exponent=g.subs(X,p['t'])+j
    value=latex(coefficient)+r'\cdot e^{'+latex(exponent)+'}'
   else:
    factor=(p['a']*p['n']+i)*X**(p['n']-1)+p['b']+j
    value=r'\left('+latex(s.expand(factor))+r'\right)e^{'+polytex(p)+'}'
   vals_tex.append(normalize_tex(value))
 else:vals_tex=[normalize_tex(latex(s.expand(v) if kind.startswith('composite') else v)) for v in vals]
 for value in vals_tex:validate_tex(value)
 qid=uid([VERSION,problem,sorted(vals_tex),level]);fid=uid([qid,key])
 answers=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in vals_tex]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[0][':answer/id']]}
 if ft=='radio':rng.shuffle(answers)
 question={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]}
 task=uid([kind,s.srepr(g),str(p.get('t','')),s.srepr(ans)])
 return validate_generated_record({'knowledge_point':kp_identity(),'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'kind':kind,'profile':'arithmetic-neighbors' if ft=='radio' else 'source-blank','parameters':{k:str(v) for k,v in p.items() if k!='constant_first'},'offsets':offsets,'attempts':attempts,'mathematical_fingerprint':task,'source':{k:CAP[k] for k in ('database','basis','lineage')},'source_difficulty':SRC[template].get(':question/difficulty'),'inferred_missing_key':template=='q-48628','math_format':FORMAT_VERSION}})

def default_field(k):return SRC[k][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186092263-source-policy.json'))

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=5)
 parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args()
 if args.count<0:parser.error('--count must be nonnegative')
 if args.difficulty=='hard':parser.error('hard is unsupported: no supplied hard source family')
 records=[generate(args.difficulty,args.seed+i,template=args.template,profile=args.profile) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False))
