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
VERSION='2.0.0-draft';SUPPORTED_LEVELS=('easy','moderate','hard');HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
TITLE=SOURCE['record'][':knowledge-point/title'];SOURCE_BASIS=SOURCE['basis'];LINEAGE=SOURCE['lineage']
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
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

# Draft public API: faithful source masks first; authored repairs/extensions explicit.
import copy,sys,itertools
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose,normalize_tex,validate_generated_record
legacy_generate=generate
ORIGINALS=dict(PROFILES)
PROFILES.update({'q-30990':('easy',{'a':8,'b':3}), 'q-47905':('easy',{'a':1,'b':2})})
LEVEL_TEMPLATES={l:[s for s,(lev,p) in PROFILES.items() if lev==l] for l in SUPPORTED_LEVELS}
LEVEL_TEMPLATES['moderate'].append('authored-point')
LEVEL_TEMPLATES['hard']=['authored-four-term']
NORMAL_PROFILES=('source-pattern','authored-method')
def D(v):
 return sp.expand(sp.diff(v,x).subs(sp.tan(x)**2,sp.sec(x)**2-1))
def tex(v):
 return sp.latex(sp.sympify(v)).replace(r'\sec^{2}{\left(x \right)}',r'\sec^{2}x').replace(r'\tan{\left(x \right)}',r'\tan x').replace(r'\sin{\left(x \right)}',r'\sin x').replace(r'\cos{\left(x \right)}',r'\cos x')
def clean(t):
 # Actual doubled slash before command in five captured bank values; only command tokens.
 return re.sub(r'\\\\(?=(?:frac|sqrt)\b)',r'\\',t)
def normalize(q):
 for k in (':question/problem',':question/worked-solution'):
  if k in q:q[k]=normalize_prose(q[k])
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(clean(a[':answer/value']))
 return q
def raw_source(sid):
 """Exact evidence record including all omissions, source identities, fields and attrs."""
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[sid]),'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':sid,'profile':'observed_raw','source_basis':SOURCE_BASIS,'lineage':LINEAGE,'role':'original MA evidence','eligible':False,'reason':'raw evidence retains omitted attributes and noncanonical captured bank escapes'}}
def source_model(sid,p):
 a=p['a'];b=p.get('b',1);c=p.get('c',4)
 if sid=='q-30990':return a*sp.tan(x)-b*x,None,[ -a*sp.csc(x)**2-b*x,-a*sp.sec(x)**2-b*x,a*sp.sec(x)**2-b,a*sp.csc(x)**2+b,a*sp.csc(x)-b],2
 if sid=='q-47905':return a*sp.tan(x)-b*sp.sin(x),None,[a*sp.sec(x)-b*sp.cos(x),a*sp.sec(x)**2-b*sp.cos(x),a*sp.sec(x)+b*sp.cos(x),a*sp.sec(x)**2+b*sp.cos(x),-a*sp.sec(x)**2+b*sp.cos(x)],1
 f,ans,bank=data(sid,p);point=sp.pi/4 if sid=='q-103081' else sp.pi if sid=='q-17912' else 0 if PROFILES[sid][0]=='moderate' else None
 i=next(i for i,z in enumerate(SOURCES[sid][':question/answer-fields'][0][':answer-field/choices']) if z[':answer/id']==SOURCES[sid][':question/answer-fields'][0][':answer-field/correct'][':answer/id'])
 return f,point,bank,i

def field(q,payload,kind,key='selection',correct=0):
 fid=uid('field:'+q[':question/id']+':'+key)
 choices=[{':answer/id':uid('answer:'+fid+':'+str(i)),':answer/type':':answer.type/math',':answer/value':normalize_tex(tex(v))} for i,v in enumerate(payload)]
 return {':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]}
def final_ids(rec):
 q=rec['question'];finger=digest({k:q[k] for k in (':question/problem',':question/worked-solution',':question/difficulty')})
 vals=[{'type':f[':answer-field/type'],'key':f[':answer-field/key'],'bank':[a[':answer/value'] for a in f[':answer-field/choices']],'correct':next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])} for f in q[':question/answer-fields']]
 q[':question/id']=uid('content:'+VERSION+':'+digest([finger,vals]))
 for f in q[':question/answer-fields']:
  right=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);f[':answer-field/id']=uid('field:'+q[':question/id']+':'+f[':answer-field/key'])
  for i,a in enumerate(f[':answer-field/choices']):a[':answer/id']=uid('answer:'+f[':answer-field/id']+':'+str(i))
  f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][right][':answer/id']]
 validate_generated_record(rec)
 return rec

