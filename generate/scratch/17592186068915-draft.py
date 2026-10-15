#!/usr/bin/env python3
"""Finite, source-shaped affine sin/cos integrals. Local review draft; no EDB writes."""
from __future__ import annotations
import argparse,hashlib,importlib.util,itertools,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('kp68915_private_formatter',HERE/'reference/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
KP=17592186068915;VERSION='linear-trig-2275-draft-v2';SOURCE=json.loads((HERE/'source.json').read_text());REC=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions'] if ':question/math-academy-id'in q}
x,u,C=s.symbols('x u C',real=True)
# difficulty, field, trig, angle slope carries pi, shift carries pi, original slots
CONFIG={
'q-10061':('easy','radio','sin',False,False,{'a':'2','b':'0','c':1}),
'q-2204':('easy','radio','sin',False,False,{'a':'5','b':'0','c':1}),
'q-10064':('easy','radio','cos',False,False,{'a':'-9','b':'3','c':1}),
'q-350040':('easy','blank','sin',False,True,{'a':'2','b':'0','c':9,'lo':'0','hi':'1/2'}),
'q-13647':('moderate','radio','sin',False,True,{'a':'4','b':'0','c':5,'lo':'0','hi':'1/2'}),
'q-346081':('moderate','blank','cos',True,True,{'a':'1/4','b':'0','c':1,'lo':'0','hi':'1/2'}),
'q-10574':('moderate','radio','sin',False,True,{'a':'3','b':'1/3','c':1,'lo':'1/3','hi':'2/3'}),
'authored-hard':('hard','radio','sin',False,True,{'a':'3','b':'1/3','c':1,'lo':'1/3','hi':'2/3'}),
}
ENDPOINTS={'q-350040':(('0','1/2'),('0','1/3'),('0','2/3')),'q-13647':(('0','1/2'),('0','1/3'),('0','2/3')),'q-346081':(('0','1/2'),('0','1/6'),('0','1/3')),'q-10574':(('1/3','2/3'),('1/6','1/2'),('1/2','5/6')),'authored-hard':(('1/3','2/3'),('1/6','1/2'),('1/2','5/6'))}
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+z))
def tex(z):return fmt.normalize_tex(s.latex(z))
def rat(z):
 if type(z)is not str or not re.fullmatch(r'-?(?:0|[1-9]\d*)(?:/[1-9]\d*)?',z):raise ValueError('rational slots require canonical strings')
 v=s.Rational(z)
 if str(v)!=z:raise ValueError('rational slots must be reduced')
 return v
def sourceid(sid):return 'q-10574' if sid=='authored-hard' else sid
def instances(sid):
 if sid not in CONFIG:raise ValueError('unknown template')
 if sid in ('q-10061','q-2204'):aa=tuple(map(str,range(2,11)));bs=('0',);cs=range(1,5)
 elif sid=='q-10064':aa=tuple(map(str,range(-10,-3)));bs=('1','2','3','4');cs=range(1,5)
 elif sid=='q-346081':aa=('1/2','1/3','1/4','1/5');bs=('0',);cs=range(1,5)
 elif sid in ('q-10574','authored-hard'):aa=('2','3','4','5','6');bs=('-1/3','-1/6','1/6','1/3');cs=range(1,5)
 else:aa=('2','3','4','5','6');bs=('0',);cs=range(2,10)
 for a,b,c in itertools.product(aa,bs,cs):
  p={'a':a,'b':b,'c':c}
  if sid in ENDPOINTS:
   for lo,hi in ENDPOINTS[sid]:yield dict(p,lo=lo,hi=hi)
  else:yield p

def guard(sid,p):
 if sid not in CONFIG or type(p)is not dict or set(p)!=set(CONFIG[sid][-1]):raise ValueError('missing or extra slots')
 if type(p['c'])is not int:raise ValueError('c requires strict builtin integer')
 for k,z in p.items():
  if k!='c':rat(z)
 if not any(p==z for z in instances(sid)):raise ValueError('outside declared finite parameter domain')
 conf=CONFIG[sid];a=rat(p['a'])*(s.pi if conf[3] else 1);b=rat(p['b'])*(s.pi if conf[4] else 1)
 return a,b,s.Integer(p['c'])
def product(c,t):
 if t.startswith('-'):return product(-c,t[1:])
 return t if c==1 else '-'+t if c==-1 else tex(c)+t
def fn(name,arg):return '\\'+name+'('+arg+')'
def integral(body,var='x',bounds=None):return r'\int'+('_{'+tex(bounds[0])+'}^{'+tex(bounds[1])+'}' if bounds else '')+' '+body+r'\,\text{d}'+var

