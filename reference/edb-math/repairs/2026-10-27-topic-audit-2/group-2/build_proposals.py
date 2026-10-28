import json,re,copy
from pathlib import Path
H=Path(__file__).resolve().parent
# Preserve the original 57 source-format proposals separately before consolidation.
if not(H/'format-proposals.json').exists():(H/'format-proposals.json').write_text((H/'proposals.json').read_text())
p={}
for filename in ['format-proposals.json','control-proposals.json','completion-proposals.json','integral-display-proposals.json','operator-proposals.json']:
 for x in json.loads((H/filename).read_text()):
  k=x['entity'],x['attribute']
  if k in p and filename=='operator-proposals.json':
   x['after']=re.sub(r'(?<![A-Za-z])\{(sin|cos|tan|sec|csc|cot|ln|log|exp)\}(?=\s*\^)',lambda m:r'\operatorname{'+m[1]+'}',p[k]['after'])
  if k in p:x['reason']=p[k]['reason']+'; '+x['reason'];x['evidence']={'earlier':p[k]['evidence'],'current':x['evidence']}
  p[k]=x
fields=json.loads((H/'fields.json').read_text())
for e,a,v,ident,bare in fields:
 if e not in [17592186216448,17592186216449,17592186216639,17592186216640,17592186216653,17592186216654,17592186064634]:continue
 k=e,a;before=p[k]['after']if k in p else v;after=re.sub(r'\\int(?=[ghx])',lambda m:m[0]+' ',before)
 if after==before:continue
 x=p.get(k,{'entity':e,'attribute':a,'before':v,'reason':'','evidence':{},'confidence':'high'})
 x['after']=after;x['reason']+='; Restore source-proved integral command boundary (strict MathJax undefined-command failure)';x['evidence']={'source':ident,'source_archive':'317'if ident=='q-2425'else'6353','strict_before_error':True,'source_semantics':'integral applied to function, not glued unknown macro'};p[k]=x
for x in p.values():
 x['after']=x['after'].replace(r'\int2^x',r'\int 2^x')
(H/'proposals.json').write_text(json.dumps(list(p.values()),indent=2)+'\n')
D=json.loads((H/'current.json').read_text());questions=copy.deepcopy(D['questions']);qp={q[':db/id']:q for q in questions};entities={}
for q in questions:
 entities[q[':db/id']]=q
 for f in q.get(':question/answer-fields',[]):
  entities[f[':db/id']]=f
  for a in f.get(':answer-field/choices',[]):entities[a[':db/id']]=a
for x in p.values():
 if x['entity']in entities:entities[x['entity']][':'+x['attribute']]=x['after']
for x in json.loads((H/'type-proposals.json').read_text()):entities[x['entity']][':answer/type']={':db/ident':':'+x['after']}
keys=json.loads((H/'key-proposals.json').read_text())
for x in keys:entities[x['entity']][':answer-field/correct']=copy.deepcopy(entities[x['after']])
for x in json.loads((H/'new-blank-answer-proposals.json').read_text()):
 a={':answer/id':x['answer_uuid'],':answer/type':{':db/ident':':answer.type/math'},':answer/value':x['value']};f=entities[x['field']];f[':answer-field/choices']=[a];f[':answer-field/correct']=a
relations=[]
for qid in[17592186217792,17592186167067,17592186167069,17592186167070,17592186088032]:
 q=qp[qid];fs=q[':question/answer-fields'];keep=[f for f in fs if f.get(':answer-field/correct')];assert len(keep)==len({f[':answer-field/key']for f in fs})
 relations.append({'entity':qid,'attribute':'question/answer-fields','before':sorted(f[':db/id']for f in fs),'after':sorted(f[':db/id']for f in keep),'reason':'Detach duplicate obsolete response fields from question; source proves one control per key, current keyed replacement bank is complete; retain all detached entities and learner history','evidence':{'basis':9122,'identity':q[':question/math-academy-id'],'source_control_count':len(keep),'history_policy':'No field, answer, or learner-response entity deletion or mutation'},'confidence':'high'})
 q[':question/answer-fields']=keep
(H/'relation-proposals.json').write_text(json.dumps(relations,indent=2)+'\n');(H/'proposed-questions.json').write_text(json.dumps(questions,indent=2)+'\n')
print('content',len(p),'keys',len(keys),'relations',len(relations))
