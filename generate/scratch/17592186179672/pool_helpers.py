"""Captured content normalization and native pool fixture; no writes."""
KP=17592186179672
def norm(q):
 def enum(x):return str(x[':db/ident']) if isinstance(x,dict) else str(x)
 result={k:str(q[k]) for k in (':question/id',':question/problem',':question/worked-solution')}
 result[':question/difficulty']=enum(q[':question/difficulty']);fields=[]
 for f in q[':question/answer-fields']:
  correct=f[':answer-field/correct'];fields.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':[':answer/id',str(correct[':answer/id'])] if isinstance(correct,dict) else correct,':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])})
 result[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key']);return result

def scoped(kp,b,unavailable):
 entities={};enums={}
 def enum(x):
  ident=str(x[':db/ident']).lstrip(':')
  if ident not in enums:
   e=len(enums)+1;enums[ident]=e;entities[str(e)]={'db/ident':ident}
  return enums[ident]
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  d={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=d
  if ':question/difficulty'in q:d['question/difficulty']=enum(q[':question/difficulty'])
  for f in q.get(':question/answer-fields',[]):
   d['question/answer-fields'].append(f[':db/id']);fd={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=fd
   if ':answer-field/correct'in f:fd['answer-field/correct']=f[':answer-field/correct'][':db/id']
   for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
 entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
 return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(unavailable)}
