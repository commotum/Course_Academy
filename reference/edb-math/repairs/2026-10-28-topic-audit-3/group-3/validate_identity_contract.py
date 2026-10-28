import copy,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=Path.cwd();sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
samples=json.loads((H/'identity-contract-samples.json').read_text());fields=[];tests=[];skips=[]
for i,s in enumerate(samples):
 record=copy.deepcopy(s['record']);q=record['question'];label=str(s['kp'])+'/'+str(i);checks=[]
 for attr in[':question/problem',':question/worked-solution']:
  if attr in q:fields.append({'entity':label,'attribute':attr,'value':q[attr]})
 for j,f in enumerate(q.get(':question/answer-fields',[])):
  kind=f[':answer-field/type'];kind=kind[':db/ident']if isinstance(kind,dict)else kind;f[':answer-field/type']=kind;right=f.get(':answer-field/correct');cid=right[1]if isinstance(right,list)else right.get(':answer/id')if isinstance(right,dict)else None
  a=next((a for a in f.get(':answer-field/choices',[])if a.get(':answer/id')==cid),None)
  if a is None:skips.append({'label':label,'field':j,'reason':'no canonical'});continue
  f[':answer-field/correct']=[':answer/id',cid]
  if kind==':answer-field.type/checkbox':fields.append({'entity':label,'attribute':'answer-field/key','value':f[':answer-field/key']})
  for choice in f[':answer-field/choices']:
   typ=choice[':answer/type'];typ=typ[':db/ident']if isinstance(typ,dict)else typ;choice[':answer/type']=typ;fields.append({'entity':label,'attribute':'answer/value','value':choice[':answer/value'],'bare_math':typ==':answer.type/math'})
  if kind==':answer-field.type/blank':checks.extend([{'field_index':j,'submitted':a[':answer/value'],'expected':'accepted'},{'field_index':j,'submitted':'987654321','expected':'rejected'}])
  else:checks.extend({'field_index':j,'submitted_answer_id':choice[':answer/id'],'expected':'accepted'if choice[':answer/id']==cid else'rejected'}for choice in f[':answer-field/choices'])
 tests.append({'label':label,'record':record,'checks':checks})
(H/'identity-contract-grading-input.json').write_text(json.dumps(tests,indent=2));(H/'identity-contract-render-input.json').write_text(json.dumps(fields,indent=2));(H/'identity-contract-native-coverage.json').write_text(json.dumps({'records':len(tests),'checks':sum(len(x['checks'])for x in tests),'skips':skips},indent=2));p=subprocess.run([str(H.parent/'check-engine'),str(H/'identity-contract-grading-input.json'),str(H/'identity-contract-grading.json')],capture_output=True,text=True);print(p.stdout,p.stderr,'nativeexit',p.returncode,'records',len(tests),'fields',len(fields))
