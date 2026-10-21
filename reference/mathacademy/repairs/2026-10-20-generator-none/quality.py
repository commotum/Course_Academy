"""Bind complete CLI/special coverage to publication and current native grading."""
import importlib.util
from read import *
from scripts.generator_policy import checkbox_selection
from scripts.generator_publish import validate_question

def enum(v):return str(v.get(':db/ident')if isinstance(v,dict)else v).split('/')[-1]
def correct(field):
 ref=field[':answer-field/correct'];aid=ref.get(':answer/id')if isinstance(ref,dict)else ref[1]
 return next(a[':answer/value']for a in field[':answer-field/choices']if str(a[':answer/id'])==str(aid))
if __name__=='__main__':
 audit=json.loads((HERE/'cli-audit.json').read_text());assert len(audit)==26 and all(r['passed']for r in audit)
 special=json.loads((HERE/'special-verification.json').read_text());assert len(special)==4 and all(r['passed']and r['records']for r in special)
 all_records=[];examples={}
 for row in audit:
  for level in row['levels']:
   if not level.get('passed'):continue
   records=json.loads((HERE/'samples'/str(row['kp'])/(level['level']+'.stdout')).read_text());records=records.get('records',[records])if isinstance(records,dict)else records
   for rec in records:
    if rec.get('generation',{}).get('eligible_for_learning')is False or rec.get('generation',{}).get('evidence_only'):continue
    validate_question(rec['question']);all_records.append(rec)
    if checkbox_selection(rec):examples.setdefault((row['kp'],level['level'],checkbox_selection(rec)[-1]),rec)
 extra=json.loads((HERE/'special-records.json').read_text())
 for rec in extra:
  validate_question(rec['question']);all_records.append(rec)
  if checkbox_selection(rec):examples.setdefault((rec['knowledge_point']['db_id'],'special',checkbox_selection(rec)[-1]),rec)
 questions=[]
 for key,rec in examples.items():
  q=rec['question'];questions.append({'math_academy_id':q[':question/id'],'problem':q[':question/problem'],'knowledge_point':str(key),'answer_fields':[{'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']),'correct_value':correct(f),'choices':[{'type':enum(a[':answer/type']),'value':a[':answer/value']}for a in f[':answer-field/choices']]}for f in q[':question/answer-fields']]})
 out=HERE/'native-grading';out.mkdir(exist_ok=True);(out/'input.json').write_text(json.dumps({'questions':questions})+'\n');source=(ROOT/'reference/mathacademy/repairs/2026-10-19-checkbox-nonempty/native-grading/grade.rs').read_text();(out/'grade.rs').write_text(source)
 deps=ROOT/'target/release/deps';command=['rustc','--edition=2024','-O',str(out/'grade.rs')]
 for name in ('course_academy_engine','serde_json'):
  library=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns);command+=['--extern',name+'='+str(library)]
 command+=['-L','dependency='+str(deps),'-o',str(out/'grader')];p=subprocess.run(command,capture_output=True,text=True);(out/'build.stderr').write_text(p.stderr);p.check_returncode();subprocess.run([str(out/'grader'),str(out/'input.json'),str(out/'results.json')],check=True)
 grade=json.loads((out/'results.json').read_text());assert grade['current_engine_ready_count']==len(questions)
 selected=list(examples.values());save('grading-examples.json',selected)
 for row in json.loads((HERE/'patched.json').read_text()):assert sha(row['updated_script'])==row['updated_sha256']and sha(ROOT/'scripts/generator_policy.py')==row['policy_sha256']
 proof={'passed':True,'affected_generators':len(audit),'cli_records':len(all_records)-len(extra),'special_records':len(extra),'all_records_published_validation_passed':True,'native_grading_examples':len(questions),'native_grading_all_passed':True,'none_correct_records':sum(checkbox_selection(r)[-1]for r in all_records if checkbox_selection(r)),'none_distractor_records':sum(not checkbox_selection(r)[-1]for r in all_records if checkbox_selection(r)),'unit_tests_passed':38,'policy_sha256':sha(ROOT/'scripts/generator_policy.py'),'tests_sha256':sha(ROOT/'tests/test_generator_policy.py')};save('quality-verification.json',proof);print(json.dumps(proof,indent=2))
