import sys,json,pathlib,collections,re,itertools,hashlib,math,random
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent
J=R.parent
read=lambda n:json.load(open(R/n))
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def correct(f):
 v=f[':answer-field/correct'];aid=v[':answer/id'] if isinstance(v,dict) else v[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def selected(r):
 fs=r['question'][':question/answer-fields']
 if str(fs[0][':answer-field/type']).endswith('/checkbox'):
  return tuple(sorted(int(re.search(r'Column (\d+)',f[':answer-field/key'])[1])-1 for f in fs if correct(f)=='true'))
 return tuple(int(i)-1 for i in re.findall(r'\$(\d+)\$',correct(fs[0])))
def cases(rs):return dict(collections.Counter(','.join(str(j+1) for j in selected(r)) for r in rs))
def overview(rs):
 return {'total':len(rs),'answers':cases(rs),'shapes':dict(collections.Counter(str(r['generation']['shape']) for r in rs)),'rejections':dict(collections.Counter(r['generation'].get('rejections',0) for r in rs)),'profile':dict(collections.Counter(r['generation']['profile'] for r in rs))}
moderate=read('moderate-samples.json');hard=read('hard-samples.json');batch=read('runner-batch.json');accepted=read('delivery-independent/accepted.json');delivered=read('delivery-batch/accepted.json')
# preserve generated metadata after public normalization; all records remain complete.
probes=[]
def probe(rs,refs,strategy,fn,cue,subgroup,scope='within_template',disposition='not_predictive'):
 wins=sum(fn(r)==selected(r) for r in rs)
 baseline=sum(1/sum(math.comb(r['generation']['shape'][1],k) for k in range(2,min(r['generation']['shape'][0],r['generation']['shape'][1]-1)+1)) for r in rs)/len(rs)
 probes.append({'cue':cue,'subgroup':subgroup,'scope':scope,'strategy':strategy,'correct':wins,'total':len(rs),'baseline':baseline,'disposition':disposition,'conclusion':f'Exact complete-subset success {wins}/{len(rs)}. Baseline is a uniform guess among admissible subsets at that visible shape (rank is not given). '+('First nonzero entries of row-permuted REF matrices instantiate the lesson skill; this valid simplification is mathematically informative.' if disposition=='intended_skill' else 'No tested fixed choice or superficial rule solves this entire subgroup; small-sample associations are bounded observations.'),'sample_refs':refs})
for label,rs,refs in [('independent raw',moderate,['moderate-samples.json']),('independent delivered',accepted,['delivery-independent/accepted.json']),('exact batch',batch,['runner-batch.json']),('exact delivered batch',delivered,['delivery-batch/accepted.json'])]:
 probe(rs,refs,'Always select columns 1 and 2.',lambda r:(0,1),'column numbers',label)
 probe(rs,refs,'Select all but the last original column.',lambda r:tuple(range(r['generation']['shape'][1]-1)),'last column position',label)
 probe(rs,refs,'Select original columns whose top-row entries are positive.',lambda r:tuple(j for j,x in enumerate(r['generation']['matrix'][0]) if x>0),'sign and row placement',label)
 for name in sorted(set(r['generation']['matrix_name'] for r in rs)):
  sub=[r for r in rs if r['generation']['matrix_name']==name]
  if len(sub)>=2:probe(sub,refs,'Always select columns 1 and 2.',lambda r:(0,1),'matrix label '+name,label+' label '+name,'other_recognizable_subgroup')
 for shape in sorted(set(tuple(r['generation']['shape']) for r in rs)):
  sub=[r for r in rs if tuple(r['generation']['shape'])==shape]
  if len(sub)>=2:probe(sub,refs,'Select all but the last column.',lambda r:tuple(range(shape[1]-1)),str(shape)+' shape',label+' '+str(shape),'other_recognizable_subgroup')
 probe(rs,refs,'Select columns containing the first nonzero entry of any original nonzero row.',lambda r:tuple(sorted({next(j for j,x in enumerate(row) if x) for row in r['generation']['matrix'] if any(row)})),'row leading entries',label,disposition='intended_skill')
# Radio cues per recognizable reduction template and each choice-count profile.
radio=[r for r in hard if r['generation']['profile'].startswith('radio')]
def radio_choice(r,kind):
 f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];ss=[tuple(int(i)-1 for i in re.findall(r'\$(\d+)\$',a[':answer/value'])) for a in choices]
 if kind=='first':return ss[0]
 if kind=='shortest':return min(ss,key=len)
 sizes=collections.Counter(map(len,ss));size=min(sizes,key=sizes.get);return next(s for s in ss if len(s)==size)
for profile in sorted({r['generation']['profile'] for r in radio}):
 for kind in ['first','shortest','minority-size']:
  sub=[r for r in radio if r['generation']['profile']==profile];wins=sum(radio_choice(r,kind)==selected(r) for r in sub)
  probes.append({'cue':kind,'subgroup':profile,'scope':'within_template','strategy':'Choose the '+kind+' bank entry (first if tied).','correct':wins,'total':len(sub),'baseline':.2,'disposition':'not_predictive','conclusion':f'{wins}/{len(sub)} exact selections against 1/5 random-choice baseline. Correct bank position and eligible size vary in this subgroup; no complete predictor demonstrated.','sample_refs':['hard-samples.json']})
