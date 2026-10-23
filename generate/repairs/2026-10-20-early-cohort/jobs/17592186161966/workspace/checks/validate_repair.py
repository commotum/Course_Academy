import sys,json,copy,shutil,subprocess,platform
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
import regressions as t
v=t.v;m=t.m;ROOT=t.ROOT;OUT=t.OUT
REPO=Path('/home/jake/Developer/Course_Academy')
JOB=ROOT.parent

def main():
 roles=json.load(open(OUT/'role-counterfactuals.json'))
 sources=json.load(open(OUT/'source-replays.json'))
 fresh=[m.generate(seed=931000+20*j+i,bank_profile=p) for j,p in enumerate(m.PROFILES) for i in range(3)]
 # Independent response-preservation witness, and a changed target with A held fixed.
 base=fresh[0];p=copy.deepcopy(base['generation']['parameters']);r=p['row'];p['A'][(r+1)%4][p['given']]+=1
 irrelevant=m.generate(seed=931000,bank_profile=base['generation']['bank_profile'],parameters=p)
 p=copy.deepcopy(base['generation']['parameters']);old_given=p['given'];p['given']=next(c for c in range(4) if c not in (p['pivot'],old_given));p.pop('choice_bank')
 target=m.generate(seed=931000,bank_profile=base['generation']['bank_profile'],parameters=p)
 cf=[base,irrelevant,target]
 for x in cf:v.inspect(x)
 def answer(r):return v.ops(v.field(r)[':answer-field/choices'][v.correct_index(r)][':answer/value'])
 assert answer(base)==answer(irrelevant) and answer(base)!=answer(target)
 assert v.matrices(base['question'][':question/problem'])==v.matrices(target['question'][':question/problem'])
 # Enumerate role assignments once; use an already verified bank and recompute only the zero row.
 role_records=[]
 for row in range(4):
  for pivot in range(4):
   for given in range(4):
    if pivot==given:continue
    cols=[c for c in range(4) if c!=pivot];targets=[c for c in cols if c!=given]
    A=[[2,4,-6,8],[1,0,2,-1],[3,1,0,2],[-1,2,1,0]];ks=[0]*4;ks[given]=-4;ks[targets[0]]=-2;ks[targets[1]]=3;A[row][pivot]=[-3,-1,1,3][row]
    for c in cols:A[row][c]=-ks[c]*A[row][pivot]
    p=dict(A=A,row=row,pivot=pivot,given=given,ks=ks,choice_bank=[(-2,3),(-2,-3),(3,2),(2,-3),(2,3)])
    role_records.append(m.generate(seed=100,bank_profile='q-130619',parameters=p))
 records=roles+fresh+cf+role_records+sources
 results=[v.inspect(r) for r in records]
 t.save('validation-records.json',records);t.save('fresh-records.json',fresh);t.save('counterfactuals.json',cf)
 t.save('math-results.json',dict(passed=len(records),independent_witness='Parse displayed matrices and operations; Fraction ratios; apply all choices and every solution stage',role_assignments=48,pivots=sorted({r['generation']['parameters']['A'][r['generation']['parameters']['row']][r['generation']['parameters']['pivot']] for r in fresh+role_records}),normal_attempts=dict(Counter(r['generation']['sampling_attempts'] for r in fresh)),normal_profiles=dict(Counter(r['generation']['bank_profile'] for r in fresh)),target_change=True,irrelevant_response_preserved=True,results=results))
 # Grader cases include every member of every identical-bank counterfactual group.
 t.save('grader-input.json',[{'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==v.correct_index(r) else 'rejected','purpose':'Key independently established from both displayed matrices'} for j,a in enumerate(v.field(r)[':answer-field/choices'])]} for i,r in enumerate(records)])
 t.save('delivery-input.json',roles+fresh+cf)
 t.save('render-input.json',[next(r for r in sources if r['generation']['bank_profile']=='q-130617'),roles[10],roles[11]])
 # Captured inventory: classify every entry and actual available provenance flags.
 src=json.load(open(JOB/'source/source.json'))['material']['kp'];source_ids={q[':question/id'] for q in src[':knowledge-point/questions']}
 inv=json.load(open(JOB/'source/inventory.json'));rows=[]
 for q in inv['questions']:
  rows.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],source=q[':question/id'] in source_ids,retired=q.get(':question/retired',False),generation={k:val for k,val in q.items() if 'generat' in k},eligibility_flags={k:val for k,val in q.items() if any(s in k for s in ('retir','unavail','disable','exclud'))}))
 assert all(x['source'] and not x['generation'] for x in rows)
 t.save('inventory-audit.json',dict(basis=inv['basis'],questions=rows,conclusion='13 original source questions, no generated stored records in captured inventory; no generated record eligible for historical repair. This is an inspected absence, not an untested pool. Live state and learner history not queried.'))
 t.save('affected-inventory.json',{'affected_questions':[]})
 manifest=json.load(open(ROOT/'package.json'));dest=OUT/'relocated';dest.mkdir(exist_ok=True)
 for name in manifest['files']:
  path=dest/name;path.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(ROOT/name,path)
 clone=v.load_generator(dest/manifest['entrypoint'])
 assert json.dumps(clone.batch('moderate',5,8123),sort_keys=True)==json.dumps(m.batch('moderate',5,8123),sort_keys=True)
 for difficulty in ['easy','hard']:
  try:m.generate(difficulty=difficulty)
  except ValueError:pass
  else:raise AssertionError('Unsupported band accepted')
 cli=subprocess.run([sys.executable,str(dest/manifest['entrypoint']),'--difficulty','moderate','--count','5','--seed','8123','--format','json'],check=True,capture_output=True,text=True)
 batch=json.loads(cli.stdout);assert len(batch)==5
 for r in batch:v.inspect(r)
 t.save('candidate-batch.json',batch)
 t.save('packaging.json',dict(deterministic=True,relocation=True,cli_count=5,python=platform.python_version(),sympy=m.sp.__version__,runtime_files=manifest['files'],unsupported_bands_rejected=['easy','hard']))
 print(json.dumps({'math_records':len(records),'fresh_records':len(fresh),'role_groups':len(roles)//5,'source_records':len(sources),'inventory_original':len(rows),'packaging':'pass'}))
if __name__=='__main__':main()
