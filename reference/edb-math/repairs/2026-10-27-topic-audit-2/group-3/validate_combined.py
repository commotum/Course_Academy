import copy,json,subprocess,collections
from pathlib import Path
H=Path(__file__).resolve().parent;D=copy.deepcopy(json.loads((H/'snapshot.json').read_text()));idents=dict(json.loads((H/'idents.json').read_text()));nodes=collections.defaultdict(list)
def walk(o):
 if isinstance(o,dict):
  if ':db/id'in o:nodes[o[':db/id']].append(o)
  for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(D)
for name in ['q334121-type-proposals.json']:
 for r in json.loads((H/name).read_text()):
  for n in nodes[r['entity']]:
   if ':answer/type'in n:n[':answer/type']={':db/id':r['after']}
for name in ['q334121-bank-membership-proposals.json','dependence-bank-membership-proposals.json','duplicate-field-membership-proposals.json']:
 for r in json.loads((H/name).read_text()):
  for n in nodes[r['entity']]:
   a=':'+r['attribute'];n[a]=[v for v in n[a]if v[':db/id']!=r['value']]
for name in ['dependence-correct-link-repairs.json','missing-key-completions.json']:
 for r in json.loads((H/name).read_text()):
  for n in nodes[r['field']]:n[':answer-field/correct']=copy.deepcopy(next(a for a in n[':answer-field/choices']if a[':db/id']==r['answer']))
for name in ['completion-solutions.json','proposals.json']:
 for r in json.loads((H/name).read_text()):
  for n in nodes[r['entity']]:
   a=':'+r['attribute']
   if a in n or(a==':question/worked-solution'and':question/id'in n):
    assert n.get(a)==r['before'],(name,r['entity'],a,n.get(a),r['before']);n[a]=r['after']
(H/'proposed-snapshot.json').write_text(json.dumps(D,indent=2));out=[];ungraded=[];control=[]
for original in D['questions']:
 q=copy.deepcopy(original);fs=q.get(':question/answer-fields',[])
 if not fs:continue
 assert len({f[':answer-field/key']for f in fs})==len(fs),(q[':db/id'],'duplicate field key')
 if any(not f.get(':answer-field/correct')for f in fs):ungraded.append(q[':db/id']);continue
 checks=[]
 for i,f in enumerate(fs):
  right=f[':answer-field/correct'];assert right[':db/id']in{a[':db/id']for a in f[':answer-field/choices']};right=next(a for a in f[':answer-field/choices']if a[':db/id']==right[':db/id']);f[':answer-field/correct']=[':answer/id',right[':answer/id']];f[':answer-field/type']=idents[f[':answer-field/type'][':db/id']]
  for a in f[':answer-field/choices']:a[':answer/type']=idents[a[':answer/type'][':db/id']]
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Current or mathematically completed canonical expression accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect constant rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'All owned source bank choices against current/repaired canonical key'}for a in f[':answer-field/choices'])
 out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Group3 calculus/ODE audit'},'generation':{'template':'current-or-proposed-record'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2));(H/'grading-coverage.json').write_text(json.dumps({'records':len(out),'checks':sum(len(r['checks'])for r in out),'missing_key_remaining':ungraded},indent=2));subprocess.run([str(H.parent/'check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],check=True);print('graded',len(out),'checks',sum(len(r['checks'])for r in out),'missingkey',ungraded)
# Render all content including checkbox display keys, preserve learner-input failures as separate classifications.
fields=[];seen=set()
def add(e,a,v,bare=False):
 if (e,a)not in seen:fields.append({'entity':e,'attribute':a,'value':v,'bare_math':bare});seen.add((e,a))
for q in D['questions']:
 for a in ['question/problem','question/worked-solution']:
  if ':'+a in q:add(q[':db/id'],a,q[':'+a])
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/id']==17592186408166:add(f[':db/id'],'answer-field/key',f[':answer-field/key'])
  for a in f.get(':answer-field/choices',[]):
   add(a[':db/id'],'answer/value',a[':answer/value'],a[':answer/type'][':db/id']==17592186045498)
   if ':answer/feedback'in a:add(a[':db/id'],'answer/feedback',a[':answer/feedback'])
for c in D['content']:
 if ':tutorial/content'in c:add(c[':db/id'],'tutorial/content',c[':tutorial/content'])
if (H/'all-contexts.json').exists():
 for q,s,m,v in json.loads((H/'all-contexts.json').read_text()):add(m,'multistep/context',v)
(H/'proposed-render-input.json').write_text(json.dumps(fields,indent=2));print('strict render fields',len(fields))
