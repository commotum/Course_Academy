"""Draft-only sine/cosine sum-rule generator. Exact raw evidence and independent inventory.
No database access. Bounds and source relationships are documented in draft evidence.
"""
import argparse,copy,hashlib,itertools,json,random,re,sys,uuid
from pathlib import Path
try: import sympy as sp
except ImportError:
 import os
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).with_suffix('')
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose,normalize_tex,validate_generated_record
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];KP_ID=17592186059675;KP_UUID=KP[':knowledge-point/id'];VERSION='sine-cosine-sum-draft-3';GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SOURCES={q.get(':question/math-academy-id',str(q[':db/id'])):q for q in KP[':knowledge-point/questions']}
MA_SOURCES={k:q for k,q in SOURCES.items() if ':question/math-academy-id' in q}
INVENTORY={k:q for k,q in SOURCES.items() if ':question/math-academy-id' not in q}
x=sp.Symbol('x',real=True);SUPPORTED_LEVELS=('easy','moderate','hard')
PROFILES={'q-1847':('easy',{'a':4,'b':2}),'q-30991':('easy',{'a':6,'n':2}),'q-341383':('easy',{'a':5,'b':1,'n':4}),'q-47985':('easy',{'a':2,'b':1,'n':2}),'q-1900':('moderate',{'k':1})}
LEVEL_TEMPLATES={'easy':['q-1847','q-30991','q-341383','q-47985','independent-easy'],'moderate':['q-1900','independent-moderate'],'hard':['independent-hard']}
SOURCE_ERRORS={'q-47906':'Unrated; missing correct/solution; two equivalent incorrect choices. Raw-only.', 'q-47908':'Unrated; missing correct/solution. Raw-only; no inferred difficulty.', 'q-167324':'Input h is absent. Raw-only.', 'q-167778':'Input h is absent. Raw-only.', 'q-166071':'Input h is absent. Raw-only.', 'q-1900':'Source f-prime(30) label must be y-prime(pi/6), since input is radians and dependent variable y.'}
def uid(v):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return normalize_tex(sp.latex(sp.sympify(v)))
def source_replay(source_id):
 q=copy.deepcopy(SOURCES[source_id]);return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':source_id,'source_basis':2275,'lineage':SOURCE['lineage'],'mode':'raw-source-replay','evidence_only':True,'eligible_for_learning':False,'normal_eligible':False,'template_supported_for_normal':source_id in PROFILES,'role':'Math Academy original' if source_id in MA_SOURCES else 'independently authored inventory','relationship_to_source_templates':'Prior registered positive amplitude transport of q-1900 or q-47985; exact independent inventory, not Math Academy source evidence.' if source_id in INVENTORY else 'Exact raw original; attributes and omissions preserved.'}}
def domains(template):
 if template=='q-1900':return {'k':range(1,13)}
 if template=='q-1847':return {'a':range(1,7),'b':range(1,7)}
 if template=='q-30991':return {'a':range(1,7),'n':(2,3,4)}
 if template=='q-341383':return {'a':range(1,7),'b':range(1,7),'n':(2,3,4)}
 if template=='q-47985':return {'a':range(1,7),'b':range(1,7),'n':(1,2,3)}
 if template=='independent-easy':return {'a':(-6,-3,-1,1,3,6),'b':(-6,-3,-1,1,3,6),'n':(2,3,4),'trig':('sin','cos')}
 if template=='independent-moderate':return {'a':(-6,-3,-1,1,3,6),'b':(-6,-3,-1,1,3,6),'trig':('sin','cos'),'point':('0','pi/6','pi/3','pi/2','pi','3*pi/2')}
 if template=='independent-hard':return {'a':(-6,-1,1,6),'b':(-6,-1,1,6),'c':(-3,-1,1,3),'d':(-3,-1,1,3),'n':(2,3,4),'m':(1,2,3)}
 raise ValueError('Unknown template')
