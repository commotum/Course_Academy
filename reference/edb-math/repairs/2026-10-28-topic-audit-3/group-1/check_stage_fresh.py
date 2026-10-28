import json,copy,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from generator_source_policy import reject_excluded_sources
rs=json.loads((H/'generator-stage-samples.json').read_text());excluded=json.loads((H.parent/'source-eligibility.json').read_text())['excluded_questions'];provenance=[];checks=[];items=[]
for index,rec in enumerate(rs):
 if 'knowledge_point'not in rec:rec['knowledge_point']={'db_id':rec['knowledge_point_id'],'title':'Fresh source generator'}
 try:reject_excluded_sources([rec],excluded);provenance.append({'index':index,'kp':rec['knowledge_point']['db_id'],'status':'pass'})
 except Exception as ex:provenance.append({'index':index,'kp':rec['knowledge_point']['db_id'],'status':'fail','error':str(ex),'generation':rec['generation']})
 q=rec['question'];case=[]
 for a in ['question/problem','question/worked-solution']:
  if q.get(':'+a):items.append({'entity':q[':question/id'],'attribute':a,'value':q[':'+a]})
 for i,f in enumerate(q[':question/answer-fields']):
  right=f.get(':answer-field/correct');rightid=right[1]if isinstance(right,list)else right.get(':answer/id')if isinstance(right,dict)else None
  if f[':answer-field/type']==':answer-field.type/checkbox':items.append({'entity':f[':answer-field/id'],'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f.get(':answer-field/choices',[]):
   bare=a[':answer/type']==':answer.type/math';value=a[':answer/value'];value='![]('+value+')'if a[':answer/type']==':answer.type/image'else value;items.append({'entity':a[':answer/id'],'attribute':'answer/value','value':value,'bare_math':bare})
   if rightid:case.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==rightid else'rejected','purpose':'Fresh canonical dispatch' })if f[':answer-field/type']!=':answer-field.type/blank'else None
  if rightid and f[':answer-field/type']==':answer-field.type/blank':
   right=next(a for a in f[':answer-field/choices']if a[':answer/id']==rightid);case.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Fresh canonical math accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect scalar rejected'}])
 if case:checks.append({'label':str(index),'record':rec,'checks':case})
(H/'stage-fresh-source-policy.json').write_text(json.dumps(provenance,indent=2));(H/'stage-fresh-grading-input.json').write_text(json.dumps(checks,indent=2));(H/'stage-fresh-render-input.json').write_text(json.dumps(items,indent=2));print('records',len(rs),'sourcefail',sum(x['status']=='fail'for x in provenance),'gradercases',len(checks),'renderfields',len(items),flush=True)
subprocess.run([str(H.parent/'check-engine'),str(H/'stage-fresh-grading-input.json'),str(H/'stage-fresh-grading.json')],check=True)
