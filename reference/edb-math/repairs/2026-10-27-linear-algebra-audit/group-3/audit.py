import collections,json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_math_structure,normalize_matrix_answer_tables,normalize_tex,MATH
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());fields=[];seen=set()
def walk(o,q=None):
 if isinstance(o,dict):
  if ':question/id'in o:q=o[':db/id']
  e=o.get(':db/id')
  for a,v in o.items():
   if isinstance(v,str)and a in (':question/problem',':question/worked-solution',':tutorial/content',':answer/value',':answer/feedback')and(e,a)not in seen:
    seen.add((e,a));fields.append({'entity':e,'attribute':a[1:],'value':v,'question':q,'bare':a==':answer/value'and o.get(':answer/type',{}).get(':db/id')==17592186045498})
   elif isinstance(v,(dict,list)):walk(v,q)
 elif isinstance(o,list):
  for v in o:walk(v,q)
walk(D['questions']);walk(D['content']);errors=[];tables=[];missing=[];sus=[]
for f in fields:
 try:validate_math_structure(f['value'],bare_math=f['bare'])
 except Exception as ex:errors.append({**f,'error':str(ex)})
 if normalize_matrix_answer_tables(f['value'])!=f['value']:tables.append(f)
 if re.search(r'(?m)^>\s*[^\n]|\\begin\{aligned\}|\\begin\{array\}',f['value']):sus.append(f)
for q in D['questions']:
 for f in q.get(':question/answer-fields',[]):
  if ':answer-field/correct'not in f:missing.append({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'field':f})
for name,val in [('fields',fields),('syntax-errors',errors),('table-candidates',tables),('missing-correct',missing),('suspects',sus)]:
 (H/(name+'.json')).write_text(json.dumps(val,indent=2))
print('fields',len(fields),'errors',len(errors),'tables',len(tables),'missing',len(missing),'sus',len(sus));print(collections.Counter(x['error']for x in errors));print(collections.Counter(x['attribute']for x in errors))