def candidates(template):
 ds=domains(template)
 for values in itertools.product(*ds.values()):
  p=dict(zip(ds,values))
  if template=='q-1847' and p['a']==p['b']:continue
  if template=='q-30991' and p['a']==1:continue
  if template=='independent-moderate' and ((p['trig']=='cos' and p['point'] in ('0','pi')) or (p['trig']=='sin' and p['point'] in ('pi/2','3*pi/2'))):continue
  yield p

def model(t,p):
 point=None
 if t=='q-1847':
  a,b=p['a'],p['b'];expr=a*sp.cos(x)+b*sp.sin(x);bank=[expr,b*sp.cos(x)+a*sp.sin(x),b*sp.cos(x)-a*sp.sin(x),-expr,a*sp.cos(x)-b*sp.sin(x)]
 elif t=='q-30991':
  a,n=p['a'],p['n'];expr=a*(x**n-sp.cos(x))+5;bank=[a*n*x**(n-1)+a*sp.sin(x),a*x**(n-1)+a*sp.sin(x),a*n*x**(n-1)-a*sp.sin(x),a*n*x**(n-1)-sp.sin(x),a*n*x**(n-1)+sp.sin(x)]
  if a==1:raise ValueError('Bank duplicates when a=1')
 elif t=='q-341383':
  a,b,n=p['a'],p['b'],p['n'];expr=sp.Rational(a,4)*sp.sin(x)+sp.Rational(b,4)*x**n;bank=[sp.diff(expr,x)]
 elif t=='q-47985':
  a,b,n=p['a'],p['b'],p['n'];expr=-a*sp.cos(x)+b*x**(-n);v=b*n;bank=[a*sp.sin(x)-v*x**(-n+1),-a*sp.sin(x)-v*x**(-n-1),a*sp.sin(x)-v*x**(-n-1),-a*sp.sin(x)+v*x**(-n-1),-a*sp.sin(x)-v*x**(-n)]
 elif t=='q-1900':
  k=p['k'];expr=k*(2*x-5*sp.cos(x));point=sp.pi/6;bank=[sp.Rational(11,2)*k,sp.Rational(21,5)*k,-sp.Rational(21,6)*k,sp.Rational(9,2)*k,sp.Rational(9,4)*k]
 elif t=='independent-easy':expr=p['a']*getattr(sp,p['trig'])(x)+p['b']*x**p['n'];bank=[sp.diff(expr,x)]
 elif t=='independent-moderate':expr=p['a']*getattr(sp,p['trig'])(x)+p['b']*x;point=sp.sympify(p['point']);bank=[sp.simplify(sp.diff(expr,x).subs(x,point))]
 else:expr=p['a']*sp.cos(x)+p['b']*sp.sin(x)+p['c']*x**p['n']+p['d']*x**(-p['m']);bank=[sp.diff(expr,x)]
 derivative=sp.diff(expr,x);correct=derivative if point is None else sp.simplify(derivative.subs(x,point));return expr,point,derivative,correct,bank