def core(sid,p,profile):
 conf=CONFIG[sid];level,field,fname=conf[:3];a,b,c=guard(sid,p);arg=a*x+b;A=tex(arg);r=c/a;definite='lo'in p;var='z' if sid=='q-2204' else 'x';V=s.Symbol(var,real=True)
 lo=rat(p['lo'])*s.pi if definite else None;hi=rat(p['hi'])*s.pi if definite else None;xb=((lo-b)/a,(hi-b)/a) if definite else None
 f=getattr(s,fname);P=(lambda z:-s.cos(z)) if fname=='sin' else s.sin
 correct=s.simplify(r*(P(hi)-P(lo))) if definite else r*P(arg)+C
 if sid=='q-10061':values=[r*s.cos(arg)+C,-c*a*s.cos(arg)+C,c*a*s.cos(arg)+C,-r*s.sin(arg)+C,correct]
 elif sid=='q-2204':values=[c*s.cos(arg)+C,correct,r*s.cos(arg)+C,-r*s.cos(x)+C,c*a*s.cos(arg)+C]
 elif sid=='q-10064':values=[-c/rat(p['b'])*s.sin(arg)+C,correct,-r*s.cos(arg)+C,-r*s.sin(arg)+C,r*s.cos(arg)+C]
 elif sid=='q-13647':values=[s.Integer(0),correct,-correct,s.Integer(1),s.Integer(-1)]
 elif sid in ('q-10574','authored-hard'):
  delta=s.simplify(P(hi)-P(lo));values=[c*delta/2,correct,2*correct,correct/2,c*a*delta/2]
 else:values=[correct]
 # Entire banks remain intact; reject wrong/wrong and correct/wrong equivalence.
 for i,v in enumerate(values):
  for w in values[:i]:
   d=s.diff(v-w,x) if not definite else v-w
   if d.has(x):
    probe=s.N(d.subs(x,s.Rational(2,7)),20)
    if probe.is_real and probe.is_finite and abs(probe)>s.Float('1e-14'):continue
   if s.trigsimp(s.expand_trig(d))==0:raise ValueError('complete bank collision modulo C')
 I=integral(product(c,fn(fname,tex(arg.subs(x,V)))),var,bounds=xb)
 src=sourceid(sid)
 if src=='q-2204':prompt='Calculate $\\displaystyle '+I+'$.'
 elif src=='q-13647':prompt='$'+I+'=$'
 elif field=='blank':prompt='Evaluate the following integral. '+('Do not round the answer.' if profile=='observed' else 'Give an exact answer.')+'\n\n$'+I+'=$\n'+('\n' if src=='q-350040' else '')+'{{field-1}}'
 else:prompt='Calculate $'+I+'.$'
 diff=r'\frac{\text{d}u}{\text{d}'+var+'}='+tex(a)+r'\,⟹\,\text{d}'+var+'='+tex(1/a)+(r'\,' if src=='q-346081' else '')+r'\text{d}u.'
 iu=integral(fn(fname,'u'),'u',(lo,hi) if definite else None)
 body=product(c,fn(fname,'u'))+r'\cdot '+('('+tex(1/a)+')' if a<0 else tex(1/a))
 sub=integral(body,'u',(lo,hi) if definite else None);scaled=product(r,iu)
 if not definite:rows=[sub,scaled,product(r,('-' if fname=='sin' else '')+fn('cos' if fname=='sin' else 'sin','u'))+'+C',tex(correct.subs(x,V))]
 else:
  primitive=product(-r if fname=='sin' else r,fn('cos' if fname=='sin' else 'sin','u'))
  bar=primitive+r'\big|_{'+tex(lo)+'}^{'+tex(hi)+'}'
  endpoint=product(-r if fname=='sin' else r,'('+fn('cos' if fname=='sin' else 'sin',tex(hi))+'-'+fn('cos' if fname=='sin' else 'sin',tex(lo))+')')
  numeric=product(-r if fname=='sin' else r,'('+tex(s.cos(hi) if fname=='sin' else s.sin(hi))+'-'+tex(s.cos(lo) if fname=='sin' else s.sin(lo))+')')
  rows=[sub,scaled,bar,endpoint,numeric,tex(correct)]
 table=''
 if definite:table='Calculating the limits for $u$ gives\n\n| $x$ | $'+tex(xb[0])+'$ | $'+tex(xb[1])+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(lo)+'$ | $'+tex(hi)+'$ |\n\n'
 solution='If we let $u='+A.replace('x','z')+',$ then' if var=='z' else 'If we let $u='+A+',$ then'
 solution+='\n\n$$\n'+diff+'\n$$\n\n'+table+'Using the above, we can '+('rewrite' if src=='q-346081' else 'write')+' the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+I+' & ='+r' \\ & ='.join(rows)+r'\end{aligned}'+'\n$$'
 return prompt,solution,values,correct,{'integrand':str(c*f(arg)),'bounds':list(map(str,xb)) if definite else None,'argument':str(arg),'primitive':str(r*P(arg)),'stage_count':len(rows),'transformed_endpoint_angles':list(map(str,(lo,hi))) if definite else None}

