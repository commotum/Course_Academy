import json,sys,hashlib,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
W=Path.cwd()
sys.path.insert(0,str(W/'checks'))
from check_repair import g,key,v
source=json.loads((W.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
results=[]
for original in source:
 sid=original[':question/math-academy-id']
 if sid not in g.CASES: continue
 record=g.source_replay(sid); q=record['question']
 for name in (':question/problem',':question/worked-solution'):
  assert q[name]==original[name],(sid,name)
 f=q[':question/answer-fields'][0]; of=original[':question/answer-fields'][0]
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']),sid
 assert key(record)[':answer/value']==of[':answer-field/correct'][':answer/value'],sid
 results.append({'source_id':sid,'question_id':original[':question/id'],'choices':len(f[':answer-field/choices'])})
accepted=json.loads((W/'evidence/delivery-batch-repair/accepted.json').read_text())
rendered=json.loads((W/'evidence/author8-render-records.json').read_text())
assert rendered==[accepted[0],accepted[-1]],'Retained UI records differ from current endpoints'
for r in rendered: v.independent(r, replay=False)
report=json.loads((W/'evidence/author8-render/rendering.json').read_text())
assert report['passed'] and len(report['cases'])==2
runtime=json.loads((W/'evidence/author10-exact-failures.log').read_text())['runtime_hashes']
assert all(hashlib.sha256((W/n).read_bytes()).hexdigest()==h for n,h in runtime.items())
result={'complete_source_banks':len(results),'source_choices':sum(r['choices'] for r in results),'source_cases':results,'ui_records_equal_current_delivered_endpoints':True,'render_input':'evidence/author8-render-records.json','render_report':'evidence/author8-render/rendering.json','visual_inspection':'Both screenshots reinspected: matrices, augmentation bars, signs, row operations, controls and solutions are readable; no clipping observed.','runtime_hashes_unchanged':runtime}
(W/'evidence/author10-source-render-binding.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'complete_source_banks':len(results),'choices':sum(r['choices'] for r in results),'actual_ui_records_bound':len(rendered),'runtime_unchanged':len(runtime)}))