def source_components(t,p):
 """Full mathematical component masks over untouched normalized source prototypes.
 Prose, punctuation, formula reminders, field fragments and ordered rows are fixed.
 Original and changed parameters always pass through this same rendering path.
 """
 a,b,n=p.get('a'),p.get('b'),p.get('n')
 def xp(e):return 'x' if e==1 else '{x}^{'+str(e)+'}'
 def frac(num,den):return r'\frac{'+str(num)+'}{'+str(den)+'}'
 def scaled(c,power):return ('' if c==1 else tex(c))+power
 if t=='q-1847':
  m={'4cos⁡x+2sin⁡x':f'{a}cos⁡x+{b}sin⁡x','4(-sin⁡x)+2(cos⁡x)':f'{a}(-sin⁡x)+{b}(cos⁡x)','2cos⁡x+4sin⁡x':f'{b}cos⁡x+{a}sin⁡x','2cos⁡x-4sin⁡x':f'{b}cos⁡x-{a}sin⁡x','-4cos⁡x-2sin⁡x':f'-{a}cos⁡x-{b}sin⁡x','4cos⁡x-2sin⁡x':f'{a}cos⁡x-{b}sin⁡x'}
 elif t=='q-30991':
  m={'6({x}^{2}-cos⁡x)+5':f'{a}({xp(n)}-cos⁡x)+5',r'6\cdot 2x+6sin⁡x+0':str(a)+r'\cdot '+str(n)+xp(n-1)+f'+{a}sin⁡x+0','12x+6sin⁡x':f'{a*n}{xp(n-1)}+{a}sin⁡x','6x+6sin⁡x':f'{a}{xp(n-1)}+{a}sin⁡x','12x-6sin⁡x':f'{a*n}{xp(n-1)}-{a}sin⁡x','12x-sin⁡x':f'{a*n}{xp(n-1)}-sin⁡x','12x+sin⁡x':f'{a*n}{xp(n-1)}+sin⁡x'}
 elif t=='q-341383':
  inp=frac(str(a)+'sin⁡x',4)+'+'+frac(scaled(b,xp(n)),4)
  tail=scaled(sp.Rational(b*n,4),xp(n-1))
  m={r'\frac{5sin⁡x}{4}+\frac{{x}^{4}}{4}':inp,r'\frac{5}{4}(cos⁡x)+\frac{1}{4}(4{x}^{3})':frac(a,4)+'(cos⁡x)+'+frac(b,4)+'('+str(n)+xp(n-1)+')',r'\frac{5cos⁡x}{4}+{x}^{3}':frac(str(a)+'cos⁡x',4)+'+'+tail,r'\frac{5\operatorname{cos}x}{4}+{x}^{3}':frac(str(a)+r'\operatorname{cos}x',4)+'+'+tail}
 elif t=='q-47985':
  v=b*n
  m={'-2cos⁡x+{x}^{-2}':f'-{a}cos⁡x+'+scaled(b,xp(-n)),'-2(-sin⁡x)+(-2){x}^{-2-1}':f'-{a}(-sin⁡x)+(-{v})'+'{x}^{-'+str(n)+'-1}','2sin⁡x-2{x}^{-1}':f'{a}sin⁡x-{v}{xp(-n+1)}','-2sin⁡x-2{x}^{-3}':f'-{a}sin⁡x-{v}{xp(-n-1)}','2sin⁡x-2{x}^{-3}':f'{a}sin⁡x-{v}{xp(-n-1)}','-2sin⁡x+2{x}^{-3}':f'-{a}sin⁡x+{v}{xp(-n-1)}','-2sin⁡x-2{x}^{-2}':f'-{a}sin⁡x-{v}{xp(-n)}'}
 elif t=='q-1900':
  k=p['k'];m={'2x-5cos⁡x':f'{2*k}x-{5*k}cos⁡x','2-5(-sin⁡x)':f'{2*k}-{5*k}(-sin⁡x)','2+5sin⁡x':f'{2*k}+{5*k}sin⁡x',r'2+5sin⁡(\frac{\pi }{6})':str(2*k)+'+'+str(5*k)+r'sin⁡(\frac{\pi }{6})',r'2+5(\frac{1}{2})':str(2*k)+'+'+str(5*k)+r'(\frac{1}{2})',r'2+\frac{5}{2}':str(2*k)+'+'+frac(5*k,2),r'\frac{11}{2}':frac(11*k,2),r'\frac{21}{5}':frac(21*k,5),r'-\frac{21}{6}':'-'+frac(21*k,6),r'\frac{9}{2}':frac(9*k,2),r'\frac{9}{4}':frac(9*k,4)}
 else:raise ValueError('Not a source template')
 return m

