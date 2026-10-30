"""Candidate repairs change only existing array fence sizing in visible fields."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/array-fences-2026-10-29';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,scalable_array_fences,ENV,environment
meta={int(k):v for k,v in json.loads((W/'metadata.json').read_text()).items()};names={e:v['db/ident']for e,v in meta.items()if'db/ident'in v}
values=json.loads((W/'array-values.json').read_text());props=[];review=[];contexts=[];shapes=collections.Counter();bare_types=collections.Counter()
visible={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/feedback','answer-field/display-key','multistep/context','multistep/content','assigned-problem/instructions','activity/description','step/content'}
for d in values:
 e,a,v=d['e'],d['a'],d['v'];bare=a=='answer/value'and names.get(meta[e].get('answer/type'),'').endswith('/math')
 if a=='answer/value':bare_types[names.get(meta[e].get('answer/type'),'unknown')]+=1
 if a not in visible:
  if a=='answer-field/key'and names.get(meta[e].get('answer-field/type'),'').endswith('/checkbox')and v.startswith('DISPLAY:'):pass
  else:
   if scalable_array_fences(v)!=v:review.append({**d,'reason':'Non-presentation or field identity value; no automatic change'})
   continue
 new=scalable_array_fences(v)if bare else MATH.sub(lambda m:scalable_array_fences(m[0]),v)
 if new!=v:
  # The only permissible bytes added are left/right delimiter-sizing commands.
  strip=lambda x:re.sub(r'\\(?:left|right)(?![A-Za-z])','',re.sub(r'\\(?:left|right)\.','',x))
  assert strip(v)==strip(new),(e,a)
  after_arrays=[];before_arrays=[]
  for text,output in [(v,before_arrays),(new,after_arrays)]:
   for m in ENV.finditer(text):
    if m[1]=='begin'and m[2]=='array':
     span=environment(text,m.start());assert span;output.append(strip(text[m.start():span[2]]))
  assert before_arrays==after_arrays,(e,a,'Array data changed')
  props.append({'entity':e,'attribute':a,'before':v,'after':new,'reason':'Make existing paired array delimiters scalable; preserve complete ordered cells, column rules, expressions and IDs.','bare_math':bare,'arrays_unchanged':len(before_arrays)})
  shapes[a]+=1
 if new==v and scalable_array_fences(v)!=v:review.append({**d,'reason':'Fixed array fences outside protected math; review context before changing'})
(H/'proposals.json').write_text(json.dumps(props,indent=2)+'\n');(H/'manual-review.json').write_text(json.dumps(review,indent=2)+'\n');report={'candidate_fields':len(props),'candidate_entities':len({p['entity']for p in props}),'attributes':dict(shapes),'manual_review':len(review),'answer_array_types':dict(bare_types)};(H/'proposal-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
