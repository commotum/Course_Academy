#!/usr/bin/env python3
"""Basis2275 other-base logarithm substitution; local review only, no DB operations."""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,random,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('');KP=17592186100817;VERSION='other-log-substitution-b2275-v1'
def module(name,path):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
fmt=module('kp00817_formatter',HERE/'reference/math_format.py')
SOURCE=json.loads((HERE/'source.json').read_text());REC=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
x,u,C=s.symbols('x u C',real=True)
# b: logarithm base; a: positive argument scale; m: argument power;
# n: log power; k/d: independent outer rational scale. Dependent values derived.
CONFIG={
'q-31329':('easy',(2,1,1,1,1,1)), 'q-31394':('easy',(5,1,1,1,1,1)),
'q-114020':('easy',(6,1,1,2,3,1)), 'q-114021':('easy',(7,1,1,1,1,2)),
'q-31395':('easy',(4,1,1,1,2,1)),
'q-31400':('moderate',(2,1,2,1,1,1)), 'q-31401':('moderate',(3,1,2,1,1,1)), 'q-210751':('moderate',(5,1,3,1,1,2)),
'q-31397':('hard',(3,1,1,-1,1,1)), 'q-31399':('hard',(5,1,1,-1,3,1)),
'q-73659':('hard',(7,4,1,-1,1,1)), 'q-31402':('hard',(5,3,1,-1,2,1)),
'q-210752':('hard',(2,1,1,-1,1,1)), 'q-210781':('hard',(3,2,1,-1,3,1)),
}
SLOTS=('b','a','m','n','k','d');ERRORS={'q-210752':'first distractor is equivalent to key modulo a constant on x>0,x!=1','q-31395':'two incorrect options are identical since ln4=2ln2'}
def parameters(v):return dict(zip(SLOTS,v))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(v)))
class Blog(s.Function):
 nargs=2
 def _latex(self,printer,exp=None):
  z=r'\log_{'+printer._print(self.args[1])+r'}\left('+printer._print(self.args[0])+r'\right)';return z if exp is None else '('+z+')^{'+exp+'}'
class LogAbs(s.Function):
 nargs=1
 def _latex(self,printer,exp=None):
  z=r'\ln\left|'+printer._print(self.args[0])+r'\right|';return z if exp is None else '('+z+')^{'+exp+'}'
def tex(v):return fmt.normalize_tex(s.latex(v).replace(r'\log',r'\ln') if not s.sympify(v).has(Blog) else s.latex(v).replace(r'\log{',r'\ln{'))
def true(v):return v.replace(Blog,lambda a,b:s.log(a)/s.log(b)).replace(LogAbs,lambda a:s.log(s.Abs(a)))
def derivative(v):
 v=true(v).replace(lambda z:z.func==s.log and z.args[0].has(s.Abs),lambda z:s.log(z.args[0].replace(s.Abs,lambda a:a)));return s.diff(v,x)
def equal(a,b):return s.simplify(s.expand_log(a-b))==0

def guard(sid,p):
 if set(p)!=set(SLOTS)or any(type(p[z])is not int for z in SLOTS):raise ValueError('builtin integer slots required')
 b,a,m,n,k,d=[p[z]for z in SLOTS];level=CONFIG[sid][0]
 if not(2<=b<=9 and 1<=a<=5 and 1<=m<=4 and 1<=k<=4 and 1<=d<=3):raise ValueError('comparable arithmetic bounds')
 if (sid=='q-31394'and b<4)or(sid=='q-31401'and b<3)or(sid=='q-31399'and b<5):raise ValueError('all logarithm bases in selected profile must exceed one')
 if level=='easy'and not(a==m==1 and n in(1,2)):raise ValueError('easy log power backbone')
 if level=='moderate'and not(a==1 and 2<=m<=4 and n==1):raise ValueError('moderate powered argument backbone')
 if level=='hard'and not(m==1 and n==-1):raise ValueError('hard reciprocal logarithm backbone')
 # q31397/q31399/q210752 use unscaled x in source; that is this family's
 # structural subcase, while separate hard families admit a as a variable.
 if sid in('q-31397','q-31399','q-210752')and a!=1:raise ValueError('unscaled-argument source profile')
 return tuple(s.Integer(p[z])for z in SLOTS)