def source_render(t,p):
 old=SOURCES[t];components=source_components(t,p)
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(components,key=len,reverse=True)))
 def render(text):return pattern.sub(lambda match:components[match[0]],text)
 prompt=normalize_prose(old[':question/problem']);solution=normalize_prose(old[':question/worked-solution'])
 if t=='q-1900':solution=solution.replace('{f}^{′}(30)',r'{y}^{′}(\frac{\pi }{6})').replace('{f}^{′}(x)','{y}^{′}(x)')
 return render(prompt),render(solution),[render(normalize_tex(a[':answer/value'])) for a in old[':question/answer-fields'][0][':answer-field/choices']]

def normal(level,seed,t,p):
 if level not in SUPPORTED_LEVELS or t not in LEVEL_TEMPLATES[level]:raise ValueError('Level/template mismatch')
 if p is None:p=random.Random(seed).choice(list(candidates(t)))
 ds=domains(t)
 if set(p)!=set(ds) or any(p[k] not in ds[k] or type(p[k])!=type(next(iter(ds[k]))) for k in ds):raise ValueError('Outside declared parameter bounds')
 expr,point,d,correct,bank=model(t,p)
 if t=='independent-moderate' and sp.diff(getattr(sp,p['trig'])(x),x).subs(x,point)==0:raise ValueError('Unqueried trig amplitude at this point')
 if any(sp.simplify(a-b)==0 for i,a in enumerate(bank) for b in bank[:i]):raise ValueError('Equivalent bank choices')
 right=[i for i,a in enumerate(bank) if sp.simplify(a-correct)==0]
 if len(right)!=1:raise ValueError('Invalid correct option')
 if t=='q-1847':prompt=r'$\frac{\text{d}}{\text{d}x}('+tex(expr)+')=$'
 elif t=='q-30991':prompt=r'Find $\frac{\text{d}y}{\text{d}x}$ for $y='+str(p['a'])+'(x^{'+str(p['n'])+r'}-\cos x)+5.$'
 elif point is not None:prompt='What is the slope of the tangent line to the curve $y='+tex(expr)+'$ at the point $x='+tex(point)+'$?'
 else:prompt='Find the derivative of $y='+tex(expr)+'.$'
 blank=len(bank)==1;key='field-1' if blank else 'selection'
 if blank:prompt+='\n\n'+(r'$\frac{\text{d}y}{\text{d}x}=$' if point is None else 'Slope:')+'\n{{field-1}}'
 if t in PROFILES:prompt,solution,values=source_render(t,p)
 else:
  parts=sp.Add.make_args(expr);deriv_parts=[sp.diff(v,x) for v in parts]
  solution=r'Use $\frac{\text{d}}{\text{d}x}(\sin x)=\cos x$ and $\frac{\text{d}}{\text{d}x}(\cos x)=-\sin x$, with the sum, constant multiple, and power rules.'+'\n\n$$\n'+r'\begin{aligned}\frac{\text{d}y}{\text{d}x} &= \frac{\text{d}}{\text{d}x}('+tex(expr)+r') \\ &= '+ '+'.join('('+tex(v)+')' for v in deriv_parts)+r' \\ &= '+tex(d)+r'.\end{aligned}'+'\n$$'
  if point is not None:
   trig=getattr(sp,p['trig']);val=sp.sin(point) if p['trig']=='cos' else sp.cos(point);signed=-p['a'] if p['trig']=='cos' else p['a'];solution+='\n\nEvaluating at $x='+tex(point)+',$\n\n$$\n'+r"\begin{aligned}y'("+tex(point)+') &= '+tex(d.subs(x,point,evaluate=False))+r' \\ &= '+str(p['b'])+'+('+str(signed)+')('+tex(val)+r') \\ &= '+tex(correct)+r'.\end{aligned}'+'\n$$\n\nTherefore, the slope is $'+tex(correct)+'.$'
 q={':question/problem':normalize_prose(prompt),':question/worked-solution':normalize_prose(solution),':question/difficulty':':question.difficulty/'+level}
 # Mathematical novelty excludes constants and aliases; banks enter identity separately.
 task=digest([sp.srepr(sp.expand(d)),None if point is None else sp.srepr(point)])
 qid=uid(VERSION+':'+task+':'+digest([q,[tex(v) for v in bank]]));fid=uid(qid+':'+key)
 if t not in PROFILES:values=[tex(v) for v in bank]
 answers=[{':answer/id':uid(fid+':'+str(i)),':answer/type':':answer.type/math',':answer/value':normalize_tex(v)} for i,v in enumerate(values)]
 q[':question/id']=qid;q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank' if blank else ':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[right[0]][':answer/id']]}]
 rel='Same direct differentiation stages and source complete bank; explicit coefficient/power slots.' if t in PROFILES else {'easy':'One sine/cosine term plus a monomial, same sum/constant/power skill as q-341383.', 'moderate':'One sine/cosine term plus linear term, then one familiar-point substitution as q-1900.', 'hard':'Four terms: sine, cosine, positive power and negative power. Combines canonical e-3631 with q-47985; no additional rule. Authored difficulty because no hard MA source exists.'}[level]
 r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':t,'profile':t,'parameters':p,'source_basis':2275,'lineage':SOURCE['lineage'],'mathematical_fingerprint':task,'domain':'real x, radians'+('; x != 0' if t in ('q-47985','independent-hard') else ''),'role':'parameterized source template' if t in PROFILES else 'authored extension','relationship_to_source_templates':rel,'source_question':t if t in PROFILES else None,'dependencies':{'sympy':sp.__version__},'bank_policy':'complete observed profile; q-1900 exact positive transport with unresolved interpretation' if t in PROFILES else 'blank; no invented distractors or feedback'}}
 validate_generated_record(r);return r

