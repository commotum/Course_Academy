#!/usr/bin/env python3
"""Bernoulli solution generator: translated coefficient arguments, real branches.

No database writes. Source profiles remain complete; only coefficient argument
x -> x+h varies. Derivative coordinates and function names remain x. The
constant-coefficient autonomous q-109029 has source replay only (no new tasks).
Easy and incomplete q-106074 are explicitly unsupported. See package evidence.
"""
import argparse,hashlib,json,random,re,uuid,os,sys
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186147454
HERE=Path(__file__).resolve().with_suffix('')
SNAPSHOT=json.loads((HERE/'source.json').read_text())
NAMESPACE=uuid.UUID(SNAPSHOT['record'][':knowledge-point/id'])
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='bernoulli-translation-1'
TITLE=SNAPSHOT['record'][':knowledge-point/title']
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions'] if ':question/worked-solution' in q and all(':answer-field/correct' in f for f in q.get(':question/answer-fields',[]))}
SUPPORTED_LEVELS=('moderate','hard')
ORIGINAL={t:{'shift':0} for t in SOURCES}
SHIFTS=tuple(range(-6,0))+tuple(range(1,7))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NAMESPACE,x))
def translate(text,h):
 if h==0:return text
 # Protect derivative coordinates, function argument notation, and prose.
 protected={}
 def keep(m):
  key='ZZTOKEN'+str(len(protected))+'ZZ';protected[key]=m[0];return key
 def math(m):
  s=m[0]
  s=re.sub(r'\\text\{d\}x|\\mathrm\{d\}x|\\(?:,|!)?\\text\{d\}x|(?<![A-Za-z])dx|[pqPQIyz]\(x\)',keep,s)
  # x in x+y, 2x, powers, or a bare argument is an algebraic coordinate slot.
  s=re.sub(r'\\text\{[^}]*\}|\\[A-Za-z]+',keep,s)
  s=re.sub(r'x',lambda _:'(x'+('+' if h>0 else '-')+str(abs(h))+')',s)
  s=re.sub(r'(?<=[A-Za-z0-9])(?=\(x[+-])',lambda _:r'\cdot ',s)
  for k,v in protected.items():s=s.replace(k,v)
  return s
 text=text.replace('with respect to $x:$','with respect to ZZCOORDZZ')
 result=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',math,text)
 return result.replace('ZZCOORDZZ','$x:$')
def value_translate(value,h):
 # Answer values contain only mathematical expressions.
 return translate('$'+value+'$',h)[1:-1]
def generate(difficulty,seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 eligible=[t for t,q in SOURCES.items() if q[':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty and t!='q-109029']
 rng=random.Random(seed);t=template or rng.choice(eligible)
 assert t in SOURCES and SOURCES[t][':question/difficulty'][':db/ident']==':question.difficulty/'+difficulty
 p=dict(parameters) if parameters is not None else {'shift':rng.choice(SHIFTS)}
 assert set(p)=={'shift'} and p['shift'] in (0,*SHIFTS)
 h=p['shift'];assert t!='q-109029' or h==0
 q=SOURCES[t];original=h==0;identity=digest([VERSION,t,p])
 qid=uid('question:'+identity);fields=[]
 for f in q[':question/answer-fields']:
  fid=uid('field:'+identity+':'+f[':answer-field/key']);answers=[];correct=None
  for a in f[':answer-field/choices']:
   value=value_translate(a[':answer/value'],h);aid=uid('answer:'+fid+':'+value)
   answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
   if a[':answer/id']==f[':answer-field/correct'][':answer/id']:correct=aid
  fields.append({':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
 problem=translate(q[':question/problem'],h)
 solution_source=q[':question/worked-solution']
 if h:
  solution_source=solution_source.replace('(1/4x)',r'(\frac{1}{4x})').replace('(3/2x)',r'(\frac{3}{2x})')
 solution=translate(solution_source,h)
 if not original:
  # Restrict the question to the nonzero family obtained by Bernoulli division.
  problem=problem.replace('Find the general solution','Find the general nonzero real solution')
  domain='x'+('+' if h>0 else '-')+str(abs(h))
  problem+='\n\nWork on an interval where $'+domain+'>0$. Choose constants and intervals on which all displayed real expressions are defined.'
  if t in ('q-109170','q-109177'):problem+=' Take $y>0$.'
  solution+='\n\nThese are the nonzero real solutions on the specified intervals; exclude denominator zeros and restrict constants and intervals to the real branches used above.'
  if t=='q-109170':solution+=' Since $z=y^{1/4}>0$, retain only intervals where the displayed expression for $z$ is positive.'
  if t=='q-109177':solution+=' Since $z=y^{3/2}>0$, retain only intervals where the displayed expression for $z$ is positive.'
 return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+difficulty,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'template':t,'profile':'observed:'+t,'parameters':p,'seed':seed,'source_question_id':q[':question/id'],'source_math_academy_id':t,'source_basis':SNAPSHOT['basis'],'evidence_only':original,'domains':'translated coordinate positive; nonzero real branches; exclude singularities','sympy':sp.__version__}}
def fingerprint(q):
 # Extract and canonicalize the ODE, not prose, seed, choice order, or IDs.
 from sympy.parsing.latex import parse_latex
 import sys
 sys.path.insert(0,'/tmp/ca-bernoulli-validation')
 text=q[':question/problem'];eq=re.search(r'\$\$([\s\S]*?)\$\$',text)
 if not eq:eq=re.search(r'\$([^$]*=[^$]*)\$',text)
 assert eq
 eq=re.sub(r'\s+','',eq[1]).rstrip('.').replace(r'\dfrac',r'\frac').replace(r'\textrm{d}',r'\text{d}')
 eq=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}', 'D',eq)
 lhs,rhs=eq.split('=')
 x,y,D=sp.symbols('x y D');env={'x':x,'y':y,'D':D,'e':sp.E}
 def parse(v):
  a=parse_latex(v,strict=True);return a.xreplace({s:env.get(str(s),s) for s in a.free_symbols})
 residual=sp.expand(parse(lhs)-parse(rhs));normal=sp.simplify(-residual.subs(D,0)/sp.diff(residual,D))
 return digest(sp.srepr(normal))
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' [key]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 records=[];seen=set()
 for seed in range(a.seed,a.seed+1000):
  r=generate(a.difficulty,seed);fp=digest([r['generation']['template'],r['generation']['parameters']['shift']])
  if fp not in seen:records.append(r);seen.add(fp)
  if len(records)>=a.count:break
 if len(records)!=a.count:raise ValueError('Finite variant limit; '+str(len(records))+' distinct available in this package')
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
