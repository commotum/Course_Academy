#!/usr/bin/env python3
"""Finite source-bank-preserving substitution generator; no database writes."""
import argparse,hashlib,json,random,uuid,sys,os,re
from pathlib import Path
try: import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186166786
KP_UUID='947ecbc7-e09a-58b6-916d-a2562a1e794a'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
TITLE='Integrating Products Containing Hyperbolic Functions Using Substitution'
VERSION='hyperbolic-product-bounded-1'
HERE=Path(__file__).resolve().with_suffix('')
DATA={'q-95537':('easy',2),'q-95543':('moderate',1)}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def fingerprint(q):
 p=q[':question/problem']
 if 'sinh{x^3}' in p:return digest(['canonical',-2,2,'x^2sinh(x^3)'])
 if 'cosh' in p:
  m=re.search(r'cosh\s*\((\d+)x\^\{2\}\)',p)
  if not m:raise ValueError('Unknown cosh task')
  return digest(['x*cosh(a*x^2)',int(m[1]),'indefinite'])
 if 'sech' in p:
  m=re.search(r'\\int_\{1\}\^\{e(?:\^\{(\d+)\})?\}',p)
  if not m:raise ValueError('Unknown sech task')
  return digest(['sech^2(ln(x))/x',1,int(m[1] or 1)])
 raise ValueError('Unknown task')
def values(level,n):
 if level=='easy':
  return [r'\frac{1}{2}\sinh (x^{2}) + C',rf'\frac{{1}}{{{2*n}}}\sinh ({n}x^{{2}}) + C',rf'-\frac{{1}}{{{2*n}}}\sinh ({n}x^{{2}}) + C',r'-\frac{1}{2}\sinh (x^{2}) + C',rf'\frac{{1}}{{2}}\sinh ({2*n}x^{{2}}) + C']
 E='e' if n==1 else rf'e^{{{n}}}';E2=rf'e^{{{2*n}}}'
 return [rf'\frac{{1 - 2{E}}}{{{E2} + 1}}',rf'\frac{{{E} - 1}}{{2{E} + 1}}',rf'\frac{{{E} + 1}}{{{E} - 1}}',rf'\frac{{{E2} - 1}}{{{E2} + 1}}',rf'\frac{{{E2} + 1}}{{{E2} - 1}}']
def solution(level,n):
 if level=='easy':return rf'''Let $u={n}x^2$. Differentiating gives $\mathrm{{d}}u={2*n}x\,\mathrm{{d}}x$, so $x\,\mathrm{{d}}x=\frac{{1}}{{{2*n}}}\mathrm{{d}}u$.

Using this substitution,

$$\begin{{aligned}}
\int x\cosh({n}x^2)\,\mathrm{{d}}x
&=\frac{{1}}{{{2*n}}}\int\cosh u\,\mathrm{{d}}u \\
&=\frac{{1}}{{{2*n}}}\sinh u+C \\
&=\frac{{1}}{{{2*n}}}\sinh({n}x^2)+C.
\end{{aligned}}$$

This antiderivative is defined for every real $x$.'''
 return rf'''Let $u=\ln x$. Differentiating gives $\mathrm{{d}}u=\frac{{1}}{{x}}\mathrm{{d}}x$.

The limits change from $x=1$ to $u=0$, and from $x=e^{{{n}}}$ to $u={n}$. Therefore,

$$\begin{{aligned}}
\int_1^{{e^{{{n}}}}}\frac{{\operatorname{{sech}}^2(\ln x)}}{{x}}\,\mathrm{{d}}x
&=\int_0^{{{n}}}\operatorname{{sech}}^2 u\,\mathrm{{d}}u \\
&=\left[\tanh u\right]_0^{{{n}}} \\
&=\tanh {n}-\tanh 0 \\
&=\frac{{e^{{{2*n}}}-1}}{{e^{{{2*n}}}+1}}.
\end{{aligned}}$$

The original interval has $x>0$, so $\ln x$ and the substitution are defined throughout.'''
def generate(level,seed=0,template=None,parameters=None):
 if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty')
 sid=template or ('q-95537' if level=='easy' else 'q-95543')
 p=parameters if parameters is not None else {'n':random.Random(seed).randint(2 if level=='easy' else 1,12 if level=='easy' else 10)}
 if sid not in DATA or DATA[sid][0]!=level or set(p)!={'n'} or type(p['n'])!=int or not (2 if level=='easy' else 1)<=p['n']<=(12 if level=='easy' else 10):raise ValueError('Outside finite sampling policy')
 n=p['n'];old=sources()[sid];of=old[':question/answer-fields'][0]
 if level=='easy':prompt=old[':question/problem'].replace(r'\intx',r'\int x').replace('2x^{2}',str(n)+'x^{2}')
 else:
  upper='e' if n==1 else rf'e^{{{n}}}'
  prompt=old[':question/problem'].replace(r'^{e}',f'^{{{upper}}}').replace('sech',r'\operatorname{sech}')
 vals=[a[':answer/value'] for a in of[':answer-field/choices']] if n==DATA[sid][1] else values(level,n)
 fp=fingerprint({':question/problem':prompt});qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'task:'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+val)),':answer/type':':answer.type/math',':answer/value':val} for val in vals]
 correct=1 if level=='easy' else 3
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(level,n),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',answers[correct][':answer/id']],':answer-field/choices':answers}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'parameters':p,'source_question':sid,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'bank_profile':sid,'mathematical_fingerprint':fp,'dependencies':{'sympy':sp.__version__},'domain':'all real x' if level=='easy' else f'1 <= x <= exp({n})','difficulty_origin':'authored: indefinite direct substitution easy; definite log substitution with transformed endpoints moderate','solution_origin':'authored; sources lack keys and solutions','sampling_policy':'easy n=2..12; moderate n=1..10. Observed-shape distractor extensions; mistake interpretations unresolved.'}}
def candidates(level):
 if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty')
 for n in range(2 if level=='easy' else 1,13 if level=='easy' else 11):yield 'q-95537' if level=='easy' else 'q-95543',{'n':n}
def batch(level,count,seed):
 if type(count)!=int or count<0:raise ValueError('Invalid count')
 ps=list(candidates(level));random.Random(seed).shuffle(ps)
 if count>len(ps):raise ValueError(f'Finite capacity {len(ps)}; requested {count}')
 return [generate(level,seed,s,p) for s,p in ps[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();rs=batch(o.difficulty,o.count,o.seed);print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,rs)))
