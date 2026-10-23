import sys
sys.dont_write_bytecode=True
import audit as a
from shortcut_regression import predict,probes
import json,collections,copy,hashlib,runpy
R=a.ROOT;m=a.m
# Run original strict failing check on both versions; preserve its artifacts separately.
strict=[]
for label,module in [('old',a.module(a.JOB/'review-0-policy-2-8bbb1cdbe4d688a3/relocated/17592186161968.py')),('current',m)]:
 out=R/('strict-'+label);out.mkdir(exist_ok=True);a.ROOT=out;a.m=module
 try:runpy.run_path(str(R/'shortcut_regression.py'),run_name='__main__');failed=False
 except AssertionError as e:failed=True;error=str(e)
 strict.append({'version':label,'assertion_failed':failed,'error':error if failed else None})
a.ROOT=R;a.m=m;assert strict[0]['assertion_failed'] and not strict[1]['assertion_failed'];a.save('strict-regression.json',strict)
# Force actual sampler's matrix rejection while retaining its selected bank/key.
Original=m.random.Random
class Instrumented(Original):
 exhaust=False
 def __init__(self,*args):super().__init__(*args);self.coeff=None;self.calls=0;self.bank_draws=0;instances.append(self)
 def choice(self,seq):
  v=super().choice(seq)
  if len(seq)==5 and all(isinstance(x,tuple) and len(x)==2 and all(isinstance(k,int) for k in x) for x in seq):self.coeff=v;self.bank_draws+=1
  return v
 def randrange(self,*args,**kw):
  v=super().randrange(*args,**kw)
  if args==(3,) and not hasattr(self,'pivot'):self.pivot=v
  return v
 def randint(self,x,y):
  self.calls+=1
  if self.exhaust or self.calls<=9:
   cols=[c for c in range(3) if c!=self.pivot];row=[0]*3;row[self.pivot]=1
   for c,k in zip(cols,self.coeff):row[c]=-k
   return row[(self.calls-1)%3]
  return super().randint(x,y)
instances=[];m.random.Random=Instrumented
try:
 success=m.generate(seed=5581,bank_profile='q-91189');i=instances[-1];assert i.calls>=18 and i.bank_draws==1;a.check(success)
 success_info={'randint_calls':i.calls,'bank_draws':i.bank_draws,'correct_coefficients':a.check(success)['coefficients']}
 Instrumented.exhaust=True
 try:m.generate(seed=5581,bank_profile='q-91189');raise AssertionError('exhaustion was accepted')
 except ValueError as e:assert str(e)=='Bounded sampler exhausted'
 failure_info={'randint_calls':instances[-1].calls,'bank_draws':instances[-1].bank_draws,'error':'Bounded sampler exhausted'}
finally:m.random.Random=Original
a.save('rejection-records.json',[success]);a.save('sampler-rejection.json',{'forced_first_matrix_rejected':success_info,'forced_exhaustion':failure_info,'rule':'Bank eligibility tested before uniform key draw; matrix retry keeps bank, key, pivot and row. No frequency-based acceptance filter.'})
# Decision cases before/after shared delivery; exact batch measured separately.
reports={};strategy_reports=[]
for label,file in [('fresh','samples.json'),('controlled','roles.json'),('delivery_input','delivery-input.json'),('delivered','delivery-samples/accepted.json'),('batch','batch.json'),('batch_delivered','delivery-batch/accepted.json')]:
 rows=a.load(R/file);reports[label]={'frequency_probe':probes(rows),'coverage':a.summarize(rows)}
 groups={'all':rows}
 groups.update({p:[r for r in rows if r['generation']['bank_profile']==p] for p in m.PROFILES})
 for group,rs in groups.items():
  if not rs:continue
  for index in range(5):strategy_reports.append({'dataset':label,'group':group,'cue':'fixed stored choice index '+str(index),'correct':sum(a.check(r)['correct_index']==index for r in rs),'total':len(rs),'baseline':.2})
  pred=probes(rs)
  if pred['attempts']:strategy_reports.append({'dataset':label,'group':group,'cue':'unique first-component mode occurring twice and unique second-component mode','correct':pred['correct'],'total':pred['attempts'],'baseline':.2})
a.save('shortcut-results.json',reports);a.save('position-probes.json',strategy_reports)
# Matched fixed banks retain all possible correct entries after publication filtering.
accepted=a.load(R/'delivery-samples/accepted.json');roles=a.load(R/'roles.json')
key=lambda r:(r['generation']['bank_profile'],json.dumps(a.mats(r['question'][':question/problem'])))
roles_by_prompt={key(r):r for r in roles};delroles=[r for r in accepted if key(r) in roles_by_prompt]
assert len(delroles)==45
for p in m.PROFILES:assert {a.check(r)['correct_index'] for r in delroles if r['generation']['bank_profile']==p}==set(range(5))
# Engine selection rule for easy-only cohort, fresh and excluding a seen/reserved item.
batch=a.load(R/'delivery-batch/accepted.json');scenarios=[]
for excluded in [[],[0],[0,1]]:
 available=[i for i in range(len(batch)) if i not in excluded];counts=collections.Counter()
 for n in range(150):
  d=hashlib.sha256(('course-academy/question-selection/v1/revision-review-'+str(n)).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;counts[available[int(u*len(available))]]+=1
 scenarios.append({'excluded_indices':excluded,'selection_counts':dict(counts),'remaining_correct_positions':[a.check(batch[i])['correct_index'] for i in available]})
a.save('selection-review.json',{'basis':5581,'rules':'question_selection.rs select: sorted unique IDs; positive easy band yields uniform hash draw within easy; zero easy weight excludes it, no policy selects smallest ID. learning.rs validate_practice_question rejects retired, incomplete, multistep; unavailable_questions excludes seen/reserved/fixed future lesson items.','input':'delivery-batch/accepted.json','scenarios':scenarios,'eligibility':'All five single-radio complete, unretired easy records remain usable before learner exclusions.','limits':'Synthetic increasing IDs and histories; future entity IDs, actual learner history, live inventory changes are not observable. This tests the selection rule, not a future draw.'})
grade=a.load(R/'grader-report.json');native={v['label']:v for v in grade['records']}
a.save('counterfactual-results.json',{'relevant':{'before':'cf-0','after':'cf-1','expected':'First multiplier -2 -> 2; same bank; old key rejected','native_before':native['cf-0'],'native_after':native['cf-1']},'irrelevant':{'before':'cf-0','after':'cf-2','expected':'Off-target entry 1 -> 8; same operation pair, updated B/stages','native_before':native['cf-0'],'native_after':native['cf-2']},'target':{'before':'cf-3','after':'cf-4','expected':'Same A; pivot changes C1 -> C2; operations/zeroed columns/B/solution follow','native_before':native['cf-3'],'native_after':native['cf-4']},'independent_visible_math':[a.check(r) for r in a.load(R/'counterfactuals.json')]})
(R/'session-state.md').write_text('147 math records and 735 native choice submissions passed. All 131 independent runtime samples and five batch records survived delivery. Forced rejection/exhaustion, prior/current strict shortcut regression, all-key fixed banks and selection rules checked. UI screenshot inspection and final evidence report pending.\n')
print(json.dumps({'strict_regression':strict,'rejection':success_info,'datasets':{k:{s:v['frequency_probe'][s] for s in ['count','attempts','correct']} for k,v in reports.items()}},indent=2))
