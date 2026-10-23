"""Executable regression for ad4d9eb2e13fc5224721; no runtime mutations/services."""
import sys,json,copy,collections,subprocess,hashlib,tempfile,shutil
from pathlib import Path
sys.dont_write_bytecode=True
import audit as a
from shortcut_regression import predict,probes
ROOT=Path(__file__).resolve().parent
m=a.m

def role_checks(records):
 groups=collections.defaultdict(list)
 for rec in records:
  a.check(rec)
  # Observable choice text and pivot, without consulting generation/key to group.
  groups[tuple(c[':answer/value'] for c in a.choices(rec))].append(rec)
 witnesses=[]
 for bank,rs in groups.items():
  if len(rs)!=5:continue
  indices={a.check(r)['correct_index'] for r in rs}
  assert indices==set(range(5)), ('fixed-bank role missing',indices)
  predictions=[predict(r) for r in rs]
  attempts=sum(p is not None for p in predictions)
  wins=sum(p==a.correctid(r) for p,r in zip(predictions,rs))
  assert attempts==0 or (attempts==5 and wins==1), (attempts,wins)
  witnesses.append({'profile':rs[0]['generation']['bank_profile'],'roles':sorted(indices),'modal_attempts':attempts,'modal_correct':wins})
 assert len(witnesses)==9, ('lost complete profile groups',len(witnesses))
 return witnesses

