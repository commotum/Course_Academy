import collections,copy,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_generated_record,MATH
D=json.loads((H/'current.json').read_text());samples=json.loads((H/'generator-samples.json').read_text());tk={k:t for t,k,q in D['links']};synthetic={'questions':[],'topics':D['topics'],'links':[]};grade=[];items=[];reports=[]
for rec in samples:
 validation_error=None
 try:validate_generated_record(rec)
 except Exception as ex:validation_error=str(ex)
 q=copy.deepcopy(rec['question']);checks=[];qid=q[':question/id'];qid='fresh:'+qid;q[':db/id']=qid
 for attr in[':question/problem',':question/worked-solution']:
  items.append({'entity':qid,'attribute':attr,'value':q.get(attr,'')})
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  f[':db/id']=f[':answer-field/id'];ft=f[':answer-field/type'];f[':answer-field/type']={':db/ident':ft};cid=f[':answer-field/correct'][1]
  for a in f.get(':answer-field/choices',[]):
   a[':db/id']=a[':answer/id'];at=a[':answer/type'];a[':answer/type']={':db/ident':at}
   if at in[':answer.type/math',':answer.type/text']:items.append({'entity':a[':answer/id'],'attribute':':answer/value','value':a[':answer/value'],'bare_math':at==':answer.type/math'})
  a=next(a for a in f[':answer-field/choices']if a[':answer/id']==cid);f[':answer-field/correct']=copy.deepcopy(a)
  if ft==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected'}for a in f[':answer-field/choices'])
  if ft==':answer-field.type/checkbox':items.append({'entity':f[':db/id'],'attribute':':answer-field/key','value':f[':answer-field/key']})
 k=rec['knowledge_point']['db_id']if isinstance(rec['knowledge_point'],dict)else rec['knowledge_point'];synthetic['questions'].append(q);synthetic['links'].append([tk[k],k,qid]);grade.append({'label':qid,'record':rec,'checks':checks})
 ps=q[':question/problem'];display_integrals=[m[0]for m in MATH.finditer(ps)if r'\int'in m[0]];reports.append({'kp':k,'identity':qid,'template':rec['generation'].get('template'),'difficulty':q[':question/difficulty'],'source_ids':rec['generation'].get('source_ids',[]),'problem':ps,'integral_display':all(m.startswith(('$$',r'\['))for m in display_integrals),'validation_error':validation_error,'notation_limits':'Scalar calculus templates require complete differential, powers, constants, domains and plotted geometry; vector notation not applicable. Source graphs retained as images.','generation':rec['generation']})
(H/'fresh-current.json').write_text(json.dumps(synthetic,indent=2));(H/'fresh-grading-input.json').write_text(json.dumps(grade,indent=2));(H/'fresh-render-input.json').write_text(json.dumps(items,indent=2));(H/'fresh-notation-review.json').write_text(json.dumps(reports,indent=2));subprocess.run([str(H.parent/'check-engine'),str(H/'fresh-grading-input.json'),str(H/'fresh-grading.json')],check=True)
for name,prefix in [('audit_scalar_math.py','scalar'),('audit_models.py','model'),('audit_other_math.py','other')]:
 s=(H/name).read_text().replace("H/'current.json'","H/'fresh-current.json'").replace("H/'scalar-math-validation.json'","H/'fresh-scalar-math-validation.json'").replace("H/'model-math-validation.json'","H/'fresh-model-math-validation.json'").replace("H/'other-math-validation.json'","H/'fresh-other-math-validation.json'")
 exec(compile(s,str(H/name),'exec'),{'__file__':str(H/name)})
print('freshrecords',len(samples),'render values',len(items),'inline calculation prompts',sum(not r['integral_display']for r in reports))
