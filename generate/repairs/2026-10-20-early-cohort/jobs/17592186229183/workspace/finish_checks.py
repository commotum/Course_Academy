#!/usr/bin/env python3
"""Post-filter probes, native grading fixtures, renderer fixtures, relocation."""
import sys
sys.dont_write_bytecode=True
import json,subprocess,shutil,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R));from repair_checks import probes,measure,independent_numeric
E=R/'evidence'
def load(p):return json.loads(p.read_text())
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2)+'\n')
samples=load(E/'delivery-sample/accepted.json');batch=load(E/'delivery-batch/accepted.json')
pre=probes(load(E/'sample-records.json'));post=probes(samples)
assert pre==post
for r in batch:independent_numeric(r)
# Same easy band => native select's second digest draw picks a sorted pool index.
# Actual entity IDs/history unavailable. Assign hypothetical relative IDs only.
ordered=sorted(batch,key=lambda r:r['question'][':question/id'])
draws=[]
for i in range(32):
 digest=hashlib.sha256(('course-academy/question-selection/v1/repair-'+str(i)).encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 r=ordered[int(u*len(ordered))];draws.append(measure(r))
assert len({m['rank'] for m in draws})>1
save('delivery-selection-results.json',{'before':pre,'after':post,'batch':[measure(r) for r in batch],
 'conditional_easy_only_selection':{'draws':32,'ranks':sorted({m['rank'] for m in draws}),'positions':sorted({m['position'] for m in draws})},
 'generator_rejection':'Physical/arithmetic rejection occurs before bank construction, after rank draw. Adjacent positive gaps cannot collide. Whole shapes reject only nonpositive translated options while retaining selected rank; earlier key-radius rule removed.',
 'selection_limits':'Read-only native select math, all-easy fresh-candidate assumption and hypothetical sorted IDs. No actual live learner history, policy weights, publication IDs or database collisions are available. Historical stored affected questions remain unchanged and are listed separately.'})
cf=load(E/'counterfactual-records.json');mini=load(E/'radius-minimal-records.json');smoke=load(E/'band-smoke-records.json');same=load(E/'delivery-controls/accepted.json')[:5]
# Every normal template and all delivered batch choices; source key omissions not graded.
representatives=samples[::8]
raw=[r for r in load(E/'source-replay-records.json') if ':answer-field/correct' in r['question'][':question/answer-fields'][0]]
records=batch+cf+mini+representatives+smoke+raw+same
cases=[]
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 cases.append({'label':'complete radio bank '+str(i),'record':r,'checks':[
 {'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected',
 'purpose':'independent mass / source designation; all four selectable wrong values rejected'} for a in f[':answer-field/choices']]})
# Same logical answer is selected in invariant pairs; new answer in relevant pairs.
for i,r in enumerate(cf):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 cases.append({'label':'controlled physical/context pair '+str(i),'record':r,
 'checks':[{'submitted_answer_id':correct,'expected':'accepted','purpose':'capacity/initial mass change recomputes answer; common flow scaling/context preserve mass'}]})
cases+=load(E/'shortcut-grader-input.json')
save('grader-input.json',cases)
save('render-records.json',batch+mini+[same[0],same[-1]])
manifest=load(R/'package.json');dest=E/'relocated-package';dest.mkdir(exist_ok=True)
assert manifest['dependencies']=={'python':'3.13.5','packages':{'sympy':'1.14.0'}}
for f in manifest['files']+['package.json']:
 p=dest/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/f,p)
args=['--difficulty','easy','--seed','20261021','--count','5','--format','json']
cmd=[sys.executable,str(dest/manifest['entrypoint']),*args]
res=subprocess.run(cmd,cwd=E,capture_output=True,text=True);assert res.returncode==0,res.stderr
original=subprocess.run([sys.executable,str(R/manifest['entrypoint']),*args],cwd=E,capture_output=True,text=True);assert original.returncode==0
assert res.stdout==original.stdout
out=json.loads(res.stdout);assert out==load(E/'batch-records.json')
save('packaging-results.json',{'passed':True,'command':cmd,'relocated_records':len(out),'identical_original_output':True,'declared_files':manifest['files'],'dependencies':manifest['dependencies'],'runtime_sha256':{f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in manifest['files']},'assets':'No diagrams or generated assets; output directory not used.'})
print(json.dumps({'post_delivery_probes_passed':True,'grader_records':len(records),'grader_checks':sum(len(c['checks']) for c in cases),'render_records':8,'relocation_passed':True}))
