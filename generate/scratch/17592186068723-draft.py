#!/usr/bin/env python3
"""Private bounded constant-multiple power substitution draft. Never accesses EDB.

Source masks preserve complete prose and ordered operations; only whole inner
polynomials are slotted. Source profiles retain incomplete evidence separately.
"""
import argparse,copy,hashlib,importlib.util,json,random,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
PROFILES=json.loads((HERE/'templates.json').read_text())
KP_ID=17592186068723
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='constant-power-substitution-v2-draft'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
LEVELS=('easy','moderate','hard')
DOMAIN=tuple(i for i in range(-40,41) if i)
X=sp.Symbol('x',real=True)
_spec=importlib.util.spec_from_file_location('constant_power_private_formatter',HERE/'math_format.py')
_format=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_format)
normalize_prose=_format.normalize_prose;normalize_tex=_format.normalize_tex
for _sid,_parent,_a in [('hard-signed-cubic-root','q-113715',-1),('hard-signed-square-root','q-72467',-1)]:
 PROFILES[_sid]=dict(PROFILES[_parent],a=_a,difficulty='hard',parent=_parent,authored=True)

def integer(v,name):
 if type(v) is not int:raise ValueError(name+' must be a builtin int, excluding bool')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return sp.latex(v,order='lex')
def allowed(t):return tuple(b for b in DOMAIN if not(t['a']<0 and t['m']%2==0 and sp.Rational(t['n']).q>1 and b<0))
def base(t,b):
 if b==t['b'] and not t.get('authored'):return t['base']
 term=('{x}^{'+str(t['m'])+'}')
 if t['a']<0:return str(b)+'-'+(str(-t['a']) if t['a']!=-1 else '')+term
 term=(str(t['a']) if t['a']!=1 else '')+term
 return term+('+' if b>0 else '')+str(b)
def parameter(t,parameters,default):
 if parameters is None:return {'b':default}
 if type(parameters) is not dict or set(parameters)!={'b'}:raise ValueError('parameters must contain exactly b')
 integer(parameters['b'],'b')
 if parameters['b'] not in allowed(t):raise ValueError('b outside declared bounded nondegenerate domain')
 return dict(parameters)
@lru_cache(maxsize=None)
def fingerprint(k,a,m,b,n):return digest(sp.srepr(sp.expand(k*X**(m-1)*(a*X**m+b)**sp.Rational(n))))
def data(t,b):
 k,a,m,n=map(sp.Rational,(t['k'],t['a'],t['m'],t['n']));u=a*X**m+b
 return u,k*X**(m-1)*u**n,k/(a*m),k/(a*m*(n+1))*u**(n+1)
