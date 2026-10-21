import sys,json,pathlib,copy,collections,hashlib
sys.dont_write_bytecode=True
from audit import E,JOB,PKG,REPO,g,dump,shortcut,field,correct,mathcheck
sys.path.insert(0,str(REPO))
from scripts.generator_publish import normalized_question,stable_identities,localize_record
I=json.load(open(JOB/'source/inventory.json'));stored={q[':question/id']:q for q in I['questions']}
H=json.load(open(PKG/'17592186115241/reference/replenishment/basis-2701/generated.json'))
reproduced=[];report=[];affected=[]
for old in H:
 md=old['generation'];level=old['question'][':question/difficulty'].split('/')[-1]
 r=g.generate(level,seed=md['seed'],parameters=md['parameters'],profile=md['bank_profile'])
 normalized=localize_record(r,E/'inventory-assets',E/'inventory-assets')
 normalized['question']=stable_identities(normalized['question'],r['knowledge_point']['id'])
 # Some historical transactions retained old authored UUIDs. Match content and preserve only observed identity after proving equivalence.
 matches=[q for q in I['questions'] if normalized_question(q,identity=False)==normalized_question(normalized['question'],identity=False)]
 qid=matches[0][':question/id'] if len(matches)==1 else None
 item={'historical_id':old['question'][':question/id'],'raw_reproduced_id':r['question'][':question/id'],'current_stable_id':normalized['question'][':question/id'],'matched_stored_id':qid,'seed':md['seed'],'parameters':md['parameters'],'template':md['template'],'matching_stored_contents':len(matches),'generation_matches_historical_core':all(r['generation'].get(k)==v for k,v in md.items() if k not in ['preparation_basis','source_snapshot'])}
 if matches:
  # Exact stored identities, identical authored fields/math: not a generated label on originals.
  q=matches[0]
  item['exact_stored_identity_and_content_match']=normalized_question(q,identity=True)==normalized_question(r['question'],identity=True)
  assert item['exact_stored_identity_and_content_match']
  r['review_evidence']={'metadata_provenance':'package historical generated.json replayed with current executable','stored_entity_id':q[':db/id'],'inventory_basis':I['basis']}
  probe=shortcut(r);item['shortcut']=probe;reproduced.append(r)
  if probe.get('correct') and probe.get('unique_modes'):
   affected.append({'question_id':qid,'entity_id':q[':db/id'],'finding':'Component-frequency shortcut: intersect most frequent first and second answer components to select the key without using the system.','reproduction':f'PYTHONDONTWRITEBYTECODE=1 {REPO}/.venv/bin/python inventory_audit.py; difficulty={level}, seed={md["seed"]}, profile={md["bank_profile"]}, parameters='+json.dumps(md['parameters'],separators=(',',':')),'evidence_path':'generated-records.json'})
 report.append(item)
dump('generated-records.json',reproduced);dump('affected-inventory.json',{'affected_questions':affected})
dump('inventory-results.json',{'basis':I['basis'],'captured_questions':len(I['questions']),'source_originals':14,'generated_metadata_records_available':len(H),'reproduced_generated':len(reproduced),'demonstrated_affected':len(affected),'records':report,'limits':['No original Math Academy question relabeled as generated.','The captured inventory omits generation metadata; exact seed/parameter provenance recovered from packaged historical generated.json and tested with the current executable. Content equality and exact stored question/field/answer identities verified using shared publisher normalization.','For retained affected IDs all prompts, worked solutions, complete banks, keys and difficulty match the stored question; the executable itself reproduced the exact stored question/field/answer identities.','Live learner histories, policy weights and future inventory are not captured.']})
# Grader results will include the post-filter records as well as inventory and paired counterfactuals.
post=json.load(open(E/'delivery-batch/accepted.json'))+json.load(open(E/'delivery-fresh/accepted.json'))
grade=[x for x in json.load(open(E/'grader-input.json')) if not x['label'].startswith('delivered-or-inventory ')]
for i,r in enumerate(post+reproduced):
 f=field(r);grade.append({'label':'delivered-or-inventory '+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'all choices; delivered identities or exact stored generated content'} for c in f[':answer-field/choices']]})
dump('grader-input.json',grade)
# Pure cue statistics before/after filtering, plus conditional template probes.
def measures(rr):
 out={}
 for key in sorted(set(r['generation']['template'] for r in rr)):
  group=[r for r in rr if r['generation']['template']==key];probes=[shortcut(r) for r in group];cond=[p for p in probes if p.get('unique_modes')]
  out[key]={'count':len(group),'conditional_total':len(cond),'conditional_correct':sum(p['correct'] for p in cond),'all_correct':sum(p.get('correct',False) for p in probes),'position_counts':dict(collections.Counter(next(j+1 for j,c in enumerate(field(r)[':answer-field/choices']) if c[':answer/id']==correct(r)) for r in group)),'probes':probes}
 return out
summary={name:measures(json.load(open(E/path))) for name,path in [('raw_batch','batch.json'),('delivered_batch','delivery-batch/accepted.json'),('raw_fresh','fresh.json'),('delivered_fresh','delivery-fresh/accepted.json'),('inventory','generated-records.json')]}
dump('delivery-shortcuts.json',summary)
# Faithful read-only reproduction of question_selection.rs selection on delivered batch IDs.
# With easy-only fresh candidates, any positive easy weight selects this entire defective pool.
rr=json.load(open(E/'delivery-batch/accepted.json'));ids=sorted(r['question'][':question/id'] for r in rr);draws=[]
for i in range(30):
 seed='independent-review-learner-'+str(i); digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);draws.append({'seed':seed,'candidate_rank':int(u*len(ids)),'selected_id':ids[int(u*len(ids))]})
dump('learner-selection.json',{'source':'engine/rust/question_selection.rs select(): sorted entity candidates, difficulty band first, SHA256 uniform offset 8 within selected band','assumptions':'Fresh easy-only batch; positive easy weight. IDs here stand for ascending reserved entity order; the precise future numeric IDs and actual learner histories are unavailable, so this tests every possible batch candidate and selection ranks rather than claiming live-user selection.','candidate_ids':ids,'draws':draws,'unique_selected':len(set(d['selected_id'] for d in draws)),'all_candidates_shortcut':all(shortcut(r).get('correct') for r in rr),'history_effect':'Excluding seen batch members leaves a subset where the same shortcut works on every remaining member. Inventory has original questions too, so this does not claim every live KP selection is affected.','unconfigured_policy':'Returns first numeric entity candidate; any of the batch candidates is shortcut-solvable.'})
print(json.dumps({'matched':len(reproduced),'affected':len(affected),'inventory_ids':[a['question_id'] for a in affected],'delivery':{k:{t:{a:v for a,v in vv.items() if a!='probes'} for t,vv in val.items()} for k,val in summary.items()}},indent=2))
