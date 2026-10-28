import itertools,json,subprocess,sys
from pathlib import Path
from migration import H,ROOT,portable
prep=json.loads((H/'review/preparation.json').read_text());records=[]
for case,plan in zip(prep['proposed'],prep['plans']):
 q=portable(case['question']);fields=q[':question/answer-fields'];checks=[];mapped=[]
 for i,f in enumerate(fields):
  correct=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected'})
 if plan['decision']=='convert':
  for c in plan['choice_mapping']:
   selected=set(c['selected']);uuids=[]
   for obj,f in zip(plan['objects'],fields):uuids.append(next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(obj['source_label'] in selected).lower()))
   correct_labels={o['source_label'] for o in plan['objects'] if o['selected']};mapped.append({'old_answer':c['old_answer'],'answer_ids':uuids,'expected':selected==correct_labels})
 else:
  for bits in itertools.product((False,True),repeat=len(fields)):
   uuids=[next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(v).lower()) for v,f in zip(bits,fields)];mapped.append({'old_answer':'consistent prior subset '+str(bits),'answer_ids':uuids,'expected':all(bits)})
 records.append({'label':str(plan['question']),'record':{'question':q,'knowledge_point':{'title':'Critical points and extrema'},'generation':{'template':'radio-to-independent-checkboxes'}},'checks':checks,'mapped_responses':mapped})
(H/'engine-input.json').write_text(json.dumps(records,indent=2)+'\n')
deps=ROOT/'target/release/deps';engine=max(deps.glob('libcourse_academy_engine*.rlib'),key=lambda p:p.stat().st_mtime_ns);serde=max(deps.glob('libserde_json*.rlib'),key=lambda p:p.stat().st_mtime_ns)
source=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next/check-checkbox-engine.rs';binary=Path('/tmp/critical-points-checkbox-grader-20261028')
command=['rustc','--edition=2024','-O',str(source),'-L','dependency='+str(deps),'--extern','course_academy_engine='+str(engine),'--extern','serde_json='+str(serde),'-o',str(binary)]
subprocess.run(command,check=True);subprocess.run([str(binary),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
(H/'engine-build.json').write_text(json.dumps({'engine_library':str(engine),'command':command},indent=2)+'\n')
