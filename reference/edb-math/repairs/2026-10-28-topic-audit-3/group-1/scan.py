import json,sys,re,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import validate_math_structure,validate_math_boundaries,normalize_matrix_answer_tables,normalize_prose
D=json.loads((H/'current.json').read_text());items=[]
for c in D['contents']:
 if ':tutorial/content'in c:items.append((c[':db/id'],'tutorial/content',c[':tutorial/content'],False))
for q in D['questions']:
 for a in ['question/problem','question/worked-solution']:
  if q.get(':'+a):items.append((q[':db/id'],a,q[':'+a],False))
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':items.append((f[':db/id'],'answer-field/key',f[':answer-field/key'],False))
  for a in f.get(':answer-field/choices',[]):
   items.append((a[':db/id'],'answer/value',a[':answer/value'],a[':answer/type'][':db/ident']==':answer.type/math'))
   if a.get(':answer/feedback'):items.append((a[':db/id'],'answer/feedback',a[':answer/feedback'],False))
issues=[];proposals=[]
for e,a,v,bare in items:
 for name,fn in [('structure',lambda:validate_math_structure(v,bare_math=bare)),('boundaries',lambda:validate_math_boundaries(v,strict=True)if not bare else None)]:
  try:fn()
  except Exception as ex:issues.append({'entity':e,'attribute':a,'check':name,'error':str(ex),'value':v})
 if not bare:
  after=normalize_matrix_answer_tables(v)
  if after!=v:proposals.append({'entity':e,'attribute':a,'before':v,'after':after,'reason':'Flattened Markdown answer matrix has spreadsheet spacing rather than matrix brackets; restore row-major matrix input layout.','evidence':'Same ordered placeholder keys and rectangular rows; source table review pending.','confidence':'pending'})
(H/'items.json').write_text(json.dumps(items,indent=2));(H/'structural-issues.json').write_text(json.dumps(issues,indent=2));(H/'matrix-candidates.json').write_text(json.dumps(proposals,indent=2));print('items',len(items),'issues',len(issues),'matrix candidates',len(proposals));print(collections.Counter((i['check'],i['error'])for i in issues));print('missing keys',[(q[':db/id'],q.get(':question/math-academy-id'),[f[':db/id']for f in q.get(':question/answer-fields',[])if ':answer-field/correct'not in f])for q in D['questions']if any(':answer-field/correct'not in f for f in q.get(':question/answer-fields',[]))]);print('missing solutions',[(q[':db/id'],q.get(':question/math-academy-id'))for q in D['questions']if not q.get(':question/worked-solution')])
