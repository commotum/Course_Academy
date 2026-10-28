import copy,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import validate_math_structure
assert not(H/'commit-intent.json').exists()
changes=json.loads((H/'proposed-changes.json').read_text())+json.loads((H/'tutorial-changes.json').read_text());fields=[];forms=[]
for e,a,before,after,reason in changes:
 validate_math_structure(after);assert re.findall(r'\{\{[^{}]+\}\}',before or'')==re.findall(r'\{\{[^{}]+\}\}',after)
 fields.append({'entity':e,'attribute':a,'before':before,'after':after,'before_sha256':hashlib.sha256((before or'').encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'math_answer':False,'answer_fields':[],'reasons':[reason]});forms.append([kw('db/cas'),e,kw(a),before,after])
for d in json.loads((H/'missing-key-repairs.json').read_text()):
 forms.extend([[kw('db/cas'),d['field'],kw('answer-field/correct'),None,d['answer']],[kw('db/ensure'),d['field'],kw('answer-field/validate')],[kw('db/ensure'),d['answer'],kw('answer/validate')],[kw('db/ensure'),d['question'],kw('question/validate')]])
(H/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');(H/'transaction.edn').write_text(dumps(forms)+'\n')
print('Prepared',len(fields),'content changes and two existing-choice key completions.')
# Complete final content snapshot for rendering/grading, with no invented IDs.
D=json.loads((H/'current.json').read_text());D['questions']=json.loads((H/'proposed-questions.json').read_text())
for activity in D['structure']:
 for s in activity[':activity/steps']:
  c=s[':step/content']
  for f in fields:
   if f['entity']==c[':db/id']and f['attribute']=='tutorial/content':c[':tutorial/content']=f['after']
(H/'proposed.json').write_text(json.dumps(D,indent=2)+'\n')
