import json,re
from pathlib import Path
h=Path(__file__).resolve().parent;values={}
for g,f in [('group-1','items.json'),('group-2','fields.json')]:
 for row in json.loads((h/g/f).read_text()):
  e,a,v=row[:3];values[e,a]=v
for p in json.loads((h/'group-3/fields.json').read_text()):values[p['entity'],p['attribute']]=p['value']
for g,f in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:
 for q in json.loads((h/g/f).read_text())['questions']:
  for field in q.get(':question/answer-fields',[]):values[field[':db/id'],'answer-field/key']=field[':answer-field/key']
for n in ['flagged','group-1','group-2','group-3','group-3/checkbox-repair']:
 for p in json.loads((h/n/'approved-proposals.json').read_text()):
  if isinstance(p['after'],str):values[p['entity'],p['attribute']]=p['after']
rx=re.compile(r'\\begin\{aligned\}\s*\[(?!\s*[tbc]\s*\])');bad=[{'entity':e,'attribute':a}for (e,a),v in values.items()if rx.search(v)];assert not bad,bad
(h/'aligned-prefix-final-scan.json').write_text(json.dumps({'scope_basis_t':9047,'after_reviewed_changes':True,'unique_text_attributes_checked':len(values),'unprotected_visible_aligned_prefixes':bad},indent=2)+'\n');print('No unprotected aligned labels in',len(values),'retained/repaired text attributes.')
