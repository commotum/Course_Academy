import collections,json,re
from pathlib import Path
H=Path(__file__).resolve().parent;names=dict(json.loads((H/'idents.json').read_text()));issues=[];counts=collections.Counter()
def typ(x):return x.get(':db/ident',names.get(x.get(':db/id')))if isinstance(x,dict)else x
for group,file in [('group-1','current.json'),('group-2','current.json'),('group-3','snapshot.json')]:
 for q in json.loads((H/group/file).read_text())['questions']:
  bykey=collections.Counter(f[':answer-field/key']for f in q.get(':question/answer-fields',[]))
  for f in q.get(':question/answer-fields',[]):
   counts['fields']+=1;fs=f.get(':answer-field/choices',[]);byid={a[':db/id']:a for a in fs};rid=f.get(':answer-field/correct',{}).get(':db/id');base={'group':group,'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'field':f[':db/id'],'key':f[':answer-field/key'],'type':typ(f[':answer-field/type'])}
   if bykey[f[':answer-field/key']]>1:issues.append({**base,'issue':'duplicate-field-key'});counts['duplicate-field-members']+=1
   if rid is None:counts['missing-key']+=1;issues.append({**base,'issue':'missing-key','bank_size':len(fs)});continue
   if rid not in byid:counts['canonical-not-owned']+=1;issues.append({**base,'issue':'canonical-not-owned','answer':rid});continue
   right=byid[rid];v=right[':answer/value'];kind=typ(right[':answer/type'])
   if base['type']==':answer-field.type/blank'and kind==':answer.type/text'and re.search(r'[$\\]|[=^+*/]',v):issues.append({**base,'issue':'math-shaped-blank-typed-text','answer':rid,'value':v});counts['math-shaped-blank-typed-text']+=1
   if kind==':answer.type/math'and re.fullmatch(r"(?:is|is not|isn't|not all|dependent|independent|bounded|unbounded|no solution|no solutions)",v.strip(),re.I):issues.append({**base,'issue':'prose-canonical-typed-math','answer':rid,'value':v});counts['prose-canonical-typed-math']+=1
(H/'field-contracts.json').write_text(json.dumps({'basis_t':json.loads((H/'basis.json').read_text())['basis_t'],'counts':counts,'issues':issues},indent=2)+'\n');print(dict(counts))
for group in ['group-1','group-2','group-3']:
 bad=[x for x in issues if x['group']==group and x['issue']in ['canonical-not-owned','math-shaped-blank-typed-text','prose-canonical-typed-math']];print(group,bad)
