#!/usr/bin/env python3
"""Chain/quotient derivatives. Exact source banks; bounded, distinct task sampling.
Read the adjacent classification, extraction, capabilities and validation reports.
No database access. Easy is deliberately unsupported, not relabeled moderate.
"""
import argparse, hashlib, json, random, uuid
from pathlib import Path
try:
 import sympy as s
except ModuleNotFoundError:
 import os,sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if Path(sys.executable).absolute()==runtime.absolute():raise
 os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186096844
KP_UUID='261910cd-a1a4-5c90-8caa-238208558458'
TITLE='Calculating a Derivative Using the Chain and Quotient Rules'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
HERE=Path(__file__).with_suffix(''); VERSION='1.0.0'
SUPPORTED_LEVELS=('moderate','hard')
x=s.Symbol('x',real=True);t=s.Symbol('t',real=True)
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# Every source radio has its own complete bank. No pooled distractor selection.
CASES={
 'q-11973':('moderate',{'a':3,'b':3,'c':5}),
 'q-2396':('moderate',{'a':7,'b':-2,'c':4}),
 'q-11978':('moderate',{'a':1}),
 'q-2403':('moderate',{'a':2}),
 'q-313362':('moderate',{'a':1,'b':3,'c':5}),
 'q-313365':('moderate',{'a':1,'b':3}),
 'q-344143':('moderate',{'a':3,'b':-2}),
 'q-343546':('moderate',{'a':3,'k':1}),
 'q-343576':('moderate',{'a':3,'b':2,'c':1}),
 'q-132975':('moderate',{'a':2,'b':2,'c':3}),
 'q-313371':('hard',{'a':2})}
EXCLUDED={'q-2400':'No answer fields; ungradable source',
 'q-128660':'f is undefined in the standalone prompt; prior-part dependencies unavailable'}
def uid(text):return str(uuid.uuid5(uuid.UUID(KP_UUID),text))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(expr):return s.latex(expr).replace(r'\log',r'\ln')
def same(a,b):
 difference=a-b
 if difference==0:return True
 funcs=difference.atoms(s.sin,s.cos,s.tan,s.sec)
 if funcs:
  args=sorted({f.args[0] for f in funcs},key=str);mapping={};circles=[]
  for i,arg in enumerate(args):
   sn,cs=s.symbols('_s'+str(i)+' _c'+str(i));circles.append((sn,cs))
   mapping.update({s.sin(arg):sn,s.cos(arg):cs,s.tan(arg):sn/cs,s.sec(arg):1/cs})
  numerator=s.fraction(s.cancel(difference.xreplace(mapping)))[0]
  for sn,cs in circles:numerator=s.rem(numerator,sn**2+cs**2-1,sn)
  return s.expand(numerator)==0
 return s.cancel(difference)==0 or s.simplify(difference)==0

def objects(name,p):
 a=s.Integer(p['a']);b=s.Integer(p.get('b',0));c=s.Integer(p.get('c',0));k=s.Integer(p.get('k',1))
 z=x;factor=s.Integer(1);den=None;point=None;domain='All real x where the displayed denominator is nonzero.'
 if name=='q-11973':
  u=a*x**2;v=(b*x+c)**2;den=(b*x+c)**3
  bank=[2*a*c*x/den,2*a*x/den,x/(b*x+c)**4,2*x/(b*x+c)**4,c*x/(b*x+c)**4]
 elif name=='q-2396':
  u=s.tan(a*x+b);v=c*x;sec=s.sec(a*x+b)**2
  bank=[(a*x*sec-u)/(c*x**2),(a*sec-u)/(c**2*x**2),(x*sec+u)/(c*x**2),(a*x*sec-u)/(c**2*x**2),(sec-u)/(c*x**2)]
  domain='x != 0 and cos(a*x+b) != 0, with the recorded a and b.'
 elif name=='q-11978':
  u=(x+a)**2;v=x**2+a**2;D=v**2
  bank=[2*a*(a**2-x**2)/D,(a-x)**2/D,2*(x+a)/D,2*(a-x)/D,(a-2*x**2)/D]
 elif name=='q-2403':
  u=s.sqrt(s.log(x));v=a*x;L=s.log(x)
  bank=[(1-2*L)/(2*a*x**2*s.sqrt(L)),(x-a*s.sqrt(L))/(a**2*x**2*L),(1-a*L)/s.sqrt(L),(1+a*s.sqrt(L))/(a*x**2*s.sqrt(L)),(L-a)/s.sqrt(L)]
  domain='x > 1 (derivative of sqrt(ln(x))).'
 elif name=='q-313362':u=a*x**3;v=(b*x+c)**2;den=(b*x+c)**3
 elif name=='q-313365':u=(x+a)**2;v=x+b;den=v**2
 elif name=='q-344143':u=s.exp(a*x**2);v=x+b;den=v**2;factor=u
 elif name=='q-343546':u=s.cos(a*x);v=x;point=k*s.pi/2
 elif name=='q-343576':u=s.exp(a*x);v=x+b;point=c
 elif name=='q-132975':
  z=t;u=a*t;v=(b*t**2+c)**2;domain='t > 0; a,b,c are positive.'
 elif name=='q-313371':u=s.log(x);v=s.exp(a*x);den=x*v;domain='x > 0.'
 else:raise ValueError(name)
 derivative=s.factor((s.diff(u,z)*v-u*s.diff(v,z))/v**2)
 answer=s.factor(derivative*den/factor) if den is not None and name not in ('q-11973',) else derivative
 if point is not None:answer=s.simplify(derivative.subs(z,point))
 if name not in ('q-11973','q-2396','q-11978','q-2403'):bank=[answer]
 assert same(bank[0],answer)
 assert all(not same(vv,ww) for n,vv in enumerate(bank) for ww in bank[:n]),'Bank collision'
 return z,u,v,derivative,answer,bank,den,factor,point,domain

