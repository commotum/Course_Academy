"""Verify prepared Boolean field grading with the current native engine, offline."""
import hashlib,json,subprocess,importlib.util
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'Cargo.toml').exists())
spec=importlib.util.spec_from_file_location('migration',OUT/'prepare.py');migration=importlib.util.module_from_spec(spec);spec.loader.exec_module(migration)
edb=migration.edb
plan=json.loads((OUT/'plan.json').read_text());records=[];mapped=0
for batch in plan['batches']:
 if batch['new_checkbox_fields']==0:continue
 b=json.loads((Path(batch['directory'])/'plan.json').read_text())
 for q in b['questions']:
  fields=[];checks=[]
  for i,label in enumerate(q['labels']):
   token=q['ma_id']+'/authored-checkbox-v1/'+label
   answers=[{':answer/id':str(edb.stable_id('answer',token+'/'+v)),':answer/type':':answer.type/text',':answer/value':v}for v in ('false','true')]
   correct=str(edb.stable_id('answer',token+'/'+str(label in q['correct']).lower()))
   fields.append({':answer-field/id':str(edb.stable_id('field',token)),':answer-field/key':label,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
   for a in answers:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'owned Boolean answer against preserved key'})
   for choice in q['choice_mapping']:
    selected=str(label in choice['selected']).lower()
    checks.append({'field_index':i,'submitted_answer_id':str(edb.stable_id('answer',token+'/'+selected)),'expected':'accepted'if (label in choice['selected'])==(label in q['correct'])else'rejected','purpose':'mapped original choice '+str(choice['old_answer'])})
  for choice in q['choice_mapping']:
   assert all((l in choice['selected'])==(l in q['correct'])for l in q['labels'])==(set(choice['selected'])==set(q['correct']));mapped+=1
  records.append({'label':q['ma_id'],'record':{'question':{':question/problem':q['problem_after'],':question/answer-fields':fields},'knowledge_point':{'title':q['kps'][0]['title']},'generation':{'template':'preserved-database-subset'}},'checks':checks,'mapped_responses':[{'old_answer':c['old_answer'],'answer_ids':[str(edb.stable_id('answer',q['ma_id']+'/authored-checkbox-v1/'+l+'/'+str(l in c['selected']).lower()))for l in q['labels']],'expected':set(c['selected'])==set(q['correct'])}for c in q['choice_mapping']]})
(OUT/'engine-input.json').write_text(json.dumps(records)+'\n')
deps=Path('/tmp/determinant-review-20261012/current-target/debug/deps')
lib=max(deps.glob('libcourse_academy_engine*.rlib'),key=lambda p:p.stat().st_mtime_ns);serde=max(deps.glob('libserde_json*.rlib'),key=lambda p:p.stat().st_mtime_ns)
source=OUT/'check-checkbox-engine.rs';binary=OUT/'check-checkbox-engine'
command=['rustc','--edition=2024','-O',str(source),'-L','dependency='+str(deps),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(serde),'-o',str(binary)]
subprocess.run(command,check=True);subprocess.run([str(binary),str(OUT/'engine-input.json'),str(OUT/'engine-report.json')],check=True)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(OUT/'native-build.json').write_text(json.dumps({'source_sha256':digest(source),'binary_sha256':digest(binary),'engine_library':str(lib),'engine_sha256':digest(lib),'command':command,'original_radio_choices_mapped':mapped,'database_writes':0},indent=2)+'\n')
r=json.loads((OUT/'engine-report.json').read_text());print(json.dumps({k:v for k,v in r.items()if k!='records'}))
