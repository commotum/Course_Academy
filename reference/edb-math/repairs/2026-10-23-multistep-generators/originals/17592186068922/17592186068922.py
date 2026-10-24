"""Bounded numerator scaling of fully replayed partial-fraction source banks.

k=1 replays sources; k=2..9 multiplies the integrand and the entire bank by k.
This explicit transport policy does not infer new misconception recipes.
Real antiderivatives apply on each connected interval excluding denominator roots.
"""
import argparse, hashlib, json, os, random, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE))
import printed as p
x=p.x;R=sp.Rational
KP_ID=17592186068922
KP_UUID='d54bab77-d77f-5275-b454-ddb565eaa280'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='partial-fractions-numerator-scale-1'
# level, response, numerator, first factor, second factor, complete source bank.
# Log banks store ordered (coefficient of ln|factor1|, coefficient of ln|factor2|).
DATA={
 'q-103989':('easy','logs',2*x-4,x,x-4,[(1,-1),(2,2),(1,2),(2,-2),(1,1)]),
 'q-49903':('easy','logs',6*x+12,x,x+3,[(4,2),(R(1,4),2),(R(1,4),R(1,2)),(1,2),(4,R(1,2))]),
 'q-103991':('easy','sum',7,x-1,x+6,[2,1,0,-1,-2]),
 'q-49604':('moderate','sum',13,2*x-3,3*x+2,[0,-2,2,1,-1]),
 'q-49905':('moderate','sum',5*x-1,x-3,2*x+1,[R(1,2),R(3,2),2,R(5,2),R(7,2)]),
 'q-103988':('moderate','logs',2*x+7,2*x+1,x+2,[(2,2),(4,1),(4,-1),(4,-2),(2,-1)]),
 'q-49908':('moderate','logs',2,x,3*x+1,[(2,1),(R(1,2),-1),(R(1,2),R(1,2)),(2,-2),(2,-3)]),
 'q-348896':('moderate','coefficients',7*x+7,x+3,x-4,[(2,5)]),
 'q-348898':('moderate','coefficients',7*x-11,x-8,x+1,[(5,2)]),
 'q-348933':('moderate','coefficients',11,2*x+5,x-2,[(-R(11,9),R(11,9))])}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())[0][0][':knowledge-point/questions']}
def math_data(t,k):
 level,kind,n,d1,d2,bank=DATA[t];n=sp.sympify(n)*k
 r1=sp.solve(d1,x)[0];r2=sp.solve(d2,x)[0]
 A=sp.simplify(n.subs(x,r1)/d2.subs(x,r1));B=sp.simplify(n.subs(x,r2)/d1.subs(x,r2))
 a=sp.simplify(A/sp.diff(d1,x));b=sp.simplify(B/sp.diff(d2,x))
 return n,d1,d2,A,B,a,b

def fingerprint(q):
 try:body,lo,hi=p.integral(q[':question/problem']);assert lo is None
 except (ValueError,AssertionError,IndexError,TypeError):
  # Underdefined f(x) source is retained and explicitly excluded, never stock.
  return hashlib.sha256(('excluded:'+q[':question/problem']).encode()).hexdigest()
 return hashlib.sha256(sp.srepr(sp.cancel(body)).encode()).hexdigest()
def latex(v):return sp.latex(sp.sympify(v))
def logsum(a,b,d1,d2):
 parts=[]
 for c,d in [(a,d1),(b,d2)]:
  c=sp.sympify(c);sign='-' if c<0 else ('+' if parts else '')
  if c==0:continue
  coeff='' if abs(c)==1 else latex(abs(c))
  parts.append(sign+coeff+r'\operatorname{ln}⁡|'+latex(d)+r'|')
 return ''.join(parts)+'+C'