def validate_parameters(name,p):
 assert set(p)==set(CASES[name][1]);assert all(type(v) is int for v in p.values())
 assert 1<=p['a']<=9
 if 'b' in p:assert -5<=p['b']<=5
 if 'c' in p:assert 1<=p['c']<=7
 if name in ('q-11973','q-313362','q-132975'):assert p['b']>0 and p['c']>0
 if name=='q-343546':assert p['a']%2==1 and p['k'] in (1,3,5)
 if name=='q-343576':assert p['b']+p['c']!=0 and p['a']*p['c']<=12,'Evaluation exponential outside validated grading bound'

def generate(level,seed=0,template=None,parameters=None,profile=None):
 assert level in SUPPORTED_LEVELS,'Unsupported level: '+level
 rng=random.Random(seed);name=template or rng.choice([n for n,(l,p) in CASES.items() if l==level])
 assert CASES[name][0]==level and profile in (None,name)
 p=parameters if parameters is not None else sample(name,rng);validate_parameters(name,p)
 z,u,v,d,ans,bank,den,factor,point,domain=objects(name,p)
 src=SOURCES[name];sf=src[':question/answer-fields'][0];ft=sf[':answer-field/type'][':db/ident'];key=sf[':answer-field/key']
 function=r'\frac{'+tex(u)+'}{'+tex(v)+'}';target=r'\frac{\text{d}y}{\text{d}x}'
 if name=='q-343546':
  target=r"f'(x)"
  problem=rf'Find the slope $m$ of the tangent line to the curve $f(x)={function}$ at $x={tex(point)}.$'+'\n\n$m=$\n{{field-1}}'
 elif name=='q-343576':
  problem=rf'If $y={function},$ find ${{y}}^{{\prime}}({tex(point)}).$'+'\n\n'+rf'${{y}}^{{\prime}}({tex(point)})=$'+'\n{{field-1}}'
 elif name=='q-132975':
  # Explicit standalone repair, recovered from the retained solution.
  problem=rf'Given that $x(t)={function},\,t>0,$ find ${{x}}^{{\prime}}(t).$'+'\n\n'+r'${x}^{\prime}(t)=\,$'+'\n{{field-1}}';target=r'{x}^{\prime}(t)'
 else:
  if name in ('q-2396','q-2403','q-344143','q-313371'):problem=rf'Find ${{y}}^{{\prime}}$ for $y={function}.$'
  else:problem=rf'Given that $y={function},$ find ${target}.$'
  if ft.endswith('/blank'):
   if name=='q-313371':target=r'{y}^{\prime}'
   cell='{{field-1}}' if factor==1 else '$(${{field-1}}$)'+tex(factor)+'$'
   problem+='\n\n| $'+target+'$ | $=$ | '+cell+' |\n| --- | --- | --- |\n|  |  | $'+tex(den)+'$ |'
 # Preserve authored mathematical stages and shared instructional sentences.
 chain='v' if name in ('q-11973','q-313362','q-132975','q-313371') else 'u'
 solution=rf'We use the quotient rule with the numerator $u({z})={tex(u)}$ and the denominator $v({z})={tex(v)}.$ '+'\n\n'+rf'Differentiating $u({z})$ and $v({z}),$ we have'+'\n\n$$\n'+rf"u'({z})={tex(s.diff(u,z))},\quad v'({z})={tex(s.diff(v,z))}."+'\n$$\n\n'+rf'Note that we used the chain rule to differentiate ${chain}.$'+'\n\nNow, applying the quotient rule and simplifying, we have\n\n$$\n'+rf"\begin{{aligned}}{target} & =\frac{{u'({z})v({z})-u({z})v'({z})}}{{[v({z})]^2}} \\ & =\frac{{({tex(s.diff(u,z))})({tex(v)})-({tex(u)})({tex(s.diff(v,z))})}}{{({tex(v)})^2}} \\ & ={tex(d)}.\end{{aligned}}"+'\n$$'
 if point is not None:
  evaluation_label='m' if name=='q-343546' else rf"y'({tex(point)})"
  solution+='\n\n'+rf'Therefore, the value at $x={tex(point)}$ is'+'\n\n$$\n'+rf"\begin{{aligned}}{evaluation_label} & ={tex(d.subs(x,point))} \\ & ={tex(ans)}.\end{{aligned}}"+'\n$$'
 # Exact source prose is replayed only at unchanged params. Mathematical
 # equivalence of every answer and solution is independently checked.
 at_source=p==CASES[name][1]
 if at_source:
  if name!='q-132975':problem=src[':question/problem']
  solution=src[':question/worked-solution']
 fp=digest([s.srepr(s.cancel(u/v)),str(z),s.srepr(point) if point is not None else None,'fragment' if den is not None and ft.endswith('/blank') else 'complete'])
 # Bank parameters participate in content identity, but novelty counts task fp.
 qid=uid('question:'+VERSION+':'+fp+':'+name+':'+digest(sorted(s.srepr(s.cancel(value)) for value in bank)))
 fid=uid(qid+':field:'+key);choices=[]
 for n,value in enumerate(bank):
  val=tex(value);choices.append({':answer/id':uid(fid+':answer:'+s.srepr(value)),':answer/type':sf[':answer-field/choices'][0][':answer/type'][':db/ident'],':answer/value':val})
 correct=choices[0][':answer/id'];random.Random(seed).shuffle(choices)
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/correct':[':answer/id',correct],':answer-field/choices':choices}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':name,'bank_profile':name if ft.endswith('/radio') else None,'parameters':p,'parameter_fingerprint':fp,'source_refs':[name], 'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'domain':domain,'dependencies':{'sympy':s.__version__},'sampling_policy':'bounded source-family parameter extensions','standalone_repair':name=='q-132975','plots':[]}}

