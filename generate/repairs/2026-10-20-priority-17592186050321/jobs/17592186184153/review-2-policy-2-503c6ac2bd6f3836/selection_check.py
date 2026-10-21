import sys;sys.dont_write_bytecode=True
from audit_math import field,answer
import json,pathlib,collections,hashlib
R=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
def template(r):return r['generation'].get('template')
def params(r):return r['generation']['parameters']
def coverage(records):
 out={}
 for t in 'PRB':
  rs=[r for r in records if template(r)==t];ps=[params(r) for r in rs]
  out[t]={'count':len(rs),'semantic_instances':len({(i['n'],i['s'],i['k']) for i in ps}),**{key:dict(collections.Counter(str(i[key]) for i in ps)) for key in ['n','s','k','constant_first','variable']}}
  if t!='B':out[t].update({'correct_positions':dict(collections.Counter(str(next(j for j,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==answer(r)[':answer/id'])) for r in rs)), 'factors':dict(collections.Counter(f for i in ps for f in i['factors'])),'omitted_cells':dict(collections.Counter(str((i['omitted_row'],i['omitted_col'])) for i in ps)),'offsets':dict(collections.Counter(str(i['offset']) for i in ps))})
 return out
accepted=load('delivery/accepted.json')
# Selection logic from engine/rust/question_selection.rs, synthetic IDs because actual IDs don't exist before publication.
# Generated moderate candidates get monotonic IDs after current highest inventory ID. No database writes.
inventory=load('../source/inventory.json') if False else json.loads((R.parent/'source/inventory.json').read_text())
base=max(q[':db/id'] for q in inventory['questions'])+100
pool={base+j:r for j,r in enumerate(accepted)}
all_inventory={q[':db/id']:q for q in inventory['questions']}
def usable(q):
 fs=q.get(':question/answer-fields',[])
 if not fs:return False
 for f in fs:
  if not f.get(':answer-field/correct'):return False
  correct=f[':answer-field/correct'].get(':answer/id')
  if not any(a.get(':answer/id')==correct for a in f.get(':answer-field/choices',[])):return False
 return not q.get(':question/retired',False)
inventory_by_id={id:q for id,q in all_inventory.items() if usable(q)}

def band(q):
 value=q.get(':question/difficulty');return value.get(':db/ident') if isinstance(value,dict) else value

def select(candidates,distribution,seed):
 candidates=sorted(set(candidates))
 if distribution is None:return candidates[0] if candidates else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def uniform(offset):return (int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 bands=[[],[],[]];unknown=[]
 for id in candidates:
  q=pool[id]['question'] if id in pool else inventory_by_id[id]
  b=band(q)
  if b is None:unknown.append(id)
  else:bands[[':question.difficulty/easy',':question.difficulty/moderate',':question.difficulty/hard'].index(b)].append(id)
 total=sum(w for w,rs in zip(distribution,bands) if rs)
 if total>0:
  draw=uniform(0)*total;chosen=None
  for j,w in enumerate(distribution):
   if not bands[j] or w==0:continue
   chosen=j
   if draw<w:break
   draw-=w
  eligible=bands[chosen]
 else:eligible=unknown
 return eligible[int(uniform(8)*len(eligible))] if eligible else None
scenarios=[]
for label,weights,seen in [('positive_moderate',[6,3,1],set()),('moderate_only',[0,1,0],set()),('moderate_disabled',[1,0,1],set()),('half_seen',[6,3,1],{i for j,i in enumerate(pool) if j%2==0}),('unconfigured',None,set())]:
 candidates=sorted((set(pool)|set(inventory_by_id))-seen);draws=[select(candidates,weights,'review-20261020-'+str(j)) for j in range(1000)]
 delivered=[pool[i] for i in draws if i in pool]
 scenarios.append({'scenario':label,'weights':weights,'seen_synthetic_ids':sorted(seen),'draws':draws,'draw_count':len(draws),'generated_selected':len(delivered),'inventory_selected':sum(i in inventory_by_id for i in draws),'none':draws.count(None),'generated_coverage':coverage(delivered),'selected_ids_are_synthetic':True})
save('selection-results.json',{'implementation':'faithful read-only reproduction of select, sorting numeric IDs, SHA256 53-bit draws, bands before within-band selection; candidates prefiltered as fresh usable','captured_basis':inventory['basis'],'source_path':'engine/rust/question_selection.rs','candidate_filter_source':'engine/rust/learning.rs validate_practice_question/validate_response_question and candidate construction at lines 595-603','inventory_excluded':[q.get(':question/math-academy-id') for id,q in all_inventory.items() if id not in inventory_by_id],'scenarios':scenarios,'limits':['No captured live policy or learner history. Synthetic increasing IDs model appended records; real entity IDs and task seeds alter exact draws.','Unconfigured policy returns smallest ID, often original source content; moderate weight zero excludes generated moderate records by design.','Captured usable inventory includes q-71169, q-133291, q-71167; four other records excluded for missing fields or canonical answer. Runtime schema ordinary-question classification is assumed from captured source status.','No raw sampler rejection/resampling branch: offset zero avoidance is a prechoice domain filter; all generated records are emitted.']})
print([(s["scenario"],s["generated_selected"],s["inventory_selected"],s["none"]) for s in scenarios])