def generate(level,seed,template,parameters):
 k=parameters['k']
 if template not in DATA or level!=DATA[template][0] or type(k) is not int or not 1<=k<=9:raise ValueError('Unsupported difficulty/template/parameter')
 old=sources()[template];level,kind,_,_,_,bank=DATA[template];n,d1,d2,A,B,a,b=math_data(template,k)
 fs=sorted(old[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
 denominator=latex(sp.expand(d1*d2)) if template=='q-49908' else '('+latex(d1)+')('+latex(d2)+')'
 integral=r'\int \frac{'+latex(n)+'}{'+denominator+r'}\,\text{d}x'
 if k==1:prompt=old[':question/problem']
 elif kind=='sum':prompt='Given that\n\n$$\n'+integral+'=a'+r'\operatorname{ln}⁡|'+latex(d1)+'|+b'+r'\operatorname{ln}⁡|'+latex(d2)+'|+C,\n$$\n\nfind the value of $a+b.$'
 elif kind=='coefficients':prompt='Evaluate the following indefinite integral and fill in the missing coefficients.\n\n$'+integral+'=$\n{{field-1}}'+r'$\,\operatorname{ln}⁡|'+latex(d1)+r'|\,+\,$'+'\n{{field-2}}'+r'$\,\operatorname{ln}⁡|'+latex(d2)+'|+C$'
 else:prompt='$'+integral+'=$'
 fp=fingerprint({':question/problem':prompt});uid=lambda s:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s))
 qid=uid('question:'+fp+':profile:'+template);fields=[]
 for i,of in enumerate(fs):
  fid=uid(qid+':field:'+of[':answer-field/key'])
  if k==1:values=[v[':answer/value'] for v in of[':answer-field/choices']]
  elif kind=='sum':values=[latex(sp.sympify(v)*k) for v in bank]
  elif kind=='logs':values=[logsum(sp.sympify(c)*k,sp.sympify(e)*k,d1,d2) for c,e in bank]
  else:values=[latex([a,b][i])]
  choices=[{':answer/id':uid(fid+':answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
  target= a+b if kind=='sum' else ([a,b][i] if kind=='coefficients' else None)
  if kind=='logs':matches=[j for j,v in enumerate(values) if sp.cancel(sp.diff(p.scalar(v),x)-n/(d1*d2))==0]
  else:matches=[j for j,v in enumerate(values) if sp.simplify(p.scalar(v)-target)==0]
  assert len(matches)==1
  fields.append({':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[matches[0]][':answer/id']]})
 r1=sp.solve(d1,x)[0];r2=sp.solve(d2,x)[0]
 # Same source sequence: factor, decompose, eliminate A then B, integrate, report.
 solution='First, we note that the denominator of the integrand can be factored as\n\n$$\n'+latex(sp.expand(d1*d2))+'=('+latex(d1)+')('+latex(d2)+').\n$$\n\nWe convert the integrand into a sum of partial fractions:\n\n$$\n'+r'\frac{'+latex(n)+'}{('+latex(d1)+')('+latex(d2)+r')}=\frac{A}{'+latex(d1)+r'}+\frac{B}{'+latex(d2)+'}.\n$$\n\nMultiplying by the denominator gives\n\n$$\n'+latex(n)+'=A('+latex(d2)+')+B('+latex(d1)+').\n$$\n\nPlugging in $x='+latex(r2)+',$ we can eliminate $A$ and solve for $B$:\n\n$$\n'+latex(n.subs(x,r2))+'='+latex(d1.subs(x,r2))+'B,\\qquad B='+latex(B)+'.\n$$\n\nPlugging in $x='+latex(r1)+',$ we can eliminate $B$ and solve for $A$:\n\n$$\n'+latex(n.subs(x,r1))+'='+latex(d2.subs(x,r1))+'A,\\qquad A='+latex(A)+'.\n$$\n\nFinally, we integrate, and we get\n\n$$\n'+r'\begin{aligned}'+integral+r'&='+latex(A)+r'\int \frac{1}{'+latex(d1)+r'}\,\text{d}x'+('+' if B>=0 else '-')+latex(abs(B))+r'\int \frac{1}{'+latex(d2)+r'}\,\text{d}x\\&='+logsum(a,b,d1,d2)+r'\end{aligned}'+'\n$$'
 if kind=='sum':solution+='\n\nFinally, $a='+latex(a)+',b='+latex(b)+',$ and $a+b='+latex(a+b)+'.$'
 if k==1:solution=old[':question/worked-solution']
 question={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':json.loads((HERE/'source.json').read_text())[0][0][':knowledge-point/title']},'question':question,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':template,'bank_profile':template,'seed':seed,'parameters':{'k':k},'policy':'Multiply source numerator and complete answer bank by k; fixed denominator and field layout','mathematical_fingerprint':fp,'domains':{'real':True,'excluded_poles':[str(r1),str(r2)],'primitive':'On each connected interval excluding poles'},'source_question':template,'dependencies':{'sympy':sp.__version__},'plots':[]}}
def candidates(level):
 if level not in ('easy','moderate'):raise ValueError('Unsupported difficulty: '+level)
 return [(t,{'k':k}) for k in range(2,10) for t in DATA if DATA[t][0]==level]
def batch(level,count,seed):
 cs=candidates(level);random.Random(seed).shuffle(cs)
 if count<0 or count>len(cs):raise ValueError('Finite variant limit; shortage remains explicit')
 return [generate(level,seed,t,params) for t,params in cs[:count]]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+ '\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
