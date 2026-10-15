#!/usr/bin/env python3
"""Cotangent differentiation draft; all MA families, source basis2275.

Registered numeric17592186115191.py and its entire evidence/cache tree are
immutable. This draft uses only its own frozen source, formatter/parser and
native-grader fixture. Raw public observed profiles preserve missing fields,
correct refs, difficulty and solutions. Normal completions and method banks
are authored and labeled. No database or registration operations exist here.
"""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).with_suffix('')
def frozen(name):
 spec=importlib.util.spec_from_file_location('cotangent_private_'+name,HERE/'reference'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
FMT=frozen('math_format');PARSER=frozen('math_parser');X=PARSER.X
KP_ID=17592186115191;VERSION='cotangent-all-families-draft-v1'
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];KP_UUID=KP[':knowledge-point/id'];TITLE=KP[':knowledge-point/title']
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' in q}
LEVELS={'q-17639':'easy','q-31279':'easy',**{sid:q[':question/difficulty'][':db/ident'].split('/')[-1] for sid,q in QS.items() if ':question/difficulty' in q}}
ANCHORS={'q-17639':{'a':23},'q-31279':{'a':2},'q-31288':{'a':6},'q-31355':{'a':1},'q-105309':{'a':5},'q-340595':{'a':3},'q-340597':{'a':1},'q-340598':{'a':1},'q-340599':{'a':1},'q-340603':{'a':1},'q-1913':{'a':2}}
TEMPLATES={sid:{'level':LEVELS[sid],'source_id':sid,'origin':'observed' if ':question/difficulty' in q else 'authored easy assignment for unrated MA original'} for sid,q in QS.items()}
OPAQUE={'q-17639','q-1913'}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def tex(v):return sp.latex(v).replace(r'\log',r'\ln')
def eq(a,b):
 diff=sp.expand(a-b)
 if diff==0:return True
 for point in (sp.pi/4,sp.pi/6):
  val=sp.simplify(diff.subs(X,point))
  if not val.has(sp.zoo,sp.nan,sp.oo) and val.is_zero is False:return False
 return sp.simplify(sp.trigsimp(diff.rewrite(sp.sin)))==0

def domain(sid):
 if sid not in QS:raise ValueError('Unknown family')
 vals=range(2,25) if sid=='q-17639' else range(2,10) if sid=='q-105309' else range(1,25) if sid=='q-31288' else range(1,13)
 return [{'a':a} for a in vals]
def checked(sid,p):
 if type(p) is not dict or set(p)!={'a'} or type(p['a']) is not int:raise ValueError('Exactly one builtin integer a required; bool is invalid')
 if p not in domain(sid):raise ValueError('Outside finite documented workload domain')
 return dict(p)
def numbers(raw,mapping):
 def sub(m):
  if re.search(r'\^\{?-?$',raw[:m.start()]):return m[0]
  return str(mapping.get(int(m[0]),int(m[0])))
 return re.sub(r'\d+',sub,raw)
def replace_many(text,pairs):
 marks={}
 for n,(old,new) in enumerate(sorted(pairs,key=lambda t:-len(t[0]))):
  mark=f'@@SLOT{n}@@';text=text.replace(old,mark);marks[mark]=new
 for mark,new in marks.items():text=text.replace(mark,new)
 return text

