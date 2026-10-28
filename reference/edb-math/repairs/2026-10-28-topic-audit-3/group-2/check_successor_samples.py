import copy,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_source_policy import reject_excluded_sources
S=json.loads((H/'successor-samples.json').read_text());excluded=json.loads((H.parent/'source-eligibility.json').read_text())['excluded_questions'];fail=[];grades=[];render=[]
for i,s in enumerate(S):
 r=copy.deepcopy(s['record']);q=r['question'];label=f"{s['kp']}:{s['band']}:{i}"
 try:reject_excluded_sources([r],excluded)
 except Exception as e:fail.append({'label':label,'error':str(e),'generation':r.get('generation')})
 checks=[]
 for j,f in enumerate(q.get(':question/answer-fields',[])):
  right=f.get(':answer-field/correct');right=right[1]if isinstance(right,list)else right.get(':answer/id')if isinstance(right,dict)else right
  ft=f[':answer-field/type'];ft=ft.get(':db/ident')if isinstance(ft,dict)else ft
  f[':answer-field/type']=ft
  for aa in f.get(':answer-field/choices',[]):
   if isinstance(aa[':answer/type'],dict):aa[':answer/type']=aa[':answer/type'][':db/ident']
  a=next((a for a in f.get(':answer-field/choices',[])if a[':answer/id']==right),None)
  if not a:fail.append({'label':label,'error':'Missing/foreign canonical answer','field':j});continue
  if ft==':answer-field.type/blank':checks.extend([{'field_index':j,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Exact fresh canonical'},{'field_index':j,'submitted':'987654321','expected':'rejected','purpose':'Wrong scalar'}])
  else:checks.extend({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right else'rejected','purpose':'Complete fresh bank'}for a in f.get(':answer-field/choices',[]))
  display=f.get(':answer-field/key','')
  if ft==':answer-field.type/checkbox':render.append({'entity':label+':'+str(j),'attribute':'answer-field/key','value':display})
  for aa in f.get(':answer-field/choices',[]):
   at=aa[':answer/type'];at=at.get(':db/ident')if isinstance(at,dict)else at
   if at!=':answer.type/image':render.append({'entity':label+':'+aa[':answer/id'],'attribute':'answer/value','value':aa[':answer/value'],'bare_math':at==':answer.type/math'})
 for k in[':question/problem',':question/worked-solution']:render.append({'entity':label,'attribute':k[1:],'value':q.get(k,'')})
 grades.append({'label':label,'record':r,'checks':checks})
(H/'successor-source-policy.json').write_text(json.dumps({'records':len(S),'failures':fail},indent=2)+'\n');(H/'successor-grading-input.json').write_text(json.dumps(grades,indent=2)+'\n');(H/'successor-render-input.json').write_text(json.dumps(render,indent=2)+'\n');print('records',len(S),'policy/contract failures',len(fail),'render fields',len(render));subprocess.run([str(H.parent/'check-engine'),str(H/'successor-grading-input.json'),str(H/'successor-grading.json')],check=True)
