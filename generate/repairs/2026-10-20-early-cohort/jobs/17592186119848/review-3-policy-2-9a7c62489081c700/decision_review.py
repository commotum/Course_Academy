import sys,json,re,collections,itertools,hashlib
from pathlib import Path
from html.parser import HTMLParser
E=Path(__file__).resolve().parent;J=E.parent
from audit_delivery import info,matrices,rank,shortcut_group
from review_helpers import correct,expected
load=lambda p:json.loads(Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def groups(rs,label_shapes):
 out=collections.defaultdict(list)
 for rec in rs:
  x=info(rec);shapes=tuple((k,tuple(v)) for k,v in sorted(x['shapes'].items())) if label_shapes else tuple(sorted(tuple(v) for v in x['shapes'].values()));key=(x['profile'],x['target'],shapes,tuple(x['excluded']),len(rec['question'][':question/answer-fields']),rec['generation']['choice_profile']);out[str(key)].append((rec,x))
 return out
reports=[];probes=[];native=[]
names=['batch','catalog','sampler-93827-5','sampler-57209-5','sampler-57209-24','exact-prefix-repaired']
for name in names:
 for stage,file in [('raw',name+'.json'),('surviving','delivery-'+name+'/accepted.json')]:
  rs=load(E/file);sub=[]
  for exact in (False,True):
   for key,items in groups(rs,exact).items():
    truths=[set(x['matches']) for _,x in items];eligible=items[0][1]['eligible'];subset='matrices have' in items[0][0]['question'][':question/problem']
    witnesses={};missing=[]
    if len(items)>1:
     for label in eligible:
      pairs=[(i,j) for i,j in itertools.combinations(range(len(items)),2) if (truths[i]-{label})==(truths[j]-{label}) and (label in truths[i])!=(label in truths[j])]
      witnesses[label]=pairs
      if subset and not pairs:missing.append(label)
     forced=[lab for lab in eligible if len({lab in t for t in truths})==1]
     assert not missing and not forced,(file,key,missing,forced)
    sub.append({'group':key,'label_shapes':exact,'count':len(items),'truths':[sorted(t) for t in truths],'independent_witnesses':witnesses,'missing':missing,'singleton':len(items)==1})
    if exact and len(items)>1:
     # Probe fixed subset and fixed count, by recognizable profile and layout.
     modal,n=collections.Counter(tuple(sorted(t)) for t in truths).most_common(1)[0]
     probes.append({'cue':'template and labeled dimensions','subgroup':name+' '+stage+' '+key,'scope':'other_recognizable_subgroup','strategy':'Always select '+(','.join(modal) or 'None'),'correct':n,'total':len(items),'baseline':1/len({tuple(sorted(t)) for t in truths}),'disposition':'not_predictive','conclusion':'No constant full response answers this repeated subgroup. Baseline is uniform over the observed permitted semantic outcomes; no significance claim from small samples.','sample_refs':[file]})
     counts=collections.Counter(len(t) for t in truths);n=counts.most_common(1)[0][1]
     probes.append({'cue':'template and qualifying-count','subgroup':name+' '+stage+' '+key,'scope':'within_template','strategy':'Assume the modal number of qualifying matrices','correct':n,'total':len(items),'baseline':max(counts.values())/len(items),'disposition':'intended_skill' if not subset else 'not_predictive','conclusion':('Singular matrix-radio requires exactly one by its stated response contract.' if not subset else 'Subset count is not fixed; joint and singleton decisions survive.')+' Baseline is the observed modal cardinality rate; cardinality success alone does not select the labels.','sample_refs':[file]})
  reports.append({'name':name,'stage':stage,'sample':file,'count':len(rs),'groups':sub})
# Source-supported strategies specifically from the two retained findings; add actual grader cases.
for stage,file in [('batch','delivery-batch/accepted.json'),('control_catalog','delivery-catalog/accepted.json')]:
 rs=[r for r in load(E/file) if shortcut_group(info(r)) and info(r)['profile']=='q-139965']
 for mode in ['hardcode_A_inspect_C','inspect_A_assume_exclusive','inspect_C_assume_exclusive']:
  wins=0
  for r in rs:
   x=info(r);t=set(x['matches'])
   if mode=='hardcode_A_inspect_C':guess={'A'}|({'C'} if 'C' in t else set())
   elif mode=='inspect_A_assume_exclusive':guess={'A'} if 'A' in t else {'C'}
   else:guess={'C'} if 'C' in t else {'A'}
   good=guess==t;wins+=good;f=r['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if set(re.findall(r'\$([A-E])\$',a[':answer/value']))==guess)
   native.append({'label':stage+' '+mode,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if good else 'rejected','purpose':'Retained shortcut action from visible rank evidence; omitted candidate never inspected'}]})
  probes.append({'cue':'rank3; shapes2x4,3x4,5x5; B dimension-excluded','subgroup':stage+' q-139965','scope':'other_recognizable_subgroup','strategy':mode,'correct':wins,'total':len(rs),'baseline':2/3,'disposition':'not_predictive','conclusion':'Baseline 2/3 is success on the two supported singleton outcomes for exclusivity, or two outcomes containing A for hardcoding A, out of three distinct rank-role cases. The delivered omitted-pivot counterexample defeats each strategy.','sample_refs':[file]})
