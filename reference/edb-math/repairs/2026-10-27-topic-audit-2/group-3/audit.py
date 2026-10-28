import collections,json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_math_structure,MATH
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());idents=dict(json.loads((H/'idents.json').read_text()));fields=[];seen=set();missing=[];classifications=[]
def walk(o,q=None):
 if isinstance(o,dict):
  if ':question/id'in o:q=o[':db/id']
  e=o.get(':db/id');checkbox=o.get(':answer-field/type',{}).get(':db/id')==17592186408166
  for a,v in o.items():
   if isinstance(v,str)and(a in (':question/problem',':question/worked-solution',':tutorial/content',':answer/value',':answer/feedback')or checkbox and a==':answer-field/key')and(e,a)not in seen:
    seen.add((e,a));fields.append({'entity':e,'attribute':a[1:],'value':v,'question':q,'bare':a==':answer/value'and o.get(':answer/type',{}).get(':db/id')==17592186045498})
   elif isinstance(v,(dict,list)):walk(v,q)
 elif isinstance(o,list):
  for v in o:walk(v,q)
walk(D['questions']);walk(D['content']);errors=[]
for f in fields:
 try:validate_math_structure(f['value'],bare_math=f['bare'])
 except Exception as ex:errors.append({**f,'error':str(ex)})
for q in D['questions']:
 for f in q.get(':question/answer-fields',[]):
  if ':answer-field/correct'not in f:missing.append({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'problem':q[':question/problem'],'field':f})
  if idents[f[':answer-field/type'][':db/id']]==':answer-field.type/blank':classifications.append({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'field':f[':db/id'],'key':f[':answer-field/key'],'answers':[{'entity':a[':db/id'],'type':idents[a[':answer/type'][':db/id']],'value':a[':answer/value']}for a in f.get(':answer-field/choices',[])]})
for name,val in [('fields',fields),('syntax-errors',errors),('missing-correct',missing),('blank-answer-classifications',classifications)]: (H/(name+'.json')).write_text(json.dumps(val,indent=2))
print('fields',len(fields),'errors',len(errors),'checkbox labels',sum(f['attribute']=='answer-field/key'for f in fields),'missing',len(missing),'blankfields',len(classifications));print(collections.Counter(e['error']for e in errors));print('blanktypes',collections.Counter(a['type']for f in classifications for a in f['answers']))
