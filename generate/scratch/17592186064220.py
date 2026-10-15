#!/usr/bin/env python3
"""Definite linear inverse-trigonometric substitutions, exact source profiles.

Positive radial and numerator scales preserve each source's normalized interval,
field fragments, complete bank, and operative solution stages. No arcsec extension.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, importlib.util, json, random, re, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
def private(name):
 spec=importlib.util.spec_from_file_location('kp64220_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=private('math_format');parser=private('math_parser')
KP_ID=17592186064220
SOURCE=json.loads((HERE/'reference/sources.json').read_text())
KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
PROFILES=json.loads((HERE/'profiles.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
LEVELS=('easy','moderate','hard');VERSION='definite-inverse-trig-v1'
x=parser.X;u=parser.U

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return sp.latex(sp.simplify(v)).replace(r'\operatorname{asin}',r'\operatorname{arcsin}').replace(r'\operatorname{atan}',r'\operatorname{arctan}')
def integer(v,name,positive=False):
 if type(v) is not int or (positive and v<=0):raise ValueError(name+' must be a '+('positive 'if positive else '')+'builtin integer')
def data(sid,p):
 t=PROFILES[sid];h,k=p['h'],p['k'];integer(h,'h',True);integer(k,'k',True)
 if not(1<=h<=9 and 1<=k<=9):raise ValueError('Scale bounds are 1..9')
 if t['field_shape']=='asin-argument' and k!=1:raise ValueError('Supplied unit coefficient requires k=1')
 A=sp.Integer(t['a'])*h*h;B=sp.Integer(t['b']);N=sp.Integer(t['n'])*k
 L=sp.sympify(t['lower'])*h;R=sp.sympify(t['upper'])*h;s=sp.sqrt(B/A)
 pref=N/(sp.sqrt(A) if t['family']=='asin' else A);coef=sp.simplify(pref/s)
 fn=sp.asin if t['family']=='asin' else sp.atan
 target=N/(sp.sqrt(A-B*x*x)if t['family']=='asin'else A+B*x*x)
 ans=sp.simplify(coef*(fn(s*R)-fn(s*L)))
 scale=sp.Integer(k)if t['family']=='asin'else sp.Rational(k,h)
 return dict(A=A,B=B,N=N,L=L,R=R,s=s,pref=pref,coef=coef,fn=fn,target=target,answer=ans,bank_scale=scale,ul=sp.simplify(s*L),ur=sp.simplify(s*R))
def integral(expr,var,lo,hi):return r'\int_{'+tex(lo)+'}^{'+tex(hi)+'} '+expr+r'\,\text{d}'+str(var)
def integrand(d):return r'\frac{'+tex(d['N'])+'}{'+(r'\sqrt{'+tex(d['A']-d['B']*x*x)+'}'if d['fn']==sp.asin else tex(d['A']+d['B']*x*x))+'}'
def unit(arg,fn):return r'\frac{1}{'+(r'\sqrt{1-('+arg+r')^{2}}'if fn==sp.asin else '1+('+arg+r')^{2}')+'}'
def changed_solution(sid,d):
 """Preserve every source prose paragraph; parameterize formal operands and table.

