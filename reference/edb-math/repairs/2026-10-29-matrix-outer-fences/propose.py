"""Repair visible table fences while preserving cells, rules and learner data."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/outer-fences-2026-10-29';sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,scalable_table_fences,_matrix_layouts,ENV,environment,cells,validate_matrix_layouts
meta={int(k):v for k,v in json.loads((W/'metadata.json').read_text()).items()};names={e:v['db/ident']for e,v in meta.items()if'db/ident'in v};parents={int(k):v for k,v in json.loads((W/'parents.json').read_text()).items()}
values=json.loads((W/'array-values.json').read_text());props=[];review=[];excluded=[];shapes=collections.Counter();bare_types=collections.Counter()
visible={'question/problem','question/worked-solution','tutorial/content','answer/value','answer/feedback','answer-field/feedback','answer-field/display-key','multistep/context','multistep/content','assigned-problem/instructions','activity/description','step/content'}
def strip(x):
 x=re.sub(r'\\(?:left|right)(?![A-Za-z])','',re.sub(r'\\(?:left|right)\.','',x))
 x=x.replace('∣','|').replace('‖',r'\|').replace('∥',r'\|')
 return re.sub(r'\\(langle|rangle)\s*',lambda m:'⟨'if m[1]=='langle'else'⟩',x)

def core(text):return _matrix_layouts(text)
def normalize(text):return scalable_table_fences(core(text))
for d in values:
 e,a,v=d['e'],d['a'],d['v'];bare=a=='answer/value'and names.get(meta[e].get('answer/type'),'').endswith('/math')
 if a=='answer/value':
  bare_types[names.get(meta[e].get('answer/type'),'unknown')]+=1
  owners=[f for f,link in parents.get(e,[])if link=='answer-field/choices']
  # Noncanonical blank answers are learner keystrokes; unowned values cannot be
  # established as authored presentation. Preserve both, including their history.
  if not owners or any(names.get(meta[f].get('answer-field/type'),'').endswith('/blank')and meta[f].get('answer-field/correct')!=e for f in owners):
   if normalize(v)!=v:excluded.append({**d,'reason':'Learner/noncanonical blank or unowned answer; preserved'})
   continue
 if a not in visible:
  # Checkbox keys are actual visible option labels, not blank placeholder names.
  if a=='answer-field/key'and names.get(meta[e].get('answer-field/type'),'').endswith('/checkbox'):pass
  else:
   if normalize(v)!=v:review.append({**d,'reason':'Non-presentation or field identity value; no automatic change'})
   continue
 canonical=core(v)if bare else MATH.sub(lambda m:core(m[0]),v)
 new=normalize(v)if bare else MATH.sub(lambda m:normalize(m[0]),v)
 if new!=v:
  assert strip(canonical)==strip(new),(e,a,'Change beyond fence sizing')
  # Independently compare each table's ordered cells, allowing environment names
  # to differ only when a legacy fenced alignment becomes a true matrix.
  grids=[]
  for text in [v,new]:
   payload=[]
   for m in ENV.finditer(text):
    if m[1]!='begin':continue
    span=environment(text,m.start());assert span
    body=strip(text[span[0]:span[1]])
    body=ENV.sub(lambda t:'\\'+t[1]+'{TABLE}',body)
    payload.append(cells(body))
   grids.append(payload)
  assert grids[0]==grids[1],(e,a,'Ordered table cells changed')
  validate_matrix_layouts(new,bare_math=bare)
  props.append({'entity':e,'attribute':a,'before':v,'after':new,'reason':'Make existing table fences scalable; preserve every ordered cell, rule, expression, field and answer identity.','bare_math':bare,'tables_unchanged':len(grids[0]),'legacy_matrix_environment_repair':canonical!=v});shapes[a]+=1
 if new==v and not bare:
  protected=[(m.start(),m.end())for m in MATH.finditer(v)]
  unprotected=[m.start()for m in ENV.finditer(v)if m[1]=='begin'and not any(a<=m.start()<b for a,b in protected)]
  if unprotected and normalize(v)!=v:review.append({**d,'reason':'Table fences outside protected math; inspect context'})
for n,rows in [('proposals',props),('manual-review',review),('preserved-learner-values',excluded)]: (H/(n+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
report={'candidate_fields':len(props),'candidate_entities':len({p['entity']for p in props}),'attributes':dict(shapes),'manual_review':len(review),'preserved_learner_values':len(excluded),'legacy_matrix_environment_repairs':sum(p['legacy_matrix_environment_repair']for p in props),'answer_table_types':dict(bare_types)};(H/'proposal-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
