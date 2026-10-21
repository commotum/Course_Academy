import sys,json,pathlib,importlib.util,hashlib,collections,subprocess
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
spec=importlib.util.spec_from_file_location('g',J/'workspace/17592186229165.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
before=dict(h=1,k=1,f=1,k2=2,f2=1,v=0)
after=dict(h=1,k=2,f=1,k2=1,f2=1,v=0)
r=g.generate('hard',seed=90211,template='mixed',parameters=before)
try:
 bad=g.generate('hard',seed=90211,template='mixed',parameters=after);error=None
except ValueError as e:error=str(e)
save('minimal-role-counterexample.json',{'command':sys.executable+' '+str(R/'focused_checks.py'),'before_parameters':before,'after_parameters':after,'template':'mixed','seed':90211,'before_record':r,'after_error':error,'mathematical_expected':'Both orders have forcing e^x+e^(2x), y(0)=0, y_c=Ae^x; unique solution (x-1)e^x+e^(2x). Only displayed order changes.','rule_to_change':'Treat forcing components as exchangeable. Allow the resonant role in either position; derive trial, derivative, explanations and coefficient equations from each component\u2019s equality to h rather than requiring first-component resonance.'})
save('minimal-role-record.json',[r])
samples=load(R/'independent-samples.json');hard=[z for z in samples if z['question'][':question/difficulty']==':question.difficulty/hard'];save('independent-hard.json',hard)
# Reproduce complete generated records corresponding to inventory UUIDs, without calling DB helpers.
inventory=load(J/'source/inventory.json');byid={q[':question/id']:q for q in inventory['questions']}
captured=load(J/'workspace/17592186229165/reference/replenishment/basis-2525/generated.json')
reproduced=[];affected=[];comparison=[]
for old in captured:
 gen=old['generation'];fresh=g.generate(old['question'][':question/difficulty'].split('/')[-1],seed=gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
 stored=byid.get(fresh['question'][':question/id']);assert stored
 equal=(fresh==old)
 assert equal and stored[':question/problem']==fresh['question'][':question/problem'] and stored[':question/worked-solution']==fresh['question'][':question/worked-solution']
 assert [a[':answer/value'] for a in stored[':question/answer-fields'][0][':answer-field/choices']]==[a[':answer/value'] for a in fresh['question'][':question/answer-fields'][0][':answer-field/choices']]
 reproduced.append(fresh)
 p=gen['parameters'];assert p['k2']!=p['h']
 comparison.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'complete_captured_generation_match':equal,'parameters':p,'template':gen['template'],'second_term_nonresonant':True})
 if gen['template']=='mixed':
  affected.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'finding':'Stored mixed hard instance belongs to a cohort fixing resonance to the first component; the last exponential always receives an ordinary trial without an exponent comparison. This is a structural practice-pool shortcut, not an incorrect individual key.','reproduction':sys.executable+' '+str(R/'focused_checks.py')+' ; regenerate hard seed '+str(gen['seed'])+' template '+gen['template']+' parameters '+json.dumps(p,sort_keys=True),'evidence_path':'generated-records.json'})
save('generated-records.json',reproduced);save('inventory-reproduction-results.json',{'basis':inventory['basis'],'inventory_questions':len(byid),'source_questions_excluded_from_generated_findings':15,'generated_questions_reproduced':comparison,'limitation':'The complete five stored generated records reproduce byte-for-byte, including question IDs and generation metadata, from the captured generated.json. Original source questions remain original.'});save('affected-inventory.json',{'affected_questions':affected})
# Faithful read-only reproduction of question_selection.rs select: difficulty first,
# stable digest, uniform within chosen band; also account for history exclusions.
def band(q):
 v=q.get(':question/difficulty');return (v.get(':db/ident') if isinstance(v,dict) else v or '').split('/')[-1]
def select(candidates,weights,seed):
 candidates=sorted(candidates,key=lambda q:q[':db/id'])
 if weights is None:return candidates[0] if candidates else None
 bs=[[q for q in candidates if band(q)==b] for b in ['easy','moderate','hard']];unrated=[q for q in candidates if not band(q)]
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def uniform(offset):return (int.from_bytes(digest[offset:offset+8],'big')>>11)/2**53
 total=sum(w for w,b in zip(weights,bs) if b)
 pool=unrated
 if total>0:
  draw=uniform(0)*total
  for w,b in zip(weights,bs):
   if not b or not w:continue
   pool=b
   if draw<w:break
   draw-=w
 return pool[int(uniform(8)*len(pool))] if pool else None
usable=[q for q in inventory['questions'] if q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/choices')]
results=[]
for scenario,weights,exclude in [('easy_only',[1,0,0],[]),('hard_only',[0,0,1],[]),('all_bands',[6,3,1],[]),('no_config',None,[]),('one_hard_remaining',[0,0,1],[q[':question/id'] for q in usable if band(q)=='hard'][1:])]:
 candidates=[q for q in usable if q[':question/id'] not in exclude];draws=[select(candidates,weights,'independent-review-'+str(i)) for i in range(512)]
 results.append({'scenario':scenario,'weights':weights,'excluded_history_ids':exclude,'candidate_ids':[q[':question/id'] for q in candidates],'selected_bands':dict(collections.Counter(band(q) for q in draws if q)),'selected_ids':dict(collections.Counter(q[':question/id'] for q in draws if q)),'hard_second_term_nonresonant':'Every available hard candidate belongs to the reproduced fixed-role cohort; selection cannot create a missing second-position-resonant case.'})
save('selection-results.json',{'implementation':str(P/'engine/rust/question_selection.rs'),'implementation_sha256':hashlib.sha256((P/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'basis':inventory['basis'],'scenarios':results,'limits':['Captured inventory contains no live policy distribution or learner history. Scenarios condition on usable candidates and specified weights; they do not predict a specific learner session.','Usability is restricted to complete keys/solutions; the two incomplete original questions are excluded. Actual history exclusions can reduce this pool further.','Stable digest draw and band rules faithfully follow the inspected native source, without database access.']})
print(json.dumps({'minimal_swap_rejected':error,'hard_sample':len(hard),'stored_generated_reproduced':len(reproduced),'selection_scenarios':len(results)},indent=2))
