#!/usr/bin/env python3
"""Isolated quotient-identity draft. The registered implementation is never imported."""
import argparse,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
H=Path(__file__).with_suffix('');KP=17592186064226
SOURCE=json.loads((H/'source.json').read_text());K=SOURCE['record'];KP_UUID=K[':knowledge-point/id'];VERSION='2.0.0-draft'
sys.path.insert(0,str(H));import math_format as fmt;import parser as p
SOURCES={q[':question/math-academy-id']:q for q in K[':knowledge-point/questions']}
SCALES=(-5,-4,-3,-2,-1,1,2,3,4,5,6,8)
HARD_COEFFICIENTS=(-4,-3,-2,-1,1,2,3,4)
ENDPOINTS=((1,6,1,4),(1,6,1,3),(1,4,1,3))
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'quotient-identity-isolated-draft'))
def strict(v,n):
 if type(v) is not int:raise ValueError(n+' must be a built-in integer')
def level(t):return SOURCES[t][':question/difficulty'][':db/ident'].split('/')[-1]
def tex(z):return sp.latex(z)
def operator_notation(text):
 return re.sub(r'(?<![A-Za-z])\{(sin|cos|tan|sec|cot|csc)\}',lambda m:'\\'+m[1]+' ',text)
def fix(s,t):
 # Captured malformed nested aligned environments are redundant wrappers.
 s=s.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
 if t=='q-73361':s=s.replace(r'\\  & (',r'\\  & =(')
 return fmt.normalize_prose(operator_notation(s))
def scaled(term,a):
 if a==1:return term
 term=term.strip().rstrip('.,');hasC=term.endswith('+C')
 if hasC:term=term[:-2]
 return str(a)+r'\left('+term+r'\right)'+('+C' if hasC else '')
def scale_block(block,a):
 if a==1:return block
 # Scale each entire operand, retaining all integral inputs, products and stages.
 b=block.strip();beg=r'\begin{aligned}';end=r'\end{aligned}'
 aligned=beg in b;b=b.replace(beg,'').replace(end,'')
 terms=re.split(r'(\\\\\s*&?\s*=|&\s*=|=)',b)
 for i in range(0,len(terms),2):
  if terms[i].strip():terms[i]=scaled(terms[i],a)
 return (beg if aligned else '')+''.join(terms)+(end if aligned else '')
def source_render(t,a):
 q=SOURCES[t];problem=fix(q[':question/problem'],t);solution=fix(q[':question/worked-solution'],t)
 if a!=1:
  # Keep the original quotient and answer fragment; only the external scalar varies.
  problem=re.sub(r'\$([^$]+)\$',lambda m:'$'+scaled(m[1].rstrip('.='),a)+('=$' if m[1].endswith('=') else '.$'),problem,count=1)
  solution=re.sub(r'\$\$([\s\S]*?)\$\$',lambda m:'$$\n'+scale_block(m[1],a)+'\n$$',solution)
 if t in ['q-352858','q-352867']:
  solution+='\n\nThe original quotient is undefined at $x=0$. This is an improper integral; the simplified integrand has a finite right limit there.'
 return fmt.normalize_prose(problem),fmt.normalize_prose(solution)