def math_transform(raw,sid,a):
 c='' if a==1 else str(a)
 if sid in ('q-17639','q-31279','q-105309','q-340595','q-1913'):
  maps={'q-17639':{23:a},'q-31279':{2:a},'q-105309':{5:a},'q-340595':{3:a},'q-1913':{2:a,8:4*a}}
  return numbers(raw,maps[sid])
 if sid=='q-31288':
  # The denominator6 in the evaluation angle is a different complete slot.
  raw=raw.replace(r'\frac{\pi }{6}','@@ANGLE@@')
  return numbers(raw,{6:a,24:4*a}).replace('@@ANGLE@@',r'\frac{\pi }{6}')
 if sid=='q-31355':
  cot=r'\operatorname{cot}x';cs=r'{csc}^{2}x'
  return replace_many(raw,[(r'\frac{-x'+cs+'-2'+cot+r'}{{x}^{3}}',r'\frac{-'+c+'x'+cs+'-'+str(2*a)+cot+r'}{{x}^{3}}'),(r'\frac{(-'+cs+r')\cdot {x}^{2}-'+cot+r'\cdot (2x)}{{x}^{4}}',r'\frac{(-'+c+cs+r')\cdot {x}^{2}-'+c+cot+r'\cdot (2x)}{{x}^{4}}'),(r'\frac{'+cot+r'}{{x}^{2}}',r'\frac{'+c+cot+r'}{{x}^{2}}')])
 if sid=='q-340597':
  log=r'\operatorname{ln}⁡(x)';cot=r'\operatorname{cot}⁡(x)'
  return replace_many(raw,[(log,c+log),(r'\frac{1}{x}',r'\frac{'+str(a)+r'}{x}'),(r'\frac{'+cot+r'}{x}',r'\frac{'+c+cot+r'}{x}'),(r'\frac{\operatorname{cot}(x)}{x}',r'\frac{'+c+r'\operatorname{cot}(x)}{x}')])
 if sid=='q-340598':
  cot=r'\operatorname{cot}⁡(x)';cs=r'{csc}^{2}⁡(x)'
  return replace_many(raw,[('1'+cot+'+x(-'+cs+')',str(a)+cot+'+'+c+'x(-'+cs+')'),(cot+'-x'+cs,c+cot+'-'+c+'x'+cs),('x'+cot,c+'x'+cot),(cot+r'\,-',c+cot+r'\,-'),(r'x{csc}^{2}(x)',c+r'x{csc}^{2}(x)')])
 if sid=='q-340599':
  log='ln⁡(x)';cot='cot⁡(x)'
  return replace_many(raw,[(cot+'+x'+log,c+cot+'+'+c+'x'+log),(r'\frac{'+cot+'+',r'\frac{'+c+cot+'+'),(cot+r'\,+',c+cot+r'\,+'),('x'+log,c+'x'+log),(log,c+log),(r'\frac{1}{x}',r'\frac{'+str(a)+r'}{x}'),(r'x\operatorname{ln}(x)',c+r'x\operatorname{ln}(x)')])
 if sid=='q-340603':
  cot='cot⁡(x)';cs=r'{csc}^{2}⁡(x)'
  return replace_many(raw,[(r'\frac{1('+cot+')-x(-'+cs+')}',r'\frac{'+str(a)+'('+cot+')-'+c+'x(-'+cs+')}'),(r'\frac{'+cot+'+x'+cs+'}',r'\frac{'+c+cot+'+'+c+'x'+cs+'}'),(r'\frac{x}{'+cot+'}',r'\frac{'+c+'x}{'+cot+'}'),(cot+r'\,+',c+cot+r'\,+'),(r'x{csc}^{2}(x)',c+r'x{csc}^{2}(x)')])
 raise ValueError('Unhandled family')

def render_source(sid,p):
 q=copy.deepcopy(QS[sid]);a=p['a']
 for key in (':question/problem',':question/worked-solution'):
  if key in q:q[key]=re.sub(r'\$\$.*?\$\$|\$[^$]*\$',lambda m:math_transform(m[0],sid,a),q[key],flags=re.S)
 for fld in q.get(':question/answer-fields',[]):
  for ans in fld[':answer-field/choices']+[fld[':answer-field/correct']] if ':answer-field/correct' in fld else fld[':answer-field/choices']:
   ans[':answer/value']=math_transform(ans[':answer/value'],sid,a)
 return q

