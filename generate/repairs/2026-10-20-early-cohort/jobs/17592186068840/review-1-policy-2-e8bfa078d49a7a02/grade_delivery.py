"""Extend independent grading with actual normalized delivery and inventory cue.
Run after review_checks.py and delivery_variation.py; single final native batch.
"""
import json,pathlib,subprocess
E=pathlib.Path(__file__).resolve().parent;R=pathlib.Path('/home/jake/Developer/Course_Academy')
cases=json.loads((E/'grader-input.json').read_text())
for label,name in [('delivery-independent','delivery-independent/accepted.json'),('delivery-batch','delivery-batch/accepted.json')]:
 for i,r in enumerate(json.loads((E/name).read_text())):
  f=r['question'][':question/answer-fields'][0]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual normalized delivery choice'} for a in f[':answer-field/choices']]
  cases.append({'label':label+' '+str(i),'record':r,'checks':checks})
for r in json.loads((E/'generated-records.json').read_text()):
 if r['generation']['template']!='reciprocal_cube':continue
 f=r['question'][':question/answer-fields'][0];choices=[a for a in f[':answer-field/choices'] if 'C +' in a[':answer/value'] and '^{2}' in a[':answer/value'] and a[':answer/value'].startswith(r'y=\sqrt[3]{C +')];assert len(choices)==1
 cases.append({'label':'historical inventory shortcut','record':r,'checks':[{'submitted_answer_id':choices[0][':answer/id'],'expected':'accepted','purpose':'reproduced historical shape cue'}]})
(E/'grader-final-input.json').write_text(json.dumps(cases,indent=2))
command=[str(R/'generate/runs/current/check-engine'),str(E/'grader-final-input.json'),str(E/'grader-final-results.json')]
p=subprocess.run(command,capture_output=True,text=True);(E/'grader-final-execution.json').write_text(json.dumps({'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2));print(p.stdout,p.stderr);raise SystemExit(p.returncode)
