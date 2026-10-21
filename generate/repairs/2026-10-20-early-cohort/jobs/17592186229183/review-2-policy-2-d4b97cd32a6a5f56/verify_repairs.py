import sys
sys.dont_write_bytecode=True
import json,subprocess,importlib.util,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;J=R.parent
results=[]
for flavor,script,want in [('current','repair_checks.py',0),('old-source','repair_checks.py',1),('old-bank','shortcut_checks.py',1),('current','shortcut_checks.py',0)]:
 w=R/'author-check'/flavor/'workspace';cmd=[sys.executable,str(w/script)];p=subprocess.run(cmd,cwd=w,capture_output=True,text=True)
 row={'fixture':flavor,'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_exit':want,'passed':p.returncode==want};results.append(row)
 assert row['passed'],row
# Replay retained complete generated records with their original implementation.
spec=importlib.util.spec_from_file_location('historical',R/'author-check/old-source/workspace/17592186229183.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sys.path.insert(0,'/home/jake/Developer/Course_Academy');from scripts.question_capture.math_format import normalize_prose
inv=json.loads((J/'source/inventory.json').read_text());byid={q[':question/id']:q for q in inv['questions']};rows=[]
records=json.loads((R/'generated-records.json').read_text())
for old in records:
 m=old['generation'];r=g.generate(m['level'],seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile']);assert r==old
 q=r['question'];s=byid[q[':question/id']];assert q[':question/problem']==s[':question/problem'];assert normalize_prose(q[':question/worked-solution'])==s[':question/worked-solution']
 def bank(q):
  f=q[':question/answer-fields'][0];k=f[':answer-field/correct'];k=k[1] if isinstance(k,list) else k[':answer/id'];return sorted(a[':answer/value'] for a in f[':answer-field/choices']),next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==k)
 assert bank(q)==bank(s)
 rows.append({'question_id':q[':question/id'],'entity_id':s[':db/id'],'original_record_and_metadata_reproduced':True,'stored_prompt_normalized_solution_bank_key_equal':True})
(R/'inventory-results.json').write_text(json.dumps({'command':sys.argv,'captured_basis':inv['basis'],'questions':len(inv['questions']),'verified_historical_records':rows,'affected_count':len(rows),'limitations':['Retained old forced-median defect; not attributed to current bank construction. Original source questions excluded. Inventory unchanged from previous review; no database access.']},indent=2)+'\n')
(R/'repair-verification.json').write_text(json.dumps({'command':sys.argv,'preflight':json.loads((J/'repair-preflight.json').read_text()),'executed_checks':results,'all_pass':True},indent=2)+'\n')
print(json.dumps({'checks':[{k:r[k] for k in ['fixture','command','exit_code','passed']} for r in results],'verified_inventory':len(rows)}))
