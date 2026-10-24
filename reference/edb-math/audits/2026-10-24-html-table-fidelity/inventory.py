import collections,json,re
from tables import H,R,W,current_tables
attrs={'question/problem','question/worked-solution','tutorial/content','multistep/context','answer/value','answer/feedback','answer-field/key','assigned-problem/instructions'}
meta=collections.defaultdict(dict);owners=collections.defaultdict(list);candidates=[];strings=0;counts=collections.Counter()
for line in(W/'current.jsonl').open():
 r=json.loads(line);e,a,v=r['e'],r['a'],r['v']
 if a in ['question/math-academy-id','tutorial/math-academy-id','question/id','answer/type','answer-field/type','answer-field/correct','knowledge-point/title','topic/title','topic/math-academy-id','question-generator/script']:meta[e][a]=v
 if a in ['answer-field/choices','question/answer-fields','knowledge-point/questions','knowledge-point/canonical-example','topic/knowledge-points','knowledge-point/question-generator']:owners[v].append([e,a])
 if isinstance(v,str):
  strings+=1
  if a in attrs and('<table'in v.lower()or re.search(r'(?m)^\s*\|?\s*:?-{3,}:?\s*\|',v)):candidates.append(r)
out=[]
for r in candidates:
 tables=current_tables(r['v'])
 if tables:out.append({**r,'tables':tables,'metadata':meta[r['e']]});counts.update(t['format']for t in tables)
(W/'inventory.json').write_text(json.dumps(out)+'\n');(W/'metadata.json').write_text(json.dumps(meta)+'\n');(W/'owners.json').write_text(json.dumps(owners)+'\n')
report={'database':'math','basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],'domain_strings_scanned':strings,'fields_with_tables':len(out),'tables_by_format':dict(counts),'fields_by_attribute':dict(collections.Counter(r['a']for r in out))}
(H/'inventory-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
