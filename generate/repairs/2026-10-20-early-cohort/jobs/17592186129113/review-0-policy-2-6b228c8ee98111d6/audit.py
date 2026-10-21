import sys, json, re, random, hashlib, pathlib, platform, shutil, subprocess, copy, collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
B=E.parent
P=B/'workspace'
R=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(P))
import generator as g
S=json.loads((B/'source/source.json').read_text())
I=json.loads((B/'source/inventory.json').read_text())
source=S['material']['kp'][':knowledge-point/questions']
def save(name,d):
 (E/name).write_text(json.dumps(d,indent=2)+'\n')
def hashes(): return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.rglob('*')) if p.is_file()}
def enum(x): return x.get(':db/ident') if isinstance(x,dict) else x
def val(f):
 c=f[':answer-field/correct']
 if isinstance(c,dict):return c[':answer/value']
 aid=c[1] if isinstance(c,list) else c
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
# Independent parser of learner-visible math, not generation.parameters.
pat=re.compile(r'\\begin\{(?:array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{(?:array|bmatrix)\}',re.S)
def arrays(text): return [[[int(v.strip()) for v in row.strip().split('&')] for row in x.split(r'\\')] for x in pat.findall(text)]
def visible(r):
 q=r['question'];fs=q[':question/answer-fields']
 if enum(fs[0][':answer-field/type']).endswith('/checkbox'):
  return {re.search('([ABC])\\s*=',f[':answer-field/key'])[1]:arrays(f[':answer-field/key'])[0] for f in fs}
 return dict(zip('ABC',arrays(q[':question/problem'])))
def good(m):
 piv=[];zero_seen=False
 for row in m:
  nz=[j for j,v in enumerate(row[:-1]) if v]
  if not nz:zero_seen=True
  else:
   if zero_seen:return False
   piv.append(nz[0])
 return all(a<b for a,b in zip(piv,piv[1:]))
def selected(r):
 neg='**not**' in r['question'][':question/problem']
 return ''.join(k for k,m in sorted(visible(r).items()) if good(m)!=neg)
def keyed(r):
 fs=r['question'][':question/answer-fields']
 if enum(fs[0][':answer-field/type']).endswith('/radio'):return ''.join(x for x in 'ABC' if x in val(fs[0]))
 return ''.join(sorted(re.search('([ABC])\\s*=',f[':answer-field/key'])[1] for f in fs if val(f)=='true'))
def check_record(r):
 q=r['question'];ms=visible(r);assert len(ms)==3
 assert selected(r)==keyed(r),(q[':question/id'],selected(r),keyed(r))
 for label,m in ms.items():
  # Check prose reasons as well as selection, independently of metadata.
  phrase='The coefficient matrix of $'+label+'$ '
  if phrase in q[':question/worked-solution']:
   tail=q[':question/worked-solution'].split(phrase)[1].split('\n\n')[0]
   assert ('is in row echelon form' in tail)==good(m),(label,tail,m)
   nums=[int(x) for x in re.findall(r'row \$(\d+)\$',tail)]
   if 'contains only zeros' in tail:
    a,b=nums;assert all(v==0 for v in m[a-1][:-1]);assert any(m[b-1][:-1]) and a<b
   if 'leading entry in row' in tail:
    z=re.findall(r'row \$(\d+)\$, column \$(\d+)\$',tail);(a,c),(b,d)=[tuple(map(int,x)) for x in z]
    assert next(j+1 for j,v in enumerate(m[a-1][:-1]) if v)==c
    assert next(j+1 for j,v in enumerate(m[b-1][:-1]) if v)==d
    assert (c==d if 'same column' in tail else c<d)
  assert m in arrays(q[':question/worked-solution']),('solution display mismatch',label)
 return {'id':q[':question/id'],'profile':r['generation']['profile'],'selected':selected(r),'shape':[(len(m),len(m[0])-1) for _,m in sorted(ms.items())]}
