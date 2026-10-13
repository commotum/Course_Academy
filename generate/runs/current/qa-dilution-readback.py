"""Root QA: read actual dilution prompts, full banks, and every math row."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
from decimal import Decimal,ROUND_HALF_UP,localcontext
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P=load('root_scalar',ROOT/'generate/runs/current/ode-scalar-parser.py');t=P.t
def rounding(x,places):
 with localcontext() as c:
  c.prec=60
  return s.Rational(str(Decimal(str(s.N(x,55))).quantize(Decimal(10)**(-places),rounding=ROUND_HALF_UP)))
def qty(prompt,unit):
 return [P.scalar(z.strip()) for z in re.findall(r'\$([^$]*?)\$',prompt) if unit in z for z in [z.split(r'\,')[0].split('kg')[0].split('L')[0].split('g/')[0].split(r'\text')[0].split('gal')[0].split('lb')[0].strip().rstrip(',')]]
def clean(text):
 text=text.strip().rstrip('.,').replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 text=re.sub(r'\\(?:text|textrm)\{[^{}]*\}','ROOTUNIT',text)
 text=text.replace(r'\cancel{ROOTUNIT}','ROOTUNIT').replace(r'\frac{ROOTUNIT}{ROOTUNIT}','(1)').replace(r'\,','').replace('⁡','')
 text=text.replace('ROOTUNIT','')
 return text
def read(text,env):
 text=clean(text)
 for pattern,key in [(r'\{?Q\}?_\{\\text\{in\}\}\^\{[′\']\}', 'IN'),(r'\{?Q\}?_\{\\text\{out\}\}\^\{[′\']\}', 'OUT')]:
  text=re.sub(pattern,lambda m: '('+s.latex(env[key])+')',text)
 # clean() removed these text subscripts; handle their normalized spelling too.
 text=re.sub(r'\{?Q\}?_\{1\}\^\{[′\']\}', 'ROOT_RATE',text)
 if text=='ROOT_RATE':raise ValueError('Rate name needs preservation before unit cleaning')
 if text.startswith(r'\int'):
  text=text[len(r'\int'):].strip();text=re.sub(r'\s*dt\s*$','',text)
  if text.startswith(r'\frac{d}{dt}'):
   # Read the explicit integral-of-a-derivative operator structurally. Its
   # primitive is the displayed differentiand up to an arbitrary constant.
   return read(text[len(r'\frac{d}{dt}'):],env)
  return s.integrate(read(text,env),t)
 if text.startswith(r'\frac{d}{dt}'):
  return s.diff(read(text[len(r'\frac{d}{dt}'):],env),t)
 text=text.replace(r'\frac{dQ}{dt}','u').replace(r'\frac{d{Q}_{c}}{dt}','('+s.latex(s.diff(env['A']*s.exp(-env['coefficient']*t),t))+')')
 text=text.replace(r'V({t}_{o})','('+s.latex(env['volume'].subs(t,env['T']))+')')
 text=text.replace(r'{t}_{o}','('+s.latex(env['T'])+')').replace(r't_{o}','('+s.latex(env['T'])+')')
 text=re.sub(r'V\((t|\([0-9]+(?:\.[0-9]+)?\)|[0-9]+(?:\.[0-9]+)?)\)',lambda m:'('+s.latex(env['volume'].subs(t,read(m[1],env)))+')',text)
 text=re.sub(r'Q\((t|[0-9]+(?:\.[0-9]+)?)\)',lambda m:'('+s.latex(env['Q'].subs(t,read(m[1],env)))+')',text)
 text=re.sub(r'I\(t\)','i',text);text=re.sub(r'V\(t\)','j',text)
 text=text.replace(r'{Q}_{c}(t)','v*e^{-'+s.latex(env['coefficient'])+'*t}')
 text=text.replace(r'{Q}_{p}(t)','z').replace(r'{Q}_{c}','(v*e^{-'+s.latex(env['coefficient'])+'*t})').replace(r'{Q}_{p}','z')
 text=text.replace(r'\alpha','z').replace('α','z').replace(r'\beta','k').replace('β','k')
 text=text.replace('Q','x').replace('C','y').replace('A','v')
 text=text.replace(r'{t}_{o}',s.latex(env['T'])).replace(r't_{o}',s.latex(env['T']))
 text=re.sub(r'((?:\\ln|\\operatorname\{ln\})⁡?)\s*(\([^()]+\)\^\{[^{}]+\})',r'\1(\2)',text)
 # Absolute values occur only for the strictly positive normalized volume.
 text=re.sub(r'\|([^|]+)\|',r'(\1)',text)
 return P.scalar(text).subs({P.x:env['Q'],P.y:env['C'],P.z:env['alpha'],P.u:env['DQ'],P.v:env['A'],P.i:env['IF'],P.j:env['volume'],P.k:env['beta']})
def rate_names(text,env):
 for pat,key in [(r"\{Q\}_\{\\text\{in\}\}\^\{[′']\}",'IN'),(r"\{Q\}_\{\\text\{out\}\}\^\{[′']\}",'OUT'),(r"Q'_\{\\text\{in\}\}",'IN'),(r"Q'_\{\\text\{out\}\}",'OUT')]:
  text=re.sub(pat,lambda m:'('+s.latex(env[key])+')',text)
 return text
def physics(k,pr):
 # Read quantities in narrative order with their declared units, not generation metadata.
 vals=[];units=[]
 for frag in re.findall(r'\$([^$]*?)\$',pr):
  m=re.match(r'\s*((?:\\frac\{[^{}]+\}\{[^{}]+\}|[0-9]+(?:\.[0-9]+)?))\s*(?:\\,)?(?:\\text\{)?(kg/L|g/L|L/min|gal/min|lb/gal|kg|gal|lb|L)',frag)
  if m:vals.append(P.scalar(m[1]));units.append(m[2])
 if k==17592186229183:
  assert units==['gal','gal','lb','lb/gal','gal/min','gal/min'],units
  H,V,q,c,ri,ro=vals;T=(H-V)/(ri-ro);places=1;kind='amount'
 else:
  assert units in (['L','kg','kg/L','L/min','L/min'],['L','kg','g/L','L/min','L/min']),units
  V,q,c,ri,ro=vals
  if units[2]=='g/L':c/=1000
  kind='sum' if 'α + β' in pr else 'difference' if r'\alpha -\beta' in pr else 'expression' if 'Which expression' in pr else 'amount'
  times=re.findall(r'\$([0-9]+)\$ minutes after pumping begins',pr)
  T=s.Rational(times[-1]) if times else s.Integer(0);places=2
 delta=ri-ro;volume=V+delta*t
 if delta==0:
  coefficient=ro/V;alpha=c*V;beta=q-alpha;IF=s.exp(coefficient*t);C=beta;A=beta
  Q=alpha+beta*s.exp(-coefficient*t)
 else:
  B=V/abs(delta);n=ro/delta;IF=(B+s.sign(delta)*t)**n
  coefficient=ro/volume;alpha=c*V;beta=q-alpha;C=beta*B**n;A=beta
  Q=c*volume+beta*(V/volume)**n
 assert s.simplify(s.diff(Q,t)-(c*ri-ro*Q/volume))==0
 assert Q.subs(t,0)==q and volume.subs(t,T)>0
 return dict(Q=Q,DQ=s.diff(Q,t),C=C,A=A,alpha=alpha,beta=beta,IF=IF,volume=volume,coefficient=coefficient,IN=c*ri,OUT=ro*Q/volume,T=T,V=V,q=q,c=c,ri=ri,ro=ro,places=places,kind=kind)
def source_check(g,k):
 src=json.loads((ROOT/f'generate/runs/current/sources/{k}.json').read_text())['record'][':knowledge-point/questions']
 cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());nfields=nvalues=nkeys=nsolutions=slashes=0
 for case in cases:
  original=next(q for q in src if q.get(':question/math-academy-id')==case['source_id'] or q[':db/id']==case['source_id'])
  got=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile'))['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in got)==(key in original),(k,case,key)
   if key!=':question/answer-fields' and key in got:assert got[key]==(original[key].get(':db/ident') if isinstance(original[key],dict) else original[key]),(k,case,key)
  assert len(got[':question/answer-fields'])==len(original[':question/answer-fields'])
  for a,b in zip(original[':question/answer-fields'],got[':question/answer-fields']):
   for key in (':answer-field/key',':answer-field/type'):assert (a[key].get(':db/ident') if isinstance(a[key],dict) else a[key])==b[key]
   def bank(f):return sorted((x[':answer/type'].get(':db/ident') if isinstance(x[':answer/type'],dict) else x[':answer/type'],x[':answer/value']) for x in f[':answer-field/choices'])
   assert bank(a)==bank(b);nfields+=1;nvalues+=len(bank(a))
   assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
   if ':answer-field/correct' in a:
    def correct(f):
     ref=f[':answer-field/correct'];ref=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
     return next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==ref)
    assert correct(a)==correct(b);nkeys+=1
   for x in a[':answer-field/choices']:
    text=x[':answer/value'];slashes+=sum(ord(text[i])==92 and ord(text[i+1])==92 for i in range(len(text)-1))
  nsolutions+=(':question/worked-solution' in original)
 return dict(questions=len(src),fields=nfields,values=nvalues,keys=nkeys,solutions=nsolutions,actual_adjacent_backslash_pairs=slashes)
def check(k):
 g=load('kp'+str(k),ROOT/f'generate/scratch/{k}.py');source=source_check(g,k);n=choices=rows=comparisons=0;coverage=set();tasks={l:set() for l in ('easy','moderate','hard')}
 for level in tasks:
  for seed in range(18 if k==17592186229183 else 40):
   r=g.generate(level,seed+1000);q=r['question'];env=physics(k,q[':question/problem']);so=q[':question/worked-solution'];coverage.add(r['generation']['template']);tasks[level].add(r['generation']['mathematical_fingerprint'])
   field=q[':question/answer-fields'][0];bank=field[':answer-field/choices']
   answer=env['Q'] if env['kind']=='expression' else env['q'] if env['kind']=='sum' else env['alpha']-env['beta'] if env['kind']=='difference' else rounding(env['Q'].subs(t,env['T']),env['places'])
   displayed=[]
   for a in bank:
    text=a[':answer/value'].split(r'\,')[0];expr=read(text.split('=',1)[-1],env);displayed.append(expr);choices+=1
    assert (s.simplify(expr-answer)==0)==(a[':answer/id']==field[':answer-field/correct'][1]),(k,level,seed,text,answer)
   assert len(set(displayed))==5
   # Independently recreate every method-bank operation from printed data.
   V,c,ri,ro,q0,T=(env[z] for z in ('V','c','ri','ro','q','T'));alpha=env['alpha'];beta=env['beta']
   if k==17592186229181:
    rate=ri/V;model=[answer if env['kind']=='expression' else env['Q'],alpha/2+(q0-alpha/2)*s.exp(-2*rate*t),2*alpha+(q0-2*alpha)*s.exp(-rate*t/2),ri*c+(q0-ri*c)*s.exp(-rate*t),alpha-beta*s.exp(-rate*t)]
   elif k==17592186229182 and env['kind']!='amount':model=[q0,alpha,-beta,alpha-beta,alpha+q0] if env['kind']=='sum' else [alpha-beta,q0,alpha,alpha+q0,2*alpha]
   elif k==17592186229182:
    vol=env['volume'];m=ro/(ri-ro);model=[env['Q'],ri*c*V/ro+(q0-ri*c*V/ro)*s.exp(-ro*t/V),c*vol,q0*(V/vol)**m,c*vol+beta*(V/vol)**(m+1)]
   else:
    vol=env['volume'];m=ro/(ri-ro);model=[env['Q'],c*vol,c*vol+beta*(V/vol)**(m+1),c*vol+beta*(V/vol)**(m-1),c*vol-c*V*(V/vol)**m]
   if env['kind']=='amount':model=[rounding(x.subs(t,T),env['places']) for x in model]
   assert all(any(s.simplify(a-b)==0 for b in model) for a in displayed),(k,level,seed)
   for block in re.findall(r'\$\$(.*?)\$\$',so,re.S):
    block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');lhs=None
    for row in block.split(r'\\'):
     row=rate_names(row,env).replace('&','').strip().rstrip('.,')
     if '=' not in row and '≈' not in row and r'\approx' not in row:continue
     approx='≈' in row or r'\approx' in row;parts=re.split(r'=|≈|\\approx',row)
     if not parts[0].strip():parts[0]=lhs
     else:lhs=parts[0]
     if any('⟹' in z for z in parts):parts=re.split('⟹',row)[0].split('=')
     if any(r'\int' in z and (r'e}^' in z or 'e^' in z) for z in parts):
      expr=re.search(r'\\int (.*?)\\,dt',row)[1];assert s.simplify(read(expr,env)-env['coefficient'])==0;comparisons+=1;continue
     values=[read(z,env) for z in parts]
     for a in values[1:]:
      if k==17592186229183:
       # Normalize the strictly positive affine volume before simplification.
       # This also avoids expensive CAS searches over nested square-root ratios.
       volume_coordinate=s.Symbol('positive_normalized_volume',positive=True)
       raw=(values[0]-a).subs(t,volume_coordinate-env['V']/(env['ri']-env['ro']))
       diff=s.simplify(s.powsimp(s.powdenest(raw,force=True),force=True))
      else:diff=s.simplify(values[0]-a)
      if approx:assert abs(float(s.N(diff)))<=10**(-env['places'])/2+1e-10,(k,level,seed,row,diff)
      elif any(r'\int' in z for z in parts):assert s.simplify(s.diff(diff,t))==0,(k,level,seed,row,diff)
      else:assert diff==0,(k,level,seed,row,diff)
      comparisons+=1
     rows+=1
   n+=1
  print(json.dumps({'kp_id':k,'level_readback_completed':level,'records_completed':n}),flush=True)
 report=dict(status='passed',kp_id=k,source=source,normal_records=n,complete_choice_values=choices,actual_displayed_equation_rows=rows,individual_equalities=comparisons,unique_sampled_tasks={l:len(x) for l,x in tasks.items()},default_templates=sorted(coverage),script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest())
 (ROOT/f'generate/runs/current/qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