def source_record(sid):
 return copy.deepcopy(next(q for q in SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')==sid))
def _identities(q):
 # Metadata/profile aliases and option order cannot create content identities.
 qid=ident([VERSION,{k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')},[[f[':answer-field/key'],f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f.get(':answer-field/correct',[None,None])[1]),None)] for f in q.get(':question/answer-fields',[])]])
 q[':question/id']=qid
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  cid=f.get(':answer-field/correct',[None,None])[1];fid=ident([qid,'field',i,f[':answer-field/key']]);f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:
   old=a[':answer/id'];a[':answer/id']=ident([fid,a[':answer/value']])
   if old==cid:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
def _record(q,t,sid,p,seed,raw):
 n=sp.Rational(t['n']);b=p['b'];dom={'number_system':'real','constraint':base(t,b)+'>0' if n.q>1 else 'all real x','branch':'principal real square root' if n.q>1 else 'integer powers','variable':'x'}
 fp=fingerprint(t['k'],t['a'],t['m'],b,str(n))
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'generator_id':GENERATOR_UUID,'seed':seed,'template':sid,'profile':sid,'bank_profile':sid,'parameters':p,'mathematical_parameters':{k:t[k] for k in ('k','a','m','n')}|p,'mathematical_fingerprint':fp,'parameter_fingerprint':fp,'domain':dom,'source_basis':SOURCE['basis'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_ids':[t.get('parent',sid.removeprefix('source:'))],'evidence_only':raw,'eligible_for_learning':not raw,'evidence_role':'raw MA evidence; original omissions and math/presentation anomalies retained' if raw else 'authored missing hard level' if t.get('authored') else 'authored completion' if sid=='q-12494' else 'source-shaped parameterized normal record','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none','sampling_policy':'Only the nonzero inner constant varies in -40..40; negative even radicands require positive shift. All other source parameters and ordered stages fixed.'}}
def raw_replay(t,sid,p,seed):
 q=source_record(sid);old=t['base'];new=base(t,p['b'])
 for k in (':question/problem',':question/worked-solution'):
  if k in q:q[k]=q[k].replace(old,new)
 for f in q.get(':question/answer-fields',[]):
  f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident'];a[':answer/value']=a[':answer/value'].replace(old,new)
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 q.pop(':db/id',None);q.pop(':question/math-academy-id',None);_identities(q)
 random.Random(seed).shuffle(q[':question/answer-fields'][0][':answer-field/choices'])
 return _record(q,t,'source:'+sid,p,seed,True)

def authored_solution(t,b):
 # Missing hard combines the already taught negative factor and square-root
 # conversion, with the same ordered substitution/integration operations.
 u=base(t,b);k,a,m,n=t['k'],t['a'],t['m'],sp.Rational(t['n']);outside=tex(k*X**(m-1));deriv=tex(a*m*X**(m-1));r=sp.Rational(k,a*m)
 factor=r'\sqrt{'+u+'}';integ=r'\int '+outside+factor+r'\,\text{d}x'
 solution=('In this case, the $'+outside+"$ that's outside the square root isn't quite the derivative of $("+u+').$ But the derivative is $'+deriv+",$ so we're only out by a constant factor.\n\nSo we make the substitution\n\n$$\nu="+u+'.\n$$\n\nIts derivative is given by\n\n$$\n'+r'\begin{aligned}\frac{\text{d}u}{\text{d}x} & ='+deriv+r'\,⟹\,('+tex(r)+r')\text{d}u='+outside+r'\,\text{d}x,\end{aligned}'+'\n$$\n\nand we can now write our integral in terms of $u,$ as follows:\n\n$$\n'+r'\begin{aligned}'+integ+r' & =\int '+factor+r'\cdot '+outside+r'\,\text{d}x \\ & =\int \sqrt{u}\cdot ('+tex(r)+r')\text{d}u \\ & ='+tex(r)+r'\int {u}^{1/2}\,\text{d}u\end{aligned}'+'\n$$\n\nFinally, we can solve the integral in terms of $u$ and then write the final result in terms of $x.$ We get\n\n$$\n'+r'\begin{aligned}'+tex(r)+r'\int {u}^{1/2}\,\text{d}u & =('+tex(r)+r')\cdot \frac{{u}^{3/2}}{(\frac{3}{2})}+C \\ & =('+tex(r)+r')\cdot \frac{2}{3}\cdot {u}^{3/2}+C \\ & ='+tex(r*sp.Rational(2,3))+r'{u}^{3/2}+C \\ & ='+tex(r*sp.Rational(2,3))+r'\sqrt{{u}^{3}}+C \\ & ='+tex(r*sp.Rational(2,3))+r'\sqrt{('+u+r')^{3}}+C.\end{aligned}'+'\n$$')
 return 'Calculate $'+integ+'.$',solution
def completed_solution(t,b):
 # q-12494 has no source solution: author the same integer-power backbone.
 u=base(t,b);n=t['n'];r=sp.Rational(1,2)
 prompt='Calculate $'+r'\int x('+u+r')^{10}\,\text{d}x.$'
 reference=PROFILES['q-2388'];sol=reference['solution'].replace('@@BASE@@',u)
 # Whole exponent/primitive slots, never arbitrary short numeral replacement.
 sol=sol.replace('{u}^{3}', '{u}^{10}').replace('{u}^{4}', '{u}^{11}').replace('^{3}', '^{10}').replace('^{4}', '^{11}').replace(r'\frac{1}{8}',r'\frac{1}{22}').replace(r'\frac{{u}^{11}}{4}',r'\frac{{u}^{11}}{11}').replace(')^{11}}{8}',')^{11}}{22}')
 return prompt,sol
def normal_generate(t,sid,p,seed):
 b=p['b'];inner=base(t,b)
 if t.get('authored'):prompt,sol=authored_solution(t,b)
 elif sid=='q-12494':prompt,sol=completed_solution(t,b)
 else:prompt=t['prompt'].replace('@@BASE@@',inner);sol=t['solution'].replace('@@BASE@@',inner)
 if sid=='q-113715':sol=sol.replace(r'\frac{2}{3}\cdot \frac{2}{3}\cdot {u}^{3/2} \\',r'\frac{2}{3}\cdot \frac{2}{3}\cdot {u}^{3/2}+C \\')
 values=[r['value'].replace('@@BASE@@',inner) for r in t['bank']]
 correct=next((i for i,r in enumerate(t['bank']) if r['correct']),4)
 if t.get('authored') or sid=='q-12496':
  # Explicit authored complete operation bank: omit constant factor, invert
  # factor, omit exponent division, and retain old exponent. No fitted bank.
  r=sp.Rational(t['k'],t['a']*t['m']);n=sp.Rational(t['n']);power='('+inner+')^{'+tex(n+1)+'}';old='('+inner+')^{'+tex(n)+'}'
  values=[tex(r/(n+1))+power+'+C',tex(1/(n+1))+power+'+C',tex(1/(r*(n+1)))+power+'+C',tex(r)+power+'+C',tex(r/n)+old+'+C'];correct=0
 values=[normalize_tex(v) for v in values]
 field={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)],':answer-field/correct':[':answer/id',str(correct)]}
 q={':question/problem':normalize_prose(prompt),':question/worked-solution':normalize_prose(sol),':question/difficulty':':question.difficulty/'+t['difficulty'],':question/answer-fields':[field]}
 _identities(q);random.Random(seed).shuffle(field[':answer-field/choices'])
 return _format.validate_generated_record(_record(q,t,sid,p,seed,False))
def generate(level='moderate',seed=0,template=None,field_type=None,parameters=None,profile=None):
 integer(seed,'seed')
 if type(level) is not str or level not in LEVELS:raise ValueError('Unknown level')
 for v in (template,profile):
  if v is not None and (type(v) is not str or not v):raise ValueError('template/profile must name a declared profile')
 if template and profile and template!=profile:raise ValueError('template/profile mismatch')
 if field_type not in (None,'radio',':answer-field.type/radio') or isinstance(field_type,bool):raise ValueError('Only radio supported')
 rng=random.Random(seed);sid=profile or template or rng.choice([s for s,t in PROFILES.items() if t['difficulty']==level])
 raw=sid.startswith('source:');key=sid.removeprefix('source:')
 if key not in PROFILES or raw and PROFILES[key].get('authored'):raise ValueError('Unknown profile')
 t=PROFILES[key]
 if t['difficulty']!=level:raise ValueError('Ineligible profile for level; raw unrated q-12494 uses authored easy API routing only')
 default=t['b'] if raw else rng.choice(allowed(t));p=parameter(t,parameters,default)
 return raw_replay(t,key,p,seed) if raw else normal_generate(t,key,p,seed)
# Easy: observed positive integer outer powers, one constant factor.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: observed negative factor OR square-root-to-power conversion.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard (authored): both negative factor and square-root conversion, same method.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def capacity(level):
 if type(level) is not str or level not in LEVELS:raise ValueError('Unknown level')
 return len({fingerprint(t['k'],t['a'],t['m'],b,str(t['n'])) for t in PROFILES.values() if t['difficulty']==level for b in allowed(t)})
def batch(level,count=1,seed=0,template=None,profile=None,field_type=None):
 integer(seed,'seed');integer(count,'count')
 if type(level) is not str or level not in LEVELS or count<0:raise ValueError('Invalid level/count')
 if template and profile and template!=profile:raise ValueError('template/profile mismatch')
 sid=profile or template
 if sid is not None:
  generate(level,seed,template,field_type,None,profile)
 pairs=[(s,b) for s,t in PROFILES.items() if t['difficulty']==level and (sid is None or s==sid or 'source:'+s==sid) for b in allowed(t)]
 unique={fingerprint(PROFILES[s]['k'],PROFILES[s]['a'],PROFILES[s]['m'],b,str(PROFILES[s]['n'])) for s,b in pairs}
 if count>len(unique):raise ValueError('Requested count exceeds finite mathematical capacity')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio supported')
 random.Random(seed).shuffle(pairs);out=[];seen=set()
 for key,b in pairs:
  if len(out)==count:break
  t=PROFILES[key];fp=fingerprint(t['k'],t['a'],t['m'],b,str(t['n']))
  if fp in seen:continue
  r=generate(level,seed,profile=sid or key,field_type=field_type,parameters={'b':b});seen.add(fp);out.append(r)
 return out
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Source has no worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 rows=[r for lev in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for r in batch(lev,a.count,a.seed,a.template,a.profile)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
