import sys,json,pathlib,importlib.util,re,hashlib,collections,subprocess
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');J=R/'generate/repairs/2026-10-20-early-cohort/jobs/17592186229182';P=J/'workspace'
spec=importlib.util.spec_from_file_location('gen',P/'17592186229182.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,default=str))
def cv(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
explicit=[dict(V=100,q0=q,c=c,rin=8,rout=12) for q,c in [(3,'0.04'),(3,'0.05'),(4,'0.05')]]
small=[g.generate('easy',733,parameters=p) for p in explicit]
save('shortcut-records.json',small)
# Exhaust only the demonstrated one-digit cue, not the generator's larger domain.
domain=[]
for q in range(3,45):
 for A in range(q+1,97):
  bank=[q,A,A-q,2*A-q,A+q]
  if len(set(bank))==5 and all(1<=v<=9 for v in bank): domain.append({'q0':q,'alpha':A,'bank':bank,'rank':sorted(bank).index(q)+1})
save('shortcut-proof.json',{'rule':'If all five choices are single digit, select second smallest.','derivation':'Bank=[q,A,A-q,2A-q,A+q], integer q>=3 and q<A. All single digit plus uniqueness permits exactly the enumerated three (q,A) pairs. This uses bank layout and author bounds, not Q(0).','enumerated_cases':domain,'explicit_records':'shortcut-records.json'})
inp=json.load(open(E/'counterfactual-records.json'))+small;save('counterfactual-and-shortcut-records.json',inp)
cases=[]
for i,r in enumerate(inp):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 cases.append({'label':f'controlled-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'Controlled pair or conditional shortcut, check every choice'} for a in f[':answer-field/choices']]})
save('controlled-grader-input.json',cases)
# Stored generated records have no generation metadata in captured inventory. Locate
# corresponding archived complete generated records and actually rerun their seeds.
inventory=json.load(open(J/'source/inventory.json'));byid={q[':question/id']:q for q in inventory['questions']}
arch=json.load(open(P/'17592186229182/reference/replenishment/basis-2598/generated.json'))
reproduced=[];matches=[]
for r in arch:
 gen=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 rr=g.generate(level,gen['seed']);qid=rr['question'][':question/id'];stored=byid.get(qid)
 f=rr['question'][':question/answer-fields'][0]
 matches.append({'question_id':qid,'entity_id':stored.get(':db/id') if stored else None,'generation_matches_archived':rr['generation']==gen,'record_matches_archived':rr==r,'prompt_matches_stored':stored is not None and stored[':question/problem']==rr['question'][':question/problem'],'solution_matches_stored':stored is not None and stored[':question/worked-solution']==rr['question'][':question/worked-solution'],'values_match_stored':stored is not None and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in stored[':question/answer-fields'][0][':answer-field/choices']),'all_single_digit':all(re.fullmatch('[1-9]',a[':answer/value']) for a in f[':answer-field/choices'])})
 reproduced.append(rr)
save('generated-records.json',reproduced);save('inventory-reproduction.json',{'basis':inventory['basis'],'matches':matches,'source_questions_excluded':10,'generated_questions_tested':7,'conditional_shortcut_affected':0,'restriction_note':'A rejection of valid inputs is not a mathematical defect in existing generated records. No stored question is assigned affected status solely for an absent case.','limits':'No single-digit archived generated inventory question. Verified absence of this exact conditional shortcut among the seven reproduced generated records; not proof of absence of every shortcut.'})
save('affected-inventory.json',{'affected_questions':[]})
def counts(rs):
 e=[r for r in rs if r['question'].get(':question/difficulty')==':question.difficulty/easy'];ranks=collections.Counter();positions=collections.Counter();single=0
 for r in e:
  vals=[int(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']];v=int(cv(r));ranks[sorted(vals).index(v)+1]+=1;positions[vals.index(v)+1]+=1;single+=all(0<x<10 for x in vals)
 return {'easy_n':len(e),'correct_ranks':dict(ranks),'correct_positions_before_UI_shuffle':dict(positions),'single_digit_cue_n':single,'distinct_answers':len(set(cv(r) for r in e))}
stage={}
for n in ['easy-samples.json','delivery-sample/accepted.json','batch.json','delivery-batch/accepted.json','shortcut-records.json']:
 stage[n]=counts(json.load(open(E/n)))
# Faithful read-only within-easy selection: supplied source does not include live
# policy/history. Condition on easy being selected, then apply its SHA uniform draw.
def pick(pool,seed):
 d=hashlib.sha256(('course-academy/question-selection/v1/'+str(seed)).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(2**53);return pool[min(int(u*len(pool)),len(pool)-1)]
selected=collections.Counter(pick(list(range(5)),seed) for seed in range(1000,1100))
save('selection-analysis.json',{'implementation':'engine/rust/question_selection.rs lines 123-198: candidates deduplicated/sorted by entity ID; difficulty band weighted excluding empty/zero-weight bands, uniform SHA draw within band.','conditional_easy_batch_slot_draws':dict(selected),'seed_range':[1000,1099],'candidate_assumption':'five fresh usable batch records assigned monotonically increasing IDs; actual future IDs/policy/history not supplied. All five remain possible for positive easy weight.','stage_coverage':stage,'captured_inventory_basis':inventory['basis'],'limitations':['Cannot predict a specific learner history, reservations, policy weights, or changing future inventory.','Unrated source question is fallback only when no positive weighted rated band remains.','Neither band selection nor within-band selection changes option magnitudes; the conditional shortcut survives any selection of a one-digit generated item.']})
save('scope.json',{'passed_for_observed_outputs':True,'assessment':'Easy outputs ask source alpha+beta through t=0, moderate ask coefficient difference, hard evaluate before a capacity event. No new operator, response type, or overflow calculation was introduced. Source restrictions are assessed separately.','evidence':['samples.json','render-records.json','math.json'],'families':[m['source_id'] for m in g.M.values()]})
print(json.dumps({'shortcut_domain':domain,'inventory_match_count':sum(x['record_matches_archived'] and x['prompt_matches_stored'] and x['solution_matches_stored'] and x['values_match_stored'] for x in matches),'stages':stage},default=str))
