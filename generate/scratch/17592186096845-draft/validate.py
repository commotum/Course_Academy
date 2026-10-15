"""Independent readback of actual rendered expressions, source bytes and native grading.

No generator model, srepr intermediates or parameter recipes supply derivatives.
Prompt and displayed function definitions are parsed before differentiation.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(p,n):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'g');F=load(HERE/'source-fidelity.py','F');F.R=ROOT/'generate/runs/current'
x=s.Symbol('x',real=True);t=s.Symbol('t',real=True);a=s.Symbol('a',positive=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
def save(n,o):(HERE/n).write_text(json.dumps(o,indent=2,ensure_ascii=False,default=str)+'\n')

@lru_cache(None)
def expr(raw):
 raw=raw.strip().rstrip('.,;').replace('\u2061','').replace('−','-')
 raw=re.sub(r'\\operatorname\{(sin|cos|tan|sec|ln)\}',r'\\\1',raw)
 raw=re.sub(r'\{(sin|cos|tan|sec)\}',r'\\\1',raw)
 raw=raw.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\qquad','').replace(r'\log',r'\ln')
 raw=re.sub(r'\s+','',raw)
 def group(z,i):
  if i>=len(z):raise ValueError('Missing command argument: '+raw)
  if z[i] in '{(':
   opening=z[i];close='}' if opening=='{' else ')';depth=1;j=i+1
   while j<len(z) and depth:depth+=int(z[j]==opening)-int(z[j]==close);j+=1
   if depth:raise ValueError('Unclosed expression: '+raw)
   return convert(z[i+1:j-1]),j
  mat=re.match(r'\d+|[xate]',z[i:])
  if not mat:raise ValueError('Invalid argument '+z[i:]+' in '+raw)
  j=i+len(mat.group());return mat.group(),j
 def argument(z,i):
  if z[i] in '{(':return group(z,i)
  # Bare function arguments in this source are monomials, including coefficient
  # and power. No following product or additive term belongs to that argument.
  match=re.match(r'(?:\d+)?(?:[xat](?:\^\{[^{}]+\}|\^\d+)?|\d+)',z[i:])
  if not match:raise ValueError('Bad bare function argument '+raw)
  j=i+len(match.group());return convert(match.group()),j
 def convert(z):
  out=[];i=0
  while i<len(z):
   if z[i]=='\\':
    mat=re.match(r'\\(frac|sqrt|sin|cos|tan|sec|ln|pi)',z[i:])
    if not mat:raise ValueError('Unsupported command '+z[i:]+' in '+raw)
    cmd=mat.group(1);i+=len(cmd)+1
    if cmd=='pi':
     if out and out[-1][-1] not in '+-*/':out.append('*')
     out.append('pi');continue
    power=None
    if i<len(z) and z[i]=='^':power,i=group(z,i+1)
    if cmd=='frac':num,i=group(z,i);den,i=group(z,i);term='(('+num+')/('+den+'))'
    elif cmd=='sqrt':num,i=group(z,i);term='sqrt('+num+')'
    else:num,i=argument(z,i);term=('log' if cmd=='ln' else cmd)+'('+num+')'
    if out and out[-1][-1] not in '+-*/':out.append('*')
    out.append('('+term+')**('+power+')' if power else term)
   elif z[i] in '{(':v,i=group(z,i);out.append('('+v+')')
   elif z[i]=='^':v,i=group(z,i+1);out.append('**('+v+')')
   else:
    if z[i] not in 'xate0123456789.+-*/':raise ValueError('Unsupported token '+z[i:]+' in '+raw)
    out.append(z[i]);i+=1
  return ''.join(out)
 parsed=parse_expr(convert(raw),local_dict={'x':x,'t':t,'a':a,'e':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'sqrt':s.sqrt,'log':s.log},transformations=TRANS)
 assert parsed.free_symbols.issubset({x,t,a}),('Unexpected parsed symbols',parsed,raw)
 return parsed

@lru_cache(None)
def eq(u,v):
 d=s.powdenest(u,force=True)-s.powdenest(v,force=True)
 if d==0:return True
 if d.is_polynomial(x,t,a):return s.expand(d)==0
 # Positive-domain real radical and log samples. A nonzero value disproves
 # identity but is never alone taken to prove equivalence.
 for z in (s.pi/4,s.pi/6):
  val=d.subs({x:z,t:z,a:2})
  if val.has(s.nan,s.zoo,s.oo):continue
  if abs(complex(val.evalf()))>1e-20:return False
 return s.simplify(s.trigsimp(d))==0

def top_sum(raw):
 depth=0;parts=[];start=0
 for i,ch in enumerate(raw):
  if ch in '({':depth+=1
  if ch in ')}':depth-=1
  if ch=='+' and depth==0:parts.append(raw[start:i]);start=i+1
 parts.append(raw[start:]);return parts

def prompt_function(q):
 maths=re.findall(r'\$([^$]+)\$',q[':question/problem'])
 for math in maths:
  z=math.strip()
  if z.startswith(('y=','y =','f(x)=')):
   return expr(z.split('=',1)[1].rstrip(','))
 raise AssertionError('Prompt omits supplied function')

def read_solution(q,df,variable=x):
 sol=q[':question/worked-solution'];opening=sol.split('Then')[0]
 defs=re.findall(r'\$([ug]\('+str(variable)+r'\)=.*?)\$',opening)+re.findall(r'\$([vh]\('+str(variable)+r'\)=.*?)\$',opening)
 assert len(defs)==2,('Product definitions',defs)
 u=expr(defs[0].split('=',1)[1]);v=expr(defs[1].split('=',1)[1]);assert eq(u*v,df),'Both product factors agree with supplied function'
 names=(defs[0][0],defs[1][0]);du=s.diff(u,variable);dv=s.diff(v,variable);derivative=s.diff(df,variable)
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);prime=blocks[0]
 pair=prime.split(r',\,') if r',\,' in prime else prime.split(r', \qquad')
 assert len(pair)==2,prime
 for row,name,expected in zip(pair,names,(du,dv)):
  lhs,rhs=row.split('=',1);label=re.sub(r'[{}]','',lhs).replace('′',"'").replace('^', '').strip();assert label==name+"'("+str(variable)+')',('Prime input label',label)
  assert eq(expr(rhs),expected),('Displayed individual derivative',row,expected)
 aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(aligned)>=1
 rows=aligned[0].split(r'\\');assert len(rows)>=3
 if names[0]=='g':
  first=rows.pop(0);assert re.sub(r'[{}\s]','',first).replace('′',"'").replace('^','')=="a_2(t)&=v_2'(t)",('Acceleration derivative label',first)
 lhs,rhs=rows[0].split(' & =',1)
 formal=re.sub(r'[{}\s]','',rhs).replace('′',"'").replace('^', '')
 expected=names[0]+"'("+str(variable)+')'+r'\cdot'+names[1]+'('+str(variable)+')+'+names[0]+'('+str(variable)+')'+r'\cdot'+names[1]+"'("+str(variable)+')'
 assert formal==expected,('Ordered product rule',formal,expected)
 subs=rows[1].split(' & =',1)[1];summands=top_sum(subs);assert len(summands)==2
 assert eq(expr(summands[0]),du*v) and eq(expr(summands[1]),u*dv),'Both displayed product summands'
 for row in rows[1:]:assert eq(expr(row.split(' & =',1)[1]),derivative),('Displayed simplification',row)
 return u,v,derivative

def read_normal(rec):
 q=rec['question'];md=rec['generation'];df=prompt_function(q);f=q[':question/answer-fields'][0]
 assert q[':question/problem'].count('{{'+f[':answer-field/key']+'}}')==(1 if f[':answer-field/type'].endswith('/blank') else 0),'Field key matches actual printed blank'
 assert md['eligible_for_learning'] and not md['evidence_only']
 assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 assert ':question/math-academy-id' not in q and ':db/id' not in q
 derivative=s.diff(df,x);values=[expr(v[':answer/value']) for v in f[':answer-field/choices']]
 ci=next(i for i,v in enumerate(f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][1]);answer=values[ci]
 if f[':answer-field/type'].endswith('/blank'):
  # Read the supplied exponential outside the blank from the actual prompt.
  suffix=q[':question/problem'].split('{{'+f[':answer-field/key']+'}}',1)[1]
  factor=expr(re.search(r'\$\)(.*)\$',suffix).group(1));assert eq(answer*factor,derivative),'Reassembled printed blank fragment'
 else:assert eq(answer,derivative),'Correct key independent differentiation'
 assert sum(eq(v,answer) for v in values)==1
 assert all(not eq(v,w) for i,v in enumerate(values) for w in values[i+1:]),'Whole rendered bank ambiguous'
 u,v,sd=read_solution(q,df);assert eq(sd,derivative)
 # Independently infer source recipe inputs from rendered product definitions;
 # no generator bank/model or metadata parameters participate in these checks.
 m=md['template'];expected_bank=None
 if m=='q-11824':
  k=s.diff(v.args[0],x);expected_bank=[(k*x+1)*v,derivative,(x+1)*v,k*x*v,k*(x+1)*v]
 elif m=='q-2392':
  k=s.diff(v.exp,x);expected_bank=[derivative,v*(s.sec(x)**2+k*s.tan(x)),v*s.sec(x)**2+k*s.tan(x),k*v*(s.sec(x)**2+s.log(a)*s.tan(x)),k*s.sec(x)**2+k*v*s.tan(x)]
 elif m=='q-9942':
  k=s.diff(v.args[0],x);phase=v.args[0];expected_bank=[2*x**2*s.sin(phase)+k*x*s.cos(phase),2*x*s.sin(phase)+x**2*s.cos(phase),2*s.sin(phase)+k*x**2*s.cos(phase),derivative,k*x*s.sin(phase)+2*x**2*s.cos(phase)]
 elif m=='q-2401':
  c=s.expand(u).coeff(x,2);expected_bank=[(c*s.Rational(1,4)*x*s.cos(x)+c*s.Rational(1,2)*x*s.sin(x))/s.sin(x),c*s.Rational(1,2)*x**2*s.sin(x)/s.sqrt(s.sin(x))-c*s.Rational(1,4)*x*s.sqrt(s.sin(x)),(c*s.Rational(1,2)*x**2*s.sin(x)-2*c*x*s.sin(x))/s.sqrt(s.sin(x)),derivative,-c*s.Rational(1,2)*x**2*s.cos(x)/s.sqrt(s.cos(x))+2*c*x*s.sqrt(s.sin(x))]
 elif m=='q-11599':
  inner=v.base;k=s.expand(inner).coeff(x,2);b=inner.subs(x,0);expected_bank=[(6*k*x**4+b*x**2)*inner**2,(6*k*x**4+3*b*x**2)*inner**2,(9*k*x**4+3*b*x**2)*inner**3,derivative,(3*b*x**4+6*k*x**2)*inner**2]
 if expected_bank is not None:
  assert len(expected_bank)==len(values)
  assert all(sum(eq(v,w) for w in values)==1 for v in expected_bank),('Every complete source error recipe from displayed factors',m)
 assert ('chain rule to differentiate $u' in q[':question/worked-solution'])==(md['template']=='q-343333'),'Correct chain factor referenced in prose'
 key=f[':answer-field/key'];assert q[':question/problem'].count('{{'+key+'}}')==(1 if f[':answer-field/type'].endswith('/blank') else 0)
 assert len(set(v[':answer/id'] for v in f[':answer-field/choices']))==len(values)
 assert md['domains']==g.domain(md['template'])
 for text in (q[':question/problem'],q[':question/worked-solution'],*[v[':answer/value'] for v in f[':answer-field/choices']]):
  assert all(ord(c)>=32 or c in '\n\t' for c in text) and text.count('$')%2==0
 assert rec==g.generate(md['level'],md['seed'],template=md['template'],parameters=md['parameters'],profile=md['profile'])
 return {'function':s.srepr(df),'derivative':s.srepr(derivative),'factors':[s.srepr(u),s.srepr(v)],'answer':s.srepr(answer),'choice_count':len(values)}

def native_checks(rec):
 q=rec['question'];f=q.get(':question/answer-fields',[{}])[0]
 if ':answer-field/correct' not in f:return []
 if f[':answer-field/type'].endswith('/radio'):return [{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Native selection grading for every field-owned answer ID'} for v in f[':answer-field/choices']]
 value=next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);equiv='2('+value+')/2'
 return [{'field_index':0,'submitted':v,'expected':e,'purpose':purpose} for v,e,purpose in [(value,'accepted','Canonical rendered blank'),(equiv,'accepted','Unreduced equivalent actual expression'),('0','rejected','Ordinary wrong zero'),('1','rejected','Ordinary wrong nonzero'),('('+value+')+1','rejected','Actual correct fragment plus one')]]

def failure(fn):
 try:fn()
 except (AssertionError,ValueError,StopIteration,KeyError):return
 raise AssertionError('Negative control did not fail')

def read_raw(rec):
 """Read every source mathematical component without filling public omissions."""
 q=rec['question'];m=rec['generation']['template'];findings=[]
 try:df=prompt_function(q)
 except AssertionError:
  assert m in ('q-143518','q-167572')
  sol=q[':question/worked-solution'];defs=re.findall(r'\$([gh]\(t\)=.*?)\$',sol.split('Then')[0]);assert len(defs)==2
  df=expr(defs[0].split('=',1)[1])*expr(defs[1].split('=',1)[1]);findings.append('Velocity appears only in solution; missing question context keeps this raw-only.')
 variable=t if m in ('q-143518','q-167572') else x;derivative=s.diff(df,variable)
 target_match=re.search(r'\$x\s*=\s*(.*?)\$',q[':question/problem'])
 target=expr(target_match.group(1).rstrip('.')) if target_match else None
 if ':question/worked-solution' in q:
  read_solution(q,df,variable)
  aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
  if target is not None:
   assert len(aligned)==2
   expected=s.simplify(derivative.subs(x,target))
   rows=aligned[1].split(r'\\')
   # Invert the literal point occurrence in the unreduced substitution stage.
   # This exposes stale chain inputs or factors even when evaluating at the
   # source point makes an entire summand vanish.
   substitution_index=1 if m=='q-313299' else 0
   first_rhs=rows[substitution_index].split(' & =',1)[1]
   if m in ('q-10009','q-313299'):
    restored=first_rhs.replace(target_match.group(1).rstrip('.'),'x')
   elif m=='q-9944':restored=re.sub(r'(?<![0-9])0(?![0-9])','x',first_rhs)
   elif m=='q-11602':restored=first_rhs.replace('(2)','(x)')
   elif m=='q-11603':restored=re.sub(r'\\cdot\s*1',lambda mat:r'\cdot x',first_rhs.replace('{1}','{x}'))
   else:raise AssertionError(('Unmapped source substitution stage',m))
   assert eq(expr(restored),derivative),('Source substitution factors and chain inputs before numerical cancellation',m)

   for i,row in enumerate(rows):
    rhs=row.split(' & =',1)[1]
    if 'frac{\\text{d}' in rhs:
     assert i==0 and m=='q-313299';subscript=rhs.rsplit('x=',1)[1].split('}',1)[0];assert subscript=='\\pi /4'
     continue
    assert eq(expr(rhs),expected),('Source substitution/intermediate evaluation',m,row,expected)
 answer=derivative.subs(x,target) if target is not None else derivative
 for f in q.get(':question/answer-fields',[]):
  values=[]
  for v in f.get(':answer-field/choices',[]):
   text=v[':answer/value']
   values.append(expr(text))
  expected=answer
  if m in ('q-343332','q-343333','q-343354'):
   suffix=q[':question/problem'].split('{{'+f[':answer-field/key']+'}}',1)[1];factor=expr(re.search(r'\$\)(.*)\$',suffix).group(1));expected=derivative/factor
  if ':answer-field/correct' in f:
   ci=next(i for i,v in enumerate(f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][1]);assert eq(values[ci],expected),('Source original key',m)
  if values:
   assert sum(eq(v,expected) for v in values)==1,('Unique source correct mathematical option',m)
   assert all(not eq(v,w) for i,v in enumerate(values) for w in values[i+1:]),('Raw bank equivalent options',m)
 return {'source_id':m,'function_readback':s.srepr(df),'derivative_readback':s.srepr(derivative),'substitution_point':s.srepr(target) if target is not None else None,'source_findings':sorted(set(findings))}

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());originals,counts=F.check(g,str(g.KP_ID),HERE);assert len(originals)==18
 raw=[g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']) for c in cases]
 for r in raw:
  assert r['generation']['observed_record']==g.SOURCES[r['generation']['template']]
  assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
 raw_readback=[read_raw(r) for r in raw];save('raw-rendered-readback.json',raw_readback)
 normal=[];review=[];readbacks=[];boundaries={};novelty={}
 for m in g.LEVELS:
  print('Independent rendered readback',m,flush=True)
  variants=[g.generate(g.LEVELS[m],i,template=m,parameters=p) for i,p in enumerate(g.parameter_domain(m))]
  for r in variants:readbacks.append(read_normal(r))
  normal+=variants;review += [g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m]),variants[0],variants[-1]]
  boundaries[m]={key:sorted({p[key] for p in g.parameter_domain(m)}) for key in g.DEFAULTS[m]}
  # A single-slot change, other slots held fixed, independently inspected.
  for key in g.DEFAULTS[m]:
   p=copy.deepcopy(g.DEFAULTS[m]);p[key]=next(v[key] for v in g.parameter_domain(m) if v[key]!=p[key] and {k:v[k] for k in p if k!=key}=={k:p[k] for k in p if k!=key})
   changed=g.generate(g.LEVELS[m],template=m,parameters=p);read_normal(changed);review.append(changed)
   assert changed['generation']['parameter_fingerprint']!=g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m])['generation']['parameter_fingerprint']
  for p in (g.parameter_domain(m)[0],g.parameter_domain(m)[-1]):
   r=g.generate(g.RAW_LEVELS[m],template=m,parameters=p,profile='observed_raw')
   if m!='q-11599':
    # Operative raw solution stages must remain internally consistent, too.
    df=prompt_function(r['question']);read_solution(r['question'],df)
   review.append(r)
 defaults=[]
 for l in g.SUPPORTED_LEVELS:
  rs=[g.generate(l,i) for i in range(60)];defaults+=rs
  assert {r['generation']['template'] for r in rs}=={m for m in g.LEVELS if g.LEVELS[m]==l}
  for r in rs:read_normal(r)
  novelty[l]=len({r['generation']['parameter_fingerprint'] for r in normal if r['generation']['level']==l})
 negative=0
 for m in g.LEVELS:
  base=g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m]);read_normal(base)
  other=g.generate(g.LEVELS[m],85,template=m,parameters=g.DEFAULTS[m],profile='default');assert base['question'][':question/id']==other['question'][':question/id']
  failure(lambda:g.generate(g.LEVELS[m],template=m,parameters={k:99 for k in g.DEFAULTS[m]}));negative+=1
  failure(lambda:g.generate(next(l for l in g.SUPPORTED_LEVELS if l!=g.LEVELS[m]),template=m));negative+=1
 for m in g.EXCLUSIONS:failure(lambda:g.generate(g.RAW_LEVELS[m],template=m));negative+=1
 for args in [dict(level='moderate',template='q-9942',parameters={'k':2,'b':1}),dict(level='hard',template='q-11599',parameters={'k':2,'b':4}),dict(level='easy',template='q-343332',parameters={'k':17}),dict(level='moderate',template='q-2401',parameters={'c':2}),dict(level='easy',template='q-343333',field_type='radio')]:failure(lambda:g.generate(**args));negative+=1
 base=g.generate('moderate',template='q-9942',parameters={'k':5,'b':2})
 mutations={'prompt':lambda q:q.update({':question/problem':q[':question/problem'].replace('5x+2','5x+3')}),'factor-definition':lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('v(x)=','v(t)=')}),'prime-input':lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace("{v}^{′}(x)","{v}^{′}(t)")}),'chain-factor':lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace(r'5\operatorname{cos}',r'4\operatorname{cos}')}),'summand':lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('(2x)', '(3x)')}),'intermediate-power':lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('5{x}^{2}','5{x}^{3}')}),'wrong-sign':lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('))+','))-')}),'key':lambda q:q[':question/answer-fields'][0][':answer-field/correct'].__setitem__(1,str(uuid.uuid4())),'bank':lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].update({':answer/value':'0'}),'control':lambda q:q.update({':question/worked-solution':q[':question/worked-solution']+'\x0c'})}
 for name,mutate in mutations.items():r=copy.deepcopy(base);mutate(r['question']);failure(lambda:read_normal(r));negative+=1
 blank=g.generate('easy',template='q-343354',parameters={'k':6,'c':2})
 for name in ('blank-factor','blank-label','domain'):
  r=copy.deepcopy(blank)
  if name=='blank-factor':r['question'][':question/problem']=r['question'][':question/problem'].replace('{e}^{6x}','{e}^{5x}')
  if name=='blank-label':r['question'][':question/problem']=r['question'][':question/problem'].replace('{{field-1}}','{{field-2}}')
  if name=='domain':r['generation']['domains']='x>0'
  failure(lambda:read_normal(r));negative+=1
 for m in ('q-10009','q-9944','q-313299'):
  r=g.generate(g.RAW_LEVELS[m],template=m,parameters={},profile='observed_raw');q=r['question']
  if m=='q-10009':q[':question/worked-solution']=q[':question/worked-solution'].replace('3'+r'\cdot '+r'\frac{\pi }{2}','4'+r'\cdot '+r'\frac{\pi }{2}')
  elif m=='q-9944':q[':question/worked-solution']=q[':question/worked-solution'].replace('⁡(0)','⁡(1)')
  else:q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\frac{\pi }{4}',r'\frac{\pi }{3}')
  failure(lambda:read_raw(r));negative+=1
 cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--seed','83','--format','json'],capture_output=True,text=True,check=True);out=json.loads(cli.stdout);assert len(out)==3 and [r['generation']['level'] for r in out]==list(g.SUPPORTED_LEVELS)
 engine=[{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(raw+normal) if native_checks(r)]
 save('engine-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';assert hashlib.sha256(binary.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 run=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stdout+run.stderr
 native=json.loads((HERE/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 save('review.json',{'original_raw_replays':raw,'supported_side_by_side':review,'cli_all':out});save('rendered-readback.json',readbacks)
 parts=['# Chain and product rules: private draft','All observed raw records are evidence-only. Hard rating, missing key and polynomial solution are authored; seven E/M backbones preserve their source prose and stages.']
 for r in raw:parts+=['## Original MA '+r['generation']['template'],g.markdown(r)]
 for r in review:parts+=['## '+('Changed raw evidence' if r['generation']['evidence_only'] else 'Eligible generated variant')+' / '+r['generation']['level']+' / '+r['generation']['template'],g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
 baseline=json.loads((HERE/'registered-baseline.json').read_text());actual=[ROOT/'generate/scratch/17592186096845.py']+sorted(p for p in (ROOT/'generate/scratch/17592186096845').rglob('*') if p.is_file());assert set(baseline)=={str(p) for p in actual};assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items())
 inv=json.loads((HERE/'independent-inventory.json').read_text());assert [r['record'] for r in inv['questions']]==[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 report={'status':'pass','draft_only':True,'source_basis':2275,'source_lineage':g.LINEAGE,'source_fidelity':counts,'independent_inventory_exact':len(inv['questions']),'correctness':{'exhaustive_rendered_records':len(normal),'independent_prompt_factors_primes_product_summands_all_intermediate_equalities_keys_complete_banks_and_blank_reassembly':True,'per_slot_boundary_values':boundaries,'meaningful_tasks_per_level':novelty,'negative_controls':negative,'raw_only_exclusions':g.EXCLUSIONS},'grading':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'preserved_registered_files':len(baseline),'registered_baseline_unchanged':True,'hard_difficulty_authored':True,'limits':['Hard is authored from an unrated source; no captured hard example or difficulty label.','Ten source templates are explicitly raw-only: missing field contracts, unavailable multipart context or unresolved finite slope distractor mechanisms.','The radical source bank includes a wrong expression with sqrt(cos(x)); its cos(x)>0 domain is recorded separately from the actual question domain.','All real differentiation restricts ln(x) to x>0, a^(kx) to positive a and radicals to positive interiors.','Single source recipe interpretations remain inferential; exact complete expression patterns, not invented explanations, are the fidelity claim.'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'source-fidelity.py',binary]}}
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
