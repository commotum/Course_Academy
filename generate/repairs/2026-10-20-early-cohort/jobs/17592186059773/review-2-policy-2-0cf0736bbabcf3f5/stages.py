import collections,copy,hashlib,json,math,pathlib,random,sys
from review import E,JOB,PKG,REPO,PY,save,load,module,inspect,key,correct,kind,field,native,command,matrices
sys.dont_write_bytecode=True

def profiles(rs):
 d={}
 for r in rs:
  sid=r['generation']['template'];x=d.setdefault(sid,{'total':0,'keys':{},'kinds':{},'changed_rows':{}});x['total']+=1
  for slot,val in [('keys',str(key(r))),('kinds',kind(correct(r))),('changed_rows',str(inspect(r)['changed']))]:x[slot][val]=x[slot].get(val,0)+1
 return d

def probes(rs,ref):
 out=[]
 def add(cue,group,scope,strategy,n,den,base,disposition,conclusion):
  out.append({'cue':cue,'subgroup':group,'scope':scope,'strategy':strategy,'correct':n,'total':den,'baseline':base,'disposition':disposition,'conclusion':conclusion,'sample_refs':[ref]})
 for sid in sorted({r['generation']['template'] for r in rs}):
  ss=[r for r in rs if r['generation']['template']==sid];counts=collections.Counter(key(r) for r in ss);n=max(counts.values());k=max(counts,key=counts.get)
  add('Recognizable full answer bank',sid,'within_template',f'Always choose source-bank slot {k+1}',n,len(ss),.2,'not_predictive',f'Compared with uniform five-choice guessing (0.2), fitted best bank-only action gives {n}/{len(ss)}. Singleton batch groups permit a memorized fitted rule but do not demonstrate an invariant; the controlled same-bank targets disprove a fixed key in every current bank. The exact batch also contains different correct keys in its repeated q-130087 bank.')
 # Mathematical cue: exact swapped rows identifies swap by the taught operation.
 ss=[r for r in rs if kind(correct(r))=='swap']
 if ss:add('Target rows equal exchanged input rows','swap targets','other_recognizable_subgroup','Match the exchanged pair of rows, select that swap',len(ss),len(ss),.2,'intended_skill','Baseline is uniform five-choice guessing. Row matching implements the source lesson, rather than an incidental label cue.')
 n=sum(key(r)==0 for r in rs);add('Authored first position','all records','overall','Choose first authored choice',n,len(rs),.2,'not_predictive',f'{n}/{len(rs)}; comparison baseline is 0.2. The real UI additionally hashes choice IDs with item and field IDs to order options.')
 return out

