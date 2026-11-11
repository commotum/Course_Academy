"""Stage exact fresh publication survivors; no database writes."""
import json,os,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(H)]
from generator_publish import Publisher,jsonable,digest
from generator_packages import verify_package,check_dependencies
from generator_approval import approved_band
from generator_pipeline import source_identity
from generator_review import REVIEW_POLICY_VERSION
from generator_refill import validate_survivors
from generate.pipeline.check_delivery import audit
from independent_math import audit as check_math

def save(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def read(p):return json.loads(Path(p).read_text())
p=Publisher.from_environment(source=':agent/codex');summary=[];reps=[];cases=[]
for kp in [17592186096672,17592186096673]:
 D=H/str(kp);source=p.extract_source(kp,D/'source');inventory=read(D/'source/inventory.json');ref=source['registered_generator'][':question-generator/script'];package=p.config.math_root/ref;manifest=read(package.parent/'generator-package.json');sha=package.parent.name;verify_package(package.parent,sha);check_dependencies(manifest['dependencies'],sys.executable)
 identity={**source_identity(source),'package_sha256':sha,'registration':ref};approval=read(p.config.math_root/'generators/approvals'/sha/(str(kp)+'.json'))
 for band in ['easy','moderate','hard']:approved_band(approval,identity,band,REVIEW_POLICY_VERSION)
 save(D/'existing-approval.json',approval);save(D/'package.json',{'registration':ref,'package_sha256':sha,'identity':identity,'manifest':manifest})
 for b,band in enumerate(['easy','moderate','hard']):
  B=D/band;B.mkdir(parents=True,exist_ok=True);runtime=B/'runtime';runtime.mkdir(exist_ok=True)
  for name in manifest['files']:
   dest=runtime/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(package.parent/name,dest)
  for offset in range(20):
   seed=202611113+b+offset*13
   command=[sys.executable,'-E','-s','-B',str(runtime/'generator.py'),'--difficulty',band,'--count','10','--seed',str(seed),'--format','json']
   r=subprocess.run(command,cwd=runtime,check=True,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});raw=json.loads(r.stdout)
   duplicate=subprocess.run(command,cwd=runtime,check=True,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});assert json.loads(duplicate.stdout)==raw,'Nondeterministic generator'
   math=[check_math(x['question'],x['question'][':question/id']) for x in raw];assert not any(x['issues'] for x in math),math
   audit(raw,inventory,source,band,B/'candidate-delivery',runtime,p.config.math_root);accepted=read(B/'candidate-delivery/accepted.json')
   if len(accepted)>=5:break
  else:raise ValueError('No five unique candidates after bounded deduplication attempts')
  final=accepted[:5];audit(final,inventory,source,band,B/'delivery',runtime,p.config.math_root);final=read(B/'delivery/accepted.json');assert len(final)==5
  save(B/'records.json',final);save(B/'math.json',{'passed':True,'candidate_checks':math,'final_checks':[check_math(x['question'],x['question'][':question/id']) for x in final]});save(B/'sampling.json',{'seed':seed,'command':command,'count_raw':len(raw),'count_final':len(final),'deterministic':True})
  result=validate_survivors(final,inventory,B/'refill',root=package.parent,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=dict(os.environ),expected_plan=approval['verification_binding']['refill_plan']);assert result['status']=='passed'
  for x in final:
   f=x['question'][':question/answer-fields'][0];k=f[':answer-field/correct'];key=k[1] if isinstance(k,list) else k.get(':answer/id') if isinstance(k,dict) else k
   cases.append({'label':str(kp)+'/'+band+'/'+x['question'][':question/id'],'record':x,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','control':'canonical' if a[':answer/id']==key else 'wrong','purpose':'Independently solved entire system and tested all offered alternatives'} for a in f[':answer-field/choices']]})
  # One representative per actual endpoint/input family in this final batch.
  groups={}
  for x in final:
   m=check_math(x['question'],x['question'][':question/id']);groups.setdefault((m['input'],m['endpoint']),x)
  reps.extend(groups.values());summary.append({'kp':kp,'band':band,'fresh':5,'seed':seed,'package_sha256':sha,'refill_passed':True})
save(H/'native-input.json',cases);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True);save(H/'render-records.json',reps);save(H/'preflight.json',{'passed':True,'database_writes':0,'batches':summary,'total_fresh':30,'ui_representatives':len(reps)})
print(json.dumps(read(H/'preflight.json')),flush=True)
