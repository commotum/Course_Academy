from reviewlib import *
from collections import defaultdict,Counter
from copy import deepcopy

def load(n):return json.load(open(ROOT/n))
def summarize(records):
 xs=[examine(r) for r in records]
 assert all(not x['errors'] for x in xs)
 return {'count':len(xs),'subsets':dict(Counter(x['selected'] for x in xs)), 'labels':{c:{'selected':sum(c in x['selected'] for x in xs),'unselected':sum(c not in x['selected'] for x in xs)} for c in 'ABC'},'templates':{str(neg):{'count':len(ys),'subsets':dict(Counter(x['selected'] for x in ys))} for neg in {x['negate'] for x in xs} for ys in [[x for x in xs if x['negate']==neg]]}}

def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 with (ROOT/'commands.log').open('a') as f:f.write(json.dumps([str(x) for x in args])+'\n'+p.stdout+p.stderr+f'\nexit={p.returncode}\n')
 assert not p.returncode,p.stderr
 return p
fresh=[]
for seed in (20261021,37193):
 stats={};rs=g.batch('easy',5,seed,stats=stats);save(f'fresh-{seed}.json',rs)
 assert rs==g.batch('easy',5,seed)
 run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',ROOT/f'fresh-{seed}.json','--source',JOB/'source/source.json','--inventory',JOB/'source/inventory.json','--difficulty','easy','--output',ROOT/f'fresh-{seed}','--asset-root',PKG,'--math-root','/media/jake/SSD/EDB/math'])
 after=load(f'fresh-{seed}/accepted.json');assert len(after)==5
 fresh.append({'seed':seed,'stats':stats,'before':summarize(rs),'after':summarize(after)})
 assert all(v['selected'] and v['unselected'] for v in summarize(after)['labels'].values())
stages={n:summarize(load(p)) for n,p in [('raw_before_nonempty','pre-policy-samples.json'),('normal_pool_after_rejection','normal-batch.json'),('independent_before_delivery','independent-samples.json'),('independent_after_delivery','delivery-independent/accepted.json'),('runner_before_delivery','runner-batch.json'),('runner_after_delivery','delivery-batch/accepted.json')]}
inv=json.load(open(JOB/'source/inventory.json'));rated=sorted([q for q in inv['questions'] if q.get(':question/difficulty')],key=lambda q:q[':db/id']);unrated=[q for q in inv['questions'] if not q.get(':question/difficulty')]
assert all(enum(q[':question/difficulty'])==':question.difficulty/easy' for q in rated)
# Selection reproduction uses actual branch's ordering/hash, no invented history.
def selected(q):
 return ''.join(sorted(re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1] for f in q.get('question',q)[':question/answer-fields'] if value(f)=='true'))
selection=[]
for n in range(32):
 seed=f'review-1-selection-20261021-{n}';d=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);q=rated[int(u*len(rated))]
 selection.append({'seed':seed,'entity_id':q[':db/id'],'question_id':q[':question/id'],'subset':selected(q)})
selection_report={'implementation':'engine/rust/question_selection.rs:125-199; reviewed actual source','captured_basis':inv['basis'],'rated_easy_count':len(rated),'unrated_count':len(unrated),'full_rated_subsets':dict(Counter(selected(q) for q in rated)),'fresh_pool_assumption':'No learner-history exclusions; seen_before_task excludes entity IDs. All rated are easy, so any positive easy weight chooses uniformly within easy. Zero easy weight never falls back to rated easy; unrated may be used. Missing distribution selects lowest entity ID.','unconfigured_first_entity':rated[0][':db/id'],'simulation':selection,'incoming_batch':'All five easy records survive. Positive easy weight preserves equal conditional weight among new five. No IDs assigned read-only, so future exact hash-to-ID mapping cannot be computed.','limitations':'No actual learner history, configured policy or new database entity IDs captured; no claim that arbitrary history subsets preserve all cases.'}
# Reproduce all five captured non-source generated records; original source excluded.
normalized=load('inventory-identity/accepted.json');stored={q[':question/id']:q for q in inv['questions']};affected=[]
for r in normalized:
 q=r['question'];s=stored[q[':question/id']]
 assert selected(q)==selected(s) and 'C' in selected(q)
 # Ensure normalized content identity, fields and full solution match stored data.
 assert q[':question/problem']==s[':question/problem'] and q[':question/worked-solution']==s[':question/worked-solution']
 stored_fields={re.search(r'\$([ABC])\s*=',t[':answer-field/key'])[1]:t for t in s[':question/answer-fields']}
 for f in q[':question/answer-fields']:
  t=stored_fields[re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]]
  assert f[':answer-field/key']==t[':answer-field/key'] and value(f)==value(t)
 r['generation']['review_reproduction']={'stored_entity_id':s[':db/id'],'inventory_basis':inv['basis'],'method':'explicit stored matrix parameters, exact worked-solution match, actual publisher-normalized identity','original_seed':'not captured; seed 0 is reconstruction only'}
 affected.append({'question_id':q[':question/id'],'entity_id':s[':db/id'],'finding':'Member of the historical five captured non-source generated records, all of which select C. This retained finite-pool defect does not affect every original/source item or the revised incoming batch.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_probe.py; run check_delivery.py --input inventory-reproduction-input.json --source ../source/source.json --inventory inventory-empty-for-identity-check.json --difficulty easy --output inventory-identity --asset-root ../workspace --math-root /media/jake/SSD/EDB/math; run stage_audit.py','evidence_path':'generated-records.json'})
