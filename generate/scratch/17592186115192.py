#!/usr/bin/env python3
"""Secant differentiation, frozen source basis2275; local review only.

Complete historical banks are parameterized together. Raw observed profiles retain
missing fields, keys and solutions and are explicitly ineligible evidence. Normal
profiles minimally complete missing assessments and use method-derived banks for
the two historically opaque banks. All eleven source presentation/solution
families are sampled, with no chain-rule or higher-derivative extension.
"""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,itertools,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('')
def frozen(name):
 s=importlib.util.spec_from_file_location('secant_private_'+name,HERE/'reference'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
FMT=frozen('math_format'); PARSER=frozen('math_parser')
X=PARSER.X
KP_ID=17592186115192
VERSION='secant-frozen-v1'
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['record'];TITLE=KP[':knowledge-point/title'];KP_UUID=KP[':knowledge-point/id']
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
LEVELS={'q-1892':'easy','q-31280':'easy',**{sid:q[':question/difficulty'][':db/ident'].split('/')[-1] for sid,q in QS.items() if ':question/difficulty' in q}}
ANCHORS={'q-1892':{'a':2},'q-31280':{'a':3},'q-1883':{'a':3},'q-1938':{'a':4},'q-337182':{'a':3,'b':5},'q-104325':{'a':3},'q-105314':{'a':5},'q-105316':{'a':3},'q-340608':{'a':2,'b':4},'q-340611':{'a':'e'},'q-340620':{'a':4,'b':1}}
TEMPLATES={sid:{'level':LEVELS[sid],'source_id':sid,'origin':'observed' if ':question/difficulty' in q else 'authored easy assignment for unrated original'} for sid,q in QS.items()}
OPAQUE={'q-104325','q-105316'}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def tex(v):return sp.latex(v).replace(r'\log',r'\ln')
def eq(a,b):
 diff=sp.expand(a-b)
 if diff==0:return True
 # Exact safe-point counterexample can reject unequal banks before expensive
 # global trig simplification; equality still requires symbolic proof.
 for point in (sp.pi/4,sp.Integer(0)):
  val=sp.simplify(diff.subs(X,point))
  if not val.has(sp.zoo,sp.nan,sp.oo) and val.is_zero is False:return False
 return sp.simplify(sp.trigsimp(diff))==0

def domain(sid):
 # Same finite domain used for explicit validation and random sampling.
 if sid=='q-340611':return [{'a':v} for v in ['e',2,3,4,5,6,7,8,9]]
 if sid in ('q-337182','q-340608','q-340620'):
  return [{'a':a,'b':b} for a in range(1,7) for b in range(1 if sid=='q-340620' else 2,7)]
 return [{'a':a} for a in range(2,10)]

def parameters_checked(sid,p):
 if not isinstance(p,dict) or set(p)!=set(ANCHORS[sid]):raise ValueError('Exact parameter keys required')
 for k,v in p.items():
  if sid=='q-340611' and k=='a' and type(v) is str and v=='e':continue
  if type(v) is not int:raise ValueError('Parameters require builtin int, excluding bool')
 if p not in domain(sid):raise ValueError('Outside documented finite workload domain')
 return dict(p)

def numbers(raw,mapping):
 """Numeric slots are whole number tokens inside math only; powers stay fixed.

 Source powers encode the operation backbone, never coefficient slots. The
 source's field identifiers and prose are not visited by this numeric masker.
 """
 def sub(m):
  before=raw[:m.start()]
  if re.search(r'\^\{?-?$',before):return m[0]
  return str(mapping.get(int(m[0]),int(m[0])))
 return re.sub(r'\d+',sub,raw)
def math_slots(text,mapping):return re.sub(r'\$\$.*?\$\$|\$[^$]*\$',lambda m:numbers(m[0],mapping),text,flags=re.S)
def replace_many(text,pairs):
 marks={}
 for n,(old,new) in enumerate(sorted(pairs,key=lambda t:-len(t[0]))):
  mark=f'@@SLOT{n}@@';text=text.replace(old,mark);marks[mark]=new
 for mark,new in marks.items():text=text.replace(mark,new)
 return text

def render_source(sid,p):
 q=copy.deepcopy(QS[sid]);a=p['a'];b=p.get('b')
 mapping={}
 if sid=='q-1892':mapping={2:a}
 elif sid in ('q-31280','q-104325','q-105316'):mapping={3:a}
 elif sid=='q-1883':mapping={3:a,6:2*a}
 elif sid=='q-1938':mapping={4:a,16:a*a}
 elif sid=='q-337182':mapping={3:a,5:b,6:2*a,10:2*b,15:a*b,25:b*b,30:2*a*b}
 elif sid=='q-105314':mapping={5:a}
 elif sid=='q-340608':mapping={2:a,4:b}
 elif sid=='q-340620':mapping={4:a}
 for k in (':question/problem',':question/worked-solution'):
  if k in q:q[k]=math_slots(q[k],mapping)
 for f in q.get(':question/answer-fields',[]):
  for ans in f.get(':answer-field/choices',[]):ans[':answer/value']=numbers(ans[':answer/value'],mapping)
  if ':answer-field/correct' in f:f[':answer-field/correct'][':answer/value']=numbers(f[':answer-field/correct'][':answer/value'],mapping)
 if sid=='q-340611':
  base='{e}' if a=='e' else '{'+str(a)+'}'
  log='1' if a=='e' else r'\ln '+str(a)
  for k in (':question/problem',':question/worked-solution'):
   q[k]=q[k].replace('{e}',base)
  q[':question/worked-solution']=q[':question/worked-solution'].replace(' & ='+base+'^{x}sec⁡(x)+',' & ='+base+'^{x}'+('' if a=='e' else log)+ 'sec⁡(x)+').replace('(1+tan⁡(x))','('+log+'+tan⁡(x))')
  for f in q[':question/answer-fields']:
   for ans in f[':answer-field/choices']+[f[':answer-field/correct']]:ans[':answer/value']=ans[':answer/value'].replace('1+',log+'+')
 if sid=='q-340620':
  c='' if b==1 else str(b)
  for k in (':question/problem',':question/worked-solution'):
   q[k]=q[k].replace('{e}^{x}',c+'{e}^{x}').replace('{e}^{0}',c+'{e}^{0}')
  q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\cdot 0+1',r'\cdot 0+'+str(b)).replace(' & =1\\end',' & ='+str(b)+r'\end')
  for f in q[':question/answer-fields']:
   for ans in f[':answer-field/choices']+[f[':answer-field/correct']]:ans[':answer/value']=str(b)
 return q

def expressions(sid,p):
 a=sp.Integer(p['a']) if p['a']!='e' else sp.E;b=sp.Integer(p.get('b',1));s=sp.sec(X);t=sp.tan(X)
 fs={'q-1892':-a*sp.sin(X)+s-3*t+11*X,'q-31280':a*s-a,'q-1883':a/X**2+sp.cos(X)-a*s,'q-1938':s/(a*X),'q-337182':a*s/(b*X**2),'q-104325':a*s/sp.exp(X),'q-105314':a**X*s,'q-105316':a*sp.sin(X)+s,'q-340608':a*s-b**X,'q-340611':a**X*s,'q-340620':a*s+b*sp.exp(X)}
 f=fs[sid];d=sp.diff(f,X)
 target={'q-337182':X*t-2,'q-340608':a*s*t,'q-340611':sp.log(a)+t,'q-340620':b}.get(sid,d)
 return f,d,target

def strip_db(obj):
 if isinstance(obj,dict):
  if set(obj)=={':db/ident'}:return obj[':db/ident']
  return {k:strip_db(v) for k,v in obj.items() if k!=':db/id'}
 if isinstance(obj,list):return [strip_db(v) for v in obj]
 return obj

def authored_solution(sid,p,d):
 a=p['a']
 if sid=='q-31280':return 'We take the derivative of each term and then add them, as follows:\n\n$$\n'+rf'\begin{{aligned}}\frac{{\text{{d}}y}}{{\text{{d}}x}} & =\frac{{\text{{d}}}}{{\text{{d}}x}}({a}\sec x-{a}) \\ & ={a}\sec x\tan x-0 \\ & ={a}\sec x\tan x\end{{aligned}}'+'\n$$'
 return 'We take the derivative of each term and then add them, as follows:\n\n$$\n'+rf'\begin{{aligned}}\frac{{\text{{d}}y}}{{\text{{d}}x}} & =\frac{{\text{{d}}}}{{\text{{d}}x}}(-{a}\sin x+\sec x-3\tan x+11x) \\ & =-{a}\cos x+\sec x\tan x-3\sec^2 x+11\end{{aligned}}'+'\n$$'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if type(level) is not str or level not in ('easy','moderate','hard'):raise ValueError('Invalid level')
 for name,value in [('template',template),('field_type',field_type),('profile',profile)]:
  if value is not None and type(value) is not str:raise ValueError(name+' requires a string')
 if type(seed) is not int:raise ValueError('Seed requires builtin int')
 rng=random.Random(seed)
 if profile and profile.startswith('observed-'):
  selected=profile[len('observed-'):]
  if template is not None and template!=selected:raise ValueError('Profile/template mismatch')
  template=selected
 if template is None:
  candidates=[sid for sid in QS if LEVELS[sid]==level]
  if field_type:candidates=[sid for sid in candidates if normal_kind(sid)==field_type.replace(':answer-field.type/','')]
  if not candidates:raise ValueError('Unsupported field type')
  template=rng.choice(candidates)
 if template not in QS or LEVELS[template]!=level:raise ValueError('Template/level mismatch')
 sid=template
 if profile not in (None,'normal','observed-'+sid):raise ValueError('Unsupported complete bank profile')
 raw=profile=='observed-'+sid
 p=parameters_checked(sid,parameters if parameters is not None else rng.choice(domain(sid)))
 q=strip_db(render_source(sid,p));f,d,target=expressions(sid,p)
 q.pop(':question/math-academy-id',None)
 if not raw:
  q[':question/difficulty']=':question.difficulty/'+level
  if ':question/worked-solution' not in q:q[':question/worked-solution']=authored_solution(sid,p,d)
  if ':question/answer-fields' not in q:
   q[':question/problem']+='\n\n'+r'$\frac{\text{d}y}{\text{d}x}=$'+'\n{{field-1}}'
   q[':question/answer-fields']=[{':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/value':tex(target),':answer/type':':answer.type/math'}]}]
  for fld in q[':question/answer-fields']:
   if sid in OPAQUE:
    a=p['a'];s=sp.sec(X);t=sp.tan(X)
    bank=([d,a*s*(t+1)/sp.exp(X),a*s*t/sp.exp(X),a*s*(t-1)/sp.exp(2*X),-d] if sid=='q-104325' else [d,-a*sp.cos(X)+s*t,a*sp.cos(X)-s*t,-d,a*sp.cos(X)])
    fld[':answer-field/choices']=[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in bank]
   matches=[ans for ans in fld[':answer-field/choices'] if eq(PARSER.expression(ans[':answer/value']),target)]
   if len(matches)!=1:raise ValueError('Complete bank is ambiguous or missing correct answer')
   fld[':answer-field/correct']=matches[0]
   # All ordinary wrongs must also differ from one another.
   vals=[PARSER.expression(ans[':answer/value']) for ans in fld[':answer-field/choices']]
   if any(eq(x,y) for n,x in enumerate(vals) for y in vals[n+1:]):raise ValueError('Whole bank collision')
  q[':question/problem']=FMT.normalize_prose(q[':question/problem'])
  q[':question/worked-solution']=FMT.normalize_prose(q[':question/worked-solution'])
  for fld in q[':question/answer-fields']:
   for ans in fld[':answer-field/choices']:ans[':answer/value']=FMT.normalize_tex(ans[':answer/value'])
 # Content identity includes all displayed content and complete unordered banks.
 identity={k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')}
 identity['level']=q.get(':question/difficulty')
 identity['fields']=[]
 for fld in q.get(':question/answer-fields',[]):
  identity['fields'].append({'key':fld[':answer-field/key'],'type':fld[':answer-field/type'],'values':sorted(a[':answer/value'] for a in fld[':answer-field/choices']),'correct':fld.get(':answer-field/correct',{}).get(':answer/value')})
 content=digest(identity);qid=uid(content)
 q[':question/id']=qid
 for n,fld in enumerate(q.get(':question/answer-fields',[])):
  old_correct=fld.get(':answer-field/correct',{}).get(':answer/value')
  fid=uid(qid+':field:'+str(n));fld[':answer-field/id']=fid
  for ans in fld[':answer-field/choices']:ans[':answer/id']=uid(fid+':'+ans[':answer/value'])
  if old_correct is not None:fld[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in fld[':answer-field/choices'] if a[':answer/value']==old_correct)]
  if fld[':answer-field/type']==':answer-field.type/radio':rng.shuffle(fld[':answer-field/choices'])
 if field_type and normal_kind(sid)!=field_type.replace(':answer-field.type/',''):raise ValueError('Field contract mismatch')
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':sid,'profile':profile or 'normal','parameters':p,'seed':seed,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_id':sid,'evidence_only':raw,'eligible_for_learning':not raw,'bank_origin':'historical evidence' if raw else 'authored method bank' if sid in OPAQUE else 'observed parameterized bank or minimally completed blank','content_sha256':content,'mathematical_fingerprint':digest([sp.srepr(f),0 if sid=='q-340620' else None]),'domain':'Each real connected interval excluding cos(x)=0; also x=0 excluded in reciprocal-power families. Hard endpoint 0 lies in (-pi/2,pi/2).','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
 if not raw:FMT.validate_generated_record(rec)
 return rec

def normal_kind(sid):return 'radio' if sid in ('q-1892','q-31280','q-104325','q-105314','q-105316') else 'blank'
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  s+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 return s+'\n'+q.get(':question/worked-solution','[Source worked solution absent.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['json','markdown'],default='markdown');args=ap.parse_args()
 records=[generate(level,args.seed+n,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for n in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