def generate(level=None,seed=0,template=None,field_type=None,parameters=None,profile=None,mode='normal',source_id=None):
 if mode not in ('normal','raw-source-replay','source-replay'):raise ValueError('Unsupported mode')
 if field_type not in (None,'blank','radio',':answer-field.type/blank',':answer-field.type/radio'):raise ValueError('Unsupported field_type')
 if profile not in (None,'observed_raw',template):raise ValueError('Unsupported profile')
 if profile=='observed_raw':return source_replay(source_id or template)
 if mode in ('raw-source-replay','source-replay'):return source_replay(source_id or template)
 if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
 eligible=LEVEL_TEMPLATES[level]
 if field_type is not None:
  requested=field_type.rsplit('/',1)[-1];eligible=[t for t in eligible if ('blank' if t in ('q-341383','independent-easy','independent-moderate','independent-hard') else 'radio')==requested]
 if not eligible:raise ValueError('Unsupported field type at this level')
 t=template or random.Random(seed).choice(eligible)
 if t not in eligible:raise ValueError('Template/field type mismatch')
 if parameters is not None:return normal(level,seed,t,parameters)
 rng=random.Random(seed);ps=list(candidates(t));rng.shuffle(ps)
 for p in ps:
  try:return normal(level,seed,t,p)
  except ValueError:continue
 raise ValueError('No valid bounded instance')

def batch(level,count,seed):
 if type(count)is not int or count<1:raise ValueError('Positive count required')
 pool=[(t,p) for t in LEVEL_TEMPLATES.get(level,[]) for p in candidates(t)];random.Random(seed).shuffle(pool);out=[];seen=set()
 for t,p in pool:
  try:r=normal(level,seed,t,p)
  except ValueError:continue
  fp=r['generation']['mathematical_fingerprint']
  if fp in seen:continue
  seen.add(fp);out.append(r)
  if len(out)==count:return out
 raise ValueError('Requested more than finite inventory')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'));parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--mode',default='normal');parser.add_argument('--source-id');a=parser.parse_args();rs=[generate(mode=a.mode,source_id=a.source_id)] if a.source_id else [r for lev in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for r in batch(lev,a.count,a.seed)];print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n'.join(markdown(r) for r in rs))
