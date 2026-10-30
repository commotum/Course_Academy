import json,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());props=json.loads((H/'proposals.json').read_text());evidence=[]
for q in S['questions']:
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']!=':answer-field.type/checkbox' or not f[':answer-field/key'].startswith('$'):continue
  before=f[':answer-field/key'];after=before.replace('{R}',r'{\mathbb{R}}').replace(r'\in R',r'\in \mathbb{R}')
  after=re.sub(r'([ABC]=)(?<!\\)\{',r'\1\\{',after)
  if not r'\end{gathered}'in after and after.endswith('}$')and not after.endswith(r'\}$'):after=after[:-2]+r'\}$'
  if after!=before:props.append({'entity':f[':db/id'],'attribute':'answer-field/key','before':before,'after':after,'reason':'Restore archived visible set braces and blackboard R in checkbox statement labels; preserve line wrapping, field IDs, option banks, and true/false keys.'});evidence.append({'question':q[':db/id'],'field':f[':db/id'],'source_identity':q[':question/math-academy-id'],'mathematical_statement_unchanged':True})
assert len({(p['entity'],p['attribute'])for p in props})==len(props)
# No mathematical blanks remain typed as text. No valid existing answer value is replaced.
assert not any(p['attribute']in['answer/value','answer/id','answer-field/id','question/id']for p in props)
(H/'proposals.json').write_text(json.dumps(props,indent=2)+'\n');(H/'statement-label-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');(H/'topology-proposals.json').write_text(json.dumps([{'operation':'retract','entity':17592186120218,'attribute':'question/answer-fields','value':17592186117469,'retain_field_and_answer_entities':True,'reason':'One source radio widget; old duplicate selection field unused in retained learner history (parent proof); keep complete replacement17592186390835.'}],indent=2)+'\n');print('Final proposals',len(props),'statement labels',len(evidence))
