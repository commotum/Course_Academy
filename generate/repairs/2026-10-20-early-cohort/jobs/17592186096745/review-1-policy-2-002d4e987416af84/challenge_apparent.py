import json,pathlib,sys
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'))
import generator as g
from review_math import check,correct_index,matrices
probes=json.load(open(E/'decision-probe-results.json'))['probes'];targets=sorted({(p['subgroup'].split(':')[1],p['cue']) for p in probes if p['subgroup'].startswith('fresh_delivered:') and p['correct']==p['total'] and p['total']>1})
old=json.load(open(E.parent/'review-0-policy-2-5c66a489da337c4d/independent-samples.json'))+json.load(open(E/'supplemental-records.json'))
def choose(r,cue):
 vals=[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 if cue=='first authored option':return 0
 if cue=='shortest TeX':return min(range(5),key=lambda j:len(vals[j]))
 if cue=='most minus signs':return max(range(5),key=lambda j:vals[j].count('-'))
 return max(range(5),key=lambda j:sum(v==0 for v in matrices(vals[j])[0]))
records=[];results=[]
for profile,cue in targets:
 candidates=[r for r in old if r['generation']['template']==profile]
 found=next((r for r in candidates if choose(r,cue)!=correct_index(r['question'])),None)
 if found is not None:r=g.generate(template=profile,seed=found['generation']['seed'])
 else:
  for j in range(10):
   r=g.generate(template=profile,seed=3921871+99991*j)
   if choose(r,cue)!=correct_index(r['question']):break
  else:raise AssertionError((profile,cue,'no counterexample'))
 assert choose(r,cue)!=correct_index(r['question']);assert not check(r)['errors']
 if r not in records:records.append(r)
 results.append({'profile':profile,'cue':cue,'seed':r['generation']['seed'],'predicted_index':choose(r,cue),'correct_index':correct_index(r['question']),'id':r['question'][':question/id'],'conclusion':'Reproducible counterexample to apparent two-sample predictor; ordinary seeded generation, not an adversarial override.'})
(E/'apparent-cue-counterexamples.json').write_text(json.dumps(records,indent=2));(E/'apparent-cue-results.json').write_text(json.dumps({'command':f'{sys.executable} challenge_apparent.py','results':results,'math':[check(r) for r in records]},indent=2,default=str))
cases=json.load(open(E/'grader-all-input.json'))
for r in records:
 q=r['question'];idx=correct_index(q);cases.append({'label':'apparent-cue-counterexample:'+q[':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'Counterexample to a superficially perfect conditional cue'} for j,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices'])]})
(E/'grader-final-input.json').write_text(json.dumps(cases,indent=2));print(json.dumps({'apparent_cues_challenged':len(results),'counterexample_records':len(records),'grader_cases':len(cases)}))
