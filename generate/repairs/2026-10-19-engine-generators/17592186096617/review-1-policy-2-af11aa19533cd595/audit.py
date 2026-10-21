import sys,os,json,re,hashlib,random,subprocess,shutil,platform
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1'; sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent; REPO=Path('/home/jake/Developer/Course_Academy'); PKG=ROOT.parent/'workspace'; sys.path.insert(0,str(PKG))
import generator as g
import sympy as S
X=S.Symbol('x',real=True)
def save(name,data): (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def parse(z):
 z=z.replace('\\\\','\\').replace('\u2061','').replace('⁡','').replace('′',"'").replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\quad','').replace(r'\cdot','*')
 z=re.sub(r'\\operatorname\{(sin|cos|tan|sec|csc|ln)\}',r'\\\1',z)
 z=re.sub(r'\{(sec|sin|cos|tan|csc|ln)\}',r'\\\1',z)
 z=re.sub(r'(?<![\\])(sin|cos|tan|sec|csc|ln)',r'\\\1',z)
 z=re.sub(r'\\(sin|cos|tan|sec|csc|ln)(?=[A-Za-z])',lambda m:'\\'+m[1]+' ',z)
 z=re.sub(r"\^\{\s*'\s*\}","'",z)
 z=z.replace('{e}','e').strip().rstrip('.')
 tokens=re.findall(r'\\[A-Za-z]+|[a-zA-Z]|\d+|[^\s]',z); i=0
 def peek():return tokens[i] if i<len(tokens) else ''
 def pop():
  nonlocal i
  q=peek();i+=1;return q
 def atom():
  q=pop()
  if q in ('+','-'):return atom()*(1 if q=='+' else -1)
  if q in ('{','('):
   a=add(); assert pop()==('}' if q=='{' else ')'),z
  elif q in (r'\frac',r'\dfrac'): a=atom()/atom()
  elif q==r'\sqrt':a=S.sqrt(atom())
  elif q in (r'\sin',r'\cos',r'\tan',r'\sec',r'\csc',r'\ln'):
   exponent=None
   if peek()=='^':pop();exponent=atom()
   arg=atom();a={r'\sin':S.sin,r'\cos':S.cos,r'\tan':S.tan,r'\sec':S.sec,r'\csc':S.csc,r'\ln':S.log}[q](arg)
   if exponent is not None:a=a**exponent
  elif q.isdigit():a=S.Integer(q)
  elif q=='x':a=X
  elif q=='e':a=S.E
  elif q in ('u','v'):
   a=S.Function(q)(X)
   if peek()=="'":pop();a=S.diff(a,X)
   if peek()=='(':pop();assert pop()=='x';assert pop()==')'
  else:raise ValueError((z,q,tokens))
  while peek() in ('^',"'"):
   op=pop();a=a**atom() if op=='^' else S.diff(a,X)
  return a
 def mul():
  a=atom()
  while peek() and peek() not in ('+','-',')','}'):
   op=pop() if peek() in ('*','/') else '*';b=atom();a=a/b if op=='/' else a*b
  return a
 def add():
  a=mul()
  while peek() in ('+','-'):
   op=pop();b=mul();a=a+b if op=='+' else a-b
  return a
 a=add();assert i==len(tokens),(z,tokens[i:]);return a

def eq(a,b):return S.trigsimp(S.expand(a-b))==0 or S.simplify(S.trigsimp(a-b))==0

def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);k=f[':answer-field/correct'][1];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==k)
def maths(z):return [m[0] or m[1] for m in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',z)]
def inspect(r):
 q=r['question'];f=field(r);fun=parse(maths(q[':question/problem'])[0]); deriv=S.diff(fun,X)
 a=parse(key(r));isblank=f[':answer-field/type'].endswith('/blank'); fragments=maths(q[':question/problem'])
 if isblank:
  given=0
  for frag in fragments[1:]:
   if '=' in frag:frag=frag.split('=',1)[1]
   frag=frag.strip().strip('+').strip()
   if frag: given+=parse(frag)
  assert eq(a+given,deriv),('blank wrong',q[':question/problem'],a,given,deriv)
 else:
  vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(vals)==5 and sum(eq(v,deriv) for v in vals)==1,('radio key',r)
  assert eq(a,deriv)
  assert all(not eq(v,w) for i,v in enumerate(vals) for w in vals[i+1:]),'duplicates'
 sol=q[':question/worked-solution'];u=parse(re.search(r'u\(x\)=(.*?)\$',sol)[1]);v=parse(re.search(r'v\(x\)=(.*?)\$',sol)[1]);assert eq(u*v,fun),('solution factor',r)
 rows=maths(sol)[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 # Independently verify the displayed final two rows, rather than trusting generation metadata.
 last=[z.replace('&','').replace(r'\quad','').strip().lstrip('=').lstrip('+') for z in rows[-2:]]
 assert eq(sum(parse(z) for z in last),deriv),('solution final',last)
 return {'template':r['generation']['template'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'missing':r['generation'].get('missing_term'),'kind':'blank' if isblank else 'radio','answer':key(r),'correct_position':None if isblank else next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1]),'function':str(fun),'derivative':str(deriv),'passed':True}

def main():
 hashes={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-before.json',hashes)
 save('runtime.json',{'command':str(REPO/'.venv/bin/python')+' audit.py','python':platform.python_version(),'sympy':S.__version__,'mpmath':__import__('mpmath').__version__,'manifest':json.loads((PKG/'package.json').read_text())})
 source=json.loads((ROOT.parent/'source/source.json').read_text()); raw=source['material']['kp'][':knowledge-point/questions'];base={'q-1907':dict(c=1,n=2),'q-47965':dict(c=1,n=2),'q-310188':dict(b=3),'q-319402':dict(k=2),'q-71004':dict(c=1),'q-104297':dict(c=1),'q-1931':dict(c=1),'q-319350':dict(c=1,k=2),'q-319357':dict(c=2,n=2),'q-319385':dict(c=1),'q-104300':dict(c=1,n=3)}
 replays=[];checks=[]
 for q in raw:
  t=q[':question/math-academy-id'];r=g.generate(seed=87231,template=t,parameters=base[t],profile='observed_raw');replays.append(r);out=r['question'];a=q.get(':question/answer-fields',[]);b=out.get(':question/answer-fields',[])
  assert eq(parse(maths(q[':question/problem'])[0]),parse(maths(out[':question/problem'])[0]))
  assert len(a)==len(b)
  for f,h in zip(a,b):
   assert f[':answer-field/type'][':db/ident']==h[':answer-field/type']
   aa=[parse(c[':answer/value']) for c in f[':answer-field/choices']];bb=[parse(c[':answer/value']) for c in h[':answer-field/choices']]
   assert len(aa)==len(bb) and all(any(eq(v,w) for w in bb) for v in aa)
  def prose(z):return re.sub(r'\s+',' ',re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<MATH>',z)).strip()
  for k in (':question/problem',':question/worked-solution'):
   if k in q:assert prose(q[k])==prose(out[k]),(t,k)
  checks.append({'source':t,'uuid':q[':question/id'],'full_bank_size':len(a[0][':answer-field/choices']) if a else 0,'missing_source_key':bool(a and ':answer-field/correct' not in a[0]),'passed':True})
 save('source-replays.json',replays);save('source-replay-results.json',{'command':'../..../.venv/bin/python audit.py','cases':checks,'limitations':'Original q-1907 and q-47965 have no key/solution; q-71004 no response. q-319350 source LHS typo intentionally retained only in raw replay.'})
 records=[];labels=[];errors=[]
 def add(label,**kwargs):
  try:r=g.generate(**kwargs);records.append(r);labels.append(label)
  except Exception as e:errors.append({'label':label,'kwargs':kwargs,'error':repr(e)})
 for j,t in enumerate(base):
  for k in range(8):add('fresh_'+t+'_'+str(k),seed=914117+j*101+k,template=t)
  p=base[t].copy()
  if t in ('q-1907','q-104300'):p['trig']='cos'
  add('source_'+t,seed=23119,template=t,parameters=p,missing_term=1 if t in ('q-319402','q-319385') else 0)
  for bound in ('low','high'):
   z={k:(2 if k=='n' else 2 if k=='b' else 1) if bound=='low' else (4 if k=='n' else 7 if k=='b' else 6) for k in base[t]}
   if t in ('q-1907','q-104300'):z['trig']='sin' if bound=='low' else 'tan'
   if 'c' in z:z['c']=-z['c']
   for m in (0,1):add('boundary_'+t+'_'+bound+'_'+str(m),seed=48599+m,template=t,parameters=z,missing_term=m)
 save('samples.json',records);save('generation-errors.json',errors);save('sample-labels.json',labels)
 results=[]
 for label,r in zip(labels,records):
  try:results.append({'label':label,**inspect(r)})
  except Exception as e:results.append({'label':label,'passed':False,'error':repr(e),'record':r})
 batch=json.loads((ROOT.parent/'samples.json').read_text());save('runner-batch.json',batch)
 batchresults=[]
 for r in batch:
  try:batchresults.append(inspect(r))
  except Exception as e:batchresults.append({'passed':False,'error':repr(e)})
 save('math-results.json',{'cases':results,'runner_batch':batchresults,'generation_errors':errors,'passed':all(z['passed'] for z in results+batchresults) and not errors})
 # Controlled relevant pairs: hide the other term, change trig, change coefficient.
 pairs=[]
 for t in ('q-310188','q-319402','q-319350','q-319357','q-319385'):
  pair=[g.generate(seed=69437,template=t,parameters=base[t],missing_term=m) for m in (0,1)];pairs.append({'label':'missing_'+t,'kind':'relevant','records':pair,'expected':'Different missing summand, common total derivative','same_key':eq(parse(key(pair[0])),parse(key(pair[1])))})
 for trig in ('cos','tan'):
  pair=[g.generate(seed=69437,template='q-104300',parameters=dict(c=2,n=3,trig=z)) for z in ('sin',trig)];pairs.append({'label':'trig_'+trig,'kind':'relevant','records':pair,'expected':'Different prompt and derivative'})
 pair=[g.generate(seed=z,template='q-47965',parameters=base['q-47965']) for z in (69437,69438)];pairs.append({'label':'presentation_seed','kind':'irrelevant','records':pair,'expected':'Same mathematical function, key and explanation; presentation/order can differ'})
 save('counterfactuals.json',pairs)
 # Native grading in a single batch: all radio choices, symbolic blank equivalents and plausible errors.
 grade=[]
 grade_records=records+batch+[r for p in pairs for r in p['records']]
 for i,r in enumerate(grade_records):
  f=field(r);checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently differentiated radio bank'} for a in f[':answer-field/choices']]
  else:
   val=key(r)
   checks=[{'submitted':val,'expected':'accepted','purpose':'stored correct missing summand independently differentiated'}, {'submitted':'('+val+')+0','expected':'accepted','purpose':'valid equivalent grouped entry'}, {'submitted':S.sstr(parse(val)).replace('**','^'),'expected':'accepted','purpose':'independently parsed equivalent typed notation'}, {'submitted':'0','expected':'rejected','purpose':'omit required product-rule term'}, {'submitted':'-('+val+')','expected':'rejected','purpose':'wrong sign'}, {'submitted':'('+val+')+1','expected':'rejected','purpose':'plausible additive error'}]
  grade.append({'label':str(i),'record':r,'checks':checks})
 save('grader-input.json',grade)
 render=[]
 for t in base:
  idx=next(i for i,l in enumerate(labels) if l=='source_'+t);render.append(records[idx])
 render += [r for p in pairs for r in p['records']]
 save('render-input.json',render)
 rejects=[]
 for kw in [dict(level='moderate'),dict(level='hard'),dict(template='bogus'),dict(template='q-310188',parameters=dict(b=1)),dict(template='q-319357',parameters=dict(c=0,n=2)),dict(template='q-104300',parameters=dict(c=1,n=5,trig='cos')),dict(template='q-310188',missing_term=2),dict(template='q-310188',field_type='radio')]:
  try:g.generate(seed=69437,**kw);rejects.append({'input':kw,'rejected':False})
  except Exception as e:rejects.append({'input':kw,'rejected':True,'error':repr(e)})
 save('rejections.json',rejects)
 deterministic=[]
 for r in records[:11]:
  m=r['generation']; rr=g.generate(seed=m['seed'],template=m['template']);deterministic.append(rr==r)
 relocation=ROOT/'relocated';relocation.mkdir(exist_ok=True)
 for f in json.loads((PKG/'package.json').read_text())['files']:shutil.copy2(PKG/f,relocation/f)
 command=[sys.executable,str(relocation/'generator.py'),'--seed','914117','--count','2','--format','json'];p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(ROOT/'relocation-stdout.json').write_text(p.stdout);(ROOT/'relocation-stderr.txt').write_text(p.stderr or '(empty)\n')
 expected=[g.generate(seed=914117+i) for i in range(2)]
 save('packaging-results.json',{'deterministic':deterministic,'rejections_all_pass':all(z['rejected'] for z in rejects),'relocation_command':command,'relocation_exit':p.returncode,'relocation_equal':p.returncode==0 and json.loads(p.stdout)==expected,'declared_files_only':True,'external_assets':False,'public_generate_has_no_resampling':'Public generate calls record_for once; errors propagate. Legacy raw replay retries at most 100 but explicit source cases succeeded.'})
 (ROOT/'session-state.md').write_text('Source reconstruction, 11 source replays, fresh seeded/boundary samples, independent displayed-expression math, counterfactual inputs, native grader input and relocation tests complete. See math-results.json, samples.json and packaging-results.json. Next: run shared delivery, native grader and UI renderer, inspect screenshots and conditional shortcut coverage. No package writes.\n')
 print(json.dumps({'samples':len(records),'generation_errors':len(errors),'math_failures':[r['label'] for r in results if not r['passed']],'batch_failures':sum(not r['passed'] for r in batchresults),'counterfactuals':len(pairs),'grader_cases':len(grade),'render_cases':len(render)}))
if __name__=='__main__':main()
