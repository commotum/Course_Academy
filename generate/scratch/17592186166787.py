#!/usr/bin/env python3
"""Bounded hyperbolic quotient substitution generator; no database writes.

Two observed complete banks. Missing keys/solutions and difficulty assignments
are authored and independently validated. No hard family is claimed.
"""
import argparse, hashlib, json, random, sys, uuid, os
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186166787
KP_UUID='c95abaf8-c2ed-500b-a9d4-20c3346367b7'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
TITLE='Integrating Quotients Containing Hyperbolic Functions Using Substitution'
VERSION='hyperbolic-quotient-bounded-1'
HERE=Path(__file__).resolve().with_suffix('')
MACROS=r'\newcommand{\csch}{\mathop{\rm csch}\nolimits} \newcommand{\coth}{\mathop{\rm coth}\nolimits}'
DATA={'q-95548':('easy',3),'q-95551':('moderate',2)}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return sp.latex(v)
def fingerprint(q):
 import re
 p=q[':question/problem']
 if '\\sinh{x^2}' in p:return digest(['canonical-x-tanh-x2'])
 if '\\coth' in p:
  m=re.search(r'(\d+)\\coth x \+ 1',p)
  if not m:raise ValueError('Unrecognized coth integrand')
  return digest(['csch^2/(a*coth+1)',int(m[1]),'indefinite'])
 if '\\cosh' in p:
  m=re.search(r'\\ln (\d+)',p)
  if not m or '3 + \\sinh x' not in p:raise ValueError('Unrecognized definite integrand')
  return digest(['cosh/(3+sinh)',0,int(m[1])])
 raise ValueError('Unrecognized mathematical task')
def values(level,n):
 if level=='easy':
  return [rf'-\frac{{1}}{{2}}\ln \mid {n}\coth x - 1 \mid + C',rf'\frac{{1}}{{{n}}}\ln \mid {n}\csch x + 1 \mid + C',rf'-\frac{{1}}{{{n}}}\ln \mid {n}\coth x + 1 \mid + C',rf'\frac{{1}}{{2}}\ln \mid {n}\csch^{{2}} x + 1 \mid + C',rf'-\frac{{1}}{{{n}}}\ln \mid \csch^{{2}} x \mid + C']
 ratio=sp.Rational(3,1)+(sp.Rational(n)-sp.Rational(1,n))/2
 return [rf'\ln ({tex(sp.Rational(n,n+1))})',rf'\ln {n*n}',rf'3\ln ({tex(sp.Rational(n*n,n*n+1))})',rf'\ln ({tex(ratio/3)})',r'\ln (\frac{3}{3})']
def solution(level,n):
 if level=='easy':
  return '$$\n'+MACROS+'\n$$'+rf'''

Let $u={n}\coth x+1$. Differentiating gives

$$\frac{{\mathrm{{d}}u}}{{\mathrm{{d}}x}}=-{n}\csch^2 x,
\qquad \csch^2 x\,\mathrm{{d}}x=-\frac{{1}}{{{n}}}\,\mathrm{{d}}u.$$

Using this substitution, we obtain

$$\begin{{aligned}}
\int\frac{{\csch^2 x}}{{{n}\coth x+1}}\,\mathrm{{d}}x
&=-\frac{{1}}{{{n}}}\int\frac{{1}}{{u}}\,\mathrm{{d}}u \\
&=-\frac{{1}}{{{n}}}\ln|u|+C \\
&=-\frac{{1}}{{{n}}}\ln|{n}\coth x+1|+C.
\end{{aligned}}$$

The antiderivative is valid on each interval where $x\ne0$ and ${n}\coth x+1\ne0$.'''
  
 upper=3+(sp.Rational(n)-sp.Rational(1,n))/2
 return rf'''Let $u=3+\sinh x$. Differentiating gives $\mathrm{{d}}u=\cosh x\,\mathrm{{d}}x$.

When $x=0$, $u=3$. When $x=\ln {n}$,

$$u=3+\frac{{e^{{\ln {n}}}-e^{{-\ln {n}}}}}{{2}}
=3+\frac{{{n}-\frac{{1}}{{{n}}}}}{{2}}={tex(upper)}.$$

Therefore,

$$\begin{{aligned}}
\int_0^{{\ln {n}}}\frac{{\cosh x}}{{3+\sinh x}}\,\mathrm{{d}}x
&=\int_3^{{{tex(upper)}}}\frac{{1}}{{u}}\,\mathrm{{d}}u \\
&=\left[\ln u\right]_3^{{{tex(upper)}}} \\
&=\ln({tex(upper)})-\ln 3 \\
&=\ln\left({tex(upper/3)}\right).
\end{{aligned}}$$

Here $u>0$ throughout the interval, so the logarithm and substitution are defined.'''
def generate(level,seed=0,template=None,parameters=None):
 if level not in ('easy','moderate'):raise ValueError('Unsupported hard: no observed or validated hard family')
 s=template or ('q-95548' if level=='easy' else 'q-95551')
 p=parameters if parameters is not None else {'n':random.Random(seed).randint(2,12)}
 if s not in DATA or DATA[s][0]!=level or set(p)!={'n'} or type(p['n'])!=int or not 2<=p['n']<=12:raise ValueError('Outside bounded parameter policy')
 n=p['n'];old=sources()[s];of=old[':question/answer-fields'][0]
 if level=='easy':prompt=old[':question/problem'].replace('3\\coth',str(n)+'\\coth')
 else:prompt=old[':question/problem'].replace('\\ln 2','\\ln '+str(n))
 if n!=DATA[s][1] and level=='easy':prompt=prompt.replace('csch',r'\csch').replace('$\\displaystyle','$'+MACROS+r' \displaystyle')
 vals=[a[':answer/value'] for a in of[':answer-field/choices']] if n==DATA[s][1] else values(level,n)
 fp=fingerprint({':question/problem':prompt});qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'task:'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+val)),':answer/type':':answer.type/math',':answer/value':val} for val in vals]
 index=2 if level=='easy' else 3
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(level,n),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',answers[index][':answer/id']],':answer-field/choices':answers}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':s,'parameters':p,'source_question':s,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'bank_profile':s,'mathematical_fingerprint':fp,'domain':'real connected intervals excluding x=0 and denominator zeros (indefinite); [0,ln(n)] (definite)','dependencies':{'sympy':sp.__version__},'difficulty_origin':'authored: single indefinite substitution easy; definite substitution with exponential endpoints moderate','solution_origin':'authored; both source solutions and keys absent','sampling_policy':'finite n=2..12; source values retained; distractor transformations are observed-shape extensions, not established author error intentions'}}
def candidates(level):
 if level not in ('easy','moderate'):raise ValueError('Unsupported level')
 for n in range(2,13):yield 'q-95548' if level=='easy' else 'q-95551',{'n':n}
def batch(level,count,seed):
 if type(count)!=int or count<0:raise ValueError('Invalid count')
 ps=list(candidates(level));random.Random(seed).shuffle(ps)
 if count>len(ps):raise ValueError(f'Finite capacity {len(ps)}; requested {count}')
 return [generate(level,seed,s,p) for s,p in ps[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();rs=batch(o.difficulty,o.count,o.seed);print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,rs)))