save('decision-stage-results.json',reports);save('shortcut-probes.json',probes);save('shortcut-grader-input.json',native)
# Both explicit relevant pivot interventions and an irrelevant scalar intervention.
controls=load(E/'counterfactual-records.json');cf=[]
for before,after in [(0,1),(2,1),(1,3)]:
 qa,qb=controls[before]['question'],controls[after]['question'];ma,mb=matrices(qa),matrices(qb)
 stale=[]
 if before!=1:
  for component in [':question/answer-fields',':question/worked-solution']:
   import copy
   bad=copy.deepcopy(qb);bad[component]=qa[component]
   wrong_key=any(expected(bad,f)[0][':answer/id']!=correct(f)[':answer/id'] for f in bad[':question/answer-fields'])
   bad_rank=any(int(v)!=rank(matrices(bad)[k]) for k,v in re.findall(r'\\(?:text|textrm)\{rank\}\(([A-E])\)\s*=\s*(\d+)',bad[':question/worked-solution']))
   assert wrong_key or bad_rank;stale.append({'component':component,'rejected':True})
 cf.append({'before_index':before,'after_index':after,'kind':'irrelevant' if before==1 else 'relevant','changed_matrices':[k for k in ma if ma[k]!=mb[k]],'before_truth':info(controls[before])['matches'],'after_truth':info(controls[after])['matches'],'prompt_changed':qa[':question/problem']!=qb[':question/problem'],'solution_changed':qa[':question/worked-solution']!=qb[':question/worked-solution'],'stale_negative_controls':stale})
save('counterfactual-results.json',cf)
# Inspect stored inventory identities; never call original captured examples generated.
inv=load(J/'source/inventory.json');source=load(J/'source/source.json');sourceids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']};original=[q for q in inv['questions'] if q[':question/id'] in sourceids];others=[q for q in inv['questions'] if q[':question/id'] not in sourceids];assert len(original)==12 and not others
save('inventory-review.json',{'basis':inv['basis'],'total':len(inv['questions']),'verified_original_source_questions':len(original),'other_records':len(others),'original_question_ids':sorted(sourceids),'conclusion':'Verified captured inventory contains only original instructional questions. No generated instances are present to reproduce. This is a verified absence, limited to capture basis5415.'});save('affected-inventory.json',{'affected_questions':[]})
# Faithful read-only selector scenarios: easy band uniform, unknown future entity IDs explicitly hypothetical.
batch=load(E/'delivery-batch/accepted.json');complete=[q for q in inv['questions'] if all(':answer-field/correct' in f for f in q[':question/answer-fields'])];base=max(q[':db/id'] for q in inv['questions'])+1
new={base+i:r for i,r in enumerate(batch)};pool={q[':db/id']:q[':question/id'] for q in complete}|{i:r['question'][':question/id'] for i,r in new.items()};scenarios=[]
for name,ids in [('originals_fresh',sorted(pool)),('originals_seen',sorted(new)),('one_joint_case_seen',sorted(i for i,r in new.items() if info(r)['matches']!=['A','C']))]:
 counts=collections.Counter()
 for i in range(192):
  seed=f'task-291203/kp-17592186119848/slot-{i}';d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;counts[pool[ids[int(u*len(ids))]]]+=1
 scenarios.append({'scenario':name,'draws':192,'pool_size':len(ids),'counts':dict(counts),'unconfigured_policy_first':pool[ids[0]]})
save('learner-selection.json',{'basis':inv['basis'],'implementation':'engine/rust/question_selection.rs select: sorted unique IDs; requested easy band with positive weight -> uniform using SHA256 bytes8:16, rightshift11; absent policy -> first; zero easy weight -> no eligible rated easy record. Prior usable-field analysis reused; no engine changes.','generation_rejection':'Catalog39 -> structural dedup24 -> choose whole repeated-profile decision blocks or singletons -> shuffle. Complete nonempty/None checkbox fields avoid rejection. Counts0..24, overcapacity and invalid parameters exercised.','new_batch':5,'existing_usable':len(complete),'hypothetical_entity_ids':{str(i):r['question'][':question/id'] for i,r in new.items()},'scenarios':scenarios,'limits':['No publication: preparation.json absent. Actual entity IDs, learner histories, reservations and retirement unavailable.','Joint case remains selectable with positive easy weight and fresh history; history can remove it after that learner sees it, which is expected novelty filtering rather than a claim of invariant per-learner balance.','Captured inventory only; later publication can change deduplication. Sensitivity scenarios use hypothetical ascending new IDs, not claimed production draws.']})
(E/'session-state.md').write_text('All current repeated groups pass independent rank-role witness tests before and after delivery. Old fixed-A and mutual-exclusivity negative fixtures fail retained/original checkers; current batch passes. Actual UI first six renders inspected; scale1 counterfactual renderer running. Next: shortcut native grading, final schema/evidence verification.\n')
print(json.dumps({'stages':len(reports),'conditional_probes':len(probes),'shortcut_grader_cases':len(native),'affected_generated_inventory':0,'counterfactuals':cf}))
