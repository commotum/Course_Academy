#!/usr/bin/env python3
"""Source-bank inverse-tangent integrals; bounded, exact, deterministic variants."""
import argparse, hashlib, json, random, re, uuid, sys
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
from functools import lru_cache
KP_ID=17592186064219
KP_UUID='227abe29-6e31-5afd-b0ca-3b8ed7d8c287'
TITLE='Calculating Indefinite Integrals Using Substitution with Inverse Tangent'
VERSION='inverse-tangent-substitution-draft-v2'
PACKAGE=Path(__file__).with_suffix('')
sys.path.insert(0,str(PACKAGE))
from math_format import normalize_prose,normalize_tex,checked_math_content
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(z):return sp.latex(sp.simplify(z)).replace(' ','')
def coefficient(z):return '' if z==1 else tex(z)
def function(z,fn,k,quotient=False):
 arg='x' if k==1 else (r'\frac{x}{'+tex(1/k)+'}' if k.is_Rational and 0<k<1 else tex(k)+'x')
 if k.is_Rational is False and tex(k).startswith(r'\frac'):
  arg=tex(k).replace('}{','x}{',1)
 arg='('+arg+')'
 f=(r'\text{arcsec}' if fn=='asec' else r'\operatorname{'+{'atan':'arctan','asin':'arcsin'}[fn]+'}⁡')+arg
 if quotient and z.is_Rational and z.p==1:return r'\frac{'+f+'}{'+str(z.q)+'}+C'
 return coefficient(z)+f+'+C'
def bank(sid,p):
 n,b=map(sp.Integer,p);s=sp.sqrt(b);c=n/s
 A=lambda z,k=s,fn='atan',q=False:function(z,fn,k,q)
 if sid=='q-49540':values=[A(n),A(1/s,q=True),A(c,fn='asin'),A(c),A(1/s,fn='asin',q=True)];ci=3
 elif sid=='q-114033':values=[A(1,1/s),A(s/n),A(c,sp.Integer(1)),A(c,1/s),A(c)];ci=4
 elif sid=='q-114035':values=[A(b),A(c),A(s),A(c,sp.Integer(1)),A(c,1/b)];ci=1
 elif sid=='q-114036':values=[A(c,sp.Integer(1)),A(s),A(b),A(1,1/s),A(c)];ci=4
 elif sid=='q-114040':values=[A(c),A(n/b),A(s),A(c,b),A(n)];ci=0
 elif sid=='q-2504':values=[A(1/s,q=True),A(s),A(1/b,b,q=True),A(1/b,q=True),A(1/(2*s),2*s,q=True)];ci=0
 elif sid=='q-2507':values=[A(1/b,sp.Integer(1),q=True),A(1/s,q=True),A(1/b,b,'asec',True),A(1/s,s,'asin',True),A(1/b,b,q=True)];ci=1
 elif sid=='q-73713':values=[A(1/c,q=True),A(1/c,fn='asin',q=True),A(c,sp.Integer(1)),A(c,fn='asin'),A(c)];ci=4
 elif sid=='q-114039':values=[A(c),A(b),A(s),A(c,b),A(c,sp.Integer(1))];ci=0
 elif sid=='q-49548':values=[A(1/b,1/b),A(1,1/s),A(c,1/s),A(c,1/b),A(1,1/b)];ci=2
 elif sid=='q-114045':values=[A(c),A(1,1/s),A(1/s,1/s),A(c,1/s),A(n/b,1/s)];ci=3
 elif sid=='q-114046':values=[A(1/s,sp.Integer(1)),A(1),A(1/s,1/s),A(1,1/s),A(s,1/s)];ci=3
 elif sid=='q-49505':values=[A(c,1/s),A(1,1/s),A(c,sp.Integer(1)),A(1),A(s)];ci=0
 elif sid=='q-49550':values=[A(c,1/s),A(c,s,'asin'),A(c,1/s,'asin'),A(c),A(1,1/s)];ci=0
 elif sid=='q-49551':values=[A(c,1/s,'asin',True),A(c,c,q=True),A(1/s,s,'asin',True),A(c,1/s,q=True),A(1/s,1/s,q=True)];ci=3
 elif sid=='q-73714':values=[A(s/n),A(c,1/s),A(1/n,1/s),A(c),A(s/n,1/s)];ci=1
 else:raise ValueError(sid)
 # Two sources omit parentheses around the unit argument. Preserve that notation.
 if sid in ('q-73713','q-49505'):values=[v.replace('⁡(x)','⁡x') for v in values]
 return values,ci

