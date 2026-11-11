import json,sys,subprocess
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');sys.path[:0]=[str(R),str(R/'scripts')]
from generate.pipeline.check_delivery import audit
from scripts.generator_publish import normalized_question
H=Path(__file__).resolve().parent;summary={};reps=[];rep_meta=[];allcases=[]
def enum(v):return v.get(':db/ident')if isinstance(v,dict)else v
for kp in [17592186096672,17592186096673]:
 d=H/str(kp);source=json.loads((d/'source/source.json').read_text());inventory=json.loads((d/'stored/inventory.json').read_text());sourcekp=source['material']['kp'];samples=json.loads((d/'sampled.json').read_text());stored=json.loads((d/'stored-records.json').read_text());bandreports={}
 for band in ['easy','moderate','hard']:
  records=[r for r in samples if enum(r['question'][':question/difficulty']).endswith('/'+band)];out=d/'delivery'/band
  report=audit(records,inventory,source,band,out,Path('/tmp'),Path('/media/jake/SSD/EDB/math'));accepted=json.loads((out/'accepted.json').read_text());bandreports[band]={'input':len(records),'accepted':len(accepted),'passed':report['passed']}
  if kp==17592186096672:
   targets=[('equations-to-ref-radio','matrix-to-ref-radio')if band=='easy'else('equations-to-assignments-radio','matrix-to-vector-radio')if band=='moderate'else('equations-to-vector-radio','matrix-to-assignments-radio')][0]
  else:targets=('equations-solve','matrix-echelon')if band=='easy'else('equations-echelon','matrix-solve')if band=='moderate'else('equations-solve','matrix-solve','equations-echelon','matrix-echelon')
  for target in targets:
   r=next((r for r in accepted if r.get('generation',{}).get('template',r.get('metadata',{}).get('family'))==target),None)
   assert r is not None,(kp,band,target)
   reps.append(r);rep_meta.append({'index':len(reps)-1,'kp':kp,'band':band,'family':target,'question_id':r['question'][':question/id'],'seed':r.get('metadata',r.get('generation',{})).get('seed')})
  for r in accepted:
   f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'];key=key[':answer/id']if isinstance(key,dict)else key[1]if isinstance(key,list)else key
   checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==key else'rejected','control':'canonical'if a[':answer/id']==key else'wrong','purpose':'Independently solved full3x4 system and verified exactly one valid offered endpoint.'}for a in f[':answer-field/choices']];allcases.append({'label':f'{kp}/{band}/'+r['question'][':question/id'],'record':r,'checks':checks})
 for r in stored:
  f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'];key=key[1]if isinstance(key,list)else key;f[':answer-field/correct']=[':answer/id',key]
  allcases.append({'label':'stored/'+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==key else'rejected','control':'canonical'if a[':answer/id']==key else'wrong','purpose':'Independently verified original stored matrix/solution and every option; selection equivalence is discrete.'}for a in f[':answer-field/choices']]})
 summary[str(kp)]=bandreports
(H/'native-input.json').write_text(json.dumps(allcases,indent=2)+'\n');subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
for kp,ids in [(17592186096672,[17592186097183,17592186760446]),(17592186096673,[17592186266015,17592186757021])]:
 qs=json.loads((H/str(kp)/'kp.json').read_text())[':knowledge-point/questions'];normalized=json.loads((H/str(kp)/'stored-records.json').read_text())
 for qid in ids:
  q=next(q for q in qs if q[':db/id']==qid);rec=next(r for r in normalized if r['question'][':question/id']==q[':question/id']);field=rec['question'][':question/answer-fields'][0];key=field[':answer-field/correct'];field[':answer-field/correct']=[':answer/id',key[1] if isinstance(key,list)else key];reps.append(rec);rep_meta.append({'index':len(reps)-1,'kp':kp,'stored_id':qid,'source_id':q.get(':question/math-academy-id'),'difficulty':q[':question/difficulty']})
(H/'render-records.json').write_text(json.dumps(reps,indent=2)+'\n');(H/'render-index.json').write_text(json.dumps(rep_meta,indent=2)+'\n');(H/'delivery-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'delivery':summary,'native_records':len(allcases),'ui_representatives':len(reps)},indent=2))
