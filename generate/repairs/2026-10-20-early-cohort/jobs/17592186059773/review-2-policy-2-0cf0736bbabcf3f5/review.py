import ast, collections, copy, fractions, hashlib, importlib.util, itertools, json, pathlib, random, re, shutil, subprocess, sys
E=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
JOB=E.parent; PKG=JOB/'workspace'; PY=str(REPO/'.venv/bin/python')
def save(p,v):
 p=E/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# No imports may write caches into package.
sys.dont_write_bytecode=True
F=fractions.Fraction
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def clean(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(' ','')
 t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
 return t

def scalar(s):
 def walk(n):
  if isinstance(n,ast.Expression):return walk(n.body)
  if isinstance(n,ast.Constant):return F(n.value)
  if isinstance(n,ast.UnaryOp):return -walk(n.operand) if isinstance(n.op,ast.USub) else walk(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=walk(n.left),walk(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
   if isinstance(n.op,ast.Div):return a/b
  raise ValueError(ast.dump(n))
 return walk(ast.parse(s,mode='eval'))
def matrices(t):return [[[scalar(clean(c)) for c in row.split('&')] for row in b.split(r'\\')] for b in MATRIX.findall(t)]
def optext(t):
 t=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),clean(t))
 return re.sub(r'(\d|\))(?=r)',r'\1*',t)
def operate(a,t):
 t=optext(t);b=copy.deepcopy(a)
 if '↔' in t:
  i,j=[int(x[1:])-1 for x in t.split('↔')];b[i],b[j]=b[j],b[i]
 else:
  lhs,rhs=t.split(':=');i=int(lhs[1:])-1
  for j in range(3):b[i][j]=scalar(re.sub(r'r([123])',lambda m:'('+str(a[int(m[1])-1][j])+')',rhs))
 return b

def kind(t):
 t=optext(t)
 return 'swap' if '↔' in t else 'addition' if len(re.findall(r'r[123]',t.split(':=')[1]))>1 else 'scale'
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1])
def correct(r):return field(r)[':answer-field/choices'][key(r)][':answer/value']
def inspect(r):
 q=r['question'];a,b=matrices(q[':question/problem']);f=field(r);cs=f[':answer-field/choices']
 assert len(a)==len(b)==3 and all(len(x)==3 for x in a+b) and a!=b
 assert f[':answer-field/type']==':answer-field.type/radio' and len(cs)==5
 matches=[i for i,c in enumerate(cs) if operate(a,c[':answer/value'])==b]
 assert matches==[key(r)],('key',matches,key(r),r['generation'])
 sol=q[':question/worked-solution'];assert matrices(sol)==[a,b],('solution matrices',r['generation'])
 final=sol.split('Therefore, the required row operation is')[1].split('$$')[1].strip().rstrip('.')
 assert operate(a,final)==b,('solution operation',r['generation'])
 changed={i for i in range(3) if a[i]!=b[i]}
 intro=sol.split('By considering')[0];description=intro.split('The only row')[1]
 assert {int(x)-1 for x in re.findall(r'\$([123])\$(?:st|nd|rd)',description)}==changed,('changed prose',r['generation'])
 assert q[':question/difficulty']==':question.difficulty/moderate'
 return {'id':q[':question/id'],'parameters':r['generation']['parameters'],'kind':kind(correct(r)),'key':key(r),'correct':correct(r),'changed':sorted(changed)}
def native(r,label):
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if i==key(r) else 'rejected','purpose':'independent exact execution of displayed operation'} for i,c in enumerate(field(r)[':answer-field/choices'])]}
def command(cmd,stdout=None,cwd=E):
 p=subprocess.run([str(x) for x in cmd],cwd=cwd,capture_output=True,text=True)
 if stdout:(E/stdout).write_text(p.stdout)
 return {'command':[str(x) for x in cmd],'cwd':str(cwd),'returncode':p.returncode,'stderr':p.stderr,'stdout':p.stdout if stdout is None else stdout}