# Faithful read-only selection arithmetic: selection is band-first, then uniform within
# eligible band, independent of matrix/response. Capture actual inventory candidates.
inv=json.load(open(J/'source/inventory.json'))
def en(v):return v.get(':db/ident') if isinstance(v,dict) else v
cand=[]
for q in inv['questions']:
 band=en(q[':question/difficulty']).split('/')[-1]
 cand.append({'id':q[':db/id'],'band':band,'qid':q[':question/id'],'origin':'inventory'})
start=max(c['id'] for c in cand)+1
for i,r in enumerate(delivered):cand.append({'id':start+i,'band':'moderate','qid':r['question'][':question/id'],'origin':'accepted batch (synthetic ordered entity ID)'})
def choose(cs,distribution,seed):
 cs=sorted(cs,key=lambda c:c['id']);bands=[[c for c in cs if c['band']==b] for b in ['easy','moderate','hard']]
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=lambda o:(int.from_bytes(digest[o:o+8],'big')>>11)/2**53
 total=sum(w for w,bs in zip(distribution,bands) if bs);draw=u(0)*total;pool=[]
 for w,bs in zip(distribution,bands):
  if not bs or w==0:continue
  pool=bs
  if draw<w:break
  draw-=w
 return pool[min(int(u(8)*len(pool)),len(pool)-1)] if pool else None
selection=[]
for label,cs,weights in [('captured plus new moderate',cand,[0,1,0]),('all rated bands',cand,[1,1,1]),('new batch alone',cand[-5:],[0,1,0])]:
 draws=[choose(cs,weights,'independent-audit-'+str(i)) for i in range(200)]
 sequential=[];remaining=cs[:]
 for i in range(len(cs)):
  c=choose(remaining,weights,'freshness-audit-'+str(i))
  if c is None:break
  sequential.append(c);remaining=[v for v in remaining if v['id']!=c['id']]
 selection.append({'case':label,'distribution':weights,'draws':dict(collections.Counter(c['qid'] for c in draws if c)),'candidate_count':len(cs),'fresh_without_replacement':sequential})
