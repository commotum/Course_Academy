import concurrent.futures,importlib.util,json
from pathlib import Path
p=Path('generate/reports/checkbox-discovery-2026-10-12');spec=importlib.util.spec_from_file_location('scan',p/'scan.py');scan=importlib.util.module_from_spec(spec);spec.loader.exec_module(scan)
r=json.loads((p/'report.json').read_text());ids=sorted({q['id']for tier in ('strong_candidates','secondary_candidates','additional_review')for q in r[tier]})
query='[:find [?q ...] :in $ [?q ...] :where [?q :question/worked-solution _]]'
def read(group):return scan.DB.query(query,[group],p/'evidence','solution-presence-'+str(group[0]),scan.BASIS)
found=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
 for rows in pool.map(read,[ids[i:i+128]for i in range(0,len(ids),128)]):found.extend(rows)
(p/'solution-checked.json').write_text(json.dumps(ids)+'\n')
canonical=scan.DB.query('[:find ?q ?kp :where [?kp :knowledge-point/canonical-example ?q]]',[],p/'evidence','canonical-membership',scan.BASIS)
(p/'canonical-membership.json').write_text(json.dumps(canonical)+'\n')
(p/'solution-presence.json').write_text(json.dumps(sorted(found))+'\n')
examples=[17592186054632,17592186064166,17592186087702,17592186105769,17592186115228,17592186152075]
examples_q=[next(q['id']for q in r['strong_candidates']if any(k['id']==id for k in q['kps']))for id in examples]
rows=scan.DB.query('[:find (pull ?q [:db/id :question/math-academy-id :question/problem :question/worked-solution]) :in $ [?q ...] :where [?q :question/id _]]',[examples_q],p/'evidence','examples',scan.BASIS)
(p/'examples.json').write_text(json.dumps([row[0]for row in rows],indent=2)+'\n')
print(json.dumps({'candidate_questions':len(ids),'worked_solutions_present':len(found),'detailed_examples':len(rows)}))