def bank(sid,p):return recipes(sid,*guard(sid,p))
def recipes(sid,b,a,m,n,k,d):
 c=k/d;ln=s.log;L=Blog(a*x**m,b);L0=Blog(x,b);A=LogAbs(L);A0=LogAbs(L0);R=c*ln(b)/m;F=R*L**(n+1)/(n+1)if CONFIG[sid][0]!='hard' else R*A
 # Each list is a complete observed bank, selected by sid before parameters.
 if sid=='q-31329':vals=[c*ln(b+1)*L/2,ln(x)*c*L**2/2,c*ln(b)*L/2,ln(x)*c*L**2/x,F]
 elif sid=='q-31394':vals=[c*ln(b)*Blog(x,b-2)/2,c*ln(b)*L/2,c*ln(x)*L**2/2,F,c*ln(x)*L**2/x]
 elif sid=='q-114020':vals=[c*ln(b)*L/(n+1),F,c*L**(n+1)/(n+1),c*ln(b)*L**(n+1),c*ln(b)*L**(n+1)/(n+1)**2]
 elif sid=='q-114021':vals=[F,c*ln(b)*L**2,c*ln(b)*L,c*2*d**2*L**2,c*2*ln(b)*L**2]
 elif sid=='q-31395':vals=[c*ln(b)/4*L,c*ln(x)*L/4,F/2,c*ln(b)/4*L**2,F]
 elif sid=='q-31400':vals=[R*L/(n+1),F,c*ln(x)*L**2/2,c*ln(b)*L/2,c*ln(b)*L**2/2]
 elif sid=='q-31401':vals=[c*ln(b-1)*Blog(x**m,b-1)**2/(2*m),F,c*ln(x)*L0**2/(2*m),c*ln(x**m)*L**2/2,c*ln(b)*L**2/2]
 elif sid=='q-210751':vals=[c*L**2/m,c*ln(b)*ln(x**m)/(2*m),F,m*ln(x**(m-1))**2/2,ln(x**m)**2/2]
 elif sid=='q-31397':vals=[c*L,s.exp(c*x),F,c*A,s.exp(b*c*x)]
 elif sid=='q-31399':vals=[c*ln(x)*LogAbs(Blog(x,10)),ln(b)*LogAbs(Blog(x,b-2)),ln(b)/b*LogAbs(Blog(x,10)),c*ln(b-2)*LogAbs(Blog(x,b-3)),F]
 elif sid in('q-73659','q-31402'):
  v1=c*ln(x**b)*A;v2=ln(a)*A0;v3=ln(b)/b*A;v4=x*ln(b)*LogAbs(Blog(x**a,b))
  vals=[v1,v2,v3,v4,F]if sid=='q-73659'else[v4,v2,v1,v3,F]
 elif sid=='q-210752':vals=[c*ln(b)*LogAbs(Blog(x**2,b)),F,2*c*A,c*ln(b)+A,c*A**2]
 elif sid=='q-210781':vals=[c*A,F,a*A,c*ln(b)*s.Abs(L),c*ln(b)*LogAbs(s.log(b*x))]
 return vals,F

def math_domain(p):
 if p['m']%2==0:return 'real x != 0; x^m>0'
 if p['n']==-1:return 'real x>0; a*x!=1'
 return 'real x>0'
def fingerprint(p):
 # For positive x, log(a*x^m)=m*ln(x)+ln(a); even m also has negative branch.
 b,a,m,n,k,d=[s.Integer(p[z])for z in SLOTS];v=s.Symbol('ln_abs_x',real=True)
 expr=s.Rational(k,d)*(m*v+s.log(a))**n/(x*s.log(b)**n)
 return digest({'integrand':s.srepr(s.cancel(s.expand(s.expand_log(expr)))),'domain':math_domain(p)})

