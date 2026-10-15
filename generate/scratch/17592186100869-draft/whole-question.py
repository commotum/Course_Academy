import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,subprocess,itertools
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
b=json.loads((D/'reference/grader-build.json').read_text())
src=(ROOT/b['source']).read_text()
needle='  reports.push(json!('
start=src.index(needle)
addition=r'''
  let mut subsets=vec![];
  for mask in 0..8usize {
   let mut response=BTreeMap::new();
   for(i,f)in fields.iter().enumerate(){
    let wanted=if mask&(1<<i)!=0{"true"}else{"false"};
    let a=f[":answer-field/choices"].as_array().unwrap().iter().find(|a|a[":answer/value"]==wanted).unwrap();
    response.insert(field_ids[i],maps[i][a[":answer/id"].as_str().unwrap()].to_string());
   }
   let expected=item["subset_expected"][mask].as_bool().ok_or("subset expected")?;
   let result=learning::grade(&snapshot,10,&response)?;
   if result!=expected{return Err(format!("subset {mask} result {result} expected {expected}").into())}
   subsets.push(json!({"mask":mask,"correct":result,"responses":response}));
  }
  let mut full=BTreeMap::new();
  for(i,f)in fields.iter().enumerate(){full.insert(field_ids[i],maps[i][f[":answer-field/correct"][1].as_str().unwrap()].to_string());}
  for id in &field_ids {
   let mut missing=full.clone();missing.remove(id);
   if learning::grade(&snapshot,10,&missing).is_ok(){return Err("Missing Boolean response accepted".into())}
  }
  let mut extra=full.clone();extra.insert(999,"100".into());
  if learning::grade(&snapshot,10,&extra).is_ok(){return Err("Extra field accepted".into())}
  checks.push(json!({"whole_question_subsets":subsets,"missing_field_rejections":3,"extra_field_rejections":1}));
'''
src=src[:start]+addition+src[start:]
(D/'whole-check.rs').write_text(src)
cmd=['rustc','--edition=2024',str(D/'whole-check.rs'),'-L','dependency='+str(ROOT/'target/release/deps'),'--extern','course_academy_engine='+str(ROOT/b['library']),'--extern','serde_json='+str(ROOT/next(p for p in b['dependencies'] if 'libserde_json-' in p)),'-o',str(D/'whole-check')]
subprocess.run(cmd,check=True)
items=json.loads((D/'engine-input.json').read_text())
if (D/'render-validation.json').exists():
 for preview in json.loads((D/'render-validation.json').read_text())['reports']:
  rec=preview['exact_record'];checks=[]
  for i,f in enumerate(rec['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual screenshot record Boolean member'})
  items.append({'label':'screenshot-'+preview['name'],'record':rec,'checks':checks})
for item in items:
 # Independently read actual printed array dimensions and ordered statements.
 import re
 dims={}
 for name,body in re.findall(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',item['record']['question'][':question/problem'],re.S):
  rows=body.split('\\\\');dims[name]=(len(rows),len(rows[0].split('&')))
 truths=[dims[a][1]==dims[b][0] for a,b in re.findall(r'The product \$([A-Z])([A-Z])\$',item['record']['question'][':question/problem'])]
 item['subset_expected']=[all(bool(mask&(1<<i))==v for i,v in enumerate(truths)) for mask in range(8)]
(D/'whole-input.json').write_text(json.dumps(items));subprocess.run([str(D/'whole-check'),str(D/'whole-input.json'),str(D/'whole-report.json')],check=True)
(D/'whole-validation.json').write_text(json.dumps({'passed':True,'records':len(items),'grade_field_checks':len(items)*6,'render_records_included':len(items)-730,'all_subsets':len(items)*8,'correct_subsets':len(items),'incorrect_subsets':len(items)*7,'missing_fields':len(items)*3,'extra_fields':len(items),'entry_points':['learning::grade','learning::grade_field'],'database_writes':0,'build_command':cmd,'source_sha256':hashlib.sha256((D/'whole-check.rs').read_bytes()).hexdigest(),'binary_sha256':hashlib.sha256((D/'whole-check').read_bytes()).hexdigest()},indent=2))
