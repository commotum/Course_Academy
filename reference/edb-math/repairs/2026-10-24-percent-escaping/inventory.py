"""Inventory every current percent-bearing domain string and its owners."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/percent-escaping'
sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import MATH
meta=collections.defaultdict(dict);owners=collections.defaultdict(list);values={};percents=[];idents={};schema={}
metadata={'answer/id','answer/type','answer-field/id','answer-field/key','answer-field/type','answer-field/correct','question/id','question/math-academy-id','tutorial/math-academy-id','knowledge-point/title','topic/title','topic/math-academy-id','question-generator/script'}
owner_attrs={'answer-field/choices','question/answer-fields','knowledge-point/questions','knowledge-point/canonical-example','topic/knowledge-points','activity/steps','step/content','knowledge-point/question-generator'}
strings=0
for line in (W/'current.jsonl').open():
 r=json.loads(line);e,a,v=r['e'],r['a'],r['v']
 if a=='db/ident':idents[e]=v
 if a in metadata:meta[e][a]=v
 if a in owner_attrs:owners[v].append([e,a])
 if isinstance(v,str):
  strings+=1
  if a in {'answer/value','answer-field/key','question/problem'}:values[e,a]=v
  if '%' in v:percents.append(r)
out=[]
for r in percents:
 v=r['v'];offsets=[];escaped=[];outside=[]
 spans=list(MATH.finditer(v))
 bare_math=r['a']=='answer/value' and idents.get(meta[r['e']].get('answer/type'))==':answer.type/math' and not spans and not v.lstrip().startswith(('$',r'\(',r'\['))
 for i,c in enumerate(v):
  if c!='%':continue
  slashes=0;j=i-1
  while j>=0 and v[j]=='\\':slashes+=1;j-=1
  inside=bare_math or any(m.start()<=i<m.end() for m in spans)
  (escaped if slashes%2 else offsets if inside else outside).append(i)
 if offsets or outside:out.append({**r,'unescaped_math_offsets':offsets,'unescaped_outside_math_offsets':outside,'escaped_percent_count':len(escaped),'metadata':meta[r['e']]})
(W/'metadata.json').write_text(json.dumps(meta)+'\n');(W/'owners.json').write_text(json.dumps(owners)+'\n');(W/'values.json').write_text(json.dumps([{'e':e,'a':a,'v':v}for (e,a),v in values.items()])+'\n');(W/'idents.json').write_text(json.dumps(idents)+'\n')
(H/'percent-inventory.json').write_text(json.dumps(out,indent=2)+'\n')
counts=collections.Counter(r['a']for r in out if r['unescaped_math_offsets']);report={'basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],'domain_strings_scanned':strings,'percent_bearing_fields':len(percents),'fields_with_unescaped_math_percent':sum(bool(r['unescaped_math_offsets'])for r in out),'math_percent_attributes':dict(counts),'outside_percent_attributes':dict(collections.Counter(r['a']for r in out if r['unescaped_outside_math_offsets']))}
(H/'inventory-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