The exact captured arithmetic layout is replayed at (h,k)=(1,1). Changed
instances use explicit positive-root normalization and individual endpoint rows.
"""
 old=SOURCES[sid][':question/worked-solution'];fn=d['fn'];name='arcsin'if fn==sp.asin else 'arctan';D=lambda t:'$$\n'+t+'\n$$'
 I=integral(integrand(d),x,d['L'],d['R']);norm=unit(tex(d['s']*x),fn);base=unit('u',fn)
 # Source's preliminary factoring block is retained only where observed.
 normalization=r'\begin{aligned}'+I+r' &= '+tex(d['pref'])+integral(norm,x,d['L'],d['R'])+r'\end{aligned}'
 # Retain the source's separate factorization and root/constant extraction
 # stages where it uses a multirow preliminary normalization.
 first=re.findall(r'\$\$(.*?)\$\$',old,re.S)[0]
 if first.count(r'\\')>=2 and r'\int'in first:
  signed='-'if fn==sp.asin else '+'
  factored=(r'\sqrt{'+tex(d['A'])+'(1'+signed+tex(d['B']*x*x/d['A'])+')}'if fn==sp.asin else tex(d['A'])+'(1+'+tex(d['B']*x*x/d['A'])+')')
  unsquared=(r'\sqrt{1-'+tex(d['B']*x*x/d['A'])+'}'if fn==sp.asin else '1+'+tex(d['B']*x*x/d['A']))
  normalization=r'\begin{aligned}'+I+r' &= '+integral(r'\frac{'+tex(d['N'])+'}{'+factored+'}',x,d['L'],d['R'])+r' \\ &= '+tex(d['pref'])+integral(r'\frac{1}{'+unsquared+'}',x,d['L'],d['R'])+r' \\ &= '+tex(d['pref'])+integral(norm,x,d['L'],d['R'])+r'\end{aligned}'
 basic=r'\int '+base+r'\,\text{d}u=\operatorname{'+name+r'}(u)+C.'
 diff=r'\frac{\text{d}u}{\text{d}x}='+tex(d['s'])+r'\quad\Longrightarrow\quad\text{d}x='+tex(1/d['s'])+r'\,\text{d}u.'
 primitive=tex(d['coef'])+r'\operatorname{'+name+r'}(u)'
 upper=tex(d['coef'])+r'\operatorname{'+name+'}('+tex(d['ur'])+')';lower=tex(d['coef'])+r'\operatorname{'+name+'}('+tex(d['ul'])+')'
 end=r'\begin{aligned}'+I+r' &= '+tex(d['pref'])+integral(norm,x,d['L'],d['R'])+r' \\ &= '+tex(d['pref'])+integral(base+r'\cdot ('+tex(1/d['s'])+')',u,d['ul'],d['ur'])+r' \\ &= '+tex(d['coef'])+integral(base,u,d['ul'],d['ur'])+r' \\ &= \left['+primitive+r'\right]_{'+tex(d['ul'])+'}^{'+tex(d['ur'])+r'} \\ &= '+upper+'-('+lower+r') \\ &= '+tex(d['coef']*fn(d['ur']))+'-('+tex(d['coef']*fn(d['ul']))+r') \\ &= '+tex(d['answer'])+r'\end{aligned}'
 blocks=re.findall(r'\$\$(.*?)\$\$',old,re.S); replacements=[]
 for i,b in enumerate(blocks):
  if i==len(blocks)-1:new=end
  elif r'\frac{\text{d}u}'in b:new=diff
  elif '+C' in b.replace(' ',''):new=basic
  else:new=normalization
  replacements.append(D(new))
 it=iter(replacements);out=re.sub(r'\$\$.*?\$\$',lambda m:next(it),old,flags=re.S)
 out=re.sub(r'we have \$.*?\.\$',lambda m:'we have $('+tex(d['s']*x)+r')^{2}.$',out)
 out=re.sub(r'substitute \$u=.*?\.\$',lambda m:'substitute $u='+tex(d['s']*x)+'.$',out)
 table='| $x$ | $'+tex(d['L'])+'$ | $'+tex(d['R'])+'$ |\n| --- | --- | --- |\n| $u$ | $'+tex(d['ul'])+'$ | $'+tex(d['ur'])+'$ |'
 out=re.sub(r'\| \$x\$ \|[^\n]*\n\| --- \| --- \| --- \|\n\| \$u\$ \|[^\n]*',lambda m:table,out)
 return out

@fmt.checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,bank_profile=None):
 integer(seed,'seed')
 if difficulty not in LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);eligible=[sid for sid,t in PROFILES.items()if t['difficulty']==difficulty]
 sid=template or rng.choice(eligible)
 if sid not in eligible:raise ValueError('Source profile/difficulty mismatch')
 t=PROFILES[sid];profile=t['bank_profile']
 if bank_profile not in (None,profile):raise ValueError('Complete observed bank required')
 # Profile is selected before parameter sampling. No pooled/fallback option recipes.
 p=dict(parameters)if parameters is not None else {'h':rng.randint(1,9),'k':1 if t['field_shape']=='asin-argument'else rng.randint(1,9)}
 if set(p)!={'h','k'}:raise ValueError('Expected h and k')
 d=data(sid,p);old=SOURCES[sid];original=p=={'h':1,'k':1}
 if original:prompt=old[':question/problem'];solution=old[':question/worked-solution']
 else:
  # Keep source question wording and answer placeholders exactly.
  prompt=re.sub(r'\{\\int \}_\{.*?\\,\\text\{d\}x',lambda m:integral(integrand(d),x,d['L'],d['R']),old[':question/problem'])
  # The one numerator-differential source has no trailing dx.
  if sid=='q-49546':
   start=old[':question/problem'].index('${');prompt=old[':question/problem'][:start]+'$'+integral(integrand(d),x,d['L'],d['R'])+'.$'
  solution=changed_solution(sid,d)
 prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution)
 # Keep the malformed raw original as ineligible evidence; serve a separately
 # documented presentation repair rather than bare italic operator letters.
 if sid in ('q-351839','q-351850'):solution=solution.replace(r'\,arctan\,',r'\,\operatorname{arctan}\,')
 values=[]
 for fi,f in enumerate(old[':question/answer-fields']):
  factor=1 if t['field_shape']=='asin-argument'or(t['field_shape']=='atan-coefficient-argument'and fi==1)else d['bank_scale']
  vals=[fmt.normalize_tex(a[':answer/value'])if original else fmt.normalize_tex(tex(factor*parser.latex(a[':answer/value'])))for a in f[':answer-field/choices']]
  ci=next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
  values.append((f,vals,ci))
 # Stable identity uses actual task, response shape and unordered semantic bank;
 # seed and option order are excluded. A fragment bank cannot collide with full value.
 task={'family':t['family'],'integrand':sp.srepr(d['target']),'bounds':[sp.srepr(d['L']),sp.srepr(d['R'])],'field_shape':t['field_shape'],'fields':[(f[':answer-field/key'],f[':answer-field/type'][':db/ident'],sorted(sp.srepr(parser.latex(v))for v in vs))for f,vs,ci in values]}
 qid=ident(task);fields=[]
 for f,vs,ci in values:
  fid=ident([qid,f[':answer-field/key']]);answers=[{':answer/id':ident([fid,v,old_a[':answer/id'] if vs.count(v)>1 else 'unique']),':answer/type':':answer.type/math',':answer/value':v}for v,old_a in zip(vs,f[':answer-field/choices'])]
  fields.append({':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':sid,'bank_profile':profile,'parameters':p,'source_ids':[sid],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'original_parameters':original,'source_presentation_repair':sid in ('q-351839','q-351850') and original,'task_fingerprint':digest(task),'domain':'h,k builtin integers 1..9; positive scale; asin argument fragment k=1; principal asin [-pi/2,pi/2] and atan (-pi/2,pi/2); original normalized interval retained','dependencies':{'sympy':sp.__version__},'plots':'none'}}

def batch(difficulty='all',count=1,seed=0):
 integer(seed,'seed');integer(count,'count',True)
 levels=LEVELS if difficulty=='all'else(difficulty,)
 if any(z not in LEVELS for z in levels):raise ValueError('Unknown difficulty')
 records=[];seen=set()
 for level in levels:
  got=0
  for i in range(count*100+100):
   r=generate(level,seed+i);fp=r['generation']['task_fingerprint']
   if fp in seen:continue
   records.append(r);seen.add(fp);got+=1
   if got==count:break
  if got!=count:raise ValueError('Bounded unique inventory exhausted')
 return records

def markdown(rec):
 q=rec['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='Field '+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+')\n\n'
  for a in f[':answer-field/choices']:out+='- $'+a[':answer/value']+'$'+(' (correct)'if a[':answer/id']==f[':answer-field/correct'][1]else'')+'\n'
 return out+'\n'+q[':question/worked-solution']

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
 try:rs=batch(args.difficulty,args.count,args.seed)
 except ValueError as e:ap.error(str(e))
 print(json.dumps(rs,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in rs))
