#!/usr/bin/env python3
"""Small signed-domain boundary sample of each transformed solution shape."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,subprocess
import regression_checks as t
g=t.load();records=[]
for sid,d in [('q-73743','easy'),('q-42156','easy'),('q-130922','moderate'),('q-42160','moderate')]:
 for u,v in [(-1,-4),(1,4)]:
  r=g.generate(d,9947,sid,{'rhs_scale':v,'column_scale':u});assert t.witness.math_record(r)['pass'];records.append(r)
t.save('boundary-records.json',records)
cases=[]
for r in records:
 z=t.witness.math_record(r);cases.append({'label':r['generation']['template']+str(r['generation']['parameters']['rhs_scale']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if z['valid_choices'][i] else 'rejected','purpose':'independent exact boundary classification'} for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])]})
t.save('boundary-grader-input.json',cases)
repo=pathlib.Path('/home/jake/Developer/Course_Academy')
cmd=[str(repo/'generate/runs/current/check-engine'),str(t.OUT/'boundary-grader-input.json'),str(t.OUT/'boundary-grader-results.json')]
p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,p.stderr
t.save('boundary-grading-command.json',{'command':cmd,'returncode':p.returncode,'stdout':p.stdout})
print(json.dumps({'boundary_records':len(records),'independent_math_passed':True,'native_grading':p.stdout.strip()}))
