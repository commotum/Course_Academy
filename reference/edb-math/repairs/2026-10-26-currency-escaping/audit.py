"""Read-only currency-delimiter audit; distinguish complete display math."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/currency-escaping-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,normalize_math_boundaries,validate_math_boundaries
TOKEN=re.compile(r'(?<!\\)\\\[[\s\S]*?\\\]|(?<!\\)\\\([\s\S]*?\\\)|(?P<bad>(?<!\\)\$\$(?:\\,\s*)*\d[^$\n]*?(?<!\\)\$(?!\$))|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$')
legacy=re.compile(r'\\\[/?math\]');found=[];unpaired=[];meta=collections.defaultdict(dict);parents=collections.defaultdict(list);counts=collections.Counter();strings=0
for line in(W/'current.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v']
 if a in ['answer/type','answer-field/type','answer-field/correct','question/math-academy-id','question/id','tutorial/math-academy-id','topic/title','topic/math-academy-id','knowledge-point/title','question-generator/script','db/ident']:meta[e][a]=v
 if a in ['answer-field/choices','question/answer-fields','knowledge-point/questions','knowledge-point/canonical-example','topic/knowledge-points','activity/steps','step/content']:parents[v].append([e,a])
 if not isinstance(v,str):continue
 strings+=1
 bad=[{'span':[m.start(),m.end()],'text':m[0]}for m in TOKEN.finditer(v)if m['bad']is not None];markers=[m[0]for m in legacy.finditer(v)]
 if bad or markers:found.append({**d,'suspects':bad,'legacy_markers':markers});counts[a]+=1
 elif a in ['question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','multistep/content']and'$'in v:
  try:validate_math_boundaries(v,strict=True)
  except ValueError as ex:
   if 'dollar'in str(ex)or'percentage'in str(ex):unpaired.append({**d,'error':str(ex)})
(H/'candidates.json').write_text(json.dumps(found,indent=2)+'\n');(H/'other-delimiter-candidates.json').write_text(json.dumps(unpaired,indent=2)+'\n');(W/'metadata.json').write_text(json.dumps(meta));(W/'parents.json').write_text(json.dumps(parents));report={'basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],'string_values_examined':strings,'known_pattern_fields':len(found),'known_pattern_occurrences':sum(len(d['suspects'])+len(d['legacy_markers'])for d in found),'attributes':dict(counts),'other_delimiter_candidates':len(unpaired)};(H/'audit-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));
for r in found[:35]:print(r['e'],r['a'],r['suspects'],r['legacy_markers'])
print('other errors',collections.Counter(d['error']for d in unpaired))