def authored_solution(fun,point=None,label='f'):
 derivative=D(fun);dt=tex(derivative)
 first=rf"\frac{{\mathrm{{d}}}}{{\mathrm{{d}}x}}\left({tex(fun)}\right)"
 # Explicit sum and constant-factor stage; no new chain/product/quotient operation.
 terms=sp.Add.make_args(sp.expand(fun));formal=[]
 for t in terms:
  k,z=t.as_independent(x,as_Add=False)
  formal.append(tex(k)+r'\frac{\mathrm{d}}{\mathrm{d}x}\left('+tex(z)+r'\right)')
 formal=' + '.join(formal)
 out=rf"We know that $\frac{{\mathrm{{d}}}}{{\mathrm{{d}}x}}(\tan x)=\sec^2 x.$ Applying the sum and constant multiple rules, we have"+'\n\n$$\n'+rf"\begin{{aligned}}{label}'(x)&={first} \\ &= {formal} \\ &= {dt}.\end{{aligned}}"+'\n$$'
 if point is not None:
  ev=derivative.subs(x,point);ans=sp.simplify(ev)
  # unevaluated substitution renderer preserves the actual expression stage.
  displayed=dt.replace('x',r'\left('+tex(point)+r'\right)')
  out+='\n\n'+f'Evaluating at $x={tex(point)},$ we get'+'\n\n$$\n'+rf"\begin{{aligned}}{label}'({tex(point)})&={displayed} \\ &= {tex(ev)} \\ &= {tex(ans)}.\end{{aligned}}"+'\n$$\n\n'+rf'Therefore, the slope is ${tex(ans)}.$'
 return out

def recipe_texts(sid,p):
 """Complete bank recipes preserve observed structure, not offsets from a key."""
 a=p['a'];b=p.get('b',1)
 if sid=='q-30990':return [fr'-{a}\csc^2 x-{b}x',fr'-{a}\sec^2 x-{b}x',fr'{a}\sec^2 x-{b}',fr'{a}\csc^2 x+{b}',fr'{a}\csc x-{b}']
 return [fr'{a}\sec x-{b}\cos x',fr'{a}\sec^2 x-{b}\cos x',fr'{a}\sec x+{b}\cos x',fr'{a}\sec^2 x+{b}\cos x',fr'-{a}\sec^2 x+{b}\cos x']

def source_variant(sid,p,seed):
 fun,point,bank,right=source_model(sid,p)
 if sid in ORIGINALS:
  rec=legacy_generate(PROFILES[sid][0],seed,sid,p);normalize(rec['question'])
 else:
  old=SOURCES[sid];a=p['a'];b=p['b'];q={':question/id':uid('temporary'),':question/difficulty':':question.difficulty/easy',':question/problem':old[':question/problem']}
  if sid=='q-30990':q[':question/problem']=q[':question/problem'].replace(r'8\tan x - 3x',fr'{a}\tan x - {b}x')
  else:q[':question/problem']=q[':question/problem'].replace(r'\tan x - 2\sin x',fr'{coeff(a)}\tan x - {b}\sin x')
  q[':question/worked-solution']=authored_solution(fun)
  q[':question/answer-fields']=[field(q,bank,'radio',correct=right)]
  for choice,value in zip(q[':question/answer-fields'][0][':answer-field/choices'],recipe_texts(sid,p)):choice[':answer/value']=normalize_tex(value)
  rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{}}
 rec['generation'].update({'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':sid,'profile':'source-pattern','parameters':p,'source_question':SOURCES[sid][':question/id'],'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'eligible':True,'role':'parameterized original source template' if sid in ORIGINALS else 'authored repair of unrated source template','math_format':'course-academy-tex-v1','dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'domain':'x>0 and cos(x)!=0' if sid in ('q-341495','q-47983') else 'real x with cos(x)!=0','mathematical_fingerprint':digest([str(sp.expand(fun)),str(point)]),'sampling_policy':'positive integer coefficients 1..6 for complete sources; a 1..8, b 1..6 for q-30990; fixed source evaluation inputs; all mandatory full-bank recipes retained'})
 return final_ids(rec)