def main():
 if len(sys.argv)>1:
  accepted=json.loads(Path(sys.argv[1]).read_text())
  # Choose controlled cases by their matrices, surviving normalization of IDs.
  wanted={json.dumps(a.mats(r['question'][':question/problem'])) for r in json.loads((ROOT/'role-records.json').read_text())}
  roles=[r for r in accepted if json.dumps(a.mats(r['question'][':question/problem'])) in wanted]
  out={'roles':role_checks(roles),'all_accepted':probes(accepted),'semantic_instances':len({json.dumps(a.mats(r['question'][':question/problem'])) for r in accepted})}
  a.save('after-delivery.json',out)
  print(json.dumps({'accepted':len(accepted),'fixed_bank_groups':len(out['roles'])}));return
 # Preserve the exact reported minimal failure, including all 120 permutations.
 subprocess.run([sys.executable,str(ROOT/'shortcut_regression.py')],check=True)
 source=json.loads((a.JOB/'source/source.json').read_text())['material']['kp']
 replays=[];source_report=[]
 for q in source[':knowledge-point/questions']:
  A,B=a.mats(q[':question/problem']);p=next(c for c in range(3) if all(A[r][c]==B[r][c] for r in range(3)))
  cols=[c for c in range(3) if c!=p];row=next(r for r in range(3) if A[r][p] and all(A[r][c] and B[r][c]==0 for c in cols))
  ks=[-A[row][c]//A[row][p] if c!=p else 0 for c in range(3)]
  rec=m.generate(seed=761,bank_profile=q[':question/math-academy-id'],parameters={'A':A,'row':row,'pivot':p,'ks':ks})
  a.check(rec);assert a.mats(rec['question'][':question/problem'])==[A,B]
  for f in q[':question/answer-fields']:
   assert sorted(a.ops(c[':answer/value']) for c in f[':answer-field/choices'])==sorted(a.ops(c[':answer/value']) for c in a.choices(rec))
   if ':answer-field/correct' in f:
    assert a.ops(f[':answer-field/correct'][':answer/value'])==a.ops(next(c[':answer/value'] for c in a.choices(rec) if c[':answer/id']==a.correctid(rec)))
  assert a.mats(q[':question/worked-solution'])==a.mats(rec['question'][':question/worked-solution'])
  replays.append(rec);source_report.append({'id':q[':question/id'],'banks':len(q[':question/answer-fields']),'complete_bank_match':True})
 canonical=m.generate(seed=762,bank_profile='q-130609',parameters={'A':[[-6,-5,1],[8,3,-4],[9,7,-2]],'row':0,'pivot':2,'ks':[6,5,0]})
 a.check(canonical);replays.append(canonical)
 a.save('source-replays.json',replays);a.save('source-replay-results.json',source_report)
 # Independent bank objects observed at anchor (-2,3), not generator recipes.
 banks={
 'q-42917':[(-3,-2),(-2,-1),(-2,-3),(-2,3),(3,-2)],
 'q-91189':[(-1,3),(2,3),(-2,3),(-2,-3),(-3,2)],
 'q-130609':[(-2,3),(3,-2),(2,3),(-2,-3),(2,-3)],
 'q-130610':[(-2,3),(2,3),(-3,2),(-2,-3),(2,-3)],
 'q-130611':[(3,-2),(-2,3),(2,3),(-2,-3),(2,-3)],
 'q-91186':[(-6,1),(-2,3),(2,3),(-2,-3),(3,-2)],
 'q-91187':[(-2,-3),(-6,1),(-2,3),(2,3),(3,-2)],
 'q-91192':[(-2,-3),(-2,3),(3,-2),(2,3),(-6,3)],
 'q-91188':[(-2,-3),(3,2),(2,3),(3,-2),(-2,3)]}
 roles=[]
 for j,(profile,bank) in enumerate(banks.items()):
  # Same background per profile, different across profiles to prevent dedup collisions.
  for x,y in bank:
   pars={'A':[[-2*x,2,-2*y],[j-4,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[x,0,y]}
   rec=m.generate(seed=842,bank_profile=profile,parameters=pars,bank_anchor=(-2,3))
   assert a.optionpairs(rec)==bank
   roles.append(rec)
 a.save('role-records.json',roles);witnesses=role_checks(roles)
 # Native normal sampling in every retained profile. No acceptance quotas/resampling.
 normal=[m.generate(seed=6100+31*j+i,bank_profile=p) for j,p in enumerate(m.PROFILES) for i in range(12)]
 original_batch=json.loads((a.JOB/'samples.json').read_text())
 batch=[m.generate(seed=r['generation']['seed'],bank_profile=r['generation']['bank_profile']) for r in original_batch]
 a.save('repaired-batch.json',batch)
 boundary=[]
 for r in range(3):
  for p in range(3):
   A=[[2,3,5],[7,11,13],[17,19,23]];ks=[0]*3
   for c,k in zip([c for c in range(3) if c!=p],[-2,3]):ks[c]=k;A[r][c]=-k*A[r][p]
   boundary.append(m.generate(seed=61,bank_profile='q-91189',parameters={'A':A,'row':r,'pivot':p,'ks':ks},bank_anchor=(-2,3)))
 pars={'A':[[4,2,-6],[1,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[-2,0,3]}
 base=m.generate(seed=842,bank_profile='q-91189',parameters=pars)
 irrelevant=copy.deepcopy(pars);irrelevant['A'][1][0]=8
 other=m.generate(seed=842,bank_profile='q-91189',parameters=irrelevant)
 assert a.optionpairs(base)==a.optionpairs(other) and a.check(base)['coefficients']==a.check(other)['coefficients']
 pivots=[m.generate(seed=61,bank_profile='q-130609',parameters={'A':[[2,2,-4],[1,3,4],[5,-1,2]],'row':0,'pivot':p,'ks':ks}) for p,ks in [(0,[0,-1,2]),(1,[-1,0,2])]]
 assert a.mats(pivots[0]['question'][':question/problem'])[0]==a.mats(pivots[1]['question'][':question/problem'])[0]
 assert a.ops(pivots[0]['question'][':question/worked-solution'])!=a.ops(pivots[1]['question'][':question/worked-solution'])
 cf=[base,other]+pivots
 runtime=roles+normal+batch+boundary+cf
 allrows=replays+runtime
 checks=[a.check(r) for r in allrows]
 a.save('records.json',runtime);a.save('math-results.json',{'count':len(checks),'checks':checks})
 a.save('variation-results.json',{'controlled_roles':witnesses,'normal':a.summarize(normal),'normal_modal_rule':probes(normal),'counterfactuals':[a.check(r) for r in cf], 'row_pivot_coverage':[(r['generation']['parameters']['row'],r['generation']['parameters']['pivot']) for r in boundary]})
 a.save('grader-input.json',[{'label':str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if a.apply(a.mats(r['question'][':question/problem'])[0],a.ops(c[':answer/value']))==a.mats(r['question'][':question/problem'])[1] else 'rejected','purpose':'Independent integer whole-column calculation'} for c in a.choices(r)]} for i,r in enumerate(allrows)])
 a.save('render-input.json',[roles[5],roles[6],boundary[0],boundary[-1],batch[0]])
 inv=json.loads((a.JOB/'source/inventory.json').read_text());source_ids={q[':question/id'] for q in source[':knowledge-point/questions']}
 generated=[q for q in inv['questions'] if q[':question/id'] not in source_ids or any('generator' in k or 'generation' in k for k in q)]
 assert not generated
 a.save('inventory-review.json',{'basis':inv['basis'],'count':len(inv['questions']),'all_ids_match_original_source':True,'generated_records':0,'conclusion':'Verified absence of historical generated records in captured inventory; not a live database audit. Original source records remain original.'})
 (a.PKG/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]}))
 manifest=json.loads((a.PKG/'package.json').read_text())
 with tempfile.TemporaryDirectory() as td:
  for f in manifest['files']:
   dest=Path(td)/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy(a.PKG/f,dest)
  run=subprocess.run([sys.executable,str(Path(td)/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','6100','--format','json'],capture_output=True,text=True,check=True,cwd=td)
  assert json.loads(run.stdout)==m.batch('easy',5,6100)
 a.save('packaging-results.json',{'relocated_runtime_only':True,'deterministic':True,'files':manifest['files'],'dependencies':manifest['dependencies']})
 print(json.dumps({'source_questions':len(source_report),'complete_source_banks':sum(x['banks'] for x in source_report),'math_records':len(allrows),'controlled_banks':len(witnesses),'normal_samples':len(normal),'native_checks_prepared':len(allrows)*5}))
if __name__=='__main__':main()
