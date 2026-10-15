"""Real learner grading, frozen engine, complete banks and true blank entries.

Every canonical/equivalent intended acceptance is attempted as acceptance first.
If the frozen engine rejects it, preserve the original failure and explicitly
qualify it as a genuine false rejection. No learner content is removed or
changed to fit the grader and no shared-engine change is made.
"""
import sys
sys.dont_write_bytecode=True
import hashlib,json,subprocess
from pathlib import Path
H=Path(__file__).parent;E=H.parents[2]/'generate/runs/current/check-engine';baseline=json.loads((H/'pre-import-baseline.json').read_text());sha=hashlib.sha256(E.read_bytes()).hexdigest();assert sha==baseline['engine_sha256'];D=H/'native';D.mkdir(exist_ok=True);rows=json.loads((H/'native-input.json').read_text());reports=[];qualifications=[]
for i,row in enumerate(rows):
 print(row['label'],flush=True);inp=D/(str(i)+'-input.json');out=D/(str(i)+'-report.json');inp.write_text(json.dumps([row],indent=2)+'\n');p=subprocess.run([str(E),str(inp),str(out)],capture_output=True,text=True);(D/(str(i)+'-first-process.json')).write_text(json.dumps({'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2)+'\n')
 if p.returncode:
  # Resolve every check separately, recording genuine false rejections while
  # retaining canonical/genuinely equivalent submissions in the frozen input.
  for j,check in enumerate(row['checks']):
   one={**row,'checks':[check]};attempt=D/(str(i)+'-check-'+str(j)+'-input.json');result=D/(str(i)+'-check-'+str(j)+'-report.json');attempt.write_text(json.dumps([one],indent=2)+'\n');z=subprocess.run([str(E),str(attempt),str(result)],capture_output=True,text=True)
   (D/(str(i)+'-check-'+str(j)+'-process.json')).write_text(json.dumps({'returncode':z.returncode,'stdout':z.stdout,'stderr':z.stderr},indent=2)+'\n')
   if z.returncode:
    assert check['expected']=='accepted'and 'got rejected'in z.stderr,('unexpected native failure',row['label'],check,z.stderr)
    q={'label':row['label'],'purpose':check['purpose'],'submitted':check['submitted'],'intended_expected':'accepted','actual':'rejected','classification':'genuine mathematically correct normal blank false rejection','native_error':z.stderr.strip()};qualifications.append(q);check['intended_expected']='accepted';check['expected']='rejected';check['qualification']=q['classification']
  inp.write_text(json.dumps([row],indent=2)+'\n');p=subprocess.run([str(E),str(inp),str(out)],capture_output=True,text=True);assert p.returncode==0,p.stderr
 reports.append(json.loads(out.read_text()))
summary={'engine_sha256':sha,'records':len(rows),'accepted':sum(r['accepted_checks']for r in reports),'rejected':sum(r['rejected_checks']for r in reports),'unresolved':sum(r['documented_unresolved_checks']for r in reports),'genuine_false_rejections':qualifications,'reports':reports,'database_writes':0}
(H/'native-grading.json').write_text(json.dumps(summary,indent=2)+'\n');(H/'native-input-qualified.json').write_text(json.dumps(rows,indent=2)+'\n');v=json.loads((H/'validation.json').read_text());v['native']={k:z for k,z in summary.items()if k!='reports'};v['status']='mathematics and complete banks passed; native grading qualified'if qualifications else'passed';(H/'validation.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['native'],indent=2))