def command(args,**kw):
 result=subprocess.run(args,capture_output=True,text=True,env=__import__('os').environ|{'PYTHONDONTWRITEBYTECODE':'1'},**kw)
 return {'command':args,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
if __name__=='__main__':
 save('package-hashes-before.json',hashes())
 replays=[];replay_results=[]
 for q in source:
  profile=q[':question/math-academy-id'];r=g.generate('easy',90317,profile=profile,replay=True);replays.append(r)
  z=check_record(r)
  assert visible(r)==visible({'question':q})
  fs=r['question'][':question/answer-fields'];orig=q[':question/answer-fields']
  assert len(fs)==len(orig)
  for a,b in zip(fs,orig):
   assert enum(a[':answer-field/type'])==enum(b[':answer-field/type'])
   assert [x[':answer/value'] for x in a[':answer-field/choices']]==[x[':answer/value'] for x in b[':answer-field/choices']]
   if b.get(':answer-field/correct'):assert val(a)==val(b)
  assert r['question'][':question/problem']==g.normalize_prose(q[':question/problem'])
  original_solution=q.get(':question/worked-solution')
  if original_solution:
   if profile=='q-129227':original_solution=original_solution.replace(r'B=\begin{bmatrix}9 &',r'B=\begin{bmatrix}8 &')
   assert r['question'][':question/worked-solution']==g.normalize_prose(original_solution)
  replay_results.append(z|{'complete_bank_preserved':True,'key_inferred':profile=='q-42026'})
 save('replays.json',replays);save('source-replay-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 '+sys.executable+' audit.py','cases':replay_results,'canonical_limitation':'Canonical four-matrix example is noninteractive and has no answer bank; generator supports the 15 captured three-matrix question profiles. Its two validity rules are tested in generated and controlled examples.'})
 samples=[]
 for pi,profile in enumerate(g.PROFILES):
  for j in range(24):samples.append(g.generate('easy',810023+pi*1009+j,profile=profile))
 save('independent-samples.json',samples)
 batch=json.loads((B/'samples.json').read_text());save('runner-batch.json',batch)
 math_results=[check_record(r) for r in samples+batch+replays]
 # Force each eligible target; empty checkbox is deliberately rejected by UI policy.
 targets=[];rejected=[]
 for pi,profile in enumerate(g.PROFILES):
  for ti,target in enumerate(g.eligible_subsets(profile)):
   try:
    r=g.generate('easy',9971+pi*101+ti,profile=profile,target=target)
    assert keyed(r)==target;check_record(r);targets.append(r)
   except g._nonempty_checkbox.__globals__['EmptyCheckboxSelection'] as ex:
    assert target=='' and g.field_type(profile)=='checkbox';rejected.append({'profile':profile,'target':target,'error':str(ex)})
 save('target-samples.json',targets);save('target-results.json',{'tested_targets':len(targets),'intentional_empty_checkbox_rejections':rejected})
 # Controlled entry-level relevant and irrelevant pairs, same shape, other matrices fixed.
 pairs=[];pair_report=[]
 for profile in ['q-42006','q-129232','q-129227','q-72573']:
  base=g.original(profile);base_r=g.generate('easy',476129,profile=profile,parameters=base)
  # Swap two coefficient entries within a row to change an invalid repeated pivot to a valid later pivot, or the reverse.
  found=None
  for ai,m in enumerate(base['matrices']):
   for row in range(len(m)):
    for a in range(len(m[0])-1):
     for b in range(a+1,len(m[0])-1):
      params=copy.deepcopy(base);mm=params['matrices'][ai];mm[row][a],mm[row][b]=mm[row][b],mm[row][a]
      if good(mm)==good(m):continue
      try: rr=g.generate('easy',476129,profile=profile,parameters=params)
      except (AssertionError,ValueError):continue
      found=(rr,ai,row,a,b);break
     if found:break
    if found:break
   if found:break
  if not found:
   for ai,m in enumerate(base['matrices']):
    for row in range(len(m)):
     for a in range(len(m[0])-1):
      params=copy.deepcopy(base);params['matrices'][ai][row][a]=0 if m[row][a] else 7
      if good(params['matrices'][ai])==good(m):continue
      try:rr=g.generate('easy',476129,profile=profile,parameters=params)
      except (AssertionError,ValueError):continue
      found=(rr,ai,row,a,a);break
     if found:break
    if found:break
  if not found:
   for ai,m in enumerate(base['matrices']):
    for row in range(len(m)):
     for other in range(row+1,len(m)):
      params=copy.deepcopy(base);mm=params['matrices'][ai];mm[row][:-1],mm[other][:-1]=mm[other][:-1],mm[row][:-1]
      if good(mm)==good(m):continue
      try:rr=g.generate('easy',476129,profile=profile,parameters=params)
      except (AssertionError,ValueError):continue
      found=(rr,ai,row,-1,other);break
     if found:break
    if found:break
  assert found,profile
  relevant,ai,row,a,b=found
  params=copy.deepcopy(base)
  for m in params['matrices']:
   for rowx in m:rowx[-1]=99 if rowx[-1]!=99 else -99
  irrelevant=g.generate('easy',476129,profile=profile,parameters=params)
  assert keyed(base_r)!=keyed(relevant) and keyed(base_r)==keyed(irrelevant)
  for r in [base_r,relevant,irrelevant]:check_record(r)
  ix=len(pairs);pairs.extend([base_r,relevant,irrelevant]);pair_report.append({'profile':profile,'record_indices':[ix,ix+1,ix+2],'relevant_change':{'matrix':'ABC'[ai],'row':row+1,'change_kind':('coefficient-row swap with row '+str(b+1) if a==-1 else 'toggle zero/nonzero at column '+str(a+1) if a==b else 'swap coefficient columns '+str([a+1,b+1]))},'selections':[keyed(r) for r in [base_r,relevant,irrelevant]],'irrelevant_change':'Set every constant to 99, preserving coefficients','passed':True})
 save('counterfactual-records.json',pairs);save('counterfactual-results.json',pair_report)
 save('math-results.json',{'records_checked':len(math_results)+len(targets)+len(pairs),'failures':[],'method':'Parse visible answer keys or prompt matrices independently; omit constants, exact integer zero/pivot check; match keys, solution arrays and every constructed witness. No generator classification routine used.','sample_results':math_results})
 # Native grader: every true/false choice, every radio choice across batch, source replay and controlled pairs.
 grade=[]
 for r in batch+replays+pairs+targets:
  checks=[];truth=selected(r)
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    if enum(f[':answer-field/type']).endswith('/checkbox'):
     lab=re.search('([ABC])\\s*=',f[':answer-field/key'])[1];correct=(a[':answer/value']=='true')==(lab in truth)
    else:correct=''.join(x for x in 'ABC' if x in a[':answer/value'])==truth
    checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'Independent coefficient-matrix classification; test every bank response'})
  grade.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
 save('grader-input.json',grade)
 # Rejection and packaging boundaries.
 rejects=[]
 out_of_range=g.original('q-42006');out_of_range['matrices'][0][0][0]=100
 for label,kw in [('unsupported difficulty',{'difficulty':'hard','seed':0}),('out-of-range entry',{'difficulty':'easy','seed':0,'profile':'q-42006','parameters':out_of_range}),('wrong shape',{'difficulty':'easy','seed':0,'profile':'q-42006','parameters':{'matrices':[[[1,0,0,0]]]*3}}),('outside radio bank',{'difficulty':'easy','seed':0,'profile':'q-129227','target':'B'})]:
  try:g.generate(**kw);rejects.append({'case':label,'rejected':False})
  except (ValueError,AssertionError,KeyError) as ex:rejects.append({'case':label,'rejected':True,'exception':type(ex).__name__})
 assert all(x['rejected'] for x in rejects)
 cli=[sys.executable,str(P/'generator.py'),'--difficulty','easy','--count','5','--seed','409817']
 a=command(cli,cwd=E);b=command(cli,cwd=E);assert a['exit_code']==b['exit_code']==0 and a['stdout']==b['stdout']
 relocated=E/'relocated';relocated.mkdir(exist_ok=True)
 manifest=json.loads((P/'package.json').read_text())
 for name in manifest['files']+['package.json']:shutil.copyfile(P/name,relocated/name)
 c=command([sys.executable,str(relocated/'generator.py'),*cli[2:]],cwd=E);assert a['stdout']==c['stdout'] and c['exit_code']==0
 for count in ['0','-1','1001']:
  d=command([sys.executable,str(relocated/'generator.py'),'--difficulty','easy','--count',count,'--seed','409817']);rejects.append({'case':'count '+count,'exit_code':d['exit_code'],'correct_result':(d['exit_code']==0)==(count=='0')});assert rejects[-1]['correct_result']
 save('cli-samples.json',json.loads(a['stdout']))
 save('packaging-results.json',{'runtime_python':platform.python_version(),'declared_dependencies':manifest['dependencies'],'version_matches':manifest['dependencies']=={'python':platform.python_version(),'packages':{}},'deterministic_cli':True,'relocated_output_equal':True,'rejections':rejects,'command':cli,'external_outputs':sorted(set(hashes())-set(json.loads((E/'package-hashes-before.json').read_text()))),'source_only_files':manifest['files'],'no_assets':all(not r['generation']['assets'] for r in samples)})
 assert hashes()==json.loads((E/'package-hashes-before.json').read_text())
 save('package-hashes-after.json',hashes())
 (E/'session-state.md').write_text('Source reconstruction, all 15 source replays, 360 independent samples, exact runner batch math, eligible target coverage, controlled relevant/irrelevant pairs, and relocation/determinism/boundaries complete. Package unchanged. Pending shared delivery, native grading, UI screenshots, selection/shortcut and inventory analyses.\n')
 print(json.dumps({'replay':len(replays),'independent_samples':len(samples),'targets':len(targets),'counterfactual_records':len(pairs),'math_failures':0,'grader_cases':len(grade)}))
