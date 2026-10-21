import json,sys,hashlib
sys.dont_write_bytecode=True
from validate_repair import E,dump,summarize,field,correct
raw=json.load(open(E/'fresh.json'));accepted=json.load(open(E/'delivery-fresh/accepted.json'));batch=json.load(open(E/'delivery-batch/accepted.json'))
before=summarize(raw);after=summarize(accepted);assert before==after
assert len(batch)==5
for r in accepted+batch:
 assert r['question'][':question/difficulty']==':question.difficulty/easy'
dump('delivery-shortcuts.json',{'raw':before,'accepted':after,'unchanged_coverage':True,'raw_count':len(raw),'accepted_count':len(accepted),'sample_count':len(batch),'baseline':'A unique choice guessed without math has chance 1/5; a tied cue is an abstention, not a successful choice.'})
# Reproduce selection ranks for the captured fresh easy band, with no assumed live history.
ids=sorted(r['question'][':question/id'] for r in accepted);draws=[]
for i in range(30):
 seed='repair-learner-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53)
 draws.append({'seed':seed,'rank':int(u*len(ids)),'question_id':ids[int(u*len(ids))]})
dump('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select, SHA256 uniform offset 8 within chosen band','assumptions':'Easy-only fresh pool with positive easy policy weight. Sorted UUIDs stand in for the future numeric entity order; all ranks are eligible. Unconfigured policy selects the first numeric candidate.','draws':draws,'limits':['Live learner history, actual future numeric entity IDs and policy weights are unavailable. No claim of live selection probabilities. History exclusions can reduce family coverage; no finite five-item batch guarantees all six cases.'],'eligible_decision_cases':list(after)})
dump('post-grader-input.json',[{'label':'delivered-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==correct(r) else 'rejected','purpose':'actual shared delivery identities, all options'} for c in field(r)[':answer-field/choices']]} for i,r in enumerate(accepted+batch)])
print(json.dumps({'pre_post_coverage_equal':True,'accepted_fresh':len(accepted),'accepted_sample':len(batch),'grader_checks':5*(len(accepted)+len(batch))}))
