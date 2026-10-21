import json,pathlib,shutil,subprocess,sys,hashlib
import jsonschema
R=pathlib.Path(__file__).resolve().parent;J=R.parent;O=J/'review-1-policy-2-800c03f7bd804ec6';P=J/'workspace'
def load(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
# Re-run the previous independent minimal attack itself, not just the author's
# stronger same-bank invariant. Preserve failing and current records separately.
logs=[]
for name,target in [('failure1',O/'relocated'),('current',P)]:
 d=R/'exact-repro'/name;d.mkdir(parents=True,exist_ok=True)
 for f in ['minimal_repro.py','bank_shortcut.py']:shutil.copyfile(O/f,d/f)
 cp=subprocess.run(['/home/jake/Developer/Course_Academy/.venv/bin/python',str(d/'minimal_repro.py'),str(target)],capture_output=True,text=True)
 logs.append({'target':name,'command':['/home/jake/Developer/Course_Academy/.venv/bin/python',str(d/'minimal_repro.py'),str(target)],'exit':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,'records':str((d/'minimal-reproduction-records.json').relative_to(R))})
 assert cp.returncode==(1 if name=='failure1' else 0)
save(R/'exact-historical-counterexamples.json',logs)
schema=load(pathlib.Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'));v=load(R/'pedagogical-variation.json');jsonschema.validate(v,schema)
references=[]
def walk(o):
 if isinstance(o,dict):
  for k,value in o.items():
   if k in ('evidence_paths','sample_refs'):references.extend(value)
   else:walk(value)
 elif isinstance(o,list):
  for value in o:walk(value)
walk(v);result=load(R/'result.json');walk(result)
for p in references:
 path=R/p;assert not pathlib.Path(p).is_absolute() and path.is_file() and path.stat().st_size>0,p
assert result['verdict']=='accepted' and not result['findings'] and len(result['checks'])==8 and all(x['status']=='passed' for x in result['checks'].values())
before=load(R/'package-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert before==after
# Both retained finding IDs are in runner preflight and our execution logs.
preflight=load(J/'repair-preflight.json');reg=load(R/'retained-regression-verification.json')
assert len(preflight['finding_ids'])==2 and all(z['exit']==0 if z['target']=='current' else z['exit']!=0 for z in reg)
result['checks']['packaging']['evidence_paths'].append('exact-historical-counterexamples.json');save(R/'result.json',result)
save(R/'contract-check.json',{'pedagogical_schema_passed':True,'all_references_exist_nonempty':True,'checked_references':len(references),'eight_checks_passed':True,'package_unchanged':True,'exact_prior_attack_old_exit':logs[0]['exit'],'exact_prior_attack_current_exit':logs[1]['exit']})
print('Evidence schema/references verified; exact previous independent attack fails prior runtime and passes current; package unchanged.')
