"""Read every current fact; keep array-bearing strings and ownership context."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/outer-fences-2026-10-29';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment
meta=collections.defaultdict(dict);parents=collections.defaultdict(list);values=[];counts=collections.Counter();attrs=collections.Counter();contexts=[]
metas={'answer/type','answer/id','answer-field/type','answer-field/correct','answer-field/key','question/id','question/math-academy-id','tutorial/id','tutorial/math-academy-id','topic/title','topic/math-academy-id','knowledge-point/title','knowledge-point/question-generator','question-generator/script','question-generator/id','db/ident'}
links={'answer-field/choices','question/answer-fields','knowledge-point/questions','knowledge-point/canonical-example','topic/knowledge-points','activity/steps','step/content','activity/scope','topic/lesson','multistep/steps','assigned-problem/content'}
for line in(W/'current.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v'];counts['facts']+=1
 if a in metas:meta[e][a]=v
 if a in links and isinstance(v,int):parents[v].append([e,a])
 if not isinstance(v,str):continue
 counts['strings']+=1
 if not any(r'\begin{'+env+'}'in v for env in ['array','aligned','alignedat','gathered','matrix','bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix','cases']):continue
 values.append(d);attrs[a]+=1
 for m in ENV.finditer(v):
  if m[1]!='begin'or m[2]not in ['array','aligned','alignedat','gathered','matrix','bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix','cases']:continue
  s=environment(v,m.start());counts['table_environments']+=1
  if not s:counts['unbalanced_tables']+=1;continue
  contexts.append({'entity':e,'attribute':a,'left':v[max(0,m.start()-60):m.start()],'right':v[s[2]:s[2]+60],'start':m.start(),'end':s[2]})
for n,v in [('metadata',meta),('parents',parents),('array-values',values)]: (W/(n+'.json')).write_text(json.dumps(v))
(H/'array-contexts.json').write_text(json.dumps(contexts,indent=2)+'\n');report={**counts,'basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],'array_strings':len(values),'array_strings_by_attribute':dict(attrs)};(H/'inventory.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
