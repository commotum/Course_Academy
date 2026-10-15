"""Private basis-2275 chain/product draft. Registered baseline is immutable.

All observed records replay through observed_raw, including exact omissions.
Eight normal families use complete parameterized source components; a missing
unrated polynomial key/solution is completed in an explicitly authored hard band.
No database or registration operations. Whole observed banks are indivisible.
"""
import argparse,copy,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
from functools import lru_cache
import sympy as s
KP_ID=17592186096845
KP_UUID='1c269944-636a-50f2-bfc9-c32a7b2e7ca3'
TITLE='Calculating a Derivative Using the Chain and Product Rules'
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2];VERSION='2.0.0-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
_spec=importlib.util.spec_from_file_location('math_format',ROOT/'scripts/question_capture/math_format.py')
math_format=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(math_format)
SOURCE=json.loads((HERE/'source.json').read_text());BASIS=SOURCE['basis'];LINEAGE=SOURCE['lineage']
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
x=s.Symbol('x',real=True);a=s.Symbol('a',positive=True)
DEFAULTS={'q-343332':{'k':4},'q-343333':{'k':5},'q-343354':{'c':2,'k':6},'q-11824':{'k':9},'q-2392':{'k':3},'q-9942':{'k':5,'b':2},'q-2401':{'c':4},'q-11599':{'k':2,'b':1}}
LEVELS={m:('hard' if m=='q-11599' else SOURCES[m][':question/difficulty'][':db/ident'].split('/')[-1]) for m in DEFAULTS}
RAW_LEVELS={m:q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/'+('hard' if m=='q-11599' else 'moderate')).split('/')[-1] for m,q in SOURCES.items()}
EXCLUSIONS={
 'q-31240':'Unrated slope source lacks key and solution; finite numeric bank is preserved raw only.',
 'q-11602':'No answer fields captured. Field contract cannot be inferred from solution alone; raw only.',
 'q-11603':'No answer fields captured. Field contract cannot be inferred from solution alone; raw only.',
 'q-11939':'No answer fields captured; raw only.',
 'q-16698':'No answer fields captured; raw only.',
 'q-143518':'Acceleration prompt omits supplied velocity and refers to unavailable multipart context; raw only.',
 'q-167572':'Acceleration prompt omits supplied velocity and refers to unavailable multipart context; raw only.',
 'q-313299':'Existing blank has neither choices nor key. Raw preserves omission; no authored field repair in this draft.',
 'q-10009':'Finite numerical slope bank has unresolved distractor mechanisms. Complete raw bank retained; no normal coefficient extension.',
 'q-9944':'Finite zero-slope bank has unresolved distractor mechanisms. Complete raw bank retained; no normal coefficient extension.'}

def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(v):return s.latex(v).replace(r'\log',r'\ln').replace(r'\left','').replace(r'\right','')
def replace_components(text,pairs):
 # Complete masks are built first. Replacement values never re-enter matching.
 out=text
 for i,(old,_) in enumerate(pairs):out=out.replace(old,f'@@COMP{i}@@')
 for i,(_,new) in enumerate(pairs):out=out.replace(f'@@COMP{i}@@',new)
 return out

def component_pairs(m,p):
 k=p.get('k');b=p.get('b');c=p.get('c')
 if m=='q-343332':return [('4x',f'{k}x'),('4\\operatorname{cos}',f'{k}'+r'\operatorname{cos}')]
 if m=='q-343333':return [('5x',f'{k}x'),('5{e}',str(k)+'{e}'),('5\\operatorname{ln}',str(k)+r'\operatorname{ln}')]
 if m=='q-343354':return [('12x+2',f'{c*k}x+{c}'),('12x',f'{c*k}x'),('2x',f'{c}x'),('6x',f'{k}x'),('2,',f'{c},'),('(2)',f'({c})'),('+2)',f'+{c})'),('6{e}',str(k)+'{e}')]
 if m=='q-11824':return [('9x',f'{k}x'),('10',str(k+1)),('9{e}',str(k)+'{e}'),('9(',str(k)+'(')]
 if m=='q-2392':return [('3x',f'{k}x'),('3{a}',str(k)+'{a}'),('3\\operatorname',str(k)+r'\operatorname'),('3{sec}',str(k)+'{sec}')]
 if m=='q-9942':return [('5x+2',f'{k}x{b:+d}' if b else f'{k}x'),('5x\\operatorname',f'{k}x'+r'\operatorname'),('5{x}',str(k)+'{x}'),('5\\operatorname',str(k)+r'\operatorname')]
 if m=='q-2401':return [('x\\operatorname{cos}⁡x+2x\\operatorname{sin}⁡x',('x' if c==4 else f'{c//4}x')+r'\operatorname{cos}⁡x+'+f'{c//2}x'+r'\operatorname{sin}⁡x'),('4{x}^{2}',str(c)+'{x}^{2}'),('8x',f'{2*c}x'),('2{x}^{2}',str(c//2)+'{x}^{2}'),('-x\\sqrt',('-x' if c==4 else f'-{c//4}x')+r'\sqrt')]
 if m=='q-11599':
  phase=f'{k}x^{{2}} + {b}';power2=f'({phase})^{{2}}';power3=f'({phase})^{{3}}'
  return [('2x^{2} + 1',phase),('12x^{4} + x^{2}',f'{6*k}x^{{4}} + '+('x^{2}' if b==1 else f'{b}x^{{2}}')),('12x^{4} + 3x^{2}',f'{6*k}x^{{4}} + {3*b}x^{{2}}'),('18x^{4} + 3x^{2}',f'{9*k}x^{{4}} + {3*b}x^{{2}}'),('3x^{4} + 12x^{2}',f'{3*b}x^{{4}} + {6*k}x^{{2}}')]
 if m in EXCLUSIONS:return []
 raise ValueError(m)

def transform(text,m,p):return replace_components(text,component_pairs(m,p))

@lru_cache(None)
def parameter_domain(m):
 if m in ('q-343332','q-343333','q-11824','q-2392'):return tuple({'k':k} for k in range(2,17))
 if m=='q-343354':return tuple({'k':k,'c':c} for k in range(2,17) for c in range(1,7))
 if m=='q-9942':return tuple({'k':k,'b':b} for k in range(3,17) for b in range(-5,6))
 if m=='q-2401':return tuple({'c':c} for c in (4,8,12,16,20,24))
 if m=='q-11599':return tuple({'k':k,'b':b} for k in range(2,10) for b in range(1,10) if b!=2*k)
 if m in EXCLUSIONS:return ({},)
 raise ValueError(m)

def model(m,p):
 k=p.get('k');b=p.get('b');c=p.get('c')
 if m=='q-343332':u=s.exp(x);v=s.sin(k*x);fragment=s.sin(k*x)+k*s.cos(k*x)
 elif m=='q-343333':u=s.exp(k*x);v=s.log(x);fragment=k*s.log(x)+1/x
 elif m=='q-343354':u=c*x;v=s.exp(k*x);fragment=c*k*x+c
 elif m=='q-11824':u=x+1;v=s.exp(k*x);fragment=None
 elif m=='q-2392':u=s.tan(x);v=a**(k*x);fragment=None
 elif m=='q-9942':u=x**2;v=s.sin(k*x+b);fragment=None
 elif m=='q-2401':u=c*x**2;v=s.sqrt(s.sin(x));fragment=None
 elif m=='q-11599':u=x**3;v=(k*x**2+b)**3;fragment=None
 else:raise ValueError(m)
 correct=s.diff(u*v,x)
 return u,v,correct,fragment if fragment is not None else correct

def bank(m,p):
 # Derive correct answer before every recipe and dependent display component.
 u,v,derivative,answer=model(m,p);k=p.get('k');b=p.get('b');c=p.get('c')
 if m=='q-11824':return [(k*x+1)*v,answer,(x+1)*v,k*x*v,k*(x+1)*v],1
 if m=='q-2392':return [answer,v*(s.sec(x)**2+k*s.tan(x)),v*s.sec(x)**2+k*s.tan(x),k*v*(s.sec(x)**2+s.log(a)*s.tan(x)),k*s.sec(x)**2+k*v*s.tan(x)],0
 if m=='q-9942':return [2*x**2*s.sin(k*x+b)+k*x*s.cos(k*x+b),2*x*s.sin(k*x+b)+x**2*s.cos(k*x+b),2*s.sin(k*x+b)+k*x**2*s.cos(k*x+b),answer,k*x*s.sin(k*x+b)+2*x**2*s.cos(k*x+b)],3
 if m=='q-2401':return [(c*s.Rational(1,4)*x*s.cos(x)+c*s.Rational(1,2)*x*s.sin(x))/s.sin(x),c*s.Rational(1,2)*x**2*s.sin(x)/s.sqrt(s.sin(x))-c*s.Rational(1,4)*x*s.sqrt(s.sin(x)),(c*s.Rational(1,2)*x**2*s.sin(x)-2*c*x*s.sin(x))/s.sqrt(s.sin(x)),answer,-c*s.Rational(1,2)*x**2*s.cos(x)/s.sqrt(s.cos(x))+2*c*x*s.sqrt(s.sin(x))],3
 if m=='q-11599':
  z=k*x**2+b;return [(6*k*x**4+b*x**2)*z**2,(6*k*x**4+3*b*x**2)*z**2,(9*k*x**4+3*b*x**2)*z**3,answer,(3*b*x**4+6*k*x**2)*z**2],3
 return [answer],0

def authored_solution(m,p):
 assert m=='q-11599';k=p['k'];b=p['b'];z=k*x**2+b
 # Only missing worked solution is authored; common observed prose and ordered
 # product stages, followed by exactly the polynomial factoring already in KP.
 return ('This question requires the product rule. Let $u(x)=x^{3}$ and $v(x)=('+tex(z)+')^{3}.$ Then\n\n$$\n'
 +r"u^{′}(x)=3x^{2},\,v^{′}(x)="+str(6*k)+'x('+tex(z)+')^{2}.\n$$\n\nNote that we used the chain rule to differentiate $v.$\n\nNow, applying the product rule and simplifying, we have\n\n$$\n'
 +r'\begin{aligned}\frac{\text{d}y}{\text{d}x} & =u^{′}(x)\cdot v(x)+u(x)\cdot v^{′}(x) \\  & =(3x^{2})(('+tex(z)+')^{3})+(x^{3})('+str(6*k)+'x('+tex(z)+')^{2})'
 +r' \\  & =3x^{2}('+tex(z)+')^{3}+'+str(6*k)+'x^{4}('+tex(z)+')^{2}'
 +r' \\  & =(3x^{2}('+tex(z)+')+'+str(6*k)+'x^{4})('+tex(z)+')^{2}'
 +r' \\  & =('+str(9*k)+'x^{4}+'+str(3*b)+'x^{2})('+tex(z)+r')^{2}.\end{aligned}'+'\n$$')

def domain(m):
 if m=='q-343333':return 'x>0'
 if m=='q-2392':return 'a>0 and cos(x)!=0; identities use arbitrary positive a'
 if m=='q-2401':return 'sin(x)>0; source wrong sqrt(cos(x)) option has its own cos(x)>0 domain'
 return 'real x'

def task_fingerprint(m,p):
 u,v,derivative,answer=model(m,p)
 # Product factorization is a fixed instructional role; canonical mathematical
 # task excludes coefficient labels, seed, answer order and equivalent factoring.
 return digest({'function':s.srepr(s.expand(u*v)),'answer':s.srepr(s.expand(answer)),'response':'factored exponential coefficient fragment' if m in ('q-343332','q-343333','q-343354') else 'full derivative','domain':domain(m)})

def raw_record(m,p,level,seed):
 src=SOURCES[m];q=copy.deepcopy(src)
 for key in (':question/problem',':question/worked-solution'):
  if key in q:q[key]=transform(q[key],m,p)
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q.get(':question/answer-fields',[]):
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for ans in f.get(':answer-field/choices',[]):
   ans[':answer/type']=ans[':answer/type'][':db/ident'];ans[':answer/value']=transform(ans[':answer/value'],m,p)
   if ':answer/feedback' in ans:ans[':answer/feedback']=transform(ans[':answer/feedback'],m,p)
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':m,'parameters':p,'profile':'observed_raw','bank_profile':'observed_raw','source_references':[m],'source_basis':BASIS,'source_lineage':LINEAGE,'evidence_only':True,'eligible_for_learning':False,'raw_only_reason':EXCLUSIONS.get(m,'Exact source evidence; missing source attributes remain missing and raw records are never served.'),'observed_record':copy.deepcopy(src),'plots':'none'}}

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed)
 if profile=='observed_raw':
  if template is None:raise ValueError('Raw requires explicit MA source template')
  m=template
  if m not in SOURCES or level!=RAW_LEVELS[m]:raise ValueError('Raw source/level mismatch')
  p=copy.deepcopy(parameters) if parameters is not None else copy.deepcopy(DEFAULTS.get(m,{}))
  if p not in parameter_domain(m) or any(type(v)!=int for v in p.values()):raise ValueError('Outside raw parameter domain')
  # Raw source may contain malformed legacy commands: preserve all bytes through
  # explicit evidence path; never normalize captured source records.
  return raw_record(m,p,level,seed)
 eligible=[m for m in LEVELS if LEVELS[m]==level and (field_type is None or SOURCES[m][':question/answer-fields'][0][':answer-field/type'][':db/ident'] in (field_type,':answer-field.type/'+field_type))]
 if not eligible:raise ValueError('No supported template for requested level and answer-field contract')
 m=template or rng.choice(eligible)
 if m not in eligible:raise ValueError('Template/level/field contract mismatch or explicit raw-only exclusion')
 ft=SOURCES[m][':question/answer-fields'][0][':answer-field/type'][':db/ident'];key=SOURCES[m][':question/answer-fields'][0][':answer-field/key']
 selected_profile='completed-observed-bank' if m=='q-11599' else 'observed-bank' if ft.endswith('/radio') else 'observed-blank'
 if profile not in (None,'default',selected_profile):raise ValueError('Unknown complete bank profile')
 # The whole profile is chosen before parameter sampling; no pool or offsets.
 p=copy.deepcopy(parameters) if parameters is not None else copy.deepcopy(rng.choice(parameter_domain(m)))
 if p not in parameter_domain(m) or any(type(v)!=int for v in p.values()):raise ValueError('Outside supported parameter bounds')
 mathematical_bank,ci=bank(m,p)
 for i,v in enumerate(mathematical_bank):
  for w in mathematical_bank[i+1:]:
   # Two exact nonzero witnesses suffice to reject equivalence; ambiguous pairs
   # are symbolically checked. Domain witnesses satisfy both source radicals.
   delta=v-w
   if delta==0:raise ValueError('Whole selected bank collision')
   if any(abs(complex(delta.subs({x:w,a:2}).evalf(40)))>1e-25 for w in (s.pi/4,s.pi/6)):continue
   if s.simplify(delta)==0:raise ValueError('Whole selected bank collision')
 src=SOURCES[m];prompt=transform(src[':question/problem'],m,p)
 worked=transform(src[':question/worked-solution'],m,p) if ':question/worked-solution' in src else authored_solution(m,p)
 values=[transform(ans[':answer/value'],m,p) for ans in src[':question/answer-fields'][0][':answer-field/choices']]
 prompt=math_format.normalize_prose(prompt);worked=math_format.normalize_prose(worked);values=[math_format.normalize_tex(t) for t in values]
 fp=task_fingerprint(m,p)
 content=digest({'prompt':prompt,'solution':worked,'fields':[{'key':key,'type':ft,'bank':sorted(values),'correct':values[ci]}],'difficulty':level,'domain':domain(m),'version':VERSION})
 uid=lambda v:str(uuid.uuid5(uuid.UUID(KP_UUID),v));qid=uid(content);fid=uid(qid+'|'+key)
 answers=[{':answer/id':uid(fid+'|'+t),':answer/type':':answer.type/math',':answer/value':t} for t in values];correct=answers[ci][':answer/id']
 if ft.endswith('/radio'):random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return math_format.validate_generated_record({'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':m,'parameters':p,'profile':selected_profile,'bank_profile':selected_profile,'parameter_fingerprint':fp,'mathematical_fingerprint':fp,'content_identity':content,'domains':domain(m),'source_references':[m],'source_basis':BASIS,'source_lineage':LINEAGE,'evidence_only':False,'eligible_for_learning':True,'difficulty_provenance':'Authored hard band from same KP unrated polynomial product; no source hard rating' if m=='q-11599' else 'Observed MA difficulty','authored_repairs':['Missing correct designation derived by differentiating rendered function; missing solution uses KP observed prose and ordered stages'] if m=='q-11599' else [],'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':'none'}})

def batch(level,count,seed=0):
 if count<0:raise ValueError('Count must be nonnegative')
 levels=SUPPORTED_LEVELS if level=='all' else (level,)
 out=[]
 for l in levels:
  pairs=[(m,p) for m in LEVELS if LEVELS[m]==l for p in parameter_domain(m)];random.Random(seed).shuffle(pairs)
  if count>len(pairs):raise ValueError('Finite configured variety exceeded')
  out += [generate(l,seed+i,template=m,parameters=p) for i,(m,p) in enumerate(pairs[:count])]
 return out

def markdown(rec):
 q=rec['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):parts += ['\n'.join(('- '+a[':answer/value']) for a in f.get(':answer-field/choices',[]))]
 if ':question/worked-solution' in q:parts += [q[':question/worked-solution']]
 return '\n\n'.join(parts)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['all',*SUPPORTED_LEVELS],required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
 rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
