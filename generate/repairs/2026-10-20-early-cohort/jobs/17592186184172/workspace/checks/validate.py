"""Offline regression: manifest relocation, current replay, independent visible math.
Run with the job Python; all outputs are local evidence, never runtime mutations.
"""
import argparse,copy,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
import sympy as sp
W=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('g',W/'17592186184172.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=W/'evidence'; E.mkdir(exist_ok=True)
REPO=Path('/home/jake/Developer/Course_Academy')
SOURCE=REPO/'generate/repairs/2026-10-20-early-cohort/jobs/17592186184172/source/source.json'
INV=SOURCE.with_name('inventory.json')
def save(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def val(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def columns(text):
 out=[]
 for m in re.finditer(r'\\begin\{(bmatrix|aligned)\}(.*?)\\end\{\1\}',text,re.S):
  if '&' in m[2]:continue
  entries=m[2].split(r'\\');v=[]
  for entry in entries:
   cell=re.sub(r'\{x\}_\{([123])\}',r'x\1',entry.strip())
   cell=re.sub(r'(?<=\d)(?=[abx])','*',cell)
   v.append(sp.sympify(cell,locals={x:sp.Symbol(x) for x in ['a','b','x1','x2','x3']}))
  vector=sp.Matrix(v);symbols=sorted(vector.free_symbols,key=str)
  out.extend([vector.diff(s) for s in symbols] if symbols else [vector])
 return out

def visible(r):
 q=r['question'];p=q[':question/problem'];fs=q[':question/answer-fields']
 n1,n2=map(int,re.search(r'\$(\d+)\s*\\times\s*(\d+)\$',p).groups());assert n1==n2;n=n1
 markers=list(re.finditer(r'(?<![A-Z])(I|II|III)\.\s*',p))
 if len(fs)==1:
  assert [m[1] for m in markers]==['I','II','III']
  prefix=p[:markers[0].start()]
  statements=[p[m.end():markers[j+1].start() if j<2 else len(p)].strip() for j,m in enumerate(markers)]
 else:prefix=p;statements=[f[':answer-field/key'] for f in fs]
 cols=columns(prefix)
 if cols:
  B=sp.Matrix.hstack(*cols);assert B.rows==n
  u=B.rank();rank=n-u
  given=('nullspace',str(B.T.rref()[0]))
 else:
  c,kind=re.search(r'\$(\d+)\$ (non-pivot|pivot) column',prefix).groups();c=int(c)
  rank=n-c if kind=='non-pivot' else c;u=n-rank;given=(kind,c)
 assert 0<=rank<=n
 def truth(s):
  s=s.replace('$','').replace('**','').strip()
  m=re.search(r'\\text\{(rank|nullity)\}\(A\)=(\d+)',s)
  if m:return (rank if m[1]=='rank' else u)==int(m[2])
  m=re.search(r'(\d+)-dimensional.*?\^\{?(\d+)',s)
  if m:return (rank,n)==tuple(map(int,m.groups()))
  if 'non-pivot columns' in s:return u==int(re.search(r'equal to\s*(\d+)',s)[1])
  m=re.search(r'has\s*(\d+)\s*pivot col',s)
  if m:return rank==int(m[1])
  if 'invertible' in s:return (rank<n) if re.search(r'\bnot\b',s) else (rank==n)
  if 'det(A)' in s:return rank==n if '\\ne' in s else rank<n
  if 'Col}' in s:return rank!=n if '\\ne' in s else rank==n
  raise AssertionError('Unrecognized statement '+s)
 truths=list(map(truth,statements))
 label=('None' if not any(truths) else 'I, II, and III' if all(truths) else ' and '.join(s for s,b in zip(['I','II','III'],truths) if b)+' only')
 if len(fs)==1:assert val(fs[0])==label,(r['generation'],truths,val(fs[0]))
 else:
  assert len(fs)==3 and any(truths)
  assert [val(f) for f in fs]==[str(b).lower() for b in truths],(r['generation'],statements,truths)
 sol=q[':question/worked-solution']
 if 'truths' in r['generation']['parameters']:
  # Check the displayed concrete solution, independently of generation metadata.
  facts=re.search(r'Hence \$\\text\{rank\}\(A\)=(\d+)\$ and \$\\text\{nullity\}\(A\)=(\d+)\$',sol)
  assert facts and tuple(map(int,facts.groups()))==(rank,u)
  assert f'={n}-{rank}={u}' in sol or f'={n}-{u}={rank}' in sol
  for j,(s,b) in enumerate(zip(statements,truths)):
   target=['I','II','III'][j] if len(fs)==1 else '“'+s+'”'
   assert '- Statement '+target+' is '+str(b).lower()+'.' in sol
  assert (label if len(fs)==1 else '; '.join(s for s,b in zip(statements,truths) if b)) in sol
  if cols:
   start=sol.index('independent spanning vectors');end=sol.index('Thus',start)
   solbasis=sp.Matrix.hstack(*columns(sol[start:end]))
   assert solbasis.rank()==u and sp.Matrix.hstack(*cols,solbasis).rank()==u
 for f in fs:
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(f[':answer-field/choices'])
 return {'n':n,'rank':rank,'nullity':u,'truths':truths,'given':given,'statements':statements,'semantic':str([n,given,statements])}

def native(r,label):
 visible(r)
 return {'label':label,'record':r,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all bank choices; key verified from visible math'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}

def audit(rows):
 groups={}
 for r in rows:
  t=visible(r);groups.setdefault(r['generation']['template'],[]).append(t['truths'])
 result={}
 for k,ts in sorted(groups.items()):
  patterns={str(t) for t in ts};counts={str(t):sum(t==x for x in ts) for t in ts}
  result[k]={'count':len(ts),'truth_patterns':len(patterns),'best_fixed_subset':max(counts.values()),'attempts':len(ts),'position_true_counts':[sum(t[i] for t in ts) for i in range(3)],'correct_choice_counts':sorted(set(map(sum,ts)))}
 return result

def relocation():
 manifest=json.loads((W/'package.json').read_text())
 with tempfile.TemporaryDirectory(prefix='generator-relocated-') as folder:
  d=Path(folder)
  for f in manifest['files']:
   target=d/f;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,target)
  results=[]
  for band in ['moderate','hard']:
   command=[sys.executable,'-I',str(d/manifest['entrypoint']),'--difficulty',band,'--count','5','--seed','12','--format','json']
   # Isolated mode removes even the package directory: use a standard launcher
   # with its only explicit import path set to the relocated package itself.
   command=[sys.executable,str(d/manifest['entrypoint']),'--difficulty',band,'--count','5','--seed','12','--format','json']
   env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(d/'assets')}
   a=subprocess.run(command,cwd=d,env=env,text=True,capture_output=True);assert a.returncode==0,a.stderr
   b=subprocess.run(command,cwd=d,env=env,text=True,capture_output=True);assert a.stdout==b.stdout
   rows=json.loads(a.stdout);assert len(rows)==5
   for r in rows:visible(r)
   results.append({'band':band,'count':len(rows),'deterministic':True})
  return {'status':'pass','files':manifest['files'],'results':results,'external_imports':'No repository directory on PYTHONPATH; declared files only; cwd is /tmp package'}

def main():
 before={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in json.loads((W/'package.json').read_text())['files']}
 save(E/'relocation.json',relocation())
 replay=[];rows=[];cases=[];counterfactuals=[];boundaries=[]
 for key in sorted(g.Q):
  difficulty=g.level_of(key);p=g.default_parameters(key)
  r=g.generate(difficulty,template=key,parameters=p);visible(r)
  original=g.clean(g.Q[key]);q=r['question']
  assert all(q[n]==original[n] for n in [':question/problem',':question/worked-solution',':question/difficulty'])
  for f,o in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert f[':answer-field/key']==o[':answer-field/key'] and f[':answer-field/type']==o[':answer-field/type']
   assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in o[':answer-field/choices']]
   assert val(f)==val(o)
  replay.append({'source_id':key,'question_id':g.Q[key][':question/id'],'fields':len(q[':question/answer-fields']),'choices':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'prompt_solution':'exact','banks':'complete'})
  cases.append(native(r,key+' source replay'))
  # Every source bank's permitted truth role, holding supplied data constant.
  group=[]
  for i,truths in enumerate(g.allowed_truths(key)):
   params={**p,'truths':truths}
   z=g.generate(difficulty,seed=91,template=key,parameters=params)
   t=visible(z);assert t['truths']==truths
   group.append(z);rows.append(z);cases.append(native(z,key+' truth role '+str(i)))
  assert len({str(visible(z)['truths']) for z in group})==len(group)
  assert len({str(visible(z)['given']) for z in group})==1
  assert all(len({visible(z)['truths'][i] for z in group})==2 for i in range(3))
  # An irrelevant coordinate change / scaled quantities preserves responses.
  truths=g.allowed_truths(key)[-1];base=group[-1]
  alt={**p,'truths':truths}
  if 'scale' in p:alt['scale']=3
  else:alt['diagonal']=[3 if i%2==0 else 1 for i in range(len(p['diagonal']))]
  z=g.generate(difficulty,seed=91,template=key,parameters=alt);visible(z)
  assert visible(z)['truths']==visible(base)['truths']
  cases.append(native(z,key+' irrelevant evidence'))
  counterfactuals.append({'source':key,'fixed_data_cases':len(group),'changed_decisions':True,'irrelevant_change_preserves_response':True})
  if 'scale' in p:
   n=g.n_of(q[':question/problem'])
   for c in [0,n]:
    z=g.generate(difficulty,seed=91,template=key,parameters={**p,'truths':truths,'count':c});t=visible(z)
    assert t['rank'] in [0,n];cases.append(native(z,key+' count boundary '+str(c)))
    boundaries.append({'source':key,'count':c,'rank':t['rank'],'nullity':t['nullity']})
 # Small normal-sampling check includes all profiles in each supported band.
 sampled=[]
 for band in g.SUPPORTED_LEVELS:
  z=g.batch(band,len([k for k in g.Q if g.level_of(k)==band])*3,1930)
  assert len({visible(r)['semantic'] for r in z})==len(z)
  sampled.extend(z)
  for i,r in enumerate(z):cases.append(native(r,band+' normal sample '+str(i)))
 # Change only the supplied pivot count; leave every tested claim unchanged.
 base=g.generate('moderate',template='q-34934',parameters={'scale':1})
 changed=g.generate('moderate',seed=25,template='q-34934',parameters={'scale':1,'count':4,'truths':[False,True,False]})
 assert visible(base)['statements']==visible(changed)['statements']
 assert visible(base)['truths']==[True,False,True] and visible(changed)['truths']==[False,True,False]
 assert base['question'][':question/problem'].replace('$3$ pivot columns','$4$ pivot columns')==changed['question'][':question/problem']
 save(E/'count-counterfactual-records.json',[base,changed])
 cases.extend([native(base,'fixed claims pivot count 3'),native(changed,'fixed claims pivot count 4')])
 # Close only coordinate-factor values missed by the small normal sample.
 def slots(records):
  out={}
  for r in records:
   k=r['generation']['template'];p=r['generation']['parameters'];c=out.setdefault(k,{})
   for name,v in p.items():
    if name=='diagonal':
     for i,x in enumerate(v):c.setdefault('diagonal_'+str(i),set()).add(x)
    elif name=='scale':c.setdefault('scale',set()).add(v)
  return out
 coverage=slots([c['record'] for c in cases])
 for key,fields in coverage.items():
  missing={slot:sorted({1,2,3}-vs) for slot,vs in fields.items() if vs!={1,2,3}}
  if not missing:continue
  assert g.is_vector(key)
  d=[1]*g.n_of(g.Q[key][':question/problem'])
  for slot,values in missing.items():
   assert len(values)==1
   d[int(slot.split('_')[1])]=values[0]
  z=g.generate(g.level_of(key),seed=91,template=key,parameters={'diagonal':d,'truths':g.allowed_truths(key)[-1]})
  cases.append(native(z,key+' missing coordinate-factor value'))
 coverage=slots([c['record'] for c in cases]);assert all(v=={1,2,3} for c in coverage.values() for v in c.values())
 save(E/'parameter-coverage.json',{k:{s:sorted(v) for s,v in c.items()} for k,c in coverage.items()})
 save(E/'source-replay-current.json',replay);save(E/'counterfactuals.json',counterfactuals)
 save(E/'boundary-cases.json',boundaries);save(E/'normal-sample.json',sampled)
 save(E/'controlled-records.json',rows)
 save(E/'native-input-current.json',cases)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input-current.json'),str(E/'native-report-current.json')],check=True)
 delivery_reports={}
 for band in g.SUPPORTED_LEVELS:
  input_path=E/(band+'-delivery-input.json');band_rows=[r for r in rows+sampled if r['question'][':question/difficulty']==':question.difficulty/'+band]
  save(input_path,band_rows)
  out=E/('delivery-'+band)
  subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(input_path),'--source',str(SOURCE),'--inventory',str(INV),'--difficulty',band,'--output',str(out),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math'],check=True,stdout=subprocess.PIPE,text=True)
  accepted=json.loads((out/'accepted.json').read_text());d=json.loads((out/'delivery.json').read_text())
  raw_audit=audit(band_rows);filtered_audit=audit(accepted)
  for k,metric in filtered_audit.items():
   assert metric['truth_patterns']==len(g.allowed_truths(k)),(band,k,metric)
   assert 0<min(metric['position_true_counts']) and max(metric['position_true_counts'])<metric['count']
  delivery_reports[band]={'delivery':d,'before':raw_audit,'after':filtered_audit}
  # Validate the actual normalized record/owned answer IDs used at delivery.
  accepted_cases=[native(r,'delivered '+r['generation']['template']) for r in accepted]
  save(out/'native-input.json',accepted_cases)
  subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(out/'native-input.json'),str(out/'native-report.json')],check=True)
 save(E/'pedagogical-variation.json',{'controlled_counterfactuals':counterfactuals,'delivery':delivery_reports,'generator_rejection':'Nonempty truths selected by construction; policy preserves explicit failures. No decision case is removed by batch semantic dedup; full profile truth support remains after delivery.','learner_selection':'question_selection.rs selects by difficulty weights and then a seeded member; learner history and actual live weights unavailable. No database selection was simulated.','limits':['Truth-role coverage is finite and source-bank constrained, not a guarantee about every cue.','Vector sources remain singular, demonstrated from their nonzero supplied nullspaces.','Captured inventory basis only; no live database examined.']})
 # Mutation checks show the visible witness detects stale runtime artifacts.
 for target in ['key','solution']:
  z=copy.deepcopy(rows[0])
  if target=='key':
   f=z['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
  else:z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace('Hence $\\text{rank}(A)=','Hence $\\text{rank}(A)=999')
  try:visible(z)
  except AssertionError:pass
  else:raise AssertionError('Mutation did not fail '+target)
 after={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in before};assert before==after
 save(E/'validation-current.json',{'status':'pass','source_replays':len(replay),'complete_choices_replayed':sum(x['choices'] for x in replay),'controlled_decision_records':len(rows),'count_boundaries':len(boundaries),'native_cases':len(cases),'native_checks':sum(len(c['checks']) for c in cases),'normal_sample':len(sampled),'semantic_controlled_instances':len({visible(r)['semantic'] for r in rows}),'runtime_files_unchanged':True,'mutation_controls':['stale key rejected','stale solution rejected'],'runtime_hashes':after})
 print((E/'validation-current.json').read_text())
if __name__=='__main__':main()
