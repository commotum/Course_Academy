"""Finite complete-bank amplitude transport for real trig quotient substitution.

m=1 replays supported sources; m=2..12 changes actual integrands and banks.
Unusable real/duplicate source banks are explicitly excluded, never repaired.
"""
import argparse,hashlib,json,os,random,sys,uuid
from pathlib import Path
try:import sympy as sp
except ImportError:
 if __name__=='__main__':
  runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186068918
KP_UUID='fc24eade-1b3d-5672-88fd-0bb48b371509'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='trig-quotient-amplitude-1'
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE));import printed as p
x=p.x;u=p.u
# level, denominator substitution, outer factor, transformed integrand, primitive, bounds
DATA={
 'q-49557':('easy',sp.sin(x),2,1/u,sp.log(u),None,None),
 'q-113998':('hard',sp.csc(x)+2,-2,1/u,sp.log(u),None,None),
 'q-350887':('hard',sp.sin(x)**2+3,1,1/u,sp.log(u),0,sp.pi/2),
 'q-350901':('hard',8*sp.cos(x)**3+5,-1,1/u,sp.log(u),sp.pi/3,sp.pi/2),
 'q-350904':('hard',sp.csc(x)+2,-1,1/u,sp.log(u),sp.pi/6,sp.pi/2),
 'q-73674':('hard',sp.sin(x**2),sp.Rational(1,2),1/u,sp.log(u),None,None),
 'q-113997':('hard',sp.tan(x)+1,1,1-1/u,u-sp.log(u),None,None)}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['kp'][':knowledge-point/questions']}
def math_data(t,m):
 level,inner,c,h,H,lo,hi=DATA[t];factor=c*m
 f=factor*sp.diff(inner,x)*h.subs(u,inner)
 F=factor*H.subs(u,inner)
 answer=F if lo is None else sp.simplify(F.subs(x,hi)-F.subs(x,lo))
 return f,F,answer,factor,inner,h,H,lo,hi

def latex(e):
 # log absolute values on real nonzero branches; definite positive logs too.
 return sp.latex(e).replace(r'\log',r'\ln')
def abs_latex(e):
 if e.func==sp.log:return r'\ln|'+latex(e.args[0])+'|'
 if e.is_Add:return '+'.join(abs_latex(a) for a in e.args).replace('+-','-')
 if e.is_Mul:
  logs=[a for a in e.args if a.has(sp.log)]
  if len(logs)==1:return latex(e/logs[0])+abs_latex(logs[0])
 return latex(e)
def fingerprint(q):
 f,lo,hi=p.integral(q[':question/problem']);return hashlib.sha256(json.dumps([sp.srepr(sp.cancel(sp.trigsimp(f))),None if lo is None else sp.srepr(lo),None if hi is None else sp.srepr(hi)]).encode()).hexdigest()
def generate(level,seed=0,template=None,parameters=None):
 t=template or next((t for t in DATA if DATA[t][0]==level),None);params=parameters or {'m':2};m=params.get('m')
 if t not in DATA or DATA[t][0]!=level or set(params)!={'m'} or type(m)is not int or not 1<=m<=12:raise ValueError('Unsupported level/template/amplitude')
 old=sources()[t];of=old[':question/answer-fields'][0];f,F,answer,factor,inner,h,H,lo,hi=math_data(t,m);indef=lo is None
 values0=[p.scalar(a[':answer/value']).subs(p.C,0) for a in of[':answer-field/choices']];bank=[a*m for a in values0]
 if of.get(':answer-field/correct'):ci=next(i for i,a in enumerate(of[':answer-field/choices']) if a[':answer/id']==of[':answer-field/correct'][':answer/id'])
 else:ci=next(i for i,a in enumerate(bank) if sp.trigsimp(sp.diff(a-F,x))==0)
 integral=r'\int '+latex(f)+r'\,\text{d}x' if indef else r'{\int }_{'+latex(lo)+r'}^{'+latex(hi)+'}'+latex(f)+r'\,\text{d}x'
 if m==1:prompt=old[':question/problem'];values=[a[':answer/value'] for a in of[':answer-field/choices']]
 else:
  prompt=('What is $'+integral+'$?' if t=='q-49557' else 'Calculate $'+integral+'.$' if indef else 'Evaluate the following integral. Do not round the answer.\n\n$'+integral+'=$\n{{field-1}}')
  values=[(abs_latex(a)+'+C') if indef else latex(a) for a in bank]
  if t=='q-350904':values[0]=r'\operatorname{ln}('+latex(sp.Rational(4,3))+')' if m==1 else latex(bank[0]) # retain two canonical aliases as separate field-owned answers
 sol='Let $u='+latex(inner)+',$ then\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+latex(sp.diff(inner,x))+'.\n$$\n\n'
 if not indef:
  ulo=sp.simplify(inner.subs(x,lo));uhi=sp.simplify(inner.subs(x,hi))
  sol+='Calculating the limits for $u$ gives\n\n| $x$ | $'+latex(lo)+'$ | $'+latex(hi)+'$ |\n| --- | --- | --- |\n| $u$ | $'+latex(ulo)+'$ | $'+latex(uhi)+'$ |\n\n'
 sol+='Using the above, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+integral+r' &= '+latex(factor)
 if indef:sol+=r'\int '+latex(h)+r'\,\text{d}u \\ &= '+abs_latex(factor*H)+r'+C \\ &= '+abs_latex(F)+r'+C'
 else:
  limits=r'_{'+latex(ulo)+'}^{'+latex(uhi)+'}'
  sol+=r'{\int }'+limits+latex(h)+r'\,\text{d}u \\ &= '+latex(factor*H)+r'\big|'+limits+r' \\ &= '+latex((factor*H).subs(u,uhi))+'-('+latex((factor*H).subs(u,ulo))+r') \\ &= '+latex(answer)
 sol+=r'\end{aligned}'+'\n$$'
 if m==1 and old.get(':question/worked-solution'):sol=old[':question/worked-solution']
 fp=fingerprint({':question/problem':prompt});uid=lambda a:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),a));qid=uid('question:'+fp+':profile:'+t);fid=uid(qid+':field:'+of[':answer-field/key'])
 answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Integrating Quotients Containing Trigonometric Functions Using Substitution'},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':t,'profile':t if len(bank)>2 else None,'parameters':params,'source_question':t,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'mathematical_fingerprint':fp,'domain':'Connected real intervals excluding trig poles and zeros of denominator; log absolute values. Definite denominators strictly positive on stated closed intervals.','dependencies':{'sympy':sp.__version__},'recipe_policy':'Positive amplitude transports every complete source-bank value, not a pooled or inferred misconception bank.'}}
def candidates(level):
 for t in DATA:
  if DATA[t][0]==level:
   for m in range(2,13):yield t,{'m':m}
def batch(level,count,seed):
 if level not in ('easy','hard') or type(count)is not int or count<1:raise ValueError('Unsupported level/count')
 c=list(candidates(level));random.Random(seed).shuffle(c)
 if count>len(c):raise ValueError('Finite variant limit: '+str(len(c)))
 return [generate(level,seed,t,a) for t,a in c[:count]]
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');v=a.parse_args();rs=batch(v.difficulty,v.count,v.seed);print(json.dumps(rs,indent=2) if v.format=='json' else '\n\n'.join(map(markdown,rs)))
