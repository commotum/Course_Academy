from review import *
import subprocess
records=[];results=[]
for template,strategy in [('harmonic_radio','smallest_nonzero_magnitude'),('exp_product_radio','smallest_nonzero_magnitude'),('exp_root_radio','largest_magnitude')]:
 for seed in range(93110,93118):
  r=g.generate(g.TEMPLATES[template][0],seed,template);records.append(r)
  f=r['question'][':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']];m=parse(key(r))
  predicted=min((v for v in vals if v!=0),key=lambda v:abs(float(v))) if strategy.startswith('smallest') else max(vals,key=lambda v:abs(float(v)))
  success=eq(predicted,m);results.append({'template':template,'seed':seed,'strategy':strategy,'correct':success,'question_id':r['question'][':question/id'],'predicted':str(predicted),'actual':str(m)})
  if not success:break
save('shortcut-followup-records.json',records);save('shortcut-followup-results.json',results)
# independently check every new record and invoke native grader in one batch
save('shortcut-followup-math.json',[mathcheck(r) for r in records]);cases=[]
for r in records:
 f=r['question'][':question/answer-fields'][0];cases.append({'label':'conditional cue counterexample '+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'check key and cue-breaking distractor'} for a in f[':answer-field/choices']]})
save('shortcut-followup-grader.json',cases)
p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(ROOT/'shortcut-followup-grader.json'),str(ROOT/'shortcut-followup-grader-results.json')],capture_output=True,text=True);print(p.stdout,p.stderr);print(json.dumps(results,indent=2))