def expressions(sid,p):
 a=sp.Integer(p['a']);cot=sp.cot(X);cs=sp.csc(X)**2
 fs={'q-17639':a*sp.tan(X)-5*X**5-cot,'q-31279':a*X-cot,'q-31288':-a*cot,'q-31355':a*cot/X**2,'q-105309':a**X-cot,'q-340595':sp.exp(X)-a*cot,'q-340597':a*sp.log(X)*cot,'q-340598':a*X*cot,'q-340599':a*sp.log(X)/cot,'q-340603':a*X/cot,'q-1913':-a*X**4*cot}
 f=fs[sid];d=sp.diff(f,X)
 target={'q-31288':4*a,'q-31355':(-a*X*cs-2*a*cot)/X**3,'q-340595':sp.exp(X)+a*cs,'q-340597':a*cot/X,'q-340598':a*X*cs,'q-340599':a*X*sp.log(X),'q-340603':a*X*cs}.get(sid,d)
 return f,d,target

def strip_db(v):
 if isinstance(v,dict):
  if set(v)=={':db/ident'}:return v[':db/ident']
  return {k:strip_db(x) for k,x in v.items() if k!=':db/id'}
 if isinstance(v,list):return [strip_db(x) for x in v]
 return v

def authored_solution(sid,a):
 if sid=='q-17639':body=rf'\begin{{aligned}}f^{{\prime}}(x) & =\frac{{\text{{d}}}}{{\text{{d}}x}}({a}\tan x-5x^{{5}}-\cot x) \\ & ={a}\sec^{{2}}x-5\cdot5x^{{4}}-(-\csc^{{2}}x) \\ & ={a}\sec^{{2}}x-25x^{{4}}+\csc^{{2}}x\end{{aligned}}'
 else:body=rf'\begin{{aligned}}f^{{\prime}}(x) & =\frac{{\text{{d}}}}{{\text{{d}}x}}({a}x-\cot x) \\ & ={a}-(-\csc^{{2}}x) \\ & ={a}+\csc^{{2}}x\end{{aligned}}'
 return 'We take the derivative of each term and then add them, as follows:\n\n$$\n'+body+'\n$$'

