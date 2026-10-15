"""Source-backed gradient reconstruction; easy only, bounded nonzero field scaling.
Run --level easy --template q-35994 --seed 1 --count 5 [--output FILE].
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,random,sys,uuid
import sympy as s
KP=17592186124569
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2]
SOURCE=json.loads((HERE/'reference/initial/source.json').read_text())
KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
sp=importlib.util.spec_from_file_location('gradient_scalar',HERE/'display_parser.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
x,y=p.x,p.y
SCALES=(-4,-3,-2,-1,1,2,3,4);VERSION='gradient-scale-1'
# Each formula is independently matched to every original source option in validation.
# P and Q are transcribed from the given field, not derived from its keyed answer.
CASES={
 'q-35994':('-y','3-x','-x*y','3*y',['-x*y-y','3-x*y','-x*y+2*x','-x*y+3*y','y*x**2/2']),
 'q-168602':('y**3-1','3*x*y**2+1','x*y**3-x','y',['x*y**3-x+y']),
 'q-132077':('cos(x+y)+y','cos(x+y)+x','sin(x+y)+x*y','0',['sin(x+y)+x**2*y/2','sin(x+y)+x*y','sin(x+y)+y**2','sin(x+y)+x+y','sin(x+y)+x**2/2+y**2/2']),
 'q-132079':('exp(y)-y*sin(x)','x*exp(y)+cos(x)','x*exp(y)+y*cos(x)','0',['x**2*exp(y)+y*cos(x)','x*exp(y)+y*sin(x)','y*exp(y)+x*cos(x)','y**2*exp(y)+x*cos(x)','x*exp(y)+y*cos(x)']),
 'q-132080':('exp(y)','x*exp(y)+2*y','x*exp(y)','y**2',['2*y*exp(y)+x**2','x*exp(y)+y**2','x*exp(y)+y','y*exp(y)+x*y**2','x**2*exp(y)+y']),
 'q-81734':('2*x*y**2+1','2*x**2*y+1','x**2*y**2+x','y',['2*x**2*y**2','x**2*y**2+y','2*x**2*y**2+x','x**2*y**2+x+y','4*x*y+x*y']),
 'q-81737':('12*x**3-1/y','(x-1)/y**2','3*x**4-x/y','1/y',['12*x**3-1/y','3*x**4-1/y','12*x**4+x**2/y-x/y','3*x**4-x/y+1/y','12*x**3*y-x/y']),
 'q-81748':('cos(x)*sin(y)','sin(x)*cos(y)+sin(y)','sin(x)*sin(y)','-cos(y)',['sin(x)*cos(y)+sin(y)','sin(x)**2+cos(y)','sin(x)*sin(y)-cos(y)','sin(x*y)+sin(y)','cos(x)*cos(y)-cos(y)']),
 'q-81749':('y*exp(x*y)','x*exp(x*y)+2*y','exp(x*y)','y**2',['y*exp(x*y)+x**2','x*y*exp(x*y)+y','x*exp(x*y)+2','exp(x*y)+y**2','exp(x*y)+x*y']),
 'q-132084':('2*x*sin(y)','x**2*cos(y)+3*y**2','x**2*sin(y)','y**3',['x**2*sin(y)+y**3','x**2*cos(y)+3*y','x**2*cos(y)+2*y','x*sin(y)+y**3','x*sin(y)+y**2']),
 'q-81736':('sin(y)+y','x*cos(y)+x','x*sin(y)+x*y','0',['x*sin(y)+x*y','cos(x*y)+x*y','x**2*sin(y)+x**2*y','x*cos(y)+x','sin(x*y)+y']),
 'q-81738':('3*x**2-y**2','4-2*x*y','x**3-x*y**2','4*y',['x**3-x*y**2+4*y','x**3-y**3+4*y-x*y**2','3*x**3+4*y-x*y**2','3*x**2*y-y**3+4*y-x*y**2','3*x**2*y-y**3+4*y'])}
EXCLUDED={'q-37346':'Unrated; no correct reference or worked solution. No authoring inferred for this incomplete source.', 'q-37343':'Two choices have the same gradient: x^2 y+y^3+C and x^2 y+y^3. The prompt only requires a potential, so the bank is ambiguous.'}
def expr(v):return s.sympify(v,locals={'x':x,'y':y})
def tex(v):return s.latex(s.expand(v),mul_symbol=None)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def data(template,k):
 raw=CASES[template];P,Q,A,H=map(expr,raw[:4]);bank=list(map(expr,raw[4]));return [s.expand(k*v) for v in (P,Q,A,H)], [s.expand(k*v) for v in bank]
def generate(level='easy',seed=0,template=None,parameters=None,profile=None):
 if level!='easy':raise ValueError('Unsupported difficulty: '+level)
 rng=random.Random(seed);template=template or rng.choice(sorted(CASES));assert template in CASES
 assert profile in (None,template+'-complete-bank')
 k=(parameters or {}).get('scale',rng.choice(SCALES));assert type(k)==int and k in SCALES
 (P,Q,A,H),bank=data(template,k);f=s.expand(A+H);raw=QUESTIONS[template];blank=template=='q-168602'
 # Identity describes mathematical content and complete authored bank, never seed/order.
 identity=digest([VERSION,template,s.srepr(P),s.srepr(Q),sorted(s.srepr(v) for v in bank),'blank' if blank else 'radio'])
 qid=uid('question/'+identity);fid=uid(qid+'/field');correct=next(i for i,b in enumerate(bank) if s.simplify(b-f)==0)
 values=[tex(v) if blank else 'f(x,y)='+tex(v)+'+C' for v in bank]
 choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 prompt='Find $f(x,y)$ such that $∇f=F,$ where $F(x,y)=('+tex(P)+r')\,i+('+tex(Q)+r')\,j.$'
 if template=='q-81737':prompt+=' Work on either half-plane $y>0$ or $y<0$.'
 if blank:prompt+='\n\n$f(x,y)=$ {{field-1}} $+C,$ where $C$ is a constant.'
 sol=(r'The gradient of the function $f(x,y)$ is defined as'+'\n\n$$\n'+r'∇f(x,y)=\frac{∂f}{∂x}\,i+\frac{∂f}{∂y}\,j.'+'\n$$\n\n'+
 'Since $∇f(x,y)=F(x,y),$ the function $f(x,y)$ must satisfy the following system:\n\n$$\n'+r'\frac{∂f}{∂x}='+tex(P)+r',\qquad \frac{∂f}{∂y}='+tex(Q)+'.\n$$\n\n'+
 'First, we integrate $\\frac{∂f}{∂x}$ with respect to $x.$ Note that the solution should contain an arbitrary function of $y:$\n\n$$\n'+r'\begin{aligned}f(x,y)&=\int \frac{∂f}{∂x}\,\text{d}x\\&=\int ('+tex(P)+r')\,\text{d}x\\&='+tex(A)+r'+g(y)\end{aligned}'+'\n$$\n\n'+
 'Now, differentiating the above expression with respect to $y,$ we obtain\n\n$$\n'+r'\frac{∂f}{∂y}='+tex(s.diff(A,y))+r"+g'(y)."+'\n$$\n\n'+
 'Taking $\\frac{∂f}{∂y}='+tex(Q)+'$ into account, we obtain\n\n$$\n'+r'\begin{aligned}'+tex(s.diff(A,y))+r"+g'(y)&="+tex(Q)+r"\\g'(y)&="+tex(s.diff(H,y))+r'\\g(y)&='+tex(H)+r'+C,\end{aligned}'+'\n$$\n\n'+
 'where $C$ is a constant.\n\nFinally, substituting $g(y)='+tex(H)+'+C$ into our expression for $f(x,y),$ we get\n\n$$\n'+'f(x,y)='+tex(f)+'+C.\n$$')
 return {'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'field-1' if blank else 'selection',':answer-field/type':':answer-field.type/blank' if blank else ':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]}]},'generation':{'version':VERSION,'seed':seed,'parameters':{'scale':k},'template':template,'bank_profile':template+'-complete-bank','source_question':raw[':db/id'],'source_basis':SOURCE['basis'],'domain':'y>0 or y<0' if template=='q-81737' else 'R^2','eligible_for_learning':True,'evidence_only':False,'sympy':s.__version__}}
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--level',default='easy');ap.add_argument('--template',choices=sorted(CASES));ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--output',type=Path);a=ap.parse_args();records=[];seen=set()
 for i in range(1000):
  if len(records)>=a.count:break
  r=generate(a.level,a.seed+i,a.template)
  if r['question'][':question/id'] not in seen:records.append(r);seen.add(r['question'][':question/id'])
 if len(records)!=a.count:raise SystemExit('finite-limit: requested count exceeds distinct bounded domain')
 text=json.dumps(records,indent=2,ensure_ascii=False)+'\n'
 if a.output:a.output.write_text(text)
 else:print(text,end='')