POINTS=(sp.Integer(0),sp.pi/4,-sp.pi/4,sp.pi,-sp.pi)
def authored(level,sid,p,seed,kind):
 a,b=p['a'],p['b']
 if level=='hard':
  c,d,n=p['c'],p['d'],p['n'];fun=a*(sp.tan(x)+b*sp.sin(x)-c*sp.cos(x))+d*x**n;der=D(fun);point=None
  # Four complete operation-error choices at the same displayed input.
  bank=[der,a*(sp.sec(x)+b*sp.cos(x)+c*sp.sin(x))+d*n*x**(n-1),a*(sp.sec(x)**2+b*sp.cos(x)-c*sp.sin(x))+d*n*x**(n-1),a*(sp.sec(x)**2+b*sp.cos(x)+c*sp.sin(x))+d*x**(n-1),sp.sec(x)**2+b*sp.cos(x)+c*sp.sin(x)+d*n*x**(n-1)]
  display=fr'{a}(\tan x+{b}\sin x-{c}\cos x)+{d}x^{{{n}}}'
  prompt=rf"Find $f'(x)$ if $f(x)={display}.$"
 else:
  point=POINTS[p['point']];fun=b*x-a*sp.tan(x);der=D(fun);s=sp.sec(point);ans=sp.simplify(der.subs(x,point));bank=[ans,b+a*s**2,sp.Integer(b),b-a*s,-b-a*s**2]
  prompt=rf"The derivative of $y={b}x-{a}\tan x$ when $x={tex(point)}$ is"
 q={':question/id':uid('temporary'),':question/problem':prompt,':question/worked-solution':authored_solution(fun,point,'y' if level=='moderate' else 'f'),':question/difficulty':':question.difficulty/'+level}
 if kind=='blank':q[':question/problem']+='\n\n'+rf"${'y' if level=='moderate' else 'f'}'({tex(point) if point is not None else 'x'})=$"+'\n{{field-1}}';bank=bank[:1]
 if any(sp.simplify((bank[i]-bank[j]).rewrite(sp.cos))==0 for i in range(len(bank)) for j in range(i)):raise ValueError('ambiguous complete bank')
 q[':question/answer-fields']=[field(q,bank,kind,'field-1' if kind=='blank' else 'selection')]
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':sid,'profile':'authored-method','parameters':p,'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'eligible':True,'role':'authored conservative extension','domain':'real x with cos(x)!=0','mathematical_fingerprint':digest([str(sp.expand(fun)),str(point)]),'dependencies':{'sympy':sp.__version__,'python':sys.version.split()[0]},'bank_recipes':['correct','tangent secant-power error','cosine derivative sign error','power multiplier omission','outer constant-distribution omission'] if level=='hard' else ['correct','tangent derivative sign error','omit tangent derivative','omit secant square','negate linear derivative and tangent derivative'],'sampling_policy':'bounded same-method four-term sum for hard; regular familiar unit-circle point slot for moderate'}}
 return final_ids(rec)

def parameters_for(sid):
 if sid=='authored-four-term':return (dict(zip(('a','b','c','d','n'),v)) for v in itertools.product(range(2,5),range(1,4),range(1,4),range(1,4),(2,3,4)))
 if sid=='authored-point':return (dict(zip(('a','b','point'),v)) for v in itertools.product(range(1,7),range(1,7),range(5)))
 return iter(candidates(sid) if sid!='q-30990' else [dict(zip(('a','b'),v)) for v in itertools.product(range(1,9),range(1,7))])
def validate_parameters(sid,p):
 if sid=='authored-four-term':
  bounds={'a':range(2,5),'b':range(1,4),'c':range(1,4),'d':range(1,4),'n':(2,3,4)}
 elif sid=='authored-point':bounds={'a':range(1,7),'b':range(1,7),'point':range(5)}
 else:bounds={k:range(1,9) if sid=='q-30990' and k=='a' else range(1,7) for k in PROFILES[sid][1]}
 if set(p)!=set(bounds) or any(type(p[k]) is not int or p[k] not in bounds[k] for k in bounds):raise ValueError('Parameters outside documented slots/bounds')
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 if profile=='observed_raw':
  if template not in SOURCES:raise ValueError('Raw replay requires original source template')
  if parameters is not None:raise ValueError('Raw evidence is not normal sampling')
  return raw_source(template)
 rng=random.Random(seed);sid=template or rng.choice(LEVEL_TEMPLATES[level])
 if sid not in LEVEL_TEMPLATES[level]:raise ValueError('Template difficulty mismatch')
 required='authored-method' if sid.startswith('authored-') else 'source-pattern'
 if profile is not None and profile!=required:raise ValueError('Profile/template mismatch')
 if sid in PROFILES and field_type is not None and field_type!=SOURCES[sid][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]:raise ValueError('Source field contract fixed')
 kind=field_type or rng.choice(('radio','blank')) if sid.startswith('authored-') else None
 if kind is not None and kind not in ('radio','blank'):raise ValueError('Unsupported authored field contract')
 ps=list(parameters_for(sid));rng.shuffle(ps)
 if parameters is not None:validate_parameters(sid,parameters);ps=[parameters]
 for p in ps:
  try:
   return authored(level,sid,p,seed,kind) if sid.startswith('authored-') else source_variant(sid,p,seed)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('No eligible full-bank instance')
def easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count,seed=0):
 if type(count)is not int or count<1:raise ValueError('Positive count required')
 out=[];seen=set()
 for i in range(10000):
  r=generate(level,seed+i);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('finite-limit')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--profile',choices=(*NORMAL_PROFILES,'observed_raw'));ap.add_argument('--field-type',choices=('radio','blank'));ap.add_argument('--parameters');ap.add_argument('--format',choices=['json','markdown'],default='json');a=ap.parse_args();levels=SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]
 rs=[generate(l,a.seed,a.template,json.loads(a.parameters) if a.parameters else None,a.profile,a.field_type) for l in levels] if a.template or a.parameters or a.profile or a.field_type else [r for l in levels for r in batch(l,a.count,a.seed)]
 print(json.dumps({'instances':rs},indent=2,ensure_ascii=False) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
