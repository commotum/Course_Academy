import json,subprocess,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R));from review_probe import field,answer,save
# This import reruns deterministic preparation; package read-only and resulting inputs are identical.
def vals(r):return sorted(int(c[':answer/value']) for c in field(r)[':answer-field/choices'])
def cue(r):
 v=vals(r)
 return r['question'][':question/difficulty'].endswith('/easy') and (min(v)>0 or [v[i+1]-v[i] for i in range(4)]==[2,1,1,1])
def bank_strategy(r):
 v=vals(r)
 if cue(r):return v[1]
 return v[-2]
groups={};gradecases=[]
for stage,path in [('raw-easy','easy-samples.json'),('delivered-easy','delivery-easy/accepted.json'),('raw-moderate','moderate-samples.json'),('delivered-moderate','delivery-moderate/accepted.json'),('raw-batch','runner-batch.json'),('delivered-batch','delivery-batch/accepted.json')]:
 rs=json.load(open(R/path));ps={}
 for r in rs:ps.setdefault(r['generation']['profile'],[]).append(r)
 detail={'count':len(rs),'profile_counts':{p:len(rr) for p,rr in ps.items()},'answers':{str(a):sum(answer(r)==a for r in rs) for a in sorted(set(answer(r) for r in rs))},'probes':[]}
 if 'moderate' not in stage:
  subsets=[('easy all','overall',rs),('visible positive bank or initial two-unit gap','other_recognizable_subgroup',[r for r in rs if cue(r)])]+[(p,'within_template',rr) for p,rr in ps.items()]
  for label,scope,rr in subsets:
   if not rr:continue
   success=sum(bank_strategy(r)==answer(r) for r in rr)
   detail['probes'].append({'cue':'numeric answer-bank spacing and minimum','subgroup':stage+': '+label,'scope':scope,'strategy':'When bank is positive or has successive gaps 2,1,1,1 choose second-smallest; otherwise choose second-largest. Never read the matrix dimensions or basis.','correct':success,'total':len(rr),'baseline':0.2,'disposition':'defect' if success==len(rr) else 'not_predictive','conclusion':f'Bank-only strategy succeeds {success}/{len(rr)}; random selection baseline is 1/5. A perfect conditional bank predictor bypasses rank-nullity. Numeric order survives option shuffling.','sample_refs':[path,'shortcut-results.json']})
  for i,r in enumerate(rs):
   chosen=next(c for c in field(r)[':answer-field/choices'] if int(c[':answer/value'])==bank_strategy(r));gradecases.append({'label':stage+' bank-only '+str(i),'record':r,'checks':[{'submitted_answer_id':chosen[':answer/id'],'expected':'accepted' if bank_strategy(r)==answer(r) else 'rejected','purpose':'Bank-only strategy actual native result'}]})
 groups[stage]=detail
save('shortcut-results.json',groups);save('shortcut-grader-input.json',gradecases)
p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(R/'shortcut-grader-input.json'),str(R/'shortcut-grader-report.json')],capture_output=True,text=True);save('shortcut-grader-command.json',{'command':p.args,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
# Actual selection algorithm transcribed: single requested easy band, candidates fresh/usable.
# Initial selection of new batch separately from current captured inventory.
selection=[]
for stage,path in [('delivered-easy','delivery-easy/accepted.json'),('delivered-batch','delivery-batch/accepted.json')]:
 rs=json.load(open(R/path));picked=[]
 for t in range(32):
  seed='independent-review-selection-'+str(t);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);idx=int(u*len(rs));r=rs[idx];picked.append({'seed':seed,'index':idx,'question_id':r['question'][':question/id'],'cue':cue(r),'bank_only_correct':bank_strategy(r)==answer(r)})
 selection.append({'stage':stage,'records':path,'candidate_order':'stable input order, synthetic strictly increasing entity IDs; all candidates same difficulty; alternative entity-ID assignments change individual picks, not universal subgroup invariants','history':'fresh cohort, no prior questions; exclusion can remove candidates but cannot change a per-record bank invariant','draws':picked,'bank_only_correct':sum(x['bank_only_correct'] for x in picked),'total':len(picked)})
save('selection-checks.json',{'basis':5443,'implementation':'engine/rust/question_selection.rs select lines 128-204','limits':'No learner policy weights or learner histories captured; 32 test seeds are explicit single-band synthetic ordering checks, not a forecast of a real learner sequence. Existing captured inventory consists solely of original source questions.','selection':selection})
print(json.dumps({k:{'count':v['count'],'probes':[(p['subgroup'],p['correct'],p['total']) for p in v['probes']]} for k,v in groups.items()},indent=2));print(p.stdout)