def sample(name,rng):
 p={k:rng.randint(1,7) for k in CASES[name][1]}
 if name=='q-313371':p['a']=rng.randint(1,9)
 if 'b' in p:p['b']=rng.choice([-5,-3,-2,-1,0,1,2,3,5])
 if name in ('q-11973','q-313362','q-132975'):p['b']=rng.randint(1,5)
 if name=='q-343576':p['c']=rng.randint(1,min(7,12//p['a']))
 if name=='q-343546':p['a']=rng.choice([1,3,5,7,9]);p['k']=rng.choice([1,3,5])
 return p

def batch(level,count,seed=0,template=None):
 assert level in SUPPORTED_LEVELS;assert 0<=count<=1000
 rng=random.Random(seed);out=[];seen=set();names=[n for n,(l,p) in CASES.items() if l==level]
 for attempt in range(max(100,count*100)):
  if len(out)==count:break
  name=template or names[attempt%len(names)]
  try:r=generate(level,rng.getrandbits(32),name)
  except AssertionError:continue
  fp=r['generation']['parameter_fingerprint']
  if fp in seen:continue
  seen.add(fp);out.append(r)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--output',type=Path);a=ap.parse_args()
 out=batch(a.difficulty,a.count,a.seed,a.template);text=json.dumps(out,indent=2) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in out)
 if a.output:a.output.write_text(text+'\n')
 else:print(text)
if __name__=='__main__':main()
