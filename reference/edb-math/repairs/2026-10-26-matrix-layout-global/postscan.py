"""Re-scan every current string after commit; confirm complete repair coverage."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/matrix-layout-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import _matrix_layouts
fields={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())};counts=collections.Counter();remaining=[];seen=set();scopes={};unexpected=[]
for line in(W/'after.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v'];counts['facts_scanned']+=1
 if a=='activity/scope':scopes[e]=v
 if (e,a)in fields:
  assert v==fields[e,a]['after'],(e,a,'changed after repair');seen.add((e,a))
 if not isinstance(v,str):continue
 counts['strings_scanned']+=1
 if '\\begin{aligned}'not in v and '\\begin{matrix}'not in v:continue
 counts['layout_strings_scanned']+=1
 if a=='answer-field/key':counts['preserved_identity_keys_containing_tex']+=1;continue
 if _matrix_layouts(v)!=v:remaining.append(d)
assert len(seen)==len(fields);(H/'postscan-remaining.json').write_text(json.dumps(remaining,indent=2)+'\n');assert not remaining,('Remaining malformed matrix fields',len(remaining))
meta={int(k):v for k,v in json.loads((W/'metadata.json').read_text()).items()};parents={int(k):v for k,v in json.loads((W/'parents.json').read_text()).items()};topics=set();questions=set();detached=[];contexts={}
for e,a in fields:
 todo=[e];seenparents=set();ctx=[]
 for depth in range(8):
  nxt=[]
  for x in todo:
   if x in seenparents:continue
   seenparents.add(x);m=meta.get(x,{})
   if 'topic/math-academy-id'in m:topics.add(m['topic/math-academy-id']);ctx.append({'entity':x,**m})
   if 'question/id'in m:questions.add(x)
   nxt.extend(p for p,attr in parents.get(x,[]))
   if x in scopes:nxt.append(scopes[x])
  todo=nxt
 contexts[str(e)]=ctx
 if not ctx:detached.append({'entity':e,'attribute':a})
(H/'topic-context.json').write_text(json.dumps(contexts,indent=2)+'\n');(H/'unowned-content.json').write_text(json.dumps(detached,indent=2)+'\n')
report={'basis_t':json.loads((W/'after.manifest.json').read_text())['basis_t'],**counts,'repaired_fields_verified':len(fields),'remaining_confirmed_matrix_layout_defects':len(remaining),'topics_with_repaired_content':len(topics),'question_entities_with_repaired_content_or_choices':len(questions),'content_without_current_lesson_ownership':len(detached),'scope':'Explicit fenced aligned/matrix tables; proper matrix environments, genuine derivations, scalar continuations, and asymmetric sign charts are preserved.'};(H/'postscan.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