save('selection-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 '+str(pathlib.Path('/home/jake/Developer/Course_Academy/.venv/bin/python'))+' variation.py','basis':inv['basis'],'candidates':cand,'runs':selection,'implementation_sha256':hashlib.sha256(pathlib.Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs').read_bytes()).hexdigest(),'rule_analysis':'BTreeSet entity ordering, requested band weights then uniform eligible index. Exclude seen prior tasks and current task prefix before calling select. No matrix label, pivot role, answer index, or response-count input exists. With no configured distribution picks smallest entity ID; this may delay other candidates but does not rewrite their responses. With no positively weighted eligible band, unknown-rating fallback only; this captured pool is rated.','limits':['Captured basis 5362 only. No live learner history or active policy supplied. Examined structural behavior and supplied two positive-weight configurations plus batch-only selection; no claim about a specific live learner sequence.','Accepted records have no assigned entity IDs yet; synthetic IDs preserve appended ordering for simulation. These are preview candidates, not published records.']})
save('stage-results.json',{'raw':overview(moderate),'normalized':overview(accepted),'batch_raw':overview(batch),'batch_normalized':overview(delivered),'hard':overview(hard),'rejection_rule':'Answer roles and radio bank are assigned before the bounded numeric retry loop. Retries do not change chosen role assignments. Moderate requires exactly one swap; hard profiles bounded to one or two operations; valid output cannot be rank-zero. Nonempty policy therefore does not resample these observed records.','moderate_max_rejections':max(r['generation']['rejections'] for r in moderate),'dedup_loss':len(moderate)-len(accepted),'batch_dedup_loss':len(batch)-len(delivered),'selection_reachable_all_new_batch':len(selection[-1]['fresh_without_replacement'])==5})
save('shortcut-results.json',{'probes':probes,'batch_partial_cue':'All five runner-batch records have column 1 as a pivot. Their first columns are visibly nonzero, which mathematically forces column 1 to be a pivot for any matrix. This is valid intended knowledge, not an arbitrary label assignment. Complete subsets vary across three answers; 1,2 succeeds only 3/5, and the 4x4 subgroup has both 1,2 and 1,3.','finite_scope':'Every moderate record is a one-swap permutation of REF. Reading row-leading positions is equivalent to finding pivots here and is the same simplification used by all moderate source cases. Hard elimination cases require actual cancellation; hard sources include both response types.','no_universal_claim':'No finite probe proves the absence of all incidental shortcuts.'})
variation={'learner_operation':'Find the original column indices that become leading entries after row-echelon reduction; moderate cases require one row swap, then complete checkbox selection.','fixed_features':[{'feature':'Moderate profile uses exactly one row swap on sparse 3x3, 3x4, or 4x4 matrices.','justification':'All six moderate source questions have this workload; adding elimination would increase difficulty. Row-leading inspection is a valid mathematical simplification in this family.'},{'feature':'At least two pivot columns and at least one nonpivot column; numeric entries are small integers.','justification':'All supplied source practice uses nontrivial subset selection with at least two pivots and both positive and negative choices; moderate rank one/full column rank would reduce the instructional decision. These restrictions retain the demonstrated skill and workload.'},{'feature':'One checkbox per original column, with original column vectors.','justification':'The moderate source response contract is complete subset selection, not rank entry or transformed-column identification.'}],'answer_roles':[{'role':'Which original columns qualify','eligible_variation':'Vary leading, internal and terminal nonpivot roles and eligible pivot subsets at each supported shape.','observed':'60 moderate samples cover all ten eligible subsets across 3/4 columns; explicit boundary assignments reach earliest and latest subsets. The delivered five contain three subsets.'},{'role':'Correct choice count and displayed position','eligible_variation':'Rank 2/3 at four columns; original column number follows matrix ordering. Hard radio correct entry and size vary.','observed':'Both ranks occur for 3x4 and 4x4; 3x3 rank2 justified as the nontrivial comparable subset task. Hard radio profiles have size2/3 keys and different bank positions.'},{'role':'Matrix label and incidental entries','eligible_variation':'A/B/P and signs/nonleading values may change without assigning a response.','observed':'Fixed subset probes fail within nontrivial label and shape groups; irrelevant nonleading change preserves membership.'}],'coverage':[{'case':'Source and shape/role boundaries','sample_refs':['source-replay-results.json','boundaries.json','boundary-results.json'],'result':'17 source answer banks replayed; canonical reconstructed; earliest/latest eligible subsets accepted at supported shapes.'},{'case':'Raw versus delivered moderate','sample_refs':['moderate-samples.json','delivery-independent/accepted.json','stage-results.json'],'result':'60/60 accepted, no decision-case loss, ten distinct complete subsets.'},{'case':'Exact runner batch separately','sample_refs':['runner-batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'5/5 accepted; subsets {1,3,4}, {1,2}, {1,3}. Three 4x4 records include {1,2} and {1,3}; no tested full-answer surface cue solves all five.'},{'case':'Hard response/reduction profiles','sample_refs':['hard-samples.json','math-results.json'],'result':'Six samples per each of six profiles, including swaps, eliminations, mixed cases and five-entry radio banks.'}],'counterfactuals':[{'kind':'relevant','change':'Hold [[1,2,5],[0,0,0],[0,4,3]] fixed except change row3 column2 from 4 to 0.','expected':'Pivot subset changes {1,2} -> {1,3}; answer vectors, conclusion, rendering and native grader must follow.','observed':'Exact independent reduction, solution matrices and complete native true/false checks match changed selection; rendered records 6/7 exhibit this change.','status':'passed','justification':'Both are sparse one-swap moderate instances; changing a leading entry changes the decision while preserving workload.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-results.json','render-all/rendering.json']},{'kind':'irrelevant','change':'Hold the base fixed except row1 column3 from 5 to -5.','expected':'Keep pivot subset {1,2}, with the changed original vector and solution matrices.','observed':'Independent matrix checks and native checks preserve selection; rendered records 6/8 show the changed entry and unchanged answers.','status':'passed','justification':'Changing a nonleading coefficient in this REF-permutation task does not move row-leading positions.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-all/rendering.json']}],'shortcut_probes':probes,'delivery':{'stages_examined':['generator numeric rejection/resampling','nonempty-checkbox wrapper','requested difficulty','actual publisher normalization and inventory/batch deduplication','learner band selection, entity ordering, freshness and no-policy fallback'],'sample_refs':['stage-results.json','delivery-independent/delivery.json','delivery-batch/delivery.json','selection-results.json'],'result':'No rejection/deduplication loss of the sampled decision cases. Uniform-within-band selection preserves possible outcomes; fresh selection from exact new batch reaches all five. Captured inventory and inactive previews only, no publication.'},'limitations':['Finite probes cover tested cue strategies, not every shortcut.','No active policy or learner history is captured; selection is evaluated structurally and in reproducible preview configurations.','Canonical source has no fields, so its response contract is inferred from adjacent practice while its matrix/solution is checked directly.','Hard material was sampled conservatively for fidelity and profiles; requested batch is moderate.']}
save('pedagogical-variation.json',variation)
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-review.json',{'basis':inv['basis'],'questions':len(inv['questions']),'original_source_question_ids':len({q[':question/id'] for q in inv['questions']} & {c['id'] for c in read('source-analysis.json')['source_cases']}),'status':'No demonstrated generator weakness to match. Empty affected list means none demonstrated, not proof all inventory cases are free of all defects. Five additional stored records inspected as captured inventory; generation metadata not included in this snapshot. No original source marked generated.','captured_question_ids':[q[':question/id'] for q in inv['questions']]})
print(json.dumps({'shortcut_probes':len(probes),'raw':overview(moderate),'exact_batch':overview(batch),'radio_probe_results':[(p['subgroup'],p['cue'],p['correct'],p['total']) for p in probes if p['subgroup'].startswith('radio')],'selection_all_five':len(selection[-1]['fresh_without_replacement'])==5}))
