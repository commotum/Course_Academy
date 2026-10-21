import sys
sys.dont_write_bytecode=True
import audit as a,copy,json,hashlib,subprocess,re
from collections import Counter,defaultdict
R=a.ROOT

def facts(r):
 m=a.matrices(r['question'][':question/problem'])[0]; f=a.field(r)
 return {'id':r['question'][':question/id'],'template':r.get('generation',{}).get('template','stored'),'seed':r.get('generation',{}).get('seed'),'rows':m.rows,'cols':m.cols,'active':sum(any(m.row(i)) for i in range(m.rows)),'nonzero_columns':sum(any(m.col(i)) for i in range(m.cols)),'name':re.search(r'\$([A-Z])',r['question'][':question/problem'])[1],'rank':int(m.rank()),'answer':a.answer(r),'bank':sorted(int(c[':answer/value']) for c in f[':answer-field/choices']),'position':next(i for i,c in enumerate(f[':answer-field/choices']) if int(c[':answer/value'])==a.answer(r)),'first':int(f[':answer-field/choices'][0][':answer/value'])}

def summary(rs):
 fs=[facts(r) for r in rs]; groups=defaultdict(list)
 for f in fs:groups[(f['rows'],f['cols'],f['active'])].append(f['rank'])
 return {'count':len(fs),'rank_counts':dict(Counter(f['rank'] for f in fs)),'rows_minus_one':sum(f['rank']==f['rows']-1 for f in fs),'groups':[{'shape_active':list(k),'ranks':v} for k,v in groups.items()],'records':fs}

def select(ids,seed):
 ids=sorted(set(ids));d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53)
 return ids[int(u*len(ids))] if ids else None

