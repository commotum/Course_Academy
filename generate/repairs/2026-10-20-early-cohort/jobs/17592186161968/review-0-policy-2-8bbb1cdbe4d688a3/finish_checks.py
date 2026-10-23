import sys
sys.dont_write_bytecode=True
import audit as a
from shortcut_regression import predict,probes
import json,hashlib,collections,copy
reports={}
for name,path in [('raw','samples.json'),('delivered','delivery-samples/accepted.json'),('batch','batch.json'),('batch_delivered','delivery-batch/accepted.json')]:
 records=a.load(a.ROOT/path);reports[name]=probes(records)
a.save('shortcut-results.json',reports)
# Observe actual rejection proposals through a temporary in-memory instrument, without modifying the package.
orig=a.m.eligible;attempts=[];active=None
for j,p in enumerate(a.m.PROFILES):
 for i in range(24):
  calls=[]
  def observed(profile,x,y):
   ok=orig(profile,x,y);calls.append({'coefficients':[x,y],'eligible':ok});return ok
  a.m.eligible=observed
  r=a.m.generate(seed=491003+101*j+i,bank_profile=p)
  # Last eligible call is the final explicit constructor validation, not a resampling proposal.
  attempts.append({'seed':491003+101*j+i,'profile':p,'proposals':calls[:-1],'accepted_parameters':r['generation']['parameters']})
a.m.eligible=orig
a.save('sampler-rejection.json',{'records':attempts,'proposals':sum(len(x['proposals']) for x in attempts),'ineligible_proposals':sum(not y['eligible'] for x in attempts for y in x['proposals']),'result':'Each profile is chosen before bounded resampling. Integral/nonzero/distinct banks and unique cleared row are enforced. Modal shortcut survives successful construction. The extra-row rejection is inspected in code; not forced by these fresh seeds.'})
# Faithful easy-only specialization of engine/rust/question_selection.rs select().
records=a.load(a.ROOT/'delivery-batch/accepted.json')
synthetic={100000000000000+i:r for i,r in enumerate(records)}
def select(pool,seed):
 ids=sorted(pool);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53
 return ids[int(u*len(ids))] if ids else None
scenarios=[]
for label,excluded in [('fresh',[]),('first question already seen',[100000000000000]),('shortcut question already seen',[100000000000001])]:
 pool={i:r for i,r in synthetic.items() if i not in excluded};counts=collections.Counter(select(pool,'independent-review-'+str(i)) for i in range(200))
 scenarios.append({'scenario':label,'excluded':excluded,'available':len(pool),'selections':dict(counts),'shortcut_selections':sum(n for i,n in counts.items() if predict(pool[i])==a.correctid(pool[i]))})
a.save('selection-review.json',{'implementation':'engine/rust/question_selection.rs: select; engine/rust/learning.rs: validate_practice_question and unavailable_questions','basis':5581,'eligibility':'Delivered records are ordinary, unretired, complete keyed single-radio easy questions. Source and generated tasks are deduplicated by shared check_delivery. Seen/current-prefix/reserved practice is excluded before selection. Retired questions fail fresh-practice validation.','weights':'With positive easy weight, a pool containing only these easy candidates is uniform after sorting entity IDs. Zero easy weight makes this rated-only pool unavailable; it does not promote another decision case. An unconfigured policy selects the smallest candidate ID.','scenarios':scenarios,'identity_limit':'Future database IDs and learner histories do not exist in this read-only review. Synthetic increasing IDs exercise the exact easy-band hash selection rule; not a prediction of a live learner draw. Every delivered case remains possible for a fresh learner with positive easy weight.','coverage':'All five delivered items survive eligibility and difficulty rules; the shortcut item is selected in the fresh and first-item-seen scenarios. Selection does not inspect or remove the defective option pattern.'})
# Each native outcome tied to rendered controlled records, not merely generation metadata.
grade={x['label']:x for x in a.load(a.ROOT/'grader-report.json')['records']}
a.save('counterfactual-results.json',{'relevant':{'before':0,'after':1,'change':'A[0][0] 4 -> -4, same pivot 2 and remaining data; first multiplier -2 -> +2.','result':'Prompt and B, first operation, both solution stages and conclusion update; former correct operation pair is a distractor and native grader rejects it.','native_before':grade['cf-0'],'native_after':grade['cf-1'],'screenshots':['render/question-006.png','render-extra/question-001.png']},'irrelevant':{'before':0,'after':2,'change':'Off-target A[1][0] 1 -> 8; target row and pivot unchanged.','result':'Correct operation pair and whole bank preserved; prompt/B and intermediate matrix entries change; grader still accepts only the same mathematical pair. IDs change as content changes.','native_before':grade['cf-0'],'native_after':grade['cf-2'],'screenshots':['render/question-006.png','render-extra/question-002.png']},'target':{'before':3,'after':4,'change':'Same A and zeroed row, pivot column changes from C1 to C2.','result':'Prompt, target labels, B, operations, pivot-coordinate explanation and native correct choice follow the chosen pivot.','native_before':grade['cf-3'],'native_after':grade['cf-4'],'screenshots':['render-extra/question-003.png','render-extra/question-004.png']}})
print(json.dumps({k:{t:v[t] for t in ['count','attempts','correct']} for k,v in reports.items()},indent=2))