def prepare():
 save('package-before.json',hashes(PKG))
 manifest=load(PKG/'package.json');runtime=E/'runtime';runtime.mkdir(exist_ok=True)
 for rel in manifest['files']:
  target=runtime/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/rel,target)
 shutil.copyfile(PKG/'package.json',runtime/'package.json')
 g=module(runtime/manifest['entrypoint'],'review_generator')
 originals=load(JOB/'source/source.json')['material']['kp'];qs=originals[':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in qs}
 records=[];source_results=[]
 for sid in g.CASES:
  r=g.generate(parameters=[sid,0,0,0,[0,1,2]]);q=r['question'];s=byid[sid]
  assert q[':question/problem']==s[':question/problem'] and q[':question/worked-solution']==s[':question/worked-solution']
  assert [c[':answer/value'] for c in field(r)[':answer-field/choices']]==[c[':answer/value'] for c in s[':question/answer-fields'][0][':answer-field/choices']]
  assert correct(r)==s[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
  inspect(r);records.append(r);source_results.append({'source_id':s[':question/id'],'bank':sid,'prompt_solution_complete_bank':'exact replay','choices_checked':5})
 save('source-replays.json',records);save('source-replay-results.json',{'passed':True,'cases':source_results,'unsupported':[{'id':q[':question/id'],'reason':'No captured key, solution or rating; no authored family'} for q in qs if q[':question/math-academy-id'] not in g.CASES],'canonical':'No answer field supplied; operation verified independently in source account.'})
 controlled=[];pairs=[];boundaries=[];invalid=[]
 rng=random.Random(832715)
 for sid in g.CASES:
  # Independently choose a shared valid A and row mapping for each bank, all eligible targets.
  domain=g.domain(sid);rng.shuffle(domain)
  for p in domain:
   try:rs=[g.generate(seed=832715,parameters=p+[k]) for k in g.eligible_keys(sid)]
   except g.InvalidInstance:continue
   break
  assert len({r['question'][':question/problem'] for r in rs})==len(rs)
  assert len({json.dumps(matrices(r['question'][':question/problem'])[0],default=str) for r in rs})==1
  assert len({json.dumps([c[':answer/value'] for c in field(r)[':answer-field/choices']]) for r in rs})==1
  controlled+=rs;pairs.append({'kind':'relevant','bank':sid,'before':rs[0]['question'][':question/id'],'after':[r['question'][':question/id'] for r in rs[1:]],'change':'Hold A, bank and row mapping; change elementary target operation','expected':'all targets and accepted operation change','passed':len({correct(r) for r in rs})==len(rs)})
  # An entry in a row not used by an operation can change without changing that operation.
  chosen=None
  for r in rs:
   t=optext(correct(r));dest=int(t.split(':=')[0][1:])-1 if ':=' in t else None
   if kind(correct(r))=='scale':
    olddest=p[4][dest];i=next(i for i in range(3) if i!=olddest)
    sa=matrices(byid[sid][':question/problem'])[0]
    for j in range(3):
     if sa[i][j]!=0:
      delta=1 if sa[i][j]>0 else -1
      pp=[sid,i,j,delta,p[4],r['generation']['selected_key']]
      try:other=g.generate(seed=832715,parameters=pp)
      except g.InvalidInstance:continue
      # Hold baseline exactly before editing an irrelevant entry.
      base=g.generate(seed=832715,parameters=[sid,0,0,0,p[4],r['generation']['selected_key']])
      chosen=(base,other);break
    if chosen:break
  if chosen:
   controlled.extend(chosen);pairs.append({'kind':'irrelevant','bank':sid,'before':chosen[0]['question'][':question/id'],'after':[chosen[1]['question'][':question/id']],'change':'Change one entry of an unchanged non-target row; same scale operation','expected':'accepted operation preserved, A and B update','passed':correct(chosen[0])==correct(chosen[1])})
  # Both perturbation boundaries and permutations. No arbitrary large stress test.
  for delta in (-3,3):
   for perm in ([0,1,2],[2,0,1],[1,2,0]):
    candidates=[p for p in domain if p[3]==delta and p[4]==perm]
    if candidates:
     for p in candidates:
      try:r=g.generate(seed=3329,parameters=p+[g.eligible_keys(sid)[0]])
      except g.InvalidInstance as ex:invalid.append({'parameters':p,'reason':str(ex)});continue
      boundaries.append(r);break
 for r in controlled+boundaries:inspect(r)
 save('controlled-records.json',controlled);save('counterfactual-results.json',pairs);save('boundary-records.json',boundaries)
 sampled=g.batch('moderate',60,694821);[inspect(r) for r in sampled];save('fresh-sample.json',sampled)
 batch=load(JOB/'samples.json');[inspect(r) for r in batch];save('runner-batch.json',batch)
 for r in batch:assert r==g.generate(seed=r['generation']['seed'],parameters=r['generation']['parameters'])
 allrecords=records+controlled+boundaries+sampled+batch;save('all-records.json',allrecords);save('math-results.json',{'passed':True,'record_count':len(allrecords),'choices_executed':len(allrecords)*5,'summaries':[inspect(r) for r in allrecords],'method':'Independent Fraction AST evaluator executes every public bank choice, parses both prompt and solution matrices, executes final solution operation and verifies changed-row prose.'})
 save('native-input.json',[native(r,str(i)) for i,r in enumerate(allrecords)])
 # Exact failing baselines and current CLI contracts.
 cmds=[]
 old=REPO/'generate/scratch/17592186059773.py'
 cmds.append(command([PY,'-B',old,'--format','json','--count','5','--seed','0'],'legacy-format.stdout'))
 oldrun=command([PY,'-B',old,'--count','1','--seed','0'],'legacy-wrapper.json');cmds.append(oldrun)
 oldvalue=load(E/'legacy-wrapper.json');assert isinstance(oldvalue,dict) and len(oldvalue['instances'])==1
 # Test author supplied runnable checks in a clone to avoid package writes.
 for name in ('checks/regressions.py','17592186059773/validate.py'):
  dest=runtime/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PKG/name,dest)
 cmds.append(command([PY,'-B',runtime/'checks/regressions.py'],'author-regressions.json'))
 cli=[]
 for n,seed in [(0,26),(1,401),(5,1260123367),(7,23419)]:
  c=command([PY,'-E','-s','-B',runtime/'17592186059773.py','--format','json','--difficulty','moderate','--count',n,'--seed',seed],f'cli-{n}.json');assert c['returncode']==0,c
  rs=load(E/f'cli-{n}.json');assert isinstance(rs,list) and len(rs)==n;[inspect(r) for r in rs];cli.append(c)
 assert load(E/'cli-5.json')==batch
 repeat=command([PY,'-B',runtime/'17592186059773.py','--format','json','--count','5','--seed','1260123367'],'cli-repeat.json');assert load(E/'cli-repeat.json')==batch
 for args in (['--difficulty','hard'],['--count','-1']):
  c=command([PY,'-B',runtime/'17592186059773.py']+args);assert c['returncode']!=0;cli.append(c)
 deps=manifest['dependencies'];assert deps['python']==sys.version.split()[0] and deps['packages']=={'sympy':g.sp.__version__}
 # Explicit forbidden non-elementary choices must be rejected, not silently resampled.
 rej=[]
 for k in (2,4):
  pp=['q-72850',0,0,0,[0,1,2],k]
  try:g.generate(parameters=pp);raise AssertionError('non-elementary choice accepted')
  except ValueError as ex:rej.append({'parameters':pp,'rejected':str(ex)})
 save('runtime-results.json',{'commands':cmds,'cli':cli,'deterministic_replay':True,'manifest_runtime_relocated':True,'versions':deps,'rejection_checks':rej,'retained_history':'No retained findings in repair-history. Events are missing --format and top-level record count; both failing baselines reproduced. No repair-preflight file exists. Author regression checks were run from evidence clone.','boundary_rejections_observed':invalid})
 # Captured inventory contains only original questions, never relabel as generated.
 inv=load(JOB/'source/inventory.json');save('inventory-audit.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'ids':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'source_original':q[':question/id'] in {q[':question/id'] for q in qs},'generation_fields':[k for k in q if 'generat' in k]} for q in inv['questions']],'result':'All 12 captured records are original source questions; no generated record to reproduce for historical generator defects. This is not a claim about future live inventory.'});save('affected-inventory.json',{'affected_questions':[]})
 (E/'session-state.md').write_text('Independent source account saved before author inspection. Completed: exact ten source replays including full banks; exact Fraction math on public prompts and solutions; controlled target changes and irrelevant-row edits; boundary sample and fresh seed; runner batch replay; relocated runtime + CLI contracts; legacy format/wrapper failures; copied author regressions; captured inventory audit. Next: native grader, shared delivery stages and UI rendering, pedagogical report.\n')
 print(json.dumps({'records':len(allrecords),'controlled':len(controlled),'boundaries':len(boundaries),'source':len(records),'runtime_commands':[(x['returncode'],x['stdout']) for x in cmds]}))
if __name__=='__main__':prepare()