x=sp.Symbol('x',real=True)
LEVELS=('easy','moderate','hard')
def strict_int(value,name,positive=False):
 if type(value) is not int or (positive and value<1):raise ValueError(name+' must be a builtin '+('positive ' if positive else '')+'int')
def source_scale(sid,p):
 n,b=map(sp.Integer,p);s=sp.sqrt(b);t=PROFILES[sid];on,ob=t['parameters'];os=sp.sqrt(ob)
 repl={'N':str(n),'C':coefficient(n/s),'R':tex(n/b),'RAW_R':r'\frac{'+str(n)+'}{'+str(b)+'}', 'ROOT_R':r'\frac{'+str(n)+r'\sqrt{'+str(b)+'}}{'+str(b)+'}', 'OVER_ROOT':r'\frac{'+str(n)+r'}{\sqrt{'+str(b)+'}}'}
 def render(txt):
  txt=txt.replace('^{2}','^{EXPONENT}')
  mapping={str(ob):str(b)}
  if os.is_Integer:mapping[str(os)]=str(s)
  txt=re.sub(r'\d+',lambda m:mapping.get(m[0],m[0]),txt).replace('^{EXPONENT}','^{2}')
  for k,z in repl.items():txt=txt.replace('@@'+k+'@@',z)
  return txt
 return render(t['prompt']),render(t['solution'])

def candidate_parameters(sid):
 t=PROFILES[sid];on,ob=t['parameters'];radical=not sp.sqrt(ob).is_Integer
 bs=[2,3,5,6,7,10,11,13] if radical else [z*z for z in range(2,13)]
 pairs=[t['parameters']]
 for b in bs:
  s=sp.sqrt(b)
  if sid=='q-114046':ns=[int(s)]
  elif t['fixed_numerator']:ns=[1]
  elif sid in ('q-49540','q-73713','q-114045'):ns=[int(s)*m for m in range(2,8)]
  elif sid=='q-49551':ns=[n for n in range(2,13) if s/n==int(s/n)]
  else:ns=range(2,17)
  pairs += [[int(n),b] for n in ns]
 return list(dict.fromkeys(map(tuple,pairs)))

# Closed form signatures distinguish all options modulo additive constants.
# Complete profiles are selected before their complete recipe bank is validated.
def admissible(sid,p):
 if len(p)!=2 or any(type(z)is not int or z<1 for z in p):return False
 vals,ci=bank(sid,p)
 from math_parser import latex
 signatures=[]
 for value in vals:
  expr=latex(value);atoms=list(expr.atoms(sp.atan,sp.asin,sp.asec));assert len(atoms)==1
  atom=atoms[0];scale=sp.simplify(atom.args[0]/x);amplitude=sp.simplify((expr-sp.Symbol('C',real=True))/atom)
  signatures.append((atom.func,sp.simplify(amplitude*scale if atom.func!=sp.asec else amplitude),scale**2))
 n,b=map(sp.Integer,p);scale=sp.sqrt(b) if PROFILES[sid]['difficulty']=='easy' else 1/sp.sqrt(b)
 target=(sp.atan,sp.simplify(n/sp.sqrt(b)*scale),scale**2)
 return len(set(signatures))==5 and [i for i,z in enumerate(signatures) if z==target]==[ci]

@lru_cache(None)
def candidates(sid):return [list(p) for p in candidate_parameters(sid) if admissible(sid,list(p))]