save('generated-records.json',normalized);save('affected-inventory.json',{'affected_questions':affected})
save('delivery-analysis.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python stage_audit.py','stages':stages,'fresh_batches':fresh,'selection':selection_report,'publication_preparation':'Absent, as permitted before preparation; actual read-only shared prepare_records used.','inventory_status':'All five captured non-source records reconstructed with exact normalized IDs and content; historical defect retained and listed. Full captured bank has counterexamples.','limits':['Captured inventory basis 5356 can change.','Original incomplete radio remains explicitly unsupported; source records were not marked generated.','No publication or database mutation.']})
probes=[]
def probe(group,name,scope,refs):
 if not group:return
 infos=[examine(r) for r in group]
 for label in 'ABC':
  successes=sum(label in x['selected'] for x in infos)
  probes.append({'cue':'visible label '+label,'subgroup':name,'scope':scope,'strategy':'Always check '+label+'; other labels still require classification.','correct':successes,'total':len(group),'baseline':4/7,'disposition':'not_predictive','conclusion':f'Baseline 4/7 is a label-selected probability for independent fair classifications conditioned on a nonempty subset. {successes}/{len(group)} selected. '+('Both checkbox actions occur.' if 0<successes<len(group) else 'This tiny subgroup has no within-group counterexample; one/two observed items do not establish a reusable shape/polarity rule. Broader shape controls below test the same cue.'),'sample_refs':refs})
for path,name in [('delivery-batch/accepted.json','exact revised batch'),('delivery-independent/accepted.json','fresh control')]:
 rs=load(path);probe(rs,name,'overall',[path])
 for neg in [False,True]:probe([r for r in rs if ('**not**' in r['question'][':question/problem'])==neg],name+' / '+('not in' if neg else 'in'),'within_template',[path])
 if name=='fresh control':
  groups=defaultdict(list)
  for r in rs:
   x=examine(r);groups[json.dumps([x['negate'],[y['shape'] for y in x['rows']]])].append(r)
  # Broader unchanged prior control covers all seven subsets within each profile;
  # supplement small fresh groups rather than treating n=8 as exhaustive.
  prior=load('prior-unaffected/delivery-independent/accepted.json')
  for sig,group in groups.items():
   pg=[r for r in prior if json.dumps([examine(r)['negate'],[y['shape'] for y in examine(r)['rows']]])==sig]
   probe(group+pg,'shape and polarity '+sig,'other_recognizable_subgroup',[path,'prior-unaffected/delivery-independent/accepted.json'])
   hist=Counter(examine(r)['selected'] for r in group+pg);best,n=hist.most_common(1)[0]
   probes.append({'cue':'matrix shapes plus prompt polarity','subgroup':sig,'scope':'other_recognizable_subgroup','strategy':'Always choose fixed subset '+best,'correct':n,'total':len(group+pg),'baseline':1/7,'disposition':'not_predictive','conclusion':'Baseline 1/7 guesses one of seven eligible nonempty subsets. Retrospective best fixed subset has counterexamples; shape does not fix selected count or labels.','sample_refs':[path,'prior-unaffected/delivery-independent/accepted.json']})
save('shortcut-probes.json',probes)
# Consolidate all controlled pairs for actual UI and real grader, no homemade substitution.
save('render-counterfactual-records.json',load('counterfactual-records.json')+load('c-counterfactual-records.json'))
save('final-grader-input.json',load('grader-input.json')+load('c-counterfactual-grader-input.json'))
save('scope-results.json',{'source_refs':['tutorial 137b0909-9a5e-5edf-8019-24e803307903, conditions I and II'],'current_changes':'Only finite-pool rejection changed; sampler, generate, sources and solutions unchanged.','fresh_samples':104,'current_runner':5,'scope':'Three ordinary integer matrices. Classification only, no row operations or reduced-echelon constraint. Shape profiles from complete easy sources; entry magnitudes -9..9 keep comparable workload. Relevant counterfactuals use equal/left leading columns, irrelevant ones use trailing entries.','errors':[]})
print(json.dumps({'stages':{k:{'count':v['count'],'labels':v['labels']} for k,v in stages.items()},'fresh_batch_seeds':[x['seed'] for x in fresh],'probes':len(probes),'historical_affected':len(affected),'selection_candidates':len(rated)}))