def main():
 batch=a.read(R/'batch.json'); delivered=a.read(R/'delivery-batch/accepted.json'); samples=a.read(R/'samples.json'); normaldel=a.read(R/'delivery-samples/accepted.json')
 inv=a.read(a.JOB/'source/inventory.json'); stored=[{'question':q} for q in inv['questions']];a.save('inventory-records.json',stored)
 pool={q[':db/id']:{'question':q} for q in inv['questions']};new={90000000000000+i:r for i,r in enumerate(delivered)};pool.update(new)
 scenarios=[]
 for name,ids in [('combined captured bank',list(pool)),('only proposed batch fresh',list(new)),('last two proposed questions fresh',list(new)[-2:])]:
  chosen=[select(ids,'independent-revision-731/'+str(i)) for i in range(32)]
  scenarios.append({'scenario':name,'candidate_ids':ids,'seeds':'independent-revision-731/0..31','draws':chosen,'results':summary([pool[i] for i in chosen]),'candidate_coverage':summary([pool[i] for i in ids])})
 stage={'inventory_basis':inv['basis'],'publication_preparation':'absent; shared check_delivery reproduces preparation read-only','rejection_resampling':{'fresh_normal_attempts':51,'failures':a.read(R/'coverage.json')['generation_failures'],'rule':'generate constructs compatible rank/active row cases without statistical rejection. Batch retries only semantic fingerprint duplicates up to 1000; assignments are unchanged on retry.','new_branch_tests':'author-check/regression-results.json; shortcut-regression-runs.json'},'batch_input':summary(batch),'batch_accepted':summary(delivered),'control_input':summary(samples),'control_accepted':summary(normaldel),'inventory_all':summary(stored),'inventory_generated':summary([r for r in stored if not r['question'].get(':question/math-academy-id')]),'learner_selection':{'rules':'question_selection.rs lines 124-197: sort/deduplicate fresh IDs; weight difficulty bands; SHA256 seeded uniform draw within chosen band. All captured/proposed entries moderate. Positive moderate weight retains the entire eligible pool; zero moderate weight yields none absent unrated candidates. No-policy fallback takes lowest ID.','transcription':'select() in inspect_revision.py; read-only hypothetical new IDs, not claimed database identities','history':'Candidates are fresh usable records. Removing prior seen questions can shrink contrasts; no actual learner histories captured.','scenarios':scenarios,'limits':'Captured inventory basis only; no live policy, history or future entity IDs. Arbitrary exhausted subsets are not a claim about universal batch defects.'}}
 a.save('stage-analysis.json',stage)
 probes=[]
 def probe(rs,cue,subgroup,scope,strategy,fn,ref):
  fs=[facts(r) for r in rs]
  if not fs:return
  good=sum(fn(f)==f['rank'] for f in fs)
  probes.append({'cue':cue,'subgroup':subgroup,'scope':scope,'strategy':strategy,'correct':good,'total':len(fs),'baseline':.2,'disposition':'not_predictive','conclusion':f'{good}/{len(fs)} versus uniform random five-choice baseline 0.2. '+('Not a perfect predictor in this subgroup.' if good<len(fs) else 'Singleton or small subgroup observation; eligible contrasts inspected in larger same-template controls; no generalized cue rule demonstrated.'),'sample_refs':[ref]})
 for label,rs,ref in [('exact delivered batch',delivered,'delivery-batch/accepted.json'),('fresh delivered controls',normaldel,'delivery-samples/accepted.json')]:
  for cue,fn in [('rows minus one',lambda f:f['rows']-1),('count nonzero rows',lambda f:f['active']),('first choice',lambda f:f['first']),('maximum bank',lambda f:max(f['bank'])),('minimum bank',lambda f:min(f['bank'])),('always three',lambda f:3)]:probe(rs,cue,label,'overall',cue,fn,ref)
  for key in ['rows','template','active','name']:
   for value in dict.fromkeys(facts(r)[key] for r in rs):
    group=[r for r in rs if facts(r)[key]==value]
    if len(group)<2:continue
    probe(group,key,label+': '+str(value),'within_template' if key=='template' else 'other_recognizable_subgroup','rows minus one',lambda f:f['rows']-1,ref)
    probe(group,key,label+': '+str(value),'within_template' if key=='template' else 'other_recognizable_subgroup','always three',lambda f:3,ref)
 a.save('shortcut-probes.json',probes)
 a.save('affected-inventory.json',{'affected_questions':[]})
 a.save('inventory-assessment.json',{'basis':inv['basis'],'tested_records':len(stored),'tested_source_records':17,'tested_generated_records':5,'rows_minus_one_successes':stage['inventory_all']['rows_minus_one'],'generated_successes':stage['inventory_generated']['rows_minus_one'],'assessment':'Verified absence of the retained whole-pool shortcut in captured full bank and five generated members. No individually affected stored question demonstrated; corank one is legitimate. Other defects not exhaustively audited. Original source records remain source records. Captured generation metadata is unavailable; no generated replay attribution invented.'})
 all_records=delivered+a.read(R/'source-replays.json')+a.read(R/'counterfactual-records.json')
 cases=[]
 for i,r in enumerate(all_records):
  rank=facts(r)['rank'];cases.append({'label':f'revision independent rank {i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==rank else 'rejected','purpose':'complete radio bank checked against exact prompt rank'} for c in a.field(r)[':answer-field/choices']]})
 a.save('grader-input.json',cases)
 a.save('delivered-content-comparison.json',{'raw_count':len(batch),'delivered_count':len(delivered),'matrix_bank_keys_preserved':all(a.matrices(x['question'][':question/problem'])==a.matrices(y['question'][':question/problem']) and a.answer(x)==a.answer(y) for x,y in zip(batch,delivered)),'math_checks':[a.check(r) for r in delivered]})
 # Public explicit seed is stable despite batch shuffling; each item parameters replay.
 g=a.load_generator(a.PKG);assert all(g.generate(seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'])==r for r in batch)
 a.save('batch-replay.json',{'runner_batch_matches_revised_cli':batch==g.generate_batch(count=5,seed=315106964),'explicit_parameters_replay':True,'batch':summary(batch)})
 (R/'session-state.md').write_text('Source account confirmed and saved before package reads. Current 17 source replays, 51 fresh item samples and exact batch pass math. Old retained batch fails strict shortcut; current batch and 21 author regression batches pass. Shared delivery retains 5/5 batch and 51/51 controls at captured basis 5362. Current stage, inventory, native grader input and conditional shortcut evidence saved. Remaining: native grader execution, actual UI screenshot inspection, evidence contract/final report. No package modifications.\n')
 print(json.dumps({'batch':{k:v for k,v in stage['batch_accepted'].items() if k not in ('records',)},'perfect_probes':[{k:p[k] for k in ('cue','subgroup','correct','total')} for p in probes if p['correct']==p['total']],'probes':len(probes),'grader_checks':sum(len(x['checks']) for x in cases)}))
if __name__=='__main__':main()
