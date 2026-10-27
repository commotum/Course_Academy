"""Read-only full current-fact audit, including bare mathematical answers."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/matrix-layout-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import _matrix_layouts,ENV,environment,cells,MATH
meta=collections.defaultdict(dict);parents=collections.defaultdict(list);values=[];allattrs=collections.Counter();counts=collections.Counter()
attrs={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/feedback','multistep/context','multistep/content','assigned-problem/instructions','activity/description','step/content'}
metas={'answer/type','answer/id','answer-field/type','answer-field/correct','answer-field/key','question/id','question/math-academy-id','tutorial/id','tutorial/math-academy-id','topic/title','topic/math-academy-id','knowledge-point/title','knowledge-point/question-generator','question-generator/script','question-generator/id','db/ident'}
links={'answer-field/choices','question/answer-fields','knowledge-point/questions','knowledge-point/canonical-example','topic/knowledge-points','activity/steps','step/content','activity/scope','topic/lesson','multistep/steps','assigned-problem/content'}
for line in (W/'current.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v'];counts['facts']+=1
 if a in metas:meta[e][a]=v
 if a in links and isinstance(v,int):parents[v].append([e,a])
 if not isinstance(v,str):continue
 counts['strings']+=1
 if '\\begin{aligned}' in v or '\\begin{matrix}' in v or '\\eqalign' in v or '\\matrix{' in v:
  allattrs[a]+=1
  if a in attrs:values.append(d)
found=[];residual=[];errors=[]
for d in values:
 try:new=_matrix_layouts(d['v'])
 except ValueError as e:errors.append({**d,'error':str(e)});continue
 if new!=d['v']:found.append({**d,'after':new})
 # Independent broad detector: retain every remaining alignment/matrix's nearest visible context.
 for m in ENV.finditer(new):
  if m[1]!='begin' or m[2]not in ('aligned','matrix'):continue
  span=environment(new,m.start())
  if not span:errors.append({**d,'error':'Unbalanced environment at '+str(m.start())});continue
  left=new[max(0,m.start()-65):m.start()];right=new[span[2]:span[2]+65]
  # Array-like delimiters including control words and invisible or grouped fences.
  if re.search(r'[\[|(]\s*(?:\{\s*)?$|\\(?:vert|lvert|rvert|Vert|lVert|rVert|lbrack|rbrack)\s*(?:\{\s*)?$',left) or re.match(r'\s*\}?\s*(?:\\right\s*)?(?:[\]|)]|\\(?:vert|rvert|lvert|Vert|rVert|lVert|rbrack|lbrack))',right):
   residual.append({'e':d['e'],'a':d['a'],'left':left,'right':right,'tex':new[m.start():span[2]],'grid':cells(new[span[0]:span[1]])})
 if '\\eqalign' in new or '\\matrix{'in new:residual.append({**d,'reason':'legacy layout command'})
for name,v in [('candidates',found),('residual',residual),('errors',errors)]: (H/(name+'.json')).write_text(json.dumps(v,indent=2)+'\n')
(W/'metadata.json').write_text(json.dumps(meta));(W/'parents.json').write_text(json.dumps(parents));(W/'layout-values.json').write_text(json.dumps(values))
summary={**counts,'basis_t':json.loads((W/'current.manifest.json').read_text())['basis_t'],'layout_strings_by_attribute':dict(allattrs),'candidate_fields':len(found),'candidate_attributes':dict(collections.Counter(d['a']for d in found)),'residual_fence_contexts':len(residual),'errors':len(errors)}
(H/'inventory-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
