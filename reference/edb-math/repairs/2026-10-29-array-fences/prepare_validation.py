import copy,hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,validate_tex,MATH
ps=json.loads((H/'proposals.json').read_text());qs=json.loads((H/'questions.json').read_text());changes={(p['entity'],':'+p['attribute']):p['after']for p in ps};qmap={q[':db/id']:q for q in qs};render=[]
for p in ps:
 render.append({'entity':p['entity'],'attribute':p['attribute'],'value':p['after'],'bare_math':p['bare_math'],'fields':qmap.get(p['entity'],{}).get(':question/answer-fields',[])})
(H/'render-input.json').write_text(json.dumps(render,indent=2)+'\n')
def transform(obj):
 if isinstance(obj,list):return[transform(x)for x in obj]
 if not isinstance(obj,dict):return obj
 out={k:transform(v)for k,v in obj.items()};e=out.get(':db/id')
 for k in out:
  if(e,k)in changes:out[k]=changes[e,k]
 return out
after=transform(qs);(H/'proposed-questions.json').write_text(json.dumps(after,indent=2)+'\n')
# Only mathematical strings and checkbox labels change. Every owned UUID/link,
# noncanonical learner entry, answer type, and correct-answer identity is stable.
def contract(q):
 return{'id':q[':question/id'],'fields':[{'id':f.get(':answer-field/id'),'eid':f[':db/id'],'type':f[':answer-field/type'],'right':f.get(':answer-field/correct'),'choices':[{k:a[k]for k in [':db/id',':answer/id',':answer/type']if k in a}for a in f.get(':answer-field/choices',[])]}for f in q.get(':question/answer-fields',[])]}
assert[contract(q)for q in qs]==[contract(q)for q in after]
for old,new in zip(qs,after):
 if any((f[':db/id'],':answer-field/key')in changes for f in old.get(':question/answer-fields',[])):
  keys=[f[':answer-field/key']for f in new[':question/answer-fields']];assert len(keys)==len(set(keys))
native=[];skipped=[]
for phase,model in [('before',qs),('after',after)]:
 for q in model:
  fs=[];checks=[]
  for f in q.get(':question/answer-fields',[]):
   kind=f[':answer-field/type'].get(':db/ident');bank=f.get(':answer-field/choices',[]);right=f.get(':answer-field/correct',{}).get(':db/id');byid={a[':db/id']:a for a in bank}
   if kind not in [':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox']:continue
   if right not in byid:skipped.append({'phase':phase,'question':q[':db/id'],'field':f[':db/id'],'reason':'Preexisting absent canonical'});continue
   i=len(fs);nf=copy.deepcopy(f);nf[':answer-field/type']=kind;nf[':answer-field/correct']=[':answer/id',byid[right][':answer/id']]
   for a in nf[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
   fs.append(nf);checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':db/id']==right else'rejected','purpose':'Same authored choice outcome before/after typography repair'}for a in bank)
  if checks:
   nq=copy.deepcopy(q);nq[':question/answer-fields']=fs;native.append({'label':phase+'-'+str(q[':db/id']),'record':{'question':nq,'knowledge_point':{'title':'Fence typography audit'},'generation':{'template':phase}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(native,indent=2)+'\n');(H/'validation-contract.json').write_text(json.dumps({'question_records':len(qs),'IDs_links_types_keys_and_learner_history_preserved':True,'graded_phases':2,'gradeable_selection_records':len(native),'preexisting_unkeyed_selection_fields':skipped,'math_changes':'Only fence sizing and cell-preserving legacy matrix environment correction','records_sha256':hashlib.sha256((H/'proposed-questions.json').read_bytes()).hexdigest()},indent=2)+'\n');print('Prepared',len(render),'renderedfields;',len(native),'before/after native records;',len(skipped),'preexistingunkeyedfieldoccurrences.')
