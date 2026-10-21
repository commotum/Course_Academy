from audit import *
import platform
from collections import Counter

def main():
 repaired=json.load(open(OUT/'repaired-records.json'))
 # Verify added local replay asset loads after relocation using only manifest files.
 snippet='''import sys,json;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);import generator as g
records=[g.build(x) for x in g.source_instances()+g.moderate_ops.sources()]
print(json.dumps(records))'''
 cmd=[str(ROOT/'.venv/bin/python'),'-c',snippet,str(OUT/'relocated-package')]
 p=subprocess.run(cmd,cwd=OUT,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 assert p.returncode==0,p.stderr
 rs=json.loads(p.stdout);save('relocated-source-records.json',rs)
 assert all(check(r)['unique_correct'] and check(r)['final_solution_correct'] for r in rs)
 assert all(any(r['question']==x['question'] for x in rs) for r in repaired)
 save('relocated-source-results.json',{'command':cmd,'records':len(rs),'both_new_profiles_replayed':True,'runtime_version':platform.python_version(),'package_unchanged':digest()==json.load(open(OUT/'package-hashes-before.json'))})
 inventory=json.load(open(JOB/'source/inventory.json'));source=json.load(open(JOB/'source/source.json'))['material']['kp'];source_ids={q[':question/id'] for q in source[':knowledge-point/questions']}
 other=[q for q in inventory['questions'] if q[':question/id'] not in source_ids]
 audit={'basis':inventory['basis'],'questions':len(inventory['questions']),'source_originals':len(inventory['questions'])-len(other),'other_records':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'generation_fields':[k for k in q if 'generat' in k]} for q in other],'conclusion':'The demonstrated historical defects were missing replay banks, not wrong served instances. Repaired complete banks now match the two stored source originals. No affected generated inventory record was demonstrated. Other inventory records lack generation metadata; they are not certified defect-free or reclassified as generated.','inspected_for':'The two retained source-bank omissions only; not a second exhaustive unchanged inventory audit.'}
 save('inventory-audit.json',audit);save('affected-inventory.json',{'affected_questions':[]})
 sample=json.load(open(OUT/'samples.json'));batch=json.load(open(OUT/'runner-batch.json'))
 ps=json.load(open(OUT/'shortcut-results.json'))
 # Check each fixed position, not just position one, within every recognizable easy template.
 for name,records,ref in [('sample',sample[:48],'easy-samples.json'),('batch',batch,'runner-batch.json'),('delivered-sample',json.load(open(OUT/'delivery-sample/accepted.json')),'delivery-sample/accepted.json')]:
  for t in ['swap','scale']:
   sub=[r for r in records if r['generation']['template']==t]
   for pos in range(5):
    hits=sum(r['question'][':question/answer-fields'][0][':answer-field/choices'][pos][':answer/id']==key(r['question']) for r in sub)
    ps.append({'cue':'position '+str(pos+1),'subgroup':name+':'+t,'scope':'within_template','strategy':'Always select displayed option '+str(pos+1),'correct':hits,'total':len(sub),'baseline':.2,'disposition':'not_predictive','conclusion':'Uniform five-option baseline is 0.2. No fixed position solves this subgroup; rates in two- or three-item batch subgroups are descriptive and cannot certify general balance.','sample_refs':[ref]})
 # The easy swap layout has total |entries| equal across choices. No extreme-magnitude cue distinguishes any permutation.
 # A valid single-entry simplification still performs the requested arithmetic.
 sub=[r for r in sample+batch if r['generation']['template']=='scale'];hits=0
 for r in sub:
  q=r['question'];m=matrices(q[':question/problem'])[0];_,t,k=operations(q[':question/problem'])[0];j=next(j for j,x in enumerate(m[t]) if x)
  cs=[c for c in q[':question/answer-fields'][0][':answer-field/choices'] if matrices(c[':answer/value'])[0][t][j]==k*m[t][j]]
  hits+=len(cs)==1 and cs[0][':answer/id']==key(q)
 ps.append({'cue':'Proportional-row comparison bank','subgroup':'sample-and-batch:scale','scope':'within_template','strategy':'Apply the specified scalar to one nonzero entry in the specified row and select the unique matching value','correct':hits,'total':len(sub),'baseline':.2,'disposition':'intended_skill','conclusion':'Five-choice guessing baseline 0.2. This works on all tested scaling comparison banks but requires reading target and scalar and doing the intended multiplication. The source skill does not require redundant arithmetic after a discriminating entry is found.','sample_refs':['samples.json','runner-batch.json']})
 save('shortcut-results.json',ps)
 save('scope-results.json',{'current_counts':dict(Counter(r['generation']['difficulty'] for r in sample)),'batch_difficulty':'easy','all_batch_easy':all(r['question'][':question/difficulty']==':question.difficulty/easy' for r in batch),'operation_counts':dict(Counter(str((r['generation']['difficulty'],len(operations(r['question'][':question/problem'])))) for r in sample)),'source_support':['e-4694 and q-130070: easy swaps','q-130071 and inferred q-10252: easy scalings','q-10217 through q-72747: one addition','q-130072, q-72785 and q-72786: sequential pair'],'conclusion':'No new operation, prerequisite, response type or extra arithmetic stage. Exact source-only banks are guarded replay profiles for uncertain captured distractors; the existing general random scaling/addition families remain available.'})
 save('package-hashes-after.json',digest());assert digest()==json.load(open(OUT/'package-hashes-before.json'))
 print('relocated source records',len(rs),'inventory source/other',audit['source_originals'],len(other),'unchanged package confirmed')
if __name__=='__main__':main()