def main():
 raw=load(E/'all-records.json');delivered=load(E/'delivery/accepted.json');batch=load(E/'batch-delivery/accepted.json')
 # Post-filter records with normalized TeX and remapped IDs must still execute and grade.
 [inspect(r) for r in delivered+batch]
 save('delivered-native-input.json',[native(r,'delivered '+str(i)) for i,r in enumerate(delivered+batch)])
 stage={'raw':profiles(raw),'accepted':profiles(delivered),'runner_batch':profiles(batch),'raw_records':len(raw),'accepted_records':len(delivered),'batch_records':len(batch)}
 save('stage-coverage.json',stage)
 ctrl=load(E/'controlled-records.json');pr=probes(ctrl,'controlled-records.json');save('shortcut-results.json',{'controlled_probes':pr,'fresh_sample_probes':probes(load(E/'fresh-sample.json'),'fresh-sample.json'),'delivered_probes':probes(delivered,'delivery/accepted.json'),'runner_batch_probes':probes(batch,'batch-delivery/accepted.json'),'interpretation':'Do not classify singleton fitted actions as demonstrated defects. All profile-only predictors are challenged by held-A complete-bank controlled witnesses; fresh and delivered samples test whether choices survive filters. Exact runner batch has four different correct authored positions and two operation types (three additions, two scales). No universal position or operation action answers its five members.'})
 # Actual sampler rejection and duplicate resampling, faithfully instrumented with same choices and RNG.
 g=module(E/'runtime/17592186059773.py','staged_generator');rng=random.Random(694821);domains={s:g.domain(s) for s in g.CASES};seen=set();res=[];attempts=[]
 while len(res)<60:
  sid=rng.choice(list(g.CASES));k=rng.choice(g.eligible_keys(sid));p=rng.choice(domains[sid])+[k]
  try:r=g.generate('moderate',694821,parameters=p)
  except g.InvalidInstance as ex:attempts.append({'parameters':p,'stage':'rejected','reason':str(ex)});continue
  fp=r['generation']['mathematical_fingerprint'];state='duplicate' if fp in seen else 'accepted'
  attempts.append({'parameters':p,'stage':state,'question_id':r['question'][':question/id']})
  if state=='duplicate':continue
  seen.add(fp);res.append(r)
 assert res==load(E/'fresh-sample.json')
 save('resampling-results.json',{'seed':694821,'attempt_count':len(attempts),'counts':dict(collections.Counter(x['stage'] for x in attempts)),'attempts':attempts,'matches_real_batch':True,'generator_rule':'Uniform bank, then uniform eligible elementary key, then domain point. Reject identity/ambiguous/duplicate outcomes; reject repeated row-permutation/uniform-scale mathematical fingerprint. No further correct-key filtering.'})
 # Read-only reproduction of question_selection.rs select on a provisional fresh moderate pool.
 # New entity IDs do not yet exist: ordinal synthetic IDs model ordering only, not a publication claim.
 def select(pool,distribution,seed):
  pool=sorted(set(pool))
  if distribution is None:return pool[0] if pool else None
  if distribution[1]<=0:return None
  h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
  u=(int.from_bytes(h[8:16],'big')>>11)/(2**53)
  return pool[int(u*len(pool))] if pool else None
 pool=list(range(100000,100000+len(batch)));counts=collections.Counter(select(pool,[6,3,1],str(i)) for i in range(1024))
 assert set(counts)==set(pool)
 nofirst=[x for x in pool if x!=pool[0]];assert all(select(nofirst,[6,3,1],str(i))!=pool[0] for i in range(64))
 save('selection-results.json',{'implementation':'Faithful SHA256 53-bit draw at offset 8 from engine/rust/question_selection.rs::select; all delivered questions are moderate, so every positive moderate weight renormalizes onto this band.','source_hash':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_inventory_basis':5359,'synthetic_fresh_pool':dict(zip(pool,[r['question'][':question/id'] for r in batch])),'seeds':'str(0)..str(1023)','counts':dict(counts),'each_candidate_selectable':True,'seen_history_scenario':'Remove first provisional entity; 64 draws never select it. Seen-before-task plus current prefix only remove questions.','zero_moderate_weight':select(pool,[1,0,1],'0'),'unconfigured_policy':select(pool,None,'0'),'limitation':'No live learner history, policy, or new entity IDs supplied. The unconfigured fallback chooses lowest fresh entity; a configured positive moderate weight samples uniformly within fresh moderate candidates. Does not assert live configured weights or a particular learner trajectory.'})
 # Representative actual UI records; all five delivered batch records plus both controlled pair kinds.
 pairs=load(E/'counterfactual-results.json');lookup={r['question'][':question/id']:r for r in ctrl};render=[];mapping=[]
 for pairkind in ('relevant','irrelevant'):
  pair=next(p for p in pairs if p['kind']==pairkind)
  for qid in (pair['before'],pair['after'][0]):
   render.append(lookup[qid]);mapping.append({'index':len(render),'purpose':pairkind+' controlled pair','original_id':qid})
 for r in batch:
  render.append(r);mapping.append({'index':len(render),'purpose':'exact delivered runner batch','original_id':r['question'][':question/id']})
 for label,condition in [('swap bank with non-elementary distractors',lambda r:r['generation']['template']=='q-72850'),('fractional addition',lambda r:kind(correct(r))=='addition' and '\\frac' in correct(r))]:
  r=next(r for r in delivered if condition(r));render.append(r);mapping.append({'index':len(render),'purpose':label,'original_id':r['question'][':question/id']})
 save('render-records.json',render);save('render-map.json',mapping)
 # Preserve original-key baseline failure for the retired fixed-bank generator.
 legacy=module(REPO/'generate/scratch/17592186059773.py','legacy_generator')
 old=[]
 sid='q-72856'
 for delta in (1,2,3):
  old.append(legacy.generate(seed=832715,parameters=[sid,0,0,delta,[0,1,2]]))
 save('legacy-fixed-bank-records.json',old)
 save('legacy-fixed-bank-results.json',{'bank':sid,'parameters':[r['generation']['parameters'] for r in old],'correct_values':[correct(r) for r in old],'fixed_key_reproduced':len({correct(r) for r in old})==1,'current_counterexample_file':'controlled-records.json','current_fixed_A_key_count':len({correct(r) for r in ctrl if r['generation']['template']==sid}),'interpretation':'Retired generator has fixed correct bank role. Current same-A witnesses vary all five eligible keys. Separate from current verdict.'})
 (E/'session-state.md').write_text('Completed source, math (197 raw records), runtime, history regressions, inventory, native grading (197 accepted/788 rejected), shared delivery (182/197 audit records; 5/5 exact batch). Saved decision-role coverage before/after, sampler traces, faithful read-only selection scenarios and counterfactuals. Next: normalized native checks and actual UI screenshots, then evidence contract and final verdict.\n')
 print(json.dumps({'raw':len(raw),'delivered':len(delivered),'batch':len(batch),'render':len(render),'conditional_probes':len(pr),'resampling':collections.Counter(x['stage'] for x in attempts)}))
if __name__=='__main__':main()