@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if type(seed)is not int:raise ValueError('seed must be a strict builtin integer')
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if profile not in (None,'observed','method'):raise ValueError('unknown profile')
 if field_type not in (None,'radio','blank'):raise ValueError('unknown field type')
 eligible=[k for k,v in CONFIG.items() if v[0]==level and (field_type is None or v[1]==field_type)]
 if template is not None and template not in eligible:raise ValueError('difficulty/template/field mismatch')
 sid=template or random.Random(seed).choice(eligible)
 if parameters is None:
  pool=list(instances(sid));random.Random(seed).shuffle(pool)
  for p in pool:
   try:out=core(sid,p,profile or 'method');break
   except ValueError:continue
  else:raise ValueError('no eligible complete banks')
 else:p=dict(parameters) if type(parameters)is dict else parameters;out=core(sid,p,profile or 'method')
 prompt,solution,values,correct,model=out;prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution)
 var=s.Symbol('z',real=True) if sid=='q-2204' else x;vals=[tex(s.simplify(v).subs(x,var)) for v in values];cv=tex(s.simplify(correct).subs(x,var));field=CONFIG[sid][1];key='selection' if field=='radio' else 'field-1'
 ident=digest([VERSION,prompt,solution,field,sorted(vals),cv,level]);qid=uid(ident);fid=uid(ident+key)
 answers=[{':answer/id':uid(fid+z),':answer/type':':answer.type/math',':answer/value':z} for z in vals];random.Random(digest([seed,'options'])).shuffle(answers)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+field,':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+cv)]}]}
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':sid,'bank_profile':profile or 'method','seed':seed,'parameters':dict(p),'source_id':sourceid(sid),'source_basis':2275,'source_lineage':SOURCE['lineage'],'evidence_only':sid=='q-2204' and profile=='observed','eligible_for_learning':not(sid=='q-2204' and profile=='observed'),'authored_rating':sid in ('q-2204','authored-hard'),'calibration':'hard label provisional: same moderate shifted definite workload; no hard source evidence' if sid=='authored-hard' else 'q2204 easy rating and missing key/solution authored' if sid=='q-2204' else 'observed difficulty','source_repairs':['missing original key, worked solution and easy rating independently completed'] if sid=='q-2204' else [],'domain':'real x; sin and cos entire on real line; every definite endpoint finite, closed interval in the unique real pole-free component','model':model,'mathematical_fingerprint':digest([model['integrand'],model['bounds']]),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__,'formatter':'private pinned math_format.py'}}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def _pool_uncached(level,template=None,field_type=None,profile=None):
 for sid,v in CONFIG.items():
  if v[0]!=level or (template is not None and sid!=template) or (field_type is not None and v[1]!=field_type):continue
  for p in instances(sid):
   try:r=core(sid,p,profile or 'method')
   except ValueError:continue
   yield sid,p,digest([r[4]['integrand'],r[4]['bounds']])
_POOLS={}
def pool(level,template=None,field_type=None,profile=None):
 key=(level,template,field_type,profile)
 if key not in _POOLS:_POOLS[key]=tuple(_pool_uncached(level,template,field_type,profile))
 return iter(_POOLS[key])
def capacity(level,**kw):return len({fp for _,_,fp in pool(level,**kw)})
def batch(level,seed=0,count=1,**kw):
 if set(kw)-{'template','field_type','profile'}:raise ValueError('unknown selector')
 if type(seed)is not int or type(count)is not int or count<1:raise ValueError('strict integer seed/count; count positive')
 if level=='all':return [r for lev in ('easy','moderate','hard') for r in batch(lev,seed,count,**kw)]
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 # Validate selectors even for empty pools.
 if kw.get('profile')not in (None,'observed','method') or kw.get('field_type')not in (None,'blank','radio'):raise ValueError('invalid selector')
 if kw.get('template')is not None and (kw['template']not in CONFIG or CONFIG[kw['template']][0]!=level):raise ValueError('invalid template')
 candidates=list(pool(level,**kw));random.Random(seed).shuffle(candidates);selected=[];seen=set()
 for sid,p,fp in candidates:
  if fp not in seen:seen.add(fp);selected.append((sid,p))
 if count>len(selected):raise ValueError('count exceeds finite meaningful task capacity '+str(len(selected)))
 return [generate(level,seed+i,template=sid,parameters=p,profile=kw.get('profile'),field_type=kw.get('field_type'))for i,(sid,p)in enumerate(selected[:count])]
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/id']+' $'+a[':answer/value']+'$' for f in q[':question/answer-fields']for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--field-type',choices=['radio','blank']);ap.add_argument('--profile',choices=['observed','method']);ap.add_argument('--format',choices=['json','markdown'],default='markdown');a=ap.parse_args()
 try:records=batch(a.difficulty,a.seed,a.count,template=a.template,field_type=a.field_type,profile=a.profile)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
