import os,sys,json,pathlib,importlib.util,copy,re,collections,itertools,hashlib,subprocess,shutil,importlib.metadata
E=pathlib.Path(__file__).resolve().parent
B=E.parent;P=B/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy')
os.environ.update(PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets'),MPLCONFIGDIR=str(E/'mplconfig'),XDG_CACHE_HOME=str(E/'cache'))
sys.dont_write_bytecode=True;sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('review_generator',P/'17592186172039.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v): (E/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def correct(f):
 c=f[':answer-field/correct'];aid=c.get(':answer/id') if isinstance(c,dict) else c[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
coords=[(1,1),(-1,1),(-1,-1),(1,-1)];words=['first','second','third','fourth']
def inspect(r,sol=True):
 q=r.get('question',r);rhs=q[':question/problem'].split('$')[1].split('=')[1].strip().replace('{','').replace('}','')
 m=re.fullmatch(r'(-?\d*)x(\^2)?(y(\^2)?)?',rhs);assert m,rhs
 c=int(m[1]) if m[1] not in ('','-') else (-1 if m[1]=='-' else 1);a=2 if m[2] else 1;b=0 if not m[3] else (2 if m[4] else 1)
 signs=[(1 if c>0 else -1)*x**a*y**b for x,y in coords];truth=[]
 for f in q[':question/answer-fields']:
  k=f[':answer-field/key']
  assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
  if k=='None of the above':t=not any(truth)
  else:
   z=re.fullmatch(r'At every point in the (first|second|third|fourth) quadrant, the slope of the slope field is (positive|negative)',k);assert z,k
   qi=words.index(z[1]);t=signs[qi]==(1 if z[2]=='positive' else -1);truth.append(t)
   if sol and 'Statement “' in q[':question/worked-solution']:
    block=q[':question/worked-solution'].split('Statement “'+k+'” is ')[1].split('\n\n- Statement')[0].split('\n\nTherefore')[0]
    assert block.startswith(str(t).lower()+'.')
    assert 'f(x,y)'+('>' if signs[qi]>0 else '<')+'0.' in block
  assert correct(f)==str(t).lower(),(q[':question/id'],k,t)
 assert len(truth)==3
 return dict(c=c,a=a,b=b,truth=truth,mask=sum(1<<i for i,t in enumerate(truth) if t),signs=signs)
def native(r,label):
 return {'label':label,'record':r,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==correct(f) else 'rejected','purpose':'independent sign truth; both boolean submissions'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}
source=json.loads((B/'source/source.json').read_text());batch=json.loads((B/'samples.json').read_text());save('batch.json',batch)
# Freeze original package content so every subsequent run can verify immutability.
save('package-before.json',{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()})
replays=[];grader=[]
# Parameters independently transcribed from the original eight questions above, rather than author assertions.
settings=[('bilinear_open_thin',2,1,1,[1,2,3],[1,1,1]),('parity_numbered',1,1,2,[1,2,3],[-1,-1,-1]),('bilinear_closed',6,1,1,[2,3,4],[-1,1,-1]),('bilinear_closed',-5,1,1,[1,2,4],[1,-1,1]),('parity_closed',8,2,2,[1,3,4],[-1,1,-1]),('bilinear_open',-1,1,1,[1,2,4],[1,1,-1]),('bilinear_open',9,1,1,[1,2,4],[-1,-1,1]),('parity_open',-4,1,2,[1,2,4],[-1,1,-1])]
def bank(q):return sorted((f[':answer-field/key'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),correct(f)) for f in q[':question/answer-fields'])
for q,conf in zip(source['material']['kp'][':knowledge-point/questions'],settings):
 t,c,a,b,qs,cs=conf;p=dict(c=c,a=a,b=b,quadrants=qs,claims=cs);r=g.generate('moderate' if a==b==1 else 'hard',seed=713,template=t,parameters=p,profile='bank'+q[':question/math-academy-id'].split('-')[1],include_none=any(f[':answer-field/key']=='None of the above' for f in q[':question/answer-fields']))
 inspect(r);assert r['question'][':question/problem']==q[':question/problem'];assert bank(r['question'])==bank(q)
 assert r['question'][':question/worked-solution'].replace('$','')==q[':question/worked-solution'].replace('$','')
 replays.append({'source_id':q[':question/id'],'parameters':p,'record':r,'prompt_exact':True,'bank_exact':True,'solution_exact':r['question'][':question/worked-solution']==q[':question/worked-solution'],'correction':'math delimiters for compact solution' if t=='parity_numbered' else None});grader.append(native(r,'source '+q[':question/id']))
save('source-replays.json',replays)
# Fresh seed set per recognizable template, plus cold-asset coverage in other bands.
records=[]
for t,(level,*_) in g.TEMPLATES.items():
 for seed in range(811,835):
  r=g.generate(level,seed=seed,template=t);inspect(r);assert r==g.generate(level,seed=seed,template=t);records.append(r)
save('samples-all.json',records);save('samples-moderate.json',[r for r in records if r['generation']['level']=='moderate'])
# Controlled relevant and irrelevant perturbations: visible claims, equation and solution all independently checked.
p=dict(c=3,a=1,b=1,quadrants=[1,2,3],claims=[1,-1,-1]);pairs=[]
base=g.generate('moderate',seed=997,parameters=p)
for name,new,expected in [('coefficient_sign',p|{'c':-3},[False,False,True]),('claim_sign',p|{'claims':[-1,-1,-1]},[False,True,False]),('target',p|{'quadrants':[4,2,3]},[False,True,False]),('positive_rescaling',p|{'c':9},[True,True,False])]:
 r=g.generate('moderate',seed=997,parameters=new);assert inspect(r)['truth']==expected;pairs.append({'change':name,'before':base,'after':r,'expected_after':expected,'result':'passed'});grader.extend([native(base,name+' before'),native(r,name+' after')])
save('counterfactuals.json',pairs)
# All truth masks explicitly for each template/power profile; construction must not reject valid assignments.
decision=[]
for t,(level,*_) in g.TEMPLATES.items():
 powers=[(1,0)] if level=='easy' else [(1,1)] if level=='moderate' else [(1,2)] if t=='parity_numbered' else [(1,2),(2,1),(2,2)]
 for a,b in powers:
  for mask in range(8):
   qs=[4,2,1];ss=[x**a*y**b for x,y in coords];claims=[ss[q-1]*(1 if mask>>i&1 else -1) for i,q in enumerate(qs)]
   r=g.generate(level,seed=127,template=t,parameters=dict(c=9,a=a,b=b,quadrants=qs,claims=claims));assert inspect(r)['mask']==mask;decision.append(r)
save('decision-records.json',decision)
# Explicit invalids and boundaries; record actual exception type and replay.
reject=[]
for delta in [{'c':0},{'c':10},{'c':True},{'a':2},{'quadrants':[1,1,3]},{'claims':[0,1,-1]}]:
 try:g.generate('moderate',parameters=p|delta)
 except ValueError as e:reject.append({'parameters':p|delta,'rejected':str(e)})
 else:raise AssertionError(delta)
for c in [-9,-1,1,9]:inspect(g.generate('moderate',parameters=p|{'c':c}))
save('rejection.json',reject)
for i,r in enumerate(batch+records+decision):inspect(r);grader.append(native(r,'sample '+str(i)))
save('native-input.json',grader)
# Captured inventory is inspected independently for keys, including unselectable empty cases.
inv=json.loads((B/'source/inventory.json').read_text());audit=[]
for q in inv['questions']:
 d=inspect(q,False);audit.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'math_keys_correct':True,'mask':d['mask'],'empty_without_none':d['mask']==0 and not any(f[':answer-field/key']=='None of the above' for f in q[':question/answer-fields'])})
save('inventory-audit.json',{'basis':inv['basis'],'results':audit})
save('math-results.json',{'source_replays':len(replays),'fresh_seeded_records':len(records),'explicit_decision_records':len(decision),'counterfactual_pairs':len(pairs),'exact_batch':len(batch),'all_visible_math_and_keys_correct':True,'inventory_checked':len(audit),'rejected_invalids':len(reject)})
# Relocate manifest-only runtime under evidence root. Historical unresolved scripts import is inspected in its original entrypoint.
manifest=json.loads((P/'package.json').read_text());D=E/'relocated';D.mkdir(exist_ok=True)
for n in manifest['files']:shutil.copyfile(P/n,D/n)
versions={'python':'.'.join(map(str,sys.version_info[:3])),'packages':{n:importlib.metadata.version(n) for n in manifest['dependencies']['packages']}};assert versions==manifest['dependencies']
runs=[]
for level in ['easy','moderate','hard']:
 cmd=[sys.executable,str(D/manifest['entrypoint']),'--difficulty',level,'--seed','983','--count','5','--format','json'];env=dict(os.environ,PYTHONPATH='');proc=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=E);assert proc.returncode==0,proc.stderr
 again=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=E);assert proc.stdout==again.stdout;out=json.loads(proc.stdout);save('relocated-'+level+'.json',out);runs.append({'command':cmd,'exit_code':0,'replay_equal':True})
save('packaging.json',{'versions':versions,'relocated_runs':runs,'history':'No retained findings. repair-preflight.json absent. Legacy scripts import failure repaired by local generator_policy and plot_renderer imports.','external_assets':str(E/'assets')})
(E/'session-state.md').write_text('Completed independent source replays (8), fresh seeded sampling, explicit truth cases, controlled pairs, mathematical/key and captured inventory checks, invalid inputs and manifest-only relocation. Next: shared delivery, native grader, renderer and selection/probe analysis.\n')
print(json.dumps(json.loads((E/'math-results.json').read_text())))
