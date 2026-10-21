import json,collections,re,hashlib
from pathlib import Path
from review_math import prompt,check,correct_index,matrices
ROOT=Path(__file__).resolve().parent

def load(p):return json.loads((ROOT/p).read_text())
def save(p,v):(ROOT/p).write_text(json.dumps(v,indent=2,default=str)+'\n')
def stats(rs):
 vals=collections.defaultdict(collections.Counter)
 for r in rs:
  p=r['generation']['parameters'];v=p['candidates'][p['correct_index']]
  for k,x in zip(('sx','sy','bx','by'),v):vals[k][x]+=1
 return {'count':len(rs),'family_counts':dict(collections.Counter(r['generation']['response_template'] for r in rs)),'profile_counts':dict(collections.Counter(r['generation']['template'] for r in rs)),'positions':dict(collections.Counter(correct_index(r['question']) for r in rs)),'distinct_rrefs':len({str(prompt(r['question']).rref()[0]) for r in rs}),'values':{k:dict(v) for k,v in vals.items()}}
sets={name:load(p) for name,p in [('fresh_raw','independent-samples.json'),('fresh_delivered','delivery-independent/accepted.json'),('batch_raw','runner-batch.json'),('batch_delivered','delivery-batch/accepted.json'),('controls_raw','focused-controls.json'),('controls_delivered','delivery-controls/accepted.json')]}
save('coverage-results.json',{k:stats(v) for k,v in sets.items()})
probes=[]
for name,rs in sets.items():
 groups=[('all',rs,'overall')]+[(f,[r for r in rs if r['generation']['response_template']==f],'within_template') for f in ('matrix','vector')]
 # Probe recognisable source-coefficient profiles, especially the two added profiles.
 groups += [(t,[r for r in rs if r['generation']['template']==t],'other_recognizable_subgroup') for t in sorted({r['generation']['template'] for r in rs})]
 for sub,records,scope in groups:
  if not records:continue
  for cue in ('first authored option','shortest TeX','most minus signs','most zero entries'):
   hits=0
   for r in records:
    bank=r['question'][':question/answer-fields'][0][':answer-field/choices'];vs=[a[':answer/value'] for a in bank]
    if cue=='first authored option':idx=0
    elif cue=='shortest TeX':idx=min(range(5),key=lambda j:len(vs[j]))
    elif cue=='most minus signs':idx=max(range(5),key=lambda j:vs[j].count('-'))
    else:idx=max(range(5),key=lambda j:sum(x==0 for x in matrices(vs[j])[0]))
    hits+=idx==correct_index(r['question'])
   probes.append({'cue':cue,'subgroup':name+':'+sub,'scope':scope,'strategy':'Select '+cue+'; break ties by authored order.','correct':hits,'total':len(records),'baseline':.2,'disposition':'not_predictive','conclusion':'Baseline: 1/5 uniform guess. Small subgroups do not establish a predictor. Added profiles have separate 10-seed controls. The unchanged code chooses a random correct slot before exchangeable tuples; values are not conditioned on the correct slot. Actual UI additionally shuffles. No tested rule solves the entire batch.','sample_refs':['decision-probe-results.json',{'fresh_raw':'independent-samples.json','fresh_delivered':'delivery-independent/accepted.json','batch_raw':'runner-batch.json','batch_delivered':'delivery-batch/accepted.json','controls_raw':'focused-controls.json','controls_delivered':'delivery-controls/accepted.json'}[name]]})
save('decision-probe-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python decision_review.py','seeds':'audit.py and focused_controls.py','probes':probes})
selection={}
for name,rs in sets.items():
 if not name.endswith('_delivered'):continue
 c=collections.Counter()
 for n in range(300):
  digest=hashlib.sha256(f'course-academy/question-selection/v1/review-revision-96745-{n}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53;c[int(u*len(rs))]+=1
 # Sequential without replacement: caller excludes seen/current prefix, so every delivered case eventually reachable.
 selection[name]={'pool_size':len(rs),'trials':300,'index_counts':dict(c),'support_preserved':len(c)==len(rs),'selected_family_draws':dict(collections.Counter({f:sum(c[j] for j,r in enumerate(rs) if r['generation']['response_template']==f) for f in {r['generation']['response_template'] for r in rs}})),'sequential_exhaustion':{'eligible_after_all_seen':0,'excluded_by':'identity only; no answer/profile-aware exclusion'}}
save('learner-selection-results.json',{'source':'engine/rust/question_selection.rs select(), weights_for_phase(), seen_before_task()','implementation_sha256':hashlib.sha256(Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs').read_bytes()).hexdigest(),'selection':selection,'basis':5370,'assumptions':['Hypothetical fresh learner; all provided generated records hard, positive hard weight; deterministic native SHA256 hard-band index draw reproduced read-only.','IDs are provisional unique sorted positions; unavailable prospective entity IDs only permute support.','Zero hard weight yields no eligible rated hard records; no active weights and history are provided. No-policy fallback selects smallest eligible entity; repeated current prefix/history exclusion consumes that ordered pool.'],'limits':['No claim about actual live learner or later inventory. All applicable stages examined under captured inputs and explicit policy conditions; future weights/history/IDs are not observed.']})
i=load('inventory-audit.json');i['instance_math_checks']=[check({'question':q,'generation':{'template':'captured non-source; generation metadata unavailable'}}) for q in i['other_records']];i['finding_scan']='Retained finding is absent source API/profile coverage, not an erroneous generated item. Both formerly missing sources are original source records in captured inventory. All 5 non-source stored questions independently pass math; no affected generated record demonstrated. Historical seed replay untested: captured questions omit generation metadata.';save('inventory-audit.json',i)
print(json.dumps({'batch':stats(sets['batch_delivered']),'new_profiles':[p for p in probes if p['subgroup'] in ('controls_delivered:q-74625','controls_delivered:q-131634')],'perfect_nontrivial_probes':[(p['subgroup'],p['cue'],p['correct'],p['total']) for p in probes if p['total']>2 and p['correct']==p['total']],'inventory_math_failures':[c for c in i['instance_math_checks'] if c['errors']]},default=str))