def render(sid,p,repair=False):
 b,a,m,n,k,d=guard(sid,p);c=k/d;vals,F=bank(sid,p)
 if repair and sid in ERRORS:
  # Explicit authored replacement of erroneous banks, maintaining all5 options.
  L=Blog(a*x**m,b);R=c*s.log(b)/m
  vals=[F,F*2,F/2,R*L,F*3]if n!=-1 else[F,F*2,F/2,R*L,R*L**2]
 arg=a*x**m;L=Blog(arg,b);R=c*s.log(b)/m
 integ=c*L**n/x
 I=r'\int '+tex(integ)+r'\,\text{d}x'
 prompt='$'+I+'=$'
 du= m/(x*s.log(b))
 display=lambda v:'\n\n$$\n'+v+'\n$$'
 sol='Let $u='+tex(L)+'.$ Differentiating, we get'+display(r'\frac{\text{d}u}{\text{d}x}='+tex(du)+r'\,\Longrightarrow\,'+tex(s.log(b)/m)+r'\,\text{d}u=\frac{\text{d}x}{x}.')
 sol+='\n\nUsing the above, we can write the integral in terms of $u$ and evaluate:'
 # Preserve factor split, substitution, constant extraction, primitive and backsubstitution.
 rows=[I+' & ='+tex(c)+r'\int '+tex(L**n)+r'\cdot\frac{\text{d}x}{x}', ' & ='+tex(c)+r'\int '+tex(u**n)+r'\cdot '+tex(s.log(b)/m)+r'\,\text{d}u', ' & ='+tex(R)+r'\int '+tex(u**n)+r'\,\text{d}u']
 if sid=='q-210781':
  rows[0]=I+' & ='+r'\int '+tex(c*L**n)+r'\cdot\frac{\text{d}x}{x}'
  rows[1]=' & ='+r'\int '+tex(c*u**n)+r'\cdot '+tex(s.log(b)/m)+r'\,\text{d}u'
 primitive=LogAbs(u)if n==-1 else u**(n+1)/(n+1)
 rows.append(' & ='+tex(R)+r'\cdot '+tex(primitive)+'+C')
 if sid=='q-31395':rows.append(' & ='+tex(R*primitive)+'+C')
 rows.append(' & ='+tex(F)+'+C')
 sol+=display(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
 return fmt.normalize_prose(prompt),fmt.normalize_prose(sol),vals,F

def sample(sid,rng):
 level,orig=CONFIG[sid]
 for _ in range(500):
  b=rng.randint(2,9);a=rng.randint(1,5)if level=='hard'and sid not in('q-31397','q-31399','q-210752')else 1;m=rng.randint(2,4)if level=='moderate'else 1;n=rng.choice([1,2])if level=='easy'else 1 if level=='moderate'else-1
  # Banks with an observed n=1 include log-square recipes; changing n would
  # change their recipe roles. The n=2 source family varies this eligible slot.
  if level=='easy'and sid!='q-114020':n=1
  p=parameters((b,a,m,n,rng.randint(1,4),rng.randint(1,3)))
  if(sid=='q-31394'and b<4)or(sid=='q-31401'and b<3)or(sid=='q-31399'and b<5):continue
  try:
   vals,F=bank(sid,p)
   if sid not in ERRORS:
    ds=[derivative(v)for v in vals]
    if any(equal(v,z)for i,v in enumerate(ds)for z in ds[:i]):continue
   return p
  except (ValueError,ZeroDivisionError):pass
 raise ValueError('whole profile has no valid sampled instance')

@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if field_type not in(None,'radio',':answer-field.type/radio'):raise ValueError('only source radio fields supported')
 if type(seed)is not int:raise ValueError('seed must be builtin int')
 if level not in('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed);eligible=[z for z in CONFIG if CONFIG[z][0]==level]
 if template is not None and template not in eligible:raise ValueError('template difficulty mismatch')
 sid=template or rng.choice(eligible);profile=profile or('repaired'if sid in ERRORS else'observed')
 if profile not in('observed','repaired'):raise ValueError('profile')
 if profile=='repaired'and sid not in ERRORS:raise ValueError('repair profile only applies to documented source errors')
 p=dict(parameters)if parameters is not None else sample(sid,rng)
 prompt,solution,vals,F=render(sid,p,profile=='repaired')
 if not(sid in ERRORS and profile=='observed'):
  ds=[derivative(v)for v in vals]
  if any(equal(v,z)for i,v in enumerate(ds)for z in ds[:i]):raise ValueError('whole source profile collision; change parameters')
 original=tuple(p[z]for z in SLOTS)==CONFIG[sid][1]
 values=[tex(v)+'+C'for v in vals]
 correctindex=next(i for i,v in enumerate(vals)if v==F)
 contents={'prompt':prompt,'solution':solution,'field':'radio','bank':values,'correct':correctindex};ch=digest(contents);qid=uid(ch);fid=uid(qid+'selection')
 answers=[{':answer/id':uid(fid+str(i)+v),':answer/type':':answer.type/math',':answer/value':v}for i,v in enumerate(values)];correctid=answers[correctindex][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'basis':2275,'template':sid,'parameters':p,'bank_profile':sid+'-'+profile,'source_ids':[sid],'math_fingerprint':fingerprint(p),'content_fingerprint':ch,'domain':math_domain(p),'eligible':not(sid in ERRORS and profile=='observed'),'evidence_only':sid in ERRORS and profile=='observed','source_error':ERRORS.get(sid)if profile=='observed'else None,'authored':not original or profile=='repaired','source_repairs':['authored complete replacement bank; original retained ineligible']if profile=='repaired'else[],'runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def batch(level='all',seed=0,count=1,**kw):
 if type(seed)is not int or type(count)is not int or count<1:raise ValueError('builtin int seed and positive builtin int count required')
 if count>500:raise ValueError('capacity guard: at most500 per level')
 rows=[];seen=set()
 for lev in(['easy','moderate','hard']if level=='all'else[level]):
  added=0
  for i in range(count*300):
   row=generate(lev,seed+i,**kw);f=row['generation']['math_fingerprint']
   if f in seen:continue
   seen.add(f);rows.append(row);added+=1
   if added==count:break
  if added<count:raise ValueError('requested mathematical task capacity unavailable')
 return rows
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 try:rows=batch(a.difficulty,a.seed,a.count,template=a.template,profile=a.profile)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(rows,ensure_ascii=False,indent=2)if a.format=='json'else'\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']for r in rows))
