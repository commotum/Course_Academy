import hashlib,json,re
from pathlib import Path
root=Path('/home/jake/Developer/Course_Academy/reference/mathacademy');rows=[]
for name in ['review-13925710','sum-rule-13925458','factorials-13831129','multistep-13931219','assessment-13930620']:
 d=root/name;c=json.loads((d/'content.json').read_text());findings=[];ids=[]
 for bucket in ['questions','canonical_examples']:
  for q in c.get(bucket,[]):
   mid=q.get('math_academy_id');ids.append(mid)
   for key in ['problem','worked_solution']:
    if not q.get(key):findings.append({'question':mid,'missing':key})
   fields=q.get('answer_fields',[])
   if bucket=='questions' and not fields and not(q.get('field_type_evidence') and q.get('correct_answer_from_solution') is not None):
    findings.append({'question':mid,'missing':'answer_fields_or_manual_source_answer'})
   for f in fields:
    if f.get('correct_value') is None: findings.append({'question':mid,'field':f.get('key'),'missing':'correct_value'})
    if f.get('type') in ['select','radio'] and not f.get('choices'):findings.append({'question':mid,'field':f.get('key'),'missing':'choices'})
 rows.append({'directory':str(d),'task_id':str(c.get('task_id') or name.rsplit('-',1)[-1]),'questions':len(c.get('questions',[])),
              'examples':len(c.get('canonical_examples',[])),'question_ids':ids,'findings':findings,
              'scope': 'Manual historical capture structure and saved verification inspected; not run through an incompatible engine checkpoint format'})
d=root/'diagnostic-capture/14033238';c=json.loads((d/'capture.json').read_text());findings=[];hashes=[]
for q in c['questions']:
 if not q.get('worked_solution'): findings.append({'id':q['id'],'missing':'worked_solution'})
 if not q.get('before',{}).get('problem'):findings.append({'id':q['id'],'missing':'problem'})
 if not q.get('before',{}).get('fields'):findings.append({'id':q['id'],'missing':'answer_fields'})
manifest=json.loads((d/'assets-manifest.json').read_text())
for asset in manifest.values():
 if not asset.get('path') or not asset.get('sha256'):continue
 p=Path(asset['path']);valid=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==asset['sha256']
 hashes.append({'path':str(p),'valid':valid})
rows.append({'directory':str(d),'task_id':'14033238','questions':len(c['questions']),'examples':0,'question_ids':[q['id'] for q in c['questions']],
 'findings':findings,'checked_assets':len(hashes),'asset_findings':[h for h in hashes if not h['valid']],
 'capture_only':c.get('capture_only'),'database_import_ready':c.get('database_import_ready'),
 'scope':'Diagnostic merged capture question structure, separately saved worked solutions, and manifest hashes; capture-only status is intentional'})
Path('/tmp/auxiliary-capture-completeness.json').write_text(json.dumps({'captures':rows},indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['task_id','questions','examples','findings']} for r in rows],indent=2))