def normal_kind(sid):return 'radio' if sid in ('q-17639','q-31279','q-105309','q-1913') else 'blank'
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if type(level) is not str or level not in ('easy','moderate','hard'):raise ValueError('Invalid level')
 if type(seed) is not int:raise ValueError('Seed requires builtin int')
 for name,value in [('template',template),('field_type',field_type),('profile',profile)]:
  if value is not None and type(value) is not str:raise ValueError(name+' requires a string')
 rng=random.Random(seed)
 for prefix in ('observed-','completed-observed-'):
  if profile and profile.startswith(prefix):
   selected=profile[len(prefix):]
   if template is not None and template!=selected:raise ValueError('Profile/template mismatch')
   template=selected
 if template is None:
  candidates=[sid for sid in QS if LEVELS[sid]==level and (field_type is None or normal_kind(sid)==field_type.replace(':answer-field.type/',''))]
  if not candidates:raise ValueError('Unsupported field type')
  template=rng.choice(candidates)
 if template not in QS or LEVELS[template]!=level:raise ValueError('Template/level mismatch')
 sid=template
 if profile not in (None,'normal','observed-'+sid,'completed-observed-q-17639'):raise ValueError('Unsupported complete profile')
 completed=profile=='completed-observed-q-17639'
 if completed and sid!='q-17639':raise ValueError('Completed historical profile belongs to q-17639')
 raw=profile=='observed-'+sid
 p=checked(sid,parameters if parameters is not None else rng.choice(domain(sid)));a=p['a'];q=strip_db(render_source(sid,p));f,d,target=expressions(sid,p)
 q.pop(':question/math-academy-id',None)
 if not raw:
  q[':question/difficulty']=':question.difficulty/'+level
  if ':question/worked-solution' not in q:q[':question/worked-solution']=authored_solution(sid,a)
  if ':question/answer-fields' not in q:
   q[':question/problem']+='\n\n'+r"$f'(\frac{\pi}{6})=$"+'\n{{field-1}}' if sid=='q-31288' else '\n\n'+r"$f'(x)=$"+'\n{{field-1}}'
   correct_tex=str(4*a) if sid=='q-31288' else math_transform(r'\frac{-x{csc}^{2}x-2\operatorname{cot}x}{{x}^{3}}',sid,a)
   q[':question/answer-fields']=[{':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':correct_tex}]}]
  for fld in q[':question/answer-fields']:
   if sid in OPAQUE and not completed:
    cs=sp.csc(X)**2;ss=sp.sec(X)**2;cot=sp.cot(X)
    if sid=='q-17639':
     right=a*ss-25*X**4+cs;bank=[right,ss-25*X**4+cs,a*ss-25*X**4-cs,a*ss-5*X**5+cs,a*ss-25*X**4]
    else:
     right=a*X**4*cs-4*a*X**3*cot;bank=[right,-4*a*X**3*cot-a*X**4*cs,4*a*X**3*cot+a*X**4*cs,-4*a*X**3*cot,a*X**4*cs]
    fld[':answer-field/choices']=[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in bank]
   matches=[ans for ans in fld[':answer-field/choices'] if eq(PARSER.expression(ans[':answer/value']),target)]
   if len(matches)!=1:raise ValueError('Complete profile missing or ambiguous correct value')
   fld[':answer-field/correct']=matches[0]
   vals=[PARSER.expression(ans[':answer/value']) for ans in fld[':answer-field/choices']]
   if any(eq(x,y) for n,x in enumerate(vals) for y in vals[n+1:]):raise ValueError('Whole bank collision')
  for k in (':question/problem',':question/worked-solution'):q[k]=FMT.normalize_prose(q[k])
  for fld in q[':question/answer-fields']:
   for ans in fld[':answer-field/choices']:ans[':answer/value']=FMT.normalize_tex(ans[':answer/value'])
 identity={k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')};identity['fields']=[]
 for fld in q.get(':question/answer-fields',[]):identity['fields'].append({'key':fld[':answer-field/key'],'type':fld[':answer-field/type'],'values':sorted(a[':answer/value'] for a in fld[':answer-field/choices']),'correct':fld.get(':answer-field/correct',{}).get(':answer/value')})
 content=digest(identity);qid=uid(content);q[':question/id']=qid
 for n,fld in enumerate(q.get(':question/answer-fields',[])):
  correct=fld.get(':answer-field/correct',{}).get(':answer/value');fid=uid(qid+':field:'+str(n));fld[':answer-field/id']=fid
  for ans in fld[':answer-field/choices']:ans[':answer/id']=uid(fid+':'+ans[':answer/value'])
  if correct is not None:fld[':answer-field/correct']=[':answer/id',next(ans[':answer/id'] for ans in fld[':answer-field/choices'] if ans[':answer/value']==correct)]
  if fld[':answer-field/type']==':answer-field.type/radio':rng.shuffle(fld[':answer-field/choices'])
 if field_type and normal_kind(sid)!=field_type.replace(':answer-field.type/',''):raise ValueError('Field contract mismatch')
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':sid,'profile':profile or 'normal','parameters':p,'seed':seed,'source_id':sid,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'evidence_only':raw or completed,'eligible_for_learning':not (raw or completed),'bank_origin':'historical bank with authored key/solution completion; opaque intent unresolved' if completed else 'historical bounded evidence' if raw else 'authored method bank' if sid in OPAQUE else 'parameterized source bank or authored minimal blank completion','content_sha256':content,'mathematical_fingerprint':digest([sp.srepr(f),sp.srepr(sp.pi/6) if sid=='q-31288' else None]),'domain':'Real connected intervals excluding sin(x)=0; quotient-by-cot also excludes cos(x)=0; logarithms require x>0; power quotient excludes x=0. Hard point pi/6 lies in (0,pi).','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
 if not raw:FMT.validate_generated_record(record)
 return record

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];text=q[':question/problem']+'\n\n'
 for fld in q.get(':question/answer-fields',[]):text+='\n'.join('- $'+ans[':answer/value']+'$' for ans in fld[':answer-field/choices'])+'\n'
 return text+'\n'+q.get(':question/worked-solution','[Original worked solution absent.]')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--format',choices=['json','markdown'],default='markdown');args=parser.parse_args()
 records=[generate(level,args.seed+n,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for n in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