def hard_render(t,slots):
 a=sp.Integer(slots['a']);b=sp.Integer(slots['b']);lo,hi=[sp.pi*sp.Rational(*z) for z in (slots['lower'],slots['upper'])]
 x=p.x;s,c=sp.sin(x),sp.cos(x)
 if t=='authored-h-cos-cot':
  num=a*c**3+b*sp.cot(x)**2;den=c**2;stages=[num/den,(a*c**3+b*c**2/s**2)/c**2,a*c+b/s**2,a*c+b*sp.csc(x)**2];anti=a*sp.sin(x)-b*sp.cot(x);identity=r'\cot^2x=\frac{\cos^2x}{\sin^2x}'
 else:
  num=a*sp.tan(x)**2-b*s**3;den=s**2;stages=[num/den,(a*s**2/c**2-b*s**3)/s**2,a/c**2-b*s,a*sp.sec(x)**2-b*s];anti=a*sp.tan(x)+b*sp.cos(x);identity=r'\tan^2x=\frac{\sin^2x}{\cos^2x}'
 I=lambda z:r'\int_{'+tex(lo)+'}^{'+tex(hi)+'} '+tex(z)+r'\,\text{d}x'
 # Use unevaluated source-shaped numerator/denominator in first stage.
 first=r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'} \frac{'+tex(num)+'}{'+tex(den)+r'}\,\text{d}x'
 upper=sp.simplify(anti.subs(x,hi));lower=sp.simplify(anti.subs(x,lo));answer=sp.simplify(upper-lower)
 terms=[first]+[I(z)for z in stages[1:]]+[r'\left('+tex(anti)+r'\right)|_{'+tex(lo)+'}^{'+tex(hi)+'}',r'\left('+tex(upper)+r'\right)-\left('+tex(lower)+r'\right)',tex(answer)]
 solution='We use the identity $'+identity+'$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,\n\n$$\n'+r'\begin{aligned}'+terms[0]+' &='+r' \\ &='.join(terms[1:])+r'\end{aligned}'+'\n$$'
 return 'Evaluate the following integral. Do not round the answer.\n\n$'+first+'=$\n{{field-1}}',solution,[tex(answer)],0

def domains(t):
 if t in ['q-49273','q-49275','q-114313','q-114308','authored-h-cos-cot','authored-h-tan-sin']:return 'Original quotient requires sin(x) != 0 and cos(x) != 0; choose each connected real component separately.'
 if t in ['q-74281','q-73365','q-352848']:return 'Original denominator cos(x)^2-sin(x)^2 != 0, with cot or tan defined; cancelled zeros remain excluded.'
 if t in ['q-74279','q-114318']:return 'sin(n*x) != 0 (n=4 for q-74279 and 1 otherwise).'
 if t in ['q-352858','q-352867','q-73357']:return 'sin(n*x) != 0 in the original quotient. A zero lower endpoint is an improper integral with the finite right limit after cancellation.'
 return 'Original quotient requires cos(n*x) != 0. Definite intervals do not cross a pole.'
