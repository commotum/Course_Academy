"""Reproduce the five retained legacy generated records; no database operations."""
import sys,importlib.util,json
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('legacy',R/'author-old/17592186087879.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
old=json.load(open(R/'generated-records.json'));inventory=json.load(open(R.parent/'source/inventory.json'));records=[];affected=[]
for r in old:
 z=g.generate('easy',seed=0,parameters=r['generation']['parameters']);q=next(q for q in inventory['questions'] if q[':question/id']==z['question'][':question/id'])
 assert z==r, 'Complete historical reconstruction changed'
 assert q[':question/problem']==z['question'][':question/problem']
 assert q[':question/worked-solution']==z['question'][':question/worked-solution']
 records.append(z);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Historical easy_constant bank fixes first answer e^x; resolved in current generator but these captured old records remain affected.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_inventory.py; legacy seed=0, parameters='+json.dumps(z['generation']['parameters'],sort_keys=True),'evidence_path':'generated-records.json'})
(R/'generated-records.json').write_text(json.dumps(records,indent=2));(R/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2));print(json.dumps({'historical_affected_records':len(records),'matched_complete_records':True,'database_writes':0}))
