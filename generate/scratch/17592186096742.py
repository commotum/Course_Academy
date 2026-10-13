"""Repeated chain rule: bounded, source-profile preserving generators.

Numeric substitutions preserve the captured prose, answer layout and banks.
Unrated linear trig-power sources supply an explicitly authored easy band.
The zero-at-origin exponential source is replay-only; the fieldless source is
excluded. These restrictions prevent cosmetic parameters from making inventory.
"""
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
try:
 import sympy as sp
except ImportError:
 if __name__=='__main__':
  runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
  os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186096742
KP_UUID='f3ee0d5d-0821-5f6b-b613-6b814e65df50'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='repeated-chain-rule-1'
HERE=Path(__file__).with_suffix('')
# source: (level, original varying parameter, replacement map)
DATA={
 'q-48569':('easy',3), 'q-48570':('easy',4),
 'q-312907':('moderate',5), 'q-2397':('moderate',9),
 'q-31352':('moderate',6), 'q-342927':('moderate',1),
 'q-31361':('hard',5), 'q-28655':('hard',5)}

def sources():
 return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}

def transport(t,s,a):
 if t=='q-342927':return s.replace('2x-1',f'2x-{a}')
 if t=='q-48569':return re.sub(r'(?<!\d)9(?!\d)',str(3*a),s).replace('3x',f'{a}x')
 maps={
  'q-48569':{9:3*a,3:a}, 'q-48570':{12:3*a,4:a},
  'q-312907':{120:24*a,15:3*a,5:a},
  'q-2397':{54:6*a,18:2*a,9:a},
  'q-31352':{6:a}, 'q-31361':{20:4*a,5:a}, 'q-28655':{5:a}}
 return re.sub(r'\d+',lambda m:str(maps[t].get(int(m[0]),int(m[0]))),s)

def function(t,a):
 x=sp.Symbol('x',real=True)
 if t=='q-48569':return x,sp.cos(a*x)**3,None
 if t=='q-48570':return x,sp.sin(a*x)**3,None
 if t=='q-312907':return x,sp.cos(a*x**3)**8,None
 if t=='q-2397':return x,sp.sin(a*x**2-1)**3,None
 if t=='q-31352':return x,sp.cot((x+a)**2),None
 if t=='q-342927':return x,sp.sqrt(sp.cos(2*x-a)),None
 if t=='q-31361':return x,sp.cot(a*x-1)**4,0
 if t=='q-28655':return x,sp.Integer(a)**sp.log(sp.cos(x)),0
 raise ValueError(t)

def fingerprint(q):
 # Parsed assessed function and evaluation point; no seed, identity or bank order.
 from sys import path
 if str(HERE) not in path:path.insert(0,str(HERE))
 from math_parser import given
 f,p=given(q[':question/problem'])
 return hashlib.sha256(json.dumps([sp.srepr(f),str(p)]).encode()).hexdigest()

def authored_solution(t,a):
 trig='cos' if t=='q-48569' else 'sin';du=r'-\sin v' if trig=='cos' else r'\cos v'
 final=(f'-{3*a}'+r'\cos^{2} '+str(a)+r'x\sin '+str(a)+'x') if trig=='cos' else (str(3*a)+r'\sin^{2} '+str(a)+r'x\cos '+str(a)+'x')
 return ("First, we express $f$ as the composite function\n\n$$\nf=u^3,\\,u=\\"+trig+" v,\\,v="+str(a)+"x.\n$$\n\nDifferentiating gives\n\n$$\n\\frac{\\mathrm{d}f}{\\mathrm{d}u}=3u^2,\\quad \\frac{\\mathrm{d}u}{\\mathrm{d}v}="+du+",\\quad \\frac{\\mathrm{d}v}{\\mathrm{d}x}="+str(a)+".\n$$\n\nApplying now the chain rule twice, we get\n\n$$\n\\begin{aligned}f'(x)&=\\frac{\\mathrm{d}f}{\\mathrm{d}u}\\cdot\\frac{\\mathrm{d}u}{\\mathrm{d}v}\\cdot\\frac{\\mathrm{d}v}{\\mathrm{d}x}\\\\\n&=3u^2\\cdot ("+du+")\\cdot "+str(a)+"\\\\\n&="+final+".\\end{aligned}\n$$")

def generate(level,seed=0,template=None,parameters=None):
 eligible=[t for t,(lv,_) in DATA.items() if lv==level and t!='q-28655']
 if not eligible:raise ValueError('Unsupported difficulty')
 rng=random.Random(seed);t=template or rng.choice(eligible)
 if t not in DATA or DATA[t][0]!=level:raise ValueError('Unsupported level/template')
 a=(parameters or {'a':rng.choice(list(range(2,13)))})['a']
 if parameters is not None and set(parameters)!={'a'}:raise ValueError('Only parameter a is supported')
 if type(a)is not int or not 1<=a<=12:raise ValueError('Integer parameter 1..12 required')
 if t=='q-28655' and a!=5:raise ValueError('Zero-at-origin source is replay-only')
 if t in ('q-48569','q-48570') and a==1:raise ValueError('Unit frequency collapses complete bank')
 old=sources()[t];of=old[':question/answer-fields'][0]
 prompt=transport(t,old[':question/problem'],a)
 sol=transport(t,old[':question/worked-solution'],a) if old.get(':question/worked-solution') else authored_solution(t,a)
 values=[transport(t,b[':answer/value'],a) for b in of[':answer-field/choices']]
 correct=of.get(':answer-field/correct')
 ci=next(i for i,b in enumerate(of[':answer-field/choices']) if b[':answer/id']==correct[':answer/id']) if correct else 0
 fp=fingerprint({':question/problem':prompt});uid=lambda s:str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s))
 qid=uid('question:'+fp+':profile:'+t);fid=uid(qid+':field:'+of[':answer-field/key'])
 answers=[{':answer/id':uid(fid+':answer:'+str(i)),':answer/type':b[':answer/type'][':db/ident'],':answer/value':val} for i,(b,val) in enumerate(zip(of[':answer-field/choices'],values))]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
 x,f,point=function(t,a)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Calculating a Derivative Using Multiple Instances of the Chain Rule'},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':t,'profile':t if len(answers)>1 else None,'parameters':{'a':a},'source_question':t,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'mathematical_fingerprint':fp,'domain':'x real; sqrt(cos(2x-a)) differentiable where cos(2x-a)>0; cotangent arguments not integer multiples of pi; exponential-log replay where cos(x)>0; trig angles radians.','dependencies':{'sympy':sp.__version__},'easy_classification_authored':level=='easy','missing_solution_authored':not bool(old.get(':question/worked-solution')),'missing_key_inferred':not bool(correct)}}

def candidates(level):
 for t,(lv,original) in DATA.items():
  if lv==level and t!='q-28655':
   for a in range(2 if level=='easy' else 1,13):
    if a!=original:yield t,{'a':a}

def batch(level,count,seed=0):
 c=list(candidates(level));random.Random(seed).shuffle(c)
 if type(count)is not int or count<1 or count>len(c):raise ValueError(f'Finite variant limit for {level}: {len(c)}')
 return [generate(level,seed,t,p) for t,p in c[:count]]

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value']+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True,choices=['easy','moderate','hard','all']);p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=[r for lv in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for r in batch(lv,a.count,a.seed)];print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