@fmt.checked_math_content
def generate(difficulty,seed=0,template=None,parameters=None):
 strict(seed,'seed')
 if difficulty not in ['easy','moderate','hard']:raise ValueError('invalid difficulty')
 rng=random.Random(seed);ts=[t for t in SOURCES if level(t)==difficulty] if difficulty!='hard' else ['authored-h-cos-cot','authored-h-tan-sin']
 t=rng.choice(ts) if template is None else template
 if t not in ts:raise ValueError('template/difficulty mismatch')
 if difficulty=='hard':
  if parameters is None:
   ends=rng.choice(ENDPOINTS);slots={'a':rng.choice(HARD_COEFFICIENTS),'b':rng.choice(HARD_COEFFICIENTS),'lower':list(ends[:2]),'upper':list(ends[2:])}
  else:slots=dict(parameters)
  if set(slots)!={'a','b','lower','upper'}:raise ValueError('expected a,b,lower,upper slots')
  if any(type(slots[z])is not list or len(slots[z])!=2 for z in ['lower','upper']):raise ValueError('endpoints must be two-integer lists')
  for k in ['a','b']:strict(slots[k],k)
  for k in ['lower','upper']:
   for z in slots[k]:strict(z,k)
  if slots['a'] not in HARD_COEFFICIENTS or slots['b'] not in HARD_COEFFICIENTS or tuple(slots['lower']+slots['upper']) not in ENDPOINTS:raise ValueError('outside declared slots')
  problem,solution,values,ci=hard_render(t,slots);ft='blank';key='field-1';sourceids=[]
 else:
  slots={'scale':rng.choice(SCALES)} if parameters is None else dict(parameters)
  strict(slots['scale'],'scale');a=slots['scale']
  if set(slots)!={'scale'} or a not in SCALES:raise ValueError('outside declared slots')
  q=SOURCES[t];f=q[':question/answer-fields'][0];ft=f[':answer-field/type'][':db/ident'].split('/')[-1];key=f[':answer-field/key'];problem,solution=source_render(t,a)
  values=[fmt.normalize_tex(z[':answer/value']) if a==1 else tex(sp.expand(a*(p.scalar(z[':answer/value'])-p.C)+p.C)) if '+C' in z[':answer/value'] else tex(sp.simplify(a*p.scalar(z[':answer/value']))) for z in f[':answer-field/choices']]
  if t=='q-74279':
   # The captured +csc²/2 differs from cot²/2 only by a constant; they
   # represent one primitive error. Keep the raw bank in source evidence and
   # serve a labeled sign-error repair for the duplicate fourth distractor.
   values[3]=tex(-a*sp.csc(4*p.x)**2/2+p.C)
  values=[operator_notation(v)for v in values]
  ci=[z[':answer/id']for z in f[':answer-field/choices']].index(f[':answer-field/correct'][':answer/id']);sourceids=[q[':db/id']]
 if ft=='blank' and '{{'+key+'}}' not in problem:problem+='\n\n{{'+key+'}}'
 expr,lo,hi=p.integral(problem);mathkey=str((sp.sstr(canonical(expr)),str(lo),str(hi)))
 qid=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),mathkey+':'+t));fid=str(uuid.uuid5(uuid.UUID(qid),key));choices=[]
 for v in values:
  v=fmt.normalize_tex(v);choices.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v})
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 return fmt.validate_generated_record({'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':K[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_ID,'version':VERSION,'seed':seed,'template':t,'profile':t,'parameters':slots,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_question_ids':sourceids,'source':'basis-2275-frozen-snapshot','eligibility':'normal-public','source_bank_repair':t=='q-74279','source_presentation_normalization':'legacy bare trig names to proper operators','authored_extension':difficulty=='hard','mathematical_key':mathkey,'domain':domains(t),'dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'plots':[]}})

def canonical(expr):
 return sp.cancel(expr.xreplace({z:{sp.tan:sp.sin(z.args[0])/sp.cos(z.args[0]),sp.cot:sp.cos(z.args[0])/sp.sin(z.args[0]),sp.sec:1/sp.cos(z.args[0]),sp.csc:1/sp.sin(z.args[0])}[z.func]for z in expr.atoms(sp.tan,sp.cot,sp.sec,sp.csc)}))

def batch(difficulty,count=1,seed=0):
 strict(count,'count');strict(seed,'seed')
 if count<=0:raise ValueError('count must be positive')
 levels=['easy','moderate','hard']if difficulty=='all'else[difficulty]
 if any(l not in ['easy','moderate','hard']for l in levels):raise ValueError('difficulty')
 # Conservative capacity guard before enumeration or sampling.
 cap={'easy':72,'moderate':141,'hard':384}
 if any(count>cap[l]for l in levels):raise ValueError('requested count exceeds bounded mathematical task capacity')
 rows=[]
 for l in levels:
  seen=set();r=random.Random(seed);out=[]
  for i in range(20000):
   v=generate(l,r.randrange(2**31));k=v['generation']['mathematical_key']
   if k in seen:continue
   seen.add(k);out.append(v)
   if len(out)==count:break
  if len(out)!=count:raise ValueError('bounded task supply exhausted')
  rows+=out
 return rows
def markdown(record):
 q=record['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='Field '+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+')\n\n'
  for a in f[':answer-field/choices']:out+='- $'+a[':answer/value']+'$'+(' (correct)'if a[':answer/id']==f[':answer-field/correct'][1]else'')+'\n'
 return out+'\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='all',choices=['easy','moderate','hard','all']);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args()
 try:records=batch(a.difficulty,a.count,a.seed)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(records,indent=2)if a.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records))
