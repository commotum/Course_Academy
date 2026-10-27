"""Full-current-fact inventory of table roles and lost operator structure."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells,MATH,normalize_limit_operators
attrs={'tutorial/content','question/problem','question/worked-solution','answer/value','answer/feedback','answer-field/feedback','multistep/context','multistep/content','assigned-problem/instructions'}
metas={'answer/type','answer/id','question/id','question/math-academy-id','tutorial/math-academy-id','topic/math-academy-id','topic/title','knowledge-point/title','knowledge-point/question-generator','question-generator/script','activity/scope','db/ident'}
links={'topic/knowledge-points','knowledge-point/questions','knowledge-point/canonical-example','question/answer-fields','answer-field/choices','answer-field/correct','activity/steps','step/content','multistep/steps','assigned-problem/content'}
meta=collections.defaultdict(dict);parents=collections.defaultdict(list);counts=collections.Counter();values=[];otherattrs=collections.Counter()
for line in(W/'current.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v'];counts['facts']+=1
 if a in metas:meta[e][a]=v
 if a in links and isinstance(v,int):parents[v].append([e,a])
 if not isinstance(v,str):continue
 counts['strings']+=1
 if '\\begin{'in v or '\\eqalign'in v or re.search(r'(?<![A-Za-z])(?:lim|det)(?:[_{(]|\s*\\)',v):
  otherattrs[a]+=1
  if a in attrs:values.append(d)
(W/'metadata.json').write_text(json.dumps(meta));(W/'parents.json').write_text(json.dumps(parents));(W/'values.json').write_text(json.dumps(values))
tables=[];operator=[];malformed=[];envcounts=collections.Counter()
for d in values:
 v=d['v'];maths=[(0,len(v),v)]if d['a']=='answer/value'and meta[d['e']].get('answer/type')==17592186045498 else[(m.start(),m.end(),m[0])for m in MATH.finditer(v)]
 for start,end,tex in maths:
  fixed=normalize_limit_operators(tex)
  if fixed!=tex:operator.append({'e':d['e'],'a':d['a'],'span':[start,end],'before':tex,'after':fixed})
 for m in ENV.finditer(v):
  if m[1]!='begin':continue
  if m[2]not in ('aligned','matrix','bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix','array','cases','alignedat'):continue
  envcounts[m[2]]+=1;span=environment(v,m.start())
  if not span:malformed.append({'e':d['e'],'a':d['a'],'start':m.start(),'reason':'Unclosed/mismatched environment'});continue
  body=v[span[0]:span[1]]
  if m[2]in ('array','alignedat'):body=re.sub(r'^\s*\{[^{}]*\}','',body,count=1)
  grid=cells(body)
  if not grid:malformed.append({'e':d['e'],'a':d['a'],'start':m.start(),'reason':'Unparseable table cells'});continue
  if len(grid)<2:continue
  width=max(map(len,grid));ragged=len({len(r)for r in grid})>1
  # A relation-bearing derivation is not a source data table.
  relation=any(re.search(r'(?<!\\)[=<>]|\\(?:approx|sim|leq?|geq?|equiv|Rightarrow|iff|implies)\b',c)for row in grid for c in row)
  if (m[2]=='aligned'and width>=3 and not relation)or(ragged and m[2]in ('matrix','bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix')):
   tables.append({'e':d['e'],'a':d['a'],'env':m[2],'span':[m.start(),span[2]],'rows':grid,'ragged':ragged,'left':v[max(0,m.start()-90):m.start()],'right':v[span[2]:span[2]+90]})
for name,rows in [('table-candidates',tables),('limit-operator-candidates',operator),('malformed-structure',malformed)]: (H/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
report={'basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],**counts,'environment_counts':dict(envcounts),'table_candidates':len(tables),'table_fields':len({(d['e'],d['a'])for d in tables}),'limit_operator_blocks':len(operator),'limit_operator_fields':len({(d['e'],d['a'])for d in operator}),'malformed_structures':len(malformed),'layout_or_operator_attributes':dict(otherattrs)};(H/'inventory-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
