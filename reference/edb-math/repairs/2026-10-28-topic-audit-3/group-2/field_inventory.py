import json,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_math_structure,validate_tex
D=json.loads((H/'current.json').read_text());fields={};identities=[];blanks=[];issues=[]
for act in D['activities']:
 for c in act['contents']:
  if ':tutorial/content'in c:fields[c[':db/id'],'tutorial/content']={'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']}
for q in D['questions']:
 for attr in ['question/problem','question/worked-solution']:
  if ':'+attr in q:fields[q[':db/id'],attr]={'entity':q[':db/id'],'attribute':attr,'value':q[':'+attr]}
 counts=collections.Counter(f[':answer-field/key']for f in q.get(':question/answer-fields',[]))
 if any(n>1 for n in counts.values()):identities.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'duplicate_keys':{k:n for k,n in counts.items()if n>1},'fields':[{'entity':f[':db/id'],'key':f[':answer-field/key'],'correct':f.get(':answer-field/correct',{}).get(':db/id')}for f in q[':question/answer-fields']]})
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']!=':answer-field.type/blank':fields[f[':db/id'],'answer-field/key']={'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']}
  else:blanks.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'field':f[':db/id'],'key':f[':answer-field/key'],'canonical':f.get(':answer-field/correct'),'problem':q[':question/problem']})
  for a in f.get(':answer-field/choices',[]):
   fields[a[':db/id'],'answer/value']={'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'}
   if ':answer/feedback'in a:fields[a[':db/id'],'answer/feedback']={'entity':a[':db/id'],'attribute':'answer/feedback','value':a[':answer/feedback']}
for f in fields.values():
 try:(validate_tex if f.get('bare_math')else validate_math_structure)(f['value'])
 except Exception as e:issues.append({**f,'error':str(e)})
(H/'baseline-render-input.json').write_text(json.dumps(list(fields.values()),indent=2)+'\n');(H/'field-identity-issues.json').write_text(json.dumps(identities,indent=2)+'\n');(H/'blank-class-review.json').write_text(json.dumps(blanks,indent=2)+'\n');(H/'structural-issues.json').write_text(json.dumps(issues,indent=2)+'\n');print('fields',len(fields),'duplicate-key questions',len(identities),'blanks',len(blanks),'structural errors',len(issues));print('blank types',collections.Counter(b.get('canonical',{}).get(':answer/type',{}).get(':db/ident')if b.get('canonical')else None for b in blanks))
