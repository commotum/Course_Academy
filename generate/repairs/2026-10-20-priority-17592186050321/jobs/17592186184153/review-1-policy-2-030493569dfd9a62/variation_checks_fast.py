"""Independent coverage, cue subgroup and read-only selection audit."""
import sys;sys.dont_write_bytecode=True
import json,pathlib,collections,hashlib,math,random
from audit_math import tex,field,answer,V,S
from functools import lru_cache
tex=lru_cache(maxsize=None)(tex)
@lru_cache(maxsize=None)
def cached_values(choice_strings):
 return [tex(a).subs(V['C'],0) for a in choice_strings]
R=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((R/n).read_text())
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
raw=load('samples.json');accepted=load('delivery/accepted.json');batch=load('runner-batch.json');delbatch=load('batch-delivery/accepted.json')
# Publisher strips generation? Preserve metadata by question content/ID if needed.
byid={r['question'][':question/id']:r for r in raw+batch}
def restore(rs):
 for r in rs:
  if 'generation' not in r:r['generation']=byid[r['question'][':question/id']]['generation']
 return rs
accepted=restore(accepted);delbatch=restore(delbatch)
sets={'raw':raw,'delivered':accepted,'runner':batch,'runner_delivered':delbatch}
allcoverage={name:coverage(rs) for name,rs in sets.items()}
save('coverage.json',allcoverage)
probes=[]
# Cues use displayed content only. Groups reflect recognizable template, exponent, sign and term order.
for stage,records in [('raw',raw),('delivered',accepted),('runner_delivered',delbatch)]:
 for t in 'PR':
  rs=[(j,r) for j,r in enumerate(records) if template(r)==t]
  groups=[('all',rs)]
  for key in ('n','s','constant_first'):
   for value in sorted(set(str(params(r)[key]) for _,r in rs)):
    groups.append((key+'='+value,[(j,r) for j,r in rs if str(params(r)[key])==value]))
  for label,group in groups:
   if not group:continue
   for mode in ('tex_length','visible_length','constant_row_frequency','power_coefficient_rank'):
    for rank in (range(5) if mode.endswith('length') else range(3)):
     correct=0;refs=[]
     for idx,r in group:
      choices=field(r)[':answer-field/choices'];p=params(r);x=V[p['variable']]
      vals=cached_values(tuple(a[':answer/value'] for a in choices))
      if mode=='tex_length':keys=[len(a[':answer/value']) for a in choices]
      elif mode=='visible_length':keys=[len(str(v)) for v in vals]
      elif mode=='constant_row_frequency':
       constants=[S.expand(v).coeff(x,1) for v in vals];cnt=collections.Counter(constants);keys=[-cnt[c] for c in constants]
      else:
       power=(-S.Rational(p['n'],2) if t=='R' else p['n'])+1
       coefficients=[v.expand().coeff(x**power) for v in vals];sortedc=sorted(set(abs(v) for v in coefficients));keys=[sortedc.index(abs(c)) for c in coefficients]
      ordered=sorted(range(len(choices)),key=lambda j:(keys[j],j))
      if mode=='power_coefficient_rank':
       eligible=[j for j,k in enumerate(keys) if k==rank];chosen=eligible[0] if eligible else -1
      else:chosen=ordered[min(rank,len(ordered)-1)]
      win=chosen>=0 and choices[chosen][':answer/id']==answer(r)[':answer/id'];correct+=win
      refs.append({'sample_index':idx,'chosen_index':chosen,'correct':win})
     probes.append({'stage':stage,'template':t,'subgroup':label,'cue':mode,'rank':rank,'correct':correct,'total':len(group),'rate':correct/len(group),'baseline':0.2,'scope':'within_template' if label=='all' else 'other_recognizable_subgroup','trials':refs})
save('shortcut-results.json',probes)
strong=[{k:v for k,v in p.items() if k!='trials'} for p in probes if p['total']>=25 and p['rate']>=0.6]
save('shortcut-strongest.json',sorted(strong,key=lambda x:-x['rate']))
# Selection logic from engine/rust/question_selection.rs, synthetic IDs because actual IDs don't exist before publication.
# Generated moderate candidates get monotonic IDs after current highest inventory ID. No database writes.
inventory=load('../source/inventory.json') if False else json.loads((R.parent/'source/inventory.json').read_text())
base=max(q[':db/id'] for q in inventory['questions'])+100
pool={base+j:r for j,r in enumerate(accepted)}
inventory_by_id={q[':db/id']:q for q in inventory['questions']}
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
save('selection-results.json',{'implementation':'faithful read-only reproduction of select, sorting numeric IDs, SHA256 53-bit draws, bands before within-band selection; candidates prefiltered as fresh usable','captured_basis':inventory['basis'],'source_path':'engine/rust/question_selection.rs','scenarios':scenarios,'limits':['No captured live policy or learner history. Synthetic increasing IDs model appended records; real entity IDs and task seeds alter exact draws.','Unconfigured policy returns smallest ID, often original source content; moderate weight zero excludes generated moderate records by design.','Inventory records lack worked solutions in capture; assumption of usable inventory candidates is conditional.','No raw sampler rejection/resampling branch: offset zero avoidance is a prechoice domain filter; all generated records are emitted.']})
print(json.dumps({'coverage_counts':{k:{t:v['count'] for t,v in d.items()} for k,d in allcoverage.items()},'max_probe_n25':max((p['rate'] for p in probes if p['total']>=25),default=None),'strongest':sorted(strong,key=lambda x:-x['rate'])[:5]}))
