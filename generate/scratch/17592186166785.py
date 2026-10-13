#!/usr/bin/env python3
"""Finite source-bank generator for reciprocal hyperbolic linear substitution."""
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186166785
KP_UUID='e112da03-ea8d-5997-a7be-4f5be5e365e2'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
TITLE='Integrating Reciprocal Hyperbolic Functions With Linear Arguments'
VERSION='reciprocal-hyperbolic-linear-1'
HERE=Path(__file__).resolve().with_suffix('')
MACROS=r'\newcommand{\sech}{\mathop{\rm sech}\nolimits} \newcommand{\csch}{\mathop{\rm csch}\nolimits}'
DATA={'q-95534':('easy',2),'q-95535':('moderate',5)}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return sp.latex(v)
def fingerprint(q):
 p=q[':question/problem']
 if '\\coth' in p:return digest(['canonical-csch-coth',3,1])
 if 'sech^{2}' in p or 'sech^2' in p:
  m=re.search(r'\\frac\{(\d+)x\}\{5\}',p)
  if not m:raise ValueError('Unrecognized squared-sech argument')
  return digest(['sech-squared',int(m[1]),5,'indefinite'])
 m=re.search(r'(?:\\sech|sech)\s*(\d+)x',p)
 if not m:raise ValueError('Unrecognized definite sech-tanh argument')
 return digest(['sech-tanh',int(m[1]),1,2])
def values(level,n):
 if level=='easy':
  a=sp.Rational(n,5);u=rf'\frac{{{n}x}}{{5}}';v=rf'\frac{{5x}}{{{n}}}'
  return [rf'{tex(a)}\tanh^{{2}} ({u}) + C',rf'-{tex(1/a)}\csch^{{2}} ({u}) + C',rf'{tex(a)}\tanh ({u})\sech ({u}) + C',rf'{tex(1/a)}\tanh ({u}) + C',rf'-5\tanh ({v}) + C']
 return [rf'\frac{{1}}{{{n}}}(\sech {n} - \sech 2)',rf'{n}(\sech 2 - \sech {n})',rf'\frac{{1}}{{{n}}}(\tanh 2 - \tanh {n})',rf'\frac{{1}}{{{n}}}(\tanh^{{2}} {2*n})',rf'\frac{{1}}{{{n}}}(\sech {n} - \sech {2*n})']
def solution(level,n):
 if level=='easy':
  a=sp.Rational(n,5);u=rf'\frac{{{n}x}}{{5}}';c=tex(1/a)
  return rf'''Let $u={u}$. Differentiating gives $\mathrm{{d}}u={tex(a)}\,\mathrm{{d}}x$, so $\mathrm{{d}}x={c}\,\mathrm{{d}}u$.

Using the substitution and $\frac{{\mathrm{{d}}}}{{\mathrm{{d}}u}}\tanh u=\sech^2 u$,

$$\begin{{aligned}}
\int\sech^2({u})\,\mathrm{{d}}x
&={c}\int\sech^2 u\,\mathrm{{d}}u \\
&={c}\tanh u+C \\
&={c}\tanh({u})+C.
\end{{aligned}}$$

The argument is linear and the integrand is defined for every real $x$.'''
 return rf'''Let $u={n}x$. Then $\mathrm{{d}}x=\frac{{1}}{{{n}}}\,\mathrm{{d}}u$. When $x=1$, $u={n}$; when $x=2$, $u={2*n}$.

Using $\frac{{\mathrm{{d}}}}{{\mathrm{{d}}u}}\sech u=-\sech u\tanh u$,

$$\begin{{aligned}}
\int_1^2\sech({n}x)\tanh({n}x)\,\mathrm{{d}}x
&=\frac{{1}}{{{n}}}\int_{{{n}}}^{{{2*n}}}\sech u\tanh u\,\mathrm{{d}}u \\
&=\frac{{1}}{{{n}}}[-\sech u]_{{{n}}}^{{{2*n}}} \\
&=\frac{{1}}{{{n}}}(\sech {n}-\sech {2*n}).
\end{{aligned}}$$

The integrand is continuous on $[1,2]$, and the result is positive because $\sech u$ decreases for $u>0$.'''
def generate(level,seed=0,template=None,parameters=None):
 if level not in ('easy','moderate'):raise ValueError('Unsupported hard: no validated hard family')
 sid=template or ('q-95534' if level=='easy' else 'q-95535')
 bounds=range(1,13) if level=='easy' else range(3,15)
 p=parameters if parameters is not None else {'n':random.Random(seed).choice(list(bounds))}
 if sid not in DATA or DATA[sid][0]!=level or set(p)!={'n'} or type(p['n'])!=int or p['n'] not in bounds:raise ValueError('Outside finite parameter policy')
 n=p['n'];old=sources()[sid];of=old[':question/answer-fields'][0]
 replay=n==DATA[sid][1]
 prompt=old[':question/problem'] if replay else (rf'Calculate the integral $\displaystyle {MACROS} \int\sech^{{2}} (\frac{{{n}x}}{{5}})\,\mathrm{{d}}x$.' if level=='easy' else rf'Evaluate the integral $\displaystyle {MACROS} \int_{{1}}^{{2}}\sech {n}x\tanh {n}x\,\mathrm{{d}}x$.')
 vals=[a[':answer/value'] for a in of[':answer-field/choices']] if replay else values(level,n)
 fp=fingerprint({':question/problem':prompt});qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'task:'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 bank=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+val)),':answer/type':':answer.type/math',':answer/value':val} for val in vals]
 index=3 if level=='easy' else 4
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(level,n),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':bank,':answer-field/correct':[':answer/id',bank[index][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'parameters':p,'source_question':sid,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'bank_profile':sid,'mathematical_fingerprint':fp,'domain':'real x; definite interval [1,2]','dependencies':{'sympy':sp.__version__},'difficulty_origin':'authored easy: one indefinite linear substitution; authored moderate: definite substitution and endpoint evaluation','solution_origin':'authored; source keys/solutions absent','sampling_policy':'easy n=1..12 with coefficient n/5; moderate n=3..14; positive rational/integer extension; no negative or shifted arguments inferred'}}
def candidates(level):
 if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty')
 for n in (range(1,13) if level=='easy' else range(3,15)):yield 'q-95534' if level=='easy' else 'q-95535',{'n':n}
def batch(level,count,seed):
 if type(count)!=int or count<0:raise ValueError('Invalid count')
 ps=list(candidates(level));random.Random(seed).shuffle(ps)
 if count>len(ps):raise ValueError(f'Finite capacity {len(ps)}; requested {count}')
 return [generate(level,seed,s,p) for s,p in ps[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();rs=batch(o.difficulty,o.count,o.seed);print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,rs)))
