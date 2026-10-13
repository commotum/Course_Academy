#!/usr/bin/env python3
"""Bounded hyperbolic linear-argument substitution generator; see package evidence."""
import argparse, json, random, uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186166784
KP_UUID='c6f89636-f9bd-563d-a489-2a16746f8707'
TITLE='Integrating Hyperbolic Functions With Linear Arguments'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.0'
SOURCE_BASIS=1972
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SUPPORTED_LEVELS=('easy','moderate')
HERE=Path(__file__).with_suffix('')
DEFAULTS={'q-95532':{'a':4,'b':-3},'q-95533':{'n':3}}
LEVELS={'q-95532':'easy','q-95533':'moderate'}
X=sp.Symbol('x',real=True)
C=sp.Symbol('C',real=True)
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def domain(m):
 return [{'a':a,'b':b} for a in range(3,9) for b in range(-5,0)] if m=='q-95532' else [{'n':n} for n in range(3,11)]
def fraction(n,d):return str(n) if d==1 else r'\frac{'+str(n)+'}{'+str(d)+'}'
def rat(v):return fraction(v.p,v.q)
def objects(m,p):
 if m=='q-95532':
  a,b=map(sp.Integer,(p['a'],p['b']));z=a*X+b
  return sp.sinh(z),sp.cosh(z)/a,[sp.cosh(a*X-b)/(-b),2*sp.cosh(z)/a,-sp.cosh(z)/a,sp.cosh(z)/a,sp.cosh(z)]
 n=sp.Integer(p['n']);result=n*sp.sinh(1/n)/2
 return sp.cosh((2*X-1)/n),result,[(n-1)*sp.sinh(sp.exp(n-1)+1)/n,result,(n-1)*sp.sinh(n/(n-1))/n,-(n-1)*sp.sinh(sp.exp(n-1)-1)/n,sp.sinh(1/n)/n]
def fingerprint(q):
 import re
 t=q[':question/problem']
 m=re.fullmatch(r'What is \$\\displaystyle \\int\\sinh \(([0-9]+)x - ([0-9]+)\)dx\$\?',t)
 if m:return 'indefinite:sinh:'+m[1]+':-'+m[2]
 m=re.fullmatch(r'Evaluate the integral \$\\displaystyle \\int_\{1/2\}\^\{1\}\\cosh \(\\frac\{2x - 1\}\{([0-9]+)\}\)dx\$\.',t)
 if m:return 'definite:cosh:2/n:-1/n:1/2:1:n='+m[1]
 return 'outside-supported-template:'+t

def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 m=template or ('q-95532' if level=='easy' else 'q-95533')
 if m not in LEVELS or LEVELS[m]!=level or profile not in (None,m):raise ValueError('Template/profile mismatch')
 p=dict(parameters) if parameters is not None else random.Random(seed).choice(domain(m))
 if p not in domain(m) or any(type(v)!=int for v in p.values()):raise ValueError('Outside bounded domain')
 integrand,correct,bank=objects(m,p)
 if m=='q-95532':
  a,b=p['a'],p['b'];z=f'{a}x - {-b}';opposite=f'{a}x + {-b}'
  values=[fraction(1,-b)+r'\cosh ('+opposite+') + C',rat(sp.Rational(2,a))+r'\cosh ('+z+') + C','-'+fraction(1,a)+r'\cosh ('+z+') + C',fraction(1,a)+r'\cosh ('+z+') + C',r'\cosh ('+z+') + C']
  # Preserve the source's unreduced coefficient spelling at its original parameters.
  problem=r'What is $\displaystyle \int\sinh ('+z+r')dx$?'
  solution='Let $u='+z+'$. Then $du='+str(a)+r'\,dx$, so $dx='+fraction(1,a)+r'\,du$.'+'\n\n$$\n'+r'\int\sinh ('+z+r')dx = '+fraction(1,a)+r'\int\sinh u\,du = '+fraction(1,a)+r'\cosh u + C = '+values[3]+'\n$$'
  ci=3
 else:
  n=p['n'];small=fraction(1,n);r=fraction(n-1,n)
  values=[r+r'\sinh (e^{'+str(n-1)+r'} + 1)',fraction(n,2)+r'\sinh ('+small+')',r+r'\sinh ('+fraction(n,n-1)+')','-'+r+r'\sinh (e^{'+str(n-1)+r'} - 1)',small+r'\sinh ('+small+')']
  problem=r'Evaluate the integral $\displaystyle \int_{1/2}^{1}\cosh (\frac{2x - 1}{'+str(n)+r'})dx$.'
  solution=r'Let $u=\frac{2x-1}{'+str(n)+r'}$. Then $du=\frac{2}{'+str(n)+r'}\,dx$, so $dx='+fraction(n,2)+r'\,du$. The bounds $x=\frac{1}{2}$ and $x=1$ become $u=0$ and $u='+small+'$.'+'\n\n$$\n'+fraction(n,2)+r'\int_{0}^{'+small+r'}\cosh u\,du = '+fraction(n,2)+r'[\sinh u]_{0}^{'+small+r'} = '+fraction(n,2)+r'(\sinh ('+small+r')-\sinh 0) = '+values[1]+'\n$$'
  ci=1
 key=json.dumps([VERSION,m,p,values],sort_keys=True);qid=uid('question:'+key);fid=uid('field:'+qid+':selection')
 answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':m,'bank_profile':m,'parameters':p,'parameter_fingerprint':fingerprint(q),'source_questions':[m],'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'domains':['x real'],'dependencies':{'sympy':sp.__version__},'plot_requirements':'none','authored_extensions':['difficulty rating','missing correct designation','missing worked solution'],'correct_expression':str(correct)}}
def batch(level,count,seed=0):
 if level not in SUPPORTED_LEVELS or type(count)!=int or count<0:raise ValueError('Unsupported level/count')
 m='q-95532' if level=='easy' else 'q-95533';pool=domain(m);random.Random(seed).shuffle(pool)
 return [generate(level,seed,m,p) for p in pool[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');a.add_argument('--template');p=a.parse_args();rows=batch(p.difficulty,p.count,p.seed) if not p.template else [generate(p.difficulty,p.seed,p.template)];print(json.dumps(rows,indent=2) if p.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