def hard_content(p):
 n,a,s=map(sp.Integer,p);b=a*s*s;k=n/(a*s)
 integrand=r'\frac{'+str(n)+'}{'+str(a)+'+'+str(b)+r'{x}^{2}}'
 prompt='Calculate $'+r'\int '+integrand+r'\,\text{d}x.$'
 sol='Note that we can rewrite this integral as\n\n$$\n'+r'\int '+integrand+r'\,\text{d}x=\frac{'+str(n)+'}{'+str(a)+r'}\int\frac{1}{1+'+str(s*s)+r'{x}^{2}}\,\text{d}x.'+'\n$$\n\nThis integral resembles the basic integral for inverse tangent,\n\n$$\n'+r'\int\frac{1}{1+u^2}\,\text{d}u=\operatorname{arctan}u+C.'+'\n$$\n\nThe only difference is that instead of $u^2$ as the variable, we have $'+str(s*s)+r'x^2=('+str(s)+r'x)^2.$'+'\n\nSo, let\'s substitute $u='+str(s)+r'x.$ Differentiating, we get'+'\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+str(s)+r'\quad\Longrightarrow\quad\text{d}x=\frac{1}{'+str(s)+r'}\text{d}u.'+'\n$$\n\nWe can now write the integral in terms of $u,$ and evaluate:\n\n$$\n'+r'\begin{aligned}\int '+integrand+r'\,\text{d}x&=\frac{'+str(n)+'}{'+str(a)+r'}\int\frac{1}{1+('+str(s)+r'x)^2}\,\text{d}x\\&=\frac{'+str(n)+'}{'+str(a)+r'}\int\frac{1}{1+u^2}\cdot\frac{1}{'+str(s)+r'}\,\text{d}u\\&='+coefficient(k)+r'\int\frac{1}{1+u^2}\,\text{d}u\\&='+coefficient(k)+r'\operatorname{arctan}u+C\\&='+function(k,'atan',s)+r'\end{aligned}'+'\n$$'
 vals=[function(k,'atan',s),function(n/a,'atan',s),function(n/(a*s*s),'atan',s),function(k,'atan',sp.Integer(1)),function(k,'atan',1/s)]
 return prompt,sol,vals,0

@checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None):
 strict_int(seed,'seed')
 if difficulty not in LEVELS:raise ValueError('unsupported difficulty')
 rng=random.Random(seed)
 sid=template or ('authored-canonical-factor' if difficulty=='hard' else rng.choice([sid for sid,t in PROFILES.items() if t['difficulty']==difficulty]))
 if difficulty=='hard':
  if sid!='authored-canonical-factor':raise ValueError('profile level mismatch')
  p=list(parameters) if parameters is not None else [rng.randint(1,17),rng.randint(2,9),rng.randint(2,12)]
  if len(p)!=3 or any(type(z)is not int for z in p) or not(1<=p[0]<=17 and 2<=p[1]<=9 and 2<=p[2]<=12):raise ValueError('invalid hard parameters')
  prompt,sol,vals,ci=hard_content(p);source_ids=['e-471'];recipes=['k atan(sx)','(n/a) atan(sx)','(n/(a*s²)) atan(sx)','k atan(x)','k atan(x/s)'];relation='authored extension of canonical e-471; same factoring and linear substitution'
 else:
  if sid not in PROFILES or PROFILES[sid]['difficulty']!=difficulty:raise ValueError('profile level mismatch')
  p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
  if tuple(p) not in candidate_parameters(sid) or not admissible(sid,p):raise ValueError('Outside validated bounded capability')
  prompt,sol=source_scale(sid,p);vals,ci=bank(sid,p);source_ids=[sid];recipes=PROFILES[sid]['recipes'];relation='observed profile with conservative same-method numeric slots'
 prompt,sol=normalize_prose(prompt),normalize_prose(sol);vals=[normalize_tex(v) for v in vals]
 fp=digest([difficulty,p]);qid=ident(['question',VERSION,fp,sid,digest(sorted(vals))]);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,z]),':answer/type':':answer.type/math',':answer/value':z} for z in vals]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'source_basis':2275,'evidence_only':False,'eligible_for_learning':True,'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_ids':source_ids,'recipes':recipes,'domain':'x real; C arbitrary real; all scales positive; principal real arctan','relationship_to_source_templates':relation,'sympy':sp.__version__}}

def batch(difficulty='all',count=1,seed=0):
 strict_int(seed,'seed');strict_int(count,'count',True)
 if difficulty not in (*LEVELS,'all'):raise ValueError('unsupported difficulty')
 levels=LEVELS if difficulty=='all' else (difficulty,);out=[];seen=set();rng=random.Random(seed)
 for level in levels:
  made=0
  for attempt in range(max(count*200,1000)):
   rec=generate(level,rng.randrange(2**53))
   p=rec['generation']['parameters']
   value=sp.Rational(p[0])/(1+p[1]*x*x) if level=='easy' else (sp.Rational(p[0])/(p[1]+x*x) if level=='moderate' else sp.Rational(p[0])/(p[1]+p[1]*p[2]**2*x*x))
   key=(level,str(sp.cancel(value)))
   if key in seen:continue
   seen.add(key);out.append(rec);made+=1
   if made==count:break
  else:raise ValueError('Finite family exhausted')
 return out

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=[*LEVELS,'all'],default='all');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
