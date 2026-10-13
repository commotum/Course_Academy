#!/usr/bin/env python3
"""Bounded source-profile tangent differentiation generator; no database writes."""
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
try:
 import sympy as sp
except ModuleNotFoundError:
 import os,sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186059676
KP_UUID='711f198b-26b4-5185-812a-102329d49313'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='1.0.1';SUPPORTED_LEVELS=('easy','moderate');HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
TITLE=SOURCE['record'][':knowledge-point/title'];SOURCE_BASIS=SOURCE['basis'];LINEAGE=SOURCE['lineage']
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROFILES={'q-341495':('easy',{'a':4,'b':3}), 'q-47983':('easy',{'a':1,'b':1}), 'q-70911':('easy',{'a':3,'b':2,'c':4}), 'q-103081':('moderate',{'a':1,'b':1}), 'q-17912':('moderate',{'a':1}), 'q-341825':('moderate',{'a':1,'b':1}), 'q-341858':('moderate',{'a':1,'b':2})}
x=sp.Symbol('x',positive=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def coeff(n):return '' if n==1 else str(n)
def half(n):return str(n//2) if n%2==0 else r'\frac{'+str(n)+'}{2}'
def num(n):return sp.latex(sp.sympify(n))
def candidates(sid):
 keys=PROFILES[sid][1]
 import itertools
 return [dict(zip(keys,z)) for z in itertools.product(*(range(1,7) for k in keys))]
def data(sid,p):
 a=p['a'];b=p.get('b',1);c=p.get('c',4);sec=1/sp.cos(x)**2
 if sid in ('q-341495','q-47983'):fun=a*sp.sqrt(x)+b*sp.tan(x);correct=a/(2*sp.sqrt(x))+b*sec
 elif sid=='q-70911':fun=a*(x*x-b*sp.tan(x))+c;correct=2*a*x-a*b*sec
 elif sid=='q-103081':fun=b*x-a*sp.tan(x);correct=b-2*a
 elif sid=='q-17912':fun=-a*sp.tan(x);correct=-a
 elif sid=='q-341825':fun=a*sp.tan(x)-b*x*x;correct=a
 else:fun=a*sp.tan(x)+b*sp.sin(x);correct=a+b
 if sid=='q-47983':bank=[(a+b*sp.sqrt(x)*sec)/(2*sp.sqrt(x)),(a+2*b/sp.cos(sp.sqrt(x))**2)/(2*sp.sqrt(x)),(a+2*b*x*sec)/(2*sp.sqrt(x)),(a+2*b*sp.sqrt(x)/sp.cos(x))/(2*sp.sqrt(x)),correct]
 elif sid=='q-70911':bank=[2*a-a*sp.cos(x)**2+c,a-a*b*sec,2*a*x-b*sec,correct,x-a/sp.cos(x)+c]
 elif sid=='q-103081':bank=[b+2*a,b,b-a*sp.sqrt(2),-b-2*a,correct]
 elif sid=='q-17912':bank=[correct,-a*sp.sqrt(2),a/sp.sqrt(3),a*sp.sqrt(2),a]
 else:bank=[correct]
 return fun,correct,list(map(sp.sympify,bank))
def replacements(sid,p):
 a=p['a'];b=p.get('b',1);c=p.get('c',4);A=coeff(a);B=coeff(b)
 if sid=='q-341495':return {'4\\sqrt{x}+3tan⁡x':f'{A}\\sqrt{{x}}+{B}tan⁡x','4\\frac{\\text{d}}{\\text{d}x}(\\sqrt{x})+3\\frac{\\text{d}}{\\text{d}x}(tan⁡x)':f'{a}\\frac{{\\text{{d}}}}{{\\text{{d}}x}}(\\sqrt{{x}})+{b}\\frac{{\\text{{d}}}}{{\\text{{d}}x}}(tan⁡x)','4(\\frac{1}{2\\sqrt{x}})+3({sec}^{2}⁡x)':f'{a}(\\frac{{1}}{{2\\sqrt{{x}}}})+{b}({{sec}}^{{2}}⁡x)',r'\frac{2}{\sqrt{x}}+3{sec}^{2}x':fr'\frac{{{half(a)}}}{{\sqrt{{x}}}}+{B}{{sec}}^{{2}}x',r'\frac{2}{\sqrt{x}}+3{sec}^{2}⁡x':fr'\frac{{{half(a)}}}{{\sqrt{{x}}}}+{B}{{sec}}^{{2}}⁡x'}
 if sid=='q-47983':
  base=r'\sqrt{x}+tan⁡x';new=fr'{A}\sqrt{{x}}+{B}tan⁡x'
  return {base:new,r'\frac{1}{2\sqrt{x}}+{sec}^{2}⁡x':fr'\frac{{{a}}}{{2\sqrt{{x}}}}+{B}{{sec}}^{{2}}⁡x',r'\frac{1+\sqrt{x}{sec}^{2}⁡x}{2\sqrt{x}}':fr'\frac{{{a}+{B}\sqrt{{x}}{{sec}}^{{2}}⁡x}}{{2\sqrt{{x}}}}',r'\frac{1+2{sec}^{2}⁡\sqrt{x}}{2\sqrt{x}}':fr'\frac{{{a}+{2*b}{{sec}}^{{2}}⁡\sqrt{{x}}}}{{2\sqrt{{x}}}}',r'\frac{1+2x{sec}^{2}⁡x}{2\sqrt{x}}':fr'\frac{{{a}+{2*b}x{{sec}}^{{2}}⁡x}}{{2\sqrt{{x}}}}',r'\frac{1+2\sqrt{x}sec⁡x}{2\sqrt{x}}':fr'\frac{{{a}+{2*b}\sqrt{{x}}sec⁡x}}{{2\sqrt{{x}}}}',r'\frac{1+2\sqrt{x}{sec}^{2}⁡x}{2\sqrt{x}}':fr'\frac{{{a}+{2*b}\sqrt{{x}}{{sec}}^{{2}}⁡x}}{{2\sqrt{{x}}}}'}
 if sid=='q-70911':return {'3({x}^{2}-2tan⁡x)+4':f'{a}({{x}}^{{2}}-{b}tan⁡x)+{c}','3{x}^{2}-6tan⁡x+4':f'{a}{{x}}^{{2}}-{a*b}tan⁡x+{c}','3\\cdot 2x-6{sec}^{2}⁡x+0':f'{a}\\cdot 2x-{a*b}{{sec}}^{{2}}⁡x+0','6x-6{sec}^{2}⁡x':f'{2*a}x-{a*b}{{sec}}^{{2}}⁡x','6-3{cos}^{2}⁡x+4':f'{2*a}-{a}{{cos}}^{{2}}⁡x+{c}','3-6{sec}^{2}⁡x':f'{a}-{a*b}{{sec}}^{{2}}⁡x','6x-2{sec}^{2}⁡x':f'{2*a}x-{b}{{sec}}^{{2}}⁡x','x-3sec⁡x+4':f'x-{a}sec⁡x+{c}'}
 if sid=='q-103081':return {'x-\\operatorname{tan}⁡x':f'{B}x-{A}\\operatorname{{tan}}⁡x','1-{sec}^{2}⁡x':f'{b}-{A}{{sec}}^{{2}}⁡x','1-{sec}^{2}⁡(\\frac{\\pi }{4})':f'{b}-{A}{{sec}}^{{2}}⁡(\\frac{{\\pi }}{{4}})','1-(\\sqrt{2})^{2}':f'{b}-{A}(\\sqrt{{2}})^{{2}}','1-2':f'{b}-{2*a}','-1':num(b-2*a),'3':num(b+2*a),'1':num(b),'1-\\sqrt{2}':f'{b}-{A}\\sqrt{{2}}','-3':num(-b-2*a)}
 if sid=='q-17912':return {'-tan⁡x':f'-{A}tan⁡x','-{sec}^{2}⁡x':f'-{A}{{sec}}^{{2}}⁡x','-{sec}^{2}⁡\\pi ':f'-{A}{{sec}}^{{2}}⁡\\pi ','-1\\cdot (-1)^{2}':f'-{a}\\cdot (-1)^{{2}}','-1':str(-a),'-\\sqrt{2}':f'-{A}\\sqrt{{2}}','\\frac{1}{\\sqrt{3}}':fr'\frac{{{a}}}{{\sqrt{{3}}}}','\\sqrt{2}':f'{A}\\sqrt{{2}}','1':str(a)}
 if sid=='q-341825':return {'\\operatorname{tan}⁡x-{x}^{2}':f'{A}\\operatorname{{tan}}⁡x-{B}{{x}}^{{2}}','{sec}^{2}⁡x-2x':f'{A}{{sec}}^{{2}}⁡x-{2*b}x','{sec}^{2}⁡(0)-2\\cdot 0':f'{A}{{sec}}^{{2}}⁡(0)-{2*b}\\cdot 0','{(\\frac{1}{\\operatorname{cos}⁡(0)})}^{2}-0':f'{a}{{(\\frac{{1}}{{\\operatorname{{cos}}⁡(0)}})}}^{{2}}-0','{(\\frac{1}{1})}^{2}':f'{a}{{(\\frac{{1}}{{1}})}}^{{2}}',' & =1.':f' & ={a}.','is $1.$':f'is ${a}.$'}
 return {'tan⁡x+2sin⁡x':f'{A}tan⁡x+{B}sin⁡x','{sec}^{2}⁡x+2cos⁡x':f'{A}{{sec}}^{{2}}⁡x+{B}cos⁡x','{sec}^{2}⁡(0)+2cos⁡(0)':f'{A}{{sec}}^{{2}}⁡(0)+{B}cos⁡(0)','1+2(1)':f'{a}+{b}(1)',' & =3.':f' & ={a+b}.','is $3.$':f'is ${a+b}.$'}
# Numeric answers use field-specific rendering, never global digit substitution.
_original_replacements = replacements
def replacements(sid,p):
 r=_original_replacements(sid,p);a=p['a'];b=p.get('b',1)
 if sid=='q-103081':
  for key in ('-1','3','1',r'1-\sqrt{2}','-3'):r.pop(key,None)
  r[' & =-1.']=f" & ={b-2*a}."
 if sid=='q-17912':
  for key in ('-1',r'-\sqrt{2}',r'\frac{1}{\sqrt{3}}',r'\sqrt{2}','1'):r.pop(key,None)
  r[' & =-1.']=f" & ={-a}.";r['is $-1.$']=f"is ${-a}.$"
 if sid=='q-341825':
  for k in (r'{(\frac{1}{\operatorname{cos}⁡(0)})}^{2}-0',r'{(\frac{1}{1})}^{2}'):
   r[k]=r[k].removeprefix('1') if a==1 else r[k]
 return r

def numeric_bank(sid,p):
 a=p['a'];b=p.get('b',1);A=coeff(a)
 if sid=='q-103081':return [str(b+2*a),str(b),fr'{b}-{A}\sqrt{{2}}',str(-b-2*a),str(b-2*a)]
 if sid=='q-17912':return [str(-a),fr'-{A}\sqrt{{2}}',fr'\frac{{{a}}}{{\sqrt{{3}}}}',fr'{A}\sqrt{{2}}',str(a)]
 return None

def render(text,repl):
 return re.sub('|'.join(re.escape(k) for k in sorted(repl,key=len,reverse=True)),lambda m:repl[m[0]],text)
def generate(level,seed=0,template=None,parameters=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
 rng=random.Random(seed);sid=template or rng.choice([s for s,(l,p) in PROFILES.items() if l==level]);assert PROFILES[sid][0]==level
 ps=candidates(sid);rng.shuffle(ps)
 if parameters is not None and parameters not in ps:raise ValueError('Parameters outside documented 1..6 integer bounds')
 if parameters is not None:ps=[parameters]
 for p in ps:
  fun,correct,bank=data(sid,p)
  if any(sp.expand(bank[i]-bank[j])==0 for i in range(len(bank)) for j in range(i)):continue
  break
 else:raise ValueError('Finite profile has no eligible parameters')
 old=SOURCES[sid];of=old[':question/answer-fields'][0];repl=replacements(sid,p)
 rf=lambda t:render(t,repl)
 task=digest([str(sp.expand(fun-fun.subs(x,0))) if sid=='q-70911' else str(sp.expand(fun)),str(sp.pi/4 if sid=='q-103081' else sp.pi if sid=='q-17912' else 0) if level=='moderate' else 'expression'])
 qid=uid('question:'+VERSION+':'+sid+':'+task+':'+digest([rf(old[':question/problem']),rf(old[':question/worked-solution']),p]));fid=uid('field:'+qid);choices=[]
 for i,old_a in enumerate(of[':answer-field/choices']):
  nb=numeric_bank(sid,p)
  val=nb[i] if nb is not None else rf(old_a[':answer/value'])
  if len(bank)==1:val=rf(old_a[':answer/value']) if sid=='q-341495' else str(correct)
  choices.append({':answer/id':uid('answer:'+fid+':'+str(i)),':answer/type':':answer.type/math',':answer/value':val})
 right=next(i for i,a0 in enumerate(of[':answer-field/choices']) if a0[':answer/id']==of[':answer-field/correct'][':answer/id'])
 q={':question/id':qid,':question/problem':rf(old[':question/problem']),':question/worked-solution':rf(old[':question/worked-solution']),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[right][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'source_question':old[':question/id'],'domain':'x>0 and cos(x)!=0 for radical templates; otherwise cos(x)!=0; evaluated points are regular','mathematical_fingerprint':task,'dependencies':{'sympy':sp.__version__},'sampling_policy':'positive integer coefficients 1..6; fixed source evaluation point; explicit coefficient extension'}}
def batch(level,count,seed):
 out=[];seen=set()
 for i in range(10000):
  r=generate(level,seed+i);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('finite-limit')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args();rs=batch(args.difficulty,args.count,args.seed);print(json.dumps({'instances':rs},indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,rs)))
