"""Verify printed arithmetic, diagram geometry, distractors and fresh batches."""
import importlib.util,json,math,os,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H/'package'))
from generate.triangle_complement_contract import inspect_record
from scripts.generator_publish import prepare_records,inventory_fingerprints
spec=importlib.util.spec_from_file_location('triangle_checked',H/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
pool=json.loads((H/'candidate-pool.json').read_text());reports=[];grading=[]
def cross(a,b,c):return abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))/2
def check(r):
 proof=inspect_record(r);p=r['generation']['parameters'];v=g.vertices(p);a,b,c,d=[v[k] for k in g.labels(p)]
 assert math.isclose(math.dist(a,b),proof['sides'][0]) and math.isclose(math.dist(a,d),proof['sides'][1])
 assert math.isclose(cross(a,b,d),proof['outer'])
 assert math.isclose(cross(a,b,c)+cross(a,c,d),proof['given'])
 assert math.isclose(cross(b,c,d),proof['raw'])
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  T,Q=proof['outer'],proof['given'];raw={'outer':T,'given':Q,'add':T+Q,'omit_half':2*T-Q,'half_result':(T-Q)/2,'half_given':T-Q/2,'twice_given':T-2*Q,'omit_sine':math.prod(proof['sides'])/2-Q,'double_outer':2*T}
  assert sorted(proof['values'])==sorted([proof['answer']]+[math.floor(raw[e]+.5) for e in r['generation']['bank_profile']])
 return proof
for i,r in enumerate(pool):
 reports.append(check(r));f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  tests=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected'} for a in f[':answer-field/choices']]
 else:
  answer=str(reports[-1]['answer']);tests=[{'submitted':answer,'expected':'accepted'},{'submitted':answer+'.000','expected':'accepted'},{'submitted':str(int(answer)+1),'expected':'rejected'}]
 grading.append({'label':str(i),'record':r,'checks':tests})
fresh=[]
for level in g.LEVELS:
 for seed in (7,37,20261027):
  batch=g.generate_batch(level,20,seed,H/'stress-assets')
  for r in batch:check(r)
  fresh+=batch
before=json.loads((H/'before.json').read_text());fingerprints=inventory_fingerprints(before[':knowledge-point/questions']+[before[':knowledge-point/canonical-example']])
new,duplicates=prepare_records(pool,g.KP['db_id'],before[':knowledge-point/id'],fingerprints,H/'offline-math',H/'assets')
assert len(new)==15 and duplicates==0
result={'passed':True,'candidate_records':15,'fresh_records':len(fresh),'diagrams_geometrically_verified':15+len(fresh),'new_questions':len(new),'duplicates':duplicates,'delivered':reports}
for name,value in [('generator-verification',result),('grader-input',grading),('render-input',pool)]:
 (H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='delivered'}))
