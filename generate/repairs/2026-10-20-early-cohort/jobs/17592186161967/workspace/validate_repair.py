"""Affected validation: source replay, full-row arithmetic, native grading inputs."""
import copy, json, platform, re, subprocess, sys
from pathlib import Path
from check_repair import g, HERE, OUT, save, inspect, mats, ops, groups_report, BASE
REPO=Path('/home/jake/Developer/Course_Academy')
JOB=HERE.parent

def main():
 source=json.loads((JOB/'source/source.json').read_text())['material']['kp']
 replays=[];replay_report=[]
 for q in source[':knowledge-point/questions']:
  A,B=mats(q[':question/problem']);p=next(i for i in range(3) if A[i]==B[i]);c=int(re.search(r'(?:\{a\}|a)_\{\d(\d)\}',q[':question/worked-solution']).group(1))-1
  ks=[0 if i==p else -A[i][c]//A[p][c] for i in range(3)]
  r=g.generate(seed=8107,bank_profile=q[':question/math-academy-id'],parameters={'A':A,'pivot':p,'column':c,'ks':ks});inspect(r)
  bb=sorted(ops(x[':answer/value']) for x in r['question'][':question/answer-fields'][0][':answer-field/choices'])
  for f in q[':question/answer-fields']:
   assert bb==sorted(ops(x[':answer/value']) for x in f[':answer-field/choices'])
   if ':answer-field/correct' in f:
    assert tuple(o[2] for o in ops(f[':answer-field/correct'][':answer/value']))==tuple(k for i,k in enumerate(ks) if i!=p)
  assert mats(r['question'][':question/problem'])==[A,B]
  replays.append(r);replay_report.append({'source_id':q[':question/id'],'banks':len(q[':question/answer-fields']),'all_options_match':True})
 save('source-replays.json',replays);save('source-replay-report.json',replay_report)
 # Small representative fresh sample across all profiles, in addition to reported seed range.
 fresh=g.batch('easy',30,20261022);save('fresh-records.json',fresh)
 regression=json.loads((OUT/'regression-records.json').read_text())
 # Changed target with the same matrix; unrelated entry with the same operation.
 fixed=[[1,1,5],[1,2,2],[2,3,4]];counter=[]
 for p,c in ((0,0),(1,0),(0,1)):
  ks=[0 if i==p else -fixed[i][c]//fixed[p][c] for i in range(3)]
  counter.append(g.generate(seed=472,bank_profile='q-42531',parameters={'A':fixed,'pivot':p,'column':c,'ks':ks}))
 irrelevant=copy.deepcopy(BASE);irrelevant['A'][1][1]+=1
 pair=[g.generate(seed=472,bank_profile='q-42531',parameters=p) for p in (BASE,irrelevant)]
 assert [r['question'][':question/answer-fields'][0][':answer-field/choices'][inspect(r)[1]][':answer/value'] for r in pair][0]==pair[1]['question'][':question/answer-fields'][0][':answer-field/choices'][inspect(pair[1])[1]][':answer/value']
 counter+=pair;save('counterfactual-records.json',counter)
 # Unit and magnitude boundaries are retained wherever five source-shaped choices exist.
 boundary=[]
 for profile,a,b in [('q-42531',1,2),('q-130451',2,1),('q-91162',-2,-2),('q-91163',-9,1),('q-91159',1,-9)]:
  p=copy.deepcopy(BASE);p['ks']=[0,a,b];p['A'][1][0]=-a;p['A'][2][0]=-b
  boundary.append(g.generate(seed=20,bank_profile=profile,parameters=p))
 save('boundary-records.json',boundary)
 batch=g.batch('easy',5,20261022);save('candidate-batch.json',batch)
 records=regression+fresh+counter+boundary+replays+batch
 grader=[]
 for i,r in enumerate(records):
  _,ci=inspect(r);f=r['question'][':question/answer-fields'][0]
  grader.append({'label':str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==ci else 'rejected','purpose':'Independently evaluated all complete row operations'} for j,a in enumerate(f[':answer-field/choices'])]})
 save('grader-input.json',grader)
 save('delivery-input.json',records)
 save('render-records.json',[pair[0],fresh[3]])
 inv=json.loads((JOB/'source/inventory.json').read_text());original_ids={q[':question/id'] for q in source[':knowledge-point/questions']}
 assert all(q[':question/id'] in original_ids for q in inv['questions'])
 save('affected-inventory.json',{'affected_questions':[]})
 save('inventory-inspection.json',{'basis':inv['basis'],'count':len(inv['questions']),'generated_count':0,'original_source_ids_match':True,'conclusion':'Verified absence of generated inventory records in captured snapshot; original questions are not eligible generated-pool repairs.','questions':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':True} for q in inv['questions']]})
 summary={'independent_math_records':len(records),'complete_source_banks':sum(x['banks'] for x in replay_report),'fresh_count':len(fresh),'fresh_groups':groups_report(fresh),'pivots':sorted({r['generation']['parameters']['pivot'] for r in fresh}),'columns':sorted({r['generation']['parameters']['column'] for r in fresh}),'counterfactual_records':len(counter),'boundary_records':len(boundary),'dependencies':{'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}}}
 save('validation-report.json',summary)
 print(json.dumps({k:v for k,v in summary.items() if k!='fresh_groups'}))
if __name__=='__main__':main()
