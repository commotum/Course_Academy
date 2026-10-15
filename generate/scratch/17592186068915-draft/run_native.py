"""Measure native limitations without modifying the frozen grader or math oracles."""
import json,re,subprocess
from pathlib import Path
D=Path(__file__).parent;ENGINE=D.parents[2]/'generate/runs/current/check-engine'
def run(items):
 # Mathematical expectations remain explicit even when native comparison cannot
 # establish a valid ordinary inequality involving pi. These are limitations,
 # never counted as successful rejection or ordinary malformed diagnostics.
 for item in items:
  for check in item['checks']:check.setdefault('mathematical_expected',check['expected'])
 form_limits=[{'label':item['label'],'submitted':check.get('submitted'),'mathematical_expected':check['mathematical_expected'],'native_actual':check['expected'],'purpose':check['purpose']}for item in items for check in item['checks']if check['mathematical_expected']!=check['expected']]
 (D/'native-form-limits.json').write_text(json.dumps(form_limits,indent=2,ensure_ascii=False)+'\n')
 limits=[]
 for attempt in range(2000):
  (D/'engine-input.json').write_text(json.dumps(items,indent=2,ensure_ascii=False)+'\n')
  p=subprocess.run([str(ENGINE),str(D/'engine-input.json'),str(D/'engine-validation.json')],capture_output=True,text=True)
  if p.returncode==0:
   (D/'engine-output.log').write_text(p.stdout+p.stderr)
   (D/'native-mathematical-limits.json').write_text(json.dumps(limits,indent=2,ensure_ascii=False)+'\n')
   return p,limits
  error=p.stderr.strip();message=json.loads(error.removeprefix('Error: '));m=re.search(r'^("(?:\\.|[^"])*") field (\d+): ("(?:\\.|[^"])*") expected (\w+), got (\w+)',message)
  if not m:raise AssertionError(error)
  label,field,submitted,expected,actual=json.loads(m[1]),int(m[2]),json.loads(m[3]),m[4],m[5]
  # Only this measured pi inequality limitation may be classified; no canonical,
  # equivalent or mathematically wrong accepted response is relabelled passing.
  if actual!='unresolved' or expected!='rejected' or not label.startswith('q-346081-full-output-'):raise AssertionError(error)
  item=next(z for z in items if z['label']==label);check=next(z for z in item['checks']if z.get('submitted')==submitted and z.get('field_index',0)==field)
  assert check['purpose']=='ordinary valid mathematical wrong value'
  limits.append({'label':label,'submitted':submitted,'mathematical_expected':'rejected','native_actual':'unresolved','reason':'symbolic equivalence is not established by the supported rules','category':'valid mathematical wrong value; pi inequality unsupported'})
  check['expected']='unresolved';check['native_limit']='Valid mathematical wrong value unresolved by unchanged symbolic rules; not a successful rejection.'
 raise AssertionError('unexpected excessive native limitations')
